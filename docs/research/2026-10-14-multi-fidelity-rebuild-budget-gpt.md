# Research: How Other Fields Pay for Costly Trials in Steps

**Scope and labels.** [SOURCE] means a statement or quote from a source opened for this report. [DERIVED] means arithmetic or a conclusion explicitly shown from sourced definitions. [UNVERIFIED] means the requested evidence was not found; it is not an assertion of fact.

**Terminology used below.** [DERIVED] Let `R` be the cost of one full trial, `r` a low-fidelity rung cost, `eta > 1` a reduction factor, and `n` the initial number of candidates. A “full-trial equivalent” is total resource divided by `R`; it is not necessarily the number of candidates actually evaluated at full fidelity.

## 1. Successive Halving, Hyperband, and ASHA

**Mechanism, in two lines.** [SOURCE] Successive Halving (SH) evaluates every candidate at an initial resource, ranks them, keeps the top `1 / eta`, increases their resource by `eta`, and repeats. Hyperband runs SH brackets spanning different initial candidate-count/resource trade-offs; ASHA uses the same rung concept but promotes without waiting for a synchronized rung barrier.

### Successive Halving

[SOURCE] Kevin Jamieson and Ameet Talwalkar, *Non-stochastic Best Arm Identification and Hyperparameter Optimization* (AISTATS, 2016), define SH for a fixed total budget `B` and an input set of `n` arms/configurations.

> “Uniformly allocate a budget to a set of hyperparameter configurations, evaluate the performance of all configurations, throw out the worst half, and repeat until one configuration remains.”  
> Kevin Jamieson et al., 2016, *Hyperband* restatement of SH.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] The original paper specifies a fixed total resource limit rather than a fixed number of completed candidates.

> “First, we verify that the algorithm never takes a total number of samples that exceeds the budget `B`.”  
> Jamieson and Talwalkar, 2016, Sec. 3.1.  
> URL: https://proceedings.mlr.press/v51/jamieson16.pdf

[SOURCE] Their stated operating condition is that the total budget is much larger than the number of arms.

> “In practice `B >> n`, and thus Successive Halving is a particularly attractive option.”  
> Jamieson and Talwalkar, 2016, p. 242.  
> URL: https://proceedings.mlr.press/v51/jamieson16.pdf

[DERIVED] In the original “discard half” form, `eta = 2`. Generalized SH uses arbitrary `eta`: resource at rung `i` is `r_i = r * eta^i`, and approximately `n_i = n / eta^i` candidates remain. There are `s + 1` rungs when `R = r * eta^s`.

[DERIVED] Under the standard **cumulative-rung accounting** used by Hyperband papers, every ideal rung costs:

```text
n_i * r_i = (n / eta^i) * (r * eta^i) = n * r
```

[DERIVED] Therefore one `s + 1` rung bracket costs approximately `(s + 1) * n * r`; compared with one full trial, this is `(s + 1) * n * r / R`.

[DERIVED] If a trial can truly resume from a checkpoint, the actual incremental work after the first rung is lower than cumulative-rung accounting. If a partial trial instead performs a distinct local search and cannot resume into the full search, its costs are separate evaluations; the checkpoint-saving calculation does not apply.

[SOURCE] SH’s stated allocation failure is choosing the initial population incorrectly.

> “Unfortunately, Successive Halving requires the number of configurations `n` as an input to the algorithm.”  
> Li et al., 2018, Sec. 3.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

### Hyperband

[SOURCE] Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh, and Ameet Talwalkar, *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization* (JMLR, 2018; ICLR version 2017), use multiple SH brackets because `n` versus initial resource is unknown.

> “Hyperband addresses this ‘`n` versus `B/n`’ problem by considering several possible values of `n` for a fixed `B`.”  
> Li et al., 2018, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] Each bracket trades candidate count against initial resource while being constructed to use approximately equal total resource.

> “Each bracket is designed to use approximately `B` total resources and corresponds to a different tradeoff between `n` and `B/n`.”  
> Li et al., 2018, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] For maximum resource `R`, Hyperband defines:

```text
s_max = floor(log_eta(R))
B = (s_max + 1) * R
```

[SOURCE] At bracket `s`, its Algorithm 1 uses:

```text
n_s = ceil((B / R) * eta^s / (s + 1))
r_s = R * eta^(-s)
```

and at each rung:

```text
n_i = floor(n_s * eta^(-i))
r_i = r_s * eta^i
```

Li et al., 2018, Algorithm 1.  
URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] The paper states the total nominal cost of one complete all-bracket Hyperband execution.

> “Hence, a single execution of Hyperband takes a finite budget of `(s_max + 1)B`.”  
> Li et al., 2018, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[DERIVED] Since `B = (s_max + 1)R`, one complete cycle costs:

```text
C_HB = (s_max + 1)^2 * R
```

That is `(s_max + 1)^2` full-trial equivalents under the paper’s cumulative-rung accounting.

[SOURCE] The `s = 0` bracket is the fully expensive reference bracket.

> “The final bracket, `s = 0`, in which every configuration is allocated `R` resources … simply performs classical random search.”  
> Li et al., 2018, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

### Hyperband rung example and cost

[SOURCE] The authors’ LeNet example uses `R = 81` and `eta = 3`.

> “We set `R` to 81 and use the default value of `eta = 3`, resulting in `s_max = 4` and thus 5 brackets.”  
> Li et al., 2018, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[DERIVED] Applying Algorithm 1 gives this schedule:

| Bracket `s` | Initial candidates | First rung | Rungs | Approximate full-resource survivors |
|---:|---:|---:|---|---:|
| 4 | 81 | `1 / 81 R` | `1, 3, 9, 27, 81` | 1 |
| 3 | 34 | `3 / 81 R` | `3, 9, 27, 81` | 1 |
| 2 | 15 | `9 / 81 R` | `9, 27, 81` | 1 |
| 1 | 8 | `27 / 81 R` | `27, 81` | about 2 after floors |
| 0 | 5 | `R` | `81` | 5 |

[DERIVED] The full cycle costs `25R`, starts 143 candidate evaluations, and, with the paper’s floor survivor rule, yields about ten full-`R` evaluations. The other `15R` full-trial equivalents were spent on partial rungs.

### Why `eta` exists, and measured sensitivity

[SOURCE] `eta` simultaneously sets the resource jump and promotion fraction.

> “SH internally evaluates configurations on a given budget, ranks them by their performance, and continues the top `eta^-1` … on a budget `eta` times larger.”  
> Falkner, Klein, and Hutter, *BOHB* (ICML, 2018), Sec. 3.2.  
> URL: https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf

[SOURCE] Hyperband’s authors report qualitative, rather than a published numeric sweep table, sensitivity to `eta`.

