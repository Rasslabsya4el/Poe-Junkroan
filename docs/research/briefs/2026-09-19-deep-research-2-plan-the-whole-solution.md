# Deep research prompt 2 of 2 -- "Planning the whole connected solution at once: surrogates, exact solvers, combining solutions, acceptance rules"

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature and software documentation and answer the questions in it. Do NOT analyse, evaluate, improve or comment
> on this prompt itself, its structure or its compatibility with any tools. The deliverable is the research report
> specified in the last section. Write the report in English.

You are doing a literature and software review for an engineering team. Use live web search and open the primary
sources (publisher pages, arXiv, author PDFs, theses, solver documentation and source repositories). This is a
combinatorial-optimization / operations-research question. It is NOT about games: do not search game forums, do not
discuss any game. Work until the questions below are answered from sources you actually opened.

## 0. Rules of evidence (strict)

- Every technique or solver you report needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM
  quote of the defining sentence(s) (<= 60 words, with page or section), and the conditions the source attaches
  (problem class, objective type, instance sizes, reported running times and hardware).
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your arithmetic or reasoning from sourced
  facts, shown step by step) or **[UNVERIFIED]** (not opened; allowed but never mixed with the other two).
- If a paper cannot be opened, say so and give the best open version. Do not reconstruct quotes from memory. "Not
  found" is a valid answer.
- Prefer primary papers and solver documentation; surveys second; no SEO listicles. Where sources disagree, quote
  both. List every URL you opened at the end.

## 1. The problem, stated abstractly

- An undirected graph G, about 1,300 nodes, a designated root r; sparse, "mostly tree-like with cycles" (a central
  ring, long corridors, many small clusters of 3-8 nodes hanging off them; average degree about 2.3).
- A solution S is a CONNECTED set of about 100 nodes containing r (cardinality budget B ~ 100, unit node costs).
- F(S) comes from a deterministic BLACK-BOX numerical simulator: NOT additive, NOT submodular. Some nodes multiply
  others, some only matter in pairs / groups, many have diminishing returns, and several hard constraints (a quantity
  must stay >= a threshold) enter as penalties. Connector nodes have little or no value of their own.
- Costs: a what-if evaluation "remove A, add B" relative to the current S: ~0.007 s; a full evaluation: ~0.1 s; a
  vector of estimated marginal values for EVERY node of G around the current S: ~17 s. Budget per solve: 10^4-10^5
  what-ifs (tens of minutes). Three independent runs (seeds) are affordable and today differ by a median 40% in
  final value.
- Today: greedy construction by best gain per node (candidate = payoff node + its path, <= 6 nodes), then local search
  (leaf swaps; remove-and-regrow of small hanging subtrees, weakest first; random ruin-and-recreate of ~20 nodes).
  Acceptance is strict improvement. 22% of the chosen nodes (the trunk near the root) are never reconsidered after
  construction. A companion review covers local-search neighbourhoods and destroy operators; THIS review is about
  methods that look at the whole solution.

## 2. Questions

**Q1. The additive surrogate as an exactly solvable problem.** If every node gets a weight w_v (our 17 s marginal-value
vector), "best connected set of <= B nodes containing r" is a rooted, cardinality- (or budget-) constrained
maximum-weight connected subgraph / node-weighted prize-collecting Steiner tree / k-cardinality tree variant.
(a) Give the exact names and the canonical formulations (flow-based, cut-based with separation, MTZ-style, tree
knapsack DP) with their primary sources. (b) Which SOLVERS handle the ROOTED + BUDGETED + NODE-WEIGHTED case out of
the box or with small changes -- check at least SCIP-Jack (which problem classes it accepts), heinz / BioNet-style
MWCS solvers, dual-ascent PCST solvers, pcst_fast, KCT-specific heuristics and libraries, and general MIP / CP-SAT
solvers (HiGHS, SCIP, OR-tools CP-SAT) with lazy connectivity cuts. These are LEADS that may be misremembered: verify
each. (c) Reported running times for instances near our size (1-2 thousand nodes, budget ~100, sparse), with hardware.
(d) For graphs that are trees or have small treewidth: the tree-knapsack dynamic programme (recurrence, complexity
O(n B^2) or better, known speed-ups) and how cycles are handled in practice (spanning-tree restriction, tree
decomposition, cycle-breaking enumeration).

