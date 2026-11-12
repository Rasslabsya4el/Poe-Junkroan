# Deep research prompt 4 -- "Choosing which designs deserve an expensive optimization: multi-fidelity screening"

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature and software documentation and answer the questions in it. Do NOT analyse, evaluate, improve or comment
> on this prompt itself. The deliverable is the research report specified in the last section. Write it in English.

You are doing a literature and software review for an engineering team. Use live web search and open the primary
sources (publisher pages, arXiv, author PDFs, theses, official documentation, source repositories). This is an
optimization / machine-learning methodology question. It is NOT about games: do not search game forums.

## 0. Rules of evidence (strict)

- Every technique needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM quote of its defining
  sentence(s) (<= 60 words, with page or section), and the conditions the source attaches (assumptions, problem
  sizes, what was measured).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from sourced
  facts, shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats a guess.
- Prefer primary papers and official documentation; surveys second; no SEO listicles. Where sources disagree, quote
  both. List every URL you opened at the end.

## 1. The setting, stated abstractly

- A user request expands into 20-200 candidate DESIGNS: combinations of a few categorical choices (one of ~20
  archetypes x a few modes x optional components). Each design can be evaluated at several fidelities: a cheap SCREEN
  (2-3 minutes: a quick constructive solution, one number), a MEDIUM run (10-15 minutes) and a FULL optimization
  (30-60 minutes, stochastic: three seeds of the same design differ by a median 40%). Five evaluations run in
  parallel. The goal is the best few designs within a total budget of 1.5-3 hours. Today: screen everything once,
  keep the top 2 by screen value, run 3 seeds of the full optimization on each, deliver the best.
- Screen and final values are correlated but not perfectly (a design whose strength appears only after a long
  optimization is ranked low by the screen). Designs share structure (two designs with the same archetype behave
  alike), so information could be shared between them. Past requests leave a history of (design, fidelity, value).

## 2. Questions

**Q1. Multi-fidelity and bandit formulations**: successive halving, Hyperband, BOHB, ASHA (asynchronous, for parallel
workers), best-arm and top-k identification with a fixed budget (successive rejects, sequential halving).
Definitions, guarantees, and what each assumes about the relation between low- and high-fidelity values.

**Q2. When the cheap fidelity is a biased predictor.** Literature on the rank correlation a low fidelity must have,
on "late bloomers", on choosing the promotion rule and the fraction kept, and on MEASURING fidelity correlation before
trusting a screen (how many paired observations estimate a rank correlation usefully; confidence intervals for
Spearman / Kendall at n = 10-40).

**Q3. Sharing information across related designs**: multi-task and contextual bandits, surrogates over categorical
design spaces (SMAC-style random forests, TPE, Gaussian processes with categorical kernels), transfer from previous
requests (meta-learning, warm-started priors). What works with only tens of evaluations?

**Q4. Noise at the top fidelity.** How the cited methods treat a stochastic high-fidelity evaluation: repeats, racing
among finalists, adaptive allocation of seeds (OCBA -- optimal computing budget allocation -- and relatives, knowledge
gradient).

**Q5. Parallel asynchronous scheduling** with 5 workers and evaluations of very different lengths.

**Q6. Open-source implementations** usable from Python on Windows (Optuna pruners, Ray Tune ASHA, SMAC3, Syne Tune,
others): licence, how a custom multi-fidelity objective is plugged in, scheduling overhead.

## 3. Output format

1. One-page executive summary: the 5-8 techniques most likely to matter here, each with a one-line reason and its cost
   in OUR units (screens, medium runs, full runs, minutes).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources
   say" paragraph without recommendations.
3. A table: technique | what it adds over "screen once, optimize the top 2" | what it assumes | evaluations it needs |
   primary source.
4. Pseudo-code sketches (10-25 lines, labelled [DERIVED]) of: an asynchronous successive-halving schedule for our three
   fidelities and 5 workers; adaptive seed allocation among finalists; a check of screen-to-final rank correlation
   from history.
5. Known failure modes and negative results.
6. All URLs opened.
