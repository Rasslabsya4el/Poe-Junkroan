# Deep research prompt 3 -- "Judging and tuning an expensive stochastic optimizer with very few runs"

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature and software documentation and answer the questions in it. Do NOT analyse, evaluate, improve or comment
> on this prompt itself. The deliverable is the research report specified in the last section. Write it in English.

You are doing a literature and software review for an engineering team. Use live web search and open the primary
sources (publisher pages, arXiv, author PDFs, theses, official documentation, source repositories). This is an
experimental-algorithmics / optimization-methodology question. It is NOT about games: do not search game forums.

## 0. Rules of evidence (strict)

- Every technique needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM quote of its defining
  sentence(s) (<= 60 words, with page or section), and the conditions the source attaches (problem class, sample
  sizes, what was measured).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from sourced
  facts, shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats a guess.
- Prefer primary papers and official documentation; surveys second; no SEO listicles. Where sources disagree, quote
  both. List every URL you opened at the end.

## 1. The setting, stated abstractly

- We develop a stochastic optimizer (construction + local search with random restarts). One RUN on one benchmark
  instance takes 30-60 minutes on one core and returns one number (higher is better). There are 32 benchmark instances
  of very different scales; results are compared as a ratio to a per-instance reference value. Five runs fit in
  parallel. A full campaign (32 instances x 3 seeds) costs about 28 machine-hours; a reduced "smoke" set (6 instances
  x 3 seeds) about 5 hours.
- Measured: for the same instance and the same code, three seeds differ by a median of 40% (max 109%). Today a code
  change is accepted when the 3-seed MEDIAN per instance does not get worse on the smoke set, then confirmed on the
  full campaign. Several code changes per day compete for the same machine.
- Runs are anytime: the best value over time is logged, so a run can be cut short or extended. The optimizer has about
  30 numeric knobs (time budgets, acceptance thresholds, sample sizes) set by hand.
- Seeds are explicit, so two code versions can run on the SAME seeds (common random numbers), although their
  trajectories diverge after the first different decision.

## 2. Questions

**Q1. Comparing two versions of a stochastic optimizer with few, expensive runs.** Best practice from the
experimental-algorithmics and metaheuristics-benchmarking literature: paired designs; common random numbers and how
much variance they remove once trajectories diverge; non-parametric paired tests and their power at n = 3-10;
bootstrap confidence intervals on medians and ratios; effect sizes (Vargha-Delaney A12 and relatives); aggregation
across heterogeneous instances (ratios, ranks, performance profiles, ECDFs of runtime-to-target as in COCO /
IOHprofiler). What sample sizes do authors report as the minimum for a defensible claim, and what is said about n = 3?

**Q2. Sequential and adaptive experimentation.** Racing (F-Race, iterated racing), sequential hypothesis tests,
successive rejects, best-arm identification with a fixed budget: how to stop a comparison early, how to spend more
runs on the instances / versions that are still undecided, and the guarantees given.

**Q3. Using anytime traces.** Methods that compare optimizers from PARTIAL runs (performance at checkpoints, area under
the anytime curve, extrapolation of convergence curves, early-stopping / learning-curve prediction from the
hyper-parameter-optimization literature): when is "value after 25% of the budget" a trustworthy predictor of the final
ranking, and how is that checked?

**Q4. Instance selection.** How to choose a small, representative subset of benchmark instances (instance space
analysis, clustering by features or by algorithm footprints, benchmark-reduction results): how large a subset
preserves the ranking of algorithm variants, with reported numbers.

**Q5. Automatic algorithm configuration under a tiny budget.** irace, SMAC, ParamILS, GGA, Hyperband / BOHB style
multi-fidelity tuning: requirements in number of runs, how they cope with 30-60 minute evaluations, capping / early
termination of bad configurations, and documented failure modes (over-tuning to the training instances).

**Q6. Reporting standards.** What recent guidelines on benchmarking optimization heuristics require for a claim
"version B is better than version A" (leads to verify: Bartz-Beielstein et al. 2020 "Benchmarking in Optimization: Best
Practice and Open Issues"; Hooker 1995 "Testing heuristics: we have it all wrong"; Johnson 2002 "A theoretician's guide
to the experimental analysis of algorithms"). Add what we missed.

## 3. Output format

1. One-page executive summary: the 5-8 practices most likely to cut our machine-hours per decision or to make our
   decisions more reliable, each with a one-line reason and its cost in OUR units (runs, machine-hours).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources
   say" paragraph without recommendations.
3. A table: practice | what it saves or improves | what it needs (runs, assumptions) | primary source.
4. Pseudo-code sketches (10-25 lines, labelled [DERIVED]) of: a paired sequential comparison of two versions with early
   stopping; a racing scheme over k versions; a check of whether partial-run rankings predict final rankings.
5. Known failure modes and negative results.
6. All URLs opened.
