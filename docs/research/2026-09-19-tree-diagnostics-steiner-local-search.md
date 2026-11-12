# Connected-subtree local-search catalogue

Scope note: general web, Reddit, wiki, and forum access was not available in this session; I could only live-inspect public GitHub sources. I therefore did not claim Reddit/wiki/forum findings. Quotes below are verbatim from the linked, inspected sources; items without a verified defining passage are marked **not found**.

## 1. Literature name

Cervenjak, Gan, Kakimura, Umboh, and Wirth, *A Radius-Sensitive Approximation Algorithm for Connected Submodular Maximization*, arXiv v1, 28 May 2026:

> “In CSM, we are given a graph \(G\), a non-negative monotone submodular function \(f\) on subsets of the vertex set of \(G\), and an integer \(k\). The goal is to select a tree in \(G\), with \(k\) edges, whose vertex set maximizes \(f\).”  
> — authors above, [arXiv](https://arxiv.org/pdf/2605.30053v1)

The same paper attaches the rooted condition only to its directed variant:

> “DRCSM further specifies a vertex to be the root of the selected out-tree.”  
> — Cervenjak et al., 28 May 2026, [arXiv](https://arxiv.org/pdf/2605.30053v1)

Conditions: this is non-negative, monotone, submodular \(f\), and its \(k\)-edge tree has \(k+1\) vertices. Those assumptions are stronger than “black-box and non-additive.”

| Objective/constraint model | Literature label |
|---|---|
| Arbitrary oracle \(F(S)\), root, connectivity, cardinality | No single standard named problem found; precise description: rooted cardinality-constrained connected-subset maximization with a value-oracle objective |
| Verified non-negative monotone submodular \(F\) | Connected Submodular Maximization; rooted/directed form: DRCSM |
| Additive node weights, root required | Rooted Maximum Node-Weight Connected Subgraph |
| Additive prizes/costs, connect required terminals | Node-Weighted Steiner Tree |
| Additive prizes with optional terminals/penalties | Prize-Collecting Steiner Tree |
| Budgeted additive prize with edge/node costs | Budgeted Prize-Collecting Steiner Tree / budgeted Steiner variants |

Verbatim defining passages for the last four labels from their primary papers: **not found** through the available live source surface.

No disagreement was found; the distinction is by assumptions, not competing names.

**what it says:** “Steiner,” “MWCS,” and “CSM” become exact labels only after specifying the objective’s algebraic structure; an unrestricted black-box objective does not inherit their guarantees.

## 2. Steiner-tree local-search neighbourhoods

Gamrath, Koch, Rehfeldt, and Shinano, *SCIP-Jack – A massively parallel STP solver*, ZIB Report 14-35, September 2014, describe the Uchoa–Werneck neighbourhoods:

> “The improvement heuristic is called whenever a new incumbent solution has been found.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

> “The basic idea of vertex insertion is to connect further vertices to an existing Steiner tree in such a way that expensive edges can be removed from it.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

> “Key-vertices with respect to a tree \(S\) are either terminals or vertices of degree at least three in \(S\). Correspondingly, a key-path is a path in \(S\), connecting two key-vertices and containing none else.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

> “In key-path exchange attempts are made to replace existing key-paths by less costly ones.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

> “Similarly, for key-vertex elimination in each step a non-terminal key-vertex and all adjoining key-paths … are extracted and an attempt is made to reconnect the so disconnected subtrees at lower costs.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

It also describes recombination:

> “Several good solutions are merged, the STP on the corresponding graph is solved and finally the improvement heuristic is applied on top.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

Conditions: this source minimizes additive edge cost, spans required terminals, and says its undirected local searches needed alterations for its directed formulation. Its “cost” comparison is therefore shortest-path/additive-cost based, not a black-box evaluation cost.

For the stated oracle timings, the evaluation portion is:

| Move | Structural work not priced by the source | Exact objective work under the stated oracle |
|---|---|---|
| Vertex insertion | Find an added vertex and removable corridor(s) | One completed candidate: 0.007 s |
| Key-path exchange | Enumerate key paths; find a replacement connection | One completed exchange: 0.007 s; screening \(p\) exact exchanges: \(0.007p\) s |
| Key-vertex elimination | Remove a branching vertex; reconnect its degree-many components | 0.007 s per completed reconnection candidate |
| Recombination | Merge incumbent supports and solve/repair the restricted graph | 0.007 s per evaluated merged candidate; construction/repair count is separate |
| Full re-evaluation | None | 0.1 s |

A source-backed big-O bound translating those moves to this graph and oracle: **not found**. The published method’s cheap scoring comes from additive edge costs; replacing it with an oracle changes that cost model.

No disagreement was found. The source itself says key-path exchange and key-vertex elimination had the largest impact “by far,” under its additive-STP setup.

**what it says:** the established Steiner vocabulary contains insertion, key-path exchange, key-vertex elimination, and recombination; all alter corridors or branch topology rather than only deleting leaves.

## 3. LNS / ALNS destroy operators and “worst” under interaction

Friedrich and Elbert, *Adaptive large neighborhood search for vehicle routing problems with transshipment facilities arising in city logistics*, published online 31 July 2021; *Computers & Operations Research* 137 (2022):

> “Route removal: a removal heuristic where a random route is selected and up to \(\delta\) customer requests of the route are randomly removed.”  
> — Friedrich & Elbert, 31 July 2021, [paper](https://doi.org/10.1016/j.cor.2021.105491)

> “Worst removal: a removal heuristic … that removes customer requests with high costs that strongly contribute to the objective function of the current solution.”  
> — Friedrich & Elbert, 31 July 2021, [paper text](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md)

> “Historical knowledge node removal: removal heuristic that saves the lowest costs associated with each customer request and removes the \(\delta\) customer requests with the highest difference between their current costs and saved historical lowest cost.”  
> — Friedrich & Elbert, 31 July 2021, [paper text](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md)

> “Shaw removal: a removal heuristic that is also called related removal and was introduced by Shaw (1997, 1998).”  
> — Friedrich & Elbert, 31 July 2021, [paper text](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md)

> “Cluster removal … aims to remove an entire cluster of customer requests.”  
> — Friedrich & Elbert, 31 July 2021, [paper text](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md)

> “Distance-related removal … is a special case of our Shaw Removal procedure, where only the distances between the currently assigned locations of the customer requests are used.”  
> — Friedrich & Elbert, 31 July 2021, [paper text](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md)

Conditions: these are routing requests, with route cost, geography, demand, time windows, and transshipment options. “Route,” “cluster,” and spatial relatedness do not themselves define a tree-subtree operator.

The ALNS framework documentation gives the destroy/repair lifecycle:

> “Destroy operators break parts of a solution down, leaving an incomplete state. This is the first part of each iteration of the ALNS meta-heuristic; the incomplete solution is subsequently repaired by any one repair operator.”  
> — N. Wouda, ALNS example, commit 25 February 2025, [source](https://github.com/N-Wouda/ALNS/blob/5ef1fd1171e6be49c947cd3e56e485509b9c1d64/examples/capacitated_vehicle_routing_problem.ipynb)

For adaptive choice, its roulette implementation states:

> “The probability of an operator being selected is based on the operator weights: operators that frequently improve the current solution — and thus have higher weights — are selected with a higher probability.”  
> — Leon Lan / N-Wouda ALNS, 25 February 2025, [source](https://github.com/N-Wouda/ALNS/blob/5ef1fd1171e6be49c947cd3e56e485509b9c1d64/alns/select/RouletteWheel.py)

> “The `RouletteWheel` scheme updates operator weights as a convex combination of the current weight, and the new score.”  
> — Leon Lan / N-Wouda ALNS, 25 February 2025, [source](https://github.com/N-Wouda/ALNS/blob/5ef1fd1171e6be49c947cd3e56e485509b9c1d64/alns/select/RouletteWheel.py)

Its attached conditions are four outcomes: new global best, improvement over current, accepted-but-not-better, and rejected. The selected destroy and repair weights become:

\[
\omega \leftarrow \theta\omega+(1-\theta)s_j.
\]

For a non-additive oracle, an exact “worst-removal” score for a feasible removable block \(B\) is the removal delta:

\[
\Delta_B = F(S)-F(S\setminus B).
\]

With a cached \(F(S)\), that costs one what-if evaluation per block: 0.007 s. Ranking \(q\) blocks exactly costs \(0.007q\) s. A sampled Shapley-style contribution averages marginal deltas across sampled insertion orders; if there are \(m\) samples over \(q\) blocks, it needs at least \(mq\) marginal evaluations, and connectedness requires a separately defined feasible closure for intermediate coalitions. A source defining that closure for this problem class: **not found**.

No disagreement was found; the limitations are explicit scope differences between routing’s additive “savings” and an interacting oracle.

**what it says:** beyond random ruin, published ALNS catalogues worst, related/Shaw, radial, route, cluster, time/string, and historical-information removal, while adaptiveness credits operator outcomes rather than assigning them fixed priorities.

## 4. Re-optimizing after changed input weights

The SCIP-Jack report uses an incumbent-centered pattern:

> “The improvement heuristic is called whenever a new incumbent solution has been found.”  
> — Gamrath et al., September 2014, [report text](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt)

For a model-specific warning about freezing high-level structure, the only directly relevant game-tree optimizer found says:

> “Locking all masteries effectively locks the entire tree, and the optimizer has no legal moves left to suggest.”  
> — kamcs-dev, 28 May 2026, [Poe Tree Optimizer README](https://github.com/kamcs-dev/Poe-Tree-Optimizer/blob/master/README.md)

Conditions: the first source is additive Steiner optimization; the second is an abandoned PoE tool with static keyword scoring and mastery dependencies. Neither establishes a universal warm-start-versus-rebuild rule for a changed black-box objective.

The standard exact-optimizer analogue is local branching. A verified secondary implementation description says:

> “Classic local branching adds a constraint bounding the Hamming distance from a binary incumbent to at most \(k\) and re-solves a sub-MIP.”  
> — discopt documentation, undated, [source](https://github.com/jkitchin/discopt/blob/7fbf27dd4ac930bd6b00f04f73d527dd442218c0/docs/notebooks/primal_heuristics.ipynb)

Its primary reference is Fischetti and Lodi, “Local branching,” *Mathematical Programming* 98 (2003), [DOI](https://doi.org/10.1007/s10107-003-0395-5). It requires a MIP representation, so it is not directly a black-box technique.

| Observable after the input changes | Measurement cost under the stated evaluator |
|---|---:|
| Old complete solution’s new value | 0.1 s full evaluation |
| One specified delete-and-repair alternative | 0.007 s |
| \(q\) exact trunk/block alternatives | \(0.007q\) s |
| New construction/rebuild | 0.007 s per evaluated construction candidate, plus final/full evaluation as applicable |
| Local-branching subproblem | Not comparable: requires an explicit MIP, not merely the oracle |

A published test that definitively answers “is the old trunk still right?” for arbitrary black-box connected-subset objectives: **not found**.

**what it says:** incumbent improvement, bounded-distance re-optimization, and fresh construction are distinct search regimes; sources do not provide a universal decision test once values are supplied only by an arbitrary evaluator.

## 5. Game skill-tree / talent-graph optimizer found

The live GitHub search found one direct Path of Exile passive-tree optimizer: [kamcs-dev/Poe-Tree-Optimizer](https://github.com/kamcs-dev/Poe-Tree-Optimizer), commit dated 28 May 2026.

> “Runs **simulated annealing** on the allocated passive nodes, swapping nodes in/out to maximize a scoring function based on your build’s keywords.”  
> — kamcs-dev, 28 May 2026, [README](https://github.com/kamcs-dev/Poe-Tree-Optimizer/blob/master/README.md)

Its move restriction is explicit:

> “Each step either adds a node from the frontier … or removes a safe leaf node and adds a replacement.”  
> — kamcs-dev, 28 May 2026, [README](https://github.com/kamcs-dev/Poe-Tree-Optimizer/blob/master/README.md)

The author reports why that static/additive approximation failed:

> “The optimizer assumes a build’s value is roughly the sum of individual node values. That assumption breaks because of mastery nodes.”  
> — kamcs-dev, 28 May 2026, [README](https://github.com/kamcs-dev/Poe-Tree-Optimizer/blob/master/README.md)

> “Fixing this would require search moves that operate at the cluster level (swap a whole cluster for another whole cluster, including the mastery), not at the single-node level.”  
> — kamcs-dev, 28 May 2026, [README](https://github.com/kamcs-dev/Poe-Tree-Optimizer/blob/master/README.md)

Conditions: Rust tool; official tree JSON matching the league; default 10,000 annealing steps; its scoring is keyword/static rather than Path of Building’s calculation engine; repository status is “abandoned.”

PoE wiki, forum, and Reddit threads: **not found / not accessible** in this session. No contradictory published PoE optimizer was found on the accessible live surface.

**what it says:** the identified PoE optimizer used frontier addition, safe-leaf replacement, and simulated annealing, then documented non-local mastery dependencies as the failure mode of its additive score.

## 6. Summary table

| Technique | What it tears down | How it picks the place | Cost per completed move | Source |
|---|---|---|---:|---|
| Vertex insertion | No deletion initially; removes expensive corridor after insertion | Candidate Steiner vertex | 0.007 s oracle evaluation | [Gamrath et al. 2014](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt) |
| Key-path exchange | One maximal path between key vertices | Existing key path; replacement connection | 0.007 s per exchange candidate | [Gamrath et al. 2014](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt) |
| Key-vertex elimination | Nonterminal branch point plus adjacent key paths | Nonterminal key vertex | 0.007 s per reconnection candidate | [Gamrath et al. 2014](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt) |
| Recombination | Multiple incumbents’ differing support | Merge several good solutions | 0.007 s per merged candidate | [Gamrath et al. 2014](https://github.com/warflash/scip-jack-rs/blob/6006df5922390198f60b0fd2108423f55ce487e1/papers/extracted/ZR14-35.txt) |
| Random destroy | Random partial solution | Uniform random selection | 0.007 s after repair/candidate completion | [N-Wouda ALNS](https://github.com/N-Wouda/ALNS/blob/5ef1fd1171e6be49c947cd3e56e485509b9c1d64/examples/capacitated_vehicle_routing_problem.ipynb) |
| Worst removal | High-contribution components | Exact removal delta / additive savings | 0.007 s per exactly scored block | [Friedrich & Elbert 2021](https://doi.org/10.1016/j.cor.2021.105491) |
| Shaw / related removal | A coherent related group | Seed plus relatedness score | 0.007 s per completed ruined-and-repaired candidate | [Friedrich & Elbert 2021](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md) |
| Cluster / route removal | One route cluster or route segment | Route partition or random route | 0.007 s per completed candidate | [Friedrich & Elbert 2021](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md) |
| Historical-information removal | Components with poor current-vs-best history | Largest current cost minus best stored cost | 0.007 s per validation candidate; history bookkeeping separate | [Friedrich & Elbert 2021](https://github.com/DiegoCChumbi/ALNS_planificacion/blob/d242d01fc998ec643acaff21262bd372007df70e/1-s2.0-S0305054821002379-main.md) |
| Roulette-weight ALNS | Whatever selected destroy removes | Probability proportional to rewarded operator weight | 0.007 s evaluation plus negligible weight update | [N-Wouda ALNS](https://github.com/N-Wouda/ALNS/blob/5ef1fd1171e6be49c947cd3e56e485509b9c1d64/alns/select/RouletteWheel.py) |
| Local branching | Up to \(k\) binary decisions around an incumbent | Hamming-distance neighbourhood | Not defined for oracle-only model | [Fischetti & Lodi 2003](https://doi.org/10.1007/s10107-003-0395-5) |

**what it says:** the catalogue separates topological Steiner moves, incumbent recombination, and destroy/repair moves; their published structural costs are not interchangeable with black-box objective-evaluation cost.