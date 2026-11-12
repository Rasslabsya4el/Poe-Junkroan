"""Splitting the suite over CI jobs: which test goes to which slot, and how long each took.

A pytest plugin, registered on the command line: `python -m pytest -p tests.shard_support --shard 3/32 ...` (CI does
this in `.github/workflows/ci.yml`; see `docs/ci.md`). It adds `--shard SLOT/TOTAL`, `--shard-durations FILE`,
`--record-durations FILE` and `--shard-report FILE`. Without `--shard` it changes nothing: every test runs, in order.
The decisions are plain functions so that `tests/test_shard_support.py` can check them.

A *group* is the unit that is never split: all tests of one module, or, when a module-scoped (or wider) fixture
is parametrized, all tests of one module and one value of that fixture. Such a fixture is where the expensive
part lives (a PobSession opened, a build evaluated); with the group in one slot, one process, it is built once.
Every process computes the same plan from the same collected tests and the same durations file, so no
coordinator is needed: the groups go to slots longest first, each to the slot with the least time so far.
"""

import json
import re
import statistics
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import pytest

WIDE_SCOPES = frozenset({"module", "package", "session"})
UNKNOWN_SECONDS = 1.0  # one test's time when the durations file holds no time at all
SHARD_FORMAT = re.compile(r"(\d+)/(\d+)")


# ---- pure decisions -------------------------------------------------------------------------------------------------


def parse_shard(text: str) -> tuple[int, int]:
    """`"3/8"` is shard 3 of 8, counted from 1."""
    found = SHARD_FORMAT.fullmatch(text.strip())
    if found is None:
        raise ValueError(f"--shard wants I/N such as 3/8, not {text!r}")
    index, count = int(found.group(1)), int(found.group(2))
    if not 1 <= index <= count:
        raise ValueError(f"--shard {text!r}: the shard number must be from 1 to {count}")
    return index, count


def group_name(nodeid: str, wide_params: Mapping[str, int]) -> str:
    """The group of a test: its module, and the index of each module-or-wider parametrized fixture.

    `wide_params` maps the argument name to the index of the value this test uses (not the value itself,
    which may print differently on two machines).
    """
    module = nodeid.split("::", 1)[0]
    if not wide_params:
        return module
    return module + "[" + ",".join(f"{name}#{wide_params[name]}" for name in sorted(wide_params)) + "]"


def read_durations(path: Path | None) -> dict[str, tuple[float, int]]:
    """Stored (seconds, number of tests) of each group; empty when no file is given.

    By group and not by test: a test id can carry anything its parameters print, and the plan needs only the
    group's time.
    """
    if path is None:
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    return {str(group): (float(entry["seconds"]), int(entry["tests"])) for group, entry in document.items()}


def group_seconds(members: Mapping[str, Sequence[str]], durations: Mapping[str, tuple[float, int]]) -> dict[str, float]:
    """Seconds per group: the stored time, plus the median seconds of one test for each test the group gained.

    A group without a stored time costs its tests at that median; with no stored time at all a test costs one second.
    """
    per_test = [seconds / tests for seconds, tests in durations.values() if tests]
    unit = statistics.median(per_test) if per_test else UNKNOWN_SECONDS
    result = {}
    for group, nodeids in members.items():
        seconds, tests = durations.get(group, (0.0, 0))
        result[group] = seconds + max(0, len(nodeids) - tests) * unit
    return result


def assign(seconds: Mapping[str, float], count: int) -> dict[str, int]:
    """Group -> shard number (from 1): longest group first, each to the shard with the least time so far.

    Ties break by group name and then by the lower shard number, so every shard gets the same answer.
    """
    loads = [0.0] * count
    plan: dict[str, int] = {}
    for group in sorted(seconds, key=lambda name: (-seconds[name], name)):
        shard = min(range(count), key=lambda index: (loads[index], index))
        loads[shard] += seconds[group]
        plan[group] = shard + 1
    return plan


