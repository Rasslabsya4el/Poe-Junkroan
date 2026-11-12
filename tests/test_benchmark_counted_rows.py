"""Shared benchmark-row counting, reports, and comparison summaries without PoB."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import benchmark  # noqa: E402

from benchmark import main as benchmark_main, render_report, rereport  # noqa: E402
from compare_runs import main as compare_main, summarize  # noqa: E402
from junkroan.optimizer.benchmark_rows import audit_finding_parts, counted_row  # noqa: E402


def rows() -> list[dict]:
    return json.loads((ROOT / "tests" / "fixtures" / "benchmark_counted_rows.json").read_text(encoding="utf-8"))


def full_row(slug: str, seed: int, ratio: float, **extra) -> dict:
    row = {
        "ok": True,
        "slug": slug,
        "seed": seed,
        "ratio_lane": ratio,
        "ratio_raw": ratio,
        "author_raw": 1000.0,
        "author_lane": 1000.0,
        "ours": 1000.0 * ratio,
        "author_life": 100.0,
        "ours_life": 100.0,
        "author_ehp": 100.0,
        "ours_ehp": 100.0,
        "author_maxhit": 100.0,
        "ours_maxhit": 100.0,
        "ours_ramp": None,
        "keystones": [],
        "audit": [],
        "audit_errors": 0,
        "fixed_point_gain": 0.0,
        "stages": [{"name": "final", "value": 1000.0, "violation": 0.0}],
    }
    row.update(extra)
    return row


def test_fixture_reproduces_fixed_point_medians_and_median_of_medians() -> None:
    summary = summarize(rows())

    assert {slug: value["median"] for slug, value in summary.items()} == {
        "bleed_bow": 141.4,
        "burning_arrow_snipe": 179.7,
        "cold_dot": 112.4,
        "impale_ballista": 92.4,
        "stormbrand": 169.4,
        "summon_raging_spirits": 158.9,
    }
    assert summary["burning_arrow_snipe"]["seeds"] == 3
    assert summary["burning_arrow_snipe"]["audit_errors"] == 1
    assert statistics.median(value["median"] for value in summary.values()) == 150.15


def test_counted_row_uses_finding_string_check_name_and_rejects_the_other_edges() -> None:
    fixed_point = rows()[3]
    assert audit_finding_parts(fixed_point["audit"][0]) == ("error", "fixed point")
    assert counted_row(fixed_point)

    assert not counted_row(full_row("infeasible", 1, 1.0, stages=[{"name": "final", "violation": 0.2}]))
    assert not counted_row(full_row("mod_error", 1, 1.0, audit=["[error] mod family: impossible prefixes"], audit_errors=1))
    assert not counted_row({"ok": False, "slug": "failed", "seed": 1, "stages": [{"violation": 0.0}]})


def test_violation_tolerance_counts_its_boundary_and_excludes_any_larger_value() -> None:
    boundary = full_row("boundary", 1, 1.0, stages=[{"name": "final", "violation": 1e-9}])
    over_boundary = full_row("over_boundary", 1, 1.0, stages=[{"name": "final", "violation": 1e-9 + 1e-15}])

    assert counted_row(boundary)
    assert not counted_row(over_boundary)


def test_legacy_rows_with_only_audit_error_count_preserve_the_old_clean_behavior() -> None:
    clean = full_row("legacy_clean", 1, 1.0)
    dirty = full_row("legacy_dirty", 1, 1.0, audit_errors=1)
    clean.pop("audit")
    dirty.pop("audit")

    assert counted_row(clean)
    assert not counted_row(dirty)


def test_even_count_uses_statistics_median_and_compare_reports_not_counted() -> None:
    data = [full_row("two_rows", 1, 0.80), full_row("two_rows", 2, 0.92)]
    data.append(full_row("two_rows", 3, 1.20, audit=["[error] mod family: impossible prefixes"], audit_errors=1))
    result = summarize(data)["two_rows"]
    report = render_report(data, stamp="fixture")

    assert result["median"] == 86.0
    assert result["not_counted"] == 1
    assert result["audit_errors"] == 1
    assert "| two_rows | 2 | 86% | 80% | 92% |" in report


def test_report_labels_only_real_infeasibility_or_non_fixed_point_errors_and_keeps_fixed_point_value() -> None:
    fixed = full_row("fixed", 1, 1.20, audit=["[error] fixed point: one more pass gained +2.8%"], audit_errors=1, fixed_point_gain=0.028)
    infeasible = full_row("infeasible", 1, 0.90, stages=[{"name": "final", "value": 900.0, "violation": 0.2}])
    error = full_row("error", 1, 0.80, audit=["[error] mod family: impossible prefixes"], audit_errors=1)
    failed = {"ok": False, "slug": "failed", "seed": 1, "error": "RuntimeError: boom"}

    report = render_report([fixed, infeasible, error, failed], stamp="fixture")

    assert "| fixed s1 |" in report and "| +2.8% |" in report
    assert "fixed s1 (audit error, not counted)" not in report
    assert "infeasible s1 (infeasible, not counted)" in report
    assert "error s1 (audit error, not counted)" in report
    assert "| failed s1 | FAILED: RuntimeError: boom" in report
    assert "not at a fixed point (> 1%): 1 of 3 builds" in report


def test_fixed_point_summary_is_strictly_greater_than_one_percent() -> None:
    exactly_one_percent = full_row("exactly_one", 1, 1.0, fixed_point_gain=0.01, audit=["[error] fixed point: one more pass gained +1.0%"], audit_errors=1)
    above_one_percent = full_row("above_one", 1, 1.0, fixed_point_gain=0.01 + 1e-15, audit=["[error] fixed point: one more pass gained +1.0%"], audit_errors=1)

    report = render_report([exactly_one_percent, above_one_percent], stamp="fixture")

    assert "not at a fixed point (> 1%): 1 of 2 builds" in report


def test_rereport_rewrites_only_median_tables_when_minimal_results_lack_row_fields(tmp_path: Path, monkeypatch, capsys) -> None:
    run = tmp_path / "20260918-1526-gear-loot"
    run.mkdir()
    (run / "results.json").write_text(json.dumps(rows()), encoding="utf-8")
    (run / "report.md").write_text("old report", encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["benchmark.py", "--rereport", str(run)])
    assert benchmark_main() == 0
    path = run / "report.md"
    report = path.read_text(encoding="utf-8")

    assert path == run / "report.md"
    assert f"report: {path}" in capsys.readouterr().out
    assert "old report" not in report
    assert "lack fields needed for the per-build table: author_raw" in report
    assert "rewritten median tables only" in report
    assert "| burning_arrow_snipe | 3 | 180% | 137% | 184% |" in report
    assert "per-reference medians, ours / author (our lane): median 150%" in report
    assert "not at a fixed point (> 1%): 3 of 18 builds" in report
    assert "| build | author" not in report


def test_rereport_tag_resolves_the_newest_matching_run(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "repo"
    older = root / "artifacts" / "benchmark" / "20260918-1200-replay"
    newer = root / "artifacts" / "benchmark" / "20260918-1300-replay"
    older.mkdir(parents=True)
    newer.mkdir()
    monkeypatch.setattr(benchmark, "ROOT", root)

    assert benchmark._resolve_run("replay") == newer


def test_compare_output_retains_audit_errors_and_adds_not_counted(tmp_path: Path, monkeypatch, capsys) -> None:
    control, candidate = tmp_path / "control", tmp_path / "candidate"
    control.mkdir()
    candidate.mkdir()
    control_rows = [full_row("spark", 1, 1.20, audit=["[error] fixed point: one more pass gained +2.0%"], audit_errors=1)]
    candidate_rows = [
        full_row("spark", 1, 1.30),
        full_row("spark", 2, 1.10, audit=["[error] mod family: impossible prefixes"], audit_errors=1),
    ]
    (control / "results.json").write_text(json.dumps(control_rows), encoding="utf-8")
    (candidate / "results.json").write_text(json.dumps(candidate_rows), encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["compare_runs.py", str(control), str(candidate), "--min-delta", "-100"])
    assert compare_main() == 0

    output = capsys.readouterr().out
    assert "| audit errors A/B | not counted A/B |" in output
    assert "| spark | 1 | 120.0 | n/a | 1 | 130.0 | n/a | 10.0 | 1/1 | 0/1 |" in output


def test_the_verdict_uses_only_references_counted_on_both_sides(tmp_path: Path, monkeypatch, capsys) -> None:
    control, candidate = tmp_path / "control", tmp_path / "candidate"
    control.mkdir()
    candidate.mkdir()
    # control counts a low reference the candidate lost: alone it would lift the candidate's median
    control_rows = [full_row("spark", 1, 1.20), full_row("arc", 1, 1.10), full_row("low", 1, 0.40)]
    candidate_rows = [full_row("spark", 1, 1.18), full_row("arc", 1, 1.08)]
    (control / "results.json").write_text(json.dumps(control_rows), encoding="utf-8")
    (candidate / "results.json").write_text(json.dumps(candidate_rows), encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["compare_runs.py", str(control), str(candidate), "--min-delta", "0"])
    assert compare_main() == 1  # -2.0 on the common two; the own-set medians (110.0 vs 113.0) would say PASS

    output = capsys.readouterr().out
    assert "counted in control only (left out of the verdict): low" in output
    assert "over the 2 common references: control 115.0, candidate 113.0, delta -2.0" in output


def test_report_loop_stop_cell_is_the_plain_stop_reason() -> None:
    rows = [full_row("converged", 1, 1.0, loop_stop="converged"), full_row("timed", 1, 1.0, loop_stop="time")]

    report = render_report(rows, stamp="fixture")
    row_lines = {line.split("|")[1].strip(): line for line in report.splitlines() if line.startswith("| ")}

    assert row_lines["converged s1"].rstrip("|").rstrip().endswith("converged")
    assert row_lines["timed s1"].rstrip("|").rstrip().endswith("time")
    assert "time*" not in report
