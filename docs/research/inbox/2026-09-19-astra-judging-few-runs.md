
# Judging and tuning an expensive stochastic optimizer with very few runs

**Evidence convention.** **[SOURCE]** means a primary paper or official documentation page opened during this research, with a short verbatim quotation and conditions. **[DERIVED]** means arithmetic or reasoning from those facts. **[UNVERIFIED]** means a lead not opened sufficiently to support a claim. The attached file was treated as the task instructions.

## 1. Executive summary

1. **Pair by instance and seed; keep common random numbers (CRN).** [SOURCE] The sample-size literature treats instances as blocks and says effective sample size is the number of instances, not repeated-run products. [DERIVED] Reusing seeds costs the current 5 smoke-set or 28 full-campaign machine-hours, while potentially reducing variance of the A-minus-B difference. Measure the realized covariance because divergent trajectories can erase the gain.

2. **Replace a three-seed accept/reject rule with a sequential practical-effect gate.** [SOURCE] Demšar recommends Wilcoxon signed-rank for two methods and notes samples as small as five independent data sets, but those are benchmark blocks, not five stochastic seeds. [DERIVED] With n=3 paired signs, the smallest two-sided exact sign p-value is 0.25; three seeds cannot support a conventional 5% claim. Start at 3, add seeds only for unresolved cases, cap at 10, then escalate to the full 32-instance campaign.

3. **Race candidates and cap clear losers.** [SOURCE] F-Race eliminates candidates once statistically sufficient evidence accumulates; ParamILS adaptive capping stops runs whose partial cost cannot beat the incumbent. [DERIVED] This can save nearly all remaining evaluations of clearly inferior versions; savings depend on observed gaps and valid bounds. The ParamILS project page reports orders-of-magnitude savings in hour-scale applications, an author-reported result rather than a universal guarantee.

4. **Use anytime traces for screening only after validation.** [SOURCE] COCO and IOHprofiler support target-based runtime ECDFs; learning-curve work supports predictive termination when future performance is unlikely to beat the incumbent. [DERIVED] A 25% checkpoint is trustworthy only if historical, held-out complete runs show high ranking correlation, low top-choice error, and calibrated false-elimination rates. No opened source establishes a universal 25% rule for stochastic local search.

5. **Build the six-instance smoke set by feature/footprint coverage and validate it against all 32.** [SOURCE] Instance Space Analysis (ISA) detects benchmark gaps and algorithm footprints. [SOURCE] A SPEC CPU2000 study found an optimal four-benchmark subset at Kendall τ=.95, while random subsets required 14 benchmarks for 95% probability of τ≥.90. [DERIVED] Six instances are defensible only after prospective smoke-vs-full ranking validation; random selection has no such guarantee.

6. **Separate tuning instances from confirmation instances.** [SOURCE] irace defines a tuning phase on representative training instances and a production/testing phase on unseen instances; it uses the same seed for different configurations on an instance. [DERIVED] Freeze the tuned configuration before the 32-instance holdout to detect over-tuning to the smoke set.

7. **Report effect sizes, uncertainty, and anytime distributions.** [SOURCE] Vargha–Delaney A12 measures stochastic superiority for ordinal outcomes; Efron’s bootstrap supplies nonparametric confidence intervals; COCO/IOHprofiler provide ECDFs and time-to-target summaries. [DERIVED] Report paired median/log-ratio differences, instance-level bootstrap CIs, A12, win/tie/loss counts, ranks, performance profiles, and target ECDFs rather than a p-value alone.

8. **Use automatic configuration only with multi-fidelity/capping and a holdout.** [SOURCE] irace, ParamILS, SMAC, GGA, Hyperband, and BOHB all allocate unequal effort adaptively, but each has assumptions and documented failure modes. [DERIVED] A naïve 5,000-evaluation tuning campaign at the current full-run cost is about 1,458 machine-hours; complete-run tuning is infeasible without early stopping or capping.

## 2. Q1 — Comparing two versions with few, expensive runs

### Paired designs and CRN

[SOURCE] Campelo, Takahashi and colleagues, “Sample size calculations for the experimental comparison of multiple algorithms on multiple problem instances,” *Journal of Heuristics* (2020), DOI 10.1007/s10732-020-09454-w, formulate comparisons as a complete-block design. Quote: “Assumption (i) indicates that the variability due to instance effects can be modelled out of our analysis by pairing or blocking” (§2, p. 4). Conditions: all algorithms run on the same sampled instances, and the target is a problem class rather than one fixed instance.

