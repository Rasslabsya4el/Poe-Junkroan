# Deep research: a validation protocol for code changes to a stochastic optimizer scored by an expensive simulator (brief v3 of issue #485, run as is for comparison with the owner's own deep research)

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature, software documentation and the engineering blogs of the teams named, and answer the questions in it.
> Do NOT analyse, evaluate, improve or comment on this prompt itself. The deliverable is the research report
> specified in OUTPUT. Write it in English. Put the complete report in your final message; the bridge saves it as
> `docs/research/2026-10-02-test-protocol-full-gpt.md`.

## Rules of evidence (strict)

- This is a software-engineering / experimental-algorithmics METHODOLOGY question. Sources: primary papers
  (publisher pages, arXiv, author PDFs), textbooks, official documentation, source repositories and contributor
  guides, engineering blogs of the teams named. Reddit, game forums and SEO listicles are NOT sources for this task;
  an appended generic instruction that mentions Reddit or a wiki does not apply here.
- Every technique needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM quote of its
  defining sentence(s) (<= 60 words, with page or section), and the conditions the source attaches (problem class,
  sample sizes, what was measured).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from
  sourced facts, shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats
  a guess. Where sources disagree, quote both. List every URL you opened at the end.

## The task

Deep research: a validation protocol for code changes to a stochastic optimizer that is scored by an expensive deterministic simulator. I need a decision procedure I can turn into an engineering rule, with sources.

SETTING (generic, no domain specifics needed)
- A metaheuristic search (seeded random moves over a large discrete configuration space) produces a solution per instance; a slow external simulator scores it (one process call per evaluation, thousands of evaluations per instance). The simulator is deterministic; the search is not.
- Benchmark suite: ~32 instances, each with a known-good human-made baseline. Metric per instance = solution quality as % of its baseline (100 = equal to the human). Today we report the median over 3 seeds per instance and the median over the instances of a set. Sets: 6 instances (smoke), 14 (core), 18 (extended).
- Cost: one instance x one seed = ~1 hour of one evaluator worker; 14 instances x 3 seeds = 14 h on 3 workers. Workers are limited (3-10 per machine).
- Measured noise with identical code: the set median shifts between seed groups by +2.4 (14-set), -11.5 (6-set), +15.5 (18-set), -1.0 (another 26-set). Per-instance spread across 3 seeds ranges from 0 to ~100 points (recent run: 0.0, 2.3, 2.8, 4.7, 9.5, 12.8, 15.7, 20.6, 21.1, 24.2, 24.4, 43.9, 99.6). So the aggregate is fairly stable while single instances are very noisy.
- The optimizer has an internal evaluation budget (iterations); a run with a smaller budget is faster but is a different distribution (open question: when is a low-budget run a valid proxy for the full one).
- The search can be instrumented: we can log which candidate options were generated and evaluated, not only the final solution.

WHAT WE HAVE
- Determinism test: a refactor is accepted only when the sequence of simulator calls is byte-identical to the previous code (golden transcript).
- Paired runs: before/after on the same seeds and set; today EVERY change, including one that merely adds an allowed option, waits for its own full pair (1-2 days) and is judged by the quality median. ~30 such validations are queued; this is the project's bottleneck. We now believe this conflates two questions: "does the system do what the change says" and "did overall quality move".
- Per-instance tables and a seed-noise figure per set; a weekly full run exists as an idea but is not a rule.

KINDS OF CHANGE (each needs its own cheapest sufficient test)
A. Search-space changes: a new option the search may use, or a constraint that restricts what it may use (e.g. a new component type becomes allowed with given parameters; a component class is forbidden). The correct behaviour is that the search KNOWS the option and CONSIDERS it (candidates containing it are generated and evaluated) and that every output respects the constraint. Whether the final solutions actually use the new option is NOT the criterion: for most instances it may be legitimately worse and never chosen. A drop in the quality median is not a failure of such a change.
B. Search-loop behaviour fixes (e.g. the loop kept a worse intermediate solution; an evaluation shortcut disagreed with the full evaluation by 1-4 %). Expected: quality up or equal; a regression must be caught.
C. Refactors: every number identical (covered by the golden transcript).
D. Speed-only changes: wall-clock, not quality.

