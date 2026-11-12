# Research: Rebuild-Dependent Choices

[DERIVED] The relevant objective has the form:

\[
F(z)=\min_{x\in X(z)} f(z,x)
\]

where `z` is an outer discrete choice, such as a keystone or unique, and `x` is the complete build selected after that choice. A greedy one-change score evaluates `f(z, x_0)` rather than `F(z)`.

[DERIVED] The central distinction in the sources is between:

- [DERIVED] solving or approximating the inner optimization separately for each outer choice;
- [DERIVED] amortizing the inner optimization through shared parameters, predictors, or a reusable super-network;
- [DERIVED] screening candidates with a cheaper fidelity and promoting only some to the full evaluation.

[UNVERIFIED] None of the academic sources opened provides a universal test that proves a cheap, unreconstructed evaluation will preserve the ranking of arbitrary coupled choices.

## 1. Bilevel / Two-Stage Optimization

### 1.1 Exact bilevel programming

**Mechanism**

[DERIVED] Treat the outer choice and the rebuilt configuration as two linked optimization levels: optimize the outer variable while constraining the inner variable to be optimal for that outer choice.

[DERIVED] For a discrete outer choice, the direct black-box interpretation is one inner optimization per outer candidate; exact cost is therefore approximately `number of outer candidates × cost of inner solve`, unless inner state or evaluations can be reused.

[SOURCE] Primary source: Luca Franceschi, Paolo Frasconi, Saverio Salzo, Riccardo Grazzi, Massimiliano Pontil, 2018, *Bilevel Programming for Hyperparameter Optimization and Meta-Learning*, PMLR. Published 3 July 2018.  
URL: <https://proceedings.mlr.press/v80/franceschi18a.html>

[SOURCE] Defining passage:

> “We introduce a framework based on bilevel programming that unifies gradient-based hyperparameter optimization and meta-learning.”

[SOURCE] The same abstract states:

> “We show that an approximate version of the bilevel problem can be solved by taking into explicit account the optimization dynamics for the inner objective.”

[SOURCE] Conditions stated by the authors:

> “We provide sufficient conditions under which solutions of the approximate problem converge to those of the exact problem.”

[SOURCE] The paper’s application is supervised hyperparameter optimization and meta-learning, with the inner problem represented by iterative optimization dynamics. The abstract does not give a universal numerical evaluation budget or candidate-count threshold.

[DERIVED] In the requested setting, an exact outer comparison of `K` coupled choices requires either `K` full rebuilds or an equivalent exact reuse mechanism. The source does not describe a shortcut that makes an arbitrary discrete outer candidate free.

### 1.2 Truncated inner optimization and hypergradients

**Mechanism**

[DERIVED] Replace the exact inner optimum with a finite optimization trajectory, an implicit approximation, or a truncated reverse/forward differentiation calculation.

[DERIVED] The outer candidate is judged using the result of an incomplete inner solve, so cost is reduced from “converge the inner optimizer for every outer point” to repeated partial inner updates plus derivative calculations.

[SOURCE] Primary source: Franceschi et al., 2017, *Forward and Reverse Gradient-Based Hyperparameter Optimization*, PMLR. Published 17 July 2017.  
URL: <https://proceedings.mlr.press/v70/franceschi17a.html>

[SOURCE] Defining passage:

> “We study two procedures (reverse-mode and forward-mode) for computing the gradient of the validation error with respect to the hyperparameters of any iterative learning algorithm such as stochastic gradient descent.”

[SOURCE] Conditions stated by the authors:

> “These procedures mirror two ways of computing gradients for recurrent neural networks and have different trade-offs in terms of running time and space requirements.”

[SOURCE] The experiments concern image and phone classification tasks, where the inner learning algorithm is iterative stochastic-gradient training. No claim is made that the method applies unchanged to a non-differentiable discrete build evaluator.

[DERIVED] This family is naturally suited to continuous or differentiable outer variables. It does not directly provide an exact method for categorical choices whose effects are exposed only after a separate combinatorial rebuild.

### 1.3 DARTS: continuous relaxation of a structural choice

**Mechanism**

[DERIVED] Relax a discrete architecture choice into continuous mixture weights, jointly maintain shared model weights, and update the structural variables using validation performance.

[DERIVED] DARTS avoids independently solving the inner problem for every discrete architecture by using one shared continuous model during search, then discretizes and retrains the selected architecture.

[SOURCE] Primary source: Hanxiao Liu, Karen Simonyan, Yiming Yang, 2019, *DARTS: Differentiable Architecture Search*, ICLR 2019. arXiv v1 posted 24 June 2018; v2 revised 23 April 2019.  
URL: <https://arxiv.org/html/1806.09055v2>

[SOURCE] Defining passage:

> “This implies a bilevel optimization problem with α as the upper-level variable and w as the lower-level variable.”

[SOURCE] Their formal problem is:

> “minα Lval(w*(α),α) s.t. w*(α)=argminw Ltrain(w,α)”

[SOURCE] Approximation passage:

> “The idea is to approximate w*(α) by adapting w using only a single training step, without solving the inner optimization completely by training until convergence.”

[SOURCE] Conditions and failure information:

> “While we are not currently aware of the convergence guarantees for our optimization algorithm, in practice it is able to reach a fixed point with a suitable choice of ξ.”

[SOURCE] Cost conditions reported by the authors include a CIFAR-10 search cost of 1.5 GPU-days for first-order DARTS and 4 GPU-days for second-order DARTS, compared with 2,000 GPU-days for NASNet and 3,150 GPU-days for AmoebaNet. The source also reports a 1 GPU-day recurrent search cost on PTB.

[SOURCE] The paper evaluates the selected architecture again from scratch. It states that weights learned during search are discarded for final architecture evaluation.

[DERIVED] DARTS is an example of an approximate bilevel solve whose cheapness comes from relaxing the outer discrete space and sharing inner weights. Its source does not establish that the ranking of the relaxed choices is reliable for every discrete, highly coupled domain.