[SOURCE] The same paper warns: “the effective sample size to be considered when testing the hypotheses of interest is the number of instances, rather than the amount of repeated runs” (§2, p. 4). Conditions: inference generalises from the finite instance sample to a wider problem class; treating every seed as an independent problem-class observation is pseudoreplication.

[SOURCE] Yang & Nelson (1991), *Operations Research* 39(4):583–591, DOI 10.1287/opre.39.4.583, study CRN in stochastic simulation comparisons. Quote: “We propose refinements for all three procedures through the use of two variance reduction techniques: common random numbers and control variates” (abstract, p. 583). Conditions: simultaneous interval comparisons of stochastic system designs; CRN is a variance-reduction device, not an unconditional guarantee.

[DERIVED] For paired outputs X_A and X_B, Var(X_B−X_A)=Var(X_A)+Var(X_B)−2Cov(X_A,X_B). If marginal variances are equal and correlation is ρ, CRN changes the paired-difference variance relative to independent runs by the factor 1−ρ. Positive ρ helps; zero ρ does not; negative ρ hurts. This is arithmetic from the variance identity, not a claim that all optimizer trajectories retain positive ρ.

[UNVERIFIED] I found no opened primary study giving a universal “trajectory divergence time” after which CRN ceases to help for construction-plus-local-search metaheuristics. Log covariance by instance, seed, and checkpoint and treat the observed curve as the engineering evidence.

### Non-parametric tests and n=3–10

[SOURCE] Demšar (2006), *JMLR* 7:1–30, recommends: “the Wilcoxon signed ranks test for comparison of two classifiers and the Friedman test with the corresponding post-hoc tests for comparison of more classifiers over multiple data sets” (abstract). Conditions: independent data sets are the sampling units; the Wilcoxon procedure uses paired differences, assumes qualitative commensurability, and has exact small-sample critical values.

[SOURCE] Demšar states: “The sample size can therefore be as small as five and is usually well below 30” (§3, p. 5). Conditions: “sample size” means independent data sets, not repeated stochastic runs on one data set. He reports an N=14 worked Wilcoxon example and exact tables through N=25.

[SOURCE] Demšar also says the Wilcoxon test “does not assume normal distributions” and can be more powerful than a t-test when t assumptions fail (§3.1.3, pp. 7–8). Conditions: continuous, unrounded paired differences; ties reduce power.

[SOURCE] Bartz-Beielstein et al. (2020), *Benchmarking in Optimization: Best Practice and Open Issues*, caution: “Similar to the median, they require a certain amount of data points and are probably meaningless for small data” (§6.2.2, p. 23). Conditions: medians and quantiles used as descriptive summaries of stochastic runs.

[DERIVED] For n=3 paired signs, an all-positive two-sided exact sign test has p=2(1/2)^3=.25. For n=5 it is .0625; n=6 gives .03125. Thus n=3 cannot yield a conventional two-sided α=.05 sign result, even with no ties. The same discreteness makes exact Wilcoxon evidence weak at n=3.

[DERIVED] A defensible smoke policy is: three common seeds for every candidate/instance; compute paired effects and intervals; add seeds only where the interval overlaps the practical-equivalence band or the sign is unstable; stop at a predeclared maximum (for example, 10) or a confidence-width target. [DERIVED] The six-instance smoke set costs 5 hours for three seeds, about 0.28 hours per extra seed; 3→10 seeds costs about 1.94 additional hours. The full campaign costs about 9.33 hours per extra seed (28/3).

### Ratios, ranks, profiles, ECDFs, and A12

[SOURCE] Bartz-Beielstein et al. describe performance profiles as “the cumulative distribution function of a performance metric … [using] the ratio of a performance metric obtained by each algorithm versus the best value” (§6.2.3, p. 23). Conditions: a defensible best-known/reference value is needed when the true optimum is unknown; profiles do not directly answer fixed-evaluation-budget success.

[SOURCE] Vargha & Delaney (2000), DOI 10.3102/10769986025002101, define A12 for ordinal data. Quote: “the A measure of stochastic superiority … may be directly applied for any discrete or continuous variable that is at least ordinally scaled” (abstract). Conditions: exact point/interval estimation and tests of A=.5 are supplied; correlated-sample generalisations are discussed.

[SOURCE] Efron (1987), JASA 82:171–185, DOI 10.1080/01621459.1987.10478410, develops bootstrap confidence intervals. Quote: “The bootstrap confidence intervals discussed in this article automatically incorporate such tricks … at the price of a considerable increase in computational effort” (abstract). Conditions: approximate intervals for parameters in nonparametric and parametric settings; accuracy is statistic- and sample-size-dependent.

