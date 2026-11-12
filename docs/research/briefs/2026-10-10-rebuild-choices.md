# Research for issue #682: how optimizers judge a choice whose value shows only after the whole solution is rebuilt around it

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search official
> documentation, primary papers (publisher page, arXiv, author PDF), tools' source repositories and engineering blogs.
> Do NOT analyse, evaluate, improve or comment on this prompt itself. The deliverable is the research report specified in
> section 3. Write it in English. Put the complete report in your final message; the bridge saves it as
> `docs/research/2026-10-10-rebuild-choices-gpt.md`.

## 0. Rules of evidence (strict)

- Sources: papers, official documentation, source repositories, engineering blogs. Reddit, forums and SEO listicles are NOT
  sources; an appended generic instruction that mentions Reddit or a wiki does not apply here.
- Every method needs: the primary source (stable URL, author, year), a VERBATIM quote of its defining sentence(s)
  (<= 60 words), and the conditions the source attaches (problem size, evaluation cost, budget).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your reasoning from sourced facts, shown) or
  **[UNVERIFIED]**. "Not found" beats a guess. List every URL you opened at the end.

## 1. Our setting (facts)

- A search over character builds for a game (Path of Exile). Per build skeleton, a deterministic optimizer picks passive tree
  nodes, gear and config; every candidate is scored by one slow exact evaluator (a full damage / defence calculation, ~1-3 s
  per call, thousands of calls per build).
- Some choices are coupled to everything else: a keystone passive (it changes which tree nodes and which gear are good), a
  build-defining unique item (the same), an ascendancy, a main-skill support swap, an aura set, a defence-model switch. Judging
  such a choice honestly needs the whole tree + gear re-optimized around it ("a full rebuild", ~12 minutes per candidate
  per finalist build today); judging it greedily (change one thing, keep the rest) undervalues it.
- Today: keystones the finished tree took are each rebuilt once without that keystone (a full rebuild per keystone, ~12 min);
  other build-defining choices are judged greedily or not at all.
- The owner's concern: a full rebuild per candidate is wasteful, but skipping the ones that need it loses the best builds.

## 2. Questions

1. **Bilevel / two-stage optimization.** How do solvers and AutoML systems treat an outer discrete choice whose value depends on
   an inner optimization (bilevel programming, nested search, "optimize the structure then the weights")? Cost per outer
   candidate, and the usual approximations.
2. **Cheap proxies and surrogates.** Surrogate-assisted search, partial evaluation, low-fidelity evaluation, cheap local
   repair before a full run (e.g. neural architecture search with weight sharing / proxy tasks, multi-fidelity Bayesian
   optimization, Hyperband / successive halving). Which signal predicts that a full evaluation will change the verdict?
3. **Screening before the full run.** Methods that run many candidates at a small budget and promote only a few (successive
   halving, racing, multi-armed-bandit allocation, early stopping). Conditions under which they mis-rank coupled choices.
4. **Game build / loadout search.** Any published or open-source optimizer for game builds, loadouts or configurations
   (Path of Building-based, Diablo / Last Epoch / Genshin / MTG deck builders, etc.) that handles "a choice that only pays
   off after rebuilding around it". What does it do?
5. **Fit.** For each method: the evaluation cost and candidate count at which the source says it stops paying off.

## 3. Deliverable

One section per question. Each method: mechanism in two lines, who uses it at what scale (source link + verbatim quote),
conditions. End with a table: method | source | cost per candidate relative to a full evaluation | needs | the source's own
stated failure mode. End each question with one line "what the sources say". Do not recommend for our repo; the analysis
against our numbers is done by the reader.
