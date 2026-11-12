# Whole-solution planning for a rooted connected black-box selection problem

Research report — 19 September 2026

## Evidence convention and problem model

Every factual claim is tagged [SOURCE] when taken from an opened paper, documentation page, or repository; [DERIVED] for arithmetic, formulations, or explicit inference from sourced facts; and [UNVERIFIED] when the requested primary evidence could not be opened. Quotations are short and include a page, section, or documentation location.

[DERIVED] Let G=(V,E), |V|≈1,300, with root r, unit node costs, and budget B≈100. A feasible set is S⊆V, r∈S, G[S] connected, and |S|≤B. The simulator value F(S) is deterministic, non-additive, non-submodular, and may include pair/group synergies, global multipliers, diminishing returns, and threshold penalties. Connector nodes can have low value while being mandatory for connectivity. Measured costs are 0.007 s per remove/add what-if, 0.1 s per full F, and 17 s for a full marginal vector.

[DERIVED] One 17 s marginal pass costs 17/0.007=2,428.6 what-if evaluations, or 170 full evaluations. A 10,000–100,000 what-if budget is 70–700 s of what-if time before rebuild overhead. A 20-node rebuild at 1–2 s/node costs 20–40 s, equivalent to 2,857–5,714 what-ifs.

## Executive summary

[SOURCE] The exact additive problem is a rooted maximum-weight connected subgraph (MWCS) with a cardinality constraint, also a node-weighted rooted prize-collecting/Steiner variant. Rehfeldt and Koch develop exact integer programming for signed node weights. SCIP-Jack documentation lists rooted MWCS and maximum-weight connected subgraph problems with budget constraints: https://scipjack.zib.de/. These formulations optimize an additive surrogate, not the simulator.

[DERIVED] For a tree, the exact unit-cost DP costs O(nB²), at most about 1,300×10,000=13 million scalar combinations for B=100; a depth-first precedence recurrence can be O(nB). For the graph with m≈2.3n/2≈1,495 edges, a spanning-tree restriction is a feasible lower bound for a maximization surrogate; exact cycles require an integer model, cycle enumeration, or a tree decomposition whose width may be large.

[SOURCE] SCIP-Jack is the strongest directly matching exact lead: its documentation lists rooted MWCS, node-weighted classes, and budget-constrained MWCS (the documentation does not prove that every combination is one out-of-the-box selector) and reports PACE benchmarks with a 3,600 s limit on Intel Xeon E3-1245 3.40 GHz/32 GB. HiGHS, SCIP/PySCIPOpt, and OR-Tools CP-SAT can express the model with explicit flow or cuts. CP-SAT source says lazy-constraint registration is unsupported, so connectivity must be static or enforced in an outer solve–separate loop. pcst_fast is a fast factor-2 PCST approximation, not an exact cardinality solver.

[DERIVED] The realistic whole-solution black-box pattern is a trust-region successive-surrogate loop: estimate weights at the incumbent, solve an additive model in a Hamming neighborhood, evaluate the true candidate, accept a true improvement or controlled non-improvement, and update the radius from actual/predicted agreement. One marginal pass plus a 10,000-what-if region is about 87 s before solver time. This revisits the 22% root trunk, but a surrogate can miss threshold interactions and can spend budget on connectors.

[SOURCE] BOCS experiments use d=10–25 and 100–150 evaluations; COMBO uses 21–60 variables and hundreds of evaluations. [DERIVED] A full second-order model at d=1,300 has 1+d+C(d,2)=845,651 coefficients. Exhaustive DG2 pair screening also needs 845,651 objective evaluations: 5,919.6 s (98.7 min) at 0.007 s or 84,565 s (23.5 h) at 0.1 s.

[SOURCE] Linkage learning, GRASP, ACO-DP, path relinking, and late-acceptance rules have evidence on related objectives, but their primary benchmarks are unconstrained binary functions, Steiner trees, KCT, routing, scheduling, or QAP. [DERIVED] Three rooted B-node trees have a union of at most 1+3(B−1)=298 nodes before duplicate removal; restricted exact repair plus a true F check is a compact recombination primitive.

| Method | Added value over current search | Cost in our units | Root + budget | Black-box |
|---|---|---:|---|---|
| Tree-knapsack DP | Exact additive solve on a tree | [DERIVED] ≤13M scalar merges | Yes on tree | Via surrogate |
| Flow/cut MIP | Exact cycles and signed weights | [UNVERIFIED] Matching timing unavailable | Yes with constraints | Via surrogate |
| SCIP-Jack | Specialized exact MWCS preprocessing | [SOURCE] 3,600 s benchmark limit | Listed in docs | Via surrogate |
| Trust-region re-solve | Whole-solution trunk moves | [DERIVED] 17 s + 70–700 s | Enforce in model | Yes |
| Sparse pair screening | Local/global interactions | [DERIVED] roughly 101–132 s for screened designs | Feasibility repair | Yes |
| Three-elite union | Alternate trunks/routes | [DERIVED] union ≤298 nodes | Yes | Yes |
| SA/TA/RRT/LAHC/SCHC | Escape strict local optima | One candidate per move; rebuild dominates | Repair moves | Yes |
| BOCS/COMBO | Pairwise/graph surrogate | Published dimensions 10–60 | No native connected set | Via surrogate |

[SOURCE] The sources describe exact additive optimization, approximations, and metaheuristics under their stated objectives; they do not establish a guarantee for the thresholded simulator. **What the sources say.** [SOURCE] Exact connected optimization of the surrogate is supported; transfer from surrogate quality to F-quality is not established.

## Q1. Additive surrogate as an exactly solvable problem

### Canonical formulations

[SOURCE] Rehfeldt, Franz, and Koch define MWCS as selecting a connected vertex subset with node profits, including negative weights, and develop exact integer programming. Their report describes the requirement as “the vertices are connected” (p. 3).

[DERIVED] Use y_v∈{0,1}, y_r=1, Σ_v y_v≤B, and maximize Σ_v w_v y_v. Let x_uv select an orientation of edge {u,v}. A single-commodity root flow is:

[DERIVED] Σ_(r,j) f_rj − Σ_(j,r) f_jr = Σ_(v≠r) y_v; for v≠r, Σ_(i,v) f_iv − Σ_(v,j) f_vj = y_v; 0≤f_uv≤(B−1)x_uv; x_uv≤y_u and x_uv≤y_v. This is exact for the additive rooted problem when selected nodes can route through selected nodes.

[DERIVED] A cut formulation adds, for every U⊆V\{r} and v∈U, Σ_(i,j)∈δ−(U) x_ij ≥ y_v. There are exponentially many cuts, so separation adds a violated root cut after an incumbent or fractional solution. An MTZ-style arborescence adds order variables t_v and t_v≥t_u+1−M(1−x_uv), plus one entering arc for each selected non-root node; it is compact but usually weaker.

