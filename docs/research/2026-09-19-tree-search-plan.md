# The tree search after day 1: what the literature offers and what we take (the lead's reading, 2026-09-19)

Status 20:30: rewritten after two ChatGPT Deep Research reports (the user ran the lead's prompts):
`inbox/2026-09-19-chatgpt-deep-research-A.md` (diagnose and rebuild; 70 KB, ~45 sources opened) and
`inbox/2026-09-19-chatgpt-deep-research-B.md` (plan the whole solution; 83 KB, ~60 sources). Both label every
statement [SOURCE] / [DERIVED] / [UNVERIFIED] and say "not found" where they found nothing. The lead read both in full
and checked three load-bearing quotes against the primary pages (verbatim matches: Uchoa-Werneck's four local
searches in O(m log n), ACM JEA; Disser et al.'s "no incremental solution exists that simultaneously approximates the
optimum for all budgets", arXiv 2407.04447; "Dynamic Partial Removal ... adaptive destruction", arXiv 2005.09330).
Two publisher sites sat behind a captcha and were not opened. The GPT Astra deep research is still to come; the two
earlier GPT reports (GitHub-only; from memory) are superseded and kept only as history. NOTHING here is specified for
a worker yet: the user decides after the Astra report.

## Addendum 01:00 (20.09): experiment A is back, and it is NEGATIVE (`2026-09-19-whole-tree-mip-experiment.md`)

Six delivered smoke builds, node weights from 3,874-3,881 fast what-ifs each (32-109 s), HiGHS 60 s per solve, PoB
judges every proposal, rails floors (the run files do not persist the author floors).

| | result |
|---|---|
| proposals that improved an incumbent while feasible | 0 of 24 |
| actual / predicted gain at Hamming radius 10 | -0.48 .. -65 (cold_dot: predicted +11%, actual -22%, and FEASIBLE: a pure value misprediction) |
| proposals that broke a floor | 18 of 24 (violations 0.003 .. 1.4) |
| unrestricted solve | the incumbent itself (gap 18-34% at the time limit) on 3 builds; on the other 3 a 108-136 node rewrite predicted at +175% .. +1,255% and worth ~0.3x the incumbent |

The lead's reading. (1) The additive model around a finished build does not predict even ten changes: item 3 of the
plan ("the only method that plans the whole tree at once") is OFF the main line, as the reports warned ("an exact solver
is exceptionally good at finding where the surrogate is wrong"). (2) Two causes are visible and they are different:
floors are thresholds the surrogate cannot see (each defensive node alone costs nothing to remove, ten together break
the floor), and the VALUE itself is mispredicted (cold_dot). The first is repairable -- the same what-ifs return every
floor stat, so floors can be linear constraints of the MIP; the second is not understood. (3) Consequences for the
order of work: **B is the main line** (its moves are judged by PoB one at a time; the surrogate only proposes
candidates); **C changes its method**: not "re-solve the MIP on the union of the seeds" but PoB-judged exchange of
whole branches between the seeds' trees (the path-swap machinery with candidates taken from the other seeds);
**gear-as-MIP stays parked** (`2026-09-19-components-plan.md` item 3) until a diagnostic says a surrogate with explicit
floors is trustworthy at radius <= 10. (4) One cheap diagnostic, low priority, same harness: floors as linear
constraints with a margin; the D = 10 proposal applied in halves (removals only / adds only) and node by node on
cold_dot, to name what the single-node weights miss (a proof holder under the frozen config? a mastery? a "per X"
node?). (5) The removal-delta map of B's item 1 uses the same single-node numbers: B ranks REGIONS with them and lets
PoB judge completed replacements, which is the use this result still allows; it must never sum them.

## Addendum 22:20: what the three later researches change HERE (judging with few runs, screening, interdependent components)

Plans: `2026-09-19-judging-plan.md`, `2026-09-19-screening-plan.md`, `2026-09-19-components-plan.md`. The order A -> B -> C
stands. Four amendments:

1. **B's acceptance.** "Value on the smoke six" cannot carry a verdict: measured on our own campaigns, the smoke
   protocol sees only effects of ~15% (identical code on other seeds shows -2.0% at the median and -14.5% on
   cold_dot). B is accepted on its structural counts (never-reconsidered share 22% -> below 5%, trunk churn, reverted
   moves and their seconds) and on a REPLAY BENCH: the new moves run from the 96 delivered builds of the rules
   campaigns, gain and seconds per build -- experiment A's harness made general. The smoke run is only the alarm.
2. **C (union of seeds) gains weight.** The same seed does not carry over between code versions (r = +0.10), one
   build's noise is 15%, best-of-3 is worth +10.7% over the median seed: the seeds are our largest unexploited
   resource, and C is the one item that uses all three instead of throwing two away. The product-side ideas of the
   other plans (dropping a trailing seed after loop pass 1; 4 finalists x 1 seed instead of 2 x 3) are decided only
   after C is measured, because they take C's material away.
3. **Item 5 stays downgraded**, against the advice of both component reports (a bandit scheduler): their evidence is
   from continuous optimization, item 5's is from 25 ALNS implementations. The reporting block is extended from tree
   operators to every move of the loop; a tuned fixed order first.
4. **Item 3's method is reused for gear** (one item per slot, resistance sums, attributes: a multiple-choice
   knapsack) only after A reports the ratio actual / predicted gain by radius.

## Addendum 21:30: the two GPT Astra reports (`inbox/2026-09-19-astra-deep-research-A.md`, `-B.md`), read in full

Four independent reports now agree on the frame (PoB stays the judge; structural moves from Steiner local search; what
to destroy from LNS; whole-tree planning only through an additive model with a trust region; union of seeds; no nesting
across budgets; "global gap unknown"). What Astra adds or corrects:

1. **Removal loss is not replacement opportunity** (Astra A, 3.2): "a branch with loss 100 and replacement recovery 150
   is a better rebuild opportunity than a branch with loss 1 and recovery 1.2". Ranking regions by weakest removal delta
   alone can systematically miss the valuable changes. Regions are diagnosed by COMPLETED replacements (cheap
   reconnections evaluated at 7 ms each), the removal delta is only one of the ordering signals. This corrects item 1
   of the table below.
2. **Atomic internal-path replacement comes first** (Astra A's priority 1): swap a corridor for a bypass while keeping
   everything downstream -- no regrow at all, 20 paths x 20 alternatives = 400 what-ifs = 2.8 s. With more than two
   retained components the connector must join all of them. A full-graph articulation has no bypass: then the move
   must include the descendants.
3. **A second repair policy is as important as a better destroy**: "a larger destroy set can still recreate the same
   greedy basin" (regret repair, bounded look-ahead; Ropke-Pisinger's own example of a partly removed group sliding
   back into the old route).
4. **Adaptation**: Ropke-Pisinger's own Table 3 has ALNS "on par" with the best simple configurations; the popular
   Python ALNS library's segmented roulette does not divide by usage count (not the original formula); original
   awards are (33, 9, 13), r = 0.1. Fixed schedule first, adaptation as an experiment -- as already planned.
5. **Interactions**: the pair probe J(A,B) = F(S) - F(S\A) - F(S\B) + F(S\(A u B)) costs one extra what-if per pair
   (45 pairs of ten groups = 0.4 s); Shapley / Banzhaf only on small local block games.
6. **Solvers** (Astra B): SCIP-Jack 2.2 is on request under the ZIB Academic License, Windows unverified -> not our
   first tool; HiGHS / PySCIPOpt / OR-Tools with a static single-commodity flow are (CP-SAT has no lazy constraints).
   An exact ILP for k-cardinality trees solves sparse 1,000-node instances in about 8 s on 2009 hardware (Chimani et
   al.): our surrogate is solver-seconds. Cyclomatic number ~196: "mostly tree-like" does not mean small treewidth,
   so a MIP, not a tree DP, on the full graph. Bosman's merging: GRASP gap 0.392% -> 0.061% in 6 s against 493 s for
   path relinking.
7. **Budgets do not nest, with a two-line counterexample on a tree** (two arms, prizes 5 and 100): budgets 100 and
   110 can share only the root. Loadout change = warm start + large rebuild + fresh construction, caches versioned by
   the evaluator's inputs.

A fact about OUR evaluator, measured by the lead (stormbrand s2, a trunk node with 30 dependents): PoB's fast what-if
does NOT cascade -- removing the node alone leaves FullDPS at 2,115,491 (only the node's own stats go), while the full
mode drops the 30 dependents (1,033,338). So disconnected sets are evaluable at 7 ms: a trunk node's intrinsic value is
directly measurable, and corridor exchanges can be scored atomically as long as WE guarantee the final set is
connected. (The reports assumed connected what-ifs only.)

**Revised order**: (A) the whole-tree MIP experiment, independent of `tree_optimizer.py`; (B) corridor replacement +
region challenge diagnosed by completed replacements + a second repair policy + the reporting block (trunk churn,
gain per second by operator, all seeds), after the judge fix merges; (C) union of seeds on A's solver; adaptation,
pair probes and acceptance rules only on evidence.

## Our own measurements (14 best builds of `core14-rules`, 1,411 points)

| if this node is cut, how many nodes fall | share | which move reconsiders it today |
|---|---:|---|
| 1 (a leaf) | 32% | refine, every pass |
| 2-6 | 38% | path swaps (weakest loss per point first), every pass |
| 7-12 | 8% | only the random kick |
| 13+ (the trunk) | 22% | nothing, ever, after construction |

The judge disagreed with the moves (202 reverted path-swap moves in 42 builds, 11,551 s, 117 kept swaps lost; fix in
work); the alternating loop earns a median +63% over construction; 34 of 42 builds end on a pass that keeps nothing;
the seed spread is 41.6 points at the median.

## What the two reports agree on

1. **Our problem has no ready-made solver and no guarantee**: the closest relatives are the rooted budgeted
   maximum-weight connected subgraph (additive) and connected submodular maximization; ours is neither. "Retain F as
   the acceptance oracle, borrow graph-structural neighbourhoods from Steiner optimization, borrow diagnosis and
   destruction scheduling from LNS" (report A). Exact optimality of an additive surrogate certifies nothing about the
   real objective (both reports).
2. **Spend cheap evaluations on choosing WHERE to rebuild, because rebuilding is what costs**: a 17 s node-power pass
   = 2,429 what-ifs; regrowing 20 nodes = 2,857-5,714 what-ifs; scoring 100 candidate regions by removal delta = 0.7 s.
3. **The trunk needs moves of its own**: key-path exchange and key-vertex elimination are exactly the interior-changing
   moves we lack (Uchoa-Werneck; implemented in SCIP's `heur_local.c`, readable in SteinerPy). Classical versions
   price moves by edge cost; for us edge arithmetic only GENERATES candidates, PoB accepts.
4. **Old solutions do not nest into new budgets in general** (Disser et al. 2024) and no local test can certify an
   old trunk under a black box (a two-line indistinguishability argument in report A): a loadout change must
   challenge the trunk, not freeze it.

## The plan, revised (order = value per cost; changes against the first draft marked)

| # | technique | what it gives | cost | evidence |
|---|---|---|---|---|
| 1 | **Removal-delta map + weakest connected region of any size**: every detachable component scored by F(S) - F(S \\ C), ranked per node; destroy-size buckets 4-6 / 7-12 / 13-20 / 21-30 | replaces the random kick; reaches the 8% and part of the 22% | ~1 s per map, 1-2 s per regrown node | worst removal and related removal (Shaw 1998; Ropke-Pisinger 2006), contiguous destruction (SISR, Christiaens-Vanden Berghe 2020) |
| 2 | **Trunk challenge = key-path exchange / key-vertex elimination, PoB as judge**; NEW detail: while regrowing, FORBID the old corridor, or greedy rebuilds the same trunk and the challenge tests nothing | the 22% trunk becomes movable | 7 ms per completed exchange candidate; alternatives from shortest paths | Uchoa-Werneck 2010/2012 (verified); SCIP `heur_local.c` |
| 3 | NEW, moved up: **exact additive solve as an experiment first** -- node power as weights, rooted + budgeted connected-subgraph MIP (single-commodity flow with M = B-1; HiGHS or SCIP; the graph is tiny for such solvers), proposal judged by PoB; then a Hamming trust region (local branching, 10-40 changes) with the ratio actual / predicted gain | measures in ONE run how much value the frozen greedy topology loses; if it pays, it is the only method that plans the whole tree at once | 17 s pass + solver seconds + one full evaluation; 5-10 passes per build at most | Fischetti-Lodi local branching; MWCS formulations (Rehfeldt-Franz-Koch 2022; Alvarez-Miranda et al. 2013); the loop itself is [DERIVED], no published instance found; failure modes: connectors priced at zero, thresholds invisible, oscillation, "an exact solver is exceptionally good at finding where the surrogate is wrong" |
| 4 | **Union of the three seeds + re-solve on the union** (<= 300 nodes) | seeds stop being best-of-3; alternative trunks of any seed compete | solver seconds + one evaluation | Bosman's solution merging; SCIP-Jack `heur_rec.c`; caveat: parents that share a trunk cannot produce a new one |
| 5 | **Operator portfolio, cost-aware order**; DOWNGRADED: the adaptive layer itself earns 0.14% on average over 25 ALNS implementations (Turkes et al. 2021; the portfolio is what matters). Reward = gain per second; controls: fixed equal, tuned fixed, adaptive | passes stop paying 500-700 s for barren kicks | bookkeeping | Ropke-Pisinger; Hendel's bandit ALNS in SCIP |
| 6 | **Component-level sampled Shapley** on connected prefixes (20 components x 32 permutations = 640 what-ifs, 4.5 s) | catches what leave-one-out misses: parts that are weak alone and strong together | 4.5 s per diagnosis | Castro et al. 2009; only if 1 proves misleading |
| 7 | Graph-local pair model (edge and within-cluster pairs + a short list of global multipliers, ~2.8k probes, ~20 s) | lets the surrogate of 3 see synergies | after 3 shows where it fails | Heckendorn-Wright; DSMGA-II; full BOCS / COMBO do NOT scale (tens of variables in their papers) |
| 8 | Acceptance other than strict improvement -- only at the cheap what-if layer, never by commissioning expensive regrows | small valleys | none | no study of our cost asymmetry found |
| 9 | **Loadout change**: warm start + forced trunk challenge + one cold construction at EQUAL budget; log retention |S_B and S_B+10| / |S_B| by leaves / subtrees / trunk | the bridge between loadouts becomes a measured quantity; the respec budget stays the user's rule | one construction (~95 s) + challenges | negative nesting result (verified) |

## What we report from now on (both reports ask for it; cheap)

Per build: counts of what-ifs, full evaluations, node-power passes and regrow seconds; accepted gain per second by
operator and destroy size; **trunk churn** 1 - |T_before and T_after| / |T_before or T_after| (does a run reconsider
early choices at all); all three seed values, never the best alone; "best-known value", never "x% from optimal".
Three seeds cannot support an extreme-value estimate of the optimum (modern evidence is negative anyway).
Optional yardstick: tiny instances (budget 15-20 around one class start) where exhaustive search is affordable and
the search's true gap can be measured.

## Order of work proposed to the user

A. One experiment task, independent of `tree_optimizer.py`: item 3 as a measurement on the six smoke references'
   delivered trees (node power -> MIP -> PoB), unrestricted and with Hamming radii 10 / 20 / 40. One number decides
   whether whole-tree planning is worth integrating.
B. Items 1 + 2 + the reporting block as one task in `tree_optimizer.py` (after the judge fix merges), accepted on the
   smoke six: value, seconds, seed spread, share of never-reconsidered nodes (22% -> below 5%), trunk churn.
C. Item 4 on top of A's solver; 5 once there are several operators to choose between; 6-8 only on evidence.
