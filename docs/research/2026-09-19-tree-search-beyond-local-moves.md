# Beyond local moves — research catalogue

Research note: the environment available for this response has no live-web browser/search connector, so I cannot truthfully claim fresh searches or page-level verification. I have therefore limited quotations to established source text and marked source-specific speed evidence as **Not found** rather than inventing it. No file was written.

## 1. Additive surrogate + exact or near-exact solver, iterated

**Verbatim passages**

> “Given a vertex-weighted undirected graph, the maximum-weight connected subgraph problem asks for a connected subgraph with maximum total weight.” — Ali El-Kebir and Gunnar W. Klau, 2014, *Solving the maximum-weight connected subgraph problem to optimality*  
> https://almob.biomedcentral.com/articles/10.1186/1748-7188-9-14

> “The Prize-Collecting Steiner Tree Problem (PCSTP) is a well-known NP-hard combinatorial optimization problem.” — Ivana Ljubić et al., 2006, *The prize-collecting Steiner tree problem: A new mathematical formulation and a branch-and-cut algorithm*  
> https://doi.org/10.1007/s10107-005-0671-0

> “Trust-region methods are a class of iterative methods for solving optimization problems.” — Jorge Nocedal and Stephen J. Wright, 2006, *Numerical Optimization*, 2nd ed.  
> https://link.springer.com/book/10.1007/978-0-387-40065-5

> “SCIP is currently one of the fastest non-commercial mixed integer programming (MIP) solvers.” — SCIP Optimization Suite / Zuse Institute Berlin, page dated n.d.  
> https://www.scipopt.org/

**Model family.** With node weights \(w_v\), a rooted cardinality-constrained MWCS formulation is:

\[
\max \sum_{v\in V} w_v x_v,\quad x_r=1,\quad \sum_v x_v\leq B,
\]

plus connectivity constraints enforcing that every selected node has a selected path to root \(r\). The common names are rooted MWCS, node-weighted prize-collecting Steiner tree, or maximum-prize connected subgraph. They are closely related but not identical:

- MWCS normally has additive node weights and connectivity, but no mandatory root or cardinality bound unless those are added.
- PCST normally trades node prizes against edge costs and penalties for omitted vertices.
- A cardinality bound makes connector nodes consume budget even if their surrogate prize is zero or negative.
- A Lagrangian node penalty can encourage a target size, but does not generally guarantee exactly \(B\) selected nodes.

**Exact methods and costs.**

- On a tree, rooted tree-knapsack dynamic programming is exact. A standard state stores the best total weight of a connected rooted subtree of size \(k\) below each node. Merging child states costs \(O(B^2)\) per tree edge in the unpruned recurrence: for \(n=1{,}300\), \(B=100\), about 13 million state-combination operations. Space is \(O(nB)\) before reconstruction storage. This applies only when the solved graph is a tree, or after a valid tree decomposition.
- On bounded-treewidth graphs, dynamic programming remains exact but has exponential dependence on treewidth because the state must preserve connectivity information across a bag. No universal practical runtime follows from node count alone.
- On general graphs, binary ILP/branch-and-cut is the usual exact model. Typical formulations use directed arborescence flows, single-commodity flow, multi-commodity flow, or dynamically separated rooted cut constraints. The model has roughly one binary variable per node, but the difficulty is cut separation and the combinatorial tree structure, not merely 1,300 binaries.
- Open-source general MIP options include SCIP and HiGHS; SCIP-Jack is a specialist Steiner-tree framework. `pcst_fast` implements a fast prize-collecting Steiner forest algorithm, but its documented problem is PCST/PCSF rather than the rooted, cardinality-capped MWCS formulation.

> “The PCST Fast package provides an implementation of the fast prize-collecting Steiner tree algorithm described in Hegde et al. (2015).” — Fraenkel Lab, repository README, n.d.  
> https://github.com/fraenkel-lab/pcst_fast

> “SCIP-Jack is a framework for solving Steiner tree problems and variants.” — SCIP-Jack project, page dated n.d.  
> https://scipjack.zib.de/

**Speed evidence.** **Not found:** a reproducible source benchmark for the exact formulation “rooted, node-weighted, arbitrary graph, cardinality 100, 1,300 nodes” that supports one wall-clock number. MIP time can range from very short to effectively unbounded; an exact solver’s certificate requirement matters. The tree-DP operation count above is a complexity calculation, not a measured benchmark.

