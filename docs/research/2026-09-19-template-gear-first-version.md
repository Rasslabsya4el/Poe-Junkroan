# Day-1 gear templates, first version (7f3e3d4): the lead's transplant on the six smoke references

Run: `scripts/gear_transplant.py --set smoke --seed 1` on branch `gpt-2026-09-19-day1-gear-templates-2`, 2026-09-19
16:05-16:35, one PoB session while `core14-rules` ran (files: `artifacts/runs/gear-templates/`, copied to
`<archive>\gear-templates\`). A = the author's rares, B = the loot simulation (best of 600),
C = the template filler; same tree, uniques and config.

| reference | seed | mode | stat | A | B loot | C wishlist | B/A | C/A | A feasible | B feasible | C feasible | B life/A | C life/A | B EHP/A | C EHP/A | seconds |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|
| cold_dot | 1 | DoT | CombinedDPS | 248,922 | 224,324 | 202,699 | 90.1% | 81.4% | True | True | True | 106.7% | 106.3% | 101.1% | 100.4% | 324 |
| bleed_bow | 1 | DoT | CombinedDPS | 587,787 | 861,252 | 292,610 | 146.5% | 49.8% | False | True | False | 100.0% | 101.2% | 100.8% | 86.7% | 371 |
| summon_raging_spirits | 1 | minion | FullDPS | 768,393 | 885,942 | 776,730 | 115.3% | 101.1% | False | False | False | 100.7% | 98.7% | 120.6% | 82.7% | 512 |
| impale_ballista | 1 | attack | FullDPS | 603,606 | 232,124 | 186,453 | 38.5% | 30.9% | False | False | False | 98.8% | 109.5% | 101.9% | 103.0% | 562 |
| stormbrand | 1 | spell | FullDPS | 1,329,611 | 1,336,182 | 1,336,265 | 100.5% | 100.5% | False | False | False | 104.3% | 108.2% | 106.0% | 101.8% | 355 |
| burning_arrow_snipe | 1 | DoT | CombinedDPS | 955,353 | 886,193 | 487,656 | 92.8% | 51.0% | False | False | False | 99.5% | 103.7% | 101.2% | 97.4% | 314 |

Median C / A = 66.2% against the loot's 96.6%. All six cap their resistances from gear (one 21% fire shortfall on
burning_arrow_snipe); life 98.7-109.5% of the author's.

## Why it is weak: one cause, read from the log

The first version prices rarity by ONE TIER's share of the pool and refuses everything under 1%
(`open_mod_min_share`): 3,192 refusals on six references -- increased cast / attack speed, elemental damage with
attacks, increased fire / cold / lightning damage, chaos resistance, damage-over-time multiplier, flat added damage,
spell suppression. What is left often moves nothing, and the filler then takes a line with delta +0:

- bleed_bow / burning_arrow_snipe (49.8% / 51.0%): the Citadel Bow gets flat physical damage (+225,704) and then
  "32% reduced Attribute Requirements" (+0) and "Bow Attacks fire an additional Arrow" (+0); increased physical
  damage, attack speed and the multiplier never reach the comparison.
- armour and jewellery: 3-6 of the open-or-craft lines per build go to a resistance at delta +0 while the set is
  already 41-143% over the cap (cold_dot overcap 81 / 133 / 105 with six such lines).

Both follow from the refused candidates, so the amendment's group share (the chosen tier and the better ones, summed,
two rails 0.2% / 1%) is the fix to measure first. Two things the amendment spec does not say and the next review must
check: a line that moves nothing (delta +0) must not be spent on an arbitrary mod -- prefer the best defensive
candidate or leave it to the bench craft, and the shopping list must mark it "free line"; and the resistance plan
must stop adding lines once the set caps (overcap is not a goal).

Time: 314-562 s per reference for A + B + C together; a template slot takes 2-11 s.