[SOURCE] Hansen et al. (2016), “COCO: Performance Assessment,” arXiv:1605.03560, aggregate time-to-target data with restarts, averages and ECDFs. Quote: “The performance assessment is based on runtimes measured in number of objective function evaluations to reach one or several quality indicator target values” (abstract). Conditions: black-box numerical optimization and predeclared target values.

[SOURCE] Official IOHprofiler documentation states: “it is recommended to aggregate ECDFs over multiple target” (IOHanalyzer GUI, ECDF section). Conditions: iterative optimization heuristics, multiple functions/targets and runtime-to-target observations.

[DERIVED] Use per-instance log ratios against the fixed reference, then aggregate the paired instance effects with a median and an instance bootstrap. Report ranks and profiles as sensitivity analyses; do not average raw scores across heterogeneous scales unless the reference and estimand justify that weighting.

**What the sources say.** [SOURCE] Instances are the independent blocks; paired non-parametric tests, effect sizes, profiles and ECDFs are robust descriptive/inferential tools. [SOURCE] CRN can reduce variance through positive covariance but is not guaranteed once trajectories diverge. [SOURCE] n=3 is a screening sample, not a defensible confirmatory sample for a conventional two-sided claim.

## 3. Q2 — Sequential and adaptive experimentation

### Racing

[SOURCE] Birattari, Stützle, Paquete & Varrentrapp, “A Racing Algorithm for Configuring Metaheuristics,” GECCO 2002, primary PDF, define F-Race as incremental evaluation. Quote: “we propose a procedure that empirically evaluates a set of candidate configurations by discarding bad ones as soon as statistically sufficient evidence is gathered against them” (abstract, p. 11). Conditions: candidate configurations are evaluated on a sequence of instance blocks; F-Race uses a non-parametric Friedman test and then pairwise comparisons.

[SOURCE] The same paper says: “The elimination of inferior candidates, speeds up the procedure and allows a more reliable evaluation of the promising ones” (§3.1, p. 3). Conditions: equal candidate exposure within each block, independent blocks, and a total computation budget; the race stops when one candidate remains or the budget is exhausted (§3.1–3.2).

[SOURCE] López-Ibáñez et al. (2016), irace, define iterated racing and give N_iter=floor(2+log2 N_param). Quote: “Iterated racing starts by estimating the number of iterations … N_iter = floor(2 + log2 N_param)” (§3.2, p. 47). Conditions: encoded parameter space, target runner, training instances and total budget.

[SOURCE] irace’s elitist variant states: “elite configurations are not eliminated from the race unless the new configurations have been evaluated on at least T_new + e instances” (§3.4, p. 49). Conditions: protects incumbents from unlucky short races but can reduce exploration.

### Sequential tests and fixed-budget best-arm identification

[UNVERIFIED] Wald’s 1945 sequential probability-ratio test is the classical source, but the opened bibliographic record was not machine-readable enough to quote boundary equations safely. Verify the original paper before implementation.

[SOURCE] Audibert, Bubeck & Munos (2010), “Best Arm Identification in Multi-Armed Bandits,” primary PDF, analyse fixed-budget Successive Rejects. Quote: “We show that these algorithms are essentially optimal since their regret decreases exponentially at a rate which is, up to a logarithmic factor, the best possible” (abstract). Conditions: stochastic arms, fixed total sample budget; the stated complexity result assumes a unique best arm.

[SOURCE] They state: “identifying the best arm (when it is unique) requires a number of samples of order (up to a log(K) factor) Σ_i 1/Δ_i²” (abstract, p. 1). Conditions: K arms and gaps Δ_i between the best mean and each suboptimal mean.

[SOURCE] Hyperband (Li et al., 2016/2018), arXiv:1603.06560, frames multi-fidelity tuning as pure exploration. Quote: “we focus on speeding up random search through adaptive resource allocation and early-stopping” (abstract). Conditions: a resource that can be increased for a configuration, finite total budget, and the loss-sequence regularity assumptions in §4.

[DERIVED] A safe two-version sequential gate needs a practical margin δ, a confidence sequence or alpha-spending rule, and n_max. After each paired seed, stop for benefit if the lower bound exceeds δ, for practical equivalence if the interval is inside [−δ,+δ], and for regression if the upper bound is below −δ. Ordinary fixed-sample p-values cannot be repeatedly peeked at without correction.

[DERIVED] For k candidates, allocate one common seed per surviving candidate and instance, eliminate a candidate when its multiplicity-adjusted bound is worse than the incumbent by δ, and give extra runs only to overlapping survivors. This is an implementation pattern derived from F-Race and Successive Rejects; exact error guarantees depend on the chosen confidence-sequence construction.

