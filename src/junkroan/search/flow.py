"""The search: a request in, ranked optimized builds out (#16).

    from junkroan.search.flow import SearchOptions, run
    outcome = run(SearchOptions(skill="Storm Brand", request=BuildRequest.from_dict({...})))

`run` is the one entry; `junkroan build` (cli.py) calls it in-process and `scripts/search.py` only parses its
arguments into `SearchOptions` and prints. Stages, each PoB-judged, processes in parallel:

  1. candidates: the skeletons of a request (or hypotheses, or every ascendancy)
  2. supports: greedy link on a rig for the first candidate, shared by the screen
  3. prepare: per candidate, bases and ascendancy nodes by PoB
  4. screen: cheap pipeline (loot N=60, greedy tree) -> `screen_order`
  5. full: `choose_finalists` (top K, + a unique variant each when the unique screen finds >= 10%), each built
     `seeds` times (D71) as separate jobs in one pool; `best_by_seed` delivers the best, the rest are kept
  6. mutation round: `mutation_batch` variants of the finished builds, screened, the ones `variant_screen_kept`
     built in full on their parent's winning seed
  7. ranking (`final_order`) and the report (`report_lines`): `<out>/search-<skill>/<stamp>/`

Every PoB call goes through a `Builder`: `PoolBuilder` opens the sessions and the process pools; a test hands a
scripted one and runs every stage without PoB. A crashed prepare, screen or seed is a `Failure`, named in the first
lines of the report; a finalist with no surviving seed makes the run exit non-zero.

Output: `$OUT_DIR/search-<skill>/<stamp>/` when `OUT_DIR` is set (a heavy run uploads `$OUT_DIR`), else
`artifacts/search-<skill>/<stamp>/` in the repository. Nothing is written outside those.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Protocol

from junkroan.report_format import human_duration
from junkroan.search.evaluations import append_row, format_rho, parse_full_ranks, row_for, selected_screen_ranks, skeleton_label, spearman
from junkroan.search.request import (DEFAULT_SEEDS, BuildRequest, full_done_line, full_optimize_line, load_request, mutation_done_line, prepared_line,
                                     rig_supports_line, screen_done_line, total_line)
from junkroan.search.runner import (apply_unique_picks, best_by_seed, format_seeds, pick_unique_variant, seed_spread, transcript_name, unique_pick_ok,
                                    variant_screen_line, weapon_alternative_ok)
from junkroan.search.skeleton import Skeleton

ROOT = Path(__file__).resolve().parents[3]

EXIT_OK = 0
EXIT_BAD_REQUEST = 1  # no candidates, or a request the expansion refused
EXIT_LOST_BUILD = 2  # a finalist has no surviving seed, or the search delivered nothing


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


# -- options -----------------------------------------------------------------------------------


@dataclass(slots=True)
class SearchOptions:
    """What one search is asked to do: the request (or hypotheses, or ascendancies) and the budget knobs."""

    skill: str
    request: BuildRequest | None = None
    hypotheses: str | None = None  # a JSON file of hypotheses (docs/HYPOTHESES.md)
    ascendancies: list[str] | None = None  # without a request or hypotheses: the ascendancy ids to try (None = all)
    dry_run: bool = False
    top: int = 3
    full_ranks: list[int] | None = None  # one-based screen ranks to optimize in full; variants off
    seeds: int | None = None  # None: the request's, else DEFAULT_SEEDS
    workers: int = 5
    loop_seconds: float | None = None
    gear: str = "loot"
    unique_min_gain: float = 0.10
    no_unique_variants: bool = False
    no_mutation: bool = False
    trace_out: str | None = None
    record_calls: str | None = None

    def __post_init__(self) -> None:
        if self.full_ranks:
            # This mode measures the original screen candidates. A unique or mutation variant
            # would be an additional, differently-screened skeleton rather than the selected rank.
            self.no_unique_variants = True
            self.no_mutation = True
        if self.request is not None:  # the skill comes from the request; a given skill is a placeholder
            self.skill = self.request.skill or self.skill
            if self.gear == "loot" and self.request.gear != "loot":
                self.gear = self.request.gear


def search_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="search", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill")
    ap.add_argument("--hypotheses", help="JSON file of hypotheses (docs/HYPOTHESES.md)")
    ap.add_argument("--request", help="build request JSON (docs/REQUEST.md); expands to hypotheses")
    ap.add_argument("--dry-run", action="store_true", help="with --request: print the echo and stop")
    ap.add_argument("--ascendancies", help="comma-separated ascendancy ids to try (default: all)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--full-ranks", type=parse_full_ranks, help="comma-separated one-based screen ranks to optimize in full; variants are disabled")
    ap.add_argument("--seeds", type=int, default=None, help=f"full builds per finalist skeleton; the best by Score is delivered (default {DEFAULT_SEEDS}, D71)")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--loop-seconds", type=float, help="maximum seconds for each full improvement loop")
    ap.add_argument("--gear", choices=("loot", "wishlist"), default="loot", help="day-1 gear model")
    ap.add_argument("--unique-min-gain", type=float, default=0.10)
    ap.add_argument("--no-unique-variants", action="store_true")
    ap.add_argument("--no-mutation", action="store_true", help="skip the second round (unique variants of the finished builds)")
    ap.add_argument("--trace-out", help="write the summed trace counters (move x class x generated/evaluated, plus a total) as JSON to this path")
    ap.add_argument("--record-calls", metavar="DIR", help="#16: record every PoB call of each session to DIR/<job>.calls.jsonl (junkroan.recording_pob)")
    return ap


def options_from_argv(argv: Sequence[str] | None = None, *, request: BuildRequest | None = None) -> SearchOptions:
    """`SearchOptions` from a search command line; `request` (in-process callers) stands for `--request FILE`."""

    a = search_parser().parse_args(argv)
    if request is None and a.request:
        request = load_request(Path(a.request))
    return SearchOptions(
        skill=a.skill, request=request, hypotheses=a.hypotheses, ascendancies=a.ascendancies.split(",") if a.ascendancies else None,
        dry_run=a.dry_run, top=a.top, full_ranks=a.full_ranks, seeds=a.seeds, workers=a.workers, loop_seconds=a.loop_seconds, gear=a.gear,
        unique_min_gain=a.unique_min_gain, no_unique_variants=a.no_unique_variants, no_mutation=a.no_mutation, trace_out=a.trace_out,
        record_calls=a.record_calls,
    )


# -- where a run writes ------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OutputPaths:
    root: Path  # search-<skill>: the latest report.md, every run's report-<stamp>.md, the logs, evaluations.jsonl
    run_dir: Path  # this run's ranked set, never deleted by a later run (#526)

    @property
    def logs(self) -> Path:
        return self.root / "logs"

    @property
    def evaluations(self) -> Path:
        return self.root / "evaluations.jsonl"


def output_paths(skill: str, *, now: time.struct_time | None = None, env: Mapping[str, str] | None = None, repo: Path = ROOT) -> OutputPaths:
    """`$OUT_DIR/search-<skill>/<stamp>` when OUT_DIR is set (a heavy run uploads it), else the repository's `artifacts/`."""

    env = os.environ if env is None else env
    base = Path(env["OUT_DIR"]) if env.get("OUT_DIR") else repo / "artifacts"
    root = base / f"search-{slugify(skill)}"
    return OutputPaths(root=root, run_dir=root / time.strftime("%Y%m%d-%H%M", now or time.localtime()))