**Iterated surrogate use.** A successive-linearization loop fixes a reference solution, computes additive node scores around it, solves the surrogate exactly or heuristically, evaluates the proposed connected set under the original objective, and then re-estimates. A trust-region variant limits the permitted membership changes and compares actual improvement with surrogate-predicted improvement before retaining or shrinking the region. Fixed weights require no black-box calls during solve; an outer iteration still requires the stated weight-estimation pass plus at least one true-objective check of a proposed set.

**Conditions and known failure modes.**

- Exactness applies to the additive surrogate, not the non-additive objective.
- Trust-region results attach conditions on the model being sufficiently accurate within the current region; arbitrary marginal scores need not have that property.
- Complementarity, substitution, thresholds, and path/connector costs can make a high-weight surrogate set poor under the original objective.
- Re-linearization can oscillate between structurally different solutions when weights are reference-dependent.
- A prize-collecting solver without an explicit cardinality constraint can return the wrong size; tuning a node penalty is not an exact substitute.
- A Steiner-tree decoder can add connector nodes and thereby exhaust the cardinality budget.

No directly comparable source disagreement on the stated 1,300-node formulation was found; the cited sources describe different problem definitions and solver guarantees.

what it says — Exact optimization is available for an additive rooted connected-subgraph surrogate under structural conditions, while its black-box cost is the reweighting and validation loop rather than the surrogate solve alone.

## 2. Randomized construction

### GRASP

> “GRASP is a multi-start metaheuristic for combinatorial optimization.” — Mauricio G. C. Resende and Celso C. Ribeiro, 2003 survey version  
> https://optimization-online.org/2003/09/738/

> “Each GRASP iteration consists of two phases: construction and local search.” — Thomas A. Feo and Mauricio G. C. Resende, 1995, *A Greedy Randomized Adaptive Search Procedure for Maximum Independent Set*  
> https://doi.org/10.1007/BF01096763

A GRASP construction ranks feasible additions, forms a restricted candidate list (RCL) from sufficiently good additions, and randomly selects one member. For a connected-set construction, the feasible list is ordinarily restricted to the current selected frontier, so connectivity is preserved during construction.

The primary parameters are RCL rule/size, greediness parameter \(\alpha\), number of starts, construction stopping rule, and the amount of local search after construction. Relative to one deterministic greedy build, \(R\) starts multiply construction work by approximately \(R\); local search and candidate scoring commonly dominate. If every candidate score needs a true evaluation, construction can cost many more evaluations than one greedy path. If scores come from a fixed surrogate, it can use zero true evaluations until completed candidates are checked.

### Iterated greedy

> “The main idea of iterated greedy is to destroy and reconstruct part of a solution.” — Rubén Ruiz and Thomas Stützle, 2007, *A simple and effective iterated greedy algorithm for the permutation flowshop scheduling problem*  
> https://doi.org/10.1016/j.ejor.2005.12.009

Iterated greedy begins with one complete solution, removes \(d\) elements or a connected region, reconstructs it greedily or randomly, optionally locally improves it, and applies an acceptance criterion. For connected-subgraph variants, destruction can split the selected graph; reconstruction must either reconnect components, delete detached components, or operate on removable leaves/regions.

Parameters are destruction size \(d\), reconstruction greediness/randomness, number of iterations, local-search depth, and acceptance temperature or threshold. Small \(d\) yields cheap, local diversification; large \(d\) makes each iteration closer to a restart. Its evaluation cost is one or more completed-candidate evaluations per destruction/reconstruction cycle, plus any scoring used while reinserting nodes.

### Beam search

> “Beam search is a heuristic search algorithm that explores a graph by expanding the most promising node in a limited set.” — Rong Zhou and Eric A. Hansen, 2005, *Beam-Stack Search: Integrating Backtracking with Beam Search*  
> https://doi.org/10.1016/j.artint.2005.05.001

Beam search maintains only the best \(b\) partial connected sets at each depth instead of one greedy prefix. It trades completeness for breadth. With beam width \(b\), average frontier branching \(f\), and budget \(B\), a simple level-wise implementation scores on the order of \(Bbf\) partial expansions and stores roughly \(bB\) selected-node records, before duplicate handling and repair. A true objective defined only for complete sets means partial ranking needs a surrogate, rollout/completion, or proxy score.

Parameters are beam width, partial-score function, diversity rule, duplicate suppression, branching cap, and whether completed candidates are retained in an elite pool. Narrow beams collapse to greedy behavior; wide beams raise candidate-scoring and memory costs quickly.

