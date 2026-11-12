# Diagnosing and rebuilding rooted connected solutions

Literature and software review · 19 September 2026

Prepared for the abstract problem in `2026-09-19-deep-research-1-diagnose-and-rebuild.md`. The deliverable follows the brief's requested English language. This is a research report, not an implementation or an empirical evaluation of the existing solver.

## Executive summary

**[DERIVED] The most promising change is to make early structural decisions reversible, then measure the value of completed replacements.** A weak-looking connector can support valuable descendants; a valuable current branch can still have a much better replacement. Neither singleton marginal values nor removal losses answer the replacement question. The closest mathematical description is **rooted, cardinality-constrained connected set optimization with a non-submodular value oracle**. Additive Steiner/MWCS methods supply useful geometry and connectivity machinery, but their objective arithmetic and approximation guarantees do not carry over.

**[DERIVED] Recommended experimental portfolio, in priority order:**

| Technique | Why it matters here | Cost in the supplied units |
|---|---|---|
| 1. Atomic internal-path replacement | Changes a corridor without first throwing away its valuable downstream region; useful wherever the graph has a bypass. Inspired by key-path exchange [S1]. | `c W` for `c` complete feasible replacements; e.g. 20 paths × 20 alternatives = **400 W = 2.8 s**, plus graph work; **0 M**, no regrow unless separately invoked. |
| 2. Trunk-inclusive region destruction and repair | Reconsiders branching decisions and their dependent selections; must sometimes exceed the current 20-node ruin size [S1], [S3], [S5]. | With `h` shortlisted regions: `h` feasible removal probes, then `h R(q)` for one repair each. At `h=3,q=20`: **3 W + 60–120 s**. A disconnected removal has no legal removal probe. |
| 3. Related/cluster destruction mixed with scattered destruction | Removes mutually dependent choices together, while retaining a way to explore distant interactions [S3], [S4], [S5]. | Structural/history scoring: **0 W, 0 M**, plus `R(q)` and one final evaluation if not already performed by repair. Optional 20–100 group probes: **0.14–0.70 s**. |
| 4. Multiple repair policies, including bounded look-ahead | A larger destroy set can still recreate the same greedy basin. Regret repair and limited-discrepancy reconstruction address a different failure than destroy selection [S3], [S5]. | `h` repairs cost approximately **h R(q)** only if each has the existing greedy cost. Beam/look-ahead costs must be measured separately; cap oracle calls explicitly. **0 M** required. |
| 5. Small operator × size × repair portfolio, credited by time | Balances cheap path probes against expensive rebuilds; adaptation is an experiment, not an assumed improvement [S3], [S12]. | **0 additional W/M** for selection and bookkeeping. Charge candidate construction, failed repairs and scoring to the operator's elapsed time. |
| 6. Warm start plus competing rebuilds after every input change | Reuses useful structure while challenging the old trunk; optimal solutions need not be nested as budget grows [S15], [S16]. | Re-evaluate three saved solutions: **3 full calls = 0.3 s**; then allocate the ordinary solve budget among warm, large-ruin and fresh starts. |
| 7. Conditional group probes; optional local Shapley/Banzhaf audit | Cheap removal/replacement measurements first; coalition attribution only for a small, explicitly feasible local game [S8], [S9]. | 100 valid group removals: **100 W = 0.7 s**. All coalitions of 10 independent blocks: **1,024 W = 7.168 s**; 12 blocks: **4,096 W = 28.672 s**. **0 M**. |

**[DERIVED] Units and accounting.** `W = 0.007 s` per connected what-if; `M = 17 s` per all-node marginal pass; `R(q) ≈ q–2q seconds` for the supplied greedy regrow cost. Thus `1 M ≈ 2,429 W`, and `R(20)=20–40 s ≈ 2,857–5,714 W` in elapsed-time equivalents. These equivalents are **not additional evaluator calls**: regrow may already include many calls. The supplied 10,000–100,000 W budget is only 70–700 seconds of pure what-if time; it does not include construction, regrow, marginal passes or other overhead.

**[DERIVED] First experiment:** compare the current solver against atomic path replacement, trunk-inclusive multiscale rebuilding, and the same rebuilding with an alternative repair. Hold wall time and input versions fixed; retain all three seed outcomes. Measure best value over time, actual trunk changes, feasible candidates, and seconds per improvement. A 40% seed spread is evidence of instability, not a 40% optimality gap. Global Shapley estimation, learned policies and Weibull gap estimates are lower priorities than testing whether the search can reach and improve the untouched structure.

## Reading the evidence

- **[SOURCE]** identifies facts supported by an opened primary paper, author manuscript, official documentation or inspected source code. Short verbatim quotations appear next to their locator. Equations and longer definitions are paraphrased/formalized. To keep quotation use proportionate, the total quoted prose from any individual source is at most 25 words; some definitions therefore use a short defining fragment rather than an entire sentence.
- **[DERIVED]** identifies this report's reasoning, proposed adaptations, cost calculations and experimental choices. They have not been validated on the supplied problem.
- **[UNVERIFIED]** identifies an unavailable original, a provenance gap, or an application for which no direct primary evidence was located. It does not mean the technique cannot work.

Source identifiers resolve to primary URLs; full authors, version, venue and access qualifications are in the bibliography. PDF page numbers include covers unless a printed page is explicitly specified. `S` denotes selected vertices; its feasibility is connectivity of **the induced graph `G[S]`**, not connectivity of an arbitrarily chosen parent tree. The main analysis assumes `|S| ≤ B`; exact-cardinality variants are distinguished where relevant. No monotonicity assumption about the simulator is made.

## Q1. Names and neighbouring fields

### 1.1 A precise formulation and the naming boundaries

**[DERIVED]** Write the actual problem as

`maximize Fθ(S), subject to r ∈ S, |S| ≤ B, and G[S] connected`.

The subscript `θ` represents the evaluator's other inputs. This is a connected subset selection problem with a value oracle. Describing it merely as “Steiner tree” would hide both the variable choice of valuable vertices and the nonadditive objective. Any connected selected set has a spanning tree, so a tree can be an auxiliary representation; changing only its edges leaves `Fθ(S)` unchanged.

| Literature name | Verified objective/constraints | Relevant established methods and limits |
|---|---|---|
| **k-cardinality tree; k-MST** | **[SOURCE]** Chimani et al. define KCT by “exactly k edges”; their objective is minimum additive edge cost. Their introduction also distinguishes node-weighted KCT [S2, abstract/§1]. The convention may therefore mean `k+1` selected vertices. | Directed-cut branch-and-cut; constructive and metaheuristic tree search. Their 200–5,000-node experiments show exact methods can compete with heuristics. This is not evidence that an arbitrary simulator is similarly tractable. |
| **Node-weighted k-cardinality tree** | **[SOURCE]** Blum and Ehrgott minimize the sum of selected node weights over a fixed-size tree [S6, §1–3]. | Leaf exchange, changed spanning-tree representation, tree tabu search and tree crossbreeding. Closest classical fixed-cardinality additive relative; not a proven oracle optimizer. |
| **Quota Steiner tree** | **[SOURCE]** Minimize connection cost while collecting at least a specified additive profit quota; distinct from imposing a cost budget [S7, §2]. | Steiner constructions, reductions and mathematical programming. A quota is a target value, not a cardinality cap. |
| **Budgeted Steiner / budgeted connected subgraph** | **[SOURCE]** Maximize additive selected-node profit subject to connection/selection cost and required terminals [S7]. Defining fragment: “maximize the total profit of the nodes”. | Rooted connectivity cuts, flow formulations, construction followed by improvement. Unit node costs give an additive version of the supplied constraint set. |
| **Prize-collecting Steiner tree, rooted PCST** | **[SOURCE]** Minimize selected edge costs plus penalties for omitted prize vertices; fixing a root yields the rooted variant. Defining fragment: “adding edges to and omitting terminals” [S10, §1]. | Primal-dual growth/pruning, local search, reductions and exact solvers. `pcst_fast` is a practical construction engine. Standard PCST has a penalty trade-off, not automatically a strict node budget. |
| **Rooted, capacity-constrained MWCS** | **[SOURCE]** Maximize “cumulated weight” in a connected vertex set containing a root, with capacity bounds; Borndörfer et al. also impose red/blue balance [S11, abstract/§2]. | IP, preprocessing and conflict cuts; 240 cases derived from five 563–569-node networks. Cardinality is the special case of unit capacity weights, without their extra balance condition. |
| **Active module / network enrichment; GMWCS** | **[SOURCE]** Biological measurements become additive node weights, or node and edge weights in GMWCS: “both nodes and edges are scored” [S13, abstract]. | Heinz and GMWCS: decomposition, reductions, tree heuristics and branch-and-cut. Biological interaction edges do not themselves make the mathematical objective a nonlinear simulator. |
| **Connected submodular maximization (CSM)** | **[SOURCE]** Select a connected tree with a size cap under a “non-negative monotone submodular function” [S14, abstract]. AAMAS 2026 also treats directed and rooted versions. | Radius-sensitive approximation algorithms. Its rooted guarantee can violate size by `1+δ`; its assumptions exclude the supplied complementary groups. This is primarily a theoretical source, not a speed benchmark for this solver. |
| **Submodular orienteering / informative routing** | **[SOURCE]** Optimize submodular information/reward with a route-derived cost constraint. Zhang and Vorobeychik propose a “generalized cost-benefit (GCB) greedy algorithm” [S17, abstract]. | Greedy marginal gain over approximate incremental routing cost; evaluated on 36 Beijing stations and a San Diego application. Route length, traversals and endpoints differ from connected node cardinality. |
| **Connected reserve / wildlife corridor design** | **[SOURCE]** Node habitat profits/costs, required reserves, connected selection and a budget [S7]. | Strong connectivity-cut MIPs and bounds; synthetic 100-node grids and real conservation graphs up to 3,299 parcels. A particularly close additive modelling analogue. |
| **Connected facility location** | **[SOURCE]** Facility opening costs, client assignment distances and a Steiner backbone cost [S18, §1]; the paper uses “opening cost, Steiner cost and connection cost”. | Approximate facility location, randomized client sampling and backbone construction. Its “black-box” subroutine is a facility-location algorithm, not an arbitrary objective oracle. A neighbouring application, not the right name for this problem. |
| **Network design with connectivity; capacitated MST** | **[SOURCE]** A broad family. CMST connects all demand vertices and bounds demand below root-adjacent subtrees [S19, §1]. | Tree/subtree exchanges, tabu search, multi-exchange improvement graphs and exact formulations. Here the selected customer set is fixed, unlike the supplied subset problem. |

**[DERIVED] Additional useful search terms:** *simulation-based combinatorial optimization*, *large neighborhood search with expensive evaluation*, *connected subset selection*, *node-budgeted network design*, *non-submodular set function optimization*, *reoptimization*, and *matheuristics*. These are descriptors/search directions, not claims of one standardized problem name with a matching off-the-shelf solver.

**[DERIVED] Why a PCST surrogate is useful but not equivalent.** Replacing `Fθ` by weights `w_v` permits optimizing `Σw_v−λ|S|` or a budgeted additive model. Varying `λ` can generate connected candidates cheaply. It does not in general recover every budget-optimal solution: discrete trade-off curves can contain unsupported points. Every surrogate proposal still needs the real `Fθ` evaluation and an explicit cardinality check.

**What the sources say — [SOURCE].** These neighbouring fields separate additive edge cost, additive node profit, and monotone submodular reward. Their published methods exploit those structures. The opened literature supplies practical additive solvers and submodular approximation results; it does not establish a best practical algorithm for this exact non-submodular oracle problem.

## Q2. Neighbourhoods for tree-shaped solutions

### 2.1 The four Steiner neighbourhoods, precisely distinguished

**[SOURCE] Uchoa and Werneck (2012), §§2–3 [S1].** Let `T` be fixed terminals and `X` the current tree's vertices. Vertex insertion tests `MST(G[X∪{v}])`; elimination tests `MST(G[X\{v}])` for nonterminal `v`. Key vertices have “degree at least three”. A key path has the defining sentence: “A key path connects two crucial vertices in S and has no internal crucial vertex.” Crucial means terminal or key vertex. Exchange removes its internal vertices and reconnects the two retained components. Key-vertex elimination removes a branching key vertex and its incident key paths, then reconnects the retained components, using the distance-network viewpoint.

The paper gives **`O(m log n)` per neighbourhood pass**, using dynamic MST/path operations, Voronoi regions, heaps and union-find. These are positive additive edge-cost problems with fixed terminals. The study uses 1,020 SteinLib instances and measures time and objective gaps. It is not an arbitrary black-box evaluation method. Earlier origins are credited in the paper; the 2012 contribution is fast evaluation, not invention of all four moves.

**[UNVERIFIED] Original-source boundary.** The opened paper attributes earlier insertion/elimination work to Minoux, Osborne–Gillett, Spira–Pan and Voß, and key-path work to Dowsland, Verhoeven et al. and Duin–Voß. Those originals were not all obtained in full text; this report does not supply reconstructed quotations or claim verified priority. The exact definitions above come from the opened 2012 primary algorithm paper.

**[SOURCE] A published correction matters when pruning the move portfolio.** Pajor, Uchoa and Werneck [S26, Appendix A.3] qualify the earlier assertion that key-vertex removal dominates Steiner-vertex removal: it is “not strictly true”. A degree-two vertex can become a key vertex in a move available to the latter. They describe such counterexamples as rare in their experiments. Therefore the two additive neighbourhoods should not be described as having a proved universal dominance relation.

**[DERIVED] Translation to the supplied problem:**

| Move | What changes | What survives the translation | What does not |
|---|---|---|---|
| Vertex insertion | One selected vertex, potentially many auxiliary edges | A useful small candidate generator if budget is free, or paired with a removal | Lower MST edge cost says nothing about simulator value; insertion alone exceeds a full budget |
| Vertex elimination | Any non-root vertex whose retained set can reconnect using retained vertices | Can remove a non-leaf of the auxiliary tree if `G[S\{v}]` stays connected | Treating every auxiliary-tree internal vertex as indispensable; pruning a low-value vertex without evaluating interactions |
| Key-path exchange | Interior corridor and possibly its attachments | Atomic removal/addition with downstream selections retained; inspect multiple bypasses | Shortest path is no longer automatically the best path; longer paths may carry valuable selected nodes |
| Key-vertex elimination/reconnection | A branching point and several incident corridors | A multicomponent rebuild candidate, provided all retained components reconnect within budget | Fixed terminals and additive reconnect cost no longer identify the best branch allocation |

**[DERIVED] Oracle scan cost is a separate quantity.** If structural filtering produces `c` distinct feasible final sets, exact scoring costs `c W`, irrespective of the additive paper's complexity. The `O(m log n)` result cannot establish that these `c` sets include the oracle-best move. Enumerating all possible simple replacement paths is potentially exponential; retaining 10–20 diverse alternatives is an engineering restriction, not an exhaustive neighbourhood scan.

### 2.2 k-cardinality exchange and changing the tree representation

**[SOURCE] Blum and Ehrgott [S6], opened technical-report version, printed pp. 8–12.** Their basic neighbourhood is obtained by “removing one leaf” and “adding one node”. Their Edge-Permutation Algorithm changes the spanning tree on the same selected vertices, exposing different leaves for later exchanges. One local-search iteration costs at most `O(k(n−k))`; edge permutation costs `O(k²)`. Their objective is additive node weight. A special single-trough landscape admits polynomial convergence; general graphs do not inherit that result. The work also develops tree tabu and crossbreeding approaches.