### 1.4 ENAS: parameter sharing across many inner problems

**Mechanism**

[DERIVED] Embed many candidate architectures as subgraphs of one larger graph and share their parameters, so candidate evaluations reuse a common set of inner weights.

[DERIVED] The search signal is a validation reward under shared weights; the chosen architecture is later retrained from scratch, so the search score is a proxy rather than the final exact score.

[SOURCE] Primary source: Hieu Pham, Melody Guan, Barret Zoph, Quoc V. Le, Jeff Dean, 2018, *Efficient Neural Architecture Search via Parameter Sharing*, ICML 2018.  
URL: <https://proceedings.mlr.press/v80/pham18a.html>  
Additional primary version: <https://arxiv.org/html/1802.03268v2>

[SOURCE] Defining passage:

> “ENAS constructs a large computational graph, where each subgraph represents a neural network architecture, hence forcing all architectures to share their parameters.”

[SOURCE] Cost passage:

> “Sharing parameters among child models allows ENAS to deliver strong empirical performances, whilst using much fewer GPU-hours than existing automatic model design approaches, and notably, 1000x less expensive than standard Neural Architecture Search.”

[SOURCE] Conditions reported by the authors:

> “In all of our experiments, for which we use a single Nvidia GTX 1080Ti GPU, the search for architectures takes less than 16 hours.”

[SOURCE] The PTB experiment uses approximately 10 hours on one GTX 1080Ti GPU. The CIFAR-10 experiments report 0.32 GPU-days for macro search and 0.45 GPU-days for micro-cell search.

[SOURCE] The search spaces are very large: approximately \(10^{15}\) recurrent models in one experiment and approximately \(1.6\times10^{29}\) convolutional models in another.

[SOURCE] The authors explicitly state the limitation:

> “The idea has apparent complications, as different child models might utilize their weights differently.”

[SOURCE] Architecture selection condition:

> “For each sampled model, we compute its reward on a single minibatch sampled from the validation set.”

[SOURCE] The selected model is then retrained from scratch. The paper says training all sampled models from scratch could improve results but would be less economical.

[DERIVED] ENAS demonstrates amortized inner optimization across a very large structural space. Its failure mode is precisely that the shared inner state may not represent the individually optimized state of every candidate.

### 1.5 Approximate versus exact bilevel results

[SOURCE] DARTS reports both the benefit and the cost of approximation:

> “Evaluating the architecture gradient exactly can be prohibitive due to the expensive inner optimization.”

[SOURCE] DARTS also reports that a simple joint optimization alternative performed poorly:

> “The resulting best convolutional cell … yielded 4.16 ± 0.16% test error using 3.1M parameters, which is worse than random search.”

[DERIVED] The sources therefore distinguish three different approximations rather than treating them as equivalent:

- [DERIVED] truncated inner dynamics, as in Franceschi et al. and DARTS;
- [DERIVED] shared inner parameters, as in ENAS;
- [DERIVED] relaxed outer variables, as in DARTS.

[DERIVED] None of these approximations is an exact “change one choice and rebuild the complete deterministic game build” operation.

**What the sources say**

[DERIVED] Bilevel systems model the rebuild explicitly, but practical AutoML systems reduce cost by truncating the inner solve, relaxing the outer choice, or sharing inner state across candidates; the source-assigned conditions determine whether those approximations are credible.

## 2. Cheap Proxies and Surrogates

### 2.1 Multi-fidelity Bayesian optimization

**Mechanism**

[DERIVED] Evaluate candidates at cheaper fidelities, such as fewer iterations, fewer data points, or smaller validation samples, then use a surrogate and an acquisition rule to decide which candidates and fidelities deserve more resources.

[DERIVED] A full evaluation remains the target fidelity; cheap observations are useful only to the extent that they predict that target.

[SOURCE] Primary source: Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, Andrew Gordon Wilson, 2020, *Practical Multi-fidelity Bayesian Optimization for Hyperparameter Tuning*, PMLR. Published 6 August 2020.  
URL: <https://proceedings.mlr.press/v115/wu20a.html>

[SOURCE] Defining passage:

> “Multi-fidelity optimization promises relief using cheaper proxies to such objectives — for example, validation error for a network trained using a subset of the training points or fewer iterations than required for convergence.”

[SOURCE] Method passage:

> “We introduce a new acquisition function, the trace-aware knowledge-gradient, which efficiently leverages both multiple continuous fidelity controls and trace observations.”

[SOURCE] Conditions attached by the authors:

> “Our approach [is] focused on efficiently optimizing hyperparameters for iteratively trained supervised learning models.”

[SOURCE] The experiments cover deep neural networks and large-scale kernel learning. The source does not state a universal minimum fidelity or a candidate-count break-even point.

[DERIVED] The source’s predictive signal is not merely the cheap score itself. It is the surrogate’s inferred value of a cheap observation for the high-fidelity objective, including information from traces across increasing fidelities.

### 2.2 Learning-curve and trace information

**Mechanism**

[DERIVED] Record a sequence of partial evaluations for the same candidate and use the shape of that sequence to predict its eventual full-budget result.

[DERIVED] Candidates can be promoted based on predicted terminal performance rather than raw early performance, and previously paid-for partial work can be reused.

[SOURCE] Wu et al. state:

> “We introduce a new acquisition function, the trace-aware knowledge-gradient, which efficiently leverages both multiple continuous fidelity controls and trace observations.”

[SOURCE] They also specify that the method supports fidelity controls such as training size, validation size, and training iterations, with iterative evaluations producing a sequence of observations.

[SOURCE] The source contrasts information value across fidelities:

> “The entire value of sampling a low fidelity is the information provided about the highest fidelity.”

[SOURCE] Conditions include iterative training, available traces, and a fidelity-cost model. The source does not give a fixed candidate-count threshold at which the method stops paying off.

[DERIVED] For a deterministic build search, an analogous signal would require a cheap evaluation whose trajectory contains information about the rebuilt optimum, not merely about the current build. The sources do not establish such a trajectory for passive trees, gear, supports, or configuration switches.

