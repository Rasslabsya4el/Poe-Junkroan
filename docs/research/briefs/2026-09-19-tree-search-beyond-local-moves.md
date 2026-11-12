# Brief: beyond local moves -- surrogate models with exact solvers, randomized construction, combining solutions, acceptance rules

Report to `docs/research/2026-09-19-tree-search-beyond-local-moves.md`. Companion of
`docs/research/briefs/2026-09-19-tree-diagnostics-steiner-local-search.md` (same abstract problem: choose a CONNECTED
set of ~100 nodes containing a root in a graph of ~1,300 nodes, maximizing a NON-additive black-box objective with
constraints; one what-if evaluation 0.007 s, one full evaluation 0.1 s; a per-node marginal-value estimate for every
node of the graph is available in ~17 s). Sources: papers, theses, lecture notes, solver documentation, engineering
write-ups from operations research / combinatorial optimization (URLs required; Reddit NOT required; nothing about
games is needed here). Quote the defining sentence of each technique verbatim with its URL. "Not found" beats a guess.
No advice about our project: a catalogue with costs and known pitfalls.

1. **Additive surrogate + exact or near-exact solver, iterated.** With per-node values as weights the problem becomes
   a rooted budgeted prize-collecting Steiner tree / maximum-weight connected subgraph with a cardinality budget. What
   solves instances of this size (1,300 nodes, budget 100) and how fast: dynamic programming on tree-like graphs (tree
   knapsack), ILP / branch-and-cut formulations, dedicated heuristics and open-source solvers? How is such a surrogate
   solution used when the true objective is non-additive (successive linearization / trust region around the current
   solution, re-estimating the weights and re-solving)? Known failure modes.
2. **Randomized construction**: GRASP (greedy randomized adaptive search, restricted candidate lists), iterated greedy,
   beam search over partial solutions. Parameters that matter, cost relative to plain greedy.
3. **Combining several good solutions**: path relinking, elite sets, crossover for connected-subgraph solutions (how
   connectivity is repaired).
4. **Acceptance rules for local search under a budget of evaluations**: strict improvement versus simulated annealing,
   threshold accepting, late-acceptance hill climbing, record-to-record travel; what is reported to work when one
   evaluation is cheap but a rebuild of a region is expensive.
5. **Estimating interactions cheaply**: pairwise interaction screening, grouping of variables that must move together,
   linkage learning; how many evaluations such estimates need.
6. One summary table: technique | what it adds over greedy + local search | evaluations it needs | source.