**What the sources say.** [SOURCE] Racing is explicitly an early-elimination design; Successive Rejects supplies fixed-budget, gap-dependent guarantees; Hyperband supplies multi-fidelity guarantees only under its model assumptions. [UNVERIFIED] No opened source gives a turnkey distribution-free sequential test for paired medians with n=3–10 stochastic optimizer seeds.

## 4. Q3 — Anytime traces and partial runs

[SOURCE] COCO says its assessment “is based on runtimes measured in number of objective function evaluations to reach one or several quality indicator target values” (Hansen et al. 2016, abstract). Conditions: black-box numerical optimization and predeclared targets.

[SOURCE] IOHanalyzer computes “the empirical cumulative distribution function of the running time … for target values specified by the user” (official GUI documentation, ECDF section). Conditions: multiple runs per function and target; aggregate ECDFs pool target/run pairs.

[SOURCE] Eggensperger et al. (2015), IJCAI, distinguish predictive termination from overfitting stopping. Quote: “we predict validation performance and terminate a run when it is unlikely to beat the performance of the best model we have encountered so far” (§2.2, p. 2). Conditions: DNN validation-accuracy learning curves, model-based extrapolation and an incumbent.

[SOURCE] The same paper says: “the goal behind our new predictive termination criterion is different” from ordinary early stopping (§2.2, p. 2). Conditions: future-performance prediction with uncertainty; results concern DNN HPO, not combinatorial local-search trajectories.

[UNVERIFIED] Freeze-Thaw Bayesian Optimization (Swersky, Snoek & Adams, 2014) is the primary pause/resume learning-curve method, but I did not use quantitative claims because the opened abstract did not expose experimental tables.

[DERIVED] Store best-so-far values at q∈{.10,.25,.50,.75,1.00} of the budget and time-to-target for predeclared relative targets. Validate each checkpoint on historical complete runs: per-instance Spearman ρ and Kendall τ between partial and final rankings, top-1 agreement, inversion rate, and bootstrap CIs over held-out instances/code changes. Calibrate a stop rule against the false-elimination rate. A checkpoint can be trusted for discarding obvious losers without being trusted for the final ranking.

**What the sources say.** [SOURCE] COCO/IOHprofiler support target-based anytime distributions; learning-curve work supports model-based termination. [DERIVED] The trustworthy checkpoint is the earliest one that passes an out-of-sample ranking and calibration test. No universal 25% fraction was found.

## 5. Q4 — Representative instance subsets

[SOURCE] Smith-Miles & Muñoz (2023), “Instance Space Analysis for Algorithm Testing,” ACM Computing Surveys 55(12), DOI 10.1145/3572895, state: “ISA … offers a more nuanced understanding of the unique strengths and weaknesses of algorithms across different regions of the instance space” (abstract). Conditions: feature vectors for instances, performance metadata and algorithm footprints; no fixed subset size is promised.

[SOURCE] ISA’s workflow collects instance features and algorithm performance, constructs a feature space, predicts selection, generates footprints, analyses gaps, and adds instances/features where needed (§3). Conditions: feature quality and representative metadata are prerequisites.

[SOURCE] Vandierendonck & De Bosschere, “Experiments with Subsetting Benchmark Suites” (2005), evaluate SPEC CPU2000 subsets by ranking 340 computers. Quote: “A representative subset ranks all computers in the same order as the full benchmark suite” (§3.2). Conditions: 26 benchmarks, Kendall τ representativeness, computer-performance ranking target.

[SOURCE] Their concrete results: “A 1-benchmark optimal subset has a representativeness of 0.88 and a subset of 4 benchmarks already has a representativeness of 0.95” (§4.1.1); “Fourteen benchmarks … are necessary to reach the 0.9 level … with a probability of 95%” (same section). Conditions: SPEC CPU2000, not this optimizer’s instance class.

[SOURCE] They warn: “the subset may be very inaccurate … it is always necessary to validate that the subset is representative” (§4.1.3). Conditions: clustering/PCA subset methods can be good at some sizes and bad at others.

[DERIVED] Select six smoke instances using normalized structural features, clustering/medoids and boundary/footprint coverage; include at least one instance per feature cluster and one per region where variants disagree. Validate prospectively by running a historical panel on all 32 instances and checking smoke-vs-full τ/ρ and top-choice error. If validation fails, enlarge or redesign the smoke set.

[UNVERIFIED] No opened primary study reports a universal subset size preserving rankings for a 32-instance, heterogeneous stochastic construction-plus-local-search optimizer.