### 2.3 Hyperband and low-fidelity screening

**Mechanism**

[DERIVED] Start many candidates with a small resource budget, discard the worst fraction, multiply the resource for survivors, and repeat until a small number reach full fidelity.

[DERIVED] Hyperband runs multiple successive-halving brackets because the useful trade-off between candidate count and initial resource is unknown.

[SOURCE] Primary source: Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh, Ameet Talwalkar, 2018, *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization*, JMLR.  
URL: <https://arxiv.org/html/1603.06560>  
PDF URL: <https://www.jmlr.org/papers/volume18/16-558/16-558.pdf>

[SOURCE] Defining passage:

> “Our procedure, Hyperband, relies on a principled early-stopping strategy to allocate resources, allowing it to evaluate orders-of-magnitude more configurations than black-box procedures like Bayesian optimization methods.”

[SOURCE] Successive-halving passage:

> “Uniformly allocate a budget to a set of hyperparameter configurations, evaluate the performance of all configurations, throw out the worst half, and repeat until one configuration remains.”

[SOURCE] Conditions attached by the source:

> “Hyperband requires two inputs (1) R, the maximum amount of resource that can be allocated to a single configuration, and (2) η, an input that controls the proportion of configurations discarded in each round of SuccessiveHalving.”

[SOURCE] The source reports \(R=81\), \(\eta=3\), five brackets, and 70 trials in the LeNet experiment. It reports 5x to 30x speedups over Bayesian-optimization competitors across its benchmark suite.

[SOURCE] The source states the key ranking condition:

> “More resources are needed to differentiate between the two configurations when either (1) the envelope functions are wider or (2) the terminal losses are closer together.”

[DERIVED] Hyperband’s “fidelity” is useful when the candidate’s intermediate performance is related to its terminal performance. In the requested setting, a cheap one-change score can be a poor fidelity if the chosen outer option changes which inner search region is favorable.

### 2.4 BOHB: surrogate-guided Hyperband

**Mechanism**

[DERIVED] Combine Hyperband’s resource allocation with a Bayesian model that proposes candidates, while retaining high-fidelity evaluations as the most reliable observations.

[DERIVED] BOHB uses low budgets to explore and high budgets to refine, but its low-budget work creates overhead when it does not improve the model.

[SOURCE] Primary source: Stefan Falkner, Aaron Klein, Frank Hutter, 2018, *BOHB: Robust and Efficient Hyperparameter Optimization at Scale*, ICML 2018.  
URL: <https://proceedings.mlr.press/v80/falkner18a.html>

[SOURCE] Defining passage:

> “We propose to combine the benefits of both Bayesian optimization and bandit-based methods, in order to achieve the best of both worlds: strong anytime performance and fast convergence to optimal configurations.”

[SOURCE] Fidelity condition:

> “With the maximum budget b = bmax, f̃(·, bmax) = f(·), whereas with b < bmax, f̃(·, b) is only an approximation whose quality typically increases with b.”

[SOURCE] Experimental scale:

> “We ran BOHB with budgets of 22, 66, 200, and 600 epochs, using 19 parallel workers.”

[SOURCE] The full-budget run in that experiment took approximately seven hours on two GPUs per worker. The complete 16-iteration run used 33 GPU-days, described by the authors as less than three full function evaluations per worker.

[SOURCE] The authors state a failure mode:

> “Traditional BO methods can still have an advantage for very large budgets, since in these late stages of the optimization process the low fidelity evaluations of BOHB can cause a constant overhead without any gain.”

[SOURCE] They also report that BOHB struggles in very high-dimensional cases because larger budgets are needed to build a good model and the low-budget evaluations then add overhead.

[DERIVED] BOHB reduces the number of expensive full evaluations, not necessarily the cost of constructing a valid rebuilt candidate. Its benefit depends on a fidelity parameter that remains informative about the full rebuilt objective.

### 2.5 MFES-HB: modeling biased low fidelities

**Mechanism**

[DERIVED] Fit separate surrogates to observations at different fidelities, then combine them with a weighted ensemble rather than treating low-fidelity scores as unbiased full-fidelity labels.

[DERIVED] The ensemble gives more influence to fidelity levels that empirically approximate the target better.

[SOURCE] Primary source: Yang Li, Yu Shen, Jiawei Jiang, Jinyang Gao, Ce Zhang, Bin Cui, 2021, *MFES-HB: Efficient Hyperband with Multi-Fidelity Quality Measurements*, AAAI. Published 18 May 2021.  
URL: <https://ojs.aaai.org/index.php/AAAI/article/view/17031>

[SOURCE] Defining passage:

> “Designing MFES-HB is not trivial as the low-fidelity measurements can be biased yet informative to guide the configuration search.”

[SOURCE] Method passage:

> “Thus we propose to build a Multi-Fidelity Ensemble Surrogate (MFES) based on the generalized Product of Experts framework, which can integrate useful information from multi-fidelity measurements effectively.”

[SOURCE] Conditions and scale:

> “The empirical studies on the real-world AutoML tasks demonstrate that MFES-HB can achieve 3.3-8.9x speedups over the state-of-the-art approach — BOHB.”

[SOURCE] The source’s condition is real-world AutoML tasks with multiple fidelity measurements. It does not state a universal candidate count or a full-evaluation cost ratio.

[DERIVED] MFES-HB is directly relevant to a setting where a cheap evaluation is systematically biased but still correlated with the final verdict. It does not remove the need to validate the fidelity relationship.

### 2.6 Shared-weight proxies and their failure mode

[SOURCE] ENAS gives the positive claim:

> “Sharing parameters among child models allows ENAS to deliver strong empirical performances.”

[SOURCE] ENAS also gives the qualification:

> “The idea has apparent complications, as different child models might utilize their weights differently.”

[SOURCE] OFA gives a related failure mode:

> “Randomly sampling a few sub-networks in each step will lead to significant accuracy drops.”