**Q2. Using an additive (or low-order) surrogate for a non-additive black box.** Literature on iterating "estimate
weights around the incumbent -> solve the surrogate exactly -> evaluate the proposal with the true objective ->
re-estimate": successive linearization / sequential approximate optimization for COMBINATORIAL problems, trust-region
or local-branching style limits on how far the proposal may move (Hamming-distance constraints), acceptance tests that
compare predicted with actual improvement, and known failure modes (oscillation, connector nodes eating the budget,
thresholds invisible to additive weights). Include surrogate-assisted and Bayesian optimization over combinatorial
structures (quadratic / pairwise surrogates, e.g. BOCS-, COMBO-type methods) and say honestly whether they scale to
~1,300 binary variables with a connectivity constraint.

**Q3. Capturing interactions cheaply.** Methods that detect which variables must move together: pairwise interaction
screening, linkage learning from evolutionary computation (LTGA / GOMEA, DSMGA-type linkage models), group testing,
sparse Walsh / Fourier or polynomial surrogates, and how many evaluations they need for n ~ 1,300 with most
interactions local (nodes interact mainly within a cluster and with a few global multipliers).

**Q4. Randomized and population construction.** GRASP (restricted candidate lists, reactive GRASP) and iterated greedy
for Steiner / k-cardinality-tree problems; beam search over partial connected solutions; ant-colony or other
constructive metaheuristics that were competitive on KCT / PCST benchmarks. What parameters mattered, and the cost
relative to plain greedy.

**Q5. Combining good solutions.** Path relinking, elite sets, and recombination for tree / connected-subgraph
solutions: how two or three good solutions are merged (union graph + re-solve on the union, as in Steiner-tree
solvers; path relinking moves that keep connectivity), how connectivity and the budget are repaired, and measured
benefit over independent multi-start.

**Q6. Acceptance rules under a fixed evaluation budget.** Strict improvement versus simulated annealing, threshold
accepting, late-acceptance hill climbing, record-to-record travel, step-counting hill climbing: original definitions,
the parameters, and any comparisons on LNS-type searches where ONE candidate evaluation is cheap but REBUILDING a
region is expensive (our regrow costs 1-2 s per node against 0.007 s per what-if). Restart strategies and how to split
a fixed budget between a few long runs and many short ones.

**Q7. Knowing how good the result is.** Upper bounds available from the additive relaxation or from solver dual
bounds; statistical estimators of the optimum from multi-start samples; what the literature accepts as evidence that a
heuristic is near-optimal on instances with no known optimum.

**Q8. Open-source code worth reading**, with language, licence, problem classes supported, and how hard it would be to
call from Python on Windows.

## 3. Output format

1. One-page executive summary: which of these methods are realistic for the problem in section 1, each with its cost in
   OUR units (0.007 s what-ifs, 17 s marginal-value passes, 0.1 s full evaluations, solver seconds).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources say"
   paragraph without recommendations.
3. A table: method | what it adds over greedy + local search | evaluations / solver time it needs at our size | handles
   a root and a cardinality budget? | works with a black-box objective? (yes / no / via surrogate) | primary source.
4. A solver table: solver | problem classes (exact wording from its documentation) | rooted? budgeted? node weights? |
   licence | interface | reported times near our size.
5. Pseudo-code sketches (10-25 lines, labelled [DERIVED]) for: the tree-knapsack DP on a tree; one surrogate-solve-
   evaluate loop with a trust region; one recombination of three solutions.
6. Known failure modes and negative results.
7. All URLs opened.