[SOURCE] A rooted node-weighted prize-collecting Steiner model uses prizes and edge costs with a root; a hard Σy_v≤B is an additional restriction. pcst_fast accepts edge costs, vertex prizes, a root, and a number of clusters; its source rejects negative prizes and costs. [DERIVED] A signed marginal vector and exact cardinality budget therefore need a general MIP or a carefully validated transformation.

[SOURCE] KCT selects a tree with exactly k edges and minimizes node/edge cost. Chimani, Kandyba, Ljubić, and Mutzel give an exact directed-cut ILP in Obtaining Optimal k-Cardinality Trees Fast, DOI https://doi.org/10.1145/1498698.1537600. KCTLIB instances include 1,000 nodes with average degree 2.5; the paper reports about 8.1 s mean for sparse cases over k=10–50% on a 2.4 GHz AMD Opteron/2 GB. [DERIVED] Exact-B connected node selection can use a node-weighted KCT with zero edge costs and k=B−1, while at-most-B requires all k≤B−1 and the original graph’s cycles add no selected nodes.

### Tree-knapsack DP and cycles

[SOURCE] Cho and Shaw, IJOC 9(4), DOI https://doi.org/10.1287/ijoc.9.4.431, call tree knapsack “a 0–1 knapsack problem on a rooted tree T” (abstract). Their depth-first recurrence exploits precedence and gives an O(nB)-type improvement for integer capacity. Kumabe, Maehara, and Sin’ya analyse automaton-constrained tree knapsack and recover this precedence case.

[DERIVED] For rooted tree T, let D_u[k] be the best weight in subtree T_u, containing u, with k selected nodes. Initialize D_u[1]=w_u and D_u[k]=−∞ otherwise. For child c, merge D_u with D_c by skipping c or taking a connected child piece: D_new[k]=max(D_u[k], max_t D_u[k−t]+D_c[t]). Postorder complexity is O(nB²), memory O(nB), and the answer is max_{1≤k≤B}D_r[k]. Negative weights are valid; shifting weights is safe only when cardinality is fixed.

[DERIVED] On a cyclic graph, a spanning-tree DP gives a feasible lower bound for a maximization surrogate. Exact cycle handling uses flow/cut MIP, cycle-state enumeration, or a tree decomposition with connectivity partitions; the latter is exponential in treewidth. With m≈1,495, cyclomatic number m−n+1≈196, so “mostly tree-like” does not certify small treewidth.

### Solver evidence

[SOURCE] SCIP-Jack documentation lists Steiner tree, node-weighted Steiner, rooted prize-collecting Steiner, rooted MWCS, and maximum-weight connected subgraph problems with budget constraints. The current site identifies version 2.2, Python/NetworkX plus C++, ZIB Academic License, and PACE experiments with 200 instances, 3,600 s, Xeon E3-1245 3.40 GHz, and 32 GB. No public Windows build or matching per-instance budgeted-MWCS timing was found.

[SOURCE] Heinz (El-Kebir and Klau, 2014, https://arxiv.org/abs/1409.5308) solves rooted and unrooted signed MWCS with branch-and-cut. Its DIMACS experiments use 408 instances, Xeon L5640 2.26 GHz/24 GB, two threads per instance, and a six-hour limit. The repository is MIT-licensed but requires LEMON, OGDF, and CPLEX; its build documentation targets Debian/Linux/macOS and does not expose a hard cardinality budget.

[SOURCE] pcst_fast (Hegde, Indyk, and Schmidt, 2014, https://people.csail.mit.edu/ludwigs/papers/dimacs14_fastpcst.pdf) is a factor-2 Lagrangian-preserving PCST approximation with O(dm log n) time. The paper uses a 2010 i7 2.66 GHz/8 GB Debian laptop and reports about 1.3 s for a 340,000-edge case. Its nonnegative-prize PCST objective is not exact rooted B-node MWCS.

[SOURCE] HiGHS is MIT-licensed C++11 LP/MIP/QP software; its documentation exposes logging, interrupt, incumbent, and root cut-pool callbacks, but not a general incumbent lazy-connectivity callback. SCIP/PySCIPOpt is Apache-2.0 and its lazy-constraint tutorial uses a custom constraint handler with check/enforce methods. OR-Tools CP-SAT is Apache-2.0 with Windows Python wheels; its C++ source says “add_lazy_constraints=true is not supported for CP-SAT” (callback registration). [DERIVED] Use static flow/cuts or an outer solve–separate–resolve loop for HiGHS and CP-SAT; use a constraint handler for SCIP.

[SOURCE] BioNet is GPL-2-or-later, has Windows binaries, and wraps HEINZ through runHeinz, but its manual requires CPLEX and does not expose root/budget semantics. [UNVERIFIED] Current KCTLIB license and Windows build status were not verifiable. No opened source reports a directly comparable 1,300-node, B=100, signed-node timing.

**What the sources say.** [SOURCE] Rooted budgeted connected selection is a standard additive MWCS/KCT/Steiner family with flow, cuts, MTZ, and tree-DP formulations. Specialized and general solvers can model it, but the opened sources lack a matching benchmark for the stated black-box instance.

## Q2. Surrogates, trust regions, and Bayesian optimization

[SOURCE] Trust-region sequential approximate optimization builds a local model, restricts the next point, evaluates the true objective, and updates the radius from agreement. Leyffer and Manns, SLIP, https://arxiv.org/abs/2106.13453, use actual versus predicted reduction for expensive mixed-integer black-box problems; their PDE-control experiments are not connected subgraphs.

[DERIVED] Use ρ=(F(S′)−F(S))/(m(S′)−m(S)). Accept a true improvement, shrink the radius for low ρ, and expand it for high ρ. Keep connectivity and cardinality inside the exact surrogate solve.

[SOURCE] Fischetti and Lodi, Local Branching, Mathematical Programming 98 (2003), DOI https://doi.org/10.1007/s10107-003-0395-5, add a Hamming-ball inequality:
[DERIVED] Σ_(i:x0_i=1)(1−x_i)+Σ_(i:x0_i=0)x_i≤Δ.
[DERIVED] With fixed cardinality, a t-for-t exchange changes 2t bits, so choose even Δ or use a direct exchange budget.

[SOURCE] BOCS (Baptista and Poloczek, ICML 2018, https://proceedings.mlr.press/v80/baptista18a.html) fits Bayesian second-order pseudo-Boolean models and uses SDP or simulated annealing for acquisition. Its experiments use d=10–25 and 100–150 evaluations. [DERIVED] At d=1,300, the coefficient count is 845,651; a dense 8-byte matrix needs about 67.7 GB for 10,000 observations and 676.5 GB for 100,000.

[SOURCE] COMBO (Oh, Tomczak, Gavves, and Welling, NeurIPS 2019, https://arxiv.org/abs/1902.00448) uses diffusion kernels on a Cartesian product graph and local acquisition search. Published experiments use 21–60 variables and 170–270 evaluations; one acquisition run samples 20,000 random vertices and starts 20 local searches. [DERIVED] Its graph prior is not a native connected-subset constraint; a decoder/repair can hide threshold effects.

[SOURCE] MCBO (NeurIPS 2023, https://proceedings.neurips.cc/paper_files/paper/2023/file/dbc4b67c6430c22460623186c3d3fdc2-Paper-Datasets_and_Benchmarks.pdf) provides Hamming trust regions and benchmarks 20 initial plus 180 later evaluations on mixed categorical tasks. [DERIVED] Published scale is far below 1,300 connected binary variables and no root-connectivity guarantee is built in.

[DERIVED] Failure modes are connector starvation, threshold blindness, oscillation between incompatible routes, over-large extrapolation, and a radius too small to escape the trunk. A true F check and best-incumbent fallback are mandatory.

**What the sources say.** [SOURCE] Trust-region/local-branching methods provide a neighborhood and predicted-versus-actual test; BOCS and COMBO are useful surrogate templates but their published scales are much smaller and they do not solve this connectivity contract directly.
## Q3. Capturing interactions cheaply

[SOURCE] DG2 (Omidvar et al., IEEE TEC 21(6), DOI https://doi.org/10.1109/TEVC.2017.2694221) screens pairwise differential interactions by comparing joint and separate changes. The paper states that all pairwise effects require at least n(n+1)/2+1 objective evaluations (p. 4). [DERIVED] For n=1,300 this is 1,300×1,301/2+1=845,651 evaluations: 5,919.557 s (98.66 min) at 0.007 s, or 84,565.1 s (23.49 h) at 0.1 s.

[SOURCE] RDG (Sun, Kirley, and Halgamuge, IEEE TEC, DOI https://doi.org/10.1109/TEVC.2017.2778089) reduces interaction-detection evaluations to O(n log n) under its continuous benchmark design and reports dimensions 1,000–5,000 with groups of about 50. [DERIVED] Its continuous perturbations and assumptions do not directly identify binary connected-subgraph interactions.

[SOURCE] LTGA (Thierens, PPSN XI 2010, DOI https://doi.org/10.1007/978-3-642-15844-5_27) learns linkage with hierarchical clustering and recombines subsets. DSMGA-II (Hsu and Yu, GECCO 2015, DOI https://doi.org/10.1145/2739480.2754737) uses pairwise linkage detection and a dependency-structure matrix (abstract). Their benchmarks are binary pseudo-Boolean functions, not connected sets.

[SOURCE] GOMEA uses a family of subsets, often a linkage tree, for gene-pool optimal mixing and has an open MIT-licensed C++/Python implementation with Windows wheels. [DERIVED] A full linkage tree has 2n−1=2,599 subsets. A conservative upper bound of one true evaluation per subset and population member is 2,599p; with p=32 this is 83,168 evaluations, or 582.2 s at 0.007 s. Actual implementations skip unchanged trials, but a connectivity-repair decoder can make “unchanged” ambiguous.

[SOURCE] Harmonica (Hazan, Klivans, and Yuan, ICLR 2018, https://arxiv.org/abs/1706.00764) learns sparse low-degree Fourier structure on Boolean functions under uniform samples. Its theorem has a noiseless sample form O~(K²sd log n), with n^O(d) time; experiments include 39 variables and 300 samples per stage. [DERIVED] This is not a guarantee for a constrained, discontinuous simulator. Sparse Walsh/polynomial regression is useful only after testing whether the residual is low-degree and sparse on feasible perturbations.

[UNVERIFIED] No opened primary paper established group testing for arbitrary non-submodular connected-set simulators with global multipliers and hard thresholds. [DERIVED] Under an ideal separable, noiseless, non-cancelling model, group tests could locate s active groups in O(s log n); pair synergies and threshold cancellation violate those assumptions.

[DERIVED] A graph-aware screening design can test all 1,495 edges, ten global-probe pairs for 13,000 node/probe combinations, and one baseline, for 15,796 evaluations or 110.6 s at 0.007 s. If all within-cluster pairs are tested for clusters of at most eight nodes, the pair count is at most 1,300×7/2=4,550; adding global probes and a baseline gives 18,851 evaluations or 132.0 s. These are candidate designs, not published guarantees.

**What the sources say.** [SOURCE] Linkage learning and interaction screening can reduce search for structured binary functions, but exact pairwise screening has an n² evaluation lower bound and faster methods rely on assumptions or unconstrained benchmarks. No opened source validates direct use on this thresholded connected black box.

## Q4. Randomized and population construction

[SOURCE] GRASP (Ribeiro, Uchoa, and Werneck, IJOC 14(3), DOI https://doi.org/10.1287/ijoc.14.3.228.116) alternates randomized restricted-candidate-list construction and local search; its Steiner implementation includes multiple construction heuristics and adaptive path relinking. The paper reports 370 Steiner instances, 128 iterations, elite set size 10, and a 400 MHz Pentium II-era platform. It reports roughly 90% of solutions within 1% of optimum in the first 16 iterations on one family. Its abstract describes an adaptive path-relinking technique applied to elite solutions.

[SOURCE] Reactive GRASP (Prais and Ribeiro, IJOC 12(3), DOI https://doi.org/10.1287/ijoc.12.3.164.12639) changes the probability of each RCL greediness level from observed solution quality. Its experiments are matrix-decomposition problems, not connected subgraphs. [DERIVED] Here, a small set of RCL quantiles can be updated from true F ranks; construction must remain root-connected and stop at B.

[SOURCE] Iterated greedy for hop-constrained Steiner trees (Yahyanejad and Sadeghi Bigham, https://arxiv.org/abs/1808.06981) destroys and reconstructs parts of a Steiner solution; its benchmarks contain 500–1,000 vertices and 625–25,000 edges with hop constraints. [DERIVED] The destroy/rebuild pattern transfers, but the objective and constraint differ from node-cardinality and black-box F.

[UNVERIFIED] I did not open a primary beam-search paper reporting a directly comparable rooted KCT/PCST benchmark. [DERIVED] A feasible beam can retain w partial root-connected frontiers by an additive bound, but each expansion needs repair or path completion; cost is approximately O(wBq) for q candidate extensions, with no optimality claim without an admissible bound.

[SOURCE] Blum and Blesa’s ACO-DP method for KCT (https://upcommons.upc.edu/server/api/core/bitstreams/fb82e0ee-454f-442c-bcef-b640f792c494/content) lets ants construct trees larger than k, then uses dynamic programming to extract the best k-cardinality tree. Tuning uses ten random 20×20 grids, k=40,…,200, determinant levels 75–99, and construction limits k+s,…,k+4s; l=k+2s was preferred for node-weighted cases. Tests use a Pentium IV 3 GHz/1 GB. Larger 30×30–50×50 grids show mean improvements over competing additive methods.

[DERIVED] Relative to plain greedy, GRASP/ACO spend extra true evaluations on several constructions and local searches; their strength is route diversity. For this budget, 8–16 complete solutions consume 8–16 full evaluations plus construction what-ifs. Reuse cached path values and keep the population small because region rebuilds dominate.

**What the sources say.** [SOURCE] GRASP, iterated greedy, beam-style retention, and ACO-DP have evidence on related Steiner/KCT objectives and show the value of randomized route diversity. Their parameters and timings are objective- and hardware-specific, with no direct black-box connected-subset guarantee.

## Q5. Combining good solutions

[SOURCE] Bosman, “A Solution Merging Heuristic for Steiner Problem in Graphs Using Tree Decompositions” (https://arxiv.org/abs/1504.07834), merges locally optimal Steiner solutions, forms a sparse union, computes a low-width tree decomposition, and solves the restricted instance exactly. On ES1000FST (roughly 2,500–2,900 vertices and 3,600–4,500 edges), it reports GRASP gap 0.392%, solution-merging gap 0.061%, path-relinking gap 0.109%; GRASP takes about 402 s, merging 6 s, and path relinking 493 s on a Xeon E5-2650v2 2.6 GHz/64 GB single-thread setup. ES10000 reports a 0.189% merging gap and about 310 s merging time.

[DERIVED] For three rooted B-node solutions represented by rooted trees, take U=S1∪S2∪S3. Each tree has at most B−1 non-root edges, so the union has at most 1+3(B−1)=298 distinct nodes. Restrict the additive MIP/DP to G[U], require r, |S|≤B, and connectivity, then evaluate the returned set with F. If the union solve fails or the true value is below the best parent, retain the best parent.

[DERIVED] Connectivity-preserving path relinking between Sa and Sb can add a shortest root-to-target path from Sb, then remove leaf subtrees or exchange equal-size rooted branches until the budget is restored. A union-repair solve is safer when cycles or connector dependencies make leaf removal impossible. The true objective must be checked after each accepted intermediate or after a sampled subset.

[UNVERIFIED] No opened source measured this exact three-elite, 298-node union strategy on a thresholded simulator. [DERIVED] Its likely benefit is alternate trunks and complementary clusters; its likely failure is common construction bias, which means the union cannot recover an omitted route.

**What the sources say.** [SOURCE] Steiner solution merging and path relinking can improve elite solutions on sparse Steiner benchmarks, sometimes at lower time than full path relinking. The opened source does not measure this three-solution black-box union repair.

## Q6. Acceptance rules under a fixed evaluation budget

[SOURCE] Simulated annealing was introduced by Kirkpatrick, Gelatt, and Vecchi, Science 220 (1983), DOI https://doi.org/10.1126/science.220.4598. For minimization the paper gives P(ΔE)=exp(−ΔE/kBT) for an uphill change (p. 672). [DERIVED] For maximization, accept F(S′)≥F(S) and otherwise accept with exp((F(S′)−F(S))/T); cool T after a batch and calibrate T0 from observed losses.

[SOURCE] Threshold accepting (Dueck and Scheuer, JCP 90(1), DOI https://doi.org/10.1016/0021-9991(90)90201-B) accepts a candidate when deterioration is below a decreasing threshold. Record-to-record travel (Dueck, JCP 104, DOI https://doi.org/10.1006/jcph.1993.1010) compares to the record and permits a bounded gap. ALNS documentation exposes both acceptance classes with start/end thresholds.

[SOURCE] Late-acceptance hill climbing (Burke and Bykov, PATAT 2008, https://patatconference.org/patat2008/proceedings/Bykov-HC2a.pdf) stores a circular list of past costs and compares a candidate with a value L steps old; its definition says the candidate is compared with the last element of the list (p. 2). Santini, Ropke, and Hvattum, J Heuristics 24 (2018), DOI https://doi.org/10.1007/s10732-018-9377-x, compare criteria on CMST, CVRP, and QAP with 150,000 iterations and 10 runs; tuned LAHC list lengths include 22,500 for CMST and 15,000 for CVRP. Their conclusion says relative merit changes with iteration count and operator costs.

[SOURCE] Step-counting hill climbing (Bykov and Petrovic, Journal of Scheduling 19, https://d-nb.info/1095446290/34) keeps a current-cost bound for a prescribed number of steps and tests all/accepted/improving variants. Exam-scheduling experiments use an Intel Core i7-3820 3.6 GHz/32 GB Windows 7 machine; variants improve cost but can take more time than ordinary hill climbing. [DERIVED] Acceptance is a budgeted control parameter, not a universally dominant rule.

[DERIVED] A 20-node destroy/rebuild costs 20–40 s, versus 0.007 s per what-if. A 10,000-what-if run can afford about 1.75–3.5 such rebuilds in time-equivalent terms; 100,000 can afford about 17.5–35. A derived accounting split could reserve 70% for cheap moves, 20% for 20-node rebuilds, and 10% for full reevaluation/elite merging; this is not a published optimum.

[DERIVED] With three seeds, compare paired traces by evaluation count and report median, interquartile range, and best-so-far rather than treating the best seed as an accuracy estimator. Every accepted candidate must be feasible and evaluated by F; surrogate scores may order candidates but must not replace the acceptance objective.

**What the sources say.** [SOURCE] SA, TA, RRT, LAHC, and SCHC define distinct controlled-deterioration rules; comparisons show rankings depend on iteration counts, neighborhoods, and implementation cost. No opened study determines a restart split for this simulator.

## Q7. Knowing how good the result is

[SOURCE] Exact MIP solvers provide a dual bound and incumbent gap for the additive surrogate when the model is exact. [DERIVED] A valid Lagrangian upper bound for the additive rooted budget problem is UB(λ)=λB+max_{S∋r, connected}Σ_v(w_v−λ), provided the inner problem is bounded and solved to the required precision. This bounds the surrogate, not F.

[SOURCE] Golden and Alt, Naval Research Logistics 26 (1979), DOI https://doi.org/10.1002/nav.3800260108, develop statistical intervals from independent heuristic observations under a fitted model. Carling and Meng, JCO, DOI https://doi.org/10.1007/s10878-015-9839-0, compare Weibull and jackknife estimators on p-median instances and warn that reliable bounds depend critically on high-quality heuristic samples (abstract). Their tests show poor coverage on difficult instances even with 100,000 simulated-annealing iterations.

[DERIVED] For an arbitrary deterministic black box with no global error certificate, no finite observations yield a distribution-free upper bound: an unseen feasible set can be assigned a higher value while preserving all observations. If a verified envelope |F(S)−m(S)|≤ε holds for every feasible S, then m*−ε≤F*≤m*+ε.

[DERIVED] Report additive incumbent/dual gaps, exact enumeration on small induced graphs, paired seeds and evaluation-count curves, held-out simulator scenarios where available, and repeated union/recombination tests. Report best feasible F, median, worst seed, evaluations, and surrogate gap separately.

**What the sources say.** [SOURCE] Dual bounds certify an exact additive model, and statistical estimators can produce model-based intervals from independent high-quality heuristic samples. No opened source gives a distribution-free optimum certificate for an arbitrary thresholded black box.

## Q8. Open-source code worth reading

[SOURCE] SCIP-Jack is C++/Python/NetworkX under a ZIB Academic License for non-commercial use. Its documentation lists rooted MWCS and budget-constrained MWCS. The current site does not document a public Windows package or stable public download.

[SOURCE] Heinz is C++ with a BioNet R wrapper; the MIT core requires CPLEX, LEMON, and OGDF. Rooted and unrooted signed MWCS are supported, but a hard cardinality budget is not exposed in the opened command interface. Linux/macOS builds are documented; Windows calling is high effort.

[SOURCE] pcst_fast is C++/Python/NumPy, MIT repository, with Windows wheels. Rooted PCST and multiple clusters are exposed by root and num_clusters. Nonnegative prizes/costs and no hard cardinality make it a relaxed lead.

[SOURCE] KCTLIB is C++ k-cardinality-tree code and benchmark library. Its public page is reachable, but current license and Windows build status were not verifiable. It is relevant for additive exact-k experiments, not the simulator.

[SOURCE] SCIP/PySCIPOpt is Apache-2.0 with Windows wheels. Custom constraint handlers can check/enforce connectivity cuts, so exact separation is possible but requires modeling work.

[SOURCE] OR-Tools CP-SAT is Apache-2.0 with Python Windows wheels and integer constraints. It needs explicit connectivity; its opened source has no lazy-constraint callback.

[SOURCE] HiGHS/highspy is MIT, C++/Python, and has Windows wheels. Use explicit flow or an outer cut loop; no general lazy incumbent separator was documented.

[SOURCE] GOMEA is an MIT C++/Python package with Windows wheels for unconstrained discrete/real optimization; a connected decoder and simulator wrapper are required. BOCS is GPL-3 MATLAB/older Python/CVX code; COMBO is an open Python repository with small published dimensions; ALNS is an MIT Python framework with acceptance and destroy/repair hooks.

**What the sources say.** [SOURCE] The ecosystem provides exact MIP engines, specialized PCST/MWCS/KCT code, and metaheuristic frameworks, but no drop-in Windows/Python solver for the complete rooted, budgeted, non-additive simulator.

## Method comparison

| Method | What it adds over greedy + local search | Evaluations / solver time at this size | Root + cardinality? | Black-box? | Primary source |
|---|---|---:|---|---|---|
| [SOURCE] Tree-knapsack DP | Exact additive reoptimization on a tree | [DERIVED] O(nB²), about 13M scalar merges | Yes on tree | Via surrogate | Cho & Shaw 1997, https://doi.org/10.1287/ijoc.9.4.431 |
| [SOURCE] Flow/cut MIP | Exact cycles and signed weights | [UNVERIFIED] Matching timing unavailable | Yes with constraints | Via surrogate | Rehfeldt & Koch 2019 |
| [SOURCE] SCIP-Jack | Specialized MWCS branch-and-cut | [SOURCE] 3,600 s PACE limit | Listed in docs | Via surrogate | https://scipjack.zib.de/ |
| [DERIVED] Trust-region surrogate | Whole-solution trunk moves | 17 s marginal + 70–700 s region | Yes in model | Yes | Leyffer & Manns |
| [SOURCE] BOCS | Pairwise pseudo-Boolean model | 100–150 evaluations in d≤25 studies | No native connectivity | Via surrogate | https://proceedings.mlr.press/v80/baptista18a.html |
| [SOURCE] COMBO | Graph diffusion prior | 170–270 evaluations in d≤60 studies | Product graph, not set | Via surrogate | https://arxiv.org/abs/1902.00448 |
| [SOURCE] DG2 | Pairwise interaction map | [DERIVED] 845,651 all-pair lower-bound tests | No native connectivity | Yes if feasible | https://doi.org/10.1109/TEVC.2017.2694221 |
| [SOURCE] LTGA/DSMGA/GOMEA | Learned linkage/recombination | [DERIVED] 83,168 conservative full-FOS evals at p=32 | Decoder needed | Yes | Thierens 2010; Hsu & Yu 2015 |
| [SOURCE] GRASP/reactive GRASP | RCL construction and elite relinking | [SOURCE] 128 iterations, elite 10 in Steiner study | Feasible construction needed | Yes | https://doi.org/10.1287/ijoc.14.3.228.116 |
| [SOURCE] ACO-DP KCT | Ant diversity plus exact k-tree DP | [SOURCE] Grid tuning, hardware-specific | Exact k | Via surrogate | Blum & Blesa 2005 |
| [SOURCE] Three-elite union | Alternate trunks/routes | [DERIVED] union ≤298 nodes + restricted solve | Yes | Yes | Bosman 2015 |
| [SOURCE] SA/TA/RRT/LAHC/SCHC | Controlled escape | One true candidate per move | Repair required | Yes | Kirkpatrick 1983; Dueck 1990 |

## Solver matrix

| Solver | Problem classes from opened documentation | Rooted? | Budgeted? | Node weights? | Licence | Interface / Windows | Reported near-size times |
|---|---|---|---|---|---|---|---|
| SCIP-Jack | [SOURCE] “rooted maximum-weight connected subgraph”; “maximum-weight connected subgraph problems with budget constraints”; node-weighted Steiner | Yes | Yes in class list | Yes | ZIB Academic, non-commercial | Python/NetworkX + C++; current distribution on request; Windows unverified | 200 PACE instances, 3,600 s, Xeon E3-1245/32 GB |
| Heinz | [SOURCE] Rooted/unrooted signed MWCS | Yes | No exposed hard budget | Signed node scores | MIT core; CPLEX dependency | C++/R; Linux/macOS docs | 408 DIMACS, six-hour limit, Xeon L5640/24 GB |
| pcst_fast | [SOURCE] PCST/PCSF with root, prizes, costs, clusters | Yes | No cardinality | Nonnegative prizes | MIT repository | Python/C++; Windows wheels | Up to 1.3 s for 340k edges on i7 laptop |
| SCIP/PySCIPOpt | [SOURCE] General MIP/constraint programming | Via flow/cuts | Yes | Yes | Apache-2.0 | Python/C++; Windows wheels; Conshdlr | No matching timing |
| HiGHS/highspy | [SOURCE] LP/MIP/QP | Via explicit flow | Yes | Yes | MIT | Python/C++; Windows wheels; outer cuts | No matching timing |
| OR-Tools CP-SAT | [SOURCE] Integer CP-SAT | Static flow/cuts | Yes | Scaled integer weights | Apache-2.0 | Python/C++; Windows wheels; no lazy callback | No matching timing |
| KCTLIB | [SOURCE] k-cardinality trees | Root transform | Exact k only | Node/edge costs | [UNVERIFIED] | C++; Windows unverified | 1,000-node sparse mean 8.1 s in paper |
| BioNet/HEINZ | [SOURCE] Maximum-scoring subnetworks | Root/budget not exposed | No | Scores | GPL wrapper; CPLEX | R Windows binary; CPLEX setup | Wrapper only |
| GOMEA | [SOURCE] Linkage black-box optimization | Decoder | Decoder | Binary/discrete | MIT | C++/Python Windows wheels | 83,168 conservative eval bound at p=32 |

## Derived pseudo-code sketches

### Tree-knapsack DP on a rooted tree

~~~text
[DERIVED] TreeDP(u):
[DERIVED]   D[1..B] = -infinity; D[1] = w[u]; used = 1
[DERIVED]   for child c of u in postorder:
[DERIVED]       C = TreeDP(c); N = D                 # skip child
[DERIVED]       for a = 1..used:
[DERIVED]           for b = 1..min(B-a, size(C)):
[DERIVED]               N[a+b] = max(N[a+b], D[a] + C[b])
[DERIVED]       D = N; used = min(B, used + size(C))
[DERIVED]   return D
[DERIVED] Answer = max(TreeDP(r)[k] for k=1..B)
~~~

### Trust-region surrogate loop

~~~text
[DERIVED] S = initial feasible incumbent; Delta = initial Hamming radius
[DERIVED] best = S
[DERIVED] repeat until evaluation budget exhausted:
[DERIVED]     w = marginal_vector(S)                 # 17 s
[DERIVED]     m = additive_or_sparse_model(w, history)
[DERIVED]     S2 = exact_solve(m, root=r, size<=B, connected, Hamming<=Delta)
[DERIVED]     if S2 == S: Delta = max(2, Delta/2); continue
[DERIVED]     true_gain = F(S2) - F(S); predicted = m(S2) - m(S)
[DERIVED]     rho = true_gain / predicted if predicted > 0 else -infinity
[DERIVED]     if true_gain > 0: S = S2; best = argmax_F(best, S)
[DERIVED]     if rho < 0.1: Delta = max(2, floor(Delta/2))
[DERIVED]     elif rho > 0.75: Delta = min(Delta_max, 2*Delta)
[DERIVED]     append(S, S2, true_gain, predicted, rho) to history
[DERIVED] return best
~~~

### Three-solution recombination

~~~text
[DERIVED] Input: feasible rooted sets S1, S2, S3 and additive weights w
[DERIVED] U = nodes(S1) union nodes(S2) union nodes(S3)
[DERIVED] restrict graph and weights to U; force y[r]=1 and sum(y)<=B
[DERIVED] solve exact connected additive model on G[U]
[DERIVED] candidates = {returned set, S1, S2, S3}
[DERIVED] for T in candidates:
[DERIVED]     repair(T) by root paths and leaf/subtree deletion if necessary
[DERIVED]     if connected(T) and |T|<=B: evaluate F(T)
[DERIVED] return argmax true F among feasible candidates
[DERIVED] if restricted solve fails: return best true parent
~~~

## Known failure modes and negative results

[DERIVED] **Connector starvation:** additive weights can spend the budget on profitable leaves and omit a zero-value bridge. Enforce connectivity in every surrogate and retain route completion.

[DERIVED] **Threshold blindness:** one-node marginals can be zero below a threshold and large after a group is present. Use pair/cluster proposals and true evaluation; do not infer submodularity.

[DERIVED] **Trunk lock-in:** a tiny trust region cannot revisit the 22% root trunk. Periodically run a larger region, three-elite union, or root-anchored destroy/rebuild.

[DERIVED] **Surrogate oscillation:** marginal vectors at alternating incumbents can point to incompatible routes. Track rho, cap radius expansion, and keep the best true incumbent.

[DERIVED] **Dense quadratic explosion:** BOCS-style second-order parameter count is 845,651 at n=1,300; dense fitting/acquisition is incompatible with the budget without sparsity.

[DERIVED] **All-pairs screening explosion:** DG2’s lower-bound 845,651 evaluations exceed a 10,000–100,000 what-if budget unless tests use a validated cheaper approximation.

[DERIVED] **Connectivity-repair bias:** linkage, beam, or BO decoders can change the intended bit flip into a path insertion/deletion. Log requested and repaired moves.

[SOURCE] **Solver callback mismatch:** CP-SAT does not support lazy-constraint registration; HiGHS documents cut-pool and incumbent callbacks but no general lazy incumbent separator. Static flow/cuts or an outer loop is required.

[SOURCE] **Approximation mismatch:** pcst_fast’s factor-2 PCST guarantee and nonnegative-prize API do not certify signed exact-cardinality MWCS. Heinz’s exact MWCS reductions do not expose the hard budget in the opened interface.

[SOURCE] **Statistical overclaim:** Golden–Alt and Carling–Meng intervals rely on fitted distributions and high-quality independent samples; they are not distribution-free certificates.

[UNVERIFIED] No opened paper reports this exact hybrid on this graph family, with these timings, or with only three seeds. Those results must be measured experimentally.

## Evidence register for named techniques and solvers

[DERIVED] The following register makes the required source/quote/condition boundary explicit. [SOURCE] Quotes are limited to short defining fragments and are accompanied by the source’s class, scale, timing, and hardware where the opened source reports them. [UNVERIFIED] means that the requested primary source or a matching condition was not available in the opened material.

| Technique or solver | Primary source and defining quote | Conditions attached by the source |
|---|---|---|
| [SOURCE] Rooted MWCS IP | Rehfeldt, Franz & Koch (2020, ZIB report), “the vertices are connected” (p. 3) | Signed node weights; exact MWCS/preprocessing; no simulator; report gives formulation rather than a matching 1,300-node timing. |
| [SOURCE] Flow/cut connectivity | Rehfeldt & Koch (2019, SIAM J. Optimization, DOI 10.1137/17M1145963), formulation sections | Exact MWCS; flow/cut constraints are model components; hardware/timing depend on instances and solver. |
| [DERIVED] MTZ formulation | Derived order constraints from standard arborescence modeling | No separate opened primary quote located; exactness follows from the stated arborescence constraints, while relaxation strength is model-dependent. |
| [SOURCE] Tree-knapsack DP | Cho & Shaw (1997, IJOC 9(4), DOI 10.1287/ijoc.9.4.431), “a 0–1 knapsack problem on a rooted tree T” (abstract) | Integer capacity and precedence/tree structure; pseudopolynomial DP; no cyclic graph or black-box threshold guarantee. |
| [SOURCE] KCT | Chimani, Kandyba, Ljubić & Mutzel (2010, JEA, DOI 10.1145/1498698.1537600), “a minimum-weight tree with k edges” (introduction) | Additive node/edge cost; sparse 1,000-node KCTLIB mean about 8.1 s on 2.4 GHz AMD Opteron/2 GB; exact k, not at-most k without enumeration. |
| [SOURCE] SCIP-Jack | SCIP-Jack documentation (v2.2, 2026), class list includes rooted MWCS and budget-constrained MWCS | Steiner/MWCS family; PACE 200 instances, 3,600 s, Xeon E3-1245 3.40 GHz/32 GB; ZIB Academic License; current distribution on request. |
| [SOURCE] Heinz | El-Kebir & Klau (2014, arXiv:1409.5308), MWCS-to-optimality paper | Rooted/unrooted signed MWCS; 408 DIMACS instances; six-hour limit; Xeon L5640 2.26 GHz/24 GB; CPLEX dependency; no opened hard-budget option. |
| [SOURCE] PCST approximation | Hegde, Indyk & Schmidt (2014, DIMACS), fast PCST paper | Nonnegative prizes/costs; factor-2 Lagrangian-preserving approximation; about 1.3 s for 340k edges on i7 2.66 GHz/8 GB Debian. |
| [SOURCE] BOCS | Baptista & Poloczek (2018, ICML), “excellent trade-off in practice” (p. 5) | Bayesian second-order pseudo-Boolean model; d=10–25; 100–150 evaluations; SDP/SA acquisition; no connectivity constraint. |
| [SOURCE] COMBO | Oh et al. (2019, NeurIPS), COMBO paper and algorithm section | Diffusion kernel on Cartesian-product categorical graph; d=21–60; 170–270 evaluations; acquisition starts use 20,000 random vertices and 20 local searches; no native connected set. |
| [SOURCE] DG2 | Omidvar et al. (2017, IEEE TEC, DOI 10.1109/TEVC.2017.2694221), pairwise differential-interaction screening | Binary/continuous benchmark interaction detection; all-pair lower bound n(n+1)/2+1; source does not validate connected feasibility repair. |
| [SOURCE] RDG | Sun, Kirley & Halgamuge (2018, IEEE TEC, DOI 10.1109/TEVC.2017.2778089), RDG interaction grouping | Continuous benchmark functions, dimensions 1,000–5,000, groups around 50; O(n log n) evaluation claim under those assumptions. |
| [SOURCE] LTGA | Thierens (2010, PPSN XI, DOI 10.1007/978-3-642-15844-5_27), linkage-tree clustering/recombination method section | Binary evolutionary optimization; hierarchical linkage learned from population; no root/budget connectivity in base algorithm. |
| [SOURCE] DSMGA-II | Hsu & Yu (2015, GECCO, DOI 10.1145/2739480.2754737), “pairwise linkage detection” (abstract) | Binary pseudo-Boolean benchmarks; dependency-structure matrix; population evaluations; no connected-subgraph constraint. |
| [SOURCE] GOMEA | Dushatskiy et al. (2021, GECCO/arXiv:2109.05259), family-of-subsets optimal mixing sections | Discrete/real black-box optimization; linkage/FOS; package offers C++/Python; no native connectivity or budget. |
| [SOURCE] Harmonica | Hazan, Klivans & Yuan (2018, ICLR), “sparse low-degree polynomial” (abstract) | Boolean functions, uniform sampling, low degree/sparsity assumptions; theorem sample form O~(K²sd log n); experiments up to 39 variables. |
| [UNVERIFIED] Group testing | No opened primary source matching arbitrary non-submodular connected simulators | O(s log n) is only an ideal separable/noiseless inference heuristic; no validated simulator condition. |
| [SOURCE] GRASP | Ribeiro, Uchoa & Werneck (2002, IJOC 14(3), DOI 10.1287/ijoc.14.3.228.116), “adaptive path-relinking” (abstract) | Steiner instances: 370 cases, 128 iterations, elite 10, Pentium II 400 MHz; additive edge-cost objective. |
| [SOURCE] Reactive GRASP | Prais & Ribeiro (2000, IJOC 12(3), DOI 10.1287/ijoc.12.3.164.12639), reactive probability update sections | Matrix-decomposition benchmarks; RCL greediness probabilities adapt to observed quality; no connected-black-box benchmark. |
| [SOURCE] Iterated greedy | Yahyanejad & Sadeghi Bigham (2018, arXiv:1808.06981), destroy/reconstruct sections | Hop-constrained Steiner; 500–1,000 vertices, 625–25,000 edges; C++/benchmark-specific; objective differs from node budget. |
| [UNVERIFIED] Beam search | No opened primary source with a matching rooted KCT/PCST benchmark | Generic beam bound in this report is derived; no source timing or guarantee for this simulator. |
| [SOURCE] ACO-DP KCT | Blum & Blesa (2005, IWANN/LNCS report), “more than k edges” construction statement | Additive KCT; 20×20 tuning grids, k=40–200; 30×30–50×50 test grids; Pentium IV 3 GHz/1 GB. |
| [SOURCE] Solution merging | Bosman (2015, arXiv:1504.07834), solution-merging method section | Steiner union + tree decomposition; ES1000FST 2,500–2,900 vertices, 3,600–4,500 edges; Xeon E5-2650v2 2.6 GHz/64 GB; merging about 6 s. |
| [SOURCE] Simulated annealing | Kirkpatrick, Gelatt & Vecchi (1983, Science, DOI 10.1126/science.220.4598), \(P(\Delta E)=\exp(-\Delta E/k_BT)\) (p. 672) | Statistical-physics/local-search analogy; temperature schedule and neighborhood determine results; not connected-subgraph-specific. |
| [SOURCE] Threshold accepting | Dueck & Scheuer (1990, JCP, DOI 10.1016/0021-9991(90)90201-B), threshold-acceptance method | Threshold decreases over iterations; source is general combinatorial optimization, not this simulator. |
| [SOURCE] Record-to-record travel | Dueck (1993, JCP, DOI 10.1006/jcph.1993.1010), record-gap method | Accepts candidates within a record-to-record deviation; source timing is problem-specific. |
| [SOURCE] LAHC | Burke & Bykov (2008, PATAT), circular-history comparison definition | Scheduler/local-search method; Santini et al. compare 150,000 iterations and tuned list lengths on CMST/CVRP/QAP. |
| [SOURCE] SCHC | Bykov & Petrovic (2016, Journal of Scheduling, DOI 10.1007/s10951-016-0469-x), step-counting bound method | Exam scheduling; Intel i7-3820 3.6 GHz/32 GB Windows 7; variants trade quality for time. |
| [SOURCE] Statistical optimum intervals | Golden & Alt (1979, Naval Research Logistics, DOI 10.1002/nav.3800260108); Carling & Meng (2016, JCO, DOI 10.1007/s10878-015-9839-0) | Fitted distributions/high-quality independent samples; p-median experiments; not distribution-free black-box certificates. |
| [SOURCE] CP-SAT callback behavior | OR-Tools CP-SAT source, callback registration | “add_lazy_constraints=true is not supported for CP-SAT”; use explicit constraints or an outer loop. |
| [SOURCE] HiGHS callbacks | HiGHS callback documentation | Logging, interrupt, incumbent and root cut-pool callbacks documented; no general lazy-connectivity callback in opened docs. |
| [SOURCE] PySCIPOpt callbacks | PySCIPOpt lazy-constraint tutorial | Custom constraint handler check/enforce interface; exact connectivity separation requires implementation. |


## Quote and condition supplements

[SOURCE] Local branching’s defining documentation is the paper’s “local branching cuts” terminology (Fischetti & Lodi, 2003, abstract); the source condition is a MIP neighborhood explored by linear inequalities, not a black-box convergence result.

[SOURCE] SLIP reports an “actual reduction” versus predicted reduction trust-region test (Leyffer & Manns, 2022, trust-region acceptance section); its measurements are expensive mixed-integer PDE-control experiments, not connected subgraphs.

[SOURCE] COMBO is defined around a “Cartesian product graph” (Oh et al., 2019, method section); its source conditions are categorical variables and graph diffusion kernels, with 21–60-variable experiments.

[SOURCE] DG2’s defining operation is “differential grouping” (Omidvar et al., 2017, method section); the source’s evaluation lower bound is for pairwise interaction detection on benchmark functions.

[SOURCE] RDG’s method is “recursive differential grouping” (Sun et al., 2018, method section); the reported O(n log n) behavior is under the paper’s continuous benchmark assumptions.

[SOURCE] LTGA builds a “linkage tree” by hierarchical clustering (Thierens, 2010, method section); the source conditions are population-based binary optimization.

[SOURCE] GOMEA uses a “family of subsets” for gene-pool optimal mixing (Dushatskiy et al., 2021, method section); the opened implementation is a general discrete/real optimizer and has no native root/connectivity constraint.

[SOURCE] Threshold accepting is a “deterministic version of simulated annealing” (Dueck & Scheuer, 1990, method description); its threshold schedule and neighborhood are problem-dependent.

[SOURCE] Record-to-record travel accepts moves within a “record-to-record deviation” (Dueck, 1993, abstract); its guarantee is empirical and problem-specific.
## All URLs opened

### Specialized connected-subgraph sources

- https://scipjack.zib.de/
- https://optimization-online.org/wp-content/uploads/2020/08/7962.pdf
- https://doi.org/10.1137/17M1145963
- https://doi.org/10.1287/ijoc.2021.1087
- https://arxiv.org/abs/1409.5308
- https://github.com/ls-cwi/heinz
- https://bioconductor.org/packages/release/bioc/html/BioNet.html
- https://www.bioconductor.org/packages/release/bioc/manuals/BioNet/BioNet.pdf
- https://people.csail.mit.edu/ludwigs/papers/dimacs14_fastpcst.pdf
- https://github.com/fraenkel-lab/pcst_fast
- https://pypi.org/pypi/pcst_fast/json

### Solvers and interfaces

- https://github.com/scipopt/scip
- https://pyscipopt.readthedocs.io/en/latest/tutorials/lazycons.html
- https://pypi.org/pypi/pyscipopt/json
- https://highs.dev/
- https://ergo-code.github.io/HiGHS/dev/callbacks/
- https://github.com/ERGO-Code/HiGHS
- https://pypi.org/pypi/highspy/json
- https://or-tools.github.io/docs/cpp/cp__sat__solver_8cc_source.html
- https://github.com/google/or-tools
- https://pypi.org/pypi/ortools/json
- https://iridia.ulb.ac.be/~cblum/kctlib/

### Tree knapsack and KCT

- https://doi.org/10.1287/ijoc.9.4.431
- https://arxiv.org/abs/1807.04942
- https://ivanaljubic.github.io/docs/publications/kcard.pdf
- https://ivanaljubic.github.io/docs/publications/kCardinalityTrees_JEA.pdf
- https://doi.org/10.1145/1498698.1537600
- https://upcommons.upc.edu/server/api/core/bitstreams/fb82e0ee-454f-442c-bcef-b640f792c494/content

### Surrogates and interactions

- https://proceedings.mlr.press/v80/baptista18a.html
- https://proceedings.mlr.press/v80/baptista18a/baptista18a.pdf
- https://github.com/baptistar/BOCS
- https://arxiv.org/abs/1902.00448
- https://github.com/QUVA-Lab/COMBO
- https://proceedings.neurips.cc/paper_files/paper/2023/file/dbc4b67c6430c22460623186c3d3fdc2-Paper-Datasets_and_Benchmarks.pdf
- https://github.com/huawei-noah/HEBO/tree/master/MCBO
- https://doi.org/10.1007/s10107-003-0395-5
- https://arxiv.org/abs/2106.13453
- https://eprints.whiterose.ac.uk/id/eprint/154094/1/VOR%2007911173.pdf
- https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/6aa1cbb3-1ad1-41ec-aee2-8f1ec1f47b98/content
- https://arxiv.org/abs/1807.11669
- https://doi.org/10.1145/2739480.2754737
- https://doi.org/10.1007/978-3-642-15844-5_27
- https://arxiv.org/abs/2109.05259
- https://github.com/CWI-EvolutionaryIntelligence/GOMEA
- https://pypi.org/pypi/gomea/json
- https://arxiv.org/abs/1706.00764

### Construction, recombination, and acceptance

- https://doi.org/10.1287/ijoc.14.3.228.116
- https://doi.org/10.1287/ijoc.12.3.164.12639
- https://arxiv.org/abs/1808.06981
- https://arxiv.org/abs/1504.07834
- https://doi.org/10.1126/science.220.4598
- https://hedibert.org/wp-content/uploads/2013/12/1983KirkpatrickGelattVecchi.pdf
- https://doi.org/10.1016/0021-9991(90)90201-B
- https://doi.org/10.1006/jcph.1993.1010
- https://alns.readthedocs.io/en/latest/api/accept.html
- https://patatconference.org/patat2008/proceedings/Bykov-HC2a.pdf
- https://doi.org/10.1007/s10732-018-9377-x
- https://d-nb.info/1095446290/34
- https://github.com/N-Wouda/ALNS

### Bounds and statistics

- https://doi.org/10.1002/nav.3800260108
- https://ideas.repec.org/a/wly/navlog/v26y1979i1p69-77.html
- https://doi.org/10.1007/s10878-015-9839-0
- https://du.diva-portal.org/smash/get/diva2%3A719712/FULLTEXT01.pdf