[DERIVED] These sources disagree only in emphasis, not in mechanism: shared representations can amortize inner optimization, but interference between candidates is a known source of proxy error.

[DERIVED] In a coupled build search, “shared state” could mean reusing a partially optimized tree, gear pool, or build statistics across outer choices. The sources support this as a class of approximation, but do not establish that shared state preserves ranking for arbitrary game mechanics.

### 2.7 Cheap local repair before full evaluation

**Mechanism**

[DERIVED] Apply a limited repair or commitment pass around an outer choice, then use the repaired build as a proxy before paying for the complete rebuild.

[DERIVED] The opened generic optimization papers do not define this exact deterministic-build operation; the closest opened implementation source uses whole-build commitment rather than a single local repair.

[SOURCE] Primary source for the game-specific implementation: MaxWilk, `poe2-build-mcp`, `docs/build-optimizer-spec.md`, source repository. Post date was not stated on the opened page.  
URL: <https://github.com/MaxWilk/poe2-build-mcp/blob/main/docs/build-optimizer-spec.md>

[SOURCE] The design spec states:

> “The automated, holistic whole-build optimizer. It does the synthesis the greedy per-slot tools can’t.”

[SOURCE] It describes the candidate mechanism:

> “For each dominant lever, build the version that maximally commits it across every source it can come from, evaluated as the whole build.”

[SOURCE] It uses a multi-pass process over passive tree, gear, jewels, supports, and combat profile, then evaluates the complete build.

[SOURCE] The stated cost is:

> “~1–3k engine evals (`commit_and_max` ≈ 50–200 evals × ~5 levers × 2–3 passes) ≈ 1–3 min.”

[SOURCE] The stated limitation is:

> “Heuristic / local optima — report ‘best found, not global.’”

[DERIVED] This is not a cheap one-node repair followed by a proof of full-build value. It is a deliberately biased, multi-stage approximation to the inner rebuild, followed by full engine evaluation.

[UNVERIFIED] No opened primary paper or official engineering source provided a general theorem identifying when a cheap local repair will preserve the verdict of a full rebuild in a deterministic game-build space.

**Where sources disagree**

[SOURCE] Hyperband presents a low-budget ranking premise:

> “Resources can take various forms, including size of training set, number of features, or number of iterations for iterative algorithms.”

[SOURCE] BOHB qualifies that premise:

> “The low fidelity evaluations of BOHB can cause a constant overhead without any gain.”

[SOURCE] MFES-HB adds that low-fidelity observations can be “biased yet informative.”

[DERIVED] The disagreement is about how much useful information low fidelity contains and when its cost is justified, not about whether high-fidelity validation remains necessary.

**What the sources say**

[DERIVED] Cheap proxies work when the source can demonstrate a fidelity relationship, a learning curve, a calibrated surrogate, or an amortized shared representation; the sources do not supply a universal proxy for a rebuild-dependent discrete game choice.

## 3. Screening Before the Full Run

### 3.1 Successive Halving

**Mechanism**

[DERIVED] Allocate the same small budget to a set of candidates, rank them, discard a fixed fraction, and repeat with geometrically larger budgets.

[DERIVED] The method spends most resources on candidates that continue to look good and evaluates many more candidates at low fidelity than at full fidelity.

[SOURCE] Primary source: Kevin Jamieson, Ameet Talwalkar, 2016, *Non-stochastic Best Arm Identification and Hyperparameter Optimization*, AISTATS/PMLR. Published 2 May 2016.  
URL: <https://proceedings.mlr.press/v51/jamieson16.html>

[SOURCE] Defining passage:

> “The proposed Successive Halving algorithm … uniformly allocate the budget to a set of arms for a predefined amount of iterations, evaluate their performance, throw out the worst half, and repeat until just one arm remains.”

[SOURCE] Claimed condition:

> “Our algorithm … makes no assumptions on the convergence behavior of the arms’ losses.”

[SOURCE] Cost condition:

> “In practice B ≫ n, and thus Successive Halving is a particularly attractive option.”

[SOURCE] The paper treats the number of observed losses as an important cost when evaluating an arm is expensive. It reports order-of-magnitude speedups on examples including 100-arm kernel-SVM searches.

[SOURCE] Its limit is explicit:

> “Without additional assumptions on the λi functions, it is impossible for any algorithm to know with certainty that an arm is the best arm.”

[SOURCE] The authors report a fallback guarantee: when favorable assumptions do not hold, Successive Halving is comparable to uniform allocation up to logarithmic factors, but the favorable speedup depends on the observed loss curves.

[DERIVED] “No assumptions” here means no assumed parametric convergence curve for theory, not no assumption about the usefulness of early observations. The algorithm still makes irreversible promotion decisions from partial scores.

### 3.2 Hyperband’s bracket search

**Mechanism**

[DERIVED] Run several Successive-Halving schedules with different starting candidate counts and minimum budgets.

[DERIVED] Each bracket explores a different trade-off between broad screening and reliable initial measurements, while the total work per bracket is approximately controlled.

[SOURCE] Hyperband states:

> “Hyperband … addresses this ‘n versus B/n’ problem by considering several possible values of n for a fixed B.”

[SOURCE] It also states:

> “A single execution of Hyperband takes a finite budget of (smax+1)B.”

[SOURCE] Conditions include maximum resource `R`, discard factor `η`, and a logarithmic number of brackets \(s_{\max}+1=\lfloor \log_\eta R\rfloor+1\).

[SOURCE] The source warns:

> “If more resources are required before configurations can differentiate themselves in terms of quality … then it would be reasonable to work with a small number of configurations.”

[SOURCE] It also warns in the opposite direction:

> “If the quality of a configuration is typically revealed after a small number of resources … then n is the bottleneck and we should choose n to be large.”

[SOURCE] The paper reports that more aggressive early stopping was effective in most of its experiments, but the best bracket was not known in advance. It recommends considering overhead when increasing aggressiveness.

