# Tree, gear, gems and config depend on each other -- who moves when: what the literature offers and what we take (the lead's reading, 2026-09-19)

Reports, read in full: `inbox/2026-09-19-chatgpt-interdependent-components.md` (65 KB), `inbox/2026-09-19-astra-interdependent-components.md`
(38 KB). Quotes checked by the lead on the primary pages: Mei, Li & Yao, Soft Computing 2016 ("impossible to decompose
the problem into independent sub-problems", "non-linear relationship in the objective function"): verbatim; Namazi et
al., arXiv 1911.03124, abstract ("the solution of one component is kept fixed while the solution of the other component
is modified. This suggests low coordination", 2-OPT "does not take into account the collection plan, which can result
in a lower objective value ... the tour modification to be rejected", "an expanded form of 2-OPT to change the
collection plan in coordination"): matches both reports. Not opened (bot check): Mansini & Zanotti 2020 (INFORMS); both
reports quote the same abstract sentences independently.

Our terms: T = passive tree, G = the rare gear (one item per slot, resistances must sum to the cap, attributes to the
requirements), K = gem links and utility picks, C = the config derived from all three. Our loop: T refine -> T path
swaps -> one G slot -> K picks, kicks (T alone and T+G together) when a pass keeps nothing.

## What the two reports agree on, in our terms

1. **Our problem has a name: the Travelling Thief Problem family** (a route and a knapsack that spoil each other's
   value). Its measured lesson: optimizing the parts in turn with the other part frozen is "poor coordination"; a
   solver that changes both in ONE move beat the turn-taking solvers on all 39 test instances (Mei et al.), and a
   route change that looks bad with the knapsack frozen becomes good when the knapsack is adjusted with it (Namazi et
   al.). Our own data say the same: the joint T+G kick keeps the largest share of the loop's gains.
2. **A joint move is not two random changes**: the first change says WHICH parts of the partner to reconsider (Namazi's
   operator re-packs only the items along the reversed segment).
3. **Equal turns waste time when the parts pay unequally**: allocate the next slice to the move type with the best
   recent gain per second, with forced re-tries of the others (bandit-style cooperative coevolution). A warning from
   the same paper family: refreshing the partner after EVERY small change converged faster and ended WORSE.
4. **"A pass kept nothing" is not "nothing is left"**: it certifies only the single-part neighbourhoods.
5. **Gear is a textbook exact problem once PoB's numbers are frozen** (multiple-choice knapsack: one choice per slot,
   several sums to satisfy). Exact solvers handle it; but the solver is exact only for the linear approximation, so
   the change is limited to a couple of slots and PoB verifies every proposal.
6. Building a part against an EMPTY partner is a convention, not evidence (our own case in the brief: gear built
   against an empty tree, 7,330 -> 4,296 before the tree caught up).
7. Feasible first, then smaller violation, then value (Deb's rules) -- this is what our `Score` already does.

## Our own numbers

Loop passes add +26 / +7 / +4 / +2 / +2%; a pass costs about 200 s at the median, up to 1,500 s; after loop pass 1 (30%
of the build's time) the build holds 82% of its final value, after pass 3 (50%) 92%: half of the machine time buys the
last 8%. 34 of 42 builds end on a pass that keeps nothing. One what-if = 7 ms, one full calc = 0.1-0.2 s.

## What we take, in order (after the tree plan's A and B; nothing here is specified for a worker yet)

1. **The joint move that follows the change** (cheapest, most direct): after a kept tree move, re-judge only the gear
   slots it touched. WHICH slots: by the best COMPLETED replacement under the new tree (one fast what-if per candidate
   line, 7 ms), not by how much the slot's current lines lost -- the tree research's correction ("removal loss is not
   replacement opportunity", Astra A 3.2) applies to gear unchanged -- plus the slots holding a tight sum
   (resistances, attributes). About 0.3 s per proposal; ten proposals cost seconds against a 200 s pass. Replaces part
   of the random T+G kick. The tree research's other warning applies to that kick as it stands: its repair is greedy on
   both parts, and "a larger destroy set can still recreate the same greedy basin" -- a second repair policy (tree
   plan B) is what makes a joint kick land somewhere new.
2. **The gain-per-second ledger is the tree plan's reporting block, extended from tree operators to every move of
   the loop** (gear slot, picks, lanes, both kicks): one table per build, no behaviour change. It is NOT a new item.
   What it feeds is a cost-aware ORDER and an end to barren passes (the tree plan's item 5: "passes stop paying
   500-700 s for barren kicks"). The adaptive bandit scheduler both component reports recommend is DOWNGRADED exactly as
   the tree plan downgraded it: the evidence for it is from continuous large-scale optimization, while the evidence
   closest to our loop (25 ALNS implementations, Turkes et al. 2021, in the tree research) puts the adaptive layer
   itself at +0.14% on average -- the portfolio and its order matter, the adaptation does not. So: ledger, then a
   tuned FIXED order, and the bandit only as the third arm of the tree plan's own control (fixed equal / tuned fixed /
   adaptive).
3. **Gear as one small exact problem -- the tree plan's item 3 on another component, and it waits for experiment A.**
   Same method (values from fast what-ifs around the incumbent, exact solve, Hamming trust region, PoB judges, the
   ratio actual / predicted gain), same solver (HiGHS), same code. A's result decides the prior: if the additive model
   holds at radius 10-20 on the tree, a 2-slot radius on gear is safe; if A shows the model breaks early, gear lines
   (which interact through the same multipliers) get pair terms first (tree plan item 7) or the idea is dropped. Gear
   has one advantage over the tree: its thresholds (resistance caps, attribute requirements) are explicit constraints
   of the model, where the tree's are invisible to the surrogate. The tree plan's warning holds: "an exact solver is
   exceptionally good at finding where the surrogate is wrong".
4. **Gear pass 1 against a rough tree, not an empty one** (an experiment, not a belief): swap the construction order on
   the smoke six on the replay bench of `2026-09-19-judging-plan.md`.

## What we do not take

A whole-solution genetic / memetic algorithm (the literature's winner on TTP): our evaluation is 1,000x more expensive
than theirs. Analytical target cascading and other engineering-design architectures: they need gradients and convexity.
Stochastic ranking / epsilon-relaxed constraints: our kicks already pass through infeasible states and `Score` orders
them; no evidence of a need.

## Does it save time, can it hurt, which tests decide

- Item 2's ledger costs nothing and tells whether the scheduler is worth writing: if passes 3+ really pay 1/10 per
  second, stopping or re-allocating them saves up to half of a build's time for a few percent of value -- a knob the
  user sets, not a default.
- Items 1 and 3 aim at quality at the same time budget. They can hurt only through time stolen from moves that pay
  more; the ledger shows that too.
- Each is judged on the replay bench (same starting builds, before / after, gain and seconds), then one smoke
  confirmation.
