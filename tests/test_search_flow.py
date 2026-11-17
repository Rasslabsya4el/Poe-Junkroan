"""#16: the search's stages driven without PoB, by a scripted "build one skeleton".

The scripted builder answers every worker call from a table (value per ascendancy and seed, crashes on demand), so
each rule of `junkroan.search.flow` is checked on numbers chosen to separate it: which skeletons go to the full
round, which seed is delivered, which mutation variant earns a full build, the delivered order, and what the report
and the exit code say when a screen or a seed crashed.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from junkroan.optimizer.build_result import BuildResult, StageRecord
from junkroan.search.flow import (EXIT_LOST_BUILD, EXIT_OK, Job, OutputPaths, SearchOptions, choose_finalists, final_order, output_paths, run,
                                  screen_order, variant_floor)
from junkroan.search.result import BuildRecord
from junkroan.search.skeleton import Skeleton

STAMP = time.strptime("2026-11-14 1200", "%Y-%m-%d %H%M")


def _record(value: float, **over: Any) -> dict:
    rec = BuildRecord(final={"Life": 4000, "TotalEHP": 20000, "EffectiveMovementSpeedMod": 1.3}, optimistic=value * 1.2, optimistic_stats={}, import_code=f"CODE-{value:.0f}",
                      xml="<PathOfBuilding/>", summary=f"summary {value:.0f}", explanation="", keystones=[], floors_missed=[])
    data = rec.to_json()
    data.update(over)
    return data


class ScriptedBuilder:
    """`Builder` without PoB. `screen[asc]` and `full[(asc, seed)]` give the values; `crash` holds ("screen", asc) or
    ("full", asc, seed) keys that answer like a crashed worker; `uniques[asc]` is the unique screen's list."""

    def __init__(self, *, screen: dict[str, float], full: dict[tuple[str, int], float], crash: set = frozenset(), uniques: dict[str, list] | None = None,
                 variant_screen: dict[str, float] | None = None, full_over: dict[str, dict] | None = None) -> None:
        self.screen, self.full, self.crash = screen, full, set(crash)
        self.uniques = uniques or {}
        self.variant_screen = variant_screen or {}
        self.full_over = full_over or {}
        self.calls: list[tuple[str, str, int | None]] = []

    def composition(self, skill, rails):  # pragma: no cover - the tests send no request that probes
        raise AssertionError("no composition probe expected")

    def rig_supports(self, rig, rails, log):
        self.calls.append(("rig", rig.ascendancy, None))
        return ["Added Lightning Damage Support"]

    def _crashed(self, *key) -> dict:
        return {"ok": False, "error": f"RuntimeError: scripted crash {key}", "considered": {}}

    def run(self, jobs: list[Job], workers: int):
        for job in jobs:
            sk = job.skeleton
            asc = sk.ascendancy
            if job.kind == "prepare":
                self.calls.append(("prepare", asc, None))
                if ("prepare", asc) in self.crash:
                    yield job, self._crashed("prepare", asc)
                    continue
                yield job, {"ok": True, "skeleton": sk.to_json(), "picks": [], "rig": {"value": 1.0, "violation": 0.0, "feasible": True}, "seconds": 1.0, "considered": {}}
                continue
            seed = job.kwargs.get("seed", 1)
            if job.kwargs["screen"]:
                variant = job.tag in self.variant_screen
                self.calls.append(("variant screen" if variant else "screen", job.tag or asc, seed if variant else None))
                if ("screen", asc) in self.crash and not variant:
                    yield job, self._crashed("screen", asc)
                    continue
                value = self.variant_screen[job.tag] if variant else self.screen[asc]
                yield job, {"ok": True, "skeleton": sk.to_json(), "screen": True, "seed": seed, "value": value, "violation": 0.0, "feasible": True,
                            **_record(value), "uniques": [] if variant else self.uniques.get(asc, []), "seconds": 60.0, "considered": {}}
                continue
            self.calls.append(("full", job.tag, seed))
            if ("full", asc, seed) in self.crash:
                yield job, self._crashed("full", asc, seed)
                continue
            key = "mut" if "-mut" in job.tag else asc
            value = self.full[(key, seed)]
            over = dict(self.full_over.get(job.tag, {}))
            feasible = over.pop("feasible", True)
            violation = over.pop("violation", 0.0)
            yield job, {"ok": True, "skeleton": sk.to_json(), "screen": False, "seed": seed, "value": value, "violation": violation, "feasible": feasible,
                        **_record(value, **over), "uniques": self.uniques.get(asc, []), "seconds": 600.0, "considered": {}}