**What the sources say.** [SOURCE] ISA is a framework for diagnosing benchmark diversity and footprints; subsetting studies show that small subsets can work but random/unvalidated choices can fail. [SOURCE] The reported four/11/14-instance numbers are domain-specific evidence, not a guarantee that six instances suffice here.

## 6. Q5 — Automatic configuration under a tiny budget

### irace and F-Race

[SOURCE] López-Ibáñez et al. (2016), *Operations Research Perspectives* 3:43–58, DOI 10.1016/j.orp.2016.09.002, define the goal as: “The immediate goal of automatic algorithm configuration is to find, automatically, the best parameter settings of an optimizer” (§1, p. 44). Conditions: encoded parameter space, representative training instances, target runner and total budget.

[SOURCE] Their worked scenario sets `maxExperiments` to 5,000 target-algorithm runs and a 20-second cutoff per run (example, p. 51). Conditions: illustrative configuration, not a minimum; effort scales with parameters, instances and runtime.

[SOURCE] irace documents a soft restart to avoid collapsed sampling distributions. Quote: “The soft-restart mechanism in irace checks for premature convergence” (§3.3, p. 48). Conditions: distributions can converge to near-identical candidates, wasting remaining budget.

[SOURCE] The elitist variant warns: “The described elitist strategy often results in a faster convergence to good parameter values, which has the disadvantage of reducing the exploration of new alternative configurations” (§3.4, p. 50). Conditions: elite retention protects incumbents but can reduce diversity.

### ParamILS and capping

[SOURCE] Hutter, Hoos, Leyton-Brown & Stützle (2009), “ParamILS,” JAIR 36:267–306, DOI 10.1613/jair.2861, introduce adaptive capping. Quote: “adaptive capping … [avoids] unnecessary runs of the algorithm to be configured by developing bounds on the performance measure to be optimized” (§4, p. 277). Conditions: a running incumbent and a valid bound from partial runtime/score.

[SOURCE] The paper’s trajectory-preserving example terminates a candidate when its partial accumulated runtime proves that even a best-case completion cannot beat the incumbent (§4.1.1). Conditions: additive runtime/score bounds; aggressive capping is heuristic and may change the search trajectory.

[SOURCE] The official ParamILS page says that for hour-scale applications adaptive capping “often reduces the required configuration budget by several orders of magnitude.” Conditions: author-maintained software statement; savings depend on gaps and valid bounds.

### SMAC, GGA, Hyperband and BOHB

[SOURCE] SMAC’s published algorithm iterates “between learning a new model, selecting new configurations based on the model and performing additional runs to compare these selected configurations against the incumbent” (Hutter, Hoos & Leyton-Brown, LION-5 2011, Algorithm 1). Conditions: configuration space, instance set, cost metric and total time budget.

[SOURCE] Ansótegui, Sellmann & Tierney (2009), GGA, state: “We propose a robust, inherently parallel genetic algorithm for the problem of configuring solvers automatically” (CP 2009 abstract). Conditions: expensive SAT-solver fitness evaluations; gender separation changes selection pressure to preserve diversity.

[SOURCE] Hyperband’s abstract reports: “Hyperband can provide over an order-of-magnitude speedup over our competitor set” (Li et al., 2016/2018). Conditions: meaningful resource levels and informative early performance; guarantees use the paper’s loss-sequence assumptions.

[SOURCE] Falkner, Klein & Hutter (2018), BOHB, say: “we propose to combine the benefits of both Bayesian optimization and bandit-based methods” (ICML abstract). Conditions: many evaluations, a fidelity axis and enough observations for model fitting; experiments are HPO benchmarks rather than arbitrary local-search traces.

[DERIVED] At the stated full-campaign cost, 5,000 complete evaluations cost approximately 5,000×28/96=1,458 machine-hours; 500 cost about 146 hours. Therefore configuration needs multi-fidelity traces, capping or a much smaller candidate budget. None of these systems implies that three complete runs per candidate reliably tune 30 knobs.

[SOURCE] irace documents unlucky early-instance elimination and reduced exploration under elitism; ParamILS distinguishes trajectory-preserving and aggressive capping; Hyperband assumes informative fidelity. [DERIVED] The project’s dominant failure mode is over-tuning the six smoke instances, so every tuning campaign needs an unseen confirmation split.

**What the sources say.** [SOURCE] Automatic configuration systems save work by racing, modelling, capping and multi-fidelity allocation; they require a training distribution and have known exploration/elimination risks. [DERIVED] For 30–60 minute evaluations, safe capping and checkpoint racing should precede broad model-based tuning.

## 7. Q6 — Reporting standards for “B is better than A”

