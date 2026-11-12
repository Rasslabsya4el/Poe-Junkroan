# Multi-fidelity screening of designs

## Executive summary

[SOURCE] The project searches 20–200 categorical designs with SCREEN, MEDIUM, and FULL evaluations and five parallel workers. The local architecture uses a cheap screen followed by top-K full optimization; D71 records three seeds per finalist.

[DERIVED] Recommended first production policy: asynchronous three-rung promotion with a protected exploration quota, a screen-to-full validation gate, and adaptive seed racing.

- SCREEN: evaluate every candidate once.
- MEDIUM: promote roughly 20–35% of screens; reserve 10–20% of medium slots for late-bloomer and underrepresented-archetype exploration.
- FULL: promote roughly 3–4 designs, then give each two seeds.
- SEEDS: spend remaining full-run budget where confidence intervals overlap or variance is high.
- Keep 10–15% of wall time as queue/process reserve.

[SOURCE] SHA/Hyperband allocate more resource to promising configurations; ASHA removes rung barriers. Jamieson and Talwalkar report a non-stochastic best-arm method that makes no convergence-curve assumptions and can be an order of magnitude faster than uniform allocation (2016, abstract, https://proceedings.mlr.press/v51/jamieson16.html).

[SOURCE] ASHA quote: “ASHA promotes configurations to the next rung whenever possible instead of waiting for a rung to complete before proceeding to the next rung” (Li et al., 2020, Section 3.2, p. 3, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf).

[SOURCE] Hyperband quote: “Hyperband attacks this trade-off by trying different n values for a fixed budget” (Optuna official documentation, https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html).

[SOURCE] Best-arm, OCBA, and knowledge-gradient methods allocate repeated noisy evaluations using gaps, variance, or value of information (Audibert et al., 2010, https://www.microsoft.com/en-us/research/publication/best-arm-identification-multi-armed-bandits/; Chen et al., 2000, https://doi.org/10.1023/A:1008349927281; Frazier et al., 2008, https://doi.org/10.1137/070693424).

[DERIVED] Example for 100 designs: 100 three-minute screens take about 60 wall minutes on five workers; 12 medium runs at 12.5 minutes take about 30 minutes; six 45-minute full seeds take about 90 minutes. Total is about 180 minutes before overhead. At 200 designs, screening alone is about 120 minutes.

## Research question and decision

[DERIVED] The decision is whether to replace “screen once, keep top two, run three full seeds each” with a budgeted multi-fidelity scheduler that can preserve late bloomers, exploit related design structure, and spend repeats where they can change the winner.

[SOURCE] Local project context opened: docs/ARCHITECTURE.md, docs/DECISIONS.md, and docs/REQUEST.md.

[UNVERIFIED] The brief’s stated 40% median seed spread was treated as a planning input; it was not independently re-estimated in this review.

## Q1. Multi-fidelity and bandit formulations

### Successive halving

[SOURCE] SHA evaluates n configurations at a low resource, retains approximately 1/eta, raises the resource by eta, and repeats. The ASHA paper gives n_i=floor(n eta^-i), r_i=r eta^(i+s), and requires minimum resource, maximum resource, reduction factor, and early-stopping rate (Li et al., 2020, Algorithm 1, pp. 2–3, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf).

[SOURCE] Hyperband treats iterations, data, or features as resources and says its analysis adapts to unknown convergence rates (Li et al., 2018, pp. 1–2, https://www.jmlr.org/papers/volume18/16-558/16-558.pdf).

[SOURCE] Defining quote: “we make no assumptions on the convergence behavior of the arms’ losses” (Jamieson & Talwalkar, 2016, abstract, https://proceedings.mlr.press/v51/jamieson16.html).

[DERIVED] Equal-count promotion is not equal-cost here because SCREEN, MEDIUM, and FULL durations differ substantially. Every rank rule must also enforce a worker-minute budget.

### Hyperband

[SOURCE] Hyperband runs multiple SHA brackets with different starting resource/configuration counts to hedge the trade-off between breadth and depth (Li et al., 2018, https://www.jmlr.org/papers/volume18/16-558/16-558.pdf).

[SOURCE] Optuna documents bracket count as floor(log_reduction(max_resource/min_resource))+1 and warns that with TPE each bracket needs more than ten trials before TPE adapts (https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html).

[DERIVED] With only three semantic fidelities and tens of evaluations, begin with one calibrated ASHA bracket plus exploration rather than many Hyperband brackets.

### ASHA

[SOURCE] ASHA does not require a pre-specified number of configurations, but retains SHA’s resource, reduction-factor, and early-stopping inputs. It promotes completed candidates when possible and otherwise grows the bottom rung (Li et al., 2020, Algorithm 2, p. 4, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf).

[SOURCE] The paper says synchronous SHA is sensitive to stragglers and dropped jobs. It also says ASHA incurs some incorrect early promotions and argues their fraction vanishes as configuration count grows (Section 3.3).

[DERIVED] That is not a finite-sample guarantee for 20 candidates. Require a minimum rung cohort, retain exploration slots, and reserve wall time.

### Best-arm and top-k identification

[SOURCE] Audibert, Bubeck and Munos show that successive rejects has exponentially decreasing error up to logarithmic factors and requires order sum_i 1/Delta_i^2 samples for a unique best arm, where Delta_i is the mean gap (abstract, https://www.microsoft.com/en-us/research/publication/best-arm-identification-multi-armed-bandits/).

[SOURCE] Bubeck, Wang and Viswanathan extend successive accepts/rejects to identify the top m arms (abstract, https://proceedings.mlr.press/v28/bubeck13.html).

[SOURCE] These results concern repeated stochastic samples from fixed arms at one fidelity and do not model a biased cheap proxy.

[DERIVED] Use SHA/ASHA across fidelities and best-arm/top-k racing only among candidates already evaluated at a common fidelity.

### BOHB

[SOURCE] Falkner, Klein and Hutter combine Bayesian configuration selection with Hyperband and report strong anytime performance across diverse benchmark classes (abstract, https://proceedings.mlr.press/v80/falkner18a.html).

[SOURCE] The ASHA paper describes BOHB as Bayesian configuration sampling combined with SHA early stopping (Li et al., 2020, pp. 4–5, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf).

[DERIVED] BOHB is a later option after pooled history exists; with tens of observations, keep random and uncertainty-based exploration.

### What the sources say

[SOURCE] SHA and Hyperband provide resource allocation with limited assumptions on exact curves. ASHA removes synchronization but permits some mispromotion. Best-arm/top-k methods address noisy ranking at a common fidelity. BOHB adds model-based proposals but needs enough observations.

## Q2. Biased cheap fidelity, late bloomers, promotion, and correlation

### Fidelity relation

[SOURCE] Kandasamy et al. describe low fidelity as cheaper and less accurate and say its purpose is to guide search toward the optimum (2017, pp. 0–1, https://proceedings.mlr.press/v70/kandasamy17a/kandasamy17a.pdf).

[SOURCE] Defining quote: “one may use cheap low fidelity experiments ... to discard bad hyper-parameters and deploy expensive high fidelity experiments ... only in a small but promising region” (Kandasamy et al., 2017, pp. 0–1).

[SOURCE] The paper says a uniform bound between high and low fidelity is restrictive because an approximation can be good in some regions and poor in others; BOCA instead models the fidelity relation.

[UNVERIFIED] No opened primary source supplied a universal minimum Spearman/Kendall correlation that prevents late-bloomer loss for arbitrary engineering optimizers.

[DERIVED] Measure top-tail recall, not only global rank correlation. A proxy can have moderate global correlation while missing the true top two.

### Promotion fraction

[SOURCE] Hyperband explicitly hedges the choice between many short evaluations and fewer long evaluations (Li et al., 2018, https://www.jmlr.org/papers/volume18/16-558/16-558.pdf).

[SOURCE] ASHA reports that aggressive early stopping worked well in its empirical tasks but says the appropriate rate is problem-dependent (Li et al., 2020, Section 2).

[DERIVED] Start with eta=3. Replay history at q=0.2, 0.33, and 0.5; choose the largest q whose lower confidence bound on top-2 recall meets the team’s tolerated miss probability. Reserve 10–20% of medium slots for exploration.

### Correlation sample size

[UNVERIFIED] No opened primary source gave a validated n=10–40 rule for screen-to-final Spearman/Kendall intervals in this engineering setting.

[DERIVED] Use paired observations, request-cluster bootstrap intervals, Spearman rho, Kendall tau, top-2 recall, top-5 recall, and interval width. Treat n=10 as diagnostic; n=20 as conservative-vs-aggressive evidence; n=40 as a possible default-setting sample only if strata are stable.

[DERIVED] Fisher-z arithmetic gives only a warning scale: 1/sqrt(n-3) is approximately 0.378 at n=10, 0.243 at n=20, and 0.164 at n=40 before a critical-value multiplier. This is not an exact finite-sample Spearman interval.

### What the sources say

[SOURCE] The literature supports measuring or modelling the low/high relationship but provides no project-independent correlation threshold or universal small-sample rule. Hyperband hedges promotion-rate uncertainty; ASHA handles promotion asynchronously.

## Q3. Sharing information across related designs

[SOURCE] SMAC targets algorithm configuration and its project page says it scales to high-dimensional and discrete input spaces (https://www.cs.ubc.ca/labs/algorithms/Projects/SMAC/).

[SOURCE] SMAC3 exposes a random-forest model, Hamming kernel, and multi-fidelity Hyperband facade (https://automl.github.io/SMAC3/main/advanced_usage/2_multi_fidelity/).

[SOURCE] Garrido-Merchan and Hernandez-Lobato warn that “GPs assume continous input variables” and show naive one-hot/rounding can fail (arXiv:1805.03463, abstract and Sections 1–3, https://arxiv.org/abs/1805.03463).

[SOURCE] Mes, Powell and Frazier use categorical/numerical features and hierarchical aggregation. Quote: “This approach greatly reduces the measurement effort required, but it requires some prior knowledge on the smoothness of the function in the form of an aggregation function” (JMLR abstract, https://jmlr.org/beta/papers/v12/mes11a.html).

[SOURCE] Bergstra et al. introduce conditional response-surface models for hyperparameter optimization (NeurIPS 2011, https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization).

[DERIVED] With tens of observations, start with pooled random forests or TPE as proposal aids, not a high-capacity GP over integer-encoded categories. Include archetype, mode, optional components, fidelity, and seed statistics. Validate transfer with leave-one-request-out replay.

[UNVERIFIED] The opened literature did not establish how much transfer is useful for this PoB design space.

### What the sources say

[SOURCE] Categorical random forests, categorical-aware kernels, and hierarchical KG can share structure, but require pooled data or a validated similarity prior. Small-data transfer must be tested retrospectively.

## Q4. Noise at top fidelity

[SOURCE] Chen et al. formulate simulation performance as an expectation estimated by sample means with variance estimated from replications and present sequential OCBA allocation (2000, DOI https://doi.org/10.1023/A:1008349927281; full text https://www.researchgate.net/publication/30845808_Simulation_Budget_Allocation_for_Further_Enhancing_the_Efficiency_of_Ordinal_Optimization).

[SOURCE] Their paper says more budget should go to designs critical for identifying good designs and suggests 5–20 initial replications in the cited simulation practice.

[SOURCE] Frazier, Powell and Dayanik define KG as maximizing expected information value per measurement and establish one-period and asymptotic results under an independent-normal ranking model (https://doi.org/10.1137/070693424).

[SOURCE] Audibert et al. show best-arm sample complexity depends on inverse squared gaps (https://www.microsoft.com/en-us/research/publication/best-arm-identification-multi-armed-bandits/).

[DERIVED] Give 3–4 finalists two full seeds each. Allocate additional seeds to the finalist with the largest uncertainty relative to its gap from the current leader. Stop when top-k intervals are separated for two allocations or the budget is exhausted. Preserve every seed value so “best observed” is not confused with estimated mean.

[UNVERIFIED] Independence/correlation of this project’s seeds was not established by the opened sources.

### What the sources say

[SOURCE] OCBA, KG, and BAI allocate repeats using variance, gaps, or value of information under explicit stochastic assumptions. They do not eliminate the need to estimate variance and retain replication data.

## Q5. Parallel asynchronous scheduling

[SOURCE] ASHA is designed to mitigate stragglers and promote on completion rather than waiting for a rung (Li et al., 2020, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf).

[SOURCE] Syne Tune separates tuner, scheduler, and backend; the backend starts/stops/pauses/resumes subprocess trials and relays metrics. Its local backend is documented as having very small start/stop/resume delays (https://syne-tune.readthedocs.io/en/latest/tutorials/basics/concepts.html).

[DERIVED] PoB stages are non-preemptible, so implement three separate jobs: SCREEN, MEDIUM, FULL. A completed screen immediately fills a free worker with a promotion or a new screen; a completed medium fills a worker with a full promotion or protected exploration medium. Keep 10–15% wall-time reserve.

[UNVERIFIED] Exact Windows/PoB process-launch and scheduler overhead was not measured.

### What the sources say

[SOURCE] ASHA is the supported pattern for heterogeneous evaluation time and stragglers. The exact best policy for five non-preemptible PoB workers remains an engineering calibration problem.

## Q6. Open-source implementations usable from Python

| Implementation | Source-backed capability/licence | Derived integration | Limitation |
|---|---|---|---|
| Optuna | HyperbandPruner/SHAPruner; trial.report + trial.should_prune; MIT. Docs: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html; licence: https://github.com/optuna/optuna/blob/master/LICENSE | One trial per design; report at fidelity boundaries; prune before next expensive job; JournalStorage/RDB for workers | Exact Windows overhead unmeasured |
| Ray Tune | ASHA support in paper; Apache-2.0 repository: https://github.com/ray-project/ray/blob/master/LICENSE | Report at stage boundaries; configure metric, max_t, grace_period, reduction_factor | Current Windows details unverified |
| SMAC3 | Multi-fidelity Hyperband/SHA, Hamming kernel, RF; BSD-3-Clause: https://github.com/automl/SMAC3; docs: https://automl.github.io/SMAC3/main/advanced_usage/2_multi_fidelity/ | Target receives ConfigSpace configuration plus budget | Package metadata declares platforms=["Linux"] |
| Syne Tune | ASHA and local subprocess backend; Apache-2.0: https://syne-tune.readthedocs.io/en/latest/getting_started.html | Report stage metric and map stage to resource | Windows support/overhead unverified |

[SOURCE] Optuna’s FAQ says n_jobs uses threads and does not overcome the GIL for ordinary Python code; multiprocessing should use JournalStorage or RDB, and SQLite can produce lock errors under concurrency (https://optuna.readthedocs.io/en/latest/faq.html).

[DERIVED] Start with a project-owned queue because the solver has only three non-preemptible stages. Add Optuna when persistent studies/storage are valuable. Defer SMAC3 on Windows until an installation spike.

## Technique comparison table

| Technique | What it adds | Assumptions | Evaluations needed | Primary source |
|---|---|---|---|---|
| SHA | Early promotion through rungs | Comparable scalar at increasing resource | One screen each; enough cohort | Jamieson & Talwalkar 2016, https://proceedings.mlr.press/v51/jamieson16.html |
| Hyperband | Multiple keep fractions/brackets | Same resource sequence; bounded budget | More trials; TPE needs >10 per bracket | Li et al. 2018, https://www.jmlr.org/papers/volume18/16-558/16-558.pdf |
| ASHA | No rung barrier; straggler tolerance | Rung comparability; some mispromotion | Minimum cohorts prudent | Li et al. 2020, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf |
| BOHB/TPE | Categorical proposals from history | Enough pooled observations | Tens are startup | Falkner et al. 2018, https://proceedings.mlr.press/v80/falkner18a.html |
| Successive rejects | Fixed-budget best-arm race | Fixed stochastic arms and gaps | Order sum 1/Delta_i^2 up to logs | Audibert et al. 2010, https://www.microsoft.com/en-us/research/publication/best-arm-identification-multi-armed-bandits/ |
| Top-k accepts/rejects | Direct top-k identification | Fixed-arm stochastic ranking | More repeats near boundary | Bubeck et al. 2013, https://proceedings.mlr.press/v28/bubeck13.html |
| BOCA/MF-GP | Models design x fidelity | GP and smooth fidelity relation | Paired cross-fidelity data | Kandasamy et al. 2017, https://proceedings.mlr.press/v70/kandasamy17a/kandasamy17a.pdf |
| Trace-aware KG | Fidelity value-of-information | Trace observations and Bayesian model | Sequential trace samples | Wu et al. 2020, https://proceedings.mlr.press/v115/wu20a.html |
| OCBA | Adaptive extra seeds | Means/variances and stochastic alternatives | Initial repeats plus increments | Chen et al. 2000, https://doi.org/10.1023/A:1008349927281 |
| Knowledge gradient | Next seed by information value | Bayesian ranking model | One repeat per decision | Frazier et al. 2008, https://doi.org/10.1137/070693424 |
| SMAC3 RF/Hamming | Categorical sharing | ConfigSpace/model fit | Pooled history | https://automl.github.io/SMAC3/main/advanced_usage/2_multi_fidelity/ |
| Hierarchical KG | Shares common features | Smoothness/aggregation prior | Validate with pooled history | Mes et al. 2011, https://jmlr.org/beta/papers/v12/mes11a.html |

## Pseudo-code sketches

### Asynchronous schedule

[DERIVED]

~~~text
inputs: designs D, workers=5, budgets=(SCREEN, MEDIUM, FULL)
rungs = {SCREEN: [], MEDIUM: [], FULL: []}
deadline = wall_limit * 0.85
while now < deadline and (unseen(D) or queued() or running()):
    while free_worker() and budget_left():
        if promotable(FULL): job = pop_best(FULL)
        elif promotable(MEDIUM): job = pop_best(MEDIUM)
        elif exploration_slot(): job = choose_exploration_medium()
        else: job = next_unseen_design_at(SCREEN)
        launch(job.design, job.fidelity, seed=job.seed)
    e = wait_for_any_completion()
    record(e.design, e.fidelity, e.value, e.seed, e.elapsed)
    if e.fidelity == SCREEN and (rank_gate(e) or exploration_slot()):
        enqueue(e.design, MEDIUM)
    if e.fidelity == MEDIUM and medium_gate(e):
        enqueue(e.design, FULL, seed=1)
return best_full_by_mean_and_confidence()
~~~

### Adaptive seed allocation

[DERIVED]

~~~text
for finalist in finalists:
    run_seed(finalist, 1)
    run_seed(finalist, 2)
while remaining_full_runs > 0:
    stats = online_mean_variance_and_count(finalists)
    leader = argmax(stats.mean)
    for finalist in finalists:
        priority[finalist] = sqrt(stats.var[finalist]/stats.n[finalist]) /
                             max(epsilon, abs(stats.mean[leader]-stats.mean[finalist]))
    finalist = argmax(priority)
    run_seed(finalist, next_seed(finalist))
    remaining_full_runs -= 1
    if top_k_intervals_separated_for_two_rounds(): break
return rank_by_mean_with_lower_bound_tiebreak()
~~~

### Screen-to-final rank check

[DERIVED]

~~~text
paired = history.rows_with(screen, final)
for scope in [all, archetype, mode, request]:
    x, y = paired[scope].screen, paired[scope].final
    rho, tau = spearman(x,y), kendall_tau(x,y)
    ci = request_cluster_bootstrap(paired[scope], statistic=(rho,tau), reps=5000)
    recall2 = fraction(final_top2(row) in screen_top20pct(row))
    recall5 = fraction(final_top5(row) in screen_top20pct(row))
    report(scope, len(x), rho, tau, ci, recall2, recall5)
if n >= 20 and lower_ci(recall2) >= 0.80 and lower_ci(rho) > 0:
    enable_aggressive_promotion()
else:
    use_conservative_keep_fraction_and_exploration()
~~~

## Known failure modes and negative results

[SOURCE] Older early-stopping methods can require strong convergence assumptions; SHA/Hyperband were designed to avoid those assumptions (Li et al., 2020, p. 1).

[SOURCE] Synchronous SHA is sensitive to stragglers/dropped jobs; ASHA allows some incorrect promotions and gives an asymptotic rather than small-sample argument (Li et al., 2020, pp. 3–4).

[SOURCE] Optuna warns about Hyperband/TPE startup dilution and SQLite concurrency problems (Optuna docs and FAQ).

[SOURCE] Naive one-hot/rounding for categorical Gaussian processes can fail (Garrido-Merchan & Hernandez-Lobato, https://arxiv.org/abs/1805.03463).

[DERIVED] A screen can omit a component only discovered by full optimization; no scheduler recovers an unreserved late bloomer. Selecting the best observed seed is optimistically biased, so retain all seeds. A changed solver invalidates old screen/full calibration. Worker-minute savings can still create a serial final tail; replay the queue with recorded durations.

[UNVERIFIED] The opened sources did not establish seed independence, exact Windows overhead, or a universal small-n correlation cutoff.

## Recommended implementation sequence

[DERIVED] 1. Persist request_id, design_id, fidelity, seed, value, duration, status, and feature snapshot.
[DERIVED] 2. Implement a project-owned asynchronous queue with three stages, five workers, minimum rung cohorts, a 10–15% wall reserve, and a 10–20% exploration quota.
[DERIVED] 3. Replay history with request-cluster bootstrap and report rank correlation plus top-tail recall by archetype.
[DERIVED] 4. Start conservatively: medium 12–20% of screens, full 3–4 designs, two seeds each, then race additional seeds.
[DERIVED] 5. Fall back to the existing top-two/three-seed policy when paired history is insufficient.
[DERIVED] 6. Add Optuna persistence or a pooled categorical surrogate only after retrospective validation.
[DERIVED] 7. Recalibrate after solver or league changes.

## All URLs opened

- https://proceedings.mlr.press/v51/jamieson16.html
- https://proceedings.mlr.press/v51/jamieson16.pdf
- https://www.jmlr.org/papers/volume18/16-558/16-558.pdf
- https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf
- https://arxiv.org/abs/1810.05934
- https://proceedings.mlr.press/v80/falkner18a.html
- https://www.microsoft.com/en-us/research/publication/best-arm-identification-multi-armed-bandits/
- https://chercheurs.lille.inria.fr/~munos/papers/files/ABM10.pdf
- https://proceedings.mlr.press/v28/bubeck13.html
- https://proceedings.mlr.press/v28/bubeck13.pdf
- https://proceedings.mlr.press/v70/kandasamy17a/kandasamy17a.pdf
- https://arxiv.org/abs/1703.06240
- https://proceedings.mlr.press/v115/wu20a.html
- https://jmlr.org/beta/papers/v12/mes11a.html
- https://epubs.siam.org/doi/abs/10.1137/070693424?journalCode=sjcodc
- https://doi.org/10.1023/A:1008349927281
- https://www.researchgate.net/publication/30845808_Simulation_Budget_Allocation_for_Further_Enhancing_the_Efficiency_of_Ordinal_Optimization
- https://arxiv.org/abs/1805.03463
- https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization
- https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html
- https://optuna.readthedocs.io/en/latest/faq.html
- https://optuna.readthedocs.io/en/latest/tutorial/10_key_features/004_distributed.html
- https://github.com/optuna/optuna
- https://github.com/optuna/optuna/blob/master/LICENSE
- https://automl.github.io/SMAC3/main/advanced_usage/2_multi_fidelity/
- https://github.com/automl/SMAC3
- https://github.com/automl/SMAC3/blob/main/setup.py
- https://syne-tune.readthedocs.io/en/latest/tutorials/basics/concepts.html
- https://syne-tune.readthedocs.io/en/latest/getting_started.html
- https://github.com/ray-project/ray/blob/master/LICENSE
- https://docs.ray.io/en/master/tune/api/doc/ray.tune.schedulers.ASHAScheduler.html