def _paths(tmp_path: Path) -> OutputPaths:
    return output_paths("Storm Brand", now=STAMP, env={"OUT_DIR": str(tmp_path / "out")})


def _run(tmp_path: Path, builder: ScriptedBuilder, **opts: Any):
    options = SearchOptions(skill="Storm Brand", ascendancies=["Inquisitor", "Hierophant", "Elementalist"], workers=1, **opts)
    lines: list[str] = []
    outcome = run(options, builder, paths=_paths(tmp_path), print_fn=lines.append, keystone_name=lambda node: None, commit="test")
    return outcome, lines


SCREEN = {"Inquisitor": 300.0, "Hierophant": 200.0, "Elementalist": 100.0}


# -- finalist choice ---------------------------------------------------------------------------------


def test_the_screen_top_goes_to_the_full_round_and_a_strong_unique_adds_its_variant():
    screened = screen_order([{"skeleton": Skeleton(class_name="Templar", ascendancy=a, main_link=["Storm Brand"]).to_json(), "value": v, "violation": vi,
                              "uniques": [{"slot": "Body Armour", "name": "Hyrri's Ire", "gain": g}]}
                             for a, v, vi, g in (("Elementalist", 100.0, 0.0, 0.5), ("Inquisitor", 300.0, 0.0, 0.05), ("Hierophant", 300.0, 0.2, 0.25))])
    assert [Skeleton.from_json(r["skeleton"]).ascendancy for r in screened] == ["Inquisitor", "Hierophant", "Elementalist"]  # value, then the smaller violation
    fin = choose_finalists(screened, top=2, full_ranks=None, unique_variants=True, min_gain=0.10, max_uniques=2)
    # Inquisitor's unique gains 5 % (< 10 %): no variant; Hierophant's 25 %: its variant follows it; Elementalist is rank 3
    assert [(sk.ascendancy, dict(sk.uniques)) for sk in fin.skeletons] == [("Inquisitor", {}), ("Hierophant", {}), ("Hierophant", {"Body Armour": "Hyrri's Ire"})]
    assert [tag for _sk, tag, _sd in fin.batch()] == ["Inquisitor-0", "Hierophant-1", "Hierophant-2"]
    ranks = choose_finalists(screened, top=1, full_ranks=[3, 1], unique_variants=False, min_gain=0.10, max_uniques=2)
    assert [tag for _sk, tag, _sd in ranks.batch()] == ["screen-3", "screen-1"]  # exactly the ranks asked for, in the order asked


# -- best of seeds -----------------------------------------------------------------------------------


def test_every_finalist_is_built_per_seed_and_the_best_seed_is_delivered(tmp_path):
    full = {("Inquisitor", 1): 1000.0, ("Inquisitor", 2): 1500.0, ("Inquisitor", 3): 1200.0, ("Hierophant", 1): 900.0, ("Hierophant", 2): 800.0, ("Hierophant", 3): 700.0}
    b = ScriptedBuilder(screen=SCREEN, full=full)
    outcome, _ = _run(tmp_path, b, top=2, seeds=3, no_unique_variants=True, no_mutation=True)
    assert outcome.exit_code == EXIT_OK and not outcome.failures
    assert sorted(c for c in b.calls if c[0] == "full") == sorted(("full", f"{a}-{i}", s) for i, a in enumerate(("Inquisitor", "Hierophant")) for s in (1, 2, 3))
    assert [(r["tag"], r["seed"], r["value"]) for r in outcome.builds] == [("Inquisitor-0", 2, 1500.0), ("Hierophant-1", 1, 900.0)]
    run_dir = outcome.paths.run_dir
    assert sorted(p.name for p in run_dir.glob("01 *.pob.txt")) == ["01 templar_inquisitor-s1.pob.txt", "01 templar_inquisitor-s3.pob.txt", "01 templar_inquisitor.pob.txt"]