def echo_line(echo: str, run_dir: Path) -> str:
    """The request echo (#524's plan line) plus the dated folder this run writes into (#526)."""
    return f"{echo}\nresults: {run_dir}"


def write_build_files(run_dir: Path, stem: str, r: dict, spares: list[dict]) -> None:
    """One ranked build into the run's own dated folder: the import code, the json, the seeds it beat."""
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / f"{stem}.pob.txt").write_text(r["import_code"], encoding="utf-8")
    (run_dir / f"{stem}.json").write_text(json.dumps({k: v for k, v in r.items() if k not in ("xml", "import_code")}, indent=1, ensure_ascii=False), encoding="utf-8")
    for sp in sorted(spares, key=lambda s: int(s.get("seed") or 0)):  # the seeds this build beat, for the spread
        (run_dir / f"{stem}-s{int(sp.get('seed') or 0)}.pob.txt").write_text(sp["import_code"], encoding="utf-8")


def publish_report(out_dir: Path, run_dir: Path, report: list[str]) -> None:
    """The run's report.md in its folder; the skill root's report.md is the latest run's, first line names the folder."""
    body = "\n".join(report) + "\n"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "report.md").write_text(body, encoding="utf-8")
    (out_dir / "report.md").write_text(f"Latest run: {run_dir}\n" + body, encoding="utf-8")


# -- the PoB side: one interface, a pool in production, a script in tests ------------------------


@dataclass(slots=True)
class Job:
    """One worker call: `kind` "prepare" (runner.prepare_candidate) or "optimize" (runner.optimize) on `skeleton`."""

    skeleton: Skeleton
    kind: str
    kwargs: dict[str, Any]
    tag: str = ""
    seed: int | None = None


class Builder(Protocol):
    def composition(self, skill: str, rails: Any) -> dict[str, float]: ...

    def rig_supports(self, rig: Skeleton, rails: Any, log: Callable[[str], None]) -> list[str]: ...

    def run(self, jobs: list[Job], workers: int) -> Iterator[tuple[Job, dict]]:
        """Every job's worker result (a plain dict, `ok` False with `error` when it crashed), in completion order."""
        ...


class PoolBuilder:
    """The real builder: PoB sessions in this process for the probe and the rig, a fresh process pool per stage."""

    def __init__(self, record_calls: str | None = None) -> None:
        self.record_calls = record_calls

    def composition(self, skill: str, rails: Any) -> dict[str, float]:
        from junkroan.pob.session import PobSession
        from junkroan.search.modes import probe_composition
        from junkroan.search.runner import recording

        with PobSession(run_id="composition") as session, recording(session, self.record_calls, "composition") as pob:
            return probe_composition(pob, skill, rails)

    def rig_supports(self, rig: Skeleton, rails: Any, log: Callable[[str], None]) -> list[str]:
        return rig_supports(rig, rails, log=log, record_calls=self.record_calls)

    def run(self, jobs: list[Job], workers: int) -> Iterator[tuple[Job, dict]]:
        from junkroan.bounded_pool import limited_completions
        from junkroan.search.runner import optimize, prepare_candidate

        fns = {"prepare": prepare_candidate, "optimize": optimize}
        with ProcessPoolExecutor(max_workers=workers) as pool:  # #958: one job per worker, gives way to the yield
            for fut, job in limited_completions(lambda job: pool.submit(fns[job.kind], job.skeleton.to_json(), **job.kwargs), jobs, workers):
                yield job, fut.result()


