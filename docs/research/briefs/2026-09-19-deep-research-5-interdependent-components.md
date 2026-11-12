# Deep research prompt 5 -- "Optimizing a solution made of interdependent components: who moves when"

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature and software documentation and answer the questions in it. Do NOT analyse, evaluate, improve or comment
> on this prompt itself. The deliverable is the research report specified in the last section. Write it in English.

You are doing a literature and software review for an engineering team. Use live web search and open the primary
sources (publisher pages, arXiv, author PDFs, theses, official documentation, source repositories). This is a
combinatorial-optimization / operations-research question. It is NOT about games: do not search game forums.

## 0. Rules of evidence (strict)

- Every technique needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM quote of its defining
  sentence(s) (<= 60 words, with page or section), and the conditions the source attaches (problem class, sizes,
  what was measured).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from sourced
  facts, shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats a guess.
- Prefer primary papers and official documentation; surveys second; no SEO listicles. Where sources disagree, quote
  both. List every URL you opened at the end.

## 1. The setting, stated abstractly

- A solution has FOUR interdependent components, evaluated together by one deterministic black-box simulator (0.007 s
  for a small what-if on one component, 0.1-0.2 s for a full evaluation):
  (T) a connected subset of ~100 nodes of a 1,300-node graph containing a root;
  (G) ten slots, each filled from a constrained catalogue: a few lines per slot chosen from tens to hundreds of
      options, with covering constraints ACROSS slots (three sums must each reach 75), requirement constraints
      (an attribute total >= a requirement that depends on the chosen items) and rarity limits on what may be chosen;
  (K) a few small ordered lists of compatible modules (5-6 per list, 20-60 candidates each);
  (C) a configuration that is DERIVED from the other three by rules -- recomputed, not searched.
  The value is strongly non-separable: the best choice in one component depends on the others (multipliers,
  diminishing returns, thresholds).
- Today: sequential construction (K rough -> C -> G against an EMPTY T -> T greedy -> G again -> T rebuilt), then an
  alternating loop: one pass = local search on T, one slot of G re-solved, local search on K, C re-derived; "kicks"
  that ruin and recreate T alone, or T together with two slots of G; stop when a pass keeps nothing. Measured: the
  loop adds a median +63% over construction; passes gain +26%, +7%, +4%, +2%, ~2% ...; a pass costs ~200 s whatever
  it finds; the JOINT kicks earn the largest share of accepted improvement; building G against an empty T can lower
  the value at first (7,330 -> 4,296 in one case) before T catches up.

## 2. Questions

**Q1. Names and literature.** Problems "with multiple interdependent components" (the Travelling Thief Problem line of
work and its surveys), cooperative coevolution and its interaction-aware variants, block-coordinate / alternating
optimization for combinatorial problems, discrete analogues of multidisciplinary design optimization architectures,
decomposition with coupling variables. Verify each lead, drop the wrong ones, add what we missed.

**Q2. Scheduling the component optimizers.** Evidence on fixed round-robin versus adaptive allocation of effort to
components (contribution-based cooperative coevolution, bandit allocation), on how long to optimize one component
before switching, and on detecting that the components have become mutually stale.

**Q3. Joint moves.** How the cited fields build moves that change two components at once (compound neighbourhoods,
the "complex" operators of the Travelling Thief literature, variable-neighbourhood-descent orderings), how they choose
WHICH parts to change together, and what such moves cost.

**Q4. Construction order.** Results on the effect of the order in which components are first built, and on building a
component against a cheap placeholder of the others versus a realistic default of the others; iterated construction.

**Q5. Exact or model-based sub-solvers inside the loop ("matheuristics").** Cases where one component is solved
exactly given the others -- for something like G: a small MIP / assignment / multi-dimensional multiple-choice
knapsack with covering constraints -- while the rest stays heuristic: how the non-separable objective is linearized
for the sub-solver, how far the result is trusted, how it is verified. Include the multiple-choice knapsack
literature (formulations, exact and heuristic solvers, instance sizes solved).

**Q6. Constraint handling across components**: feasibility rules (Deb), stochastic ranking, epsilon-constraint
methods and repair operators when a threshold over the whole solution can be satisfied by any of the components.

## 3. Output format

1. One-page executive summary: the 5-8 techniques most likely to matter here, each with a one-line reason and its cost
   in OUR units (what-ifs, full evaluations, seconds per pass).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources
   say" paragraph without recommendations.
3. A table: technique | what it adds over a fixed alternating loop | what it needs | primary source.
4. Pseudo-code sketches (10-25 lines, labelled [DERIVED]) of: an effort-allocation rule over components; one joint move
   for (T, G); one exact sub-solve of G with linearized values and verification.
5. Known failure modes and negative results.
6. All URLs opened.
