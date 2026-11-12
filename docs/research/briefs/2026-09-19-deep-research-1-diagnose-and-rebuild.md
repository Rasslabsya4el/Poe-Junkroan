# Deep research prompt 1 of 2 -- "Where is a connected solution weak, and how do we rebuild that part?"

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature and software documentation and answer the questions in it. Do NOT analyse, evaluate, improve or comment
> on this prompt itself, its structure or its compatibility with any tools. The deliverable is the research report
> specified in the last section. Write the report in English.

You are doing a literature and software review for an engineering team. Use live web search and open the primary
sources (publisher pages, arXiv, author PDFs, theses, solver documentation, source repositories). This is a
combinatorial-optimization / operations-research question. It is NOT about games: do not search game forums, do not
discuss any game. Work until the questions below are answered from sources you actually opened.

## 0. Rules of evidence (strict)

- Every technique you report needs: the primary source (authors, year, venue, DOI or stable URL), a VERBATIM quote of
  the sentence(s) that define it (<= 60 words, with page or section), and the conditions the source attaches
  (problem class, objective type, instance sizes, what was measured).
- Separate three kinds of statement and label each one: **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your own
  arithmetic or reasoning from sourced facts, shown step by step), **[UNVERIFIED]** (you believe it but did not open a
  source -- allowed, but never mixed into the other two).
- If you cannot open a paper, say so and give the best open version (arXiv / author page / thesis chapter). Do not
  reconstruct quotes from memory. "Not found" is a valid answer and is better than a guess.
- Prefer primary papers and solver documentation over surveys; prefer surveys over blog posts; no SEO listicles.
- Where sources disagree, quote both sides.
- At the end list every URL you opened.

## 1. The problem, stated abstractly

- An undirected graph G with about 1,300 nodes and a designated root r. The graph is sparse and "mostly tree-like with
  cycles": a central ring, several long corridors, many small clusters (3-8 nodes) hanging off the corridors, average
  degree about 2.3.
- A solution S is a CONNECTED set of about 100 nodes containing r (a cardinality budget B ~ 100; all nodes cost 1).
- The value F(S) comes from a deterministic BLACK-BOX evaluator (a numerical simulator). F is NOT additive and NOT
  submodular: some nodes multiply the contribution of others, some only matter together (pairs / groups), many have
  diminishing returns, and several hard constraints ("floors": e.g. a quantity must stay >= a threshold) are part of
  the objective as penalties. Pure connector nodes have little or no value of their own.
- Evaluation costs: a what-if evaluation of "remove node set A and add node set B" relative to the current solution
  costs ~0.007 s as long as the result is connected; a full evaluation ~0.1 s; a vector of estimated marginal values
  for EVERY node of the graph (allocated or not) around the current solution costs ~17 s. Budget per solve: on the
  order of 10^4-10^5 what-if evaluations (tens of minutes); three independent seeds are affordable.
- The INPUT changes over time: the evaluator's other inputs (not the graph) are re-optimized in alternation with S,
  and later the whole instance is re-solved with a larger budget (B = 110, 120, ...) and different evaluator inputs.
  We then want to REUSE the old solution but must be able to change its early parts.

## 2. What we do today (so you can position the literature against it)

1. Greedy construction: repeatedly add the candidate with the best value gain per node, where a candidate is a payoff
   node plus the path to it (up to 6 nodes).
2. Local search, alternating: (a) swap the weakest leaves for the best candidate of equal size; (b) for every small
   hanging subtree (<= 6 nodes, i.e. what falls off when one node is cut) in order of smallest loss per node: remove
   it, re-spend the freed nodes greedily, keep if better; (c) "ruin and recreate": remove RANDOM branches of 2-12 nodes
   (about 20 nodes in total), regrow greedily, keep if better.
3. Measured on delivered solutions: 32% of chosen nodes are leaves and 38% sit in hanging subtrees of 2-6 nodes (both
   are reconsidered every pass); 8% sit in subtrees of 7-12 nodes (only the random move reaches them); 22% are TRUNK
   nodes (cutting them would drop more than 12 others) and no move ever reconsiders them after construction. Three
   seeds of the same instance differ by a median 40% in final value. Ruin-and-recreate accounts for the largest share
   of accepted improvement, which we read as "the local moves are too small".

## 3. Questions