[SOURCE] Bartz-Beielstein et al. (2020) enumerate eight essentials: “clearly stated goals, well-specified problems, suitable algorithms, adequate performance measures, thoughtful analysis, effective and efficient designs, comprehensible presentations, and guaranteed reproducibility” (abstract). Conditions: optimization benchmarking, including stochastic and multi-problem experiments.

[SOURCE] Johnson (2002), DIMACS 059, DOI 10.1090/dimacs/059/11, lists ten principles including: “Use instance testbeds that can support general conclusions,” “Ensure reproducibility,” “Ensure comparability,” “Report the full story,” and “Draw well-justified conclusions” (§Introduction, p. 3). Conditions: experimental algorithm analysis across implementations, instances, metrics and environments.

[SOURCE] Johnson warns: “many randomized algorithms can also yield widely-varying results for the same instance. Thus it can be dangerous to infer too much from a single run on a single instance” (p. 18). Conditions: randomized algorithms and finite testbeds.

[SOURCE] Hooker (1995), “Testing Heuristics: We Have It All Wrong,” *Journal of Heuristics* 1:33–42, DOI 10.1007/BF02430364, writes: “Competitive testing tells us which algorithm is faster but not why” (abstract). Conditions: horse-race studies where polished code and benchmark choice can hide causal understanding.

[SOURCE] Campelo & Takahashi et al. (2020) state: “The number of instances is determined based on the desired sensitivity … for the detection of effects larger than a predefined minimally relevant effect size (MRES)” (Conclusion, p. 24). Conditions: planned power, family-wise confidence, and frequentist sample-size design; Wilcoxon extensions use asymptotic relative efficiency.

[DERIVED] A claim “B is better than A” must predeclare the target population (the 32-instance family), estimand (median per-instance ratio, mean log ratio, target-attainment time, or another stated quantity), practical margin δ, pairing/seed policy, stopping rule, number of instances/runs, failure handling, and holdout result. Report effects and intervals, not only p-values.

[DERIVED] Because multiple code changes, checkpoints, metrics and subsets compete for the same machine, register the candidate list and primary estimand before final outcomes, or label post-hoc comparisons exploratory. Use Holm or another family-wise correction for several versions versus a common incumbent.

[SOURCE] Bartz-Beielstein et al. distinguish strict computational reproducibility from broader scientific reproducibility. Quote: “the classical understanding of reproducibility in computer science … differs substantially from the understanding in other experimental sciences” (§9, p. 33). [DERIVED] Archive revision, compiler/runtime, CPU, seeds, instance hashes, checkpoints, logs and analysis scripts; independently rerun important claims.

[SOURCE] The sample-size paper notes that conventional practice often uses “arbitrarily-set numbers of repeated runs, usually 30 or 50” (§1, p. 2), and warns against treating repeated runs as independent instances. [DERIVED] Use a precision/MRES target instead of an arbitrary run count.

[SOURCE] Johnson criticises giving a heuristic a known optimum and stopping when it reaches it, because deployment normally lacks that information (§8, pp. 17–18). [DERIVED] Use blind fixed budgets or deployment-available targets, not hidden reference optima, for early stopping.

**What the sources say.** [SOURCE] Guidance converges on explicit goals, representative testbeds, paired/blocked designs, effect sizes and uncertainty, full reporting, and reproducibility. [SOURCE] Hooker and Johnson warn that benchmark horse races can be fragile and non-explanatory. [DERIVED] The current three-seed smoke median is an appropriate screening signal, not a complete confirmatory claim.

## 8. Practice matrix