**[DERIVED]** A 32-leaf solution and at most 1,200 outside vertices give an intentionally loose `32×1,200 = 38,400` pair bound: **268.8 seconds** if every pair were oracle-scored. Adjacency and connectivity filtering can make this much smaller. Changing a parent tree alone costs zero oracle calls because `S` is unchanged; it can expose deletions hidden by the current representation. An articulation test on `G[S]` is the more direct way to find deletable vertices.

### 2.3 Subtree swaps, prune-and-regraft, and ejection-like multi-exchanges

**[SOURCE] Ahuja, Orlin and Sharma (2001) [S19], §§2–5.** Their CMST generalization allows “exchanges of nodes among multiple subtrees simultaneously”. Cyclic or path transfers move nodes, or rooted subtrees, across root branches. A negative subset-disjoint cycle in an improvement graph represents a profitable compound move. The neighbourhood is exponential; their cycle search is heuristic. For unit demand, constructing node-exchange arc costs takes `O(n²K)`, with branch capacity `K`; tree-based costs can take `O(n²K²)`. These bounds depend on additive MST arithmetic. Experiments use 40/80-node homogeneous and 50/100/200-node heterogeneous cases, measuring best costs under time limits.

**[DERIVED]** This supplies a concrete tree analogue of an ejection chain: inserting one group displaces another, which displaces a third, until a feasible compound exchange closes. For arbitrary `F`, adding independently estimated transfer gains is unsound. A bounded beam can generate chains using structural/surrogate scores, but only a connected completed chain gets an exact oracle score. With beam width `b`, maximum depth `d`, and `c` proposals per beam state, the generation limit is roughly `b d c`; score only feasible completions, rather than claiming `b d c` legal intermediate evaluations.

**[DERIVED]** “Prune-and-regraft” needs two different interpretations here. Reattaching an unchanged selected subtree through different already-selected edges changes no value. Replacing its access corridor, or removing one selected subtree and spending its vertices elsewhere, changes `S` and can improve `F`. The latter overlaps the current ruin-and-recreate operator; the useful extension is access to larger dependency closures and different repair policies.

**[UNVERIFIED]** No opened primary study demonstrated a canonical Lin–Kernighan variable-depth Steiner/k-cardinality neighbourhood evaluated by this kind of deterministic non-submodular simulator. Nor was an original, universally named “corridor move” located. The atomic corridor operator in this report is explicitly derived from key-path geometry. It is not presented as a verified published black-box algorithm.

### 2.4 Connectivity and cheap pre-filtering

**[DERIVED]** Before scoring `S'=(S\A)∪P`, check root membership, distinct-node cardinality and connectivity. If removing `A` leaves several retained components, every component must reconnect; reconnecting just the two apparent path endpoints is insufficient when internal vertices have side branches. Reject impossible connectors using shortest *additional-node-count* paths, forbidden-vertex masks, and boundary reachability. Use surrogate value only to order the remaining candidates, never to certify that a rejected candidate cannot improve `F`.

**[DERIVED]** Distinguish three objects: a chosen parent tree; the selected induced graph `G[S]`; and the full graph `G`. An articulation in the parent tree may have a bypass in `G[S]`; an articulation in `G[S]` may have a bypass through unselected vertices of `G`. If a non-root vertex is an articulation in **full `G`**, with retained valuable descendants on its far side, no path replacement can keep those descendants and remove that vertex. The move must instead retain the connector or reconsider the descendants too.

**[SOURCE] Black-box-adjacent evidence.** Reijnen et al. [S20, §4] evaluate candidate repairs for stochastic orienteering through repeated simulation: five evaluations during insertion and 100 after repair. Their filters/orderings use distance, prizes and historical edge scores. This verifies simulation-based ALNS in routing; it does not verify the four Steiner neighbourhoods with arbitrary oracle values.

**What the sources say — [SOURCE].** Fast Steiner scans derive their efficiency from additive structure. Cardinality search includes leaf exchange and changes of spanning-tree representation; capacitated tree search includes large compound exchanges. Simulation-based ALNS exists in routing, but direct evidence for the requested combination of tree neighbourhoods and unrestricted black-box value was not located.

## Q3. Deciding what to destroy

### 3.1 Destroy operators and their actual scoring rules

**[SOURCE] The original LNS rationale.** Kilby, Prosser and Shaw's April 1998 report [S5, §§2–4] describes “relaxing some of these decisions” and rebuilding them. It explicitly favours related decisions because independent decisions could instead be reconstructed separately. It also warns that deterministic relatedness can stagnate. Its reconstruction is constrained tree search; this is not a numerical-simulator experiment. The report's title page says 1998 despite a conflicting date in the hosting page metadata.

**[SOURCE] Ropke and Pisinger, PDPTW paper [S3, §§3.1–3.2].** Defining fragments are “removes requests with high cost(i,s)” for worst removal, “requests that are similar” for Shaw removal, and “best route and its second best route” for regret. These operators concern requests in routes with explicit travel costs and scheduling constraints. Experiments include more than 350 instances and up to 500 requests. For their minimization objective `f`, the exact rules are:

1. **Worst removal:** `cost(i,s)=f(s)−f(s without i)`. Remove large-cost requests, with randomized rank selection; recompute after deletions. This is conditional deletion cost, not an additive ownership allocation.
2. **Shaw/related removal:** start with a random request. Repeatedly choose an already removed request `i`, rank remaining `j` by increasing relatedness distance, and choose index `floor(y^p |L|)`, with `y` uniform in `[0,1)`. The paper combines normalized pickup/delivery distance, visit-time difference, demand difference and vehicle compatibility:

   `R(i,j)=φ[d(Ai,Aj)+d(Bi,Bj)] + χ[|tAi−tAj|+|tBi−tBj|] + ψ|li−lj| + ω[1−|Ki∩Kj|/min(|Ki|,|Kj|)]`.

   Smaller means more related. Their tuned coefficients are `(φ,χ,ψ,ω)=(9,3,2,5)` with rank exponent `p=6`; worst removal uses exponent 3. These numbers are tied to their normalized routing features.
3. **Regret-k insertion:** if `Δij` is request `i`'s best insertion cost in its j-th best route, prioritize the request maximizing `Σ(j=2..k)(Δij−Δi1)`, then insert at its cheapest position. Few feasible routes receive special priority. This is a repair operator, not intrinsically a destroy score.

**[SOURCE] Ropke and Pisinger, backhauls paper [S4, §§5.3–5.5].** Cluster removal partitions a selected route into “two clusters” using Kruskal stopped before the final merge, then removes one randomly; further nearby routes can be processed. Neighbor-graph removal stores the best full-solution cost observed for each directed adjacency. A request's score sums the historical weights of its current incident adjacencies; high scores are removed in this minimization setting. The definition refers to the “best solution encountered so far”.

The separate request graph stores how often request pairs co-occur in the same route among the best 100 distinct solutions. High co-occurrence defines relatedness for joint removal. Crucially, directly removing low co-occurrence-score requests was “an unpromising approach”: the authors say it counteracted diversification. Their final mechanism uses history to identify a group, not simply to preserve the most frequent incumbent structure. The study covers several explicit-cost backhaul-routing classes, not black-box set functions.

| Destroy family | Place selection | Transfer to the supplied problem |
|---|---|---|
| Worst / high deletion saving | **[SOURCE]** Conditional removal delta [S3] | **[DERIVED]** For maximization rank low `L(A)=F(S)−F(S\A)` among feasible removals. Ratios `L(A)/|A|` are optional heuristics, not exact replacement value. |
| Shaw / related | **[SOURCE]** Random seed plus biased relatedness ranks [S3], [S5] | **[DERIVED]** Graph distance, shared access corridor, common floor dependency, observed joint effects and history are possible features. Normalize features and retain random selection. |
| Kruskal cluster | **[SOURCE]** Split a route's geometric complete graph into two clusters [S4] | **[DERIVED]** A selected-region cluster is analogous, but graph-connected blocks require an explicit construction; proximity clustering alone does not ensure graph connectivity. |
| Neighbor history | **[SOURCE]** Poor historical context of current adjacencies [S4]; the maximization routing example removes low historical scores [S20] | **[DERIVED]** History belongs to an input version and context. Do not copy a minimization sign into a maximization implementation. |
| Path / segment / subtree | **[SOURCE]** Path interiors and branch components have exact tree definitions in [S1], [S19] | **[DERIVED]** Sample an internal path, a hanging dependency closure, or a branching region. This report's set-destruction versions are adaptations, not the papers' identical operators. |
| Critical / bottleneck | **[UNVERIFIED]** The opened survey [S25, §4.2.4] attributes worst-forward-time-slack critical destruction to Grimault et al. (2017); its full primary paper was inaccessible | **[DERIVED]** Tight-floor dependency groups are a possible analogue. The primary paper's precise critical score is not reconstructed here. |

**[SOURCE, secondary scope]** Voigt's review [S25] ranks sequence-based removal highly across 211 VRP articles, but that is cross-study routing evidence. It does not compare graph-connected destruction against scattered destruction under an arbitrary set oracle. The original sources above, rather than this ranking, support the operator definitions.

### 3.2 Removal loss is not replacement opportunity

**[DERIVED]** For a feasible retained core `C=S\A`, three quantities answer different questions:

- `L(A)=F(S)−F(C)`: damage caused by deleting `A` in the current context.
- `F(C∪P)−F(C)`: value recovered by a specific legal replacement `P`.
- `I(A)=max(P in tested repairs) F(C∪P)−F(S)`: the best **observed** improvement available from rebuilding `A`.

The first costs one W if `C` is connected. The third requires actual completed alternatives. A branch with loss 100 and replacement recovery 150 is a better rebuild opportunity than a branch with loss 1 and recovery 1.2. That example establishes why ordering only by weakest removal loss can systematically miss valuable changes. A connector's deletion loss also includes all dependent vertices removed with it; call this a *group* loss, not that connector's intrinsic contribution.

**[DERIVED]** Nonadditivity makes cached deletion scores context-dependent. Sequential worst removal can require approximately `a q` probes for `a` possible deletions and `q` rounds. For `a=100,q=20`, the crude bound is 2,000 W = 14 s, versus 100 W = 0.7 s for one frozen ranking. Reusing frozen scores is a deliberate approximation. The 17-second global marginal pass is not automatically better than a small set of connected group probes; its estimated values may answer a different question and include infeasible singleton counterfactuals.

### 3.3 Shapley, Banzhaf and sensitivity

**[SOURCE] Shapley sampling.** Burgess and Chapman (2021), IJCAI [S8, §§1, 3–4], define the value through “average marginal contribution across every possible sequence of player join orderings”. They stratify contributions by coalition size and allocate samples to reduce an empirical Bernstein uncertainty bound. The bound uses range information and observed variance; initialization requires at least two samples per stratum where applicable. Their experiments include 15-player airport and voting games. This is attribution estimation, not a connected-search benchmark.

**[DERIVED]** For `k` components and a utility `U` defined on *every* coalition, the ordinary Shapley value is

`φi = average over random permutations π of [U(predecessorsπ(i)∪{i})−U(predecessorsπ(i))]`.

Evaluate all prefixes of each permutation to estimate all components together. `m` permutations take at most `m(k+1)` utility evaluations; caching the common empty/full endpoints reduces this to at most `m(k−1)+2`, with further savings from repeated subsets. For `k=100,m=64`, the naive bound is **6,464 W = 45.248 s**; the endpoint-cached bound is **6,338 W = 44.366 s**. This is only 64 marginal observations per component, not a guaranteed precise ranking. At `k=1,300`, the naive bound becomes **83,264 W = 582.848 s**. Exact attribution can reuse all `2^k` coalition utilities: 1,024 for 10 components, 4,096 for 12.

**[SOURCE] Banzhaf and sample reuse.** Wang and Jia (2023), AISTATS [S9, §§2, 4], define leave-one-out error by the “change of model performance” after exclusion, and Banzhaf by the uniform average marginal contribution over subsets excluding `i`. Their estimator uses the “Maximum Sample Reuse (MSR) principle”: sample whole coalitions uniformly and reuse each utility observation across all players. With `U∈[0,1]`, Theorem 4.9 bounds calls by `O(ε⁻² log(k/δ))` for simultaneous `ℓ∞` error, and `O(k ε⁻² log(k/δ))` for `ℓ2` error. Evaluation concerns ML data valuation, including stochastic training; it does not establish better destroy decisions.

**[DERIVED]** The Banzhaf identity explains the reuse:

`βi = E[U(C) | i∈C] − E[U(C) | i∉C]`, for uniformly sampled subsets `C`.

Naively sampling `m` paired differences separately for each of `k` players costs `2km` calls. MSR instead uses `m` total coalition calls, estimating two conditional sample means for each player; sufficient inclusion/exclusion counts and variance still matter. Thus `m=1,000` is **7 s** at W cost, not 1,000 independent paired observations per player. If `U` has known range width `H`, normalizing changes the relevant accuracy to `ε/H`; the asymptotic bound is not a constant-time promise for unbounded penalty scales.

**[DERIVED] The decisive feasibility issue:** ordinary coalitions of selected graph nodes are often disconnected. The given W interface cannot evaluate them. Valid alternatives are (a) a fixed connected core plus disjoint blocks each independently attached to that core, with every block union within budget; or (b) an explicitly defined completion map `φ(C)` that connects/repairs every coalition. In (b) the game is `U(C)=F(φ(C))`, and the attribution depends on the completion policy. Sampling only connected coalitions does **not** estimate ordinary Shapley/Banzhaf values without changing the definition and estimator. The prices above apply only when each required utility is a valid 7 ms call. They cannot justify thousands of disconnected calls at that price.

**[DERIVED] Local interaction/sensitivity probes.** For two disjoint removable groups with all four configurations feasible, measure

`J(A,B)=F(S)−F(S\A)−F(S\B)+F(S\(A∪B))`.

With cached current and single-removal values, this costs one extra W per pair. Positive `J` indicates complementary contribution in this particular retained context; it does not characterize all other contexts. Testing all 45 pairs of ten groups after ten single removals costs **55 W = 0.385 s** with current `F(S)` cached. Sampling different feasible contexts gives sensitivity information, but is not a global causal or Shapley certificate. If a floor statistic is separately observable, its deletion delta can identify jointly needed support; if only aggregate `F` is exposed, that diagnosis cannot be inferred reliably from the score alone.

**[UNVERIFIED] Influence-function shortcut.** No opened primary source supplied a justified low-cost influence formula for an arbitrary nondifferentiable connected-set simulator. Differentiability, internal gradients or a validated surrogate would be additional information. This report therefore does not promise Hessian-based or gradient-based contribution estimates from the stated interface.

### 3.4 Learned destroy policies and adaptive size

**[SOURCE] Learned variable selection.** Huang, Ferber, Tian, Dilkina and Steiner (2023), ICML [S21], learn from an expert that “collects positive and negative solution samples”. Their CL-LNS uses known ILP variable/constraint features, graph attention and contrastive learning. Benchmarks include vertex cover, independent set, auctions and set cover; experiments allow 60 minutes per instance and two minutes per repair sub-ILP. A generic schedule keeps size after improvement and otherwise uses `k←min(γk,βn)`; their standard settings include `γ=1.02, β=0.5`. These are ILP experiment settings, not recommended constants for this simulator.

**[SOURCE] Learned online control.** Reijnen et al. (2024), ICAPS [S20], jointly select destroy, repair, “10% to 100% destroy severity”, and acceptance temperature. Seven search-state features include progress/stagnation information; the reward is five for a new global best and zero otherwise. The OPSWTW evaluation uses three sets of 250 instances, with 20, 50 and 100 customers, and compares quality, training and inference costs. It is the strongest opened evidence for simulation-based adaptive neighbourhood control, but has a training distribution and routing-specific operators.