> “We stress that results are not very sensitive to the choice of `eta`.”  
> Li et al., 2018, Sec. 3.6.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] Their attached conditions are: `eta` controls aggressiveness, theory points toward `eta = e`, and their practical runs used `eta = 3` or `eta = 4`.

> “The theoretical analysis suggests setting `eta = e ≈ 2.718`; in practice, we use `eta = 3` or `eta = 4`.”  
> Li et al., 2018, Sec. 3.6.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] BOHB independently gives the same qualitative conclusion but identifies the budget endpoints as more important.

> “Like HB (Li et al., 2017), BOHB is also quite insensitive to this choice in a reasonable range.”  
> Falkner, Klein, and Hutter, 2018, supplementary Sec. G.  
> URL: http://proceedings.mlr.press/v80/falkner18a/falkner18a-supp.pdf

[SOURCE] The same BOHB study conditions that statement on the chosen low fidelity carrying information.

> “To get substantial speedups, an evaluation with a budget of `b_min` should contain some information about the quality of a configuration with larger budgets.”  
> Falkner, Klein, and Hutter, 2018, supplementary Sec. G.  
> URL: http://proceedings.mlr.press/v80/falkner18a/falkner18a-supp.pdf

[SOURCE] In Li et al.’s LeNet experiment (`R = 81`, `eta = 3`, five brackets, 70 trials of each bracket), the most and least aggressive brackets were not best.

> “In practice, we do not know a priori which bracket `s` … will be most effective, and in this case neither the most nor least aggressive setting is optimal.”  
> Li et al., 2018, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[DERIVED] The sources therefore report robustness to modest `eta` changes in their tested ranges, but also demonstrate sensitivity to the resulting allocation regime: a middle bracket won in the cited `R = 81`, `eta = 3` study.

### ASHA

[SOURCE] Liam Li, Kevin Jamieson, Afshin Rostamizadeh, Ekaterina Gonina, Jonathan Ben-Tzur, Moritz Hardt, Benjamin Recht, and Ameet Talwalkar, *A System for Massively Parallel Hyperparameter Tuning* (MLSys, 2020), define Asynchronous Successive Halving Algorithm (ASHA).

> “ASHA promotes configurations to the next rung whenever possible instead of waiting for a rung to complete before proceeding.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] If no configuration qualifies for promotion, it fills the bottom rung.

> “If no promotions are possible, ASHA simply adds a configuration to the base rung, so that more configurations can be promoted to the upper rungs.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] ASHA was designed for much larger populations and worker pools than the setting in this issue.

> “ASHA is designed for what we refer to as the ‘large-scale regime,’ where … we must evaluate orders of magnitude more hyperparameter configurations than available parallel workers.”  
> Li et al., 2020, Sec. 1.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] It does not require an initial candidate count in its open-ended form.

> “Given its asynchronous nature it does not require the user to pre-specify the number of configurations to evaluate.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] Its authors’ production defaults were `eta = 4`, promoting the top quarter, with a most-aggressive minimum resource `r = R / 256`.

> “Elimination rate: we set `eta = 4` so that the top `1/4` of configurations are promoted to the next rung.”  
> Li et al., 2020, Sec. 5.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

> “Maximum early-stopping rate … indicates a minimum resource of `r = R/256`.”  
> Li et al., 2020, Sec. 5.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[DERIVED] With `eta = 4` and `r = R / 256`, an ideal five-rung bracket begins 256 candidates at `R / 256`, promotes 64 to `R / 64`, 16 to `R / 16`, four to `R / 4`, and one to `R`. Its cumulative rung accounting is `5R`; its checkpoint-resume incremental training work is `4R`.

[SOURCE] ASHA’s wall-clock claim has conditions: sufficient workers and a trial resource whose time scales linearly.

> “Under the assumption that the training time of a configuration is linear in the resource allocation … ASHA can return a configuration trained to completion in time … `≤ 2 time(R)`.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] The same source explicitly distinguishes the resumed-training case.

> “When training is iterative, ASHA can return an answer in `time(R)`, since incrementally trained configurations can be checkpointed and resumed.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

### ASHA’s stated failure mode

[SOURCE] ASHA trades synchronization waits for imperfect early promotions.

> “ASHA is able to remove the bottleneck associated with synchronous promotions by incurring a small number of incorrect promotions.”  
> Li et al., 2020, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] Their definition is promotion-specific, not false elimination.

> “Incorrect promotions, i.e. configurations that were promoted early on but are not in the top `1/eta` of configurations in hindsight.”  
> Li et al., 2020, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] Their `sqrt(n)` argument has a large-rung condition.

> “In the first rung with `n` evaluated configurations, the number of mispromoted configurations is roughly `sqrt(n)`.”  
> Li et al., 2020, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[DERIVED] The fraction is approximately `1 / sqrt(n)`, so the paper’s large-`n` rationale does not establish a small error fraction at `n = 2` through `6`.

[SOURCE] Ray Tune’s current official `AsyncHyperBandScheduler` documents the operative parameters rather than requiring a candidate count.

> “Implements the Async Successive Halving.”  
> Ray Project documentation, accessed 2026-10-14.  
> URL: https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.AsyncHyperBandScheduler.html

[SOURCE] Its current documented defaults are `max_t = 100`, `grace_period = 1`, `reduction_factor = 4`, `brackets = 1`.

> “This should provide similar theoretical performance as HyperBand but avoid straggler issues that HyperBand faces.”  
> Ray Project documentation, accessed 2026-10-14.  
> URL: https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.AsyncHyperBandScheduler.html

[SOURCE] Ray’s source documentation attaches an operational failure condition to absent progress reports.

> “Passing a key that is not present in the reported result causes the scheduler to skip its decision for that step.”  
> Ray Project documentation, accessed 2026-10-14.  
> URL: https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.AsyncHyperBandScheduler.html

**What the sources say.** [SOURCE] SH and Hyperband pay for full trials through geometrically spaced rungs and top-`1 / eta` promotion; Hyperband varies the initial allocation because no single candidate-count/resource split is known beforehand. [SOURCE] Published defaults cluster around `eta = 3` or `4`, with qualitative “not very sensitive in a reasonable range” claims, while published examples show a middle bracket can outperform both extremes. [SOURCE] ASHA’s main benefit and error analysis target large asynchronous populations, not two to six candidates.

## 2. Learning-Curve Extrapolation for Early Stopping

**Mechanism, in two lines.** [SOURCE] Learning-curve methods monitor intermediate values and stop a run if a fitted model, learned ranking predictor, or heuristic indicates it is unlikely to beat a comparison threshold. [SOURCE] The primary papers use posterior probability, predicted final value, pairwise ranking probability, patience, or rung rank; they usually report search regret and elapsed resource, not a standardized false-drop rate.

