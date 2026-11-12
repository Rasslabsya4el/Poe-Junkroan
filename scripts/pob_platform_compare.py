"""Proof that PoB gives the same numbers on Linux as on Windows: dump on each system, then compare.

`dump` evaluates reference builds (PoB import codes) in the pinned headless runtime of THIS system and writes
every stat of every output PoB computes: for each build, for each socket group with an active skill, that group
is made the main skill and the whole `build.calcsTab.mainOutput` (and the minion's output when there is one) is
written recursively, every number as `%.17g` (round-trips a double exactly). `sequence` then runs an
optimizer-like run of PoB calls through `PobSession` (the worker subprocess, as the optimizer uses it) and writes
every call's result at full precision, plus the `RecordingPob` transcript of the calls. `compare` reads two
dumps and lists every difference with its stat, both values and the relative size.

    python scripts/pob_platform_compare.py dump --out win.json
    python scripts/pob_platform_compare.py sequence --out win.seq.json --transcript win.calls.jsonl
    python scripts/pob_platform_compare.py compare win.json linux.json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from junkroan.pob.brand_instances import brand_gems_at_count_one_xml  # noqa: E402
from junkroan.pob.session import decode_import_code  # noqa: E402

FIXTURES = (
    "tests/fixtures/tuadh_329/arc_archmage.pob.txt",
    "tests/fixtures/tuadh_329/absolution_minions.pob.txt",
    "tests/fixtures/tuadh_329/bleed_bow.pob.txt",
    "tests/fixtures/tuadh_329/ignite_penance_brand.pob.txt",
    "tests/fixtures/tuadh_329/impale_cyclone.pob.txt",
    "tests/fixtures/tuadh_329/poison_spark.pob.txt",
    "tests/fixtures/tuadh_329/cold_dot.pob.txt",
    "tests/fixtures/tuadh_329/pyroclast_mine.pob.txt",
    # timeless jewels: PoB inflates their data through the host zlib (zlib1.dll / libz.so.1)
    "tests/fixtures/zizaran_327/assassin_poison_spark.pob.txt",
    "tests/fixtures/zizaran_326/chieftain_righteous_fire.pob.txt",
    "tests/fixtures/zizaran_325/hierophant_ice_nova_archmage.pob.txt",
    "tests/fixtures/zizaran_329/occultist_essence_drain.pob.txt",
)
SEQUENCE_FIXTURE = "tests/fixtures/tuadh_329/arc_archmage.pob.txt"
SEQUENCE_KEYS = ("CombinedDPS", "FullDPS", "Life", "EnergyShield", "Mana", "TotalEHP", "PhysicalMaximumHitTaken",
                 "FireResist", "ColdResist", "LightningResist", "ChaosResist", "Str", "Dex", "Int", "Speed")

# Every stat of every output: recursive over plain tables, keys sorted, numbers as %.17g.
DUMP_LUA = r"""
local out = {}
local function fmt(v)
  local t = type(v)
  if t == 'number' then
    if v ~= v then return 'nan' end
    if v == math.huge then return 'inf' end
    if v == -math.huge then return '-inf' end
    return string.format('%.17g', v)
  elseif t == 'string' then return 's:' .. v
  elseif t == 'boolean' then return tostring(v)
  end
  return nil