**Q1. Names and neighbouring fields.** Under which names is this problem (or its additive / submodular relaxations)
studied? Check at least, and report for each what objective structure it assumes and what its best practical
heuristics are: k-cardinality tree / k-MST / quota and budgeted Steiner tree; (rooted, budgeted) prize-collecting
Steiner tree; (rooted, cardinality-constrained) maximum-weight connected subgraph (incl. bioinformatics "active
module" tools); connected submodular maximization and submodular orienteering / informative path planning with
connectivity; conservation-planning "connected reserve / wildlife corridor design" under a budget; connected facility
location; network design with connectivity. These names are LEADS that may be misremembered -- verify each, drop the
wrong ones, add the ones we missed.

**Q2. Neighbourhoods for tree-shaped solutions.** Define precisely (with the original papers) the local-search
neighbourhoods used for Steiner-type and k-cardinality-tree problems: Steiner-vertex insertion / elimination,
key-path exchange, key-vertex elimination, path-based and "corridor" moves, subtree-swap / prune-and-regraft moves,
ejection chains, variable-depth (Lin-Kernighan-style) moves on trees. For each: which part of the solution it can
change (leaf, hanging subtree, interior path, branching node), the cost of scanning the neighbourhood, and -- most
important for us -- whether it was ever used with an objective evaluated by a black box rather than by edge-cost
arithmetic, and how candidate moves were pre-filtered cheaply in that case.

**Q3. Deciding WHAT to destroy (diagnosis).** In Large Neighbourhood Search / Adaptive LNS / ruin-and-recreate /
iterated greedy: catalogue destroy operators beyond random (worst removal, related / Shaw removal, cluster removal,
history-based removal, segment / path / subtree removal, "critical" or bottleneck-based removal) WITH their scoring
rules. Then the part we care about most: when the objective is non-additive, how is the "contribution" or "weakness"
of a component estimated? Compare leave-one-out / removal deltas, Shapley or Banzhaf value estimates (sampling
schemes and their evaluation counts), influence / sensitivity estimates, regret measures, and learned destroy policies
(machine-learning-guided LNS). Are there results on the SIZE of the destroyed region (adaptive destroy size, size
schedules) and on destroying CONNECTED regions versus scattered elements?

**Q4. Adaptive choice among operators and budgets.** ALNS roulette weights (the original formulation and its
parameters), bandit-based operator selection, and any evidence on when adaptive selection beats a fixed order; how
time per operator (not only success rate) is accounted for.

**Q5. Re-optimization after the input changed.** Literature on re-optimizing Steiner-type / connected-subgraph
solutions after weights or budget change ("reoptimization of Steiner trees" and relatives, warm starts in LNS,
solution repair, incremental / dynamic variants). Is there any principled test for "the old trunk is still right"
other than rebuilding and comparing? What is known about nesting solutions across budgets (is an optimal B-solution
close to contained in an optimal B+10-solution; incremental / "anytime" budgeted variants)?

**Q6. How to know how far from optimal we are without knowing the optimum.** Statistical estimation of the optimum
from multi-start results (extreme-value / Weibull estimators), use of seed spread as a quality signal, upper bounds
from additive relaxations, and what practitioners report as reasonable stopping rules.

**Q7. Open-source code worth reading.** Implementations of the above for tree / connected-subgraph problems
(language, licence, which neighbourhoods they implement, how they represent the solution for fast connectivity
checks -- e.g. Euler-tour trees, link-cut trees, articulation-point tests).

## 4. Output format

1. A one-page executive summary: the 5-8 techniques most likely to matter for the problem in section 1, each with a
   one-line reason and its evaluation cost in OUR units (number of 0.007 s what-ifs, number of 17 s marginal-value
   passes, regrow cost of about 1-2 s per node).
2. One section per question with the quotes and conditions as specified in section 0, ending with a short
   "what the sources say" paragraph (no recommendations inside those paragraphs).
3. A table: technique | changes which part of the solution | how it picks the place | cost per move in our units |
   used with black-box objectives? (yes / no / unknown, with source) | primary source.
4. A list of pseudo-code sketches (10-25 lines each) for the three techniques you judge most transferable, adapted to
   a black-box F with the costs above, clearly labelled [DERIVED].
5. Known failure modes and negative results you found.
6. All URLs opened.