def rig_supports(rig: Skeleton, rails: Any, *, log: Callable[[str], None] = print, record_calls: str | None = None) -> list[str]:
    """Supports for the screen, chosen once by PoB on a rig: bases, ascendancy, cheap gear
    and half a tree first (a bare rig deals ~200 DPS, so flat-damage supports such as Decay
    win every time and multipliers never show their value)."""

    from junkroan.optimizer.loot_gear import LootGear
    from junkroan.optimizer.objective_select import objective_for
    from junkroan.optimizer.tree_optimizer import TreeOptimizer
    from junkroan.pob.session import PobSession
    from junkroan.search.generator import SkeletonGenerator
    from junkroan.search.runner import recording

    with PobSession(run_id=f"search-rig-{os.getpid()}") as session, recording(session, record_calls, "rig") as pob:
        gen = SkeletonGenerator(pob, rails, objective=objective_for(rails, rig.main_link[0], mode=rig.mode).without_sustain(), log=log)
        rig.apply(pob, gem_level=rails.gems.level, gem_quality=rails.gems.quality, main_quality=rails.gems.main_quality)
        gen.refresh_castability()
        gen.screen_bases(rig)
        gen.pick_ascendancy_nodes(rig)
        LootGear(pob, gen.objective, rails, log=log).fill(rig.rare_bases, passes=1, n=40, seed=3)
        TreeOptimizer(pob, gen.objective.without("EffectiveMovementSpeedMod"), max_trials=300, log=log).allocate(rails.passive_points // 2)
        gen.pick_supports(rig, n_supports=5)
    return list(rig.main_link[1:])


# -- the run's record: report, failures, evaluation rows ---------------------------------------


@dataclass(frozen=True, slots=True)
class Failure:
    """A worker that crashed: which stage, which skeleton or finalist tag, which seed, its error."""

    stage: str  # "prepare", "screen", "full", "variant screen"
    what: str
    error: str
    seed: int | None = None

    def line(self) -> str:
        return f"- {self.stage} failed {self.what}" + (f" seed {self.seed}" if self.seed is not None else "") + f": {self.error}"


@dataclass(slots=True)
class Ledger:
    """What the stages leave besides their return value: report lines, failures, trace parts, evaluation rows."""

    skill: str
    evaluations: Path | None = None
    commit: str | None = None
    print_fn: Callable[[str], None] = field(default=lambda msg: print(msg, flush=True))
    report: list[str] = field(default_factory=list)
    failures: list[Failure] = field(default_factory=list)
    considered: list[Any] = field(default_factory=list)

    def say(self, msg: str) -> None:
        """A line for the console and the report."""
        self.print_fn(msg)
        self.report.append(msg)

    def tell(self, msg: str) -> None:
        """A line for the console only."""
        self.print_fn(msg)

    def fail(self, failure: Failure) -> None:
        self.failures.append(failure)
        self.print_fn(failure.line())

    def evaluation(self, skeleton: Skeleton, rung: str, result: dict, seed: int | None) -> None:
        if self.evaluations is not None:
            append_row(self.evaluations, row_for(request=skeleton.source_label or self.skill, skeleton=skeleton, rung=rung, result=result, seed=seed, commit=self.commit))


def _uniques_cell(res: dict) -> list:
    return [(u["slot"], u["name"], f"{u['gain']:+.0%}") for u in res.get("uniques", [])[:3]]


# -- 1. candidates -----------------------------------------------------------------------------


@dataclass(slots=True)
class Candidates:
    skeletons: list[Skeleton]
    options: SearchOptions  # the request's own top, workers and seeds settled in
    echo: str | None = None  # a request's echo (docs/REQUEST.md)
    ok: bool = True  # False: the request expansion found problems


def candidates(opts: SearchOptions, rails: Any, builder: Builder, ledger: Ledger) -> Candidates:
    """The candidate skeletons: a request's expansion, validated hypotheses, or one per ascendancy."""

    from junkroan.search.hypothesis import ascendancies, load_hypotheses, normalize_ascendancy_ids, validate

    skeletons: list[Skeleton] = []
    if opts.request is not None:
        from junkroan.search.request import expand

        req = opts.request
        composition = None
        wants_probe = req.skill and (not [m for m in req.modes if m != "auto"] or any(m in ("ignite", "poison", "bleed") for m in req.modes))
        if wants_probe:
            composition = builder.composition(req.skill, rails)
        exp = expand(req, rails, composition=composition, unique_variants=not opts.no_unique_variants, mutation=not opts.no_mutation)
        # the flag wins over the request file for the seeds, which the echo was computed from
        settled = replace(opts, top=req.top, workers=req.workers, seeds=opts.seeds if opts.seeds is not None else req.seeds)
        for v in exp.validations:
            v.skeleton.source_label = f"{opts.skill}: {exp.echo}"
            skeletons.append(v.skeleton)
        return Candidates(skeletons=skeletons if exp.ok else [], options=settled, echo=exp.echo, ok=exp.ok)
    if opts.hypotheses:
        for h in load_hypotheses(Path(opts.hypotheses)):
            v = validate(h)
            if not v.ok:
                ledger.say(f"- rejected hypothesis {h.name!r}: {'; '.join(v.problems)}")
                continue
            v.skeleton.notes = h.why or h.name
            v.skeleton.source_label = f"{opts.skill}: {h.name}"
            skeletons.append(v.skeleton)
        return Candidates(skeletons=skeletons, options=opts)
    wanted = normalize_ascendancy_ids(opts.ascendancies) if opts.ascendancies else None
    for asc in ascendancies().values():
        if wanted and asc["ascendancy_id"] not in wanted:
            continue
        skeletons.append(Skeleton(class_name=asc["class_name"], ascendancy=asc["ascendancy_id"], level=rails.level, main_link=[opts.skill],
                                  notes=f"{asc['class_name']} {asc['ascendancy_id']}", source_label=opts.skill))
    return Candidates(skeletons=skeletons, options=opts)


# -- 2. shared supports ------------------------------------------------------------------------


def shared_supports(skeletons: list[Skeleton], rails: Any, builder: Builder, ledger: Ledger, clock: Callable[[], float] = time.perf_counter) -> list[str] | None:
    """The link of the first candidate that needs supports, picked on a rig; None when every candidate has six."""

    need = [sk for sk in skeletons if len(sk.main_link) < 6]
    if not need:
        return None
    t0 = clock()
    rig = Skeleton.from_json(need[0].to_json())
    supports = builder.rig_supports(rig, rails, lambda m: ledger.tell(f"  rig: {m}"))
    ledger.say(rig_supports_line(rig.class_name, rig.ascendancy, clock() - t0, supports))
    return supports


# -- 3. prepare, 4. screen ---------------------------------------------------------------------


def prepare(skeletons: list[Skeleton], opts: SearchOptions, builder: Builder, ledger: Ledger, logs: Path, supports: list[str] | None) -> list[Skeleton]:
    """Every candidate's blanks filled by PoB, in completion order; a crashed one is a `Failure`."""

    jobs = [Job(sk, "prepare", {"log_path": str(logs / f"prepare-{sk.ascendancy}.log"), "shared_supports": supports, "gear_mode": opts.gear,
                                "record_calls": opts.record_calls}) for sk in skeletons]
    out: list[Skeleton] = []
    for job, res in builder.run(jobs, opts.workers):
        sk = job.skeleton
        ledger.considered.append(res.get("considered"))
        if not res["ok"]:
            ledger.fail(Failure("prepare", f"{sk.class_name}/{sk.ascendancy}", res["error"]))
            continue
        prepared_sk = Skeleton.from_json(res["skeleton"])
        rig = dict(res.get("rig") or {})
        if rig:
            rig["seconds"] = res["seconds"]
            ledger.evaluation(prepared_sk, "rig", rig, None)
        out.append(prepared_sk)
        ledger.tell(f"  prepared {sk.class_name}/{sk.ascendancy} in {human_duration(res['seconds'])}: {[(p['what'], p['choice']) for p in res['picks']]}")
    return out


def screen_order(screened: list[dict]) -> list[dict]:
    """Value first, violation only breaks ties: the full optimize repairs a screen's missed floor (every screen-infeasible
    skeleton that reached full depth ended feasible, violations 0.008-0.276), and feasibility-first sank Raise Zombie's
    full-depth winner (Guardian, 0.008 short) from screen rank 2 to 15 (docs/readings/2026-09-22-winner-recall.md)."""

    return sorted(screened, key=lambda r: (r["value"], -r["violation"]), reverse=True)


def screen(prepared: list[Skeleton], opts: SearchOptions, builder: Builder, ledger: Ledger, logs: Path) -> list[dict]:
    """The cheap pipeline on every prepared skeleton, ranked by `screen_order`; a crashed one is a `Failure`."""

    jobs = [Job(sk, "optimize", {"log_path": str(logs / f"screen-{sk.ascendancy}.log"), "screen": True, "gear_mode": opts.gear,
                                 "unique_screen": not opts.no_unique_variants and sk.unique_slots != "none",
                                 "record_calls": opts.record_calls, "transcript": transcript_name("screen", sk.to_json(), sk.ascendancy)})
            for sk in prepared]
    out: list[dict] = []
    for job, res in builder.run(jobs, opts.workers):
        sk = job.skeleton
        ledger.considered.append(res.get("considered"))
        if not res["ok"]:
            ledger.fail(Failure("screen", f"{sk.class_name}/{sk.ascendancy}", res["error"]))
            continue
        ledger.evaluation(Skeleton.from_json(res["skeleton"]), "screen", res, None)
        out.append(res)
        ledger.tell(f"  screened {sk.class_name}/{sk.ascendancy}: {res['value']:,.0f} (viol {res['violation']:.3f}) in {human_duration(res['seconds'])}; uniques {_uniques_cell(res)}")
    return screen_order(out)


def screen_table(screened: list[dict]) -> list[str]:
    lines = ["", "| # | skeleton | screen DPS | viol | best unique |", "|---|---|---|---|---|"]
    for i, r in enumerate(screened, 1):
        sk = Skeleton.from_json(r["skeleton"])
        u = r["uniques"][0] if r["uniques"] else None
        lines.append(f"| {i} | {sk.class_name}/{sk.ascendancy} | {r['value']:,.0f} | {r['violation']:.3f} | {f'{u['name']} ({u['slot']}, {u['gain']:+.0%})' if u else '-'} |")
    return [*lines, ""]


# -- 5. finalists and the full round ---------------------------------------------------------------


@dataclass(slots=True)
class Finalists:
    skeletons: list[Skeleton]
    screen_ranks: list[int | None]  # the screen rank of each (full-ranks mode only), None for a variant
    rows: list[tuple[int, dict]]  # the (screen rank, screen result) the finalists came from
    considered: list[Any] = field(default_factory=list)

    def batch(self) -> list[tuple[Skeleton, str, int]]:
        """(skeleton, tag, first seed) per finalist: tag `screen-<rank>` in full-ranks mode, else `<ascendancy>-<i>`."""
        return [(sk, f"screen-{rank}" if rank is not None else f"{sk.ascendancy}-{i}", 1) for i, (sk, rank) in enumerate(zip(self.skeletons, self.screen_ranks))]


def choose_finalists(screened: list[dict], *, top: int, full_ranks: list[int] | None, unique_variants: bool, min_gain: float, max_uniques: int) -> Finalists:
    """The screen's top `top` (or exactly the `full_ranks`), each followed by its unique variant when the screen found one."""

    selected = selected_screen_ranks(full_ranks or [], len(screened))
    rows = [(rank, screened[rank - 1]) for rank in selected] if full_ranks else [(rank, row) for rank, row in enumerate(screened[:top], 1)]
    out = Finalists(skeletons=[], screen_ranks=[], rows=rows)
    for rank, r in rows:
        sk = Skeleton.from_json(r["skeleton"])
        out.skeletons.append(sk)
        out.screen_ranks.append(rank if full_ranks else None)
        if unique_variants:
            var, considered = pick_unique_variant(sk, r["uniques"], min_gain, max_uniques)
            out.considered.append(considered)
            if var is not None:
                out.skeletons.append(var)
                out.screen_ranks.append(None)
    return out


@dataclass(slots=True)
class FullRound:
    winners: list[dict]  # the best seed of each finalist (best_by_seed)
    spares: list[dict]  # the seeds the winners beat
    lost: list[str]  # finalist tags with no surviving seed


def full_round(batch: list[tuple[Skeleton, str, int]], opts: SearchOptions, builder: Builder, ledger: Ledger, logs: Path, *, seeds: int = 1) -> FullRound:
    """Build every (skeleton, tag, first seed) of the batch `seeds` times, all jobs in one pool, and keep the best
    build per skeleton (D71: the seed is worth ~17 points). A crashed seed is a `Failure`; a finalist whose every seed
    crashed is `lost`."""

    from junkroan.search.runner import seed_jobs

    def kwargs(sk: Skeleton, tag: str, seed: int) -> dict:
        kw = {"log_path": str(logs / f"full-{tag}-s{seed}.log"), "screen": False, "seed": seed, "gear_mode": opts.gear,
              "repick_supports": len(sk.fixed_supports) < 5, "unique_screen": not opts.no_mutation and sk.unique_slots != "none",
              "record_calls": opts.record_calls}
        if opts.loop_seconds is not None:
            kw["loop_seconds"] = opts.loop_seconds
        return kw

    jobs = [Job(sk, "optimize", kwargs(sk, tag, sd), tag=tag, seed=sd) for sk, tag, sd in seed_jobs(batch, seeds)]
    out: list[dict] = []
    for job, res in builder.run(jobs, opts.workers):
        ledger.considered.append(res.get("considered"))
        if not res["ok"]:
            ledger.fail(Failure("full", job.tag, res["error"], seed=job.seed))
            continue
        res["tag"], res["seed"] = job.tag, job.seed
        ledger.evaluation(Skeleton.from_json(res["skeleton"]), "full", res, job.seed)
        out.append(res)
        ledger.tell(f"  full {job.tag} seed {job.seed}: {res['value']:,.0f} (viol {res['violation']:.3f}) in {human_duration(res['seconds'])}; uniques {_uniques_cell(res)}")
    winners, others = best_by_seed(out)
    for w in winners:
        if len(w["seed_runs"]) > 1:
            ledger.say(f"  {w['tag']}: {format_seeds(w)}")
    won = {str(w.get("tag") or "") for w in winners}
    lost = [tag for _sk, tag, _sd in batch if tag not in won]
    return FullRound(winners=winners, spares=others, lost=list(dict.fromkeys(lost)))


def full_ranks_lines(selected_ranks: list[int], screened: list[dict], finals: list[dict]) -> list[str]:
    """The full-ranks table (screen rank against full rank) and its rank correlations."""

    def stage_value(result: dict, *, loop_pass: bool) -> float | None:
        stages = result.get("stages") or []
        if loop_pass:
            stage = next((stage for stage in stages if stage.get("name") == "loop pass 1"), None)
        else:
            loop_start = next((index for index, stage in enumerate(stages) if stage.get("name") == "loop pass 1"), None)
            construction = stages[:loop_start] if loop_start is not None else [stage for stage in stages if stage.get("name") not in {"config (final lanes)", "fixed point check"}]
            stage = construction[-1] if construction else None
        value = (stage or {}).get("value")
        return float(value) if isinstance(value, (int, float)) else None

    by_screen_rank = {int(str(result["tag"]).removeprefix("screen-")): result for result in finals if str(result.get("tag") or "").startswith("screen-")}
    full_ranked = sorted(by_screen_rank.items(), key=lambda pair: (not bool(pair[1].get("feasible")), float(pair[1].get("violation") or 0.0), -float(pair[1].get("value") or 0.0)))
    full_ranks = {screen_rank: rank for rank, (screen_rank, _result) in enumerate(full_ranked, 1)}
    lines = ["", "| screen rank | skeleton | screen value | full value | full rank | time |", "|---|---|---|---|---|---|"]
    for screen_rank in selected_ranks:
        full = by_screen_rank.get(screen_rank)
        scr = screened[screen_rank - 1]
        if full is None:
            lines.append(f"| {screen_rank} | {skeleton_label(Skeleton.from_json(scr['skeleton']))} | {scr['value']:,.0f} | failed | - | - |")
            continue
        lines.append(f"| {screen_rank} | {skeleton_label(Skeleton.from_json(full['skeleton']))} | {scr['value']:,.0f} | {full['value']:,.0f} | {full_ranks[screen_rank]} | {human_duration(full['seconds'])} |")
    paired = [(rank, screened[rank - 1], full) for rank, full in by_screen_rank.items()]
    full_values = [full["value"] for _rank, _screen, full in paired]
    lines.append(f"Spearman rho (screen value, full value) = {format_rho(spearman([s['value'] for _r, s, _f in paired], full_values))} (n = {len(paired)})")
    if full_ranked:
        w = full_ranked[0][0]
        lines.append(f"the full-depth winner sits at screen rank {w}: inside top 2: {'yes' if w <= 2 else 'no'}, top 3: {'yes' if w <= 3 else 'no'}, top 5: {'yes' if w <= 5 else 'no'}")
    construction = [stage_value(full, loop_pass=False) for _rank, _screen, full in paired]
    loop_one = [stage_value(full, loop_pass=True) for _rank, _screen, full in paired]
    stages = "; ".join(f"{rank}: {construction[i]:,.0f} / {loop_one[i]:,.0f}" if construction[i] is not None and loop_one[i] is not None else f"{rank}: n/a" for i, (rank, _s, _f) in enumerate(paired))
    lines.append(f"construction / loop pass 1 by screen rank: {stages}; Spearman rho (construction, full) = {format_rho(spearman(construction, full_values))}; "
                 f"Spearman rho (loop pass 1, full) = {format_rho(spearman(loop_one, full_values))}")
    return lines


# -- 6. the mutation round ---------------------------------------------------------------------


def _finished_order(finals: list[dict]) -> list[dict]:
    return sorted(finals, key=lambda r: (r["feasible"], -r["violation"], r["value"]), reverse=True)


def mutation_batch(finals: list[dict], *, top: int, min_gain: float, max_uniques: int, keystone_name: Callable[[int], str | None]) -> list[tuple[Skeleton, str, int]]:
    """Variants of the top finished builds, each continuing from the seed its parent won with: every structural
    keystone the build took rebuilt without it (D40), the runner-up weapon types (D41), and the uniques that beat
    the build's rares. `keystone_name(node id)` names a skeleton's fixed keystones (the request asked for them: no variant)."""

    batch: list[tuple[Skeleton, str, int]] = []
    for r in _finished_order(finals)[:top]:
        base = Skeleton.from_json(r["skeleton"])
        parent_seed = int(r.get("seed") or 1)
        fixed = {name.lower() for name in (keystone_name(int(i)) for i in base.keystones) if name}
        for keystone in r.get("keystones") or []:
            if keystone.lower() in {k.lower() for k in base.forbid_keystones} or keystone.lower() in fixed:
                continue
            var = Skeleton.from_json(r["skeleton"])
            var.drop_picked_utilities()
            var.forbid_keystones = [*base.forbid_keystones, keystone]
            var.notes = (var.notes or "") + f" -> without {keystone}"
            batch.append((var, f"{var.ascendancy}-no-{slugify(keystone)}", parent_seed))
        for alt in base.weapon_alternatives[:2]:  # runner-up weapon types from the base screen, as whole builds (D41)
            if not weapon_alternative_ok(base, alt):
                continue  # it would change a forced base or a forced-affix slot's class (#510)
            var = Skeleton.from_json(r["skeleton"])
            var.drop_picked_utilities()
            var.weapon_alternatives = []
            var.rare_bases["Weapon 1"] = alt["Weapon 1"]
            var.sockets.pop("Weapon 1", None)
            if alt.get("Weapon 2"):
                var.rare_bases["Weapon 2"] = alt["Weapon 2"]
            else:
                var.rare_bases.pop("Weapon 2", None)
            var.sockets.pop("Weapon 2", None)
            var.notes = (var.notes or "") + f" -> weapon {alt['Weapon 1']}"
            batch.append((var, f"{var.ascendancy}-w-{slugify(alt['Weapon 1'])}", parent_seed))
    seen = {json.dumps(Skeleton.from_json(r["skeleton"]).uniques, sort_keys=True) + Skeleton.from_json(r["skeleton"]).ascendancy for r in finals}
    for r in _finished_order(finals)[:top]:
        base = Skeleton.from_json(r["skeleton"])
        parent_seed = int(r.get("seed") or 1)
        picked = dict(base.uniques)
        for u in r["uniques"]:
            if u["gain"] >= min_gain and u["slot"] not in picked and len(picked) < max_uniques and unique_pick_ok(base, u["slot"], u["name"].split(", ")[0]):
                picked[u["slot"]] = u["name"].split(", ")[0]
        key = json.dumps(picked, sort_keys=True) + base.ascendancy
        if picked == base.uniques or key in seen:
            continue
        seen.add(key)
        var = Skeleton.from_json(r["skeleton"])
        var.drop_picked_utilities()
        apply_unique_picks(var, picked, replace=True)
        var.notes = (var.notes or "") + f" -> mutation uniques {picked}"
        batch.append((var, f"{var.ascendancy}-mut{len(batch)}", parent_seed))
    return batch


def variant_floor(screened: list[dict], top: int) -> float:
    """Half of the best screen value among the top finalists: what a variant's screen must reach (#525)."""
    return 0.5 * max((r["value"] for r in screened[:top]), default=0.0)


def screen_variants(batch: list[tuple[Skeleton, str, int]], floor_value: float, opts: SearchOptions, builder: Builder, ledger: Ledger, logs: Path) -> list[tuple[Skeleton, str, int]]:
    """Screen every variant first (3 min each); the ones that hold up (`variant_screen_kept`) earn the full round.
    A Smite sceptre variant that finished at 31k after 15 min screened at a fraction of the sword."""

    jobs = [Job(sk, "optimize", {"log_path": str(logs / f"screen-{tag}.log"), "screen": True, "seed": sd, "gear_mode": opts.gear, "record_calls": opts.record_calls},
                tag=tag, seed=sd) for sk, tag, sd in batch]
    kept: list[tuple[Skeleton, str, int]] = []
    for job, res in builder.run(jobs, opts.workers):
        ledger.considered.append(res.get("considered"))
        if not res["ok"]:
            ledger.fail(Failure("variant screen", job.tag, res["error"]))
            continue
        ledger.evaluation(Skeleton.from_json(res["skeleton"]), "screen", res, job.seed)  # a variant screen is an evaluation like any other
        ok, line = variant_screen_line(job.tag, res, floor_value)
        ledger.tell(line)
        if ok:
            kept.append((job.skeleton, job.tag, int(job.seed or 1)))
    return kept


# -- 7. ranking and the report -------------------------------------------------------------------


def final_order(finals: list[dict]) -> list[dict]:
    """The delivered order: a build with audit errors sinks, then feasible first, then the smaller violation, then the value."""
    return sorted(finals, key=lambda r: (not r.get("audit_errors"), r["feasible"], -r["violation"], r["value"]), reverse=True)


def build_name(sk: Skeleton) -> str:
    return (f"{sk.class_name}/{sk.ascendancy}" + (f" + {', '.join(sk.uniques.values())}" if sk.uniques else "")
            + (f" (no {', '.join(sk.forbid_keystones)})" if sk.forbid_keystones else "") + (f" [{sk.rare_bases['Weapon 1']}]" if sk.rare_bases.get("Weapon 1") else ""))


def stamp_builds(finals: list[dict]) -> None:
    """Each ranked build's file stem, `NN <name>`, into `stem`."""
    for i, r in enumerate(finals, 1):
        r["stem"] = f"{i:02d} {slugify(build_name(Skeleton.from_json(r['skeleton'])))}"


def ranking_lines(finals: list[dict]) -> list[str]:
    """The ranked table and one section per build (why, picks, seeds, explanation, summary). `finals` in `final_order`, stamped."""

    from junkroan.optimizer.audit import floors_cell
    from junkroan.optimizer.explain import pareto_front
    from junkroan.optimizer.objective import bossing_defence

    front = pareto_front([{"value": r["value"] if r["feasible"] and not r.get("audit_errors") else 0, "ehp": bossing_defence(r["final"] or {})} for r in finals])  # the defence axis is the bossing one (D53)
    lines = ["", "| rank | build | DPS (conservative) | seed | spread | optimistic | life | max hit (boss) | EHP (map) | MS | uniques | audit | floors | pareto | time |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(finals, 1):
        sk = Skeleton.from_json(r["skeleton"])
        f = r["final"]
        audit = f"{r.get('audit_errors', 0)} errors / {len(r.get('audit', [])) - r.get('audit_errors', 0)} warnings" if r.get("audit") else "clean"
        runs = r.get("seed_runs") or []
        spread = f"{seed_spread(r.get('seed_values') or []):.1%} ({len(runs)} seeds)" if len(runs) > 1 else "-"
        lines.append(f"| {i} | {build_name(sk)} | {r['value']:,.0f} | {r.get('seed', 1)} | {spread} | {r['optimistic'] or 0:,.0f} | {f.get('Life')} | {bossing_defence(f):,.0f} | "
                     f"{f.get('TotalEHP', 0):,.0f} | {f.get('EffectiveMovementSpeedMod', 0):.2f} | {', '.join(sk.uniques.values()) or '-'} | {audit} | "
                     f"{floors_cell(r.get('floors_missed'))} | {'front' if (i - 1) in front else ''} | {human_duration(r['seconds'])} |")
    lines.append("")
    for i, r in enumerate(finals, 1):
        sk = Skeleton.from_json(r["skeleton"])
        lines.append(f"## {i}. {sk.class_name}/{sk.ascendancy}: {' - '.join(sk.main_link)}")
        lines.append(f"why: {sk.notes}")
        lines.append(f"ascendancy nodes {sk.ascendancy_nodes}; bases {sk.rare_bases}; uniques {sk.uniques}; keystones {r.get('keystones') or []}"
                     + (f" (forbidden {sk.forbid_keystones})" if sk.forbid_keystones else ""))
        if r.get("seed_runs"):
            others = [d for d in r["seed_runs"] if not d["best"]]
            lines.append(f"seeds: {format_seeds(r)}" + (f" The other seeds' builds: {', '.join(f'{r['stem']}-s{d['seed']}.pob.txt ({d['value']:,.0f})' for d in others)}." if others else ""))
        if r.get("explanation"):
            base_notes = sk.notes or ""
            variants = []
            for o in finals:
                osk = Skeleton.from_json(o["skeleton"])
                if o is not r and osk.ascendancy == sk.ascendancy and (osk.notes or "").startswith(base_notes + " -> "):
                    variants.append(((osk.notes or "")[len(base_notes) + 4:], o["value"]))
            lines.append("")
            text = r["explanation"] if not variants else r["explanation"] + "\n- Variants rebuilt as whole builds: " + ", ".join(f"{label} {v:,.0f}" for label, v in variants) + "."
            if len(r.get("seed_runs") or []) > 1:  # the same skeleton built several times: the delivered one is the best of them
                text += "\n- Seeds: " + format_seeds(r)
            lines.append(text)
        lines += ["```", r["summary"], "```"]
    return lines


def failure_lines(failures: list[Failure], lost: list[str]) -> list[str]:
    """The block the report opens with when anything crashed: every failure with its error, every lost finalist."""

    if not failures and not lost:
        return []
    head = f"**FAILED: {len(failures)} job(s) crashed" + (f"; {len(lost)} finalist(s) lost every seed: {', '.join(lost)}" if lost else "") + "**"
    return [head, *(f.line() for f in failures), ""]


# -- the run -------------------------------------------------------------------------------------


@dataclass(slots=True)
class SearchOutcome:
    """What a search delivered: the ranked builds (worker results in `final_order`, best first) and how it went."""

    builds: list[dict]
    failures: list[Failure]
    lost: list[str]  # finalist tags with no surviving seed
    report: list[str]
    exit_code: int
    paths: OutputPaths | None = None
    echo: str | None = None


def _commit() -> str | None:
    try:
        value = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True, timeout=2).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    return value or None


def _keystone_namer() -> Callable[[int], str | None]:
    from junkroan.optimizer.tree_graph import TreeGraph

    graph = TreeGraph.load()
    return lambda node: graph.nodes[node].name if node in graph.nodes else None


def run(opts: SearchOptions, builder: Builder | None = None, *, rails: Any = None, paths: OutputPaths | None = None,
        clock: Callable[[], float] = time.perf_counter, print_fn: Callable[[str], None] | None = None,
        keystone_name: Callable[[int], str | None] | None = None, commit: str | None = None) -> SearchOutcome:
    """One search, start to end. `builder` defaults to the PoB pool; `paths` to `output_paths(skill)`."""

    from junkroan.optimizer.rails import Rails

    t_all = clock()
    rails = rails or Rails.load()
    builder = builder or PoolBuilder(record_calls=opts.record_calls)
    paths = paths or output_paths(opts.skill)
    paths.logs.mkdir(parents=True, exist_ok=True)
    ledger = Ledger(skill=opts.skill, evaluations=paths.evaluations, commit=commit if commit is not None else _commit(),
                    **({"print_fn": print_fn} if print_fn else {}))

    def done(builds: list[dict], lost: list[str], code: int, echo: str | None = None) -> SearchOutcome:
        report = [f"# Search: {opts.skill}", "", *failure_lines(ledger.failures, lost), *ledger.report]
        return SearchOutcome(builds=builds, failures=list(ledger.failures), lost=lost, report=report, exit_code=code, paths=paths, echo=echo)

    # -- 1. candidates
    cands = candidates(opts, rails, builder, ledger)
    opts = cands.options
    if cands.echo is not None:
        ledger.tell(echo_line(cands.echo, paths.run_dir))
        if opts.dry_run or not cands.ok:
            return SearchOutcome(builds=[], failures=[], lost=[], report=[], exit_code=EXIT_OK if cands.ok else EXIT_BAD_REQUEST, paths=paths, echo=cands.echo)
        ledger.report.append(cands.echo)
    if not cands.skeletons:
        ledger.say("no candidates")
        return done([], [], EXIT_BAD_REQUEST, cands.echo)
    opts = replace(opts, seeds=max(1, opts.seeds or DEFAULT_SEEDS))
    ledger.say(f"{len(cands.skeletons)} candidate skeletons; {opts.seeds} seed(s) per finalist")

    # -- 2.-4. supports, prepare, screen
    supports = shared_supports(cands.skeletons, rails, builder, ledger, clock)
    t0 = clock()
    prepared = prepare(cands.skeletons, opts, builder, ledger, paths.logs, supports)
    ledger.say(prepared_line(len(prepared), clock() - t0))
    t0 = clock()
    screened = screen(prepared, opts, builder, ledger, paths.logs)
    ledger.say(screen_done_line(clock() - t0))
    for line in screen_table(screened):
        ledger.say(line)

    # -- 5. finalists, the full round
    fin = choose_finalists(screened, top=opts.top, full_ranks=opts.full_ranks, unique_variants=not opts.no_unique_variants,
                           min_gain=opts.unique_min_gain, max_uniques=rails.gear.max_uniques)
    ledger.considered.extend(fin.considered)
    ledger.say(full_optimize_line(len(fin.skeletons), opts.seeds, workers=opts.workers, mutation_finalists=0 if opts.no_mutation else len(fin.rows)))
    t0 = clock()
    first = full_round(fin.batch(), opts, builder, ledger, paths.logs, seeds=opts.seeds)
    finals, spares, lost = list(first.winners), list(first.spares), list(first.lost)
    ledger.say(full_done_line(clock() - t0, len(fin.skeletons), opts.seeds))
    if opts.full_ranks:
        for line in full_ranks_lines(selected_screen_ranks(opts.full_ranks, len(screened)), screened, finals):
            ledger.say(line)

    # -- 6. the mutation round
    if not opts.no_mutation:
        t0 = clock()
        batch = mutation_batch(finals, top=opts.top, min_gain=opts.unique_min_gain, max_uniques=rails.gear.max_uniques, keystone_name=keystone_name or _keystone_namer())
        if batch:
            ledger.say(f"mutation round: {len(batch)} variants of the finished builds (" + ", ".join(tag for _sk, tag, _sd in batch) + ")")
            kept = screen_variants(batch, variant_floor(screened, opts.top), opts, builder, ledger, paths.logs)
            if kept:  # a variant is one build on its parent's winning seed: the seeds were spent on the finalists
                second = full_round(kept, opts, builder, ledger, paths.logs)
                finals += second.winners
                spares += second.spares
                lost += second.lost
            ledger.say(mutation_done_line(clock() - t0, len(kept), len(batch)))

    # -- 7. ranking, files, report
    finals = final_order(finals)
    stamp_builds(finals)
    for line in ranking_lines(finals):
        ledger.say(line)
    ledger.say(total_line(clock() - t_all))
    paths.run_dir.mkdir(parents=True, exist_ok=True)
    spares_by_tag: dict[str, list[dict]] = {}
    for sp in spares:
        spares_by_tag.setdefault(str(sp.get("tag") or ""), []).append(sp)
    for r in finals:
        write_build_files(paths.run_dir, r["stem"], r, spares_by_tag.get(str(r.get("tag") or ""), []))
    code = EXIT_LOST_BUILD if lost or not finals else EXIT_OK
    outcome = done(finals, lost, code, cands.echo)
    publish_report(paths.root, paths.run_dir, outcome.report)
    (paths.root / f"report-{paths.run_dir.name}.md").write_text("\n".join(outcome.report) + "\n", encoding="utf-8")
    if opts.trace_out:
        from junkroan.search.trace_out import write_trace_out

        write_trace_out(opts.trace_out, ledger.considered)
    for line in failure_lines(outcome.failures, lost):
        ledger.tell(line)
    ledger.tell(f"report: {paths.run_dir / 'report.md'}")
    return outcome


def main(argv: Sequence[str] | None = None, *, request: BuildRequest | None = None) -> int:
    """A search command line, run in this process; the exit code of `run`."""

    import sys

    for stream in (sys.stdout, sys.stderr):  # requests carry the user's own words; a cp1252 console must not kill the run
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    return run(options_from_argv(argv, request=request)).exit_code


__all__ = ["Builder", "Failure", "Job", "OutputPaths", "PoolBuilder", "SearchOptions", "SearchOutcome", "choose_finalists", "final_order",
           "full_round", "main", "mutation_batch", "options_from_argv", "output_paths", "run", "screen_order", "search_parser", "variant_floor"]