# -- the variant keep rule -------------------------------------------------------------------------------


def test_a_mutation_variant_is_built_in_full_only_when_its_screen_reaches_half_the_finalists_screen(tmp_path):
    uniques = {"Inquisitor": [{"slot": "Body Armour", "name": "Hyrri's Ire", "gain": 0.3}], "Hierophant": [{"slot": "Helmet", "name": "Crown of Eyes", "gain": 0.3}]}
    full = {("Inquisitor", 1): 1000.0, ("Hierophant", 1): 900.0, ("mut", 1): 1100.0}
    # the floor is half of the best top-2 screen: 0.5 * 300 = 150; the first variant screens at 151, the second at 149
    b = ScriptedBuilder(screen=SCREEN, full=full, uniques=uniques, variant_screen={"Inquisitor-mut0": 151.0, "Hierophant-mut1": 149.0})
    outcome, lines = _run(tmp_path, b, top=2, seeds=1, no_unique_variants=True)
    assert variant_floor([{"value": 300.0}, {"value": 200.0}, {"value": 1000.0}], 2) == 150.0
    assert ("variant screen", "Inquisitor-mut0", 1) in b.calls and ("variant screen", "Hierophant-mut1", 1) in b.calls
    assert [c for c in b.calls if c[0] == "full" and "mut" in c[1]] == [("full", "Inquisitor-mut0", 1)]
    assert [r["tag"] for r in outcome.builds] == ["Inquisitor-mut0", "Inquisitor-0", "Hierophant-1"]
    assert any("Hierophant-mut1: 149" in line and "dropped" in line for line in lines)


# -- the final order -------------------------------------------------------------------------------


def test_the_delivered_order_sinks_audit_errors_then_infeasible_then_value():
    rows = [{"tag": "a", "audit_errors": 1, "feasible": True, "violation": 0.0, "value": 9000.0},
            {"tag": "b", "audit_errors": 0, "feasible": False, "violation": 0.1, "value": 8000.0},
            {"tag": "c", "audit_errors": 0, "feasible": True, "violation": 0.0, "value": 1000.0},
            {"tag": "d", "audit_errors": 0, "feasible": True, "violation": 0.0, "value": 2000.0},
            {"tag": "e", "audit_errors": 0, "feasible": False, "violation": 0.05, "value": 100.0}]
    assert [r["tag"] for r in final_order(rows)] == ["d", "c", "e", "b", "a"]


def test_the_report_ranks_builds_in_the_delivered_order(tmp_path):
    full = {("Inquisitor", 1): 1000.0, ("Hierophant", 1): 2000.0, ("Elementalist", 1): 3000.0}
    over = {"Elementalist-2": {"audit": ["error: x"], "audit_errors": 1}, "Hierophant-1": {"feasible": False, "violation": 0.1}}
    outcome, _ = _run(tmp_path, ScriptedBuilder(screen=SCREEN, full=full, full_over=over), top=3, seeds=1, no_unique_variants=True, no_mutation=True)
    assert [r["tag"] for r in outcome.builds] == ["Inquisitor-0", "Hierophant-1", "Elementalist-2"]
    report = (outcome.paths.run_dir / "report.md").read_text(encoding="utf-8")
    lines = report.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("| rank | build |"))
    ranked = lines[head + 2:head + 5]
    assert [line.split("|")[2].strip() for line in ranked] == ["Templar/Inquisitor", "Templar/Hierophant", "Witch/Elementalist"]
    assert [line.split("|")[3].strip() for line in ranked] == ["1,000", "2,000", "3,000"]
    assert sorted(p.name for p in outcome.paths.run_dir.glob("*.pob.txt")) == ["01 templar_inquisitor.pob.txt", "02 templar_hierophant.pob.txt", "03 witch_elementalist.pob.txt"]