### Fitted curve and best-so-far threshold

[SOURCE] Tobias Domhan, Jost Tobias Springenberg, and Frank Hutter, *Speeding up Automatic Hyperparameter Optimization of Deep Neural Networks by Extrapolation of Learning Curves* (IJCAI, 2015), fit an ensemble of parametric curves with MCMC uncertainty.

> “We stopped training a network if our extrapolation model was 95% certain that it would not improve over the best known performance.”  
> Domhan, Springenberg, and Hutter, 2015, Sec. 3.2.  
> URL: https://www.ijcai.org/Proceedings/15/Papers/487.pdf

[SOURCE] The decision measure is probability of exceeding the best score by the maximum step.

> “We then consider the predicted probability `P(y_m >= y_hat | y_1:n)` that the network … will exceed the performance `y_hat`.”  
> Domhan, Springenberg, and Hutter, 2015, Sec. 3.2.  
> URL: https://www.ijcai.org/Proceedings/15/Papers/487.pdf

[SOURCE] Their measured conditions are `delta = 0.05`, checks every `p = 30` epochs, `k = 10` validation observations per epoch for fully connected networks, `k = 2` for CNNs, and CIFAR-10/CIFAR-100/MNIST searches with 100 to 150 configurations and maximum epochs of 100 or 285.

> “Every `p` epochs, we gather the performance values … and run MCMC to probabilistically extrapolate performance to the final step.”  
> Domhan, Springenberg, and Hutter, 2015, Sec. 3.2.  
> URL: https://www.ijcai.org/Proceedings/15/Papers/487.pdf

[SOURCE] Under those network- and dataset-specific settings, the paper reports an average CIFAR-10 optimizer run reduction from 40 to 18 hours and roughly twofold speedups in CNN searches.

> “The average time required by the optimizer to find a good configuration was reduced from 40 hours to 18 hours.”  
> Domhan, Springenberg, and Hutter, 2015, Sec. 4.2.  
> URL: https://www.ijcai.org/Proceedings/15/Papers/487.pdf

[UNVERIFIED] The paper does **not** report a false-drop/false-elimination percentage: the proportion of stopped runs that would have become the high-fidelity optimum, top-`k`, or threshold-beating configuration if continued.

### Curve prediction using previous configurations

[SOURCE] Aaron Klein, Stefan Falkner, Jost Tobias Springenberg, and Frank Hutter, *Learning Curve Prediction with Bayesian Neural Networks* (ICLR, 2017), separate per-curve extrapolation from methods learning across configuration identities.

> “The LC-Extrapolation method by Domhan et al. (2015), the GP, and the last seen value work on individual learning curves and do not allow to model performance across hyperparameter configurations.”  
> Klein et al., 2017, Sec. 3.  
> URL: https://mlanthology.org/iclr/2017/klein2017iclr-learning/

[SOURCE] Their conditions include four benchmark data sets: 256 CNN configurations trained 40 epochs on CIFAR-10; 4,096 fully connected configurations trained 100 epochs on MNIST; 1,024 logistic-regression configurations trained 100 epochs; and 1,024 VAE configurations trained 300 epochs.

[UNVERIFIED] This paper reports MSE, log likelihood, and Hyperband immediate regret rather than a false-drop rate or a specific “last `k` slopes” stopping rule.

### Predicted final performance and safety factor

[SOURCE] Bowen Baker, Otkrist Gupta, Ramesh Raskar, and Nikhil Naik, *Accelerating Neural Architecture Search using Performance Prediction* (2017), use sequential regression features of partial learning curves, gradients, and architecture.

> “We may mistakenly terminate the optimal configuration.”  
> Baker et al., 2017, Sec. 3.3.  
> URL: https://arxiv.org/html/1705.10823

[SOURCE] Their stopping condition compares predicted final performance to the best seen and applies a safety threshold `Delta`; a larger `Delta` is more conservative. The tested conditions include 100 completed configurations for regression-model training and curve sets including 500 TinyImageNet ResNets for 140 epochs, 500 CIFAR-10 ResNets for 50 epochs, 1,000 MetaQNN architectures for 20 epochs, and 300 Penn Treebank LSTMs for 60 epochs.

[SOURCE] In their MetaQNN experiment, `Delta = 0.99` gave a 3.8x speedup; their ResNet experiment reported that only `Delta = 0.99` consistently recovered the top model and gave a 3.4x speedup.

> “Only `Delta = 0.99` consistently recovers the top model.”  
> Baker et al., 2017, Sec. 4.1.  
> URL: https://arxiv.org/html/1705.10823

[UNVERIFIED] The recovery marker is not a false-drop rate. The paper gives recovery/speedup outcomes across repetitions, but does not publish the denominator and count required to calculate the rate of wrongly stopped candidates.

### Pairwise ranking and regret

[SOURCE] Martin Wistuba and Tejaswini Pedapati, *Learning to Rank Learning Curves* (ICML, 2020), use a direct pairwise probability that a run will beat the current best rather than only a final-value regression.

> “Promising runs may be terminated and unpromising runs may run longer than needed.”  
> Wistuba and Pedapati, 2020, Sec. 1.  
> URL: https://proceedings.mlr.press/v119/wistuba20a/wistuba20a.pdf

[SOURCE] Their `LCRankNet` criterion continues when the predicted chance a new model beats the incumbent is at least `delta`; their experiments used `delta = 0.45`.

> “If the predicted probability that the new model is better than the best one is below 45%, the run is terminated early.”  
> Wistuba and Pedapati, 2020, Sec. 3.  
> URL: https://arxiv.org/pdf/2006.03361

[SOURCE] The conditions were 200 random NASNet architectures trained for 100 epochs on each of CIFAR-10, CIFAR-100, Fashion-MNIST, Quickdraw, and SVHN; tests occurred every third epoch. Transfer data contained 1,000 architectures across five datasets.

[SOURCE] Table 1 reports **regret**, not false drops. For example, LCRankNet reports 0.22% regret in 20 GPU-hours on CIFAR-10 and 0.00% regret in 11 GPU-hours on CIFAR-100, versus 1,023 and 1,021 GPU-hours respectively without early termination.

> “We define regret as the difference between the accuracy of the model found by the random search and the accuracy of the model found by one of the methods.”  
> Wistuba and Pedapati, 2020, Sec. 4.  
> URL: https://arxiv.org/pdf/2006.03361

[SOURCE] The paper shows examples of wrong early termination rather than giving a population-rate statistic.

> “We continue now with the discussion of the two examples … which LCRankNet erroneously terminated early.”  
> Wistuba and Pedapati, 2020, Sec. 4.  
> URL: https://arxiv.org/pdf/2006.03361

[SOURCE] It also identifies a fitted-curve limitation in the Domhan method.