**[SOURCE] Simpler size control already exists.** The 1998 LNS report increases size on stagnation and allows reduction when progress is easy [S5]. Ropke–Pisinger sample removal count uniformly from 4 to `min(100,ξn)`, with `ξ=0.4` in the opened version [S3]. They note that varying removal size under a fixed iteration count changes running time, complicating comparisons.

**[DERIVED] Connected versus scattered destruction is an interaction question.** A contiguous corridor region captures local access dependencies. Distant nodes can still be complementary through `F`, so a purely geographic destroy rule can miss them. Conversely, scattering 20 removals among unrelated leaves may act like many small independent repairs. The appropriate comparison is equal-time experiments with graph-contiguous regions, dependency-related groups, and scattered groups; the opened evidence does not provide a universal winner.

**[DERIVED]** A practical trial schedule is region sizes `{4,8,16,32,48}`, plus a full restart arm. These values are proposed experimental bins. A nominal request for 16 nodes may produce a larger dependency closure; record and charge the **actual** changed set. A 48-node limit still cannot guarantee access to every trunk decision, so retain occasional near-global reconstruction. At the supplied rates, a single 48-node greedy repair already costs roughly 48–96 seconds.

**What the sources say — [SOURCE].** Established diagnosis mechanisms include deletion costs, relatedness, cluster geometry and historical compatibility. Regret concerns future insertion opportunities. Shapley/Banzhaf estimate contextual average contributions under a defined coalition game. Adaptive size and learned control have evidence in routing and ILP, while their benefits for connected non-submodular simulator search remain unmeasured.

## Q4. Choosing operators and allocating time

### 4.1 Original ALNS roulette, including the parameter/version distinction

**[SOURCE] Ropke and Pisinger [S3, §§3.3–3.5, 4.3].** The original selection uses a “roulette wheel”: choose operator `j` with `pj=wj/Σiwi`, starting equally. Destroy and repair weights are separate. In each 100-iteration segment, accumulate score `πi` and usage count `θi`, then update

`wi,next = (1−r)wi + r πi/θi`.

Three awards distinguish a global best, a previously unaccepted improving solution, and a previously unaccepted worse solution that is accepted. Both applied operators receive the same award because their contributions are not separable. The **opened 2005 technical-report version** of the 2006 paper uses `(σ1,σ2,σ3)=(33,9,13)` and `r=0.1`; it does not say `(33,9,3)`. No award is assigned to a rejected move. Implementations need an explicit convention when `θi=0` rather than dividing by zero.

**[SOURCE] Acceptance matters too.** Their simulated-annealing rule permits worsening moves, with geometric cooling; the best-so-far solution is retained separately. This changes the search compared with always accepting only strict improvement [S3, §3.5].

**[DERIVED]** For maximization, a worsening candidate with `Δ=F(S')−F(S)<0` is accepted with probability `exp(Δ/T)`. A temperature calibrated to observed feasible score differences is meaningful; a raw temperature copied from a different penalty scale is not. If floors are truly mandatory, enforce feasibility separately. A finite penalty in `F` alone does not prove that every accepted or final solution satisfies them.

### 4.2 Bandits and the evidence for adaptation

**[SOURCE] Hendel (2018 report; later journal version), [S12, §§3–5].** His MIP ALNS uses epsilon-greedy, UCB and Exp3 over neighbourhoods. Defining fragment: “guided by selection strategies for the multi armed bandit problem”. Reward incorporates finding a solution, closing an objective gap and effort. He approximates effort using free-variable fraction times subproblem node-budget consumption:

`ξ=(1−nfixed/ninteger)×nodes_used/node_limit`.

This is a deterministic proxy, not measured seconds. His closed-gap reward requires a dual bound. Table 4 reports roughly 1–3% aggregate time/integral changes over 665 instances, with much larger effects on a 110-instance affected subset. The subset result is not an average benefit over all instances.

**[SOURCE] Adaptation does not invariably win.** Ropke–Pisinger's Table 3 comparison describes ALNS as “on par” with the best simple configurations [S3]. That experiment supports robustness of the mixture, not strict superiority. Hendel's results are favourable for a different setting [S12]. Voigt's secondary review also advises that adaptive selection does not eliminate operator screening [S25]. These findings concern different portfolios, benchmarks and resource budgets; they are not a contradiction requiring one result to be discarded.

**[DERIVED]** Classical stationary-bandit intuition has limits: operator reward changes as the incumbent, temperature, remaining budget and evaluator inputs change. Scoring an arm by improvement over the current incumbent also differs from improvement over the best-so-far. Discount old observations or reset them after an input change; keep an exploration floor. An arm can be `(destroy family, size bin, repair policy)` to expose interactions, but too many arms consume the affordable trials before learning anything useful.

### 4.3 Time-aware credit and a library discrepancy

**[DERIVED]** For each arm record elapsed time `t`, feasible completions, current-solution improvement, best-so-far improvement and amount rebuilt. A simple comparable return is `max(0,Fnew_best−Fold_best)/t`, averaged over a recent window. A small separate exploration allocation is needed because zero immediate gain does not mean a diversifying move is worthless. This is a proposed empirical rule, **not** Hendel's published reward and not a bandit regret guarantee. Evaluate against uniform random choice and a fixed schedule under equal wall time.

**[SOURCE] Official ALNS documentation and inspected Python code [C1].** `AlphaUCB` treats allowed destroy/repair pairs as actions. `RouletteWheel` updates per iteration; `SegmentedRouletteWheel` updates at segment boundaries. In the inspected `SegmentedRouletteWheel.py`, `_d_seg_weights` and `_r_seg_weights` accumulate awards and are used directly in the update. There is **no division by operator usage count**. Consequently this library class is not an exact implementation of the original `πi/θi` formula. Its four outcome scores also include rejection, whereas the original description has three positive award cases.

**[DERIVED]** More frequent usage then contributes more total segment score in that implementation. If reproducing the original rule is important, add count normalization or write a small selector; naming a library class “segmented roulette” is insufficient to establish mathematical equivalence. The library's `decay` weights the old estimate, so it corresponds to `1−r` in the original notation, not `r`.

**What the sources say — [SOURCE].** Original ALNS learns separate operator weights from average segment rewards. Later approaches select coupled actions and account for effort. Published experiments show both ties with well-chosen fixed configurations and benefits from adaptation. The opened library offers related, but not identical, update rules.

## Q5. Reoptimization after evaluator inputs or budget change

### 5.1 What Steiner reoptimization actually proves

**[SOURCE] Bilò (2018), ICALP [S15, §1.1].** Reoptimization starts from a previous solution and “a local modification that slightly changes the instance”. The paper handles increasing/decreasing one edge cost and changing one vertex between terminal and Steiner status. Given an old `ρ`-approximation, it obtains a `(ρ+ε)`-approximation after the change; for decreasing an edge cost or removing terminal status, its scheme requires `ρ=1`. The problems remain strongly NP-hard and have no FPTAS unless P=NP. The algorithms reconnect forests after bounded component changes; the result is theoretical, not a simulator runtime study.

**[DERIVED]** Reoptimizing other simulator inputs may alter many interactions at once, so it is not one of these four local modifications. Likewise, the old heuristic solution is not known to be optimal. The theorem supplies neither a certified fixed trunk nor a runtime prediction here. It does support treating prior structure as useful information rather than discarding it automatically.

### 5.2 Budgets do not imply nested optima

**[SOURCE] Disser, Griesbach, Klimm and Lutz (2024 preprint) [S16, abstract and Theorems 1–2].** They study rooted additive-prize Steiner selection with a growing edge-cost budget and irrevocable additions. Defining fragment: “a growing budget constraint”. Pure same-budget multiplicative approximation is not generally possible for one incremental solution across all budgets. Their positive results explicitly permit additive budget slack: on a tree, density-greedy achieves `(χ,1)`, where `χ` is root eccentricity measured in edge cost. General-graph results require further qualifications. These are theoretical guarantees, without an empirical comparison on the supplied cardinality oracle.

**[DERIVED] A direct unit-node counterexample.** Let root `r` have two disjoint arms: `r–a1–a2`, with prize 5 only at `a2`, and `r–b1–b2–b3`, with prize 100 only at `b3`. All other prizes are zero. At `B=3` including the root, the unique optimum is `{r,a1,a2}`. At `B=4`, the unique optimum is `{r,b1,b2,b3}`. Their intersection is only `{r}`. This already uses a tree and additive nonnegative prizes. Scale the arm lengths to 99 and 109 non-root vertices to obtain the same obstruction at budgets 100 and 110. Thus even a modest budget increase can require replacing almost the whole solution.

**[DERIVED]** An anytime algorithm that can revise its solution is different from an incremental algorithm that may only append decisions. The latter's impossibility result does not prevent effective warm starts; it prevents assuming that irrevocable retention is harmless.

### 5.3 Is there a principled old-trunk test?

**[DERIVED]** There are three different forms of evidence:

1. **Topological necessity.** A full-graph articulation may be mandatory *conditional on retaining a downstream region*. This certifies access, not that the region should remain selected.
2. **A global dominance certificate.** If a valid bound proves that every feasible solution omitting some trunk vertex is worse than the incumbent, that vertex is certified for that objective and budget. Additive exact solvers can sometimes support such tests. The stated arbitrary oracle supplies no such bound by itself.
3. **An empirical challenge.** Completed corridor alternatives, region rebuilds and fresh starts fail to beat the warm start within a stated budget. This is useful evidence of robustness to the tested challenges, not proof of optimality.

**[DERIVED] A sufficient stability inequality, with strong assumptions.** Suppose the feasible set is unchanged, every feasible `S` satisfies `|Fnew(S)−Fold(S)|≤ε`, and an old solution `S*` is known to beat **every** solution omitting trunk `K` by a margin `g>2ε`. Then for every such competitor `T`,

`Fnew(S*)−Fnew(T) ≥ Fold(S*)−Fold(T)−2ε ≥ g−2ε > 0`.

This certifies that a new optimum cannot omit `K`. It requires a global old margin and a uniform drift bound, not just a few observed score changes. Expanding `B` changes the feasible set, so the old margin does not cover newly feasible competitors. No opened source provided a practical way to derive these assumptions from the given oracle alone.

### 5.4 Reuse protocol

**[DERIVED]** Freeze `θ` during each graph solve. On a change, re-evaluate all retained incumbents and elites under the new `θ`; discard or version objective-dependent caches, marginal vectors, contribution ranks and operator history. Keep graph-only topology and shortest-node-count information. Cache by `(θ-version, canonical selected set)` and include `B` or other configuration in the key whenever evaluation depends on them. A relative-delta cache must also identify its base solution.

With three affordable starts, compare (a) a warm solution with unrestricted local/region moves, (b) a large rebuild from the warm solution, and (c) a fresh construction. These are deliberately different initialization policies, not three statistically exchangeable samples for fitting a common endpoint distribution. For seed-spread measurement, keep a separate experiment with identical policies and independent random seeds. Alternating optimization of `S` and other inputs can reach a coordinatewise plateau; it does not establish joint global optimality.

**What the sources say — [SOURCE].** Steiner reoptimization has approximation schemes for carefully defined local input changes and assumptions on the old solution. Incremental budgeted selection has negative results even with additive prizes on trees, and positive results explicitly trade extra budget for guarantees. These results do not justify freezing a heuristic trunk after arbitrary evaluator changes.

## Q6. Quality without a known optimum

### 6.1 What extreme-value estimators estimate

**[SOURCE] Carling and Meng (2016), Journal of Combinatorial Optimization [S22, opened author manuscript, §§2–5].** Statistical optimum estimation uses a sample of independently restarted heuristic outcomes to estimate the endpoint of their distribution. Defining fragment: “a sample of heuristic solutions”. For their minimization experiment, the Weibull point estimate is the best observed value; a fitted tail supplies a lower interval endpoint. They also compare first- and second-order jackknife estimators. With high-quality samples in their p-median experiments, they report: “The required number of replicates is as modest as 10.” These are empirical findings with conditions, not a sample-size theorem for arbitrary solvers.

**[SOURCE] A contrary case.** Velasco, Guerrero and Hospitaler (2022), Swarm and Evolutionary Computation [S23, opened abstract only], report that “global optimum estimates depend on the search algorithm's performance”. Their structural-engineering case compares two genetic algorithms and two evolution strategies with different settings. Poor searches give variable estimates; low variability from stronger searches can also make estimation fail. The full paper was not accessible, so exact instance counts and estimator implementations are **[UNVERIFIED]** here.

**[SOURCE] Another objective-dependent result.** Meng's 2015 working paper [S24, abstract/experimental section] reports “Jackknife estimators have better performance than Weibull estimators” for genetic search on 40 QAPLIB cases. It examines up to 100 heuristic outcomes and favours higher-order jackknife at larger sample sizes. This is a different outcome from treating Weibull as a generally preferred estimator.

**[DERIVED]** A convenient maximization tail model would assume that, near an unknown endpoint `z*`, `P(Z>z*−x)≈c x^α`. Then the maximum of `m` independent draws satisfies approximately `P(z*−max Zi>x)≈exp(−mcx^α)`. This explains the Weibull endpoint idea; it is not a fitted model or confidence bound for the supplied solver. If the solver never visits the optimal basin, the endpoint of its outcome distribution may itself be below the global optimum. Shared warm starts, adaptive budgets, reused elites, discreteness and mixtures of search policies complicate the model further. Independent repeated identical outcomes can still be independent; repetition alone does not prove dependence.

**[DERIVED]** Three seeds are insufficient to substantiate a tail model, test its fit and estimate an unknown endpoint with credible coverage. The positive p-median finding at ten restarts cannot be transferred as a universal minimum. Fitting a three-parameter curve through three outcomes would produce a number, not a verified gap estimate.

### 6.2 Seed spread: useful but limited

**[DERIVED]** A reported median 40% spread suggests sensitivity to the search trajectory. It does not distinguish unexamined trunk choices, repair bias, budget allocation, floor cliffs, inconsistent input versions or a scoring/cache bug. First state how spread is calculated and whether scores can cross zero; relative percentages can become unstable under penalties. Keep raw per-seed values, current input version, accepted improvements by operator, and best-so-far trajectories.

Large spread can coexist with one optimum found and two poor runs, or with all runs far below optimum. Zero spread can mean all runs repeatedly enter the same poor basin. Therefore seed dispersion is a reliability metric, not a bound on `F*−Fbest`.

### 6.3 When an additive relaxation gives a real upper bound

**[SOURCE]** Connected-reserve and MWCS formulations produce objective bounds for their **known additive objectives**, and connectivity cuts can strengthen them [S7], [S11], [S13]. They do not claim that frozen simulator marginals upper-bound a non-submodular function.

**[DERIVED]** A valid route to a certificate is to prove an envelope

`Fθ(S) ≤ c + Σ(v∈S) wv` for **every feasible S**.

Then a proven upper bound `U` on maximizing that envelope over rooted connected sets of size at most `B` also bounds the simulator optimum. Exact solution of the envelope is unnecessary if the solver returns a valid upper bound. For maximization, a heuristic envelope solution supplies a lower bound on the envelope optimum and cannot serve this purpose.

**[DERIVED]** Even ignoring connectivity gives a valid looser bound: include the fixed root contribution and the largest up to `B−1` positive remaining `wv`. This is an upper bound only after the envelope inequality is established. Singleton marginals do not establish it: two vertices can each have zero value alone and value 100 together. Pair terms, known physical maxima or verified simulator inequalities might yield an envelope; regression fit on sampled sets does not certify it.

**[DERIVED] An oracle limitation.** After any finite collection of queries that leaves a feasible set `T` unqueried, two functions can agree on every observation yet differ arbitrarily at `T`. Both remain deterministic non-submodular oracles. Without further restrictions or a known global range, no query-based method can certify a finite absolute optimality gap from those observations alone. A known range gives a trivial bound; a useful smaller bound needs additional structure.

