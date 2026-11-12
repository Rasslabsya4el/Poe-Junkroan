# Screening skeletons cheaply before the expensive optimize: what the literature offers and what we take (the lead's reading, 2026-09-19)

Reports read in full: `inbox/2026-09-19-chatgpt-multi-fidelity-screening.md` (77 KB, ~50 sources) and
`inbox/2026-09-19-astra-multi-fidelity-screening.md` (the second delivery; the first file was empty). Quotes checked by
the lead on the primary pages: MFES-HB (AAAI) "low-fidelity measurements can be biased yet informative to guide the
configuration search", "3.3-8.9x speedups over the state-of-the-art approach --- BOHB"; ASHA (arXiv 1810.05934)
"promotes configurations to the next rung whenever possible instead of waiting for a rung to complete before proceeding
to the next rung" -- both verbatim; the ASHA text also carries the "incorrect promotions" caveat Astra cites.

Our setting: `junkroan build` screens 20-200 skeletons at 2-3 min each, optimizes the top 2 in full (30-60 min) on 3
seeds, 5 workers, 1.5-3 h per request.

## What the report says, in our terms

1. The whole family (successive halving, Hyperband, ASHA, BOHB) is one idea: give every candidate a little, keep a
   fraction, give the survivors more. It is only as good as the cheap look predicts the expensive result, and a wrong
   early cut cannot be undone. No source gives a "safe" rank correlation; it has to be measured on our own data, and
   the number that matters is not the correlation but WINNER RECALL: how often the skeleton that wins at full depth
   is inside the screen's top m.
2. A cheap look can be biased, not just noisy (a "late bloomer": weak at the screen, strong after the full optimize).
   Repeating the screen does not fix bias; a middle rung or a wider cut does.
3. Ten paired observations only detect a catastrophe (observed rho 0.5 at n = 10 has an interval of -0.19 .. 0.86);
   30-40 pairs give a usable estimate.
4. Seeds at the top: fixed "3 seeds for each of 2 finalists" is not the best use of six full runs; ranking-and-selection
   (OCBA, knowledge gradient) spends the next run where it can still change the answer. One seed per design cannot
   estimate that design's noise: the pooled noise (ours: 15% per run, `2026-09-19-judging-plan.md`) is the prior.
5. Sharing information across related skeletons (random-forest surrogates, TPE, transfer from earlier requests) needs
   far more history than we have; Optuna's TPE burns ~10 trials per bracket before it learns anything.
6. Workers should never wait for a cohort (ASHA): promotion is decided as results arrive.

## What Astra adds or corrects

1. **At large requests the SCREEN is the bottleneck, not the finals**: 100 skeletons x 3 min = 60 min of wall time on
   five workers, 200 = 120 min, before anything is optimized. No ladder fixes that; only a cheaper first look or a cap.
2. **A protected exploration quota**: 10-20% of the middle-rung slots go to skeletons the screen ranked low
   (late bloomers, ascendancies absent from the top). ASHA's own argument that wrong promotions vanish is asymptotic
   and says nothing at 20 candidates.
3. A gate for being aggressive (derived, not sourced): at least 20 screen / full pairs, lower confidence bound of
   top-2 recall >= 0.80, lower bound of the rank correlation above 0; otherwise the conservative cut + the quota.
4. Seeds: 3-4 finalists x 2 seeds, then the next seed goes where sqrt(var / n) / gap-to-leader is largest (ChatGPT:
   4 x 1 + 2 adaptive from a pooled noise prior). Astra's version costs more than today's six full runs.
5. "A changed solver invalidates old screen / full calibration": the recall test is repeated after a big change of
   the loop. Tools: SMAC3's package metadata declares Linux only, Optuna's `n_jobs` is threads and SQLite locks under
   concurrency -- both reports end at "a project-owned queue first".
6. Persist every evaluation (request, skeleton, rung, seed, value, seconds, features) so that history accumulates.

## Our own numbers

Request sizes as they are today: the three acceptance requests of 19.09 had ONE candidate skeleton each (one
ascendancy, one mode, no variants; preparation 38-54 s, screen 95-150 s); a broad request (`search-cold_snap`) screened
13 ascendancies in 970 s and optimized the top 2 plus their variants. So the topic starts to matter with broad requests
and unique / keystone variants, which is where the product is going, not where the acceptance requests are.

We have NO paired screen / full data beyond the two promoted skeletons per request: the question the whole topic
turns on is unmeasured. What we do have (96 builds of the rules campaigns) is how early a build's own value predicts its
final value ACROSS SEEDS of one skeleton: end of construction = 23% of the time, 61% of the final value, r = +0.33 with
the final; after loop pass 1 = 30% of the time, 82% of the value, r = +0.60. So "construction + pass 1" is a candidate
MIDDLE rung (about 12 min), the bare construction is not.

