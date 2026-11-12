# Testing: which test a change gets, and how long it takes (D113)

Read before the first PoB run of a ticket. Every ticket that touches optimizer code names its kind in its body
before its first PoB run; the PR names the kind and shows its numbers. The rule's reasons and numbers are in D113
and D84. Locally only quick, targeted tests run; every PoB run past that is a heavy run
(`python .github/scripts/heavy_dispatch.py`, `docs/ci.md`). Local tests read PoB's data files: fetch them once by the pin
in `locks/pob.source.lock.json` (`git clone --depth 1 --branch <pinned tag> <repo_url> vendor/pob/source`, then check the
commit); without them about 150 quick tests fail on a missing `vendor/pob/source/...` file.

## 1. Decide the kind

| kind | what changed | examples |
|---|---|---|
| A | the search space: an option becomes allowed, or a class is forbidden (rails, rulebook values, templates, bases, oils, sockets, cluster sizes, unique tiers) | #392 (uniques T5 only), #436 (flasks), #433 (cluster jewels), #429 (template lines) |
| B | how the loop or the evaluation behaves (a move's logic, judging, the objective, trial_stats, seeds) | #179 (loot fill ends on its best set), #398 (an emptied slot's trial), #464 (seed collisions), #419 |
| C | a refactor: every PoB number must stay identical | #35, #42, #51 (judging context, loop as a module) |
| D | speed only | a cache, a faster parser |
| none | no optimizer code: docs, process, CI, research notes | |

If a change is A but also touches selection, loop control, evaluation values or termination, it is B.

## 2. The test per kind

| kind | PoB-free tests | PoB test | size | never |
|---|---|---|---|---|
| A | rail / unit tests: the forbidden value refused, the allowed one accepted | the trace counter on a replay-bench pass of 1-2 delivered builds where the option is legal (`replay_bench.py --trace`): `generated(x) > 0 and evaluated(x) > 0`; for a restriction `evaluated(forbidden) = 0 and output(forbidden) = 0` on every build; one witness fixture where x is the known-best move | minutes | a before/after set run; a metric gain as proof; "a lower median = failure" |
| B | a test that encodes the defect (invariant or differential), PoB-free where the defect allows | D84's bench: `replay_bench.py --move <m>` on the smoke six delivered builds, base and head at one seed, per-build paired deltas and structural counts | about 25 min per side on 5 workers | a per-ticket paired set run, unless the bench alerts (a build under -15) or the whole loop changes: then 14 builds x 1 seed, a further seed block only by a rule written before it |
| C | the suite | identical PoB call transcript base vs head (`replay_bench.py --record-calls`, `compare_calls.py`) and finals equal to the digit (D95) | about 25 min per side on 5 workers | tolerating any difference: a difference means the change is A or B |
| D | the suite + C's transcript | interleaved base/head timings on one runner | under 1 h | a quality claim |
| none | the suite (CI) | none | no PoB | any PoB run |
| main | - | the weekly core run (below) | hours, once a week | judging a ticket by it; "rerun until green" (one fresh seed block on an alert, then revert if confirmed) |

What a paired set run costs, for the record: one half of core14 x 3 seeds was 14 h 10 min at 3 workers. The smoke
set's own A/A noise is -11.5 points at the median, so such a pair cannot see the 1-10 point effects a ticket claims;
that is why no ticket is judged by one (D113).

## 3. What the PR shows

- A: the move x class counts of the trace pass and its duration.
- B: the bug test, then the per-build paired table of the bench (gain, duration, counts).
- C: "identical, N calls, finals equal".
- D: the timing table.
- none: the suite line.

## 4. The weekly core run

The one place that says whether overall quality moved: core14 x 3 seeds on `main`, sent once a week as a heavy run,
read paired per reference against the previous weekly core run. It gates nothing.

```bash
python scripts/benchmark.py --set core14 --gear template --seed 4 --seeds 3 --workers <N>
```

## 5. When a build goes to the owner (a Reading)

The owner reads finished PoBs for the errors numbers cannot show (a nonsensical item, a dead node, a flask that makes
no sense). A reading request is a plain dark page: one row per build with an Open PoB button (its pobb.in link) and
one line of what to look at. He is asked in exactly these cases:

- **After every weekly core run**: the best-seed build of every reference whose median moved against the previous
  weekly core run by more than that reference's own spread, and of every reference a rule merged that week touches.
- **After a kind-A rule lands**: one build from the trace pass where the new option was picked (the witness).
- **When an audit cannot judge**: a new kind of error suspected; the reading's verdict becomes an audit check.
- **Never** for kind-B or kind-C proofs (numbers decide), or for single seeds of a run.

## 6. Commands

```bash
python -m pytest -q -m "not slow"                          # quick, local: a targeted file or test only
python -m pytest -q -m pob tests/test_<one>.py             # one PoB test, local if under a minute
python scripts/replay_bench.py --builds "<run>/*.pob.txt" --move picks --seed 1 --workers 5 --tag b<issue>-base --record-calls artifacts/proof-<issue>/base
python scripts/replay_bench.py --builds "<run>/*.pob.txt" --move picks --seed 1 --workers 5 --tag b<issue>-head --record-calls artifacts/proof-<issue>/head --against b<issue>-base
python scripts/compare_calls.py artifacts/proof-<issue>/base artifacts/proof-<issue>/head
```

The bench and benchmark lines run as heavy runs, each at its own ref (base at the merge-base, head at the branch).