### 6.4 Stopping rules and an honest quality statement

**[SOURCE]** The original LNS implementation report says the generic stop rule is “time-based”; its concrete VRP variant counts insertion checks since the last best improvement [S5, §3/§5]. Ropke–Pisinger use a fixed 25,000 iterations [S3]; CL-LNS reports anytime performance under runtime cutoffs [S21]. These are resource/progress criteria, not global optimality certificates.

**[DERIVED]** Stop this solve at its agreed wall-time/oracle limit, or after a predeclared low-return window **after** every important move family and size has had an opportunity. Keep a small final budget for trunk challenges and independent full evaluation of the chosen solution. Record the number of feasible challenges and the largest actual region rebuilt. If enumerating a finite neighbourhood exhaustively, a failed pass certifies only local optimality in that precise neighbourhood. Restricted shortlist or stochastic search cannot even make that exhaustive local claim.

**[DERIVED]** Report: best and all seed values; improvement over the existing solver under equal time; time to best; validation of connectedness/cardinality/floors; and “global gap unknown” unless a valid envelope bound exists. Best-known-relative regret is useful for comparisons but must be named as such. There is no evidence here for a defensible numeric global-gap estimate from three seeds.

**What the sources say — [SOURCE].** Statistical endpoint estimation has both positive application-specific studies and published failures. Exact additive formulations can produce valid bounds on their own objectives. Practical LNS commonly stops by resource or stagnation criteria; none of those facts converts a small set of oracle outcomes into a global certificate.

## Q7. Source code worth reading

**[SOURCE]** The following availability/licence statements were checked on 19 September 2026. MIT/BSD labels describe the repositories themselves; commercial solver dependencies have separate terms. No package was installed or benchmarked for this review.