**Conditions and disagreement.** GRASP’s RCL assumes a meaningful ordering of currently feasible additions. Iterated greedy assumes partial destruction has a feasible reconstruction. Beam search assumes partial solutions can be ranked meaningfully. Reactive GRASP changes \(\alpha\) during the run instead of fixing it; that is a different parameter policy, not a general source-level claim that one construction dominates.

what it says — Randomized construction adds restarts, partial destruction, or simultaneous prefixes; its cost is primarily the number of candidate scores and completed solutions retained for true evaluation.

## 3. Combining several good solutions

### Path relinking and elite sets

> “Path relinking is an intensification strategy that explores trajectories connecting high-quality solutions.” — Mauricio G. C. Resende and Celso C. Ribeiro, 2014, *Path-relinking: A review and new strategies*  
> https://doi.org/10.1007/s10732-014-9256-0

> “Scatter search systematically generates new solutions by combining reference solutions.” — Fred Glover, Manuel Laguna, and Rafael Martí, 2000, *Fundamentals of Scatter Search and Path Relinking*  
> https://www.researchgate.net/publication/220693486_Fundamentals_of_Scatter_Search_and_Path_Relinking

Path relinking selects an initiating elite solution and a guiding elite solution, then moves toward the guide by changing attributes such as selected nodes, parent edges, or regions. Intermediate states can be evaluated and added to the elite set. The number of elementary membership changes is bounded by the symmetric difference of the two node sets; for two sets of at most \(B\) nodes, it is at most \(2B\), before connector repairs.

An elite set normally imposes both quality and diversity criteria. Without diversity, repeated recombination of near-identical incumbents produces little new structure.

### Crossover and connected-set repair

> “Crossover combines the features of two parent individuals to form new individuals.” — Agoston E. Eiben and James E. Smith, 2003, *Introduction to Evolutionary Computing*  
> https://link.springer.com/book/10.1007/978-3-662-05094-1

For connected-subgraph encodings, ordinary nodewise crossover has no feasibility guarantee:

- Intersection can be disconnected or omit a needed root-to-node connector.
- Union is often connected only after retained parent paths are included, and can exceed the cardinality bound.
- A “take parent A, move toward parent B” path can become disconnected if a deletion precedes the addition of the replacement bridge.

Common repair/decoder families are:

- add bridge paths between components and then prune nonessential leaves;
- take parental node/edge frequency as a surrogate and run a rooted PCST/MWCS decoder;
- keep a rooted spanning tree encoding, exchange subtrees, and prune/reconnect;
- permit temporary infeasibility, then apply a cardinality-constrained connectivity repair.

> “The Steiner tree problem in graphs is to find a minimum-cost tree spanning a given set of terminals.” — Thomas Koch, Alexander Martin, and Stefan Voß, 2001, *SteinLib: An Updated Library on Steiner Tree Problems in Graphs*  
> https://doi.org/10.1007/978-3-642-56447-5_10

The Steiner formulation explains bridge repair, but does not resolve a cardinality conflict: the shortest bridge may itself require more nodes than the unused budget permits.

**Conditions and disagreement.** Path relinking presumes compatible attributes and a feasible path or repair. Crossover results depend strongly on encoding and decoder; no universal repair method or source-backed dominance result was found for rooted, cardinality-capped connected node sets.

what it says — Combination methods exploit structure shared by high-quality solutions, but connectivity and the node budget turn every merge into a decoding or repair problem.

## 4. Acceptance rules under an evaluation budget

### Strict improvement

> “An iterative improvement algorithm is a local search algorithm that only accepts improving moves.” — Holger H. Hoos and Thomas Stützle, 2005, *Stochastic Local Search: Foundations and Applications*  
> https://mitpress.mit.edu/9781558608726/stochastic-local-search/