> “Domhan et al. (2015)’s method underestimates performance when the learning curve is short.”  
> Wistuba and Pedapati, 2020, Sec. 4.  
> URL: https://arxiv.org/pdf/2006.03361

[SOURCE] Their operational mitigation was a no-stop grace period.

> “We follow the recommendation by Domhan et al. (2015) and do not end processes before we have seen the first 30 epochs.”  
> Wistuba and Pedapati, 2020, Sec. 4.  
> URL: https://arxiv.org/pdf/2006.03361

### Patience or “still climbing” measures

[SOURCE] Steven Adriaensen, Herilalaina Rakotoarison, Samuel Müller, and Frank Hutter, *Efficient Bayesian Learning Curve Extrapolation using Prior-Data Fitted Networks* (NeurIPS, 2023), compares extrapolation with a `Patience(k)` heuristic.

> “A criterion Patience(k) … terminate[s] a training run when model performance did not improve for k epochs.”  
> Adriaensen et al., 2023, Sec. 4.3.  
> URL: https://arxiv.org/html/2310.20447

[SOURCE] This is a no-improvement measure, not a fitted slope over the last `k` steps. In the paper’s model-selection experiment, termination is instead based on the chance of beating best-so-far:

> “Decide to stop the current run if that probability does not exceed some fixed threshold `delta`.”  
> Adriaensen et al., 2023, Sec. 4.3.  
> URL: https://arxiv.org/html/2310.20447

[SOURCE] The conditions are a total budget of 20 full runs (`20m`), 40 random run orderings per task, 53 tasks across LCBench, NAS-Bench-201, Taskset, and PD1, with confidence `1 - delta = 0.95`. Coarse checks occur at 10%, 20%, 40%, and 80% of the horizon; fine checks occur each epoch after the first.

[SOURCE] The reported outcome is regret/speedup, not false-drop count: fine-grained LC-PFN had lower-regret speedups of about 3.3x on LCBench and Taskset, and 2x to 6x speedups on 45 datasets.

> “On NAS-Bench-201, we find that all termination criteria considered, including standard Patience heuristics, fail on all 3 tasks.”  
> Adriaensen et al., 2023, Sec. 4.3.  
> URL: https://arxiv.org/html/2310.20447

[SOURCE] Their source-stated condition for this failure is an inflection-point curve shape outside the learned prior.

> “This is likely related to the particular shape of learning curves on this benchmark, having an inflection point … not resembling any in the prior.”  
> Adriaensen et al., 2023, Sec. 4.3.  
> URL: https://arxiv.org/html/2310.20447

### False-drop rates

[UNVERIFIED] Across the opened foundational papers, no standardized false-drop rate was found. The papers report prediction quality, recovery of a selected optimum, average regret, speedup, examples of incorrect stops, or ASHA’s **mispromotions**. None gives the requested rate with a consistent denominator such as “stopped candidates that would be top-`k` at full fidelity.”

[DERIVED] Search regret is not a false-drop rate: a low regret can coexist with false stops that did not change the best eventual selected candidate, while zero false stops may still not establish the quality of the remaining search.

**What the sources say.** [SOURCE] The dominant stopping rules are probability of beating best-so-far from a fitted curve, predicted final-value threshold with a safety factor, direct pairwise ranking probability, and no-improvement patience. [SOURCE] They establish speedup and regret under substantial candidate populations and iterative metrics, but the requested false-drop percentage is generally not reported; documented failures include short-curve underestimation, curve crossings, and unfamiliar inflection-point shapes.

## 3. Multi-Fidelity With a Fixed Total Budget Known in Advance

**Mechanism, in two lines.** [SOURCE] SH is natively fixed-budget: it takes a total budget and a chosen number of candidates, then reallocates resource by ranking. Hyperband makes the unknown starting-count decision by executing a finite collection of brackets, each constructed to cost about the same `B`.

### Full-trial baseline

[DERIVED] With total budget `C` and full trial cost `R`, a uniform full-trial plan can afford:

```text
N_full_uniform = floor(C / R)
```

Each candidate is a full evaluation and every one of these `N_full_uniform` candidates reaches full fidelity.

### Finite SH bracket

[SOURCE] Jamieson and Talwalkar’s SH accepts both a budget and a candidate count.

> “The input to Successive Halving is a set of `n` arms and a budget `B`.”  
> Jamieson and Talwalkar, 2016, Algorithm 1.  
> URL: https://proceedings.mlr.press/v51/jamieson16.pdf

[DERIVED] For a planned finite `s + 1`-rung SH bracket, with `R = r * eta^s`, the standard accounting is:

```text
C ≈ (s + 1) * n * r
```

so the count that fits a known total budget is:

```text
n ≈ floor(C / ((s + 1) * r))
  = floor((C / R) * eta^s / (s + 1))
```

[DERIVED] Ignoring floor effects, the number reaching `R` is:

```text
n_full ≈ n / eta^s
       ≈ C / ((s + 1) * R)
```

[DERIVED] Thus the entire budget determines both initial candidates and full-fidelity candidates after choosing `eta`, rung depth `s`, and minimum fidelity `r`. Integer floors and ceilings must be applied to get the actual submitted run counts.

### Complete Hyperband cycle

[SOURCE] Hyperband’s bracket formulas define `n_s` and `r_s` from `R`, `eta`, and bracket index `s`, and state that a complete execution has finite cost `(s_max + 1)B`.

> “A single execution of Hyperband takes a finite budget of `(s_max + 1)B`.”  
> Li et al., 2018, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[DERIVED] Under Hyperband’s definitions:

```text
s_max = floor(log_eta(R / r_min))
B = (s_max + 1) * R
C_cycle = (s_max + 1)^2 * R
```

[DERIVED] For a known total budget `C_total`, the number of complete Hyperband cycles that fit is:

```text
L = floor(C_total / C_cycle)
```

[DERIVED] The fixed submitted initial-run count from those complete cycles is:

```text
N_initial = L * sum from s=0 to s_max of
              ceil((B / R) * eta^s / (s + 1))
```

[DERIVED] The exact number reaching full fidelity comes from applying the source’s `floor(n_i / eta)` survivor rule inside every bracket. It is not equal to `C_total / R`, because most resource is intentionally assigned to partial rungs.

### ASHA and a fixed submitted run count

[SOURCE] ASHA differs from finite Hyperband because it can continue launching bottom-rung trials until an external stop condition is met.

> “ASHA does not require the user to pre-specify the number of configurations to evaluate.”  
> Li et al., 2020, Sec. 3.2.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[SOURCE] The same paper’s production-system discussion treats stopping as a caller-level choice.