end
local function walk(prefix, tbl, depth, seen)
  if seen[tbl] or depth > 6 then return end
  seen[tbl] = true
  local keys = {}
  for k in pairs(tbl) do
    if type(k) == 'string' or type(k) == 'number' then keys[#keys + 1] = k end
  end
  table.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
  for _, k in ipairs(keys) do
    local v = tbl[k]
    local path = prefix .. '.' .. tostring(k)
    if type(v) == 'table' then
      if getmetatable(v) == nil then walk(path, v, depth + 1, seen) end
    else
      local text = fmt(v)
      if text then out[#out + 1] = path .. '=' .. text end
    end
  end
end
local groups = build.skillsTab.socketGroupList
local original = build.mainSocketGroup
for index, group in ipairs(groups) do
  if group.enabled ~= false and group.displaySkillList and #group.displaySkillList > 0 then
    build.mainSocketGroup = index
    build.buildFlag = true
    runCallback('OnFrame')
    local label = 'g' .. index .. '[' .. tostring(group.displayLabel or group.label or '') .. ']'
    walk(label .. '.player', build.calcsTab.mainOutput, 0, {})
    local env = build.calcsTab.mainEnv
    if env and env.minion and env.minion.output then walk(label .. '.minion', env.minion.output, 0, {}) end
  end
end
build.mainSocketGroup = original
build.buildFlag = true
runCallback('OnFrame')
return table.concat(out, '\n')
"""


def _system() -> dict[str, Any]:
    return {"platform": sys.platform, "machine": platform.machine(), "python": platform.python_version()}


def dump(out: Path) -> None:
    from junkroan.pob.headless_runtime_worker import HeadlessLuaRuntime
    from junkroan.pob.release_manager import PoBReleaseManager

    runtime_root = PoBReleaseManager().fetch().extract_dir.resolve()
    session_root = Path(tempfile.mkdtemp(prefix="pobcmp-"))
    os.environ["POB_RUNTIME_ROOT"] = runtime_root.as_posix()
    os.environ["POB_HEADLESS_USER_PATH"] = session_root.as_posix()
    os.environ["POB_HEADLESS_WORKDIR"] = session_root.as_posix()
    os.environ.setdefault("CI", "1")
    started = time.perf_counter()
    runtime = HeadlessLuaRuntime(runtime_root=runtime_root, session_root=session_root,
                                 wrapper_path=ROOT / "src/junkroan/pob/headless_wrapper.lua")
    boot = time.perf_counter() - started
    builds: dict[str, dict[str, str]] = {}
    seconds: dict[str, float] = {}
    for fixture in FIXTURES:
        code = (ROOT / fixture).read_text(encoding="utf-8").strip()
        t0 = time.perf_counter()
        runtime.load_reopen_source(brand_gems_at_count_one_xml(decode_import_code(code)))
        text = runtime._bridge.execute(DUMP_LUA, nret=1)[0] or ""
        seconds[fixture] = round(time.perf_counter() - t0, 3)
        builds[fixture] = dict(line.split("=", 1) for line in text.splitlines())
        print(f"{fixture}: {len(builds[fixture])} values in {seconds[fixture]:.1f} s", flush=True)
    out.write_text(json.dumps({"system": _system(), "boot_s": round(boot, 2), "seconds": seconds,
                               "jit": runtime.jit_guard, "builds": builds}, indent=1, sort_keys=True), encoding="utf-8")


def sequence(out: Path, transcript: Path, rounds: int) -> None:
    """An optimizer-like run: per allocated node, remove it, read stats, a fast trial batch, add it back, read."""

    from junkroan.pob.session import PobSession
    from junkroan.recording_pob import RecordingPob

    results: list[Any] = []
    timings: list[float] = []
    with PobSession(run_id="platform-compare") as session:
        pob = RecordingPob(session, transcript)

        def call(name: str, *args: Any, **kwargs: Any) -> Any:
            t0 = time.perf_counter()
            try:
                value = getattr(pob, name)(*args, **kwargs)
            except Exception as exc:  # a refusal is a result too: both systems must give the same one
                value = {"error": f"{type(exc).__name__}: {exc}"}
            timings.append(time.perf_counter() - t0)
            results.append({"call": name, "result": value})
            return value

        call("load_import_code", (ROOT / SEQUENCE_FIXTURE).read_text(encoding="utf-8").strip())
        keys = list(SEQUENCE_KEYS)
        call("stats", keys)
        tree = call("tree_light")
        masteries = {int(str(n).split(":")[0]) for n in (tree.get("mastery_effect_ids") or ())}
        allocated = sorted(int(n) for n in tree["user_allocated_node_ids"] if int(n) not in masteries)
        start = allocated[len(allocated) // 3:][:rounds]
        for node in start:
            call("remove_nodes", [node])
            call("stats", keys)
            call("trial_stats", [{"add": [node]}, {"remove": [allocated[0]]}], keys, mode="fast")
            call("add_nodes", [node])
            call("stats", keys)
        pob.close_recording()
    out.write_text(json.dumps({"system": _system(), "calls": len(results), "seconds_per_call": timings,
                               "results": results}, sort_keys=True, default=str), encoding="utf-8")
    print(f"{len(results)} calls, mean {sum(timings) / len(timings) * 1000:.1f} ms per call")


def _flatten(prefix: str, value: Any, into: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key in sorted(value, key=str):
            _flatten(f"{prefix}.{key}", value[key], into)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _flatten(f"{prefix}[{index}]", item, into)
    else:
        into[prefix] = value


def _as_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def compare(left: Path, right: Path, show: int) -> int:
    a, b = json.loads(left.read_text(encoding="utf-8")), json.loads(right.read_text(encoding="utf-8"))
    fa: dict[str, Any] = {}
    fb: dict[str, Any] = {}
    _flatten("", a.get("builds", a.get("results")), fa)
    _flatten("", b.get("builds", b.get("results")), fb)
    only_a, only_b = sorted(set(fa) - set(fb)), sorted(set(fb) - set(fa))
    common = sorted(set(fa) & set(fb))
    diffs = []
    for key in common:
        if fa[key] != fb[key]:
            x, y = _as_number(fa[key]), _as_number(fb[key])
            rel = abs(x - y) / max(abs(x), abs(y)) if x is not None and y is not None and max(abs(x), abs(y)) > 0 else math.inf
            diffs.append((rel, key, fa[key], fb[key]))
    numeric = sum(1 for key in common if _as_number(fa[key]) is not None)
    print(f"{left.name} ({a['system']['platform']}) vs {right.name} ({b['system']['platform']})")
    print(f"values compared: {len(common)} (numeric {numeric}); identical: {len(common) - len(diffs)}; "
          f"different: {len(diffs)}; only left: {len(only_a)}; only right: {len(only_b)}")
    for rel, key, x, y in sorted(diffs, reverse=True)[:show]:
        print(f"  {key}: {x} | {y} | rel {rel:.3g}")
    for key in (only_a + only_b)[:show]:
        print(f"  one side only: {key}")
    return 0 if not diffs and not only_a and not only_b else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    d = sub.add_parser("dump")
    d.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("sequence")
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("--transcript", type=Path, required=True)
    s.add_argument("--rounds", type=int, default=60)
    c = sub.add_parser("compare")
    c.add_argument("left", type=Path)
    c.add_argument("right", type=Path)
    c.add_argument("--show", type=int, default=40)
    args = parser.parse_args()
    for name in ("out", "transcript", "left", "right"):  # the runtime chdirs into PoB's folder
        if getattr(args, name, None) is not None:
            setattr(args, name, getattr(args, name).resolve())
    if args.command == "dump":
        dump(args.out)
        return 0
    if args.command == "sequence":
        sequence(args.out, args.transcript, args.rounds)
        return 0
    return compare(args.left, args.right, args.show)


if __name__ == "__main__":
    raise SystemExit(main())