def order_longest_first(groups: Iterable[str], seconds: Mapping[str, float]) -> list[str]:
    """The groups of one shard in the order they should start, so the long ones do not end the run alone."""
    return sorted(groups, key=lambda name: (-seconds[name], name))


def write_json(path: Path, document: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def recording(seconds: Mapping[str, float], groups: Mapping[str, str]) -> dict[str, object]:
    """What `--record-durations` writes: the seconds of each test that ran, and of each group of them."""
    by_group: dict[str, dict[str, float]] = {}
    for nodeid, spent in seconds.items():
        entry = by_group.setdefault(groups.get(nodeid, nodeid.split("::", 1)[0]), {"seconds": 0.0, "tests": 0})
        entry["seconds"] += spent
        entry["tests"] += 1
    rounded = {group: {"seconds": round(entry["seconds"], 3), "tests": int(entry["tests"])} for group, entry in by_group.items()}
    return {"tests": {nodeid: round(spent, 3) for nodeid, spent in seconds.items()}, "groups": rounded}


# ---- the pytest wiring ----------------------------------------------------------------------------------------------

RECORDED: dict[str, float] = defaultdict(float)
GROUPS: dict[str, str] = {}  # node id -> group, kept for the recording


def pytest_addoption(parser):
    group = parser.getgroup("shard", "split the suite over CI jobs")
    group.addoption("--shard", metavar="I/N", help="run only slot I of N (from 1); every slot must see the same tests")
    group.addoption("--shard-durations", metavar="FILE", help="JSON file of seconds per group that balances the slots")
    group.addoption("--record-durations", metavar="FILE", help="write the seconds of every test that ran to FILE")
    group.addoption("--shard-report", metavar="FILE", help="write how many tests were collected and selected to FILE")


def _wide_params(item) -> dict[str, int]:
    """Index of the value of each parametrized fixture of module scope or wider that the test uses."""
    callspec = getattr(item, "callspec", None)
    if callspec is None:
        return {}
    return {
        name: callspec.indices[name]
        for name, scope in callspec._arg2scope.items()
        if getattr(scope, "value", scope) in WIDE_SCOPES
    }


@pytest.hookimpl(trylast=True)  # after every other plugin and conftest has deselected (markers, -k): plan what remains
def pytest_collection_modifyitems(config, items):
    option = config.getoption("shard")
    if config.getoption("record_durations"):
        GROUPS.update({item.nodeid: group_name(item.nodeid, _wide_params(item)) for item in items})
    if option is None:
        return
    try:
        index, count = parse_shard(option)
        durations = read_durations(Path(config.getoption("shard_durations")) if config.getoption("shard_durations") else None)
    except (ValueError, OSError) as problem:
        raise pytest.UsageError(str(problem)) from problem

    group_of = {id(item): group_name(item.nodeid, _wide_params(item)) for item in items}
    members: dict[str, list[str]] = defaultdict(list)
    for item in items:
        members[group_of[id(item)]].append(item.nodeid)
    seconds = group_seconds(members, durations)
    plan = assign(seconds, count)

    mine = [name for name, slot in plan.items() if slot == index]
    start = {name: place for place, name in enumerate(order_longest_first(mine, seconds))}
    selected = sorted((item for item in items if group_of[id(item)] in start), key=lambda item: start[group_of[id(item)]])
    chosen = {id(item) for item in selected}
    dropped = [item for item in items if id(item) not in chosen]
    if dropped:
        config.hook.pytest_deselected(items=dropped)
    items[:] = selected

    report = config.getoption("shard_report")
    if report:
        write_json(
            Path(report),
            {
                "slot": index, "slots": count, "collected": len(dropped) + len(selected),
                "selected": len(selected), "groups": len(mine), "seconds": round(sum(seconds[name] for name in mine), 1),
            },
        )  # fmt: skip


def pytest_runtest_logreport(report):
    RECORDED[report.nodeid] += report.duration


def pytest_sessionfinish(session):
    target = session.config.getoption("record_durations")
    if target:
        write_json(Path(target), recording(RECORDED, GROUPS))