> “The stopping criterion can be a number of configurations, compute time, or a performance threshold.”  
> Li et al., 2020, Sec. 5.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[DERIVED] When the run count must be fixed at submission, ASHA’s open-ended scheduling property does not itself derive that count. A finite implementation must precompute a finite bracket or a finite sequence of rungs under the `C` equations above.

### Published fixed-budget comparison

[SOURCE] BOHB makes explicit that each SH run is capped by a bracket cost and compares its worst case with full-fidelity random search.

> “As every SH run consumes a budget of at most `(s_max + 1) * b_max` … in the worst case (when the lower fidelities are misleading), BOHB is at most this factor times slower than RS.”  
> Falkner, Klein, and Hutter, 2018, Sec. 4.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1807.01774

[SOURCE] This comparison assumes a continuing series of SH runs, a uniform-random fraction `rho`, and a fidelity whose maximum `b_max` is the target objective; it is not a formula for a user-submitted finite candidate count.

**What the sources say.** [SOURCE] Fixed total resource can derive a finite SH/Hyperband schedule directly once minimum fidelity, maximum fidelity, rung depth, and reduction factor are fixed. [SOURCE] SH needs the initial candidate count as an input; Hyperband derives multiple such counts for a finite complete cycle; ASHA’s core algorithm deliberately leaves total candidate count to an external stopping criterion.

## 4. Promotion When Candidates Are Few: Two to Six

**Mechanism, in two lines.** [SOURCE] SH reduces a population at each rung by a factor `eta`; with a tiny population, floor/ceiling choices rapidly make the method a one-stage screen plus one or a few full evaluations. The literature’s formal and empirical arguments primarily study larger candidate pools, not two to six.

### What SH and Hyperband say about the allocation decision

[SOURCE] Hyperband frames its core uncertainty as the choice between exploring many short evaluations and deeply evaluating a smaller set.

> “For a fixed `B`, it is not clear a priori whether we should (a) consider many configurations … or (b) consider a small number of configurations.”  
> Li et al., 2018, Sec. 3.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] The authors identify conditions favoring a smaller initial population: slow convergence or small ultimate score gaps.

> “When the envelopes are wide or the final losses are close, more resources are required before configurations can be reliably distinguished.”  
> Li et al., 2018, Sec. 3.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[SOURCE] Their LeNet scale was not tiny: `R = 81`, `eta = 3`, and the five brackets started 81, 34, 15, 8, and 5 configurations.

> “We set `R` to 81 and use the default value of `eta = 3`, resulting in `s_max = 4` and thus 5 brackets.”  
> Li et al., 2018, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[DERIVED] Of that paper’s five brackets, only the `s = 0` bracket starts at five full trials and `s = 1` starts at eight candidates. It does not report an experiment beginning with two to six total choices.

### ASHA’s small-population relevance

[SOURCE] ASHA’s error argument expressly relies on many observations in a rung.

> “The number of mispromoted configurations is roughly `sqrt(n)`.”  
> Li et al., 2020, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

[DERIVED] With two to six initial candidates, an `eta = 2` rung has one to three promotions and `eta = 3` has zero to two after integer rounding. There are too few comparison observations for the cited large-`n` mispromotion fraction argument to be informative.

[SOURCE] ASHA’s reported architecture-search experiment used 16 workers, `eta = 4`, and `R = 300` epochs, not a small fixed candidate list.

> “We use 16 workers, a maximum resource `R = 300`, and `eta = 4`.”  
> Li et al., 2020, Sec. 4.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1810.05934

### Fixed partial budget per candidate versus halving

[UNVERIFIED] No opened primary source directly tests the requested head-to-head condition: two to six fixed candidates, the same fixed total budget, and a single fixed partial budget for every candidate versus multi-rung SH promotion.

[SOURCE] Hyperband’s `s = 1` bracket is structurally a two-stage version of that comparison: evaluate candidates at a fixed initial fidelity, retain top `1 / eta`, then evaluate survivors at full fidelity.

[SOURCE] In its `R = 81`, `eta = 3` example, that bracket begins eight configurations at 27 epochs and advances approximately two to 81 epochs. The source’s reported comparison averages 70 trials of each bracket.

> “We ran Hyperband and each of the individual brackets for 70 trials.”  
> Li et al., 2018, Sec. 3.3.  
> URL: https://ar5iv.labs.arxiv.org/html/1603.06560

[UNVERIFIED] The paper does not publish a numerical ablation isolating the one-stage partial-screen version against a multi-rung version at population sizes two through six.

### Model-based methods with low sample counts

[SOURCE] BOHB delays use of its KDE model until enough observations exist.

> “BOHB always uses the model for the largest budget for which enough observations are available.”  
> Falkner, Klein, and Hutter, 2018, Sec. 4.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1807.01774

[SOURCE] Its minimum observations depend on search-space dimension, not only candidate count.

> “We use `N_min = d + 1` observations before fitting a KDE.”  
> Falkner, Klein, and Hutter, 2018, Sec. 4.1.  
> URL: https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf

[DERIVED] For a small candidate list, this source does not support expecting a model-based selector to fit unless the number of observations exceeds the hyperparameter-space dimension plus one.

**What the sources say.** [SOURCE] SH literature recognizes that slow separation and close final scores favor more resource per candidate, but its published evidence does not establish a winner between one partial screen and repeated halving for two to six choices. [SOURCE] ASHA’s promotion-error rationale and empirical target regime are large populations; fixed-partial versus halving at the requested small scale was not found.

## 5. Fidelity That Changes the Problem’s Shape

**Mechanism, in two lines.** [SOURCE] Multi-fidelity methods assume a lower-cost result contains information about the high-fidelity result, but sources document that rankings can change with fidelity. [UNVERIFIED] A controlled primary study specifically measuring “smaller search space through local repair” against “same search space trained shorter” was not found in the opened literature.

### Budget-induced rank changes

[SOURCE] Arber Zela, Aaron Klein, Stefan Falkner, and Frank Hutter, *Towards Automated Deep Learning: Efficient Joint Neural Architecture and Hyperparameter Search* (2018), directly measured rank correlation between shorter and longer runs.

> “The ranking of the top configurations cannot be deduced from the ranking of much shorter runs only.”  
> Zela et al., 2018, Sec. 4.3.  
> URL: https://arxiv.org/html/1807.06906

[SOURCE] Conditions: joint search of ten architecture decisions and seven hyperparameters on CIFAR-10; 400-second, 1,200-second, one-hour, and three-hour budgets; `eta = 3`; 256 three-hour-equivalent evaluations; total 32 GPU-days.

[SOURCE] Reported Spearman correlations of validation-error ranks were:

| Budget pair | Spearman rank correlation |
|---|---:|
| 400 seconds to 1,200 seconds | 0.87 |
| 1,200 seconds to 1 hour | 0.88 |
| 1 hour to 3 hours | 0.86 |
| 400 seconds to 1 hour | 0.31 |
| 1,200 seconds to 3 hours | 0.64 |
| 400 seconds to 3 hours | 0.05 |

Zela et al., 2018, Table 1.  
URL: https://arxiv.org/html/1807.06906

[SOURCE] The paper reports a bias that makes the low correlation notable rather than a random-sampling artifact.

> “The 3 hour results are biased towards configurations which perform well at lower budgets.”  
> Zela et al., 2018, Sec. 4.3.  
> URL: https://arxiv.org/html/1807.06906

[DERIVED] A rank correlation of 0.05 between 400 seconds and three hours reports almost no rank association in that selected study. This is a training-time fidelity result, not a local-search-space restriction result.

### Explicit literature warning on low/high fidelity rank correlation

[SOURCE] Martin Wistuba, Arlind Kadra, and Josif Grabocka, *Supervising the Multi-Fidelity Race of Hyperparameter Configurations* (NeurIPS, 2022), state the general fidelity issue.

> “The low-budget (few epochs) performances are not always a good indicator for the full-budget (full convergence) performances.”  
> Wistuba, Kadra, and Grabocka, 2022, Sec. 1.  
> URL: https://arxiv.org/html/2202.09774

[SOURCE] Their concrete mechanism is a curve crossing due to regularization.

> “A properly regularized network converges slower in the first few epochs, however, typically performs better than a non-regularized variant after the full convergence.”  
> Wistuba, Kadra, and Grabocka, 2022, Sec. 1.  
> URL: https://arxiv.org/html/2202.09774

[SOURCE] Their conditions include 35 LCBench data sets with 2,000 networks each trained 50 epochs, 12 TaskSet NLP tasks, and NAS-Bench-201 with 15,625 architectures trained 200 epochs.

[SOURCE] They define a high-budget-good configuration as top-third at a budget and bad if it was in the bottom two-thirds at at least one lower budget. Under that measure:

> “The ground truth percentage reaches 40% on LCBench and 80% on NAS-Bench-201.”  
> Wistuba, Kadra, and Grabocka, 2022, Sec. 5, Experiment 3.  
> URL: https://arxiv.org/html/2202.09774

[DERIVED] This 40%/80% statistic is a rank-reversal/promotion-conflict proxy, not a false-elimination percentage for a particular scheduler.

### Low-fidelity function approximation and search-space complexity

[SOURCE] BOHB defines low fidelity as an approximation rather than an equivalent objective.

> “With `b < b_max`, [the low-fidelity function] is only an approximation … whose quality typically increases with `b`.”  
> Falkner, Klein, and Hutter, 2018, Sec. 3.2.  
> URL: https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf

[SOURCE] BOHB’s protection against misleading low fidelity is eventually to model the highest budget with enough data.

> “This enables it to overcome wrong conclusions drawn on smaller budgets by eventually relying on results with the highest fidelity only.”  
> Falkner, Klein, and Hutter, 2018, Sec. 4.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1807.01774

[SOURCE] Its stated worst case is lower fidelity being misleading.

> “In the worst case (when the lower fidelities are misleading), BOHB is at most this factor times slower than RS.”  
> Falkner, Klein, and Hutter, 2018, Sec. 4.1.  
> URL: https://ar5iv.labs.arxiv.org/html/1807.01774

[SOURCE] BOHB reports that increasing search dimension can make lower-budget information less useful. In its counting-ones experiments, 64 dimensions caused noise-related degradation.

> “With as many as 64 dimensions, TPE and SMAC started to perform better than BOHB since the noise grows.”  
> Falkner, Klein, and Hutter, 2018, Sec. 5.1.  
> URL: https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf

### A source using lower data fidelity as a different problem

[SOURCE] Hanlin Gu, Heng Wang, and Hongxu Chen, *Accelerating Hyperparameter Optimization of Deep Neural Network via Progressive Multi-Fidelity Evaluation* (IEEE Access, 2020), explicitly treats data-subset evaluation as a fidelity with bias.

> “The evaluation performance on the data subset is biased in different cases.”  
> Gu, Wang, and Chen, 2020, Sec. 3.  
> URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7206157/

[SOURCE] Its proposed response is simultaneous progression in epochs and data fidelity.

> “The configurations are first evaluated with a small number of epochs and low fidelity. After filtering … we dynamically increase the number of epochs and fidelity simultaneously.”  
> Gu, Wang, and Chen, 2020, Sec. 3.  
> URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7206157/

[SOURCE] Its reported conditions include LeNet on MNIST/CIFAR-10, an initial 10% data subset comparison, and a wall-clock comparison in which BOHB took 31 hours for 16 resource units versus 19 hours for FastHO.

> “BOHB takes 31 h … In contrast, FastHO takes only 19 h which is 63% faster than BOHB.”  
> Gu, Wang, and Chen, 2020, Sec. 4.  
> URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7206157/

[DERIVED] This is evidence that an approximation which changes available training data can create low-fidelity bias. It is analogous in kind, but not evidence that a bounded local repair of a game build has a particular correlation with a global rebuild.

### Search-space restriction specifically

[UNVERIFIED] No opened paper reports a rank-correlation number for the specific fidelity transformation “optimize only a bounded local subspace” versus “rebuild/optimize the complete space,” while holding the candidate identity and full evaluator fixed.

[DERIVED] A partial local repair is not merely a shorter run if its optimizer cannot access the tree, gear, or configuration alternatives reachable by a full rebuild. The quoted training-time and data-subset studies establish the general failure mode, rank changes under a proxy, and the need for empirical correlation; they do not quantify that local-repair correlation.

**What the sources say.** [SOURCE] Lower fidelity can reverse rankings: the cited rank correlation falls to 0.05 for 400 seconds versus three hours, and a cited high-budget-good/low-budget-bad proxy reaches 40% to 80% in benchmark settings. [UNVERIFIED] No source was found that measures the requested smaller-search-space local-repair fidelity directly, so its rank relationship is not established by the training-shorter literature.

## 6. Engineering Write-Ups: Build and Configuration Optimizers That Pay in Steps

**Mechanism, in two lines.** [SOURCE] Systems and compiler optimizers typically avoid measuring every candidate at maximum cost by using short evaluations, learned cost models, or search-strategy budget allocation. [SOURCE] The closest direct staged “rank then promote to more expensive evaluation” system found is Dremel; compiler autotuners more commonly use cheap prediction followed by selected expensive measurements.

### 1. Dremel: RocksDB configuration tuning

[SOURCE] Chenxingyu Zhao, Tapan Chugh, Jaehong Min, Ming Liu, and Arvind Krishnamurthy, *Dremel: Adaptive Configuration Tuning of RocksDB KV-Store* (SIGMETRICS, 2022), uses Successive Halving across workload replay durations.

