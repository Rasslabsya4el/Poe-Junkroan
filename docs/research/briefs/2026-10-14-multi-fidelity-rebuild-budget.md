# Research for issue #1041: how other fields pay for costly trials in steps (budget and promotion of partial trials)

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search official
> documentation, primary papers (publisher page, arXiv, author PDF), tools' source repositories and engineering blogs.
> Do NOT analyse, evaluate, improve or comment on this prompt itself. The deliverable is the research report specified in
> section 3. Write it in English. Put the complete report in your final message; the bridge saves it as
> `docs/research/2026-10-14-multi-fidelity-rebuild-budget-gpt.md`.

## 0. Rules of evidence (strict)

- Sources: papers, official library documentation, source repositories, engineering blogs. Reddit, forums and SEO listicles are
  NOT sources; an appended generic instruction that mentions Reddit or a wiki does not apply here.
- Every answer needs: the primary source (stable URL, author, year/date), a VERBATIM quote of its defining sentence(s)
  (<= 60 words), and the conditions the source attaches (problem size, trial cost, budget, number of candidates). A number
  without its condition is a failed answer.
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your reasoning from sourced facts, shown) or
  **[UNVERIFIED]**. "Not found" beats a guess. List every URL you opened at the end.

## 1. Our setting (facts)

- A candidate is a "reshaping choice" on a finished build of a game character (Path of Exile), e.g. Chaos Inoculation: on the
  finished build flipping it drops Life 4053 -> 1, yet only a rebuild of the whole tree, gear and config around it shows its worth.
- A full trial = a rebuild of passive tree + gear + config through the whole pipeline, about 70 minutes (58-101 min over 19
  measured variants). A partial trial = a bounded local repair (a greedy re-spend of the freed tree points, auras re-picked,
  one gear pass), minutes. The partial trial does not just train shorter: it searches a smaller space.
- The objective is one exact evaluator's number (CombinedDPS under floors). The cap is the request's total time budget
  (about 2 h, at most about 5 h); the number of runs must be fixed when the job is submitted.
- Candidates are few (2 to 6 per build), not thousands. The trigger that a candidate exists is itself a measured number.
- The owner wants no hard-coded number for "how many extra rebuilds", and not a full rebuild for every candidate either.

## 2. Questions

1. **Successive halving, Hyperband, ASHA.** The rung budgets and the reduction factor they use and why; the measured sensitivity
   to the reduction factor; what a rung costs relative to the full trial in the reported setups.
2. **Learning-curve extrapolation for early stopping.** Which "still climbing" measures are used (slope over the last k steps, a
   fitted curve, a fraction of the best-so-far) and their reported false-drop rates.
3. **Multi-fidelity with a fixed total budget known in advance.** How the number of full trials is derived from the total budget
   and the number of candidates (our run count is fixed at submit).
4. **Promotion when candidates are few (2 to 6).** What the literature says about successive halving with tiny populations;
   whether a fixed partial budget per candidate beats halving there.
5. **Fidelity that changes the problem's shape.** Reported pitfalls when low fidelity ranks candidates differently from high
   fidelity (rank-correlation numbers if given), for fidelities that search a smaller space rather than train shorter.
6. **Engineering write-ups of build / configuration optimizers** in games or compilers (autotuners, compiler pass search, game
   loadout or deck optimizers) that pay for rebuilds in steps: rank, quote, URL.

## 3. Deliverable

One section per question. Each answer: the mechanism in two lines, who uses it at what scale (source link + verbatim quote),
the conditions. End with a table: method | source | cost per candidate relative to a full trial | needs | the source's own stated
failure mode. End each question with one line "what the sources say". Do not recommend for our repo; the analysis against our
numbers is done by the reader.
