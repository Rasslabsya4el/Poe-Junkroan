"""The one check of the CI run: green only when every shard passed.

Reads the folder the shard jobs uploaded, one subfolder `results-<shard>` each with `junit.xml`, `shard.json` (what
`--shard-report` wrote) and `durations.json` (what `--record-durations` wrote), and prints a Markdown report; the same
text goes to `$GITHUB_STEP_SUMMARY` when that is set. Exit 1 when:

- a shard is missing, or has no result files (the job died, was cancelled or timed out);
- a test failed or errored;
- a shard ran another number of tests than it was given, or the shards together do not add up to the tests
  collected (a test dropped or run twice), or two shards disagree on what the suite is;
- fewer tests collected than `--min-tests` (an empty run is not a pass);
- a test skipped with a reason that holds a `--forbid-skip` text (e.g. the pinned PoB is missing on the runner).

Other skips are counted and listed by reason. `--merged-durations FILE` writes the seconds and the number of tests
of every group, for `tests/shard_durations.json` (see `docs/ci.md`).

Standard library only: it runs on the bare runner.
"""

import argparse
import collections
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TOP_TESTS = 15


def read_shard(folder: Path) -> dict | None:
    """The numbers of one shard, or None when its files are not there."""
    try:
        suite = ET.parse(folder / "junit.xml").getroot()
        if suite.tag == "testsuites":
            suite = suite[0]
        report = json.loads((folder / "shard.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, ET.ParseError, IndexError):
        return None
    cases = suite.findall("testcase")
    skips = collections.Counter()
    for case in cases:
        for skipped in case.findall("skipped"):
            skips[(skipped.get("message") or "").strip()] += 1
    return {
        "report": report,
        "tests": len(cases),
        "failed": sum(1 for case in cases if case.find("failure") is not None or case.find("error") is not None),
        "skipped": sum(skips.values()),
        "skips": skips,
        "seconds": float(suite.get("time") or 0),
    }


def read_durations(folder: Path) -> dict:
    try:
        recorded = json.loads((folder / "durations.json").read_text(encoding="utf-8"))
        return {"tests": recorded["tests"], "groups": recorded["groups"]}
    except (OSError, ValueError, KeyError):
        return {"tests": {}, "groups": {}}


def check(results: Path, shards: int, min_tests: int = 1, forbid_skips: tuple[str, ...] = ()) -> tuple[list[str], list[str], dict, dict]:
    """(problems, report lines, seconds per test, seconds and tests per group) of the whole run."""
    problems: list[str] = []
    lines = ["| shards | tests | passed | skipped | failed | slowest shard |", "|---|---|---|---|---|---|"]
    durations = {"tests": {}, "groups": {}}
    found = {}
    for number in range(1, shards + 1):
        folder = results / f"results-{number}"
        shard = read_shard(folder) if folder.is_dir() else None
        if shard is None:
            problems.append(f"shard {number}/{shards}: no result files (the job did not finish)")
            continue
        found[number] = shard
        for kind, values in read_durations(folder).items():
            durations[kind].update(values)

    skips = collections.Counter()
    if found:
        collected = {shard["report"]["collected"] for shard in found.values()}
        if len(collected) != 1:
            problems.append(f"the shards collected different numbers of tests: {sorted(collected)}")
        if max(collected) < min_tests:
            problems.append(f"only {max(collected)} tests were collected, at least {min_tests} are expected")
        for number, shard in found.items():
            if shard["tests"] != shard["report"]["selected"]:
                problems.append(f"shard {number}: ran {shard['tests']} tests but was given {shard['report']['selected']}")
            if shard["failed"]:
                problems.append(f"shard {number}: {shard['failed']} test(s) failed or errored")
        given = sum(shard["report"]["selected"] for shard in found.values())
        if len(found) == shards and given != max(collected):
            problems.append(f"the shards were given {given} tests in all but {max(collected)} were collected")
        total = sum(shard["tests"] for shard in found.values())
        skipped = sum(shard["skipped"] for shard in found.values())
        failed = sum(shard["failed"] for shard in found.values())
        slowest = max(shard["seconds"] for shard in found.values())
        lines.append(f"| {len(found)}/{shards} | {total} | {total - skipped - failed} | {skipped} | {failed} | {slowest / 60:.1f} min |")
        for shard in found.values():
            skips.update(shard["skips"])

    for reason, count in skips.items():
        if any(text in reason for text in forbid_skips):
            problems.append(f"{count} test(s) skipped for a reason CI does not accept: {reason}")
    if skips:
        lines += ["", "Skips by reason:", ""]
        lines += [f"- {count} x {reason or '(no reason)'}" for reason, count in skips.most_common()]
    groups = {group: {"seconds": round(entry["seconds"], 3), "tests": entry["tests"]} for group, entry in sorted(durations["groups"].items())}
    return problems, lines, durations["tests"], groups


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("results", type=Path, help="folder holding the results-<shard> folders")
    parser.add_argument("--shards", type=int, required=True, help="number of shards")
    parser.add_argument("--merged-durations", type=Path, help="write the seconds and tests per group here")
    parser.add_argument("--min-tests", type=int, default=1, help="fail when fewer tests were collected")
    parser.add_argument("--forbid-skip", action="append", default=[], metavar="TEXT", help="fail when a skip reason holds TEXT (repeatable)")
    parser.add_argument("--job-result", default="success", help="result of the shard jobs as the workflow knows it")
    args = parser.parse_args(argv)

    problems, lines, tests, groups = check(args.results, args.shards, args.min_tests, tuple(args.forbid_skip))
    if args.job_result != "success":
        problems.append(f"the shard jobs ended as '{args.job_result}'")
    if args.merged_durations is not None:
        args.merged_durations.parent.mkdir(parents=True, exist_ok=True)
        args.merged_durations.write_text(json.dumps(groups, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        top = sorted(tests.items(), key=lambda pair: -pair[1])[:TOP_TESTS]
        lines += ["", f"Slowest {len(top)} tests:", ""]
        lines += [f"- {seconds:.1f} s  `{nodeid}`" if seconds < 90 else f"- {seconds / 60:.1f} min  `{nodeid}`" for nodeid, seconds in top]

    verdict = "FAILED" if problems else "all shards passed"
    text = "\n".join([f"## CI summary: {verdict}", "", *lines, *([""] + [f"- PROBLEM: {p}" for p in problems] if problems else [])])
    print(text)
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(text + "\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