## How this fits the tree-search plan, and one thing both reports get wrong for us

Both reports treat a finalist's seeds as noisy MEASUREMENTS of one number (the design's mean) and warn that taking the
best seed "favours high-variance designs". For judging CODE that is right (`2026-09-19-judging-plan.md`). For the
PRODUCT it is not our situation: a delivered build is a real PoB build whose number PoB reproduces exactly -- the seed
noise is SEARCH noise, there is no regression to the mean. And the tree plan's item C (union of the three seeds +
re-solve) turns seeds from samples into material: alternative trunks that compete in one solve. So for us (a) the
target of seed allocation is "the chance that one more seed, or the union, beats the best build we hold", where a
skeleton with a wide seed spread (ours range from 8 to 109 points by reference) is MORE worth another seed, not less;
(b) "2 finalists x 3 seeds" against "4 x 1 + 2" cannot be decided before C is measured, because C needs several seeds
of the SAME skeleton to have anything to merge. Reporting stays as the tree plan says: all seed values, never the best
alone.

## The loadout axis (the user, 2026-09-19): an earlier loadout is never a filter

"Late bloomer" above means DEPTH of search inside one loadout (a 2-3 minute look against a 40 minute optimize). The
user raised the other axis, and it is the more dangerous one: a build that only comes online with endgame pieces often
shares nothing with its day-1 / T16 version; a funnel "pick skeletons at day 1, upgrade the winners" would remove
exactly the builds the product exists to find. The tree research says the same one level down (optimal trees do not
nest across budgets). Rule for the loadout work, recorded before it starts (the user's words, 2026-09-19): every loadout is built on
its own, under its own rails, from the skeleton level, to be the best AT ITS LEVEL; the system never builds a PoB with
the next loadout in mind, and an endgame+ build that looks nothing like the endgame one is fine as long as it is better.
A BRIDGE between two finished loadouts (adjusting them for a less painful transition: shared trunk, fewer changed
slots, respec cost) is an optional quality-of-life step AFTER both are built -- an idea to keep, never a constraint.
And test 1 below is repeated
on the endgame loadout: a build that needs five pieces at once is under-rated by a shallow look more than a day-1 build
is, so the exploration quota matters more there, not less. Today only the day-1 rails exist, so nothing is being lost
yet; the recorded first step of the loadout work ("day-1 + T16 slice, nested tree") must be re-read against this rule.

## What we take, in order

1. **Measure winner recall first (the test that decides everything else).** For 3 requests (one hit, one DoT, one
   minion), optimize in full, one seed, 10 skeletons spread over the screen ranking (top 3, four from the middle, three
   from the bottom): 10 x ~40 min / 5 workers = about 1.5 h per request, 4.5 h in all, queueable. Report Spearman,
   and for m = 2, 3, 5: is the full-depth winner inside the screen's top m; the middle-rung value of each for the same
   table. 30 pairs = the sample size the report calls usable.
2. If the winner is often outside the top 2: widen to top m at a middle rung (construction + loop pass 1) and promote
   2 from there. If the screen already finds the winner: nothing changes -- the cheapest outcome.
   When widening, keep Astra's quota: one middle-rung slot in five for a skeleton from outside the screen's top
   (fits the product's goal of non-meta builds).
3. **Six full runs spent adaptively** (4 finalists x 1 seed, then 2 more runs where another seed is most likely to
   beat the best build held) instead of 2 x 3: same cost, twice the skeletons seen at full depth. Decided after test 1
   (how often rank 3-4 wins) AND after the tree plan's C (what a second and third seed of the same skeleton are worth
   as material for the union).
4. Check worker idle time in one request's log (the pool is already asynchronous; a number, not a rewrite).
5. Persist the evaluation rows from now on (item 6 above): zero risk, and the only way test 1 ever gets cheaper.
6. For requests above ~60 skeletons: measure what the 45 s preparation value (the rig) already predicts about the
   150 s screen -- if it ranks the bottom half correctly, the screen's wall time halves. A measurement on stored
   logs first.

## What we do not take

Optuna / Ray Tune / SMAC3 / Syne Tune as a dependency: our ladder has three rungs and one promotion rule, about 30 lines
inside `search/runner.py`; Ray on Windows is beta. Surrogates and transfer across requests: tens of observations, not
thousands. Hyperband's several brackets: with three rungs there is one decision to hedge, and test 1 measures it.

## Does it save time, can it hurt

Saves nothing by itself; it protects quality (a lost winner is the expensive mistake) and item 3 sees twice the
skeletons for the same machine time. The only way it hurts is a more aggressive cut than today's, which nothing here
proposes before test 1.