| Code / status | Language and licence | Relevant implementation inspected | Connectivity representation and practical scope |
|---|---|---|---|
| [ALNS](https://github.com/N-Wouda/ALNS) [C1] | Python; MIT, licence opened | `SegmentedRouletteWheel.py`, `AlphaUCB.py`, selector docs | User supplies state, objective, destroy and repair. It has no built-in connected-tree neighbourhood or connectivity engine. Appropriate orchestration reference; observe the count-normalization difference in Q4. |
| [pcst_fast](https://github.com/fraenkel-lab/pcst_fast) [C2] | C++ with Python interface; MIT | `src/pcst_fast.cc` at `25ab31a245b2278848b5a8814924cdb3039b4279` | Cluster growth, edge-event queues/pairing heaps, component labelling and strong pruning. Constructs additive PCST/forest solutions. It does not implement the four local-search neighbourhoods or enforce a hard cardinality budget for arbitrary `F`. |
| [Heinz](https://github.com/ls-cwi/heinz) [C3] | C++; MIT; CPLEX, LEMON and OGDF dependencies | `blockcuttree.h` and `treeheuristicsolverimpl.h` at `ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa` | Explicit block-cut representation using LEMON; tree heuristic computes a Kruskal MST and solves a selected subtree problem. Useful decomposition/construction reference for additive MWCS; not proof of simulator-safe reductions. |
| [GMWCS solver](https://github.com/ctlab/gmwcs-solver) [C4] | Java; MIT; CPLEX dependency | `graph/Blocks.java` at `5b030be7e55a9db424de4a0ff7cc25af18a64bc8` | DFS entry/low-link values, edge stack and articulation/block extraction. Published solver uses decomposition, reductions and integer programming for node/edge-additive objectives [S13]. No link-cut tree identified in the inspected block code. |
| [NetworkX biconnected components](https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/biconnected.html) [C5] | Python; BSD-3-Clause | `_biconnected_dfs`, articulation and block generators | Official definition: “Yield the articulation points, or cut vertices, of a graph.” Nonrecursive DFS with discovery/low-link information; static recomputation, not dynamic forest maintenance. Useful correctness reference. |
| [SCIP-Jack](https://scipjack.zib.de/) [C6] | Solver with C++ and Python interfaces advertised | Official availability page only; current implementation not obtained | Version 2.2 announced 3 May 2026; available on request under **ZIB Academic License**, free for noncommercial academic use. Do not classify it as unrestricted open-source because SCIP core uses a different licence. Current neighbourhood/data-structure details were not inspected. |

**[SOURCE]** The `pcst_fast` API permits a root, a target number of clusters, and pruning modes; the README's description is “Goemans-Williamson scheme”. Its associated 2014 paper [S10] preserves the additive PCST factor-2 Lagrangian guarantee. That guarantee does not apply after replacing the prizes with a changing nonlinear objective. The inspected Heinz tree-heuristic implementation explicitly calls `lemon::kruskal`; the GMWCS block code explicitly stores DFS `enter` and `up` maps. These are source observations, not inferred architecture claims from repository names.

**[DERIVED] Data-structure choice at this scale.** Start with a 1,300-bit membership mask or equivalent, adjacency lists, a selected spanning tree for proposing paths, and direct BFS/DFS verification on `G[S']`. Compute articulation points on `G[S]` for deletion candidates and on full `G` for globally unavoidable access. The graph has approximately `1,300×2.3/2 ≈ 1,495` edges, so asymptotically linear graph checks visit a small graph; actual runtime still needs measurement. A static DFS interval order can make auxiliary-tree subtree extraction cheap after each accepted change, but it is not an Euler-tour-tree dynamic data structure.

**[SOURCE]** Uchoa–Werneck describe link-cut trees for path maximum, cut and link operations, but also note that simpler linear-time variants can be faster in practice when paths are not extremely long [S1, §2.1]. Their published graph machinery is worth reading even without adopting its objective arithmetic.

**[DERIVED]** Fully dynamic trees do not by themselves solve connectivity in a cyclic induced graph: an edge deletion may require finding a replacement non-tree edge. Nor do they make an expensive nonadditive score additive. At this problem size, implement complex dynamic connectivity only if profiling shows static checks are significant next to 7 ms evaluations and 1–2 seconds per rebuilt node.

**[UNVERIFIED]** A maintained, licence-verified public implementation of all four Uchoa–Werneck moves that can directly accept this simulator was not located. No Euler-tour-tree implementation was verified in the inspected solver files. SCIP-Jack's current request-only code was not accessed. These are limits of this review, not claims that no such implementation exists.

**What the sources say — [SOURCE].** Open code provides generic ALNS control, additive PCST construction, MWCS decomposition and ordinary articulation algorithms. The inspected implementations do not constitute a ready-made rooted non-submodular oracle solver. The current SCIP-Jack distribution has a more restrictive availability/licence status than the public MIT libraries.

## Cross-technique comparison

**[DERIVED]** Costs below are adaptations using the supplied timings, not timings published by the papers. `a` is the number of candidate regions; `c` is the number of complete feasible alternatives actually scored; `h` is the number of repairs launched. All rows require **0 marginal passes** unless one is explicitly bought as an optional surrogate refresh. “No” means the cited implementation uses explicit objective structure; “unknown” means no matching application was verified. “Yes” is qualified when evidence is only from another domain.

| Technique | Changes which part | Picks the place by | Cost per move/pass in these units | Used with black-box objectives? | Primary evidence |
|---|---|---|---|---|---|
| Steiner vertex insertion/elimination | One vertex, including a removable internal vertex | MST edge-cost improvement; derived version uses legal candidate probes | `c W`; insertion at full budget requires a compound move | **No** in source | [S1], §§2.1–2.2 |
| Key-path / atomic corridor replacement | Interior path and access route | Key-path topology, alternative component connections | `c W`; e.g. 400 W = 2.8 s; plus optional `R(q)` | **No** in source; oracle adaptation **unknown** | [S1], §3.2 |
| Key-vertex elimination / multicomponent rebuild | Branching point and incident paths | Reconnect retained components | `c W` for completed candidates; `h R(q)` if using regrow | **No** in source | [S1], §3.3 |
| Leaf swap + spanning-tree permutation | Leaves; different removable vertices after rewiring | Additive node costs and changed representation | 0 W for rewiring alone; `c W` for scored swaps | **No** in source | [S6], §3 |
| Subtree/cyclic multi-exchange | Several branches or rooted subtrees | Negative subset-disjoint cycles in an improvement graph | No transferable exact oracle scan bound; cap complete candidates at `c W` | **No** in source | [S19], §§3–5 |
| Conditional worst group removal | Feasibly removable leaf/group; trunk plus dependency closure | Low current removal loss, optionally per freed node | `a W` frozen scores, up to roughly `a q W` sequential rescoring, plus `R(q)` | **No** for routing source; oracle delta definition itself is implementable | [S3], §3.1.3; [S9], §2 |
| Related / Shaw removal | A group, contiguous or scattered | Graph/domain similarity and shared dependencies | 0 W for structural score; `R(q)` + final W if needed | **No** in classical sources | [S3], §3.1.1; [S5], §4 |
| Cluster removal | Cluster of linked decisions | Kruskal split / derived graph region | 0 W for structural choice; `R(q)` | **No** in source | [S4], §5.3 |
| History-based removal | Poor-context nodes or compatible groups | Best observed context; elite co-occurrence | 0 W to read history; `R(q)` | **Yes, simulation-based routing**, not this tree problem | [S4], §§5.4–5.5; [S20], §4 |
| Regret / alternative repair | Rebuilds destroyed region | Opportunity loss between insertion options | Approximately `h R(q)` only for equally cheap repairs; explicit cap for look-ahead | **No** for original regret; simulation repair exists separately | [S3], §3.2.2; [S20] |
| Sampled Shapley | Diagnostic attribution, not itself a move | Average marginal over permutation contexts | At most `m(k+1) W`, only for feasible coalition game | **Yes**, callable coalition utilities in attribution; destroy-search benefit **unknown** | [S8] |
| Banzhaf MSR | Diagnostic attribution | Conditional means over random coalitions | `m W` total, only for feasible coalition game; accuracy not fixed by `m` alone | **Yes**, ML utility calls; connected-destroy benefit **unknown** | [S9], §4 |
| Learned variable destroy | ILP decision subsets | Trained expert imitation/contrastive policy | Training and inference unknown here; `R(q)` not equivalent to sub-ILP solve | **No** for CL-LNS | [S21] |
| Learned operator/size control | Selects move family, size and repair | Search-state policy | 0 extra W for inference itself; training cost unquantified here | **Yes, stochastic routing simulation** | [S20] |
| Roulette / bandit selection | Chooses among available moves | Recent outcome/effort rewards | 0 extra W/M; selected arm pays its full cost | **Yes** for generic ALNS callback integration; no task-specific performance proof | [S3], [S12], [C1] |
| Warm-start challenge | Potentially entire old structure | Re-evaluation plus alternative rebuilds | 0.1 s per retained full re-evaluation + ordinary search budget | **No** for additive reoptimization theorem; oracle use is derived | [S15], [S16] |

## Three transferable algorithms — all [DERIVED]

These sketches deliberately separate structural construction from evaluation. They are proposed adaptations, not pseudocode reproduced from the papers. `Exact(S0,T,θ)` uses one what-if relative to the immutable snapshot `S0`, removing `S0\T` and adding `T\S0`; both sets must have the same evaluator input version. It returns the same value as a full evaluation of `T`. `Valid(T)` checks root, unique-node budget, connectivity and any explicitly available mandatory constraints. An evaluated candidate does not mutate the live incumbent. A final full evaluation checks the chosen result.

### A. Atomic internal-path replacement

```text
01 function CorridorPass(S, θ, B, query_cap, alternative_cap):
02     S0 ← immutable copy of S; best ← S0; base ← cached Fθ(S0)
03     H ← G induced by S0; tree ← spanning tree of H rooted at r
04     paths ← internal path proposals from tree and blocks of H
05     queries ← 0
06     for A in paths, ordered by structural opportunity:
07         if r ∈ A: continue
08         C ← S0 \ A; components ← connected components of G[C]
09         if no connector avoiding A can join these components within B: continue
10         proposals ← diverse connector sets avoiding A, capped at alternative_cap
11         for P in proposals:
12             T ← C ∪ P                         // preserve every retained component
13             if T = S0 or not Valid(T): continue
14             if queries = query_cap: return best
15             value ← Exact(S0, T, θ); queries ← queries + 1
16             if value > cached Fθ(best): best ← T; cache its value
17     return best
```

**[DERIVED]** “Diverse connector sets” is a bounded graph generator, not an exact Steiner solver for `F`. At minimum vary the access route and additional-node count; for more than two retained components it must construct a connecting network, not merely one path. This pass temporarily forbids removed path vertices to make bypass attempts concrete. It intentionally misses alternatives that retain part of that path; other proposals/regions cover those. `T` may use fewer than `B` nodes, which is legal under the assumed cap. Filling leftover budget is a separately charged repair and is not assumed beneficial for a nonmonotone objective. Cost: at most `query_cap W`, plus graph generation.

### B. Diagnose a region by completed replacements

```text
01 function RegionChallenge(S, θ, q, region_cap, repair_cap, deadline):
02     S0 ← immutable copy of S; best ← S0
03     regions ← mixed related, branch, internal and scattered proposals
04     regions ← dependency-aware candidates near size q, capped at region_cap
05     shortlist ← empty list
06     for A in regions:
07         if r ∈ A: continue
08         C ← S0 \ A
09         if G[C] is connected: loss ← Fθ(S0) - Exact(S0, C, θ)
10         else: loss ← unknown                    // never score disconnected C
11         tests ← cheap complete reconnections/replacements for (C, A)
12         evaluate only Valid(tests), within the probe allowance and deadline
13         update best using those exact completed values
14         add (A, C, observed opportunity, loss, structural novelty) to shortlist
15     choose repair_cap entries using evidence plus a random exploration slot
16     for entry in chosen entries while time remains:
17         anchor ← connected retained core or a budget-feasible reconnected core
18         if no such anchor is constructed: skip this entry
19         for repair policy in the small allowed portfolio while time remains:
20             T ← bounded repair(anchor, θ), permitting changed access choices
21             if not Valid(T): continue; else evaluate/cache Exact(S0, T, θ)
22             if Fθ(T) > Fθ(best): best ← T
23     return best, actual costs and changed-region statistics
```

**[DERIVED]** Every repair that uses the 7 ms interface must evaluate connected partial candidates. If all retained components cannot be reconnected within budget, another region proposal must explicitly include the descendants to discard; the repair cannot silently delete supposedly retained components. Rank by observed completed improvement where available, otherwise mix uncertain candidates rather than declaring them weak from an infeasible deletion. Use reserved probe/repair allowances inside the deadline. With `a` feasible removal probes, `c` completed probes and `h` repairs, cost is roughly `(a+c) W + ΣR(qactual)`, avoiding double-counted final evaluations.

### C. Time-aware portfolio with reoptimization

```text
01 function SolveVersion(θ, B, saved_elites, wall_budget, query_budget):
02     freeze θ; start timer; invalidate objective caches from older versions
03     elites ← feasible saved sets, fully reevaluated under θ
04     starts ← warm, large-rebuild and fresh starts (use fresh if no warm exists)
05     arms ← small set of (destroy family, size bin, repair policy)
06     initialize discounted return estimates and a nonzero exploration allocation
07     best ← best exactly evaluated feasible start
08     for each start using an explicit share of the remaining wall budget:
09         current ← start; initialize temperature from feasible score deltas
10         while wall time and query allowance remain for this share:
11             arm ← select by return estimates with forced exploration
12             before ← Fθ(best); begin measuring the arm's complete elapsed time
13             candidate, counters ← run arm(current, θ, remaining allowances)
14             elapsed ← all scoring, construction, failed repair and evaluation time
15             if candidate is Valid and its exact score is available:
16                 if Fθ(candidate) > Fθ(best): best ← candidate
17                 Δ ← Fθ(candidate) - Fθ(current)
18                 if Δ ≥ 0 or random() < exp(Δ / temperature): current ← candidate
19             credit ← max(0, Fθ(best) - before) / max(elapsed, timer_resolution)
20             discount/update this arm's credit; log outcomes and actual size
21             update temperature and remaining allowances, including overhead
22     fully reevaluate best; check structure and all exposed mandatory constraints
23     save best and diverse elites with θ-version; return best and search log
```

**[DERIVED]** Reserve final validation time before the search starts. The `starts` construction itself consumes the total budget. If `θ` changes, stop this frozen-version solve and start a new version; do not compare old scores directly. This is a practical portfolio proposal, not a UCB theorem. Compare its selector against the same arms in a fixed/uniform schedule so that any gain is not wrongly attributed to adaptation rather than the new moves.

## Failure modes and negative results

| Failure / negative result | Evidence and implication |
|---|---|
| A connector looks worthless alone but enables a valuable region | **[DERIVED]** Its singleton or conditional deletion score cannot be interpreted as intrinsic value. Evaluate whole connected replacements. |
| A removed group contains one member of a synergy, so regrow recreates the incumbent | **[SOURCE]** Ropke–Pisinger's cluster example explicitly explains why removing only part of a group sends insertions back to the old route [S4, Fig. 5]. **[DERIVED]** This is a plausible analogous failure of the current repair, not a measured diagnosis of this solver. |
| More ruin does not necessarily improve the search | **[SOURCE]** Size changes alter repair runtime and success [S3], [S5]. **[DERIVED]** An expensive destroy can yield fewer useful trials; naive fixed-iteration comparisons favour unequal budgets. |
| The real graph offers no bypass | **[DERIVED]** A full-graph articulation blocks corridor replacement while downstream selections are retained. Increase the reconsidered dependency closure or keep that access vertex. |
| The parent tree falsely forbids a valid deletion | **[SOURCE]** Same-node tree permutation exposes new cardinality neighbours [S6]. **[DERIVED]** Check induced-graph articulation rather than treating parent descendants as unavoidable. |
| Edge-only moves do no optimization work | **[DERIVED]** If `S` does not change, the supplied set objective cannot change. Rewiring may aid future moves but should not count as an objective improvement. |
| Submodular guarantees are imported into complementary rewards | **[SOURCE]** CSM/GCB guarantees have structural and sometimes budget-slack assumptions [S14], [S17]. **[DERIVED]** Those guarantees do not survive this violation. |
| Historical consensus suppresses diversification | **[SOURCE]** Direct low co-occurrence-score removal was unsuccessful in [S4, §5.5]; the authors changed how history was used. |
| Adaptation rewards an ineffective combination | **[SOURCE]** Original ALNS credits both components jointly [S3]. **[DERIVED]** Separate weights can hide destroy/repair interactions; an oversized action space can make coupled learning ineffective too. |
| Shapley values rank components well but not rebuild opportunities | **[DERIVED]** Average attribution and best alternative use of a budget are different optimization quantities. Connectivity/completion changes the attribution game. |
| Learned policies fail after evaluator changes | **[SOURCE]** Published learned methods have explicit training tasks/features [S20], [S21]. **[DERIVED]** Generalization to new `θ`, floors or budget must be tested; it is not implied by good routing/ILP results. |
| Old and new budget optima share almost nothing | **[SOURCE]** Incremental same-budget limitations [S16]; **[DERIVED]** the unit-node counterexample in Q5. |
| Three stable seeds are mistaken for optimality | **[SOURCE]** EVT failures and model limitations [S22], [S23], [S24]; **[DERIVED]** a never-visited basin is invisible in seed spread. |
| A surrogate “upper bound” underestimates synergistic value | **[DERIVED]** Without a proved global envelope, an additive score is only a search surrogate. |
| Cached what-if scores survive a changed context | **[DERIVED]** Determinism holds only for fixed evaluator inputs and configuration. Version caches and verify the final result with the independent full evaluator. |

## Engineering decision and validation plan — [DERIVED]

Build around four boundaries: a **versioned evaluator adapter**, a **connected-candidate generator**, a **repair interface**, and an **experiment logger**. This report does not name repository modules because the request is an abstract literature review and no implementation audit was performed.

1. Establish that every scored proposal is a canonical connected set and that relative what-if values match full evaluation on representative accepted candidates. Record feasibility/floor outputs separately if available.
2. Add path replacement and dependency-aware internal-region candidates. Count *actual* reconsidered trunk nodes and changed access routes. The given 32/38/8/22 percentages should not be treated as disjoint until their measurement convention is confirmed: nested hanging subtrees can overlap.
3. Add an alternative repair policy and a small size schedule. Compare against the existing solver with exactly the same wall budget and fixed `θ`; retain all three paired seed outcomes per instance rather than only best-of-three.
4. Only then compare uniform/fixed operator scheduling with roulette and time-aware selection. Keep construction, marginal refreshes, failures and regrow inside the measured budget. Report exploratory results as exploratory when only three seeds are available.
5. Exercise changed-`θ` and larger-`B` cases, comparing warm, large-rebuild and fresh initializations. Keep the best feasible solution across those searches under the **new** objective.

For each run store: input/version hash; `B`; seed and initialization policy; exact selected sets; best value over wall time; W/full/M counts; repair seconds; attempted and completed region sizes; rejected connectivity/cardinality/floor checks; and which accepted moves changed old trunk vertices. Use equal-time value and time-to-target comparisons. Targets may be pooled best-known values, explicitly labelled as such. This validation plan tests the central hypotheses without pretending to certify a global optimum.

## Bibliography and evidence locators

The source map below distinguishes full papers, author versions, documentation, inspected code and unavailable originals. A source identifier elsewhere in this report refers to the version specified here.

- **S1.** Eduardo Uchoa and Renato F. Werneck (2012). *Fast Local Search for the Steiner Problem in Graphs*. ACM Journal of Experimental Algorithmics 17(2), Article 2.2. DOI `10.1145/2133803.2184448`. [Opened author PDF][S1]. Definitions §§2–3; practical data structures §2.1; experiments §5. Full text.
- **S2.** Markus Chimani, Maria Kandyba, Ivana Ljubić and Petra Mutzel (2009). *Obtaining Optimal k-Cardinality Trees Fast*. ACM Journal of Experimental Algorithmics 14; preliminary ALENEX 2008 version. [Opened author manuscript][S2]; [institutional publication metadata](https://ucrisportal.univie.ac.at/en/publications/obtaining-optimal-k-cardinality-trees-fast/). Abstract/§1 for conventions; computational study for scale and exact-versus-heuristic comparison.
- **S3.** Stefan Ropke and David Pisinger (2006). *An Adaptive Large Neighborhood Search Heuristic for the Pickup and Delivery Problem with Time Windows*. Transportation Science 40(4), 455–472. DOI `10.1287/trsc.1050.0135`. [Opened 8 August 2005 technical-report version][S3]. Printed pp. 6–10 for operators/weights; §4.3 for parameter vector; Table 3 for non-superiority to the best simple choices. PDF has a repository cover page.
- **S4.** Stefan Ropke and David Pisinger (2006). *A Unified Heuristic for a Large Class of Vehicle Routing Problems with Backhauls*. European Journal of Operational Research 171(3), 750–775. DOI `10.1016/j.ejor.2004.09.004`. [Opened 28 July 2004 technical report][S4]. §§5.3–5.5, printed pp. 11–12 / PDF pp. 12–13, for cluster and history removal.
- **S5.** Philip Kilby, Patrick Prosser and Paul Shaw (April 1998). *Implementation of LNS for Constrained VRPs*. APES Report APES-01-1998. [Opened author-uploaded full text][S5]. §§2–5. The separate Shaw CP98 original, DOI `10.1007/3-540-49481-2_30`, was located but its full PDF timed out; no quote from that unavailable original is attributed here.
- **S6.** Christian Blum and Matthias Ehrgott (2003). *Local Search Algorithms for the k-Cardinality Tree Problem*. Discrete Applied Mathematics 128, 511–540. DOI `10.1016/S0166-218X(02)00548-6`. [Opened earlier technical-report PDF][S6], visually read because its embedded text encoding is defective; [repository record](https://kluedo.ub.rptu.de/frontdoor/index/index/year/2000/docId/519). Printed pp. 8–13 for leaf exchange, tree permutation, complexity and crossbreeding. Page references are to this report, not the final journal pagination.
- **S7.** Bistra Dilkina and Carla P. Gomes (2010). *Solving Connected Subgraph Problems in Wildlife Conservation*. CPAIOR, LNCS 6140, 102–116. [Opened author PDF][S7]. §2 for budget/quota/PCST distinctions; formulations and experiments for connectivity bounds and conservation instances.
- **S8.** Mark A. Burgess and Archie C. Chapman (2021). *Approximating the Shapley Value Using Stratified Empirical Bernstein Sampling*. IJCAI, 73–81. DOI `10.24963/ijcai.2021/11`. [Opened proceedings PDF][S8]. §§1, 3–4; PDF pp. 4–5 for initialization and example games.
- **S9.** Jiachen T. Wang and Ruoxi Jia (2023). *Data Banzhaf: A Robust Data Valuation Framework for Machine Learning*. AISTATS, PMLR 206, 6388–6421. [Opened paper][S9]; [official metadata](https://proceedings.mlr.press/v206/wang23e.html). §2 for LOO/range assumption; §4.3 and Theorem 4.9 for MSR and sample complexity.
- **S10.** Chinmay Hegde, Piotr Indyk and Ludwig Schmidt (2014). *A Fast, Adaptive Variant of the Goemans-Williamson Scheme for the Prize-Collecting Steiner Tree Problem*. Workshop of the 11th DIMACS Implementation Challenge. [Opened author paper][S10]. Abstract/§1 and growth/pruning algorithm. Additive PCST experiments include approximately 340,000 edges.
- **S11.** Ralf Borndörfer, Stephan Schwartz and William Surau (2022). *Rooted Maximum Weight Connected Subgraphs with Balancing and Capacity Constraints*. INOC, 63–68. DOI `10.48786/inoc.2022.12`. [Opened proceedings PDF][S11]. §2 for formulation; §5 for 240 instances and 563–569 nodes.
- **S12.** Gregor Hendel (2018). *Adaptive Large Neighborhood Search for Mixed Integer Programming*. ZIB Report 18-60, 18 December 2018; subsequently published in Mathematical Programming Computation (2022). [Opened report][S12]. §3.3, printed pp. 12–13 / PDF pp. 14–15, for reward/effort; §4 for bandits; Table 4 for results. Numerical claims here refer to the report.
- **S13.** Alexander A. Loboda, Maxim N. Artyomov and Alexey A. Sergushichev (2016). *Solving Generalized Maximum-Weight Connected Subgraph Problem for Network Enrichment Analysis*. WABI 2016; arXiv:1605.02168. [Opened full preprint][S13]. Formulation, decomposition and §6 benchmark comparisons; ten runs with a 1,000-second cutoff in the reported study.
- **S14.** Philip Cervenjak, Junhao Gan, Naonori Kakimura, Seeun William Umboh and Anthony Wirth (2026). *A Radius-Sensitive Approximation Algorithm for Connected Submodular Maximization*. AAMAS 2026. DOI `10.65109/IPZQ7320`; arXiv:2605.30053. [Opened full paper][S14]. Abstract and formal problem/approximation statements. Conference identification is printed on page 1; this is not labelled merely an unreviewed preprint.
- **S15.** Davide Bilò (2018). *New Algorithms for Steiner Tree Reoptimization*. ICALP, LIPIcs 107, Article 19. DOI `10.4230/LIPIcs.ICALP.2018.19`; arXiv:1804.10791. [Opened full preprint][S15]. §1.1 specifies the four modifications and the old-solution assumptions. A later 2024 publisher version was found but not usable as full text in this session.
- **S16.** Yann Disser, Svenja M. Griesbach, Max Klimm and Annette Lutz (2024). *Bicriterial Approximation for the Incremental Prize-Collecting Steiner-Tree Problem*. arXiv:2407.04447, opened v1. [Opened full preprint][S16]. Abstract and Theorems 1–2; additive budget slack is essential to the stated guarantees.
- **S17.** Haifeng Zhang and Yevgeniy Vorobeychik (2016). *Submodular Optimization with Routing Constraints*. AAAI. [Opened proceedings PDF][S17]. GCB algorithm, assumptions and sensor/marketing experiments.
- **S18.** Friedrich Eisenbrand, Fabrizio Grandoni, Thomas Rothvoß and Guido Schäfer (2008). *Approximating Connected Facility Location Problems via Random Facility Sampling and Core Detouring*. SODA. [Opened author PDF][S18]. §1 for objective and approximation construction. The black-box reference is to a known facility-location subsolver.
- **S19.** Ravindra K. Ahuja, James B. Orlin and Dushyant Sharma (2001). *Multi-Exchange Neighborhood Structures for the Capacitated Minimum Spanning Tree Problem*. Mathematical Programming 91, 71–97. DOI `10.1007/s101070100234`. [Opened author-uploaded full manuscript][S19], revised March 2001. §§3–5 for multi-exchange and improvement graphs; §7 for benchmarks. Publisher/PDF mirror access was problematic; the author-uploaded text was available.
- **S20.** Robbert Reijnen, Yingqian Zhang, Hoong Chuin Lau and Zaharah Bukhsh (2024). *Online Control of Adaptive Large Neighborhood Search Using Deep Reinforcement Learning*. ICAPS 34. DOI `10.1609/icaps.v34i1.31507`. [Opened full arXiv version][S20]; [official publication record](https://ojs.aaai.org/index.php/ICAPS/article/view/31507). §§3–4 for control, simulation counts, operators and benchmark sizes.
- **S21.** Taoan Huang, Aaron M. Ferber, Yuandong Tian, Bistra Dilkina and Benoit Steiner (2023). *Searching Large Neighborhoods for Integer Linear Programs with Contrastive Learning*. ICML, PMLR 202, 13869–13890. [Opened proceedings paper][S21]; [official metadata](https://proceedings.mlr.press/v202/huang23g.html). §2.2 for size control; model/training and experiments for scope.
- **S22.** Kenneth Carling and Xiangli Meng (2016). *On Statistical Bounds of Heuristic Solutions to Location Problems*. Journal of Combinatorial Optimization 31(4), 1518–1549. DOI `10.1007/s10878-015-9839-0`. [Opened author-uploaded manuscript][S22], headed *Confidence in heuristic solutions?*. §§2–5, printed pp. 4–16, for estimators, assumptions and conditional positive results. The displayed final-article abstract and author manuscript are distinguished where their scope differs.
- **S23.** Luis Velasco, Hector Guerrero and Antonio Hospitaler (2022). *Can the Global Optimum of a Combinatorial Optimization Problem Be Reliably Estimated Through Extreme Value Theory?* Swarm and Evolutionary Computation 75, 101172. DOI `10.1016/j.swevo.2022.101172`. [Opened abstract][S23]. Full text unavailable; only the abstract's conclusions and stated experimental design are used.
- **S24.** Xiangli Meng (2015). *Statistical Bound of Genetic Solutions to Quadratic Assignment Problems*. Dalarna University Working Papers 2015:02. [Opened institutional PDF][S24]. Abstract and experimental section. This is a working paper, not a claimed journal publication.
- **S25.** Stefan Voigt (online 18 May 2024). *A Review and Ranking of Operators in Adaptive Large Neighborhood Search for Vehicle Routing Problems*. European Journal of Operational Research. DOI `10.1016/j.ejor.2024.05.033`. [Opened accepted/open-access paper][S25]. **Secondary evidence**, used for taxonomy, leads and cross-study scope only; not substituted for unavailable original definitions.
- **S26.** Thomas Pajor, Eduardo Uchoa and Renato F. Werneck (2014). *A Robust and Scalable Algorithm for the Steiner Problem in Graphs*. arXiv:1412.2787. [Opened full report][S26]. Multistart, recombination, local search and dual ascent; additive-STP context. Its use of “black boxes” for modular local-search components does not mean an arbitrary objective oracle.

**Code/documentation sources, current when opened:**

- **C1.** N-Wouda/ALNS maintainers, Python ALNS. [Repository][C1]; [selector documentation](https://alns.readthedocs.io/en/latest/api/select.html); [MIT licence](https://raw.githubusercontent.com/N-Wouda/ALNS/master/LICENSE.md); [segment-update code](https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/SegmentedRouletteWheel.py); [AlphaUCB code](https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/AlphaUCB.py). These last files were read from `master`, not a pinned release.
- **C2.** Fraenkel Lab/pcst_fast maintainers. [Repository][C2]; [pinned implementation](https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/src/pcst_fast.cc); [pinned MIT licence](https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/LICENSE.txt).
- **C3.** Mohammed El-Kebir, Gunnar W. Klau and Heinz contributors. [Repository][C3]; [MIT licence](https://raw.githubusercontent.com/ls-cwi/heinz/master/LICENSE); [pinned block-cut tree](https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/blockcuttree.h); [pinned tree heuristic](https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/impl/treeheuristicsolverimpl.h).
- **C4.** Loboda, Artyomov, Sergushichev and GMWCS contributors. [Repository][C4]; [MIT licence](https://raw.githubusercontent.com/ctlab/gmwcs-solver/master/LICENSE); [pinned block decomposition](https://raw.githubusercontent.com/ctlab/gmwcs-solver/5b030be7e55a9db424de4a0ff7cc25af18a64bc8/src/main/java/ru/ifmo/ctddev/gmwcs/graph/Blocks.java).
- **C5.** NetworkX developers. [Opened source documentation][C5]; [articulation API](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html); [BSD-3-Clause licence](https://raw.githubusercontent.com/networkx/networkx/main/LICENSE.txt). The documentation identifies version 3.6.1 and cites Hopcroft–Tarjan (1973).
- **C6.** SCIP-Jack developers. [Official availability and licence page][C6]. Version 2.2, May 2026; source requested through the authors, not obtained during this review.

[S1]: https://renatowerneck.wordpress.com/wp-content/uploads/2016/06/uw12-steiner-ls.pdf
[S2]: https://ivanaljubic.github.io/docs/publications/kCardinalityTrees_JEA.pdf
[S3]: https://backend.orbit.dtu.dk/ws/portalfiles/portal/3154899/An%20adaptive%20large%20neighborhood%20search%20heuristic%20for%20the%20pickup%20and%20delivery%20problem%20with%20time%20windows_TechRep_ropke_pisinger.pdf
[S4]: https://backend.orbit.dtu.dk/ws/portalfiles/portal/3155117/A%20unified%20heuristic%20for%20a%20large%20class%20of%20Vehicle%20Routing%20Problems%20with%20Backhauls_TechRep_Ropke_Pisinger.pdf
[S5]: https://www.researchgate.net/publication/2914450_Apes_Report_Apes-01-1998
[S6]: https://kluedo.ub.rptu.de/files/519/gelb_48.pdf
[S7]: https://www.cs.cornell.edu/gomes/pdf/2010_dilkina_cpaior_subgraph.pdf
[S8]: https://www.ijcai.org/proceedings/2021/0011.pdf
[S9]: https://proceedings.mlr.press/v206/wang23e/wang23e.pdf
[S10]: https://people.csail.mit.edu/ludwigs/papers/dimacs14_fastpcst.pdf
[S11]: https://openproceedings.org/2022/conf/inoc/INOC_2022_paper_19.pdf
[S12]: https://optimization-online.org/wp-content/uploads/2018/12/6992.pdf
[S13]: https://arxiv.org/pdf/1605.02168
[S14]: https://arxiv.org/pdf/2605.30053
[S15]: https://arxiv.org/pdf/1804.10791
[S16]: https://arxiv.org/pdf/2407.04447
[S17]: https://cdn.aaai.org/ojs/10066/10066-13-13594-1-2-20201228.pdf
[S18]: https://people.idsia.ch/~grandoni/Pubblicazioni/EGRS08soda.pdf
[S19]: https://www.researchgate.net/publication/2384064_Multi-exchange_neighborhood_structures_for_the_capacitated_minimum_spanning_tree_problem
[S20]: https://arxiv.org/pdf/2211.00759
[S21]: https://proceedings.mlr.press/v202/huang23g/huang23g.pdf
[S22]: https://www.researchgate.net/publication/267025927_On_statistical_bounds_of_heuristic_solutions_to_location_problems
[S23]: https://www.researchgate.net/publication/363041653_Can_the_Global_Optimum_of_a_Combinatorial_Optimization_Problem_be_Reliably_Estimated_Through_Extreme_Value_Theory
[S24]: https://du.diva-portal.org/smash/get/diva2%3A791806/FULLTEXT01.pdf
[S25]: https://edoc.ku.de/id/eprint/34084/1/1-s2.0-S0377221724003928-main.pdf
[S26]: https://arxiv.org/pdf/1412.2787
[C1]: https://github.com/N-Wouda/ALNS
[C2]: https://github.com/fraenkel-lab/pcst_fast
[C3]: https://github.com/ls-cwi/heinz
[C4]: https://github.com/ctlab/gmwcs-solver
[C5]: https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/biconnected.html
[C6]: https://scipjack.zib.de/

## URL access register

This register lists opened or attempted target URLs, including redirects, failed access, discovery queries and code/API inspection. A successful HTTP response does not imply usable full text; evidence status is specified in the bibliography. Search-result snippets were used to locate sources, not to reconstruct unavailable definitions. Repeated openings are deduplicated. Browser search queries were also used for discovery; only retained target URLs are reproduced, rather than inventing missing browser-history addresses. Access date: 19 September 2026.

| # | Opened / attempted URL | Access record |
|---|---|---|
| 1 | [https://www.google.com/search?q=fast+local+search+Steiner+problem+Uchoa+Werneck+key+vertex+path+pdf](https://www.google.com/search?q=fast+local+search+Steiner+problem+Uchoa+Werneck+key+vertex+path+pdf) | search_steiner: HTTP 200; sparse/interstitial content possible |
| 2 | [https://www.google.com/search?q=Steiner+tree+reoptimization+weights+local+modifications+pdf](https://www.google.com/search?q=Steiner+tree+reoptimization+weights+local+modifications+pdf) | search_reopt: HTTP 200; sparse/interstitial content possible |
| 3 | [https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+local+search+pdf](https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+local+search+pdf) | search_kct: HTTP 200; sparse/interstitial content possible |
| 4 | [https://www.google.com/search?q=Ropke+Pisinger+2006+adaptive+large+neighborhood+search+pdf](https://www.google.com/search?q=Ropke+Pisinger+2006+adaptive+large+neighborhood+search+pdf) | search_alns: HTTP 200; sparse/interstitial content possible |
| 5 | [https://www.google.com/search?q=optimization+Weibull+extreme+value+estimating+global+optimum+multistart+de+Haan](https://www.google.com/search?q=optimization+Weibull+extreme+value+estimating+global+optimum+multistart+de+Haan) | search_extreme: HTTP 200; sparse/interstitial content possible |
| 6 | [https://www.google.com/search?q=budgeted+connected+submodular+maximization+connected+reserve+design+pdf](https://www.google.com/search?q=budgeted+connected+submodular+maximization+connected+reserve+design+pdf) | search_connected: HTTP 200; sparse/interstitial content possible |
| 7 | [https://html.duckduckgo.com/html/?q=fast+local+search+Steiner+problem+Uchoa+Werneck+pdf](https://html.duckduckgo.com/html/?q=fast+local+search+Steiner+problem+Uchoa+Werneck+pdf) | ddg_steiner: request failed |
| 8 | [https://arxiv.org/abs/1412.2787](https://arxiv.org/abs/1412.2787) | arxiv_steiner: HTTP 200 |
| 9 | [https://www.bing.com/search?q=Ropke+Pisinger+2006+adaptive+large+neighborhood+search+pdf](https://www.bing.com/search?q=Ropke+Pisinger+2006+adaptive+large+neighborhood+search+pdf) | bing_alns: HTTP 200 |
| 10 | [https://www.microsoft.com/en-us/research/wp-content/uploads/2010/09/steiner.pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/09/steiner.pdf) | werneck: HTTP 404 |
| 11 | [https://backend.orbit.dtu.dk/ws/portalfiles/portal/3154899/ropke.pdf](https://backend.orbit.dtu.dk/ws/portalfiles/portal/3154899/ropke.pdf) | ropke: HTTP 200 |
| 12 | [https://backend.orbit.dtu.dk/ws/portalfiles/portal/3154899/An%20adaptive%20large%20neighborhood%20search%20heuristic%20for%20the%20pickup%20and%20delivery%20problem%20with%20time%20windows_TechRep_ropke_pisinger.pdf](https://backend.orbit.dtu.dk/ws/portalfiles/portal/3154899/An%20adaptive%20large%20neighborhood%20search%20heuristic%20for%20the%20pickup%20and%20delivery%20problem%20with%20time%20windows_TechRep_ropke_pisinger.pdf) | ropke redirect: HTTP 200 |
| 13 | [https://www.bing.com/search?q=%22k-cardinality+tree%22+%22search%22+pdf](https://www.bing.com/search?q=%22k-cardinality+tree%22+%22search%22+pdf) | bing_kct: HTTP 200 |
| 14 | [https://www.bing.com/search?q=maximum+weight+connected+subgraph+heuristic+BioNet+GMWCS+github](https://www.bing.com/search?q=maximum+weight+connected+subgraph+heuristic+BioNet+GMWCS+github) | bing_mwcs: HTTP 200 |
| 15 | [https://www.bing.com/search?q=%22Shaw%22+%221998%22+%22constraint%22+vehicle+pdf](https://www.bing.com/search?q=%22Shaw%22+%221998%22+%22constraint%22+vehicle+pdf) | bing_shaw: HTTP 200 |
| 16 | [https://www.bing.com/search?q=%22connected%22+%22reserve%22+%22budget%22+optimization](https://www.bing.com/search?q=%22connected%22+%22reserve%22+%22budget%22+optimization) | bing_reserve: HTTP 200 |
| 17 | [https://www.bing.com/search?q=%22Steiner%22+%22reoptimization%22+pdf](https://www.bing.com/search?q=%22Steiner%22+%22reoptimization%22+pdf) | bing_reopt: HTTP 200 |
| 18 | [https://www.bing.com/search?q=%22connected+submodular%22+maximization](https://www.bing.com/search?q=%22connected+submodular%22+maximization) | bing_submod: HTTP 200 |
| 19 | [https://www.bing.com/search?q=%22estimating%22+%22optimum%22+%22Weibull%22](https://www.bing.com/search?q=%22estimating%22+%22optimum%22+%22Weibull%22) | bing_evt: HTTP 200 |
| 20 | [https://arxiv.org/pdf/1412.2787](https://arxiv.org/pdf/1412.2787) | steiner_robust: HTTP 200 |
| 21 | [https://renatowerneck.wordpress.com/publications/](https://renatowerneck.wordpress.com/publications/) | werneck_pubs: HTTP 404 |
| 22 | [https://alns.readthedocs.io/en/latest/api/select.html](https://alns.readthedocs.io/en/latest/api/select.html) | alns_docs: HTTP 200 |
| 23 | [https://api.crossref.org/works?query.title=Steiner%20tree%20reoptimization&amp;rows=6](https://api.crossref.org/works?query.title=Steiner%20tree%20reoptimization&rows=6) | scholar_reopt: HTTP 200 |
| 24 | [https://api.crossref.org/works?query.title=Local%20search%20algorithms%20for%20the%20k-cardinality%20tree%20problem&amp;rows=3](https://api.crossref.org/works?query.title=Local%20search%20algorithms%20for%20the%20k-cardinality%20tree%20problem&rows=3) | scholar_kct: HTTP 200 |
| 25 | [https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+pdf&amp;udm=14&amp;gbv=1](https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+pdf&udm=14&gbv=1) | google_basic: HTTP 200; sparse/interstitial content possible |
| 26 | [https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+pdf&amp;gbv=1](https://www.google.com/search?q=k-cardinality+tree+variable+neighborhood+search+pdf&gbv=1) | google_basic redirect: HTTP 200; sparse/interstitial content possible |
| 27 | [https://api.crossref.org/works?query=Weibull%20estimating%20global%20optimum%20de%20Haan&amp;rows=4](https://api.crossref.org/works?query=Weibull%20estimating%20global%20optimum%20de%20Haan&rows=4) | scholar_evt: HTTP 200 |
| 28 | [https://github.com/fraenkel-lab/pcst_fast](https://github.com/fraenkel-lab/pcst_fast) | pcst_fast: HTTP 200 |
| 29 | [https://arxiv.org/pdf/2103.04206](https://arxiv.org/pdf/2103.04206) | lns_survey: HTTP 200 |
| 30 | [https://scipjack.zib.de/](https://scipjack.zib.de/) | scipjack: HTTP 200 |
| 31 | [https://renatowerneck.wordpress.com/](https://renatowerneck.wordpress.com/) | werneck_root: HTTP 200 |
| 32 | [https://www.google.com/goto?url=CAESZAHrOzAVBZov2vY3F2lbyeebDjbQbVFixnqo0NXilF81XqXMPjyy0qE5J0lXhNLAz6M9oPhypUogVA4zeu_YWv5eWDHKhcIMfwO82smjICRd6Nf-xtjKyBpMziQrt3wVI_Cszrc](https://www.google.com/goto?url=CAESZAHrOzAVBZov2vY3F2lbyeebDjbQbVFixnqo0NXilF81XqXMPjyy0qE5J0lXhNLAz6M9oPhypUogVA4zeu_YWv5eWDHKhcIMfwO82smjICRd6Nf-xtjKyBpMziQrt3wVI_Cszrc) | kct_core: HTTP 404 |
| 33 | [https://fileserver-az.core.ac.uk/download/pdf/82442393.pdf](https://fileserver-az.core.ac.uk/download/pdf/82442393.pdf) | kct_core redirect: HTTP 404 |
| 34 | [https://github.com/N-Wouda/ALNS](https://github.com/N-Wouda/ALNS) | alns_repo: HTTP 200 |
| 35 | [https://api.crossref.org/works?query.title=Approximating%20the%20Shapley%20Value%20Using%20Stratified%20Empirical%20Bernstein%20Sampling&amp;rows=2](https://api.crossref.org/works?query.title=Approximating%20the%20Shapley%20Value%20Using%20Stratified%20Empirical%20Bernstein%20Sampling&rows=2) | scholar_shapley: HTTP 200 |
| 36 | [https://www.google.com/goto?url=CAESgQEB6zswFdd5u8pbcNC6YC0p60w22tVqW9f4mYGp7Mn1cV1bQCvccZc3dteKMz4D8VkDJJRqQiGOmarfc95mY04uvVcFk5jxgihUrl6VV7JDFsRU6lM5D93_pPO4yX64xUAQMXRbjwt9NXqhe1YpeDE2srhyA6g2lu9TWb8-lAmJsUk](https://www.google.com/goto?url=CAESgQEB6zswFdd5u8pbcNC6YC0p60w22tVqW9f4mYGp7Mn1cV1bQCvccZc3dteKMz4D8VkDJJRqQiGOmarfc95mY04uvVcFk5jxgihUrl6VV7JDFsRU6lM5D93_pPO4yX64xUAQMXRbjwt9NXqhe1YpeDE2srhyA6g2lu9TWb8-lAmJsUk) | kct_ljubic: HTTP 200 |
| 37 | [https://ivanaljubic.github.io/docs/publications/kCardinalityTrees_JEA.pdf](https://ivanaljubic.github.io/docs/publications/kCardinalityTrees_JEA.pdf) | kct_ljubic redirect: HTTP 200 |
| 38 | [https://link.springer.com/article/10.1007/s00453-024-01243-2](https://link.springer.com/article/10.1007/s00453-024-01243-2) | reopt_2024: HTTP 200; sparse/interstitial content possible |
| 39 | [https://www.google.com/goto?url=CAESfAHrOzAVuqFtrh29HzTYBOorOh3HzKkfMOmLoJTC09ci1cRfdgkCTfag7t7h5Ec6sr8sqIg_6k5RQ7VaW5KtA8snSi9ZZv5s0XomT21Zs1d2fnG7tEZ1qb89IFyAT5PI5qCH221cAXO4a7HQh6WxfM03zARe655L_mclcMU](https://www.google.com/goto?url=CAESfAHrOzAVuqFtrh29HzTYBOorOh3HzKkfMOmLoJTC09ci1cRfdgkCTfag7t7h5Ec6sr8sqIg_6k5RQ7VaW5KtA8snSi9ZZv5s0XomT21Zs1d2fnG7tEZ1qb89IFyAT5PI5qCH221cAXO4a7HQh6WxfM03zARe655L_mclcMU) | rehfeldt_thesis: HTTP 200 |
| 40 | [https://opus4.kobv.de/opus4-zib/files/8514/dissertation_rehfeldt.pdf](https://opus4.kobv.de/opus4-zib/files/8514/dissertation_rehfeldt.pdf) | rehfeldt_thesis redirect: HTTP 200 |
| 41 | [https://arxiv.org/pdf/2211.00759](https://arxiv.org/pdf/2211.00759) | operator_rl: HTTP 200 |
| 42 | [https://arxiv.org/pdf/1804.10791](https://arxiv.org/pdf/1804.10791) | reopt_2018: HTTP 200 |
| 43 | [https://www.google.com/goto?url=CAESfgHrOzAVXZp6FvqMEkG3babvJDB0zWY4-R9lzbVSy_fcRviqJ8SZhQNOHHpEvfYGsLtcy4SF7IrqUBRT3SGekNGmzdXMLSj5kEmP79DYDk_aeyJN2OV0fXDBIR5abgJbmvU3uSof20IgngBlMtIDwoMbtZC1jDBRqDG7c0T1rA](https://www.google.com/goto?url=CAESfgHrOzAVXZp6FvqMEkG3babvJDB0zWY4-R9lzbVSy_fcRviqJ8SZhQNOHHpEvfYGsLtcy4SF7IrqUBRT3SGekNGmzdXMLSj5kEmP79DYDk_aeyJN2OV0fXDBIR5abgJbmvU3uSof20IgngBlMtIDwoMbtZC1jDBRqDG7c0T1rA) | alns_review: HTTP 200 |
| 44 | [https://edoc.ku.de/id/eprint/34084/1/1-s2.0-S0377221724003928-main.pdf](https://edoc.ku.de/id/eprint/34084/1/1-s2.0-S0377221724003928-main.pdf) | alns_review redirect: HTTP 200 |
| 45 | [https://www.google.com/goto?url=CAESfwHrOzAVikibO8QuIuqYakAK4jczA97MrQjwoIlmtVRvm68dZL74mq6kmDzOWqpZz7UYO5Rd5euurNMCtElLTfPfdW8FIMEygZ4NL4Akxpt3LXpwLZe6SsNPUEMi7xhIcOio_18ZiNx1VyhpnbvdzvEygac0R6-rNcrB5a2fEfY](https://www.google.com/goto?url=CAESfwHrOzAVikibO8QuIuqYakAK4jczA97MrQjwoIlmtVRvm68dZL74mq6kmDzOWqpZz7UYO5Rd5euurNMCtElLTfPfdW8FIMEygZ4NL4Akxpt3LXpwLZe6SsNPUEMi7xhIcOio_18ZiNx1VyhpnbvdzvEygac0R6-rNcrB5a2fEfY) | evt_2022: HTTP 403 |
| 46 | [https://www.sciencedirect.com/science/article/abs/pii/S2210650222001390](https://www.sciencedirect.com/science/article/abs/pii/S2210650222001390) | evt_2022 redirect: HTTP 403 |
| 47 | [https://github.com/scipopt/scip](https://github.com/scipopt/scip) | scip_github: HTTP 200 |
| 48 | [https://github.com/ls-cwi/heinz](https://github.com/ls-cwi/heinz) | heinz_github: HTTP 200 |
| 49 | [https://renatowerneck.wordpress.com/wp-content/uploads/2016/06/uw12-steiner-ls.pdf](https://renatowerneck.wordpress.com/wp-content/uploads/2016/06/uw12-steiner-ls.pdf) | steiner_fast: HTTP 200 |
| 50 | [https://www.google.com/goto?url=CAESfQHrOzAV_YCvFxq_NVyZRMxNWmZYTalM5y8XRIFE6BrYs2MFHrhAPuG4FuKqD2qGRYYZz5-NyhHjS2-6yiawaVA9BJ8D1T3skfRsuNMjNfPqh_EFwu7eP7vIRQfKfeuQwjzbpX6w3xqZLJr3ShkclR_1USqXLesZQuwwC2Wo](https://www.google.com/goto?url=CAESfQHrOzAV_YCvFxq_NVyZRMxNWmZYTalM5y8XRIFE6BrYs2MFHrhAPuG4FuKqD2qGRYYZz5-NyhHjS2-6yiawaVA9BJ8D1T3skfRsuNMjNfPqh_EFwu7eP7vIRQfKfeuQwjzbpX6w3xqZLJr3ShkclR_1USqXLesZQuwwC2Wo) | reserve: HTTP 200 |
| 51 | [https://www.cs.cornell.edu/gomes/pdf/2010_dilkina_cpaior_subgraph.pdf](https://www.cs.cornell.edu/gomes/pdf/2010_dilkina_cpaior_subgraph.pdf) | reserve redirect: HTTP 200 |
| 52 | [https://www.ijcai.org/proceedings/2021/0011.pdf](https://www.ijcai.org/proceedings/2021/0011.pdf) | shapley_2021: HTTP 200 |
| 53 | [https://people.csail.mit.edu/ludwigs/papers/dimacs14_fastpcst.pdf](https://people.csail.mit.edu/ludwigs/papers/dimacs14_fastpcst.pdf) | pcst_paper: HTTP 200 |
| 54 | [https://www.google.com/goto?url=CAESdgHrOzAVR1Q0xptPGc1nHwajxKKOaID1yyHaf6owl0vPgcc_3jKaqlbxa41XD5J5XTh2R-6UqIAfLYJ0hgWnCRxlXbmKdvbtV3yBXtwz0CGcF3AVWD7Uq6EJ3Qtemn33Mog2ruupU9gIwvx0BSjn46F1IAuZT-Q](https://www.google.com/goto?url=CAESdgHrOzAVR1Q0xptPGc1nHwajxKKOaID1yyHaf6owl0vPgcc_3jKaqlbxa41XD5J5XTh2R-6UqIAfLYJ0hgWnCRxlXbmKdvbtV3yBXtwz0CGcF3AVWD7Uq6EJ3Qtemn33Mog2ruupU9gIwvx0BSjn46F1IAuZT-Q) | routing_submod: HTTP 200 |
| 55 | [https://cdn.aaai.org/ojs/10066/10066-13-13594-1-2-20201228.pdf](https://cdn.aaai.org/ojs/10066/10066-13-13594-1-2-20201228.pdf) | routing_submod redirect: HTTP 200 |
| 56 | [https://cran.r-project.org/web/packages/mwcsr/index.html](https://cran.r-project.org/web/packages/mwcsr/index.html) | mwcsr: HTTP 200; sparse/interstitial content possible |
| 57 | [https://raw.githubusercontent.com/N-Wouda/ALNS/master/LICENSE](https://raw.githubusercontent.com/N-Wouda/ALNS/master/LICENSE) | alns_license: HTTP 404 |
| 58 | [https://www.google.com/goto?url=CAESWAHrOzAVsNnSK7ct3w-U0kvHdhbxYfX0gwddgXjNn-ujViEE0url8ahYfWS_BQ770LAuA2hk1W9kgSN-n-qgiu-A3uRtJ-2DKSE9dZICN8aXLdLMrT1dpEk](https://www.google.com/goto?url=CAESWAHrOzAVsNnSK7ct3w-U0kvHdhbxYfX0gwddgXjNn-ujViEE0url8ahYfWS_BQ770LAuA2hk1W9kgSN-n-qgiu-A3uRtJ-2DKSE9dZICN8aXLdLMrT1dpEk) | gmwcs_abs: HTTP 200 |
| 59 | [https://arxiv.org/abs/1605.02168](https://arxiv.org/abs/1605.02168) | gmwcs_abs redirect: HTTP 200 |
| 60 | [https://raw.githubusercontent.com/ls-cwi/heinz/master/LICENSE](https://raw.githubusercontent.com/ls-cwi/heinz/master/LICENSE) | heinz_license: HTTP 200 |
| 61 | [https://www.google.com/goto?url=CAESeQHrOzAVScXus5Wwe5q4Gq5Al-2KMm2UooIGr65XA37wtgQ3gTZPfw8b_F5np81W01_DBAiuoGbYpz09UwiD5WAFfZ9Yqim9M9j8KXXScZWgIvgLEoDVaQdju0_EjHy_VaGJw-HGRlO-F6uGKBGL-neY8fOxUc5V4ZA](https://www.google.com/goto?url=CAESeQHrOzAVScXus5Wwe5q4Gq5Al-2KMm2UooIGr65XA37wtgQ3gTZPfw8b_F5np81W01_DBAiuoGbYpz09UwiD5WAFfZ9Yqim9M9j8KXXScZWgIvgLEoDVaQdju0_EjHy_VaGJw-HGRlO-F6uGKBGL-neY8fOxUc5V4ZA) | mwcs_capacity: HTTP 200 |
| 62 | [https://openproceedings.org/2022/conf/inoc/INOC_2022_paper_19.pdf](https://openproceedings.org/2022/conf/inoc/INOC_2022_paper_19.pdf) | mwcs_capacity redirect: HTTP 200 |
| 63 | [https://api.crossref.org/works?query.title=Can%20the%20global%20optimum%20of%20a%20combinatorial%20optimization%20problem%20be%20reliably%20estimated%20through%20extreme%20value%20theory&amp;rows=1](https://api.crossref.org/works?query.title=Can%20the%20global%20optimum%20of%20a%20combinatorial%20optimization%20problem%20be%20reliably%20estimated%20through%20extreme%20value%20theory&rows=1) | evt_meta: HTTP 200 |
| 64 | [https://www.google.com/goto?url=CAEScwHrOzAV7YetgCnGmkBVtJp7-w0NsKXrKFuc-ZGbd3AZ_oklzrujQW6yso-81YOSUotE2ZLKW_FAOYWMg4LLPiZCoQJdqCpYiWD0Ut3ynexqTqSWSO_AyIzURuosrgGlnRB2UMJoorkbWmm97_Cznfq3F5A](https://www.google.com/goto?url=CAEScwHrOzAV7YetgCnGmkBVtJp7-w0NsKXrKFuc-ZGbd3AZ_oklzrujQW6yso-81YOSUotE2ZLKW_FAOYWMg4LLPiZCoQJdqCpYiWD0Ut3ynexqTqSWSO_AyIzURuosrgGlnRB2UMJoorkbWmm97_Cznfq3F5A) | cfl: HTTP 200 |
| 65 | [https://people.idsia.ch/~grandoni/Pubblicazioni/EGRS08soda.pdf](https://people.idsia.ch/~grandoni/Pubblicazioni/EGRS08soda.pdf) | cfl redirect: HTTP 200 |
| 66 | [https://www.google.com/goto?url=CAESbgHrOzAVxWC6O17b8-R7-OJsGpGj8zuic5fdSEh-mSttlRR9S4TKGtc6c_5sdPwJiucuzPMbPrI5jul_fdz79_69J4A0e8ZsSgFgmvAtE8PRHXIvolROLYulpejzUdrhlIWy-9pbm7CF_TwclNkg](https://www.google.com/goto?url=CAESbgHrOzAVxWC6O17b8-R7-OJsGpGj8zuic5fdSEh-mSttlRR9S4TKGtc6c_5sdPwJiucuzPMbPrI5jul_fdz79_69J4A0e8ZsSgFgmvAtE8PRHXIvolROLYulpejzUdrhlIWy-9pbm7CF_TwclNkg) | banzhaf: HTTP 200 |
| 67 | [https://proceedings.mlr.press/v206/wang23e/wang23e.pdf](https://proceedings.mlr.press/v206/wang23e/wang23e.pdf) | banzhaf redirect: HTTP 200 |
| 68 | [https://www.google.com/goto?url=CAESewHrOzAVEbxcM6d2HrrrTEAtUQL801DbwMc40jOeFfFRVqDn2Q4bNnmDk1jTAqFNw-Pgh46EI4RqdGjtZlo4I8wsqBzvREKBvuB7Jct9dzbK95zWrEKuAS-Y1n1bBmm6NKVxQhKrNef0m2OA-UhePEOM2RnDk9ENC0pO8Q](https://www.google.com/goto?url=CAESewHrOzAVEbxcM6d2HrrrTEAtUQL801DbwMc40jOeFfFRVqDn2Q4bNnmDk1jTAqFNw-Pgh46EI4RqdGjtZlo4I8wsqBzvREKBvuB7Jct9dzbK95zWrEKuAS-Y1n1bBmm6NKVxQhKrNef0m2OA-UhePEOM2RnDk9ENC0pO8Q) | blum_page: HTTP 200 |
| 69 | [https://kluedo.ub.rptu.de/frontdoor/index/index/year/2000/docId/519](https://kluedo.ub.rptu.de/frontdoor/index/index/year/2000/docId/519) | blum_page redirect: HTTP 200 |
| 70 | [https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.articulation_points.html) | networkx_articulation: HTTP 200 |
| 71 | [https://api.crossref.org/works/10.1016/j.ejor.2020.10.045](https://api.crossref.org/works/10.1016/j.ejor.2020.10.045) | alns_meta: HTTP 200 |
| 72 | [https://arxiv.org/pdf/1605.02168](https://arxiv.org/pdf/1605.02168) | gmwcs: HTTP 200 |
| 73 | [https://api.crossref.org/works?query.title=A%20stochastic%20method%20for%20estimating%20the%20minimum%20of%20a%20function&amp;rows=3](https://api.crossref.org/works?query.title=A%20stochastic%20method%20for%20estimating%20the%20minimum%20of%20a%20function&rows=3) | scholar_evt_original: HTTP 200 |
| 74 | [https://www.google.com/goto?url=CAES3wEB6zswFbXbrxleVctfRTTachS2HYGFthckuo23a-9JGTHr5yxaEGg31a6h994b2f1UqH0-SB9kITyv0u3Kg-SqEIgv2sAMoULl3jwROkqLKA4QADM1C1gvRIERqnY7_YSHIZn3aI1J0mNKweco65dk9R6YuruogvArUrPxv4L4Tnmn-0E4zLt3HRzJldU40UktTFkTTHWcUd9ghtq9IiY4e-xN-2HdxYP5GZBRjz7oG0RwHOtjU_PPUZdPr4U0iJ3yR0hCjbyj4Rri-yytvPSjugLzqPBpOwrPC0N-o23C](https://www.google.com/goto?url=CAES3wEB6zswFbXbrxleVctfRTTachS2HYGFthckuo23a-9JGTHr5yxaEGg31a6h994b2f1UqH0-SB9kITyv0u3Kg-SqEIgv2sAMoULl3jwROkqLKA4QADM1C1gvRIERqnY7_YSHIZn3aI1J0mNKweco65dk9R6YuruogvArUrPxv4L4Tnmn-0E4zLt3HRzJldU40UktTFkTTHWcUd9ghtq9IiY4e-xN-2HdxYP5GZBRjz7oG0RwHOtjU_PPUZdPr4U0iJ3yR0hCjbyj4Rri-yytvPSjugLzqPBpOwrPC0N-o23C) | ropke_backhaul: HTTP 200 |
| 75 | [https://backend.orbit.dtu.dk/ws/portalfiles/portal/3155117/A%20unified%20heuristic%20for%20a%20large%20class%20of%20Vehicle%20Routing%20Problems%20with%20Backhauls_TechRep_Ropke_Pisinger.pdf](https://backend.orbit.dtu.dk/ws/portalfiles/portal/3155117/A%20unified%20heuristic%20for%20a%20large%20class%20of%20Vehicle%20Routing%20Problems%20with%20Backhauls_TechRep_Ropke_Pisinger.pdf) | ropke_backhaul redirect: HTTP 200 |
| 76 | [https://www.google.com/goto?url=CAESbwHrOzAVLsC1qbphL07F9MSHaaxoSNYFaoqaEdFeQtTQdAOs4e7yFkn-ByltoFoI2zzENpl93A5TFOPer4hiV3VUfCIJmvRa2Yc62agDZcjwLJymO57dDOMJT-Ep1frvXvgh3Qws02-l766Op1TPoQ](https://www.google.com/goto?url=CAESbwHrOzAVLsC1qbphL07F9MSHaaxoSNYFaoqaEdFeQtTQdAOs4e7yFkn-ByltoFoI2zzENpl93A5TFOPer4hiV3VUfCIJmvRa2Yc62agDZcjwLJymO57dDOMJT-Ep1frvXvgh3Qws02-l766Op1TPoQ) | cmst: HTTP 200; sparse/interstitial content possible |
| 77 | [https://link.springer.com/article/10.1007/s101070100234](https://link.springer.com/article/10.1007/s101070100234) | cmst redirect: HTTP 200; sparse/interstitial content possible |
| 78 | [https://www.google.com/goto?url=CAESqAEB6zswFX5EbaZa_ThgbDxYtiINeYw-KKCQ09hPkHmpSisCwO9W2T4ozM3SF8n1XGrODEYcJJ35f4U7cgJIDYq4U-k4GQodkXKghtBDGtqkgiUwLeCfgNcTIWtXykukKyIgwtoaAeeem0uHmKptHXiAjaXekAun7BGC5jir6UbGe8DXzN01RCySGTdox5XlHdlFtl4RILM96fQF3RuljGOHDJWRUed4np4](https://www.google.com/goto?url=CAESqAEB6zswFX5EbaZa_ThgbDxYtiINeYw-KKCQ09hPkHmpSisCwO9W2T4ozM3SF8n1XGrODEYcJJ35f4U7cgJIDYq4U-k4GQodkXKghtBDGtqkgiUwLeCfgNcTIWtXykukKyIgwtoaAeeem0uHmKptHXiAjaXekAun7BGC5jir6UbGe8DXzN01RCySGTdox5XlHdlFtl4RILM96fQF3RuljGOHDJWRUed4np4) | hendel_page: HTTP 200 |
| 79 | [https://www.zib.de/userpage/hendel/publication/adaptive-large-neighborhood-search-for-mixed-integer-programming/](https://www.zib.de/userpage/hendel/publication/adaptive-large-neighborhood-search-for-mixed-integer-programming/) | hendel_page redirect: HTTP 200 |
| 80 | [https://github.com/scipopt/scipstp](https://github.com/scipopt/scipstp) | scipjack_repo: HTTP 404 |
| 81 | [https://github.com/ctlab/gmwcs-solver](https://github.com/ctlab/gmwcs-solver) | gmwcs_repo: HTTP 200 |
| 82 | [https://www.google.com/goto?url=CAESWAHrOzAVCVV1xULE0_Asmzq4s3HhXo5T7uMOf-m39o9SMOD0mE3yPWyuzLykTQiDtwKhDaoxCkYtHrxCo9AlbP_gQDos9jVhuOvYlWyYGcTXJXH8xZfiYKU](https://www.google.com/goto?url=CAESWAHrOzAVCVV1xULE0_Asmzq4s3HhXo5T7uMOf-m39o9SMOD0mE3yPWyuzLykTQiDtwKhDaoxCkYtHrxCo9AlbP_gQDos9jVhuOvYlWyYGcTXJXH8xZfiYKU) | incremental: HTTP 200 |
| 83 | [https://arxiv.org/pdf/2407.04447](https://arxiv.org/pdf/2407.04447) | incremental redirect: HTTP 200 |
| 84 | [https://www.google.com/goto?url=CAEScAHrOzAVdXtduiibnWFyOg2bVJO-CU1hrKrtQ8FxCLfAG7FrExlXbM5hYuOIRrFJdCJVH8pLNX1kgnkLEQipyyHESCIyWdhKynE8gjY-0P4LKxIVLccn5tu_TX_qfDKaAU5YRt3bdPoO1_Ws5iohbqE](https://www.google.com/goto?url=CAEScAHrOzAVdXtduiibnWFyOg2bVJO-CU1hrKrtQ8FxCLfAG7FrExlXbM5hYuOIRrFJdCJVH8pLNX1kgnkLEQipyyHESCIyWdhKynE8gjY-0P4LKxIVLccn5tu_TX_qfDKaAU5YRt3bdPoO1_Ws5iohbqE) | ilp_lns: HTTP 200 |
| 85 | [https://proceedings.mlr.press/v202/huang23g/huang23g.pdf](https://proceedings.mlr.press/v202/huang23g/huang23g.pdf) | ilp_lns redirect: HTTP 200 |
| 86 | [https://api.github.com/repos/ctlab/gmwcs-solver/git/trees/master?recursive=1](https://api.github.com/repos/ctlab/gmwcs-solver/git/trees/master?recursive=1) | gmwcs_tree: HTTP 200 |
| 87 | [https://raw.githubusercontent.com/N-Wouda/ALNS/master/LICENSE.md](https://raw.githubusercontent.com/N-Wouda/ALNS/master/LICENSE.md) | alns_license_actual: HTTP 200 |
| 88 | [https://raw.githubusercontent.com/ctlab/gmwcs-solver/master/LICENSE](https://raw.githubusercontent.com/ctlab/gmwcs-solver/master/LICENSE) | gmwcs_license: HTTP 200 |
| 89 | [https://api.github.com/repos/fraenkel-lab/pcst_fast/git/trees/master?recursive=1](https://api.github.com/repos/fraenkel-lab/pcst_fast/git/trees/master?recursive=1) | pcst_tree: HTTP 200 |
| 90 | [https://api.crossref.org/works/10.1007/s101070100234](https://api.crossref.org/works/10.1007/s101070100234) | cmst_meta: HTTP 200 |
| 91 | [https://api.github.com/repos/ls-cwi/heinz/git/trees/master?recursive=1](https://api.github.com/repos/ls-cwi/heinz/git/trees/master?recursive=1) | heinz_tree: HTTP 200 |
| 92 | [https://optimization-online.org/2018/12/6992/](https://optimization-online.org/2018/12/6992/) | hendel_opt_page: HTTP 200 |
| 93 | [https://kluedo.ub.rptu.de/files/519/gelb_48.pdf](https://kluedo.ub.rptu.de/files/519/gelb_48.pdf) | blum: HTTP 200 |
| 94 | [https://kluedo.ub.rptu.de/frontdoor/deliver/index/docId/519/file/gelb_48.pdf](https://kluedo.ub.rptu.de/frontdoor/deliver/index/docId/519/file/gelb_48.pdf) | blum redirect: HTTP 200 |
| 95 | [https://arxiv.org/abs/2211.00759](https://arxiv.org/abs/2211.00759) | operator_rl_abs: HTTP 200 |
| 96 | [https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/impl/treeheuristicsolverimpl.h](https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/impl/treeheuristicsolverimpl.h) | heinz_heuristic: HTTP 200 |
| 97 | [https://raw.githubusercontent.com/ctlab/gmwcs-solver/5b030be7e55a9db424de4a0ff7cc25af18a64bc8/src/main/java/ru/ifmo/ctddev/gmwcs/graph/Blocks.java](https://raw.githubusercontent.com/ctlab/gmwcs-solver/5b030be7e55a9db424de4a0ff7cc25af18a64bc8/src/main/java/ru/ifmo/ctddev/gmwcs/graph/Blocks.java) | gmwcs_blocks: HTTP 200 |
| 98 | [https://raw.githubusercontent.com/ctlab/gmwcs-solver/5b030be7e55a9db424de4a0ff7cc25af18a64bc8/src/main/java/ru/ifmo/ctddev/gmwcs/solver/RootedSolver.java](https://raw.githubusercontent.com/ctlab/gmwcs-solver/5b030be7e55a9db424de4a0ff7cc25af18a64bc8/src/main/java/ru/ifmo/ctddev/gmwcs/solver/RootedSolver.java) | gmwcs_heuristic: HTTP 200; sparse/interstitial content possible |
| 99 | [https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/LICENSE.txt](https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/LICENSE.txt) | pcst_license: HTTP 200 |
| 100 | [https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/src/pcst_fast.cc](https://raw.githubusercontent.com/fraenkel-lab/pcst_fast/25ab31a245b2278848b5a8814924cdb3039b4279/src/pcst_fast.cc) | pcst_code: HTTP 200 |
| 101 | [https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/blockcuttree.h](https://raw.githubusercontent.com/ls-cwi/heinz/ebd0a046bb559f8ace2a0edaf7c6bd36bbd522aa/src/solver/blockcuttree.h) | heinz_blocks: HTTP 200 |
| 102 | [https://optimization-online.org/wp-content/uploads/2018/12/6992.pdf](https://optimization-online.org/wp-content/uploads/2018/12/6992.pdf) | hendel: HTTP 200 |
| 103 | [https://www.researchgate.net/publication/363041653_Can_the_Global_Optimum_of_a_Combinatorial_Optimization_Problem_be_Reliably_Estimated_Through_Extreme_Value_Theory](https://www.researchgate.net/publication/363041653_Can_the_Global_Optimum_of_a_Combinatorial_Optimization_Problem_be_Reliably_Estimated_Through_Extreme_Value_Theory) | evt_abstract, S23: HTTP 403; web: abstract opened; full paper unavailable |
| 104 | [https://hal.science/hal-01543503/document](https://hal.science/hal-01543503/document) | critical, critical destroy original: HTTP 200; web: fetch failed; direct access returned challenge page |
| 105 | [https://arxiv.org/pdf/2605.30053](https://arxiv.org/pdf/2605.30053) | submod_2026, S14: HTTP 200; web: full PDF opened |
| 106 | [https://citeseerx.ist.psu.edu/document?doi=573f915656b828d6c0bb4beb2c867cce624c1779&amp;repid=rep1&amp;type=pdf](https://citeseerx.ist.psu.edu/document?doi=573f915656b828d6c0bb4beb2c867cce624c1779&repid=rep1&type=pdf) | cmst_open, CMST mirror: request failed; web: fetch failed; author manuscript opened elsewhere |
| 107 | [https://du.diva-portal.org/smash/get/diva2%3A791806/FULLTEXT01.pdf](https://du.diva-portal.org/smash/get/diva2%3A791806/FULLTEXT01.pdf) | evt_bounds, S24: HTTP 200; web: failed; direct institutional PDF successfully read |
| 108 | [https://raw.githubusercontent.com/networkx/networkx/main/LICENSE.txt](https://raw.githubusercontent.com/networkx/networkx/main/LICENSE.txt) | networkx_license: HTTP 200 |
| 109 | [https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/AlphaUCB.py](https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/AlphaUCB.py) | alns_ucb_code: HTTP 200 |
| 110 | [https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/SegmentedRouletteWheel.py](https://raw.githubusercontent.com/N-Wouda/ALNS/master/alns/select/SegmentedRouletteWheel.py) | alns_segment_code: HTTP 200 |
| 111 | [https://arxiv.org/abs/2605.30053](https://arxiv.org/abs/2605.30053) | S14 abstract: web: opened |
| 112 | [https://www.researchgate.net/publication/2384064_Multi-Exchange_Neighborhood_Structures_for_the_Capacitated_Minimum_Spanning_Tree_Problem](https://www.researchgate.net/publication/2384064_Multi-Exchange_Neighborhood_Structures_for_the_Capacitated_Minimum_Spanning_Tree_Problem) | S19: web: author-uploaded full text opened |
| 113 | [https://www.researchgate.net/publication/2384064_Multi-exchange_neighborhood_structures_for_the_capacitated_minimum_spanning_tree_problem](https://www.researchgate.net/publication/2384064_Multi-exchange_neighborhood_structures_for_the_capacitated_minimum_spanning_tree_problem) | S19 redirect: web: author-uploaded full text opened |
| 114 | [https://www.researchgate.net/publication/267025927_On_statistical_bounds_of_heuristic_solutions_to_location_problems](https://www.researchgate.net/publication/267025927_On_statistical_bounds_of_heuristic_solutions_to_location_problems) | S22: web: author-uploaded manuscript and abstract opened |
| 115 | [https://www.sciencedirect.com/science/article/pii/S0305054817301508](https://www.sciencedirect.com/science/article/pii/S0305054817301508) | critical destroy original: web: full-page fetch failed; abstract/search discovery only |
| 116 | [https://ucrisportal.univie.ac.at/en/publications/obtaining-optimal-k-cardinality-trees-fast/](https://ucrisportal.univie.ac.at/en/publications/obtaining-optimal-k-cardinality-trees-fast/) | S2 metadata: web: institutional record opened |
| 117 | [https://citeseerx.ist.psu.edu/document?doi=9a4d69b0b44d06e2f38bb6086618f16263871d4f&amp;repid=rep1&amp;type=pdf](https://citeseerx.ist.psu.edu/document?doi=9a4d69b0b44d06e2f38bb6086618f16263871d4f&repid=rep1&type=pdf) | Shaw CP98 original: web: timeout |
| 118 | [https://www.researchgate.net/publication/2914450_Apes_Report_Apes-01-1998](https://www.researchgate.net/publication/2914450_Apes_Report_Apes-01-1998) | S5: web: author-uploaded full text opened |
| 119 | [https://freuder.me/wp-content/uploads/2019/09/shaw_cp98.pdf](https://freuder.me/wp-content/uploads/2019/09/shaw_cp98.pdf) | Shaw 2019 retrospective: web: four-page author commentary opened; not original CP98 paper |
| 120 | [https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/biconnected.html](https://networkx.org/documentation/stable/_modules/networkx/algorithms/components/biconnected.html) | C5: web: official source documentation opened |
| 121 | [https://proceedings.mlr.press/v206/wang23e.html](https://proceedings.mlr.press/v206/wang23e.html) | S9 metadata: web: official record opened |
| 122 | [https://proceedings.mlr.press/v202/huang23g.html](https://proceedings.mlr.press/v202/huang23g.html) | S21 metadata: web: official record opened |
| 123 | [https://ojs.aaai.org/index.php/ICAPS/article/view/31507](https://ojs.aaai.org/index.php/ICAPS/article/view/31507) | S20 metadata: web: official record opened |