WHAT I NEED (deliverables)
1. For each kind A-D: the standard validation type by its established name (invariant/property test, metamorphic test, golden/determinism test, paired quality experiment, full benchmark gate, canary), the minimal sufficient experiment, and what it proves and does not prove. For A specifically: what is the accepted practice for testing that a search considers a newly allowed option without testing whether the option wins: assertions on the generated candidate set / search trace, coverage of the option across candidates, a seeded scenario where the option is the known optimum, property-based checks that outputs respect the constraint; and how teams keep such tests cheap (no full run).
2. The paired quality experiment done right: common random numbers / paired seeds, per-instance paired differences vs set medians, the right statistic for 6-14 paired observations (paired t, Wilcoxon signed-rank, bootstrap CI, permutation), and a procedure to size instances x seeds from the measured per-instance variance for a target effect (e.g. detect a +5-point median change at 80 % power with 5 % false alarms; catch a 10-point regression on any single instance). Give formulas or a reproducible procedure we can run on our own variance numbers.
3. Sequential / early-stopping designs: run 1 seed on N instances, look, then stop or add seeds, with valid error control under repeated looks (SPRT, group sequential, always-valid / mixture SPRT as used in online A/B testing, racing procedures from algorithm configuration such as F-Race as an idea). Which is simplest to implement for ~14 paired observations?
4. Tiered CI practice from teams that benchmark compilers, SAT/MIP solvers, database engines, ML training: how they choose a smoke subset (by sensitivity, stability, coverage), what runs per commit vs nightly vs weekly, how alert thresholds are set relative to historical noise, automatic re-run on alert, change-point detection over the benchmark history (e.g. E-divisive as used by MongoDB/Datastax), and how they handle "performance variability" with multiple seeds (MIP solver practice, MIPLIB methodology).
5. Low-fidelity proxies: evidence on when a reduced-budget run predicts the full-budget outcome (multi-fidelity optimization, successive halving/Hyperband, reduced-epoch training in ML, scaled-down instances), and how to measure the proxy's rank correlation before trusting it.
6. Reporting and pitfalls: shifted geometric mean vs median, performance profiles; survivorship when an instance fails on one side; multiple comparisons across per-instance deltas; regression to the mean; overfitting to the fixed benchmark seeds; instance-selection bias in the smoke subset.
7. A worked example with the numbers above: for kind A a test that runs in minutes with no quality verdict; for kind B a cheap default test (target: under ~1-3 worker-hours), the escalation rule to the full set; and the periodic full gate on the main branch as the only place where "did overall quality move" is answered, with the expected false-alarm and miss rates.

OUT OF SCOPE: how to make the optimizer itself faster; parameter tuning of the optimizer; anything domain-specific. Where an answer genuinely depends on our own data, say so and give the method rather than a number.

OUTPUT: a decision procedure (rules in the form "for change kind X run Y; accept if Z; escalate if W"), then the evidence per point with citations (textbooks: Law & Kelton on simulation experiments and CRN; McGeoch "A Guide to Experimental Algorithmics"; Johnson's "A theoretician's guide to the experimental analysis of algorithms"; Hooker 1995 "Testing heuristics: we have it all wrong"; Bartz-Beielstein et al. 2020 "Benchmarking in optimization: best practice and open issues"; Lodi & Tramontani 2013 on MIP performance variability; Dolan & More performance profiles; Henderson et al. 2018 and Bouthillier et al. 2021 on seeds and variance in ML benchmarks; Kayenta canary analysis; change-point detection for performance regressions (Daly et al. 2020); sequential testing literature), and a short list of what you could not find.