| Practice | What it saves or improves | What it needs (runs, assumptions) | Primary source |
|---|---|---|---|
| Pair instances and seeds; CRN | [DERIVED] Removes instance-level noise and can reduce paired-difference variance; same run count as today | Same instance/seed pairs; measure covariance | [SOURCE] Campelo & Takahashi et al. 2020; Yang & Nelson 1991, DOI [10.1287/opre.39.4.583](https://doi.org/10.1287/opre.39.4.583) |
| Sequential practical-effect gate | [DERIVED] Avoids full confirmation for clearly worse/better changes | δ, confidence sequence/alpha spending, n_max; starts at n=3 but usually continues | [SOURCE] Wald 1945; Campelo & Takahashi et al. 2020 |
| F-Race / iterated racing | [SOURCE] Eliminates weak candidates before all instance evaluations | Blocked instances, multiplicity control, candidate pool, budget | [SOURCE] Birattari et al. 2002; López-Ibáñez et al. 2016 |
| Adaptive capping | [SOURCE] Stops partial runs that cannot beat incumbent | Valid lower/upper bounds; aggressive mode may change trajectory | [SOURCE] Hutter et al. 2009 ParamILS |
| Anytime checkpoint racing | [DERIVED] Discards obvious losers before full budget | Historical ranking/crossing validation and calibration | [SOURCE] Hansen et al. 2016 COCO; Eggensperger et al. 2015 |
| Feature/footprint smoke subset | [DERIVED] Keeps routine smoke cost near 5 h instead of 28 h if ranking is preserved | Instance features and full-vs-smoke validation | [SOURCE] Smith-Miles & Muñoz 2023; Vandierendonck & De Bosschere 2005 |
| A12 + bootstrap CI | [SOURCE] Adds scale-free stochastic superiority and uncertainty | Independent instance blocks; small n yields wide intervals | [SOURCE] Vargha & Delaney 2000; Efron 1987 |
| Train/holdout split | [DERIVED] Detects over-tuning to smoke instances | Frozen training set, unseen confirmation set | [SOURCE] López-Ibáñez et al. 2016; Bartz-Beielstein et al. 2020 |
| ECDF/time-to-target | [SOURCE] Shows anytime and target-attainment behaviour | Predeclared targets and comparable runtime units | [SOURCE] Hansen et al. 2016; IOHprofiler docs |

## 9. Pseudo-code sketches

### 9.1 Paired sequential comparison of two versions

```text
[DERIVED] INPUT A,B; instances I; initial common seeds S0; margin δ; n_max; α
[DERIVED] for each instance i:
[DERIVED]     run A and B on every seed in S0; store paired differences d[i,s]
[DERIVED]     while n < n_max:
[DERIVED]         estimate Δ_i and CI_i by paired bootstrap over seeds
[DERIVED]         if CI_i.lower > δ: label BENEFIT; break
[DERIVED]         if CI_i.upper < -δ: label REGRESSION; break
[DERIVED]         if CI_i ⊂ [-δ,δ]: label EQUIVALENT; break
[DERIVED]         add one common seed; run A and B; append d[i,s]
[DERIVED]     aggregate instance effects with a predeclared paired procedure
[DERIVED]     update a confidence sequence or alpha-spending boundary
[DERIVED]     if global lower bound > δ: return ACCEPT_B
[DERIVED]     if global upper bound < -δ: return REJECT_B
[DERIVED]     if global interval ⊂ [-δ,δ]: return PRACTICAL_EQUIVALENCE
[DERIVED] return UNDECIDED; escalate to full campaign
```

### 9.2 Racing over k versions

```text
[DERIVED] INPUT versions V; ordered/stratified instances I; common seeds S; margin δ; budget B
[DERIVED] survivors ← V; observations ← ∅
[DERIVED] for i in I while budget remains and |survivors| > 1:
[DERIVED]     choose one common seed s; run every survivor on (i,s)
[DERIVED]     update blocked estimates and bounds versus incumbent
[DERIVED]     eliminate v when its multiplicity-adjusted bound is worse by δ
[DERIVED]     allocate extra seeds only to survivors whose bounds overlap
[DERIVED]     randomise future instances within feature strata
[DERIVED] return incumbent, survivors, bounds, and consumed budget
```

### 9.3 Validate partial-run ranking prediction

```text
[DERIVED] INPUT historical complete traces; checkpoints Q={.10,.25,.50,.75,1.0}
[DERIVED] split by code change/instance family into train and holdout
[DERIVED] for q in Q except 1.0:
[DERIVED]     for held-out instance i:
[DERIVED]         rank versions at q·budget and at full budget
[DERIVED]         record Spearman/Kendall, top-1 agreement, inversion rate
[DERIVED]     bootstrap instances for CIs; fit P(partial winner = final winner)
[DERIVED] choose earliest q whose lower CI passes the predeclared threshold
[DERIVED] validate q on a later untouched batch of code changes
[DERIVED] during live racing, stop only when calibrated P(beating incumbent) < p_stop
[DERIVED] if no q passes, use traces descriptively and require full runs
```

## 10. Known failure modes and negative results

- [SOURCE] **Pseudoreplication:** treating runs or instance×run products as independent can make nominal confidence levels arbitrarily anti-conservative (Campelo & Takahashi et al. 2020, §2).
- [DERIVED] **n=3 discreteness:** the smallest two-sided sign p-value is .25.
- [SOURCE] **Median instability:** medians/quantiles are “probably meaningless for small data” (Bartz-Beielstein et al. 2020, §6.2.2).
- [DERIVED] **CRN failure:** covariance near zero gives no variance reduction; negative covariance increases paired variance.
- [SOURCE] **Racing false elimination:** irace documents a good configuration discarded after only five unlucky instances (§3.2).
- [SOURCE] **Premature convergence:** irace says collapsed sampling distributions waste budget on near-identical configurations (§3.3).
- [SOURCE] **Elitism/exploration tradeoff:** irace reports faster convergence with reduced exploration (§3.4).
- [SOURCE] **Aggressive capping trajectory change:** ParamILS separates trajectory-preserving from heuristic aggressive capping.
- [DERIVED] **Partial-curve crossing:** a fixed early-rank rule fails when curves cross; validate crossing empirically.
- [SOURCE] **Unvalidated benchmark reduction:** subsetting can be inaccurate for some sizes and must be validated (Vandierendonck & De Bosschere).
- [SOURCE] **Benchmark overfitting:** fixed standard suites can be tuned to and fail to generalise (Bartz-Beielstein et al. 2020; Campelo & Takahashi et al. 2020).
- [SOURCE] **Known-optimum stopping bias:** Johnson criticises stopping a heuristic using an optimum unavailable in deployment.
- [DERIVED] **Multiplicity:** several versions, checkpoints, metrics and subsets create many opportunities for a favourable result; predeclare the primary estimand and correct or label exploratory analyses.

## 11. URLs opened

1. [Bartz-Beielstein et al. 2020 PDF](https://cavalab.org/assets/papers/Bartz-Beielstein%20et%20al.%20-%202020%20-%20Benchmarking%20in%20Optimization%20Best%20Practice%20and%20Op.pdf)
2. [Bartz-Beielstein et al. arXiv](https://arxiv.org/abs/2007.03488)
3. [Hooker 1995 PDF](https://sci2s.ugr.es/keel/pdf/specific/articulo/hoo95.pdf)
4. [Hooker DOI](https://doi.org/10.1007/BF02430364)
5. [Demšar 2006 PDF](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf)
6. [Johnson 2002 PDF](https://web.cs.dal.ca/~eem/gradResources/A-theoreticians-guide-to-experimental-analysis-of-algorithms-2001.pdf)
7. [Johnson DOI](https://doi.org/10.1090/dimacs/059/11)
8. [Campelo & Takahashi et al. 2020](https://link.springer.com/article/10.1007/s10732-020-09454-w)
9. [Yang & Nelson 1991](https://doi.org/10.1287/opre.39.4.583)
10. [Vargha & Delaney 2000](https://doi.org/10.3102/10769986025002101)
11. [Efron 1987](https://doi.org/10.1080/01621459.1987.10478410)
12. [Birattari et al. 2002 F-Race PDF](https://groups.csail.mit.edu/EVO-DesignOpt/pb/uploads/Site/racing.pdf)
13. [Audibert, Bubeck & Munos 2010](https://chercheurs.lille.inria.fr/~munos/papers/files/ABM10.pdf)
14. [Hyperband](https://arxiv.org/abs/1603.06560)
15. [irace 2016 PDF](https://iridia.ulb.ac.be/~mbiro/paperi/LopDubPer-etal2016orp.pdf)
16. [ParamILS technical report](https://ml.informatik.uni-freiburg.de/wp-content/uploads/papers/09-TR-ParamILS.pdf)
17. [ParamILS official page](https://www.cs.ubc.ca/labs/algorithms/Projects/ParamILS/)
18. [SMAC official page](https://www.cs.ubc.ca/labs/algorithms/Projects/SMAC/)
19. [SMAC paper](https://www.cs.ubc.ca/labs/algorithms/Projects/SMAC/papers/11-LION5-SMAC.pdf)
20. [GGA 2009 PDF](https://citeseerx.ist.psu.edu/document?doi=997dd6c2d49f6d89a4f9b28729163dc18549f3d3&repid=rep1&type=pdf)
21. [BOHB 2018 PDF](https://aad.informatik.uni-freiburg.de/wp-content/uploads/papers/18-ICML-BOHB.pdf)
22. [COCO Performance Assessment](https://arxiv.org/abs/1605.03560)
23. [IOHprofiler GUI documentation](https://iohprofiler.github.io/IOHanalyzer/GUI/)
24. [ISA DOI](https://doi.org/10.1145/3572895)
25. [Vandierendonck & De Bosschere](https://www.researchgate.net/publication/4146527_Experiments_with_subsetting_benchmark_suites)
26. [Eggensperger et al. 2015 PDF](https://www.ijcai.org/Proceedings/15/Papers/487.pdf)
27. [Eiben & Smit 2011 PDF](https://www.cs.vu.nl/~gusz/papers/2011-Eiben-Smit-EA-parameters-and-their-tuning.pdf)