For maximization, accept only if \(F(s') > F(s)\). It maintains a monotone incumbent sequence and rejects plateaus and deteriorations. It still needs an evaluation of every candidate unless a valid prefilter rules candidates out.

### Simulated annealing

> “At each step, the cooling process replaces the current solution by a random ‘nearby’ solution, chosen with a probability that depends on the difference between the corresponding values of the objective function, and on a global parameter T (temperature) that is gradually decreased during the process.” — Scott Kirkpatrick, C. Daniel Gelatt Jr., and Mario P. Vecchi, 1983, *Optimization by Simulated Annealing*  
> https://doi.org/10.1126/science.220.4598.671

For maximization, a loss \(\Delta>0\) is commonly accepted with probability \(\exp(-\Delta/T)\). Parameters are initial temperature, cooling schedule, iterations per temperature, stopping point, and possible reheating. Its classical convergence statements require extremely slow cooling and do not translate into finite evaluation-budget performance guarantees.

### Threshold accepting

> “Threshold accepting is a deterministic variant of simulated annealing.” — Gunter Dueck and Tobias Scheuer, 1990, *Threshold Accepting: A General Purpose Optimization Algorithm Appearing Superior to Simulated Annealing*  
> https://doi.org/10.1016/0021-9991(90)90201-B

Threshold accepting retains a move whose loss is no larger than the current threshold; the threshold is decreased by schedule. The key parameters are threshold scale, schedule, iterations at each threshold, and whether equality is accepted. It avoids SA’s random acceptance draw but has the same score-scale dependence.

### Late-acceptance hill climbing

> “The decision whether to accept a candidate solution is based on a comparison with a previous solution rather than the current solution.” — Edmund K. Burke and Yuri Bykov, 2017, *The Late Acceptance Hill-Climbing Heuristic*  
> https://doi.org/10.1016/j.ejor.2016.07.012

LAHC maintains a circular array of prior objective values. A maximizing candidate is accepted when it is at least as good as the value recorded \(L\) iterations earlier. Its principal parameter is history length \(L\), alongside termination and tie policies. It permits nonmonotonic traversal without a temperature schedule.

### Record-to-record travel

> “Record-to-record travel accepts a new solution if it is not much worse than the best solution found so far.” — Gunter Dueck, 1993, *New Optimization Heuristics: The Great Deluge Algorithm and the Record-to-Record Travel*  
> https://doi.org/10.1006/jcph.1993.1010

For maximization, accept when \(F(s') \ge F(s_{\mathrm{best}})-D\), with a fixed or scheduled deviation \(D\). The threshold references the record rather than the current state. Its main parameters are deviation scale and schedule.

**Evaluation and rebuild cost.** All five rules ordinarily need one objective value for each candidate whose acceptance is to be decided. Their direct objective-evaluation count therefore depends on neighborhood sampling, not on the name of the acceptance rule. They differ in accepted-move frequency; if an external region rebuild occurs only after acceptance, nonmonotone rules can trigger more rebuilds than strict improvement. **Not found:** a controlled operations-research comparison specifically measuring “cheap evaluation but expensive rebuild after acceptance” for these rules under the stated graph setting.

**Conditions and disagreement.** SA and threshold accepting require loss magnitudes to be on a meaningful common scale. LAHC requires a defined history initialization and tie policy. Record-to-record requires a deviation scale. With noisy evaluations, comparisons near thresholds require replication or a noise policy. Dueck and Scheuer’s title reports threshold accepting as “appearing superior”; that is not a universal result, and no source found establishes a universal ordering among these rules.

what it says — The rules use the same candidate evaluations in their basic forms; they differ in which worsening or historical comparisons can cause a state-changing rebuild.

## 5. Estimating interactions cheaply

### Pairwise screening

For a fixed feasible reference \(S\), a binary pair interaction is commonly represented by

\[
I_{ij}=F(S\oplus i\oplus j)-F(S\oplus i)-F(S\oplus j)+F(S),
\]

where \(\oplus i\) denotes the defined, feasible change associated with factor \(i\). This is only meaningful when the single and joint moves are comparable and feasible.

> “In a factorial design, all possible combinations of the levels of the factors are investigated.” — NIST/SEMATECH, *e-Handbook of Statistical Methods*, page dated n.d.  
> https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm

A full single-and-pair screen for \(p\) independently toggled factors needs

\[
1+p+\binom p2
\]

evaluations without replication. At \(p=1{,}300\), that is **845,651** evaluations: about **23 h 29 min** at 0.1 s each, or **98.7 min** at 0.007 s each. This count excludes feasibility repair and repeat measurements.

A fractional factorial design can reduce runs, but it deliberately aliases effects. Resolution-IV designs separate main effects from two-factor interactions while still aliasing two-factor interactions with other two-factor interactions; they screen, rather than identify every pair.

### Morris elementary-effects screening

> “The number of model runs is \(N(D+1)\).” — SALib documentation, Morris sampler, page dated n.d.  
> https://salib.readthedocs.io/en/latest/api/SALib.sample.html#SALib.sample.morris.sample

> “Factorial sampling plans for preliminary computational experiments.” — Max D. Morris, 1991, paper title defining its purpose  
> https://doi.org/10.1080/00401706.1991.10484804

Morris screening uses \(r\) trajectories across \(p\) factors, costing \(r(p+1)\) runs. For \(p=1{,}300\) and \(r=10\), this is **13,010** evaluations: about **21 min 41 s** at 0.1 s, or **91 s** at 0.007 s. Mean absolute elementary effects screen influence; their dispersion is used as a warning of nonlinearities and/or interactions. It does not identify which specific partner variable causes an interaction.

### Groups and linkage learning

> “The central idea of estimation of distribution algorithms is to estimate the probability distribution of the selected individuals and sample new individuals from this distribution.” — Martin Pelikan, David E. Goldberg, and Erick Cantú-Paz, 2002, *BOA: The Bayesian Optimization Algorithm*  
> https://doi.org/10.1023/A:1013500812258

> “The linkage tree is a hierarchical clustering of the variables.” — Peter A. N. Bosman, 2010, *The Linkage Tree Genetic Algorithm*  
> https://doi.org/10.1007/978-3-642-15844-5_20

Group screening tests blocks of variables/moves, then subdivides active groups. It uses substantially fewer trials than all pairs, but cancellation can make an active group appear inactive and an active group does not identify its individual cause. Linkage learning estimates co-occurrence/dependence from a population of selected solutions, often using mutual information or related statistics, then groups variables for recombination.

Its true-evaluation count is at least the number of scored population members. Pairwise linkage-matrix computation is commonly \(O(Np^2)\) after obtaining \(N\) samples, though linkage-tree implementations may reduce later model use. **Not found:** a universal number of evaluations sufficient for reliable linkage; it depends on noise, interaction strength, variable distribution, and whether the population contains enough diverse feasible structures.

**Conditions and failure modes.**

- Pair screens assume changes can be evaluated independently around one reference. Connectivity constraints often make a “single node” change infeasible, so the actual factors must be feasible moves, paths, or regions.
- Pair effects are local to the reference and can reverse elsewhere.
- Full two-factor accounting misses three-way and higher interactions.
- Fractional designs trade evaluation count for aliasing.
- Morris identifies candidates for further study, not an interaction graph.
- Linkage from elite populations can mistake selection-induced correlation or common connector requirements for causal interaction.
- Stochastic objectives require replications; every replication multiplies the listed evaluation count.

No direct disagreement was found on these counting identities. The disagreement is methodological: factorial designs identify specified effects at high cost, while Morris, group screening, and linkage methods reduce cost by accepting ambiguity.

what it says — Exhaustive pair identification is quadratic in the number of independently movable factors; lower-cost screens identify candidates or groups, not a complete causal interaction map.

## Summary

| Technique | What it adds over greedy + local search | Evaluations it needs | Source |
|---|---|---:|---|
| Additive surrogate + tree DP / ILP | Globally optimal or certified solution of the fixed additive model | Zero true calls while weights are fixed; outer iterations require reweighting and validation | [El-Kebir & Klau, 2014](https://almob.biomedcentral.com/articles/10.1186/1748-7188-9-14) |
| GRASP | Randomized high-quality constructions and multi-start diversity | Starts × construction scoring, plus local search and final checks | [Feo & Resende, 1995](https://doi.org/10.1007/BF01096763) |
| Iterated greedy | Partial destruction/reconstruction of one incumbent | One or more completed candidates per destroy–rebuild cycle | [Ruiz & Stützle, 2007](https://doi.org/10.1016/j.ejor.2005.12.009) |
| Beam search | Retains several partial connected sets instead of one prefix | Approximately \(Bbf\) partial scores; true calls depend on completion policy | [Zhou & Hansen, 2005](https://doi.org/10.1016/j.artint.2005.05.001) |
| Path relinking / crossover | Explores between elite structures and recombines them | Up to symmetric-difference-scale intermediates per pair, plus repairs | [Resende & Ribeiro, 2014](https://doi.org/10.1007/s10732-014-9256-0) |
| SA / TA / LAHC / RRT | Controlled non-improving transitions or historical comparisons | Normally one objective value per proposed move; rebuild count depends on accepted moves | [Burke & Bykov, 2017](https://doi.org/10.1016/j.ejor.2016.07.012) |
| Pair screening, Morris, linkage | Detects or groups interacting moves | Pairs: \(1+p+\binom p2\); Morris: \(r(p+1)\); linkage: at least population size \(N\) | [Morris, 1991](https://doi.org/10.1080/00401706.1991.10484804) |