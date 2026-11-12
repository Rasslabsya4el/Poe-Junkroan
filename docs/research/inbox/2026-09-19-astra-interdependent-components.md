# Interdependent-component optimization: who moves when

**Scope.** [SOURCE] This report executes the supplied research brief for a four-component deterministic black-box optimizer: tree component **T**, cross-slot catalogue component **G**, ordered compatible-module lists **K**, and derived component **C**. [DERIVED] One full simulator evaluation is treated as 0.1–0.2 s and a one-component what-if as 0.007 s, using the costs in the brief; source papers use their own budgets and are not directly comparable.

**Evidence labels.** [SOURCE] means a claim is taken from a source opened during this review; [DERIVED] means arithmetic or design derived from sourced facts and the supplied costs; [UNVERIFIED] means a lead was not opened and is not used as evidence.

## 1. Executive summary

1. **Interaction-aware coordination and compound moves.** [SOURCE] TTP research proves that nonlinear coupling prevents additive decomposition and reports that a whole-solution memetic algorithm beat standard and dynamic cooperative coevolution under comparable budgets (Mei, Li & Yao, *Soft Computing*, 2016, DOI 10.1007/s00500-014-1487-2). [SOURCE] The later CoCo solver changes the packing plan while exploring tour moves and uses tour information during item selection (Namazi et al., *Journal of Heuristics*, 2023, DOI 10.1007/s10732-023-09518-7). [DERIVED] The closest analogue is a **(T,G) compound move** followed by C re-derivation; one candidate costs one full evaluation (0.1–0.2 s) plus 0.007-s screening what-ifs.

2. **Contribution-based effort allocation.** [SOURCE] Bandit-based cooperative coevolution identifies that round-robin gives uniform resources even when components contribute unequally, then allocates resources proportional to observed contribution (Kazimipour et al., *Applied Soft Computing*, 2019, DOI 10.1016/j.asoc.2018.12.007). [DERIVED] Use arms for T, each G slot/block, each K list, TG, and GK; reward is accepted full-objective gain divided by evaluation cost. An arm decision is negligible; a probe costs one full evaluation unless a valid cached delta exists.

3. **Staleness and dynamic refresh.** [SOURCE] TTP work says component searches often see only the other component’s unchanged current solution, creating poor coordination. [SOURCE] Resource-allocation CC work combines contribution measurement, stagnation handling, pruning and bandit selection (Kim & Choi, *Applied Soft Computing*, 2021, DOI 10.1016/j.asoc.2021.108013). [DERIVED] Track each component’s last accepted improvement, collaborator age, and the gain after a collaborator refresh; force a joint probe when isolated progress stalls but a refresh helps.

4. **Exact/limited-time G sub-solve.** [SOURCE] MMKP is “one item for each group” with multiple resource constraints; Mansini & Zanotti’s core-based exact method solves increasing subproblems by recursive variable fixing, closes ten open instances to optimality, and reports better solutions in three minutes than Gurobi in one hour (INFORMS JOC 2020, DOI 10.1287/ijoc.2019.0909). [SOURCE] Gurobi documents MIP starts, partial starts, solution pools and quality bounds. [DERIVED] Build a linear marginal-value surrogate for G at fixed (T,K), impose all catalogue constraints exactly, time-limit the solve, and verify candidates in the real simulator.

5. **Warm starts and bounded trust.** [SOURCE] Gurobi accepts feasible MIP starts, may repair infeasible starts, can complete partial starts with a node limit, and exposes solution-pool bounds after early termination. [DERIVED] Record exact/optimal status, incumbent, bound, gap and simulator value; treat a timed-out candidate as bounded/heuristic, never as proof.

6. **Feasibility-first handling.** [SOURCE] Deb’s rules prefer feasible over infeasible, better objective among feasible, and lower violation among infeasible (Deb, *CMAME*, 2000, DOI 10.1016/S0045-7825(99)00389-8). [SOURCE] Stochastic ranking balances objective and violation without a fixed penalty coefficient and was tested on 13 benchmarks (Runarsson & Yao, *IEEE TEC*, 2000, DOI 10.1109/4235.873238). [DERIVED] Use Deb ordering for production acceptance and stochastic ranking only for exploratory infeasible kicks.

7. **Realistic collaborator construction.** [SOURCE] TTP constructive methods first build a tour without packing, then freeze it while constructing packing; a deterministic constructive heuristic is strong on very large instances, while random search from an empty packing can fail to reach it within ten minutes (Polyakovskiy et al., *GECCO* 2014). [DERIVED] Replace “G against empty T” with 2–3 representative collaborator states; at 0.1–0.2 s each this is negligible beside a 200-s pass.

8. **Coupling-variable architectures.** [SOURCE] Nonhierarchical analytical target cascading (ATC) introduces target-response coupling and system-wide functions over variables from multiple subproblems (Tosserams et al., *JMD*, 2010, DOI 10.1115/1.4001346). [SOURCE] MDO surveys describe collaborative system/discipline architectures (Martins & Lambe, *AIAA J.*, 2013). [DERIVED] Use explicit snapshots and consistency residuals, but do not claim convex convergence for this discrete black-box problem.

## 2. Q1 — Names and literature

### Travelling Thief Problem and multi-component optimization

**Primary source:** Yi Mei, Xiaodong Li and Xin Yao, “On investigation of interdependence between sub-problems of the Travelling Thief Problem,” *Soft Computing* 20 (2016) 157–172, DOI [10.1007/s00500-014-1487-2](https://doi.org/10.1007/s00500-014-1487-2). [SOURCE] Defining quote: “First, the analysis on the mathematical formulation shows that it is impossible to decompose the problem into independent sub-problems due to the non-linear relationship in the objective function.” (abstract). [SOURCE] Conditions: two components (TSP tour and knapsack), nonlinear objective, TTP benchmark instances; standard/dynamic CC and a whole-solution memetic algorithm were compared under comparable budgets.

[SOURCE] The same paper states that its memetic algorithm obtained much better results than both standard and dynamic CC on all test instances (abstract/results). [SOURCE] Conditions: the result is for the authors’ TTP benchmark and operators, not this simulator.

**Primary source:** Majid Namazi, M.A.H. Newton, Conrad Sanderson and Abdul Sattar, “Solving travelling thief problems using coordination based methods,” *Journal of Heuristics* 29 (2023) 487–544, DOI [10.1007/s10732-023-09518-7](https://doi.org/10.1007/s10732-023-09518-7), author PDF [https://conradsanderson.id.au/pdfs/namazi_solving_ttp_coordination_methods_2023.pdf](https://conradsanderson.id.au/pdfs/namazi_solving_ttp_coordination_methods_2023.pdf). [SOURCE] Defining quote: “Existing TTP solvers deal with city selection and item selection separately, keeping decisions for one type unchanged while dealing with the other type. This separation essentially means very poor coordination between two types of decision.” (abstract, p. 1). [SOURCE] Conditions: static TTP; all cities visited; 2-opt tour and bit-flip packing neighborhoods; TTP benchmark instances.

[SOURCE] Namazi et al. classify TTP methods as constructive, fixed-tour, cooperative, full-encoding and hyper-heuristic. Cooperative methods alternate tour and packing searches while keeping the other component unchanged (Section 3). [SOURCE] Conditions: classification is specific to TTP literature.

**What the sources say.** [SOURCE] TTP is the closest named line because it models individually meaningful but nonseparably coupled components. [SOURCE] It supports interaction-aware coordination and compound operators; it does not prove a fixed alternating loop is always inferior on every problem.

### Cooperative coevolution and interaction awareness

**Primary source:** Behzad Kazimipour, Mohammad N. Omidvar, A.K. Qin, Xiaodong Li and Xin Yao, “Bandit-based cooperative coevolution for tackling contribution imbalance in large-scale optimization problems,” *Applied Soft Computing* 76 (2019) 265–281, DOI [10.1016/j.asoc.2018.12.007](https://doi.org/10.1016/j.asoc.2018.12.007), repository [https://eprints.whiterose.ac.uk/id/eprint/156297/](https://eprints.whiterose.ac.uk/id/eprint/156297/). [SOURCE] Defining quote: “Cooperative coevolution typically works by breaking a problem down into smaller subproblems (or components) and coevolving them in a round-robin fashion, resulting in a uniform resource allocation among its components.” (abstract). [SOURCE] Conditions: large-scale continuous benchmarks; bandit credit assignment allocates effort proportional to measured contribution.

[SOURCE] Mei et al. write: “For the non-linearly interdependent subcomponents, a weak selection pressure is more promising, e.g., selecting the collaborators randomly.” (Section 2). [SOURCE] Conditions: observation for nonlinear TTP coupling; independent components favor stronger collaborator selection in the same discussion.

[UNVERIFIED] Specific primary papers for differential grouping, CCVIL, recursive grouping and BLVG were found in search results but not opened in full; they are excluded as evidence.

**What the sources say.** [SOURCE] CC is a valid abstraction for T/G/K blocks, but static round-robin and stale best collaborators are documented weaknesses under nonlinear coupling. [SOURCE] Contribution-based allocation and weaker/multiple collaborators are documented responses.

### Block-coordinate and alternating optimization

**Primary source:** Amir Beck and Luba Tetruashvili, “On the Convergence of Block Coordinate Descent Type Methods,” *SIAM Journal on Optimization* 23 (2013), DOI [10.1137/120887679](https://doi.org/10.1137/120887679). [SOURCE] Defining quote: “We study smooth convex programming problems where the decision variables vector is split into several blocks of variables. We analyze the block coordinate gradient projection method in which each iteration consists of performing a gradient projection step with respect to a certain block taken in a cyclic order.” (abstract). [SOURCE] Conditions: smooth convex programming; the paper proves sublinear convergence and, under strong convexity, a linear rate. [DERIVED] Those assumptions do not match the discrete black-box simulator.

**What the sources say.** [SOURCE] Alternating optimization is the mathematical analogue of the current loop. [SOURCE] Its strongest guarantees are for smooth convex settings and do not cover this landscape.

### Discrete MDO and coupling variables

**Primary source:** S. Tosserams et al., “A Nonhierarchical Formulation of Analytical Target Cascading,” *Journal of Mechanical Design* 132 (2010) 051002, DOI [10.1115/1.4001346](https://doi.org/10.1115/1.4001346). [SOURCE] Defining quote: “This paper presents a new ATC formulation that allows nonhierarchical target-response coupling between subproblems and introduces system-wide functions that depend on variables of two or more subproblems.” (abstract). [SOURCE] Conditions: engineering MDO; augmented-Lagrangian coordination; convergence relies on convexity/continuity assumptions.

**Primary source:** Joaquim R.R.A. Martins and Andrew B. Lambe, “Multidisciplinary Design Optimization: A Survey of Architectures,” *AIAA Journal* 51 (2013), author PDF [https://websites.umich.edu/~mdolaboratory/pdf/Martins2013.pdf](https://websites.umich.edu/~mdolaboratory/pdf/Martins2013.pdf). [SOURCE] The survey describes collaborative system/discipline architectures and adaptations for multiobjective, robust and multifidelity MDO (Section 4.2). [SOURCE] Conditions: engineering disciplines with explicit shared/coupling variables.

**What the sources say.** [SOURCE] ATC/MDO contributes coupling-variable bookkeeping, consistency residuals and a master/discipline split. [DERIVED] Only the coordination pattern transfers directly; convex convergence theorems do not.

## 3. Q2 — Scheduling effort and stale collaboration

### Adaptive allocation

[SOURCE] Kazimipour et al. state that their framework allocates computational resources to each component proportional to its contribution to overall improvement (abstract). [SOURCE] Conditions: online multi-armed-bandit credit assignment; large-scale continuous benchmarks.

**Primary source:** Kim & Choi, “Cooperative coevolutionary algorithm with resource allocation strategies to minimize unnecessary computations,” *Applied Soft Computing* 113 (2021) 108013, DOI [10.1016/j.asoc.2021.108013](https://doi.org/10.1016/j.asoc.2021.108013). [SOURCE] Its indexed abstract lists contribution evaluation, stagnation escape, contribution/size allocation, pruning and multi-armed-bandit subproblem selection. [SOURCE] Conditions: CEC’2010/CEC’2013 large-scale continuous benchmarks; fully nonseparable functions are excluded from the resource-allocation comparison because they have one subproblem.

**[DERIVED]** Maintain `r_a = accepted_gain / (full_evals + 0.047*what_if_evals)`, because `0.007/0.15 ≈ 0.047` full-evaluation equivalents. Choose the arm maximizing `r_a + sqrt(2 ln N/n_a)` and reserve one probe per arm every horizon `H`.

### Slice length and switching

[SOURCE] TTP cooperative methods alternate searches until no further improvement; CoCo inserts coordination changes during component exploration rather than waiting for a complete isolated pass (Namazi et al., Sections 3 and 5). [SOURCE] No opened paper establishes a universal optimal inner-iteration count.

**[DERIVED]** Stop a slice after `q` consecutive failures, budget `B_a`, or collaborator-age trigger. At 0.15 s per full evaluation, five evaluations cost about 0.75 s; the reported 200-s pass is about 1,333 full evaluations.

### Staleness detection

[SOURCE] Namazi et al. say that existing methods use the other component’s unchanged current solution and that the best overall solution requires mutual correspondence. [SOURCE] Mei et al. report that standard/dynamic CC still loses to a whole-solution MA on TTP benchmarks.

**[DERIVED]** Record collaborator age and cross-effect ratio `gain_after_refresh / gain_before_refresh`. Mark a pair stale when age exceeds `H` and the ratio exceeds `1+δ`, or when isolated moves fail but a paired probe improves. A paired probe costs one full evaluation.

**What the sources say.** [SOURCE] Adaptive effort is supported when contributions are imbalanced; no opened source gives a universal slice length or formal stale-state detector for discrete black-box optimization. [DERIVED] The detector above is an operational synthesis of the documented failure mode.

## 4. Q3 — Joint moves

### TTP compound/coordination operators

[SOURCE] Namazi et al. write: “Our proposed approaches could also be viewed as cooperative approaches since our algorithm also does move between cyclic tour exploration and collection plan exploration in an interleaving fashion.” (Section 4). [SOURCE] Their heuristics change collection plans during tour exploration and exploit tour structure during item selection.

[SOURCE] Their Lemma 8 says that after cached prefix/suffix data, evaluating a 2-opt tour move needs `O(e-b)` time; Lemma 9 says a bit-flip packing move needs `O(n-t(li))` time (author PDF, p. 4). [SOURCE] Conditions: TTP incremental objective and cached arrays, not a generic simulator.

**[DERIVED] TG move.** Pick a T segment and G slots touching affected nodes/attributes; apply a T reconnect and simultaneously re-solve/perturb those G slots; derive C; use 0.007-s what-ifs for screening and one 0.1–0.2-s full evaluation for acceptance.

### Which parts move together

[SOURCE] CoCo selects coordinated item moves using tour position, item profitability and carrying effects rather than arbitrary independent bits (Sections 5.2–5.3). [SOURCE] A simple local-search coordination approach was ineffective, motivating human-designed and learned coordination heuristics.

**[DERIVED]** Build an interaction graph over T, G slots, K lists and derived outputs. Weight edge `(a,b)` by median absolute full-objective change from paired perturbations; probe the largest edges first. Pair candidates `(T,G_j)`, `(G_i,G_j)` for shared covering sums, and `(T,K_l)` for multiplier effects.

### VND/VNS ordering

**Primary source:** Mladenović & Hansen, “Variable Neighborhood Search,” *Computers & Operations Research* 24 (1997) 1097–1100, DOI [10.1016/S0305-0548(97)00031-2](https://doi.org/10.1016/S0305-0548(97)00031-2). [SOURCE] Defining quote: “Systematic change of neighborhood within a local search algorithm yields a simple and effective metaheuristic for combinatorial optimization.” (abstract). [SOURCE] Conditions: TSP and backhaul illustrations; neighborhood changes are used both in descent and to escape local optima.

[SOURCE] The opened VNS tutorial states that implementations often rank moves by application complexity or neighborhood size and return to the first neighborhood after a descent step. [SOURCE] Conditions: generic VNS/VND framework.

**[DERIVED]** Use cheap single-slot/one-K moves, then T moves, then TG moves, then multi-slot/GK kicks; reset after every accepted move and reverse the order temporarily when cheap neighborhoods are exhausted.

**What the sources say.** [SOURCE] Compound moves are a central response to poor coordination; TTP provides concrete examples and incremental costs. [SOURCE] VNS supplies an ordering/reset mechanism, while pair selection must be measured or engineered.

## 5. Q4 — Construction order and placeholders

**Primary source:** Polyakovskiy et al., “A Comprehensive Benchmark Set and Heuristics for the Travelling Thief Problem,” *GECCO* 2014, author PDF [https://www.researchgate.net/publication/261361597_A_Comprehensive_Benchmark_Set_and_Heuristics_for_the_Travelling_Thief_Problem](https://www.researchgate.net/publication/261361597_A_Comprehensive_Benchmark_Set_and_Heuristics_for_the_Travelling_Thief_Problem). [SOURCE] Defining quote: “First, we use the Chained Lin-Kernighan heuristic to quickly construct a good TSP tour. We do this without considering the knapsack part of the TTP problem. Once we have this tour, it remains fixed for the duration of the subsequent optimization.” (Section 4). [SOURCE] Conditions: 9,720 static TTP instances; tour fixed while packing is constructed.

[SOURCE] The same paper reports: “The deterministic constructive heuristic SH … is well suited for very large instances with many items. The reason is that SH quickly constructs a decent packing plan, whereas RLS and EA start from the empty packing plan and then cannot reach SH’s performance within 10 minutes.” (results discussion). [SOURCE] Conditions: 10-minute runs, 30 repetitions for randomized iterative heuristics, varying cities/items/capacity/correlation.

[SOURCE] The benchmark construction balances component scales so near-optimality in one subproblem cannot make the other negligible. [SOURCE] Conditions: TTP benchmark calibration.

**[DERIVED]** A G solution against empty T estimates intrinsic catalogue value but omits T/K-induced thresholds and multipliers. Construct G against a portfolio of incumbent `(T,K)`, diversified `(T,K)` and median-quality `(T,K)`; verify each and retain the best. Three evaluations cost 0.3–0.6 s before local search.

[SOURCE] TTP literature distinguishes constructive, cooperative and full-encoding methods and reports that constructive methods can be strong on large instances because packing is much cheaper than complete coupled search (Namazi et al., Section 3; Polyakovskiy et al.). [SOURCE] No source establishes a universal optimal first component.

**[DERIVED]** Iterated construction is a restart operator: sample a collaborator portfolio, construct one component, derive C, verify, and inject the candidate into the adaptive loop. Ten restarts cost about 1–2 s with one verification each.

**What the sources say.** [SOURCE] Tour-first construction is fast and can be effective for large TTP instances, but it freezes a coupled component. [DERIVED] A small realistic portfolio is a defensible replacement for a single empty placeholder; direct evidence for this exact four-component system is unavailable.

## 6. Q5 — Exact/model-based G sub-solvers

### MMKP formulation

**Primary source:** Renata Mansini and Roberto Zanotti, “A Core-Based Exact Algorithm for the Multidimensional Multiple Choice Knapsack Problem,” *INFORMS Journal on Computing* 32 (2020) 1061–1079, DOI [10.1287/ijoc.2019.0909](https://doi.org/10.1287/ijoc.2019.0909). [SOURCE] Defining quote: “In the multidimensional multiple choice knapsack problem (MMKP), items with nonnegative profits are partitioned into groups. Each item consumes a predefined nonnegative amount of a set of resources with given availability. The problem looks for a subset of items consisting of exactly one item for each group that maximizes the overall profit without violating the resource constraints.” (abstract). [SOURCE] Conditions: exactly one item per group, multiple capacities, nonnegative profits/resources.

[SOURCE] The authors state: “The method exactly solves subproblems of increasing size by means of a recursive variable-fixing process until an optimality condition is satisfied.” They close ten open benchmark instances to optimality and report better solutions in three minutes than Gurobi in one hour. [SOURCE] Conditions: their MMKP benchmark set; not a guarantee for this catalogue.

**[DERIVED]** Encode G choice `x[j,i]∈{0,1}`; enforce `Σ_i x[j,i]=1`, covering sums `Σ a^r_{ji}x[j,i]≥75`, attribute/requirement constraints, rarity limits and incompatibilities. Convert “at least” constraints to solver convention with signs or slack variables.

### Linearizing the simulator

**[DERIVED]** At incumbent `(T0,K0,G0)`, compute baseline `F0` and marginal coefficients `Δji = F(T0,K0,G0 with i in slot j)−F0`. Solve `max Σ Δji xji`, optionally adding pair corrections for strongest measured interactions. Keep hard G constraints exact. Re-derive C and verify every candidate in the original simulator; the surrogate ranks candidates but is not a proof.

[SOURCE] Namazi et al. warn that exact evaluation of one TTP component conditional on the other can be costly and not scale to large problems (pp. 1–2). [SOURCE] Conditions: TTP dynamic-programming/labeling context.

### Trust and verification

[SOURCE] Gurobi’s official warm-start documentation says feasible starts are accepted, infeasible starts may be repaired, failed starts are discarded, and fixing start variables plus an IIS can diagnose infeasibility ([https://doc.gurobi.com/projects/optimizer/en/current/features/warmstart.html](https://doc.gurobi.com/projects/optimizer/en/current/features/warmstart.html)). Defining quote: “If the solution defined by the values you provide is feasible, it is accepted immediately.” (Warm Start Options, “Providing a Feasible Solution”). [SOURCE] Its solution-pool documentation says `PoolSearchMode=2` searches systematically for `n` best solutions and `PoolObjBound` evaluates quality after early termination ([https://docs.gurobi.com/projects/optimizer/en/current/features/solutionpool.html](https://docs.gurobi.com/projects/optimizer/en/current/features/solutionpool.html)). Defining quote: “Setting the parameter to 2 causes the MIP to do a systematic search for the `n` best solutions.” (Solution Pool).

**[DERIVED]** Log solver status, incumbent, bound, gap, wall time, simulator value and feasibility checksum. Accept automatically only when simulator verification improves the incumbent. Timed-out solutions are bounded/heuristic, never exact.

**What the sources say.** [SOURCE] MMKP matches G structurally and exact/recursive methods exist for limited instances. [SOURCE] Official MIP controls provide warm starts, bounded termination and solution pools. [DERIVED] A linearized, warm-started, time-limited G solve is defensible only with simulator verification.

## 7. Q6 — Cross-component constraints

### Deb feasibility rules

**Primary source:** Kalyanmoy Deb, “An Efficient Constraint Handling Method for Genetic Algorithms,” *Computer Methods in Applied Mechanics and Engineering* 186 (2000) 311–338, DOI [10.1016/S0045-7825(99)00389-8](https://doi.org/10.1016/S0045-7825(99)00389-8), PDF [https://repository.ias.ac.in/9407/1/310.pdf](https://repository.ias.ac.in/9407/1/310.pdf). [SOURCE] Defining quote: “When two feasible solutions are compared, the one with better objective function value is chosen, (ii) when one feasible and one infeasible solutions are compared, the feasible solution is chosen, and (iii) when two infeasible solutions are compared, the one with smaller constraint violation is chosen.” (Section 2, p. 2). [SOURCE] Conditions: pairwise tournament selection in population-based GA/EC methods; nine constrained problems, including engineering design; not directly a point-search method.

**[DERIVED]** Compare candidates lexicographically by hard legality, total normalized violation and objective. Assign infinite priority to structural invalidity and normalize threshold deficits so a deficit in one component can be compared with another.

### Stochastic ranking

**Primary source:** Thomas P. Runarsson and Xin Yao, “Stochastic Ranking for Constrained Evolutionary Optimization,” *IEEE Transactions on Evolutionary Computation* 4 (2000) 284–294, DOI [10.1109/4235.873238](https://doi.org/10.1109/4235.873238), PDF [https://faculty.csu.edu.cn/_tsf/00/65/AriuAjbIFJzy.pdf](https://faculty.csu.edu.cn/_tsf/00/65/AriuAjbIFJzy.pdf). [SOURCE] Defining quote: “This paper introduces a novel approach to balance objective and penalty functions stochastically, i.e., stochastic ranking.” (abstract, p. 284). [SOURCE] Conditions: `(μ,λ)` evolution strategy; 13 benchmark problems; ranking probability decides whether objective or violation dominates a comparison.

[SOURCE] The paper reports that adaptive ranking avoids a predefined penalty sequence but pays slightly longer search time (Section III). [DERIVED] Use it only for exploratory infeasible kicks when contractual feasibility must dominate production acceptance.

### Epsilon constraints

**Primary source:** George Mavrotas, “Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems,” *Applied Mathematics and Computation* 213 (2009) 455–465, PDF [https://www.researchgate.net/profile/Mohamed_Mourad_Lafifi/post/What_is_stopping_criteria_of_the_e-constraint_optimization_algorithm_for_multi-objective_optimization_problems/attachment/59d64e0f79197b80779a77a9/AS%3A490975777824768%401494069155557/download/Mavrotas.pdf](https://www.researchgate.net/profile/Mohamed_Mourad_Lafifi/post/What_is_stopping_criteria_of_the_e-constraint_optimization_algorithm_for_multi-objective_optimization_problems/attachment/59d64e0f79197b80779a77a9/AS%3A490975777824768%401494069155557/download/Mavrotas.pdf). [SOURCE] Defining quote: “By parametrical variation in the RHS of the constrained objective functions (εi) the efficient solutions of the problem are obtained.” (Section 2, p. 456). [SOURCE] The paper says ε-constraint can produce non-extreme efficient solutions and is useful for integer and mixed-integer problems (pp. 456–457).

**[DERIVED]** During infeasible exploration solve with thresholds relaxed to `75−εr` or requirement minus ε, then decrease ε geometrically. Verify true constraints before an incumbent can be accepted; each ε level adds a sub-solve.

### Repair operators

**Primary source:** Sancho Salcedo-Sanz, “A survey of repair methods used as constraint handling techniques in evolutionary algorithms,” *Computer Science Review* 3 (2009) 175–192, DOI [10.1016/j.cosrev.2009.07.001](https://doi.org/10.1016/j.cosrev.2009.07.001). [SOURCE] Defining quote: “This paper provides a survey of the most important repair heuristics used in evolutionary algorithms to solve constrained optimization problems.” (abstract). [SOURCE] Conditions: permutation, binary-cardinality, graph/tree and grouping repairs plus hybrid evolutionary/local-search methods.

**[DERIVED]** Repair G by removing the lowest marginal-value item causing an upper-bound violation, adding the highest marginal-value legal item for a failed covering sum, then rechecking all cross-slot constraints. If ties are consequential, branch into two repairs.

**What the sources say.** [SOURCE] Deb supplies feasibility-first comparison; stochastic ranking supplies adaptive objective/violation balance; ε-constraint supplies controlled relaxation; repair supplies problem-specific restoration. [DERIVED] These mechanisms can be layered without turning the simulator objective into an arbitrary penalty.

## 8. Comparison table

| Technique | What it adds over a fixed alternating loop | What it needs | Primary source |
|---|---|---|---|
| Contribution/bandit allocation | [SOURCE] Effort proportional to measured contribution rather than uniform round-robin. | Reward, exploration rule, common cost accounting. | Kazimipour et al. 2019, DOI 10.1016/j.asoc.2018.12.007 |
| Staleness detector | [DERIVED] Joint refresh when isolated progress and cross-effects diverge. | Ages, collaborator snapshots, paired probes. | Namazi et al. 2023, DOI 10.1007/s10732-023-09518-7 |
| TG compound neighborhood | [SOURCE] Changes coupled components during one coordinated move. | Interaction graph, screening, full verification. | Namazi et al. 2023 |
| VND/VNS order | [SOURCE] Changes neighborhoods systematically and resets after descent. | Ordered neighborhoods and cost estimates. | Mladenović & Hansen 1997, DOI 10.1016/S0305-0548(97)00031-2 |
| Realistic collaborator portfolio | [DERIVED] Removes dependence on empty T/K during G construction. | 2–3 representative collaborator states. | Polyakovskiy et al. 2014 |
| Iterated construction | [SOURCE] Re-seeds coupled incumbents before intensification. | Restart budget and archive. | Namazi et al. 2023; Polyakovskiy et al. 2014 |
| Linearized MMKP G solve | [SOURCE] Exact catalogue constraints with approximate objective. | Marginals, MIP, limit, verification. | Mansini & Zanotti 2020, DOI 10.1287/ijoc.2019.0909 |
| MIP starts/solution pool | [SOURCE] Reuses G and quantifies bounded alternatives. | MIP solver and status logging. | Gurobi official documentation |
| Deb rules | [SOURCE] Feasibility-first acceptance without penalty-scale tuning. | Violation metric. | Deb 2000, DOI 10.1016/S0045-7825(99)00389-8 |
| Stochastic ranking | [SOURCE] Balances objective and violation during exploration. | Ranking probability and population. | Runarsson & Yao 2000, DOI 10.1109/4235.873238 |
| ε-constraint | [SOURCE] Controlled path from relaxed to true thresholds. | ε schedule and repeated solves. | Mavrotas 2009 |
| Domain repair | [SOURCE] Restores catalogue/rarity/covering feasibility. | Repair priorities and recheck. | Salcedo-Sanz 2009, DOI 10.1016/j.cosrev.2009.07.001 |
| ATC/MDO pattern | [SOURCE] Explicit coupling snapshots and consistency residuals. | Coupling variables; no discrete convergence guarantee. | Tosserams et al. 2010, DOI 10.1115/1.4001346 |

## 9. Pseudo-code sketches

### Adaptive effort allocation

```text
[DERIVED] arms ← {T, G1..G10, K1..Km, TG, GK}
[DERIVED] initialize pulls[a], reward[a], age[a] for every arm
[DERIVED] incumbent ← verified_initial_solution()
[DERIVED] repeat until budget exhausted:
[DERIVED]   force an unpulled arm; otherwise choose argmax reward[a]/pulls[a] + sqrt(2 ln N/pulls[a])
[DERIVED]   freeze collaborators except a; run a slice until q failures or B[a] evaluations
[DERIVED]   derive C; evaluate candidate with the full simulator
[DERIVED]   gain ← max(0, value(candidate)-value(incumbent))
[DERIVED]   cost ← full_evals + 0.047*what_if_evals
[DERIVED]   reward[a] ← (1−η)reward[a] + η*gain/max(cost,1)
[DERIVED]   update pulls, ages and incumbent using feasibility-first acceptance
[DERIVED]   if stale_pair_detected(): enqueue a joint probe
[DERIVED] return incumbent
```

### One joint move for (T,G)

```text
[DERIVED] choose T segment S and G slots J with largest measured interaction edges
[DERIVED] T1 ← reconnect_or_2opt(T,S); freeze G outside J
[DERIVED] score legal choices in J with 0.007-s what-if deltas
[DERIVED] G1 ← solve_or_repair_J(partial_G, covering, rarity, attributes)
[DERIVED] candidate ← (T1,G1,K); candidate.C ← derive_C(candidate)
[DERIVED] repair candidate if hard legality fails
[DERIVED] reject if cheap screen is below incumbent by a margin
[DERIVED] otherwise evaluate candidate in the full simulator
[DERIVED] accept only if feasible and improving; optionally archive by stochastic ranking
```

### G sub-solve and verification

```text
[DERIVED] freeze T0,K0; compute F0 for incumbent G0
[DERIVED] estimate Δ[j,i] from one-choice what-ifs or cached marginals
[DERIVED] build binary x[j,i] and maximize Σ Δ[j,i] x[j,i]
[DERIVED] add one-choice-per-slot, covering, requirements, rarity and compatibility constraints
[DERIVED] provide G0 as MIP start; set deterministic WorkLimit/NodeLimit
[DERIVED] solve and record status, incumbent, bound, gap and time
[DERIVED] enumerate best candidate and solution-pool alternatives within allowed gap
[DERIVED] derive C for each; reject illegal candidates
[DERIVED] evaluate survivors in the true simulator
[DERIVED] accept only a verified improvement; return certificate and incumbent
```

## 10. Known failure modes and negative results

- **[SOURCE] Isolated optimality misleads.** Mei et al. show the TTP objective is not additively separable; standalone TSP/KP objectives are not directly related to the coupled objective (2016, Sections 2–3).
- **[SOURCE] Alternation can remain poorly coordinated.** Namazi et al. report that frozen collaborators and simple local-search coordination are ineffective (2023, abstract and Section 5).
- **[SOURCE] Uniform effort wastes budget.** Kazimipour et al. identify contribution imbalance as the weakness of round-robin allocation (2019, abstract).
- **[SOURCE] Empty-start search can be dominated by construction.** Polyakovskiy et al. report that RLS/EA from empty packing could not reach SH within ten minutes on very large instances.
- **[SOURCE] Exact coordination may not scale.** Namazi et al. warn that exact dynamic-programming/labeling evaluation can be costly.
- **[SOURCE] Penalty parameters are difficult.** Deb reports generic penalties can be unsatisfactory and require parameter choices.
- **[SOURCE] Stochastic ranking costs adaptation time.** Runarsson & Yao report slightly longer search time for adaptive ranking.
- **[SOURCE] Deb’s method is population-oriented.** Deb notes it is not suitable for classical point-by-point search.
- **[SOURCE] MIP starts can fail or slow a solve.** Gurobi documents rejection of infeasible/poor starts and potentially expensive partial-start completion.
- **[SOURCE] Early MIP termination is not proof.** Use solver status and bounds; a timed-out candidate is heuristic unless a valid bound certifies quality.
- **[DERIVED] Surrogate misranking.** Marginals omit higher-order T–G–K interactions; every accepted G candidate needs true-simulator verification.
- **[DERIVED] Staleness oscillation.** Cap joint refresh probes and decay rewards after failed refreshes.
- **[DERIVED] Joint kicks can destroy feasibility.** Repair and feasibility ordering must precede acceptance; keep the incumbent immutable until verification.
- **[UNVERIFIED]** No opened source supplies a theorem for the optimal component order, universal inner-loop length, or a four-component black-box stale-state detector.

## 11. Cross-question synthesis

[SOURCE] The literature consistently treats interdependent components as a coupled objective rather than a sum of independently optimized objectives. [SOURCE] TTP studies document poor coordination from frozen collaborators, benefits from compound/coordination operators, and strong performance of whole-solution or coordinated methods. [SOURCE] CC studies document contribution imbalance and adaptive allocation. [SOURCE] MMKP/matheuristic work documents exact or bounded sub-solves for one-choice-per-group plus multiple constraints, while official MIP documentation documents warm starts, bounded termination, solution pools and verification. [SOURCE] Constraint-handling literature documents feasibility-first comparison, stochastic ranking, ε-constraint relaxation and repair. [SOURCE] MDO/ATC documents explicit coupling variables under stronger assumptions. [DERIVED] These sources support measuring contribution, refreshing stale collaborators, using joint neighborhoods, embedding a bounded G solve, and verifying every candidate against the original simulator; thresholds and budgets remain empirical for this project.

## 12. All URLs opened

1. https://doi.org/10.1007/s00500-014-1487-2
2. https://doi.org/10.1007/s10732-023-09518-7
3. https://conradsanderson.id.au/pdfs/namazi_solving_ttp_coordination_methods_2023.pdf
4. https://eprints.whiterose.ac.uk/id/eprint/156297/
5. https://doi.org/10.1016/j.asoc.2018.12.007
6. https://doi.org/10.1115/1.4001346
7. https://websites.umich.edu/~mdolaboratory/pdf/Martins2013.pdf
8. https://doi.org/10.1137/120887679
9. https://doi.org/10.1016/S0305-0548(97)00031-2
10. https://staff.fmi.uvt.ro/~daniela.zaharie/am2016/proiecte/tehnici/VNS/originalVNS.pdf
11. https://doi.org/10.1287/ijoc.2019.0909
12. https://doi.org/10.1016/S0045-7825(99)00389-8
13. https://repository.ias.ac.in/9407/1/310.pdf
14. https://doi.org/10.1109/4235.873238
15. https://faculty.csu.edu.cn/_tsf/00/65/AriuAjbIFJzy.pdf
16. https://doi.org/10.1016/j.cosrev.2009.07.001
17. https://www.researchgate.net/profile/Mohamed_Mourad_Lafifi/post/What_is_stopping_criteria_of_the_e-constraint_optimization_algorithm_for_multi-objective_optimization_problems/attachment/59d64e0f79197b80779a77a9/AS%3A490975777824768%401494069155557/download/Mavrotas.pdf
18. https://doc.gurobi.com/projects/optimizer/en/current/features/warmstart.html
19. https://docs.gurobi.com/projects/optimizer/en/current/features/solutionpool.html
20. https://www.researchgate.net/publication/261361597_A_Comprehensive_Benchmark_Set_and_Heuristics_for_the_Travelling_Thief_Problem
21. https://doi.org/10.1016/j.asoc.2021.108013
22. https://doi.org/10.1016/j.cam.2012.12.005
23. https://doi.org/10.1002/9781118897072.ch8