[DERIVED] Hyperband reduces sensitivity to the unknown screening aggressiveness, but it does not solve a fidelity mismatch. If a coupled build looks weak until its surrounding tree and gear have been reconfigured, an aggressive bracket can discard it before its value appears.

### 3.3 Racing and early elimination

**Mechanism**

[DERIVED] Allocate additional evaluation budget adaptively to candidates that currently appear promising and stop candidates that are sufficiently unlikely to win.

[DERIVED] Racing can be synchronous, as in classic Successive Halving, or asynchronous, where candidates are promoted as soon as enough comparable observations exist.

[SOURCE] Hyperband summarizes the general adaptive-evaluation idea:

> “These approaches are adaptive in computation, allocating more resources to promising hyperparameter configurations while quickly eliminating poor ones.”

[SOURCE] The same paper reports that earlier approaches often rely on convergence assumptions or heuristics, and that performance can suffer when those assumptions are violated.

[SOURCE] Jamieson and Talwalkar state:

> “No algorithm can provably identify a hyperparameter with a value within ε of the optimal without known, explicit functions γi.”

[SOURCE] Their setting assumes an iterative algorithm where additional resource produces an observable intermediate loss. The source does not give a general guarantee for arbitrary deterministic black-box evaluations with no meaningful partial trajectory.

[DERIVED] In the requested setting, the natural racing unit would not be “seconds of the exact evaluator” unless intermediate evaluator states have a meaningful monotone interpretation. A partial rebuild can be a different candidate rather than a lower-fidelity version of the same candidate.

### 3.4 BOHB screening conditions

**Mechanism**

[DERIVED] Use a model to choose which candidates enter Hyperband, then use Successive Halving to allocate budgets among them.

[DERIVED] BOHB promotes candidates using increasingly reliable budgets while retaining model guidance for candidate generation.

[SOURCE] BOHB states:

> “Bandit-based configuration evaluation approaches based on random search lack guidance and do not converge to the best configurations as quickly.”

[SOURCE] It reports budgets of 22, 66, 200, and 600 epochs, 19 parallel workers, and a full run of 33 GPU-days.

[SOURCE] Its failure condition is:

> “BOHB struggles in the very high dimensional case.”

[SOURCE] The authors attribute that to higher noise, the need for larger budgets to build a good model, and low-budget evaluations adding a constant overhead.

[DERIVED] BOHB is most directly applicable when the screening resource is naturally divisible and the low-budget candidate remains semantically the same candidate at higher budgets. A partial tree/gear rebuild may not satisfy that condition.

### 3.5 MFES-HB and biased screening

**Mechanism**

[DERIVED] Screen with multiple fidelity levels, fit fidelity-specific models, and weight those models according to how well they predict the target fidelity.

[DERIVED] Promotion is therefore based on learned cross-fidelity reliability rather than assuming that every low-fidelity score is equally trustworthy.

[SOURCE] MFES-HB states:

> “The low-fidelity measurements can be biased yet informative to guide the configuration search.”

[SOURCE] Its empirical condition is real-world AutoML tasks, where it reports 3.3x to 8.9x speedups over BOHB.

[SOURCE] The paper does not state an absolute candidate count at which screening ceases to pay off.

[DERIVED] MFES-HB provides a model for dealing with systematic low-fidelity bias, but the required calibration data must contain enough high-fidelity observations to estimate that bias.

### 3.6 Mis-ranking coupled choices

[SOURCE] Hyperband gives a formal ranking intuition:

> “It is possible to distinguish between the two configurations when the envelopes no longer overlap.”

[SOURCE] It states that the envelopes may remain wide when convergence is slow or candidates have similar terminal quality.

[SOURCE] Jamieson and Talwalkar state:

> “Without additional assumptions on the λi functions, it is impossible for any algorithm to know with certainty that an arm is the best arm.”

[DERIVED] A coupled outer choice is especially vulnerable when:

- [DERIVED] the cheap evaluation does not include the inner decision variables that express the choice’s value;
- [DERIVED] the choice changes the feasible or attractive region of the inner search;
- [DERIVED] the choice has a delayed payoff after several coordinated changes;
- [DERIVED] the cheap score has a different ordering from the fully rebuilt score.

[UNVERIFIED] The opened sources do not provide a game-build-specific mis-ranking rate for keystones, uniques, ascendancies, support swaps, aura sets, or defence-model switches.

**Where sources disagree**

[SOURCE] Jamieson and Talwalkar emphasize robustness:

> “Successive Halving … makes no assumptions on the convergence behavior of the arms’ losses.”

[SOURCE] The same paper limits that statement:

> “Without additional assumptions on the λi functions, it is impossible for any algorithm to know with certainty that an arm is the best arm.”

[SOURCE] Hyperband says early stopping can be “safe for neural network tasks” in its experiments, while also saying that the optimal allocation depends on the unknown envelope functions and terminal-loss distribution.

[DERIVED] The sources support empirical usefulness, not universal safety. “No assumed curve” is a theoretical model property; it is not a guarantee against delayed or non-monotonic candidate value.

**What the sources say**

[DERIVED] Screening pays when low-budget performance separates winners from losers before the full budget, and it mis-ranks when the candidate’s eventual value is delayed, close, noisy, or structurally different at higher fidelity.

## 4. Game Build / Loadout Search

### 4.1 Path of Building: integrated what-if evaluation, not whole-build outer search

**Mechanism**

[DERIVED] Path of Building maintains a build state containing passive nodes, skills, items, and configuration, and recalculates offence and defence after edits.

[DERIVED] Its documented interaction is local planning and comparison; the opened repository documentation does not describe a solver that enumerates build-defining choices and fully re-optimizes the rest of the build for each one.

[SOURCE] Primary source: Path of Building Community, source repository README. Post date was not stated on the opened page.  
URL: <https://github.com/PathOfBuildingCommunity/PathOfBuilding>

[SOURCE] The repository describes itself as:

> “Offline build planner for Path of Exile.”

[SOURCE] Passive-tree behavior:

> “Fully integrated with the offence/defence calculations; see exactly how each node will affect your character!”

[SOURCE] Item behavior:

> “Fully integrated with the offence/defence calculations; see exactly how much of an upgrade a given item is!”

[SOURCE] The feature list includes passive-tree planning, skills, auras, support gems, item planning, unique items, crafting, and offence/defence calculations.

[SOURCE] The repository also has a public website describing node power and upgrade comparisons: <https://pathofbuilding.community/>

[DERIVED] The documented model is a high-fidelity evaluator and interactive what-if planner. The source does not document an outer loop of the form “try every keystone, rebuild the entire tree and gear, then compare.”

[UNVERIFIED] No opened Path of Building source page established a published cost per optimizer candidate or a rule for deciding which changes require a full rebuild.

### 4.2 POEMOOTREES: passive-tree-only optimization

**Mechanism**

[DERIVED] POEMOOTREES searches for connected passive-tree routes satisfying selected stat objectives and can generate shareable tree links.

[DERIVED] It does not, in the opened description, jointly optimize gear, skills, supports, auras, or configuration around a build-defining choice.

[SOURCE] Primary source: POEMOOTREES project page. Post date was not stated on the opened page, which returned a 404 during retrieval.  
URL: <https://lazyloafs.github.io/POEMOOTREES/>

[SOURCE] Search result description:

> “POEMOOTREES is an unofficial Path of Exile passive skill tree optimizer, planner, and URL builder.”

[SOURCE] The described objectives include life, damage, resistances, attributes, keystones, jewel sockets, and connected routes.

[DERIVED] This is a restricted inner optimization over the passive tree, not a whole-build rebuild evaluator.

### 4.3 `poega`: genetic-algorithm build search

**Mechanism**

[DERIVED] The repository identifies a genetic algorithm as the search mechanism for Path of Exile builds.

[DERIVED] The opened repository page does not explain whether each chromosome is fully rebuilt and exactly evaluated, whether choices are coupled, or how fitness is computed.

[SOURCE] Primary source: cboursnell, `poega`, source repository. Post date was not stated on the opened page.  
URL: <https://github.com/cboursnell/poega>

[SOURCE] Repository description:

> “Path of Exile build designer with genetic algorithm”

[UNVERIFIED] The opened source did not provide a documented evaluation budget, candidate count, rebuild procedure, full evaluator details, or stated failure mode. The repository therefore supports only the existence of a genetic-algorithm PoE build project, not a conclusion about its handling of rebuild-dependent choices.

### 4.4 Genshin Optimizer: exhaustive candidate combinations plus pruning

**Mechanism**

[DERIVED] Genshin Optimizer represents candidate artifacts and equipment as per-slot candidate arrays, constructs builds from their combinations, and evaluates them with a calculation graph.

[DERIVED] It reduces the exact Cartesian search using symbolic range, branch, monotonicity, and top-N pruning before worker-based evaluation.

[SOURCE] Primary source: frzyc, Genshin Optimizer, source repository. Post date was not stated on the opened page.  
URL: <https://github.com/frzyc/genshin-optimizer>

[SOURCE] Repository description:

> “An Artifact optimizer for Genshin Impact(And other Gacha games).”

[SOURCE] The solver source defines the optimization objective and candidate arrays, including light cones or weapons and equipment by slot.  
URL: <https://github.com/frzyc/genshin-optimizer/blob/54e791a606e84426c451c156f790177d55df6ef0/libs/game-opt/solver/src/solver.ts>

[SOURCE] The solver code initializes worker processes and calls a pruning pass before distributing work. It evaluates remaining combinations in parallel and retains `topN` builds.

[SOURCE] The pruning source describes its purpose:

> “Reduce the complexity of the optimization problem”

[SOURCE] It also states:

> “Remove candidates that do not meet the minimum requirements in any builds”

[SOURCE] And:

> “Remove candidates that are never in the topN builds”

[SOURCE] The source uses range bounds and monotonicity to remove candidates before exact evaluation.  
URL: <https://github.com/frzyc/genshin-optimizer/blob/54e791a606e84426c451c156f790177d55df6ef0/libs/pando/engine/src/optimization/prune.ts>

[DERIVED] This is evidence for exact or bounded combination search over a fixed build model, not evidence that Genshin Optimizer treats a build-defining outer choice as a separate bilevel variable requiring a fresh full rebuild.

[UNVERIFIED] The opened source did not state a universal candidate-count threshold, an exact per-build evaluation time, or a policy for re-optimizing the rest of a character around a new set bonus or character mechanic.

### 4.5 `poe2-build-mcp`: explicit whole-build commit-and-max

**Mechanism**

[DERIVED] Select an archetype lever, deliberately commit to it across passive tree, gear, jewels, supports, and combat profile, then evaluate the assembled complete build.

[DERIVED] Repeat the commitment pass for several levers and retain the best engine-verified build subject to constraints; this directly represents value that appears only after coordinated rebuilding.

[SOURCE] Primary source: MaxWilk, `poe2-build-mcp`, source repository and optimizer design specification. Post date was not stated on the opened pages.  
Repository: <https://github.com/MaxWilk/poe2-build-mcp>  
Specification: <https://github.com/MaxWilk/poe2-build-mcp/blob/main/docs/build-optimizer-spec.md>

[SOURCE] The specification describes the problem:

> “Greedy per-slot/per-node optimizers are each locally optimal but myopic — they won't over-commit to a multiplier … before it pays off.”

[SOURCE] It defines the whole-build primitive:

> “The commitment lives in stacking ONE lever across tree+gear+jewels+supports together and judging the global result — not per slot.”

[SOURCE] The outer search is described as trying each dominant lever, plus a balanced pass, and keeping the build with the best objective subject to defensive constraints.

[SOURCE] The stated scale is:

> “~1–3k engine evals (`commit_and_max` ≈ 50–200 evals × ~5 levers × 2–3 passes) ≈ 1–3 min.”

[SOURCE] The source explicitly limits the result:

> “Heuristic / local optima — report ‘best found, not global.’”

[SOURCE] The repository README describes the optimizer as:

> “the holistic whole-build optimizer: archetype-seeded commit-and-max across tree + gear + jewels + supports”

[DERIVED] Among the opened game-build sources, this is the clearest direct implementation of a rebuild-dependent outer-choice strategy.

[UNVERIFIED] The source is an open-source design specification rather than a peer-reviewed benchmark, and the opened pages do not provide independent accuracy measurements for how often its heuristic preserves the best fully rebuilt choice.

### 4.6 What was not found

[UNVERIFIED] The live search did not find a peer-reviewed Path of Exile, Diablo, Last Epoch, Genshin, or MTG optimizer paper that reports a validated benchmark specifically for “choose a coupled build-defining option, fully re-optimize the remaining loadout, and compare against greedy one-change scoring.”

[UNVERIFIED] The opened game-tool sources mostly fall into three categories: high-fidelity interactive calculators, exact or pruned fixed-structure loadout enumeration, and heuristic whole-build synthesis.

**What the sources say**

[DERIVED] Existing game tools either expose high-fidelity what-if calculations, prune exact combinations inside a fixed model, or explicitly search whole-build commitments; the opened sources do not establish a general, benchmarked solution for every rebuild-dependent choice.

## 5. Fit: Cost, Candidate Counts, Needs, and Failure Modes

[DERIVED] The table uses “relative to a full evaluation” only where the source provides enough information to state it. “Not stated” is used where the opened source did not provide a defensible ratio.

| Method | Source | Cost per candidate relative to a full evaluation | Needs | Source’s own stated failure mode |
|---|---|---:|---|---|
| Exact bilevel / nested solve | [SOURCE] Franceschi et al. 2018, <https://proceedings.mlr.press/v80/franceschi18a.html> | [DERIVED] Approximately one inner solve per outer candidate; no universal ratio stated | [SOURCE] Inner optimization dynamics; convergence conditions for approximation | [SOURCE] Approximate solutions require sufficient conditions to converge to the exact problem; no universal budget threshold stated |
| Truncated hypergradient | [SOURCE] Franceschi et al. 2017, <https://proceedings.mlr.press/v70/franceschi17a.html> | [DERIVED] Partial inner trajectory plus derivative work; exact ratio not stated | [SOURCE] Differentiable iterative inner algorithm; memory/time trade-off | [SOURCE] Reverse and forward procedures have different running-time and space trade-offs |
| DARTS | [SOURCE] Liu et al. 2019, <https://arxiv.org/html/1806.09055v2> | [SOURCE] 1.5 GPU-days first-order CIFAR search; 4 GPU-days second-order; final model retrained | [SOURCE] Continuous relaxation, differentiable losses, shared weights, validation split | [SOURCE] Exact architecture gradient can be prohibitive; no convergence guarantee stated; continuous-to-discrete discrepancy remains |
| ENAS | [SOURCE] Pham et al. 2018, <https://arxiv.org/html/1802.03268v2> | [SOURCE] Less than 16 hours on one GTX 1080Ti; roughly 1,000x below standard NAS in reported setting | [SOURCE] Common supergraph and shared parameters; validation reward; final retraining | [SOURCE] Different child models may utilize shared weights differently |
| Once-for-All / OFA | [SOURCE] Cai et al. 2020, <https://arxiv.org/html/1908.09791v5> | [SOURCE] 1,200 GPU-hours one-time training; 40 GPU-hours to collect predictor data; specialization search negligible | [SOURCE] One super-network; progressive shrinking; 16K sampled sub-networks; 10K validation images | [SOURCE] Enumerating all sub-networks is computationally prohibitive; naïve random sampling causes significant accuracy drops because of interference |
| Multi-fidelity BO / taKG | [SOURCE] Wu et al. 2020, <https://proceedings.mlr.press/v115/wu20a.html> | [SOURCE] No universal ratio; cheap fidelities are explicitly intended to replace some full evaluations | [SOURCE] Iterative training, multiple fidelity controls, trace observations, cost-aware acquisition | [SOURCE] The method is tied to informative fidelity traces; no arbitrary black-box ranking guarantee is stated |
| Successive Halving | [SOURCE] Jamieson and Talwalkar 2016, <https://proceedings.mlr.press/v51/jamieson16.html> | [SOURCE] Budget is allocated geometrically; 100-arm SVM experiment achieved over an order-of-magnitude wall-clock speedup | [SOURCE] Intermediate losses, a total budget, and candidates comparable at each rung | [SOURCE] Without additional assumptions it is impossible to know with certainty that an arm is best |
| Hyperband | [SOURCE] Li et al. 2018, <https://arxiv.org/html/1603.06560> | [SOURCE] One run costs approximately \((s_{\max}+1)B\); LeNet used \(R=81,\eta=3\), five brackets | [SOURCE] Maximum resource `R`, discard factor `η`, meaningful partial evaluations | [SOURCE] Wider convergence envelopes or close terminal values require more resources before candidates can be distinguished |
| BOHB | [SOURCE] Falkner et al. 2018, <https://proceedings.mlr.press/v80/falkner18a.html> | [SOURCE] Budgets 22/66/200/600 epochs; 33 GPU-days total; full budget about 7 hours per worker | [SOURCE] Multi-fidelity budgets, KDE surrogate, enough high-budget observations, parallel workers | [SOURCE] Low-fidelity evaluations can create constant overhead without gain; struggles in very high dimensions |
| MFES-HB | [SOURCE] Li et al. 2021, <https://ojs.aaai.org/index.php/AAAI/article/view/17031> | [SOURCE] Reports 3.3x–8.9x speedup over BOHB; absolute candidate count not stated | [SOURCE] Multiple biased but informative fidelity datasets; fidelity-specific surrogates | [SOURCE] Low-fidelity measurements are biased, so naïve use can mislead |
| PoB interactive what-if | [SOURCE] Path of Building Community, <https://github.com/PathOfBuildingCommunity/PathOfBuilding> | [UNVERIFIED] Full evaluator cost per edit not stated on opened source page | [SOURCE] Existing build state, game calculation engine, user-selected edits | [UNVERIFIED] No documented outer-search failure mode because no such optimizer was documented on the opened page |
| POEMOOTREES | [SOURCE] <https://lazyloafs.github.io/POEMOOTREES/> | [UNVERIFIED] Cost not stated | [SOURCE] Passive-tree graph and stat objectives | [UNVERIFIED] Gear, skills, and full-build coupling were not documented in the opened description |
| `poega` | [SOURCE] <https://github.com/cboursnell/poega> | [UNVERIFIED] Cost and candidate count not stated | [SOURCE] Genetic-algorithm representation and fitness evaluator; details not found | [UNVERIFIED] Rebuild behavior and failure mode not documented on the opened page |
| Genshin Optimizer exact/pruned solver | [SOURCE] <https://github.com/frzyc/genshin-optimizer/blob/54e791a606e84426c451c156f790177d55df6ef0/libs/game-opt/solver/src/solver.ts> | [DERIVED] Exact evaluation of remaining Cartesian combinations after symbolic pruning; ratio not stated | [SOURCE] Candidate arrays, calculation graph, constraints, top-N target, worker parallelism | [SOURCE] Pruning only removes candidates using stated range/monotonicity/top-N logic; no general coupled-choice guarantee |
| `poe2-build-mcp` commit-and-max | [SOURCE] <https://github.com/MaxWilk/poe2-build-mcp/blob/main/docs/build-optimizer-spec.md> | [SOURCE] Approximately 1–3k engine evaluations and 1–3 minutes for the specified five-lever, 2–3-pass example | [SOURCE] Archetype lever profiles, whole-build engine, constraints, multi-stage tree/gear/jewel/support search | [SOURCE] “Heuristic / local optima”; result is “best found, not global” |