> “Each round runs all configurations with a time budget, collects performance metrics for all configurations, performs an early stop for the worst half, and repeats until one configuration remains.”  
> Zhao et al., 2022, Sec. 4.  
> URL: https://homes.cs.washington.edu/~arvind/papers/dremel.pdf

[SOURCE] The reported setting is a RocksDB configuration space with millions of configurations, represented in one evaluation by four quantized fused features giving `5^4 = 625` arms, across 18 workload/hardware settings. Full workload replays can take tens of minutes or hours.

[SOURCE] Its source condition for promotion is probabilistic, not a guarantee.

> “A configuration that performs poorly for a short time is more likely to perform poorly for a longer time.”  
> Zhao et al., 2022, Sec. 4.  
> URL: https://homes.cs.washington.edu/~arvind/papers/dremel.pdf

[SOURCE] Its stated failure condition is therefore the weak point of stepwise replay: short-time rankings can fail to predict longer-time rankings, with workload and hardware behavior changing the outcome.

### 2. TVM: learned ranking, then hardware measurement

[SOURCE] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Meghan Cowan, Haichen Shen, Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin, and Arvind Krishnamurthy, *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning* (OSDI, 2018), explores compiler schedules with a learned cost model and selected real measurements.

> “Once we choose a cost model, we can use it to select promising configurations on which to iteratively run real measurements.”  
> Chen et al., 2018, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi18-chen.pdf

[SOURCE] The system measures runtime on target hardware, which is materially expensive relative to prediction.

> “Performance on real hardware … can be on the order of seconds depending on the specific workload/hardware target.”  
> Chen et al., 2018, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi18-chen.pdf

[SOURCE] TVM uses rank rather than absolute-runtime prediction because the measurement batch only needs an ordering.

> “Since the explorer selects the top candidates based only on the relative order of the prediction … we need not predict the absolute execution times directly.”  
> Chen et al., 2018, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi18-chen.pdf

[SOURCE] In the cited system, tree boosting predicts in about 0.67 ms, compared with hardware measurements on the order of seconds.

> “On average, the tree boosting model does prediction in 0.67 ms, thousands of times faster than running a real measurement.”  
> Chen et al., 2018, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi18-chen.pdf

[SOURCE] Its search condition is a very large schedule space; source text describes “billions of possible configurations” for real-world operators. Its stated limitation is that the learned ranker must be cheaper than measurements and must improve from measured data; early random seeds can be weak.

### 3. Ansor: complete-program search, cost-model ranking, hardware measurement

[SOURCE] Lianmin Zheng, Chengfan Jia, Minmin Sun, Zhao Wu, Cody Hao Yu, Ameer Haj-Ali, Yida Wang, Jun Yang, Danyang Zhuo, Koushik Sen, Joseph E. Gonzalez, and Ion Stoica, *Ansor: Generating High-Performance Tensor Programs for Deep Learning* (OSDI, 2020), constructs complete tensor programs, ranks large batches cheaply, and measures only selected programs.

> “At each iteration, we first use evolutionary search to find a small batch of promising programs according to a learned cost model. We then measure these programs on hardware to get the actual execution time cost.”  
> Zheng et al., 2020, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi20-zheng.pdf

[SOURCE] Its cost condition is a huge low-level annotation space: tile sizes, parallelism, unrolling, and vectorization create billions of possibilities, while the learned model can compare many cheaply.

> “It allows us to compare tens of thousands of programs in the search space in seconds, and pick the promising ones to do actual measurements.”  
> Zheng et al., 2020, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi20-zheng.pdf

[SOURCE] The system reports typically fewer than 30,000 measured programs and fewer than ten high-level sketches per subgraph.

> “We train the cost model on-the-fly with measured programs (typically less than 30,000).”  
> Zheng et al., 2020, presentation accompanying OSDI paper.  
> URL: https://www.usenix.org/sites/default/files/conference/protected-files/osdi20_slides_zheng.pdf

[SOURCE] Its stated failure condition is that random programs have broad coverage but not guaranteed quality, and that predicting from incomplete programs is unreliable.

> “The performance of randomly sampled programs is not necessarily good.”  
> Zheng et al., 2020, Sec. 5.  
> URL: https://www.usenix.org/system/files/osdi20-zheng.pdf

### 4. CompilerGym: compiler pass and flag search

[SOURCE] Chris Cummins, Bram Wasti, Jiadong Guo, Brandon Cui, Jason Ansel, Sahir Gomez, Somya Jain, Jia Liu, Olivier Teytaud, Benoit Steiner, Yuandong Tian, and Hugh Leather, *CompilerGym: Robust, Performant Compiler Optimization Environments for AI Research* (CGO, 2022), provides pass-order and flag-search environments for methods with explicit evaluation budgets.

> “The action space consists of a discrete choice from 124 optimization passes extracted automatically from LLVM.”  
> Cummins et al., 2022, Sec. 4.  
> URL: https://arxiv.org/html/2109.08267

[SOURCE] Its explicit stopping condition is open-ended compiler pass repetition.

> “There is no maximal episode length as episodes can run forever … the user must estimate when no further gains can be achieved.”  
> Cummins et al., 2022, Sec. 4.  
> URL: https://arxiv.org/html/2109.08267

[SOURCE] The reported evaluation condition includes cBench autotuning for one hour, repeated ten times. Runtime reward uses median of three measurements during search and 30 for final reporting.

[SOURCE] Its stated failure modes include compiler crashes, timeouts, infinite loops, out-of-memory conditions, runtime nondeterminism, and platform-specific reward measurements.

### 5. OpenTuner: adaptive budget by search strategy

[SOURCE] Jason Ansel, Shoaib Kamil, Kalyan Veeramachaneni, Jonathan Ragan-Kelley, Jeffrey Bosboom, Una-May O’Reilly, and Saman Amarasinghe, *OpenTuner: An Extensible Framework for Program Autotuning* (PACT, 2014), reallocates evaluations between search techniques rather than between candidate fidelities.

> “Techniques which perform well will receive larger testing budgets and techniques which perform poorly will be disabled.”  
> Ansel et al., 2014.  
> URL: https://github.com/jansel/opentuner

[SOURCE] Its condition is application-defined candidate representations and program-measurement cost; no universal candidate count or rung budget is specified.

[SOURCE] Its stated limitation is that no one search technique or representation is universally best.

> “No single search technique performs best for every problem.”  
> Ansel et al., 2014.  
> URL: https://github.com/jansel/opentuner

