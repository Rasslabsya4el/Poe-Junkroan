# 2026-10-02 D113. A change is proven by the test of its kind; the weekly core run on main alone says whether quality moved

Status: Accepted; amended by D113 amd 1, D113 amd 2 (both removed with the old machine set-up)

rules the bench for a move; this ADR adds the kinds D84 did not name (a search-space rule, a refactor, speed) and
the one place the question "did overall quality move" is answered.

Why now (measured): one half of a paired run is 14 h 10 min for core14 x 3 seeds at 3 workers (`392-before`, Run
#479) and 11 h+ for the smoke six (`430-smoke-after`); on 2026-10-02 25 pair halves were waiting
for the Day-1 rulebook tickets, days of machine time, every rulebook rule waiting on its own pair. The pair cannot
prove what those tickets claim: the smoke A/A noise is -11.5 points at the median (seeds 4-6 against 1-3) and one
build's seed spread reaches 99.6 points (spark, #479), so 14 x 3 cannot see a 5-point mean shift (about 31
instances would, at a paired sd of 10), and a feature no build in the set picks leaves a 28 h pair silent about
the feature (the owner, 13:10, #485). The owner's rule in his words (14:05, #485): a change to build generation
itself keeps the paired PoB runs, 10 h there is fine; a feature (flasks, sockets, clusters) is proven by "it works
and the search sees it in its considerations", never by a build-metric gain; nothing must break. His deep research
(`docs/research/2026-10-02-test-protocol-owner-gpt.md`) and the two terra raw reports (digest in #485, 13:58) give
the same table and the sizing numbers quoted here.

Decision: every change is classified before its test is chosen, and the closing comment names the kind.

| kind | the test, its time | proves | never |
|---|---|---|---|
| A: a search-space rule (an allowed option or a restriction; the rulebook tickets) | (1) rail / unit tests without PoB; (2) the trace counter at the `trial_stats` boundary on a replay-bench pass of 1-2 delivered builds where the option is legal, minutes: for an option `generated(x) > 0 and evaluated(x) > 0`, for a restriction `evaluated(forbidden) = 0 and output(forbidden) = 0` on every build of the pass; (3) one witness fixture where x is the known-best move and selection keeps it | the option is wired through generation and evaluation, the forbidden class cannot leak | a metric gain; a lower median is not a failure. Reclassify as B only when move selection, loop control, evaluation values or termination also change |
| B: a loop or evaluation fix | a bug-specific invariant or differential test first (PoB-free where the defect allows); then D84's bench: the touched move replayed on the smoke six delivered builds, same seed, base against head, 21-25 min on 5 workers, per-build paired deltas and structural counts. A full paired set run only on an alert (a build under D84's -15, two sd of the A/A noise) or when the whole loop changes: then 14 x 1 seed first, a further seed block only by a rule written before the run | the defect is gone and the move did not get grossly worse on the builds where it reproduces | "the 14-set improved" |
| C: a refactor | an identical PoB call transcript base against head (`scripts/compare_calls.py`) and final values equal to the digit (D95); until #493 fixes the call order, the first-difference clause of #35/#42 | nothing visible at the PoB boundary changed | any difference tolerated: a difference means the change is A or B |
| D: speed only | C's equality plus interleaved base/head timings on one host | the time moved, the behaviour did not | a quality claim |
| main | the weekly gate: core14 x 3 seeds (`--gear wishlist`, 42 build-runs, about 14 h at 3 workers), one heavy run pinned at main, paired per reference against the previous gate; on an alert exactly one fresh seed block, never "rerun until green"; a confirmed regression reverts the commit | whether overall quality moved: the only place that question is answered | a per-ticket verdict |

Thresholds: a number becomes a gate only after the A/A archive gives it (MongoDB dropped a static 10 % threshold at
up to 99 % false alerts; D84's -15 is two sd of our own A/A). Until the archive holds three gates, the per-reference
guard is "below the previous gate by more than that reference's own measured spread", and the aggregate is read as
D84 reads it: paired per reference, median of the paired deltas (never `median(new) - median(old)`), a reference
that failed on one side recorded, not dropped.

Consequences: the trace counter is one instrumentation ticket before any kind-A proof (counts keyed by (move,
option class) at `PobSession.trial_stats`, generated counts at each gear or gem filler's candidate list, written next to
`moves` in `results.json` by `benchmark.py` and `replay_bench.py`). The queued kind-A pairs of 10 tickets (#392 #438 #432
#434 #437 #426 #427 #428 #429 #430) are cancelled, the running `392-after` with them (its `before`, Run #479, is
the first gate sample); #447 (the pair for #419, an evaluation fix) becomes a kind-B bench; the kind-B pairs (#174
#179 #188 #398 #464, #7) stay queued as the owner allows, behind the P0 proofs, and each kind-B ticket
gets the bench first. Principle 6 is reworded, the rule lives
in `docs/TESTING.md`, the owner's words in
`docs/research/2026-10-02-paired-run-cost-grill.md`. Not decided here: the sentinel set for kind B stays the smoke
six until per-build A/A data says otherwise; the gate's seed count is resized once three gates exist.

## D113 amd 1 and amd 2 (2026-10-05, #568, #570): removed with the old machine set-up

Both sized the weekly core run's worker count on the owner's PC (amd 1: one per physical core; amd 2: the free
slots of the host at start). The weekly core run is now a heavy run on CI runners; its worker count follows the
runner it gets (`docs/ci.md`). One reading rule of both stays: a build stopped by a wall-clock budget moves with
per-worker speed, so such rows are named when two runs are compared.