# -- failures: named first, a lost finalist fails the run --------------------------------------------


def test_a_crashed_screen_and_a_crashed_seed_open_the_report_and_the_run_still_delivers(tmp_path):
    full = {("Inquisitor", 1): 1000.0, ("Inquisitor", 2): 1100.0, ("Hierophant", 1): 900.0, ("Hierophant", 2): 950.0}
    b = ScriptedBuilder(screen=SCREEN, full=full, crash={("screen", "Elementalist"), ("full", "Inquisitor", 2)})
    outcome, _ = _run(tmp_path, b, top=2, seeds=2, no_unique_variants=True, no_mutation=True)
    assert outcome.exit_code == EXIT_OK  # every finalist kept a seed
    assert [(f.stage, f.what, f.seed) for f in outcome.failures] == [("screen", "Witch/Elementalist", None), ("full", "Inquisitor-0", 2)]
    report = (outcome.paths.run_dir / "report.md").read_text(encoding="utf-8").splitlines()
    assert report[0] == "# Search: Storm Brand"
    assert report[2].startswith("**FAILED: 2 job(s) crashed**")
    assert "screen failed Witch/Elementalist" in report[3] and "scripted crash" in report[3]
    assert "full failed Inquisitor-0 seed 2" in report[4]
    assert [(r["tag"], r["seed"]) for r in outcome.builds] == [("Inquisitor-0", 1), ("Hierophant-1", 2)]


def test_a_finalist_with_no_surviving_seed_fails_the_run(tmp_path):
    full = {("Inquisitor", 1): 1000.0, ("Hierophant", 1): 900.0}
    b = ScriptedBuilder(screen=SCREEN, full=full, crash={("full", "Hierophant", 1)})
    outcome, lines = _run(tmp_path, b, top=2, seeds=1, no_unique_variants=True, no_mutation=True)
    assert outcome.exit_code == EXIT_LOST_BUILD
    assert outcome.lost == ["Hierophant-1"]
    report = (outcome.paths.run_dir / "report.md").read_text(encoding="utf-8").splitlines()
    assert report[2] == "**FAILED: 1 job(s) crashed; 1 finalist(s) lost every seed: Hierophant-1**"
    assert "full failed Hierophant-1 seed 1: RuntimeError" in report[3]
    assert any(line.startswith("**FAILED") for line in lines)  # the console says it too, at the end


def test_a_search_where_every_screen_crashed_delivers_nothing_and_fails(tmp_path):
    b = ScriptedBuilder(screen=SCREEN, full={}, crash={("screen", a) for a in SCREEN})
    outcome, _ = _run(tmp_path, b, top=2, seeds=1, no_unique_variants=True, no_mutation=True)
    assert outcome.exit_code == EXIT_LOST_BUILD and outcome.builds == [] and len(outcome.failures) == 3


def test_a_crashed_prepare_is_named_and_the_others_go_on(tmp_path):
    full = {("Inquisitor", 1): 1000.0, ("Hierophant", 1): 900.0}
    b = ScriptedBuilder(screen=SCREEN, full=full, crash={("prepare", "Elementalist")})
    outcome, _ = _run(tmp_path, b, top=2, seeds=1, no_unique_variants=True, no_mutation=True)
    assert outcome.exit_code == EXIT_OK and [(f.stage, f.what) for f in outcome.failures] == [("prepare", "Witch/Elementalist")]
    assert not any(c[0] == "screen" and c[1] == "Elementalist" for c in b.calls)
    assert "prepare failed Witch/Elementalist" in outcome.report[3]