**What the sources say.** [SOURCE] Dremel is a direct production-style example of successive-halving time-budget promotion for expensive configuration replays. [SOURCE] TVM and Ansor use a different stepwise pattern: model-predict/rank many candidates, measure a selected batch, retrain the ranker, and repeat. [SOURCE] Compiler optimization sources explicitly identify noisy hardware measurements, huge search spaces, failures/timeouts, and weak early rankings as operational constraints.

## Comparison Table

| Method | Source | Cost per candidate relative to a full trial | Needs | Source’s own stated failure mode |
|---|---|---:|---|---|
| Successive Halving | Jamieson and Talwalkar, 2016, https://proceedings.mlr.press/v51/jamieson16.html | [DERIVED] Rung `i`: `r * eta^i / R`; ideal bracket total `(s + 1)nr / R` | [SOURCE] Fixed total budget `B`, initial arm count `n`, comparable intermediate loss | [SOURCE] Requires `n`; wrong `n` creates the exploration versus per-candidate-resource problem |
| Hyperband | Li et al., 2018, https://www.jmlr.org/papers/v18/16-558.html | [DERIVED] Complete cycle `(s_max + 1)^2` full-trial equivalents; individual brackets about `(s + 1)n_sr_s / R` | [SOURCE] Maximum resource `R`, minimum resource, `eta`, lower-fidelity signal | [SOURCE] Aggressive brackets may be “throwaways”; too-small `R` may not distinguish candidates; initialization/validation overhead matters |
| ASHA | Li et al., 2020, https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf | [DERIVED] In `eta=4`, `r=R/256` five-rung ideal bracket: `5R` cumulative, `4R` resumable incremental | [SOURCE] Monotonic resource, intermediate metric, enough workers/candidates, checkpoints for resumed work | [SOURCE] Incorrect asynchronous promotions; reproducible resumption requires model, optimizer, RNG, and data-generator state |
| Curve extrapolation | Domhan et al., 2015, https://www.ijcai.org/Proceedings/15/Papers/487.pdf | [SOURCE] Variable; checks every 30 epochs in cited study, stops when posterior chance to beat incumbent is below threshold | [SOURCE] Partial learning curve, maximum horizon, fitted curve family and uncertainty model | [SOURCE] Model can be wrong; later work reports short-curve underestimation |
| Pairwise curve ranking | Wistuba and Pedapati, 2020, https://proceedings.mlr.press/v119/wistuba20a.html | [SOURCE] Variable; cited run terminates at every third epoch after a 30-epoch grace period | [SOURCE] Partial curves, incumbent, model/data for ranking or transfer | [SOURCE] Promising runs may be terminated; examples show erroneous early termination |
| BOHB | Falkner, Klein, and Hutter, 2018, https://proceedings.mlr.press/v80/falkner18a.html | [DERIVED] Hyperband bracket cost; high-budget model only after enough observations | [SOURCE] Fidelity hierarchy, `eta`, KDE data with `N_min = d + 1`, random exploration fraction | [SOURCE] Lower fidelities can mislead; low-budget work can become constant overhead at large budgets |
| Dremel | Zhao et al., 2022, https://homes.cs.washington.edu/~arvind/papers/dremel.pdf | [SOURCE] Increasing workload replay-time budgets; worst half removed each round | [SOURCE] Short replay performance informative of longer replay; configuration representation | [SOURCE] Short-run performance is only more likely, not guaranteed, to indicate long-run performance |
| TVM autotuning | Chen et al., 2018, https://www.usenix.org/system/files/osdi18-chen.pdf | [SOURCE] Model prediction about 0.67 ms; physical measurement can be seconds | [SOURCE] Measured seed data, cost model cheaper than hardware measurement, target hardware | [SOURCE] Cost model can be inaccurate; early data is weak and measurements are noisy/hardware-specific |
| Ansor autotuning | Zheng et al., 2020, https://www.usenix.org/system/files/osdi20-zheng.pdf | [SOURCE] Cheap ranking of tens of thousands in seconds; only selected programs receive hardware measurements | [SOURCE] Valid complete-program generator, learned cost model, target hardware | [SOURCE] Random samples are not necessarily good; incomplete-program prediction is unreliable |
| CompilerGym | Cummins et al., 2022, https://arxiv.org/html/2109.08267 | [SOURCE] Search-defined; runtime reward uses three runs during search, 30 final runs | [SOURCE] Compiler environment, termination/time policy, target-specific objective | [SOURCE] No natural maximum pass-order length; crashes, timeouts, OOM, and nondeterministic runtime occur |
| OpenTuner | Ansel et al., 2014, https://github.com/jansel/opentuner | [SOURCE] Application-defined program measurements; budget promoted between techniques | [SOURCE] A suitable configuration representation and measurable objective | [SOURCE] No one technique or representation is best for every problem |

## URLs Opened

1. https://proceedings.mlr.press/v51/jamieson16.html
2. https://proceedings.mlr.press/v51/jamieson16.pdf
3. https://www.jmlr.org/papers/v18/16-558.html
4. https://ar5iv.labs.arxiv.org/html/1603.06560
5. https://openreview.net/forum?id=ry18Ww5ee
6. https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf
7. https://ar5iv.labs.arxiv.org/html/1810.05934
8. https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.AsyncHyperBandScheduler.html
9. https://proceedings.mlr.press/v80/falkner18a.html
10. https://proceedings.mlr.press/v80/falkner18a/falkner18a.pdf
11. http://proceedings.mlr.press/v80/falkner18a/falkner18a-supp.pdf
12. https://ar5iv.labs.arxiv.org/html/1807.01774
13. https://www.ijcai.org/Proceedings/15/Papers/487.pdf
14. https://mlanthology.org/iclr/2017/klein2017iclr-learning/
15. https://arxiv.org/html/1705.10823
16. https://proceedings.mlr.press/v119/wistuba20a.html
17. https://proceedings.mlr.press/v119/wistuba20a/wistuba20a.pdf
18. https://arxiv.org/pdf/2006.03361
19. https://arxiv.org/html/2310.20447
20. https://arxiv.org/html/1807.06906
21. https://arxiv.org/html/2202.09774
22. https://pmc.ncbi.nlm.nih.gov/articles/PMC7206157/
23. https://homes.cs.washington.edu/~arvind/papers/dremel.pdf
24. https://www.usenix.org/system/files/osdi18-chen.pdf
25. https://www.usenix.org/conference/osdi18/presentation/chen
26. https://www.usenix.org/system/files/osdi20-zheng.pdf
27. https://www.usenix.org/conference/osdi20/presentation/zheng
28. https://www.usenix.org/sites/default/files/conference/protected-files/osdi20_slides_zheng.pdf
29. https://tvm.apache.org/2021/03/03/intro-auto-scheduler
30. https://arxiv.org/html/2109.08267
31. https://github.com/facebookresearch/CompilerGym
32. https://github.com/jansel/opentuner