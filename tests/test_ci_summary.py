"""The summary check of the CI run: green only when every shard ran and passed."""

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "ci_summary.py"
spec = importlib.util.spec_from_file_location("ci_summary", SCRIPT)
ci_summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci_summary)

POB_SKIP = "PoB runtime not present"
OTHER_SKIP = "needs a local author PoB"


def write_shard(results, number, *, tests=3, selected=None, collected=6, skips=(), failures=0, seconds=2.0):
    """A shard folder as the job uploads it: `tests` test cases, the first `len(skips)` skipped, then `failures` failed."""
    folder = results / f"results-{number}"
    folder.mkdir(parents=True)
    cases = []
    for index in range(tests):
        body = ""
        if index < len(skips):
            body = f'<skipped type="pytest.skip" message="{skips[index]}"/>'
        elif index < len(skips) + failures:
            body = '<failure message="boom"/>'
        cases.append(f'<testcase classname="t" name="test_{number}_{index}" time="1.0">{body}</testcase>')
    xml = f'<testsuites><testsuite name="pytest" tests="{tests}" time="{seconds}">{"".join(cases)}</testsuite></testsuites>'
    (folder / "junit.xml").write_text(xml, encoding="utf-8")
    report = {"slot": number, "slots": 2, "collected": collected, "selected": tests if selected is None else selected}
    (folder / "shard.json").write_text(json.dumps(report), encoding="utf-8")
    recorded = {
        "tests": {f"t::test_{number}_{index}": 1.0 + 150 * index for index in range(tests)},
        "groups": {f"t_{number}": {"seconds": 2.0 * number, "tests": tests}},
    }
    (folder / "durations.json").write_text(json.dumps(recorded), encoding="utf-8")


def full_run(results, **options):
    for number in (1, 2):
        write_shard(results, number, **options)


def run(results, tmp_path, *extra):
    merged = tmp_path / "merged.json"
    code = ci_summary.main([str(results), "--shards", "2", "--merged-durations", str(merged), *extra])
    return code, merged


def test_every_shard_present_and_green_passes_and_reports_the_totals(tmp_path, capsys):
    results = tmp_path / "results"
    full_run(results)

    code, merged = run(results, tmp_path)

    out = capsys.readouterr().out
    assert code == 0
    assert "all shards passed" in out
    assert "| 2/2 | 6 | 6 | 0 | 0 |" in out
    assert json.loads(merged.read_text(encoding="utf-8")) == {
        "t_1": {"seconds": 2.0, "tests": 3},
        "t_2": {"seconds": 4.0, "tests": 3},
    }
    assert "5.0 min  `t::test_1_2`" in out  # the slowest tests are listed, past 90 s in minutes
    assert "1.0 s  `t::test_1_0`" in out


def test_a_missing_shard_or_one_that_left_no_files_fails_the_run(tmp_path, capsys):
    results = tmp_path / "results"
    full_run(results)
    for leftover in (results / "results-2").iterdir():
        leftover.unlink()

    code, _ = run(results, tmp_path)

    assert code == 1
    assert "shard 2/2: no result files" in capsys.readouterr().out
    (results / "results-2").rmdir()
    assert run(results, tmp_path)[0] == 1


def test_a_failed_test_fails_the_run(tmp_path, capsys):
    results = tmp_path / "results"
    write_shard(results, 1, failures=1)
    write_shard(results, 2)

    code, _ = run(results, tmp_path)

    assert code == 1
    assert "shard 1: 1 test(s) failed or errored" in capsys.readouterr().out


def test_a_shard_that_ran_other_tests_than_it_was_given_fails_the_run(tmp_path, capsys):
    results = tmp_path / "results"
    write_shard(results, 1, tests=4, collected=6)
    write_shard(results, 2, tests=2, selected=3)

    code, _ = run(results, tmp_path)

    assert code == 1
    assert "ran 2 tests but was given 3" in capsys.readouterr().out


def test_shards_whose_tests_do_not_add_up_to_the_collected_ones_fail_the_run(tmp_path, capsys):
    results = tmp_path / "results"
    full_run(results, collected=7)

    code, _ = run(results, tmp_path)

    assert code == 1
    assert "in all but 7 were collected" in capsys.readouterr().out


def test_a_forbidden_skip_fails_the_run_and_another_skip_is_only_counted(tmp_path, capsys):
    results = tmp_path / "results"
    full_run(results, skips=(OTHER_SKIP, POB_SKIP))

    code, _ = run(results, tmp_path)
    out = capsys.readouterr().out
    assert code == 0
    assert "| 2/2 | 6 | 2 | 4 | 0 |" in out
    assert f"2 x {OTHER_SKIP}" in out

    code, _ = run(results, tmp_path, "--forbid-skip", "PoB runtime")
    assert code == 1
    assert f"2 test(s) skipped for a reason CI does not accept: {POB_SKIP}" in capsys.readouterr().out


@pytest.mark.parametrize("result", ["failure", "cancelled"])
def test_a_workflow_that_did_not_end_in_success_fails_the_run(tmp_path, capsys, result):
    results = tmp_path / "results"
    full_run(results)

    code, _ = run(results, tmp_path, "--job-result", result)

    assert code == 1
    assert f"ended as '{result}'" in capsys.readouterr().out


def test_a_run_that_collected_fewer_tests_than_the_floor_fails(tmp_path, capsys):
    results = tmp_path / "results"
    full_run(results)

    code, _ = run(results, tmp_path, "--min-tests", "7")

    assert code == 1
    assert "only 6 tests were collected, at least 7 are expected" in capsys.readouterr().out