### Candidate-count and break-even findings

[DERIVED] The sources do not give one common candidate-count threshold at which all methods stop paying off. Their reported scales are method-specific:

- [SOURCE] DARTS compares 1.5–4 GPU-days against 2,000–3,150 GPU-days for earlier NAS methods.
- [SOURCE] ENAS searches spaces with approximately \(10^{15}\) to \(10^{29}\) possible architectures while using under 16 hours on one GPU in its reported experiments.
- [SOURCE] OFA reports more than \(10^{19}\) sub-networks, 16,000 sampled sub-networks for predictor training, 40 GPU-hours of predictor-data collection, and a 1,200 GPU-hour one-time training cost.
- [SOURCE] Successive Halving reports an experiment with 100 arms and an order-of-magnitude speedup, while explicitly conditioning usefulness on `B ≫ n`.
- [SOURCE] Hyperband reports \(R=81\), \(\eta=3\), five brackets, and 70 LeNet trials.
- [SOURCE] BOHB reports 19 workers, four budgets, 16 iterations, 33 GPU-days, and fewer than three full function-equivalent evaluations per worker.
- [SOURCE] MFES-HB reports 3.3x–8.9x over BOHB but no absolute candidate count.
- [SOURCE] `poe2-build-mcp` reports 1–3k engine evaluations for its specified whole-build heuristic, not a global-optimum guarantee.
- [UNVERIFIED] The opened sources do not state the candidate count at which an exact deterministic game-build evaluator, specifically, should switch from full rebuilds to screening.

[DERIVED] The source-defined stopping conditions are therefore qualitative or workload-specific: low fidelity must be predictive, the total budget must dominate per-candidate overhead, enough high-fidelity observations must exist to calibrate the surrogate, and the amortized setup cost must be spread across enough candidates or deployment scenarios.

## Opened URLs

[SOURCE] The following primary-source URLs were opened during the research:

1. <https://proceedings.mlr.press/v80/franceschi18a.html>
2. <https://proceedings.mlr.press/v80/franceschi18a/franceschi18a.pdf>
3. <https://proceedings.mlr.press/v70/franceschi17a.html>
4. <https://proceedings.mlr.press/v51/jamieson16.html>
5. <https://arxiv.org/html/1603.06560>
6. <https://arxiv.org/abs/1603.06560>
7. <https://www.jmlr.org/papers/volume18/16-558/16-558.pdf>
8. <https://proceedings.mlr.press/v115/wu20a.html>
9. <https://ojs.aaai.org/index.php/AAAI/article/view/17031>
10. <https://proceedings.mlr.press/v80/falkner18a.html>
11. <https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf>
12. <https://arxiv.org/abs/1807.01774>
13. <https://proceedings.mlr.press/v80/pham18a.html>
14. <https://arxiv.org/html/1802.03268v2>
15. <https://arxiv.org/abs/1802.03268>
16. <https://arxiv/html/1806.09055v2>
17. <https://arxiv.org/abs/1806.09055>
18. <https://arxiv/html/1908.09791v5>
19. <https://arxiv.org/abs/1908.09791>
20. <https://github.com/mit-han-lab/once-for-all>
21. <https://github.com/PathOfBuildingCommunity/PathOfBuilding>
22. <https://pathofbuilding.community/>
23. <https://github.com/cboursnell/poega>
24. <https://github.com/frzyc/genshin-optimizer>
25. <https://github.com/frzyc/genshin-optimizer/blob/54e791a606e84426c451c156f790177d55df6ef0/libs/game-opt/solver/src/solver.ts>
26. <https://github.com/frzyc/genshin-optimizer/blob/54e791a606e84426c451c156f790177d55df6ef0/libs/pando/engine/src/optimization/prune.ts>
27. <https://github.com/MaxWilk/poe2-build-mcp>
28. <https://github.com/MaxWilk/poe2-build-mcp/blob/main/docs/build-optimizer-spec.md>
29. <https://lazyloafs.github.io/POEMOOTREES/>
30. <https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/blob/510802af/src/Classes/PassiveTree.lua>