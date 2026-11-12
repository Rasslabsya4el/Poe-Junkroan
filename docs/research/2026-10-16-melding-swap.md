# Melding 2-for-2 tree swap on Contagion A1 (#1159)

Build: A1 `01 witch_occultist_no_iron_will_prophecy_wand`, seed 1, pobb.in `V96SPqICYIRW`
(`artifacts/search-contagion/20261015-0336`), decode in `docs/research/2026-10-16-reading-7-builds-decode.md:3-4`.
Swap (the owner's reading, 2026-10-16): remove the last (leaf) Life node on the Cruel Preparation path and on the
Blood Drinker path, take the two missing nodes of Melding (4 of 4).

Command (one PobSession, delivered config, no search): `python scripts/probe_melding_swap.py --out artifacts/probe-1159`
(json: `artifacts/probe-1159/row1.json`; probe took 8.9 s).

## Row 1: swap table

Before and after are PoB reads of the same build; the swap is two `mutate_nodes` removals and two additions.

| stat | before | after | delta |
|---|---:|---:|---:|
| CombinedDPS | 37,844 | 37,844 | 0.00 |
| Life | 4,535 | 4,502 | -33.00 |
| EnergyShield | 511 | 713 | 202 |
| TotalEHP | 12,995 | 13,431 | 435 |
| PhysicalMaximumHitTaken | 5,046 | 5,215 | 169 |
| FireMaximumHitTaken | 18,021 | 18,625 | 604 |
| ColdMaximumHitTaken | 18,021 | 18,625 | 604 |
| LightningMaximumHitTaken | 18,021 | 18,625 | 604 |
| ChaosMaximumHitTaken | 7,198 | 7,146 | -52.00 |
| FireResist | 75.00 | 75.00 | 0.00 |
| ColdResist | 75.00 | 75.00 | 0.00 |
| LightningResist | 75.00 | 75.00 | 0.00 |
| ChaosResist | 37.00 | 37.00 | 0.00 |
| EffectiveMovementSpeedMod | 1.30 | 1.30 | 0.00 |

Floors of `src/junkroan/optimizer/rails_default.json` (every floor of the file the objective reads):

| floor | floor value | before | after |
|---|---:|---|---|
| Life | 4,500 | 4,535 ok | 4,502 ok (margin 2) |
| PhysicalMaximumHitTaken | 4,700 | 5,046 ok | 5,215 ok |
| FireMaximumHitTaken | 14,800 | 18,021 ok | 18,625 ok |
| ColdMaximumHitTaken | 14,600 | 18,021 ok | 18,625 ok |
| LightningMaximumHitTaken | 16,000 | 18,021 ok | 18,625 ok |
| EffectiveMovementSpeedMod | 1.20 | 1.30 ok | 1.30 ok |
| MoMCastsAfterMaxHit | 3 | 1,000,000 ok (not applicable, no Mind over Matter) | 1,000,000 ok |
| FireResist / ColdResist / LightningResist (elemental_resist_each) | 65 | 75 ok each | 75 ok each |

The elemental_resist_goal of 75 is met by all three before and after. ChaosResist has no floor (`null`).
TotalEHP is only reported (rails_default.json), and it rises by 435 (+3.3 %) with the objective unchanged.

## Nodes

Melding group (corpus `group_id` 543; four non-mastery nodes, plus a mastery):

| node id | name | kind | A1 before |
|---|---|---|---|
| 61320 | Life and Energy Shield | normal | allocated |
| 63799 | Life and Energy Shield | normal | allocated |
| 55247 | Life and Energy Shield | normal | missing (swap: added first) |
| 18865 | Melding | notable | missing (swap: added second) |
| 25281 | Life Mastery | mastery | missing (in group 543, not part of the two-node swap) |

A1 holds 2 of the 4 non-mastery Melding nodes; the swap takes the other two, 55247 and 18865 (a chain from the
allocated 63799, so cost 2).

Leaf Life nodes (an allocated Life node whose only allocated neighbour is the path's notable):

| path | notable (id) | leaf Life node removed | stats |
|---|---|---|---|
| Cruel Preparation | 21958 | 14936 Life | 6% increased maximum Life |
| Blood Drinker | 27788 | 25260 Life | 6% increased maximum Life |

Allocated passive count: 110 before, 110 after (2 removed, 2 added).

## Not in this row

Row 2 (the refine trace on A1: generated / evaluated of a candidate holding both missing Melding nodes) is the
other worker's, written to its report, not here.

## Row 2: does the tree search generate and evaluate the Melding candidate (unit 2, read 2026-10-16)

`PYTHONPATH=<wt>/src python scripts/probe_melding_refine.py --max-seconds 300` (the refine pass took 33 s, the whole probe 46 s). Melding = node 18865 (notable, +7% max Life, 3% of Life as Extra ES), missing; node 55247 (Life and ES) also missing; the pair (55247, 18865) is a cost-2 candidate; its Life Mastery 25281 sits behind it and is not part of the owner's 4 of 4.

| trace class | generated | evaluated |
|---|---|---|
| `melding:both` (trial holds 55247 and 18865) | 1 | 1 |
| `melding:both+add-only` (the candidate's own add probe) | 1 | 1 |
| `melding:both+swap` (a swap trial that removes leaves) | 0 | 0 |

The add probe shows CombinedDPS 37,844.14 (+0.0 %), Life 4,700, EnergyShield 719. Its gain per point is 0.0, so it ties with every zero-gain candidate and ranks 157 of 300; the swap batch takes only `top_candidates` = 80, so no swap trial holds Melding. Cut: `for _key, meta, cost in ranked[:top_candidates]` at `src/junkroan/optimizer/tree_optimizer.py:1284`, rank key `tree_optimizer.py:2346-2356` (measured: the rank; no other cause was tested). Even if measured, acceptance at `tree_optimizer.py:1311-1313` needs `value >= score * (1 + 0.002)`.

## Row 3: verdict (lead)

Row 1: TotalEHP +435 (+3.3 %), CombinedDPS 37,844 -> 37,844 (0.00 %, so the objective is down by less than 0.5 %), every `rails_default.json` floor ok (Life margin 2 points: 4,502 against 4,500; Life -33 and ChaosMaximumHitTaken -52 are the costs). Row 2: swap evaluated = 0. Row 3 fires: a fix ticket is opened as a sub-issue of #1149 (the parent of #1159).