def test_a_crashed_mutation_variant_is_named_but_does_not_fail_the_run(tmp_path):
    uniques = {"Inquisitor": [{"slot": "Body Armour", "name": "Hyrri's Ire", "gain": 0.3}]}
    full = {("Inquisitor", 1): 1000.0, ("Hierophant", 1): 900.0, ("mut", 1): 1100.0}  # the variant's value, replaced by the crash below
    b = ScriptedBuilder(screen=SCREEN, full=full, uniques=uniques, variant_screen={"Inquisitor-mut0": 200.0})
    original = b.run

    def run_with_variant_crash(jobs, workers):
        for job, res in original(jobs, workers):
            if job.tag == "Inquisitor-mut0" and not job.kwargs["screen"]:
                res = {"ok": False, "error": "RuntimeError: scripted variant crash", "considered": {}}
            yield job, res

    b.run = run_with_variant_crash
    outcome, _ = _run(tmp_path, b, top=2, seeds=1, no_unique_variants=True)
    assert outcome.exit_code == EXIT_OK and outcome.lost == []
    assert [(f.stage, f.what, f.seed) for f in outcome.failures] == [("full", "Inquisitor-mut0", 1)]
    assert outcome.report[2] == "**FAILED: 1 job(s) crashed**"
    assert [r["tag"] for r in outcome.builds] == ["Inquisitor-0", "Hierophant-1"]


# -- output under $OUT_DIR, nothing outside -------------------------------------------------------------


def test_output_goes_under_out_dir_when_it_is_set_else_artifacts(tmp_path):
    with_env = output_paths("Storm Brand", now=STAMP, env={"OUT_DIR": str(tmp_path)})
    assert with_env.run_dir == tmp_path / "search-storm_brand" / "20261114-1200"
    assert with_env.logs == tmp_path / "search-storm_brand" / "logs"
    without = output_paths("Storm Brand", now=STAMP, env={}, repo=tmp_path / "repo")
    assert without.run_dir == tmp_path / "repo" / "artifacts" / "search-storm_brand" / "20261114-1200"


def test_a_run_writes_only_under_its_output_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    full = {("Inquisitor", 1): 1000.0}
    outcome, _ = _run(tmp_path, ScriptedBuilder(screen=SCREEN, full=full), top=1, seeds=1, no_unique_variants=True, no_mutation=True, trace_out=str(tmp_path / "out" / "trace.json"))
    written = sorted(str(p.relative_to(tmp_path)).replace("\\", "/") for p in tmp_path.rglob("*") if p.is_file())
    assert all(w.startswith("out/") for w in written), written
    assert not any(home.rglob("*"))
    assert {"out/search-storm_brand/report.md", "out/search-storm_brand/evaluations.jsonl", "out/search-storm_brand/20261114-1200/report.md",
            "out/search-storm_brand/report-20261114-1200.md", "out/trace.json"} <= set(written)
    rows = [json.loads(line) for line in (outcome.paths.evaluations).read_text(encoding="utf-8").splitlines()]
    assert [r["rung"] for r in rows].count("full") == 1


# -- one result type -------------------------------------------------------------------------------


def test_the_build_record_carries_every_field_once():
    res = BuildResult(skeleton=Skeleton(class_name="Templar", ascendancy="Inquisitor", main_link=["Storm Brand"]), import_code="X", xml="<x/>")
    res.stages.append(StageRecord(name="loop pass 1", seconds=1.0, stats={}, score_value=5.0, violation=0.0))
    res.moves = [{"move": "refine", "pass": 1}]
    res.floors_missed = ["Life"]
    data = BuildRecord.from_result(res).to_json()
    assert data["moves"] == [{"move": "refine", "pass": 1}] and "move_rows" not in data
    assert data["floors_missed"] == ["Life"] and data["stages"] == [{"name": "loop pass 1", "seconds": 1.0, "value": 5.0, "violation": 0.0, "notes": ""}]
    assert json.loads(json.dumps(data)) == data  # plain data: crosses a process, lands in a file


@pytest.mark.parametrize("module", ["junkroan.search.runner", "benchmark"])
def test_the_search_worker_and_the_benchmark_row_both_take_the_record(module):
    import importlib
    import inspect
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    source = inspect.getsource(importlib.import_module(module))
    assert "BuildRecord.from_result(res).to_json()" in source
    assert '"move_rows": res.moves' not in source
