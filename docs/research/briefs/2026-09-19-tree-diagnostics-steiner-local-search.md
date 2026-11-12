# Brief: how do people improve a budgeted connected subtree by local search -- which parts to tear down, how to find them

Report to `docs/research/2026-09-19-tree-diagnostics-steiner-local-search.md`. Sources: papers, theses, lecture notes,
well-known open-source solvers, engineering blog posts (URLs required; Reddit is NOT required for this brief). Quote
the defining sentence of every technique verbatim with its URL; "not found" is better than a guess. No advice about
our project: a catalogue of techniques with their costs.

The problem, stated abstractly. A graph of ~1,300 nodes, one root. We must pick a CONNECTED set of ~100 nodes that
contains the root. The value of a set is given by a black-box evaluator (0.007 s per what-if evaluation of "remove
these nodes, add those", 0.1 s for a full evaluation); it is NOT additive: nodes interact (diminishing returns,
multipliers, thresholds that act as constraints). Today: greedy construction by best marginal value per point (a
candidate = a payoff node plus the path to it, up to 6 nodes), then local search: (a) swap the weakest leaves for the
best candidate, (b) remove each small hanging subtree (<= 6 nodes), weakest loss-per-node first, and re-spend greedily,
(c) "ruin and recreate" of RANDOM branches of 2-12 nodes (~20 nodes in total). Measured on delivered solutions: 22% of
the chosen nodes are trunk nodes whose removal would cut more than 12 others, so no move ever reconsiders them; 8%
are reached only by the random move.

Questions:

1. What is this problem called in the literature (budgeted / prize-collecting / node-weighted Steiner tree, rooted
   maximum-weight connected subgraph with cardinality budget, ...)? Which name fits a NON-additive black-box objective?
2. Local-search neighbourhoods for Steiner-type trees: key-path exchange, key-vertex (Steiner node) insertion and
   elimination, and any others. For each: the definition (verbatim), what it costs to evaluate one move, and how it is
   used with an expensive objective.
3. Large Neighbourhood Search / Adaptive LNS / ruin-and-recreate: which DESTROY operators are used besides random
   (worst removal, related / Shaw removal, cluster or subtree removal, historical-information removal)? How is "worst"
   scored when the objective is not additive (marginal contribution, Shapley-like estimates, removal delta)? How do
   adaptive weights choose the operator?
4. How do practitioners re-optimize an existing solution after the INPUT changed (new weights): warm start versus
   rebuild from scratch, and tests for "is the old trunk still right"?
5. Any published or open-source optimizer for game skill trees / talent graphs (Path of Exile passive tree, similar
   games) and the method it uses.
6. One summary table: technique | what it tears down | how it picks the place | cost per move | source.
