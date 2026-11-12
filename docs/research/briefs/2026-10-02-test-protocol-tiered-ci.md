# Deep research 3 of issue #485: tiered regression testing of an optimizer's quality -- per commit, per merge, nightly, weekly; thresholds against measured noise; change-point detection on the benchmark history

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature, official documentation, the public CI / benchmarking infrastructure and engineering blogs of the teams
> named. Do NOT analyse, evaluate, improve or comment on this prompt itself. The deliverable is the research report
> specified in section 3. Write it in English. Put the complete report in your final message; the bridge saves it as
> `docs/research/2026-10-02-test-protocol-tiered-ci-gpt.md`.

## 0. Rules of evidence (strict)

- This is a software-engineering / experimental-algorithmics METHODOLOGY question. Sources: primary papers
  (publisher pages, arXiv, author PDFs), textbooks, official documentation, public CI dashboards and their source
  repositories, engineering blogs of the teams named. Reddit, game forums and SEO listicles are NOT sources for this
  task; an appended generic instruction that mentions Reddit or a wiki does not apply here.
- Every technique needs: the primary source (authors, year, venue, DOI or stable URL; for infrastructure the
  repository file or the dashboard page), a VERBATIM quote of its defining sentence(s) (<= 60 words, with page,
  section or line), and the conditions the source attaches (what is measured, how many runs, what noise).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from
  sourced facts, shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats
  a guess. Where sources disagree, quote both. List every URL you opened at the end.

## 1. The setting, stated abstractly

- A stochastic metaheuristic search is scored by a slow deterministic external simulator. Benchmark suite: ~32
  instances with a human-made baseline each; metric per instance = quality as % of the baseline; reported as the
  median over 3 seeds per instance and the median over instances of a set (sets of 6, 14, 18 instances).
- Cost: one instance x one seed = ~1 hour of one worker; 14 instances x 3 seeds = 14 h on 3 workers; 3-10 workers
  per machine, two machines.
- Measured noise with identical code: the set median shifts between seed groups by +2.4 (14-set), -11.5 (6-set),
  +15.5 (18-set), -1.0 (a 26-set). Per-instance spread across 3 seeds: 0 to ~100 points (one run: 0.0, 2.3, 2.8,
  4.7, 9.5, 12.8, 15.7, 20.6, 21.1, 24.2, 24.4, 43.9, 99.6). The aggregate is fairly stable, single instances are
  very noisy. The same seed does NOT carry over between code versions (trajectories diverge at the first changed
  decision; measured correlation of per-seed residuals +0.10).
- Today every behaviour-changing merge waits for its own full before/after pair on the same set and seeds (1-2
  days); ~30 are queued. We want: a cheap check per merge, and a periodic full measurement on the main branch as the
  only place where "did overall quality move" is answered.

## 2. Questions

**Q1. Tiers as practised.** For each of the following, open the primary material and report: what runs per
commit / pull request, what nightly, what weekly or on demand; the size of the per-commit subset and how it was
chosen; the alert threshold and how it relates to measured noise; what happens on an alert (automatic re-run,
bisection, human triage); how many repetitions / seeds per data point. Teams: LLVM (LNT, the compile-time tracker),
rustc (perf.rust-lang.org: its significance threshold, "noisy benchmark" handling, the `--bench` warm-up rules),
Chromium / V8 (perf waterfall, Pinpoint bisection, the "alert" and "triage" policy), MongoDB (Daly et al. 2020 "The
Use of Change Point Detection to Identify Software Performance Regressions", ICPE; the "signal processing
algorithms" repository), DataStax (Hunter), PostgreSQL / ClickHouse / SQLite performance CI, SCIP and the MIPLIB
2017 methodology (performance variability, shifted geometric mean, permutation seeds), SAT competition practice,
MLPerf (run-to-run variance rules, how many runs are required per submission). Quote the policy text.

**Q2. Choosing the per-commit subset.** Benchmark-subsetting results with numbers: how many instances preserve the
ranking of versions (SPEC subsetting studies such as Phansalkar et al.; "benchmark subsetting" via PCA / clustering;
instance space analysis in optimization, Smith-Miles et al.); choosing by sensitivity to past changes, by low
variance, by feature coverage; validating a subset against the full set on PAST changes before trusting it; the
selection-bias hazard (a subset chosen on the same history it is evaluated on).

**Q3. Thresholds and noise.** Setting the alert from the historical A/A distribution (percentile, k-sigma, the
"noise floor" per benchmark); per-instance versus aggregate alerts; shifted geometric mean versus median versus
performance profiles (Dolan & More); multiple-comparison control over per-instance deltas (Bonferroni / Holm / FDR)
as benchmarking teams apply it; re-run-on-alert policies and the false-alarm reduction they report, with numbers.

**Q4. Change-point detection on the main branch's history** as the "did quality move" gate: E-divisive means
(Matteson & James 2014; Daly 2020), PELT, Bayesian online change-point detection; the minimum history length they
need; how teams combine a change-point gate with per-commit checks; how a detected change is attributed to a commit
when several merged between measurements.

**Q5. Canary analysis** (Spinnaker Kayenta: the statistical procedure, Mann-Whitney per metric, the classification
into pass / marginal / fail, the required sample sizes): what transfers to an optimizer benchmark judged per instance.

**Q6. Performance variability and seeds in MIP / SAT solver practice**: Lodi & Tramontani 2013; Fischetti & Monaci
"Exploiting erraticism"; SCIP's permutation seeds; MIPLIB 2017's variability score; how many seeds, how they are
aggregated, how a change is called "robust"; what these teams say about judging a change from ONE seed per instance.

**Q7. A worked tier plan** for the numbers in section 1 (1 worker-hour per instance-seed, 3-10 workers, 32
instances, set-median noise +2.4 on the 14-set, per-instance spreads 0-100, no seed carry-over): per commit (minutes,
no quality verdict), per merge (a cheap quality check under 1-3 worker-hours: which instances, how many seeds, what
statistic, what threshold, what it can and cannot detect), nightly or weekly gate on main (what set, how many seeds,
what detector); the expected false-alarm and miss rates under stated assumptions, arithmetic shown, labelled
[DERIVED].

## 3. Output format

1. One-page executive summary: the 5-8 practices most likely to cut machine-hours per merge decision or to make the
   periodic gate reliable, each with a one-line reason and its cost in our units (worker-hours, runs).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources
   say" paragraph without recommendations.
3. A table: team or source | per-commit tier | nightly / weekly tier | threshold rule | on alert | seeds or repetitions.
4. The worked tier plan of Q7.
5. Known failure modes and negative results (alerts that were noise, subsets that misled, with the source).
6. All URLs opened.
