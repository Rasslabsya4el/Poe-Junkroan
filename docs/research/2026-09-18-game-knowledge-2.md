# Research brief 2: Path of Exile 1 mechanics (patch 3.26-3.29 era)

Read on 2026-09-18. `poewiki.net` was attempted first for every topic but returned its JavaScript Anubis anti-bot page, so the usable sources below are PoEDB and the Path of Building Community source. "Not found" means no usable source was located, not that the behaviour is disproved.

## 1. Perforate

In Blood Stance, Perforate makes its spikes burst sequentially in a tight radius and a target can be hit by multiple spikes; in Sand Stance, the spikes thrust outward for coverage rather than a reliable single-target overlap. The regular level-20 gem creates 12 spikes before quality, has Blood radius 8 and Sand radius 11, and applies 75% less damage in Blood Stance; quality can add up to two spikes. Each hit can apply Bleeding normally, but only the highest-damage bleed deals damage at a time unless the build has a specific stacking rule such as Crimson Dance, so hit count primarily improves application/selection rather than multiplying ordinary bleed DPS. PoB has the user-entered `perforateSpikeOverlap` input, explicitly only for Blood Stance and capped at the gem's spike count; a threefold result with similar gear is therefore plausibly an overlap input of 3 versus 1, compounded by stance, bleed-stack rule, and condition differences, rather than a gear difference.

**Numbers / formula:** `Blood hits = entered overlapping spikes`; regular level 20: `12 spikes`, Blood radius `8`, Sand radius `11`, Blood damage multiplier `0.25`; ordinary bleed DPS is `max(active bleed DPS)`, not the sum of all inflicted bleeds.

**Sources:** [PoEDB Perforate](https://poedb.tw/us/Perforate) (read 2026-09-18); [PoB ConfigOptions: Perforate overlap input](https://raw.githubusercontent.com/PathOfBuildingCommunity/PathOfBuilding/dev/src/Modules/ConfigOptions.lua) (read 2026-09-18).

**Confidence:** high for skill and PoB-input facts; medium for the exact practical explanation of a particular 3x comparison.

## 2. Elemental Hit

Elemental Hit chooses one of fire, cold, or lightning per attack, deals only that chosen element, and avoids choosing the same element twice consecutively. Combat Focus exclusions reduce the possible choices; without exclusions, a build scaling only one element has an expected chosen-element contribution of about one third of its fire-only PoB result only when the other two choices contribute negligibly. "Average the three parts" is mathematically valid only when calculated as `(fire-part DPS + cold-part DPS + lightning-part DPS) / 3` under the same conditions, not as one third of a single selected part; no usable community source was found establishing a different accepted shortcut. PoB's source exposes Elemental Hit as a random-element skill, but I did not find a direct PoB issue or documentation source proving whether its displayed aggregate is automatically this three-part average, so an optimizer should explicitly evaluate all three parts and average them when elements remain available.

**Numbers / formula:** `expected DPS = sum(DPS of each selectable element) / selectable-element count`; with all three available: `(fire + cold + lightning) / 3`; the no-repeat rule changes short two-attack sequencing but not the stationary one-third marginal frequency of each element.

**Sources:** [PoEDB Elemental Hit](https://poedb.tw/us/Elemental_Hit) (read 2026-09-18); [PoB active-gem corpus: random_element tag](../../src/junkroan/pob/corpus_data/active_gems.json) (read 2026-09-18); [PoB ConfigOptions random-element mode](https://raw.githubusercontent.com/PathOfBuildingCommunity/PathOfBuilding/dev/src/Modules/ConfigOptions.lua) (read 2026-09-18).

**Confidence:** high for game selection rules and the expectation formula; medium for the recommended PoB treatment; direct PoB display behaviour not found.

## 3. Corpse Pact and corpse supply

Corpse Pact grants 4% increased attack and cast speed for each corpse consumed recently, capped at 200%, and chills/shocks enemies near corpses spawned recently; "recently" is four seconds. A normal Desecrate cast spawns 5 corpses with a shared cap of 10, while Volatile Dead consumes up to 3 per cast, so a hand-cast Desecrate then Volatile Dead loop has 5 spawned corpses initially, then 2 remaining after one VD cast, and records 3 corpses consumed. With a sustained VD consumption rate `r` corpses/s, the Corpse Pact count is `min(50, 4r)`; for three VD casts/s consuming three each, that is 36 corpses recently and 144% increased speed, provided corpses are actually available. Automation can maintain the cap more consistently, but a sourced universal cast/cooldown rate was not found; Undertaker raises Desecrate's maximum corpse allowance from 10 to 12, not its stated five corpses per ordinary cast, and therefore improves buffer rather than per-cast output.

**Numbers / formula:** `Corpse Pact speed = 4% * min(corpses consumed in last 4 s, 50)`; hand-cast first cycle: `Desecrate 5`, `VD consumes <=3`, `2 remain`; at `3 VD casts/s * 3 corpses`, `36 recently`, `144%`; Undertaker cap `10 -> 12`.

**Sources:** [PoB corpus: Corpse Pact](../../src/junkroan/pob/corpus_data/ascendancies.json) (read 2026-09-18); [PoEDB Desecrate](https://poedb.tw/us/Desecrate) (read 2026-09-18); [PoEDB Volatile Dead](https://poedb.tw/us/Volatile_Dead) (read 2026-09-18); [PoB corpus: Undertaker](../../src/junkroan/pob/corpus_data/passives.json) (read 2026-09-18).

**Confidence:** high for caps and formula; medium for hand-cast/automation practical values because setup timing varies.

## 4. Sigil of Power

Sigil of Power has four maximum stages, needs cumulative mana spent in its area for each stage, cannot gain stages more often than once per second, and lasts 12 seconds. At level 20 each stage requires 400 mana, so four stages require 1,600 total mana: casts costing 50, 150, and 400 mana at three casts/s reach that total in about 10.67 s, 3.56 s, and 1.33 s respectively; the one-second gate makes the latter two approximately four seconds in practice. PoB's `sigilOfPowerStages` is an unrestricted count input at the UI layer; game data caps the effective range at `0..4`, so the optimizer should clamp it to that range. The first-stage timing convention is not stated by the sources, so use four seconds as conservative ramp time for sufficiently expensive builds rather than claim a sub-second full ramp.

**Numbers / formula:** level 20 threshold `400 mana/stage`; `mana-only full-ramp time = 1,600 / (cast cost * casts/s)`; conservatively `t_full = max(4 s, mana-only full-ramp time)` when the duration permits; input range `0..4`.

**Sources:** [PoEDB Sigil of Power](https://poedb.tw/us/Sigil_of_Power) (read 2026-09-18); [PoB config surface: sigilOfPowerStages](../../src/junkroan/pob/corpus_data/config_surfaces.json) (read 2026-09-18).

**Confidence:** high for caps, threshold, and input; medium for exact first-stage timing.

## 5. Withered

Withered stacks to 15 and each standard stack makes the target take 6% increased chaos damage, for 90% increased chaos damage taken at 15 stacks before effect modifiers. Withering Touch has 25% chance per supported attack hit and a two-second duration, so its expected application rate is `0.25 * hit rate`; it cannot be assumed to maintain 15 stacks without measuring hit rate and expiry. For a Wither spell totem, use `15 / (N * casts per second)` as the no-expiry ramp estimate; at the historic 0.28 s base cast time this is about `4.2 / N` seconds, while a two-second duration means one totem cannot sustain 15 without cast-speed/duration help and several totems commonly can. Withering Step applies only while its buff persists and ends when another skill is used, so it is an opening/refresh source rather than a sustained boss-stack assumption for a skill-spamming build.

**Numbers / formula:** `max stacks = 15`; `full multiplier from standard stacks = 1 + 15 * 0.06 = 1.90`; Withering Touch expected stacks/s `= 0.25 * hits/s`; Wither-totem ramp estimate `= 15 / (N * cast rate)`.

**Sources:** [PoEDB Withered](https://poedb.tw/us/Withered) (read 2026-09-18); [PoEDB Withering Touch](https://poedb.tw/us/Withering_Touch_Support) (read 2026-09-18); [PoB calculation source: Withered stack limit](https://raw.githubusercontent.com/PathOfBuildingCommunity/PathOfBuilding/dev/src/Modules/CalcPerform.lua) (read 2026-09-18).

**Confidence:** high for cap, effect, duration, and Withering Touch chance; medium for totem timing because cast speed and placement vary.

## 6. Sacrifice Support

Sacrifice Support supports eligible non-reserved hit spells and makes each cast sacrifice 20% of current life to gain added chaos damage equal to 35-54% of life sacrificed, depending on gem level. At level 20, the added chaos damage is `0.54 * 0.20 * current life = 10.8% of current life` as added minimum and maximum chaos damage per cast, while the next cast costs 20% of the now-lower current life. PoB models the support's added damage, but a direct source proving that it includes the repeated current-life payment in a life-cost or net-regeneration statistic was not found; treat this as a mandatory external self-cost calculation, not a PoB sustain result. Practical sustain must cover a geometric current-life drain plus incoming damage, normally requiring recovery between casts or a deliberately low casting cadence; no sourced build-guide rule was found that justifies a universal sustain floor.

**Numbers / formula:** per cast `life_after = 0.8 * life_before`; level-20 added chaos `= 0.54 * sacrificed life = 0.108 * current life`; after `n` uninterrupted casts, `life_n = life_0 * 0.8^n`.

**Sources:** [PoEDB Sacrifice Support](https://poedb.tw/us/Sacrifice_Support) (read 2026-09-18); [PoB support-gem corpus](../../src/junkroan/pob/corpus_data/support_gems.json) (read 2026-09-18).

**Confidence:** high for gem text and formula; low for PoB cost accounting because a direct verification source was not found.

## 7. Shrapnel Ballista plus Arrow Nova

The combination does not work: Arrow Nova excludes skills that create minions, while Shrapnel Ballista creates a ballista-totem minion. Consequently there are no Arrow Nova landing patterns, known build usage, or a specific PoB overestimation to model for this pair. Shrapnel Ballista itself fires three arrows and can shotgun one target; its own multi-arrow overlap must still be handled separately. PoEDB's support eligibility listing excludes `CreatesMinion`, and the Shrapnel Ballista page lists Arrow Nova among broad support discovery text but the actual support restriction is decisive.

**Numbers / formula:** Arrow Nova normal effect would be `+4 projectiles`, circular firing, and `16% less projectile damage` at level 20, but effective compatibility with Shrapnel Ballista is `false`; Shrapnel Ballista base arrows per attack `= 3`.

**Sources:** [PoEDB Arrow Nova Support](https://poedb.tw/us/Arrow_Nova_Support) (read 2026-09-18); [PoEDB Shrapnel Ballista](https://poedb.tw/us/Shrapnel_Ballista) (read 2026-09-18); [PoB support-gem corpus: Arrow Nova](../../src/junkroan/pob/corpus_data/support_gems.json) (read 2026-09-18).

**Confidence:** high.

## 8. Accuracy

No usable source was found for a league-start community consensus such as "95% minimum," so that threshold should be recorded as an owner policy, not a sourced game rule. A hit chance below 100% is a direct multiplicative loss to attack-hit DPS and to any on-hit effects: at 95%, expected hit-trigger rate and attack damage are 0.95 of the displayed always-hit case; at 90% and 80% they are 0.90 and 0.80. The felt degradation is therefore not a separate mechanic: misses make damage, leech, ailments, charge generation, and other on-hit recovery visibly intermittent, with the severity depending on attack rate and the build's reliance on those effects. For optimizer rails, 95% is a defensible conservative floor, but it should be evaluated against PoB's actual `ChanceToHit` rather than inferred from accuracy rating.

**Numbers / formula:** `expected hit DPS = nominal hit DPS * ChanceToHit / 100`; loss relative to capped hit chance: `5% at 95`, `10% at 90`, `20% at 80`.

**Sources:** [PoEDB Accuracy](https://poedb.tw/us/Accuracy) (read 2026-09-18); practice threshold source not found.

**Confidence:** high for the probability formula; low for any universal player-practice threshold.

## Optimizer Summary

1. Perforate Blood Stance: require an explicit overlap assumption from `1` through the spike cap; never inherit it silently.
2. Regular Perforate level 20 has `12` spikes; Blood is `0.25x` damage per spike, so overlap is the decisive boss variable.
3. Elemental Hit with no exclusions: score `(fire + cold + lightning) / 3`, not a scaled single element.
4. Corpse Pact: `speed = 4% * min(consumed in last 4 s, 50)`; VD consumes at most `3` corpses/cast.
5. Desecrate normally supplies `5` corpses and holds `10`; Undertaker raises only the hold cap to `12`.
6. Sigil of Power: clamp stage input to `0..4`; at level 20 use `400 mana/stage` and a conservative four-second full-ramp gate.
7. Withered: cap `15`, standard effect `6% increased chaos damage taken/stack`, and calculate source-specific application rate.
8. Sacrifice Support: charge `20% current life/cast`; at level 20 add chaos equal to `10.8% current life` per cast before recovery.
9. Reject Shrapnel Ballista plus Arrow Nova as incompatible because Arrow Nova excludes minion-creating skills.
10. Use `ChanceToHit >= 95%` as a configurable policy rail; multiply hit DPS and all on-hit rates by actual chance to hit.
