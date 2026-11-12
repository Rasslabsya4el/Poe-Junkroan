# What our loot simulation actually rolls (2026-09-18)

Subject: the **rare items our own pipeline produced** — best of N random rares per slot with
PoB spawn weights, plus at most one bench craft (`src/junkroan/optimizer/loot_gear.py`).
Not the authors' rares (a second agent has those).

Corpus: 567 generated rares.

| run | builds | rares |
|---|---|---|
| `artifacts/benchmark/20260918-0723-rules-smoke` | 18 | 174 |
| `artifacts/benchmark/20260917-0844-core14-frozen` | 42 | 393 |

Every one of the 567 is **item level 70, quality 20** (`rails.gear.item_level` /
`rails.gear.quality`), and every log line says **best of 200** — both runs rolled N=200 in
the construction passes as well. `rails.gear.construction_best_of_n` was raised to 600 later
on 2026-09-18, so runs after these two draw 600 in construction and 200 in the loop.

All 2,824 explicit affixes resolved to a PoB mod id, group and tier: **0 unresolved**
(our rares keep their `Prefix: {range:x}<mod id>` lines, so nothing has to be matched by text).

---

## 1. Per slot

Tier = rank within the mod's PoB group ordered by required level, T1 best — the same
definition as `tests/fixtures/tuadh_329/gear_tiers.json`, so it is directly comparable with
the authors. `rank%` = tier / ladder length averaged over mods (0 = always the top tier,
1 = always the bottom). `rank70%` = the same against the ladder **reachable at ilvl 70**;
it is the honest "how close to the best obtainable roll", because mods above ilvl 70 cannot
drop on these items at all.

| slot | items | ilvl | pre | suf | affixes | bench | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8+ | rank% | rank70% | med mod ilvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Body Armour | 57 | 70 | 2.47 | 2.75 | 5.23 | 49% | 2% | 5% | 20% | 28% | 15% | 9% | 7% | 14% | 0.57 | 0.44 | 48 |
| Helmet | 57 | 70 | 2.49 | 2.49 | 4.98 | 74% | 14% | 18% | 19% | 17% | 11% | 10% | 5% | 7% | 0.54 | 0.46 | 46 |
| Gloves | 57 | 70 | 2.53 | 2.53 | 5.05 | 74% | 18% | 13% | 21% | 22% | 12% | 6% | 3% | 4% | 0.52 | 0.44 | 44 |
| Boots | 60 | 70 | 2.60 | 2.58 | 5.18 | 58% | 9% | 19% | 19% | 20% | 13% | 8% | 5% | 7% | 0.56 | 0.48 | 40 |
| Belt | 54 | 70 | 2.50 | 2.43 | 4.93 | 65% | 12% | 14% | 14% | 17% | 12% | 11% | 9% | 11% | 0.52 | 0.44 | 44 |
| Amulet | 54 | 70 | 2.26 | 2.57 | 4.83 | 72% | 9% | 14% | 21% | 18% | 13% | 9% | 6% | 10% | 0.55 | 0.47 | 44 |
| Ring 1 | 57 | 70 | 2.21 | 2.74 | 4.95 | 77% | 17% | 16% | 22% | 12% | 10% | 7% | 5% | 11% | 0.53 | 0.47 | 36 |
| Ring 2 | 60 | 70 | 2.35 | 2.50 | 4.85 | 75% | 18% | 14% | 15% | 18% | 13% | 7% | 6% | 8% | 0.53 | 0.47 | 37 |
| Weapon 1 | 54 | 70 | 2.46 | 2.46 | 4.93 | 74% | 8% | 17% | 21% | 15% | 14% | 11% | 7% | 9% | 0.62 | 0.54 | 40 |
| Weapon 2 | 57 | 70 | 2.53 | 2.33 | 4.86 | 82% | 8% | 16% | 26% | 19% | 10% | 7% | 5% | 10% | 0.56 | 0.47 | 45 |
| **all** | **567** | **70** | **2.44** | **2.54** | **4.98** | **70%** | **11%** | **15%** | **20%** | **19%** | **12%** | **8%** | **6%** | **9%** | **0.55** | **0.47** | **44** |

"bench" is the share of items carrying at least one `{crafted}` line; counted as lines it is
0.85 per item (87 items carry a two-line hybrid craft, e.g. `Adds 7 to 10 Fire Damage /
Adds 7 to 10 Cold Damage`). No mod on any item requires ilvl > 70.

**Affix count is where best-of-200 shows up first.** The roller draws its mod count uniformly
from `{4,4,4,5,5,6}` (50% / 33% / 17%); what survives selection is 28% / 46% / 26%. Selection
roughly halves 4-mod items and doubles 6-mod items — expected, and it is the single biggest
driver of every "our items are richer" number below.

**Top tiers per item** (the rails cap `max_t1_per_rare: 1` / `max_t2_per_rare: 2` /
`max_tier: 8` lives in `optimizer/gear_filler.py`, the *old* deterministic filler;
`LootGear` — what the pipeline actually runs — enforces none of them):

| T1 mods on one rare | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| ours (567) | 52% | 40% | 7% | 1% |
| authors (93) | 68% | 26% | 5% | 1% |

20% of our rares carry one mod worse than T8 and 2% carry two, so the `max_tier: 8` rail is
also not in force. Against the reachable-at-70 ladder our rares average 1.59 best-available
mods each.

### Top 12 families by frequency (median tier in brackets)

- **Body Armour** — IncreasedLife 51 (T4); FireResistance 36 (T4); LightningResistance 29 (T4); BaseLocalDefences 24 (T4); ColdResistance 24 (T4); DefencesPercent 18 (T5); LifeRegeneration 18 (T8); IncreasedMana 17 (T6); Intelligence 15 (T5); BaseLocalDefencesAndLife 14 (T3); Strength 11 (T3); DefencesPercentAndStunRecovery 10 (T4)
- **Helmet** — IncreasedLife 52 (T1); ColdResistance 29 (T4); FireResistance 25 (T4); BaseLocalDefencesAndLife 23 (T2); LightningResistance 22 (T4); Intelligence 20 (T6); DefencesPercent 18 (T5); BaseLocalDefences 16 (T4); IncreasedMana 13 (T6); DefencesPercentAndStunRecovery 11 (T3); IncreasedAccuracy 7 (T5); ChaosResistance 7 (T2)
- **Gloves** — IncreasedLife 47 (T2); ColdResistance 29 (T4); LightningResistance 28 (T4); Dexterity 23 (T5); BaseLocalDefences 20 (T3); PhysicalDamage 15 (T1); FireResistance 15 (T4); BaseLocalDefencesAndLife 11 (T2); DefencesPercentAndStunRecovery 11 (T3); IncreasedMana 8 (T5); FireDamage 8 (T2); DefencesPercent 8 (T4)
- **Boots** — MovementVelocity 52 (T3); IncreasedLife 51 (T2); ColdResistance 36 (T4); FireResistance 35 (T4); LightningResistance 27 (T5); LifeRegeneration 17 (T4); BaseLocalDefencesAndLife 15 (T2); Strength 12 (T4); DefencesPercentAndStunRecovery 12 (T5); BaseLocalDefences 11 (T3); Dexterity 10 (T4); StunRecovery 6 (T4)
- **Belt** — IncreasedLife 50 (T2); LightningResistance 33 (T4); Strength 30 (T5); IncreasedMana 26 (T4); FireResistance 21 (T5); IncreasedEnergyShield 20 (T8); IncreasedPhysicalDamageReductionRating 17 (T6); ColdResistance 17 (T5); LifeRegeneration 12 (T6); AttackerTakesDamageNoRange 10 (T2); BeltFlaskRecoveryRate 9 (T5); StunDurationIncreasePercent 7 (T2)
- **Amulet** — IncreasedLife 39 (T2); AllAttributes 15 (T4); ColdResistance 15 (T3); IncreasedEnergyShield 14 (T10); AllResistances 14 (T2); PhysicalDamage 12 (T4); LightningResistance 11 (T4); IncreasedMana 10 (T8); Dexterity 10 (T5); IncreasedCastSpeed 10 (T2); Intelligence 10 (T6); EvasionRatingPercent 8 (T5)
- **Ring 1** — IncreasedLife 45 (T2); IncreasedEnergyShield 20 (T6); PhysicalDamage 19 (T3); AllResistances 18 (T2); LightningResistance 18 (T4); Dexterity 16 (T4); Intelligence 15 (T4); IncreasedMana 15 (T9); Strength 14 (T6); ColdResistance 11 (T4); IncreasedCastSpeed 10 (T2); LifeRegeneration 9 (T2)
- **Ring 2** — IncreasedLife 49 (T2); AllResistances 25 (T2); IncreasedEnergyShield 19 (T5); PhysicalDamage 19 (T2); FireResistance 16 (T6); Dexterity 16 (T4); LightningResistance 15 (T5); ColdResistance 14 (T5); Intelligence 13 (T5); IncreasedEvasionRating 12 (T4); ColdDamage 10 (T6); IncreasedMana 10 (T6)
- **Weapon 1** — WeaponCasterDamagePrefix 29 (T4); SpellAddedElementalDamage 19 (T3); LocalPhysicalDamagePercent 14 (T5); Strength 13 (T5); PhysicalDamage 11 (T4); CriticalStrikeMultiplier 11 (T4); Dexterity 10 (T5); ColdDamage 10 (T8); SpellCriticalStrikeChanceIncrease 10 (T3); LightningDamage 9 (T3); FireDamage 9 (T7); IncreasedAttackSpeed 9 (T3)
- **Weapon 2** — IncreasedLife 33 (T2); WeaponCasterDamagePrefix 20 (T4); LightningResistance 17 (T5); FireResistance 15 (T4); ColdResistance 13 (T4); DamageWithWeaponTypeSkill 10 (T4); PhysicalDamage 9 (T3); IncreasedMana 9 (T9); SpellAddedElementalDamage 9 (T4); Strength 9 (T4); IncreasedAttackSpeed 9 (T3); BaseLocalDefencesAndLife 8 (T2)

Life and the three elemental resistances are the top families of every armour slot — the
objective's floors, doing exactly what they are there for. Boots: MovementVelocity on 52 of
60 items is the `EffectiveMovementSpeedMod >= 1.2` rail (D28).

---

## 2. "Luck"

Per mod: **share** = weight of the mods of its own family (PoB group) at or above the chosen
tier, divided by the total spawn weight of that affix type on that base at ilvl 70 — "how
often a prefix roll lands at least this good a mod of this family". Per item: the product
over its non-crafted affixes. Bench crafts are deterministic and are excluded.

The product is a **rarity index, not a drop probability** (mods are drawn sequentially without
replacement and families block each other, and an item with more affixes must be rarer); it is
comparable across items of the same affix count and across our gear vs the authors'.

| slot | items | median | p10 | p90 | −log10(median) | affixes/item | −log10 per mod |
|---|---|---|---|---|---|---|---|
| Body Armour | 57 | 9.8e-08 | 3.4e-09 | 6.7e-06 | 7.01 | 5.23 | 1.35 |
| Helmet | 57 | 1.3e-07 | 3.7e-09 | 3.3e-06 | 6.88 | 4.98 | 1.40 |
| Gloves | 57 | 4.2e-08 | 2.0e-09 | 7.1e-07 | 7.37 | 5.05 | 1.48 |
| Boots | 60 | 2.7e-07 | 6.5e-09 | 7.9e-06 | 6.57 | 5.18 | 1.28 |
| Belt | 54 | 2.8e-07 | 5.6e-09 | 4.0e-06 | 6.55 | 4.93 | 1.37 |
| Amulet | 54 | 2.5e-08 | 2.4e-10 | 4.1e-07 | 7.61 | 4.83 | 1.61 |
| Ring 1 | 57 | 2.5e-08 | 1.8e-09 | 8.3e-07 | 7.61 | 4.95 | 1.52 |
| Ring 2 | 60 | 3.0e-08 | 1.2e-09 | 1.7e-06 | 7.52 | 4.85 | 1.52 |
| Weapon 1 | 54 | 1.5e-08 | 1.6e-10 | 3.3e-07 | 7.82 | 4.93 | 1.62 |
| Weapon 2 | 57 | 5.3e-08 | 9.4e-10 | 9.7e-07 | 7.27 | 4.86 | 1.53 |
| **all** | **567** | **5.4e-08** | **1.3e-09** | **2.2e-06** | **7.27** | **4.98** | **1.45** |

**Against the authors** (their 93 tier-resolved rares, same formula, each at its own item
level): median product 5.5e-07 vs our 5.4e-08 (1.0 decade rarer), **but** p10 9.4e-10 vs our
1.3e-09 — their unluckiest decile is *rarer* than ours. Normalised per mod the two are
identical: **median −log10 share 1.45 for both**. Of the 1.0-decade gap, ~0.7 is simply that
our items put 4.98 affixes into the product against their 4.49 (their lines that
`gear_tiers.json` could not resolve to a mod carry no share and cannot enter it; counted as
raw explicit lines they have 4.61, see table 4); the remaining ~0.3 is the slightly better
tiers.
Per slot, per-mod rarity (ours vs authors): Body Armour 1.35/1.30, Helmet 1.40/1.34, Gloves
1.48/1.43, Boots 1.28/1.30, Belt 1.37/1.27, Amulet 1.61/1.47, Ring 1 1.52/1.49, Ring 2
1.52/1.52, Weapon 1 1.62/**1.69**, Weapon 2 1.53/**1.57** — the authors' *weapons* are the
luckier ones.

### The 15 least likely items

| # | run / build | slot | base | product | 1 in |
|---|---|---|---|---|---|
| 1 | core14 / stormbrand-s2 | Weapon 2 | Blood Sceptre | 1.8e-12 | 5.7e11 |
| 2 | core14 / absolution_minions-s2 | Ring 2 | Bone Ring | 8.7e-12 | 1.2e11 |
| 3 | rules-smoke / cold_dot-s1 | Weapon 1 | Void Sceptre | 9.5e-12 | 1.1e11 |
| 4 | core14 / physical_dot-s2 | Weapon 1 | Driftwood Wand | 1.2e-11 | 8.3e10 |
| 5 | core14 / winter_orb-s1 | Amulet | Jade Amulet | 3.9e-11 | 2.6e10 |
| 6 | rules-smoke / burning_arrow_snipe-s2 | Amulet | Jade Amulet | 4.2e-11 | 2.4e10 |
| 7 | core14 / hit_penance_brand-s2 | Weapon 2 | Void Sceptre | 4.2e-11 | 2.4e10 |
| 8 | core14 / smite-s1 | Ring 2 | Two-Stone Ring | 5.0e-11 | 2.0e10 |
| 9 | rules-smoke / burning_arrow_snipe-s2 | Ring 1 | Two-Stone Ring | 7.1e-11 | 1.4e10 |
| 10 | core14 / absolution_minions-s1 | Weapon 2 | Ancient Spirit Shield | 7.3e-11 | 1.4e10 |
| 11 | rules-smoke / cold_dot-s1 | Amulet | Citrine Amulet | 7.3e-11 | 1.4e10 |
| 12 | core14 / stormbrand-s1 | Weapon 1 | Karui Sceptre | 9.6e-11 | 1.0e10 |
| 13 | rules-smoke / stormbrand-s2 | Ring 2 | Two-Stone Ring | 1.0e-10 | 1.0e10 |
| 14 | core14 / absolution_minions-s3 | Ring 1 | Bone Ring | 1.2e-10 | 8.7e9 |
| 15 | core14 / cold_dot-s2 | Ring 2 | Topaz Ring | 1.3e-10 | 7.5e9 |

For scale, the authors' own five rarest day-1 rares sit at 7.2e-11 … 3.3e-10 (Winter Orb's
Opal Wand, Ignite Penance Brand's Two-Stone Ring and Platinum Sceptre, Viper Strike's Corsair
Sword, Cold DoT's ilvl-85 Void Sceptre) — i.e. items 5-15 of our list are in the same band as
the authors' luckiest, and only items 1-4 are out of it.

Mod lines of the four that are:

**1. stormbrand-s2 Weapon 2, Blood Sceptre** — the one item on the list a human would query:

```
Pre T2/9 (ilvl 62) 0.0038  Adds 58 to 107 Fire Damage to Spells      [SpellAddedFireDamage8]
Pre T1/2 (ilvl 63) 0.0076  +2 to Level of Socketed Melee Gems        [LocalIncreaseSocketedMeleeGemLevel]
Suf T3/9 (ilvl 66) 0.0092  +39 to Strength                           [Strength7]
Pre T3/8 (ilvl 58) 0.0099  83% increased Spell Damage                [SpellDamageOnWeapon6]
Suf T3/7 (ilvl 55) 0.0184  22% increased Cast Speed                  [IncreasedCastSpeed5]
Suf T3/3 (ilvl 15) 0.0367  22% chance to Freeze                      [ChanceToFreeze1]
```

**2. absolution_minions-s2 Ring 2, Bone Ring** — T1 fire damage + T2 mana regen + T1 life:

```
Suf T1/4 (ilvl 50) 0.0041  21% increased Fire Damage                 [FireDamagePercent4]
Suf T2/6 (ilvl 55) 0.0081  51% increased Mana Regeneration Rate      [ManaRegeneration5]
Suf T4/8 (ilvl 48) 0.0163  +31% to Fire Resistance                   [FireResist5]
Pre T1/8 (ilvl 44) 0.0181  +113 to maximum Life                      [IncreasedLife7]
Pre T3/7 (ilvl 58) 0.0181  +104 to Evasion Rating                    [IncreasedEvasionRating5]
Pre T8/9 (ilvl 13) 0.0489  Adds 3 to 7 Cold Damage to Attacks        [AddedColdDamage2]
```

**3. cold_dot-s1 Weapon 1, Void Sceptre** — T2 Cold DoT multiplier (share 0.0013) is the whole story:

```
Suf T2/5 (ilvl 64) 0.0013  +31% to Cold Damage over Time Multiplier  [ColdDamageOverTimeMultiplier4]
Pre T6/8 (ilvl 23) 0.0129  33% increased Physical Damage             [...PercentAndAccuracyRating3]
Suf T3/7 (ilvl 55) 0.0184  22% increased Cast Speed                  [IncreasedCastSpeed5]
Suf T4/9 (ilvl 55) 0.0184  +36 to Strength                           [Strength6]
Pre T4/8 (ilvl 46) 0.0326  58% increased Spell Damage                [SpellDamageOnWeapon5]
Pre T6/9 (ilvl 26) 0.0523  Adds 17 to 32 Fire Damage to Spells       [SpellAddedFireDamage4]
```

**4. physical_dot-s2 Weapon 1, Driftwood Wand** — two DoT multipliers on one wand:

```
Pre T3/10 (ilvl 63) 0.0032 Adds 11 to 209 Lightning Damage           [LocalAddedLightningDamage8]
Suf T3/5  (ilvl 68) 0.0056 +17% to Damage over Time Multiplier       [GlobalDamageOverTimeMultiplier1h3]
Suf T4/5  (ilvl 12) 0.0080 +21% to Physical Damage over Time Mult.   [PhysicalDamageOverTimeMultiplier2]
Suf T3/6  (ilvl 44) 0.0186 27% increased Critical Strike Chance      [LocalCriticalStrikeChance4]
Pre T6/9  (ilvl 26) 0.0550 Adds 15 to 30 Fire Damage to Spells       [SpellAddedFireDamage4]
Pre T6/8  (ilvl 23) 0.0821 39% increased Spell Damage                [SpellDamageOnWeapon3]
```

### The "+1 gems on day 1" question, directly

22 of 567 items (4%) carry a gem-level mod at all:

| count | share | mod |
|---|---|---|
| 8 | 0.0033 | `GlobalLightningSpellGemsLevel1` +1 to Level of all Lightning Spell Skill Gems |
| 3 | 0.0056 | `GlobalIncreaseMinionSpellSkillGemLevel1` +1 to Level of all Minion Skill Gems |
| 3 | **0.0008** | `GlobalSpellGemsLevel1` +1 to Level of all Spell Skill Gems |
| 2 | 0.0033 | `GlobalColdSpellGemsLevel1_` +1 to Level of all Cold Spell Skill Gems |
| 2 | 0.0152 | `LocalIncreaseSocketedMeleeGemLevel1` +1 to Level of Socketed Melee Gems |
| 2 | 0.0153 | `LocalIncreaseSocketedGemLevel1` +1 to Level of Socketed Gems |
| 2 | 0.0195 | `LocalIncreaseSocketedBowGemLevel2` +2 to Level of Socketed Bow Gems |
| 1 | 0.0076 | `LocalIncreaseSocketedMeleeGemLevel` +2 to Level of Socketed Melee Gems |
| 1 | 0.0391 | `LocalIncreaseSocketedBowGemLevel1` +1 to Level of Socketed Bow Gems |

Only **two** items carry two gem-level mods at once, and both are legal (different families):

- `core14/cold_dot-s3` Weapon 1 Void Sceptre: `GlobalSpellGemsLevel1` (+1 all Spell Gems, share 0.0008) + `LocalIncreaseSocketedMeleeGemLevel1`
- `core14/toxic_rain-s3` Weapon 1 Highborn Bow: `LocalIncreaseSocketedGemLevel1` + `LocalIncreaseSocketedBowGemLevel1` (joint share ~6e-4)

`+1 to Level of all Spell Skill Gems` on a Void Sceptre (share 0.0008, 3 items) is the single
rarest mod family we roll, followed by `LightningDamagePrefixOnWeapon7` (0.00053, 1 item) and
`ColdDamageOverTimeMultiplier4` / `PhysicalDamageOverTimeMultiplier4` (~0.0013, 1 each).

---

## 3. How much did the winner beat the field?

**The per-roll scores are not recorded anywhere.** `LootGear.fill_slot` evaluates all 200
trials in one `trial_stats` call and keeps a running best (`best = (key, r, s)`); the losing
199 scores are discarded, and `LootSlotResult` stores only `before` / `after_loot` /
`after_bench`. Neither `results.json` nor the logs carry a distribution. Answering "how much
did the best of 200 beat the median roll" needs a one-line change in `fill_slot` (keep the
quantiles of the 200 `Score.value`s) and a re-run — it cannot be reconstructed from these
artifacts.

What the logs do record is the **A → B** line, and its semantics are narrower than "the gain
best-of-200 bought": the slot is emptied before every re-roll (`pipeline.py:528`, and
`fill(passes=…)` for p>0), so **A is the build with that slot empty** and B the build with the
winner equipped. A → B is therefore *what the winning item is worth*, not *what the extra
rolls were worth*. The old item competes as an incumbent, so B can never be worse in rank.

1,739 loot rolls in the 18 rules-smoke logs, all at N=200, 45-187 rolls per build:

| slot | rolls | median A | median B | med ΔV | p25 | p75 | ΔV>0 | med Δviol | bench kept | bench ΔV | bench Δviol | incumbent kept |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Body Armour | 164 | 669,540 | 669,540 | 0.0% | 0.0% | 0.0% | 18% | −1.268 | 8% | 0.00% | −0.052 | 100 |
| Helmet | 172 | 705,362 | 727,150 | 0.0% | 0.0% | 0.3% | 28% | −0.580 | 14% | 0.00% | −0.058 | 99 |
| Gloves | 172 | 625,885 | 631,697 | 0.0% | 0.0% | 3.0% | 48% | −0.667 | 18% | 0.00% | −0.046 | 96 |
| Boots | 169 | 675,017 | 675,017 | 0.0% | 0.0% | 0.2% | 26% | −0.815 | 13% | 0.00% | −0.030 | 92 |
| Belt | 144 | 616,874 | 647,642 | 0.7% | 0.0% | 3.8% | 60% | −0.447 | 14% | 0.00% | −0.015 | 88 |
| Amulet | 225 | 656,025 | 674,762 | 0.5% | 0.0% | 4.0% | 59% | −0.424 | 31% | 0.12% | −0.006 | 96 |
| Ring 1 | 196 | 813,342 | 829,240 | 1.2% | 0.0% | 3.0% | 63% | −0.679 | 28% | 0.28% | −0.013 | 93 |
| Ring 2 | 182 | 668,666 | 688,965 | 1.2% | 0.0% | 3.5% | 59% | −0.639 | 25% | 0.26% | −0.018 | 95 |
| Weapon 1 | 120 | 464,764 | 551,661 | **23.1%** | 3.1% | 32.7% | 75% | −0.065 | 32% | **3.64%** | 0.000 | 92 |
| Weapon 2 | 195 | 336,818 | 450,768 | **16.3%** | 4.3% | 28.9% | 79% | −0.217 | 34% | 0.72% | 0.000 | 88 |
| **all** | **1739** | 646,252 | 672,870 | **0.2%** | 0.0% | 4.0% | 52% | **−0.456** | 22% | 0.00% | −0.015 | **939** |

Reading it:

- **Armour slots buy floors, not damage.** Their median ΔV is 0.0% and their median Δviol is
  −0.4 to −1.3: a body armour is worth ~1.3 violation units (life, resists) and nothing
  measurable in DPS. Weapons are the mirror image: +23% / +16% median value, Δviol ≈ 0.
- **The bench craft is a floor tool too** — kept on 22% of rolls, median ΔV 0.00% with median
  Δviol −0.015, except on weapons (+3.6% value on Weapon 1). The most-chosen crafts are
  `+48 to maximum Life` (38), `+12 to all Attributes` (26), `+28 to Strength` (22),
  `+28 to maximum Energy Shield` (16).
- **The incumbent wins its own slot 939 times out of the 1,217 loop re-rolls (77%).** Once a
  build is assembled, three quarters of the 200-roll draws produce nothing better than what is
  already equipped. That is the strongest available (indirect) statement about the marginal
  value of N here, and it argues that the loop's re-rolls are where N is being wasted, not
  construction.
- Construction (522 rolls): median ΔV +0.0%, up in 29%, median Δviol −0.103.
  Loop (1,217 rolls): median ΔV +1.4%, up in 62%, median Δviol −0.772.
- Largest single feasible→feasible rolls are all weapons: stormbrand-s2 Weapon 2
  678,163 → 1,191,036 (+76%), impale_ballista-s3 Weapon 2 +75%, impale_ballista-s1
  Weapon 2 +71%.

---

## 4. Ours vs the authors' real day-1 rares

Ours: 567 rares, all ilvl 70. Authors: 299 rares parsed out of the 32 fixture builds
(ilvl percentiles over all 299); the affix/tier/craft columns come from the 93 rares already
tier-resolved in `tests/fixtures/tuadh_329/gear_tiers.json` (10 builds), which is the cheap
join — the deep dive is the other agent's.

Author item level over all 299 rares: min 10, p10 54, p25 64, **median 72**, p75 75, p90 79,
max 85. Ours is a flat 70 by rail.

| slot | ours n | affixes | crafted lines | rank% | T1/item ‖ | auth n (ilvl med) | tiered n | affixes | crafted | rank% | T1/item |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Body Armour | 57 | 5.23 | 0.79 | 0.57 | 0.11 ‖ | 31 (75) | 9 | 4.89 | 0.56 | 0.54 | 0.11 |
| Helmet | 57 | 4.98 | 0.88 | 0.54 | 0.68 ‖ | 30 (69) | 9 | 4.56 | 0.78 | 0.50 | 0.56 |
| Gloves | 57 | 5.05 | 0.95 | 0.52 | 0.91 ‖ | 30 (71) | 9 | 5.22 | 0.67 | 0.51 | 0.56 |
| Boots | 60 | 5.18 | 0.65 | 0.56 | 0.48 ‖ | 32 (69) | 10 | 4.60 | 0.60 | 0.52 | 0.70 |
| Belt | 54 | 4.93 | 0.69 | 0.52 | 0.61 ‖ | 28 (72) | 9 | 4.44 | 0.56 | 0.53 | 0.00 |
| Amulet | 54 | 4.83 | 0.91 | 0.55 | 0.43 ‖ | 29 (72) | 8 | 4.00 | 0.75 | 0.54 | 0.38 |
| Ring 1 | 57 | 4.95 | 1.04 | 0.53 | 0.82 ‖ | 30 (70) | 10 | 4.60 | 0.70 | 0.59 | 0.30 |
| Ring 2 | 60 | 4.85 | 0.95 | 0.53 | 0.87 ‖ | 32 (66) | 10 | 4.30 | 0.70 | 0.55 | 0.40 |
| Weapon 1 | 54 | 4.93 | 0.80 | 0.62 | 0.37 ‖ | 30 (76) | 9 | 4.67 | 1.00 | 0.64 | 0.44 |
| Weapon 2 | 57 | 4.86 | 0.89 | 0.56 | 0.37 ‖ | 27 (71) | 10 | 4.80 | 0.80 | 0.61 | 0.50 |
| **all** | **567** | **4.98** | **0.85** | **0.55** | **0.57** ‖ | **299 (72)** | **93** | **4.61** | **0.71** | **0.55** | **0.40** |

Tier histograms, non-crafted mods:

| | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8+ |
|---|---|---|---|---|---|---|---|---|
| ours (2,824 mods) | 11% | 15% | 20% | 19% | 12% | 8% | 6% | 9% |
| authors (422 mods) | 9% | 21% | 18% | 15% | 13% | 9% | 6% | 9% |

**Verdict.** Mean tier rank is identical (0.55 vs 0.55) and per-mod rarity is identical
(−log10 share 1.45 vs 1.45). Where we are ahead of the authors: **+0.37 affixes per item**
(4.98 vs 4.61), **+0.17 T1 mods per item** (0.57 vs 0.40, and 8% vs 6% of items with two or
more), **+0.14 crafted lines per item**. Where we are behind: our item level is pinned at 70
while their median is 72 (p90 79, max 85), which costs us the top tier of the high-ilvl mod
groups entirely — and it shows in the weapons, the one place where the authors' per-mod rarity
beats ours (1.69 vs 1.62 on Weapon 1). Two things follow, both measurable:

- The gap is **affix count, not mod quality**. Best-of-200 with a uniform `{4,4,4,5,5,6}` mod
  count is what pushes 6-mod items from 17% to 26%; the authors sit at 19%. A day-1 player's
  real rares are a mix of 4- and 5-mod drops and our selection quietly upgrades that.
- The rails' own tier caps (`max_t1_per_rare: 1`, `max_t2_per_rare: 2`, `max_tier: 8`) are dead
  code as far as the current pipeline goes: they are read by `GearFiller`, which the pipeline
  no longer uses. 8% of our rares are above the T1 cap and 22% carry a mod below T8.
  Either the caps belong in `LootGear` as a rejection filter on the 200 rolls, or they should
  be deleted from `rails_default.json` so nothing claims a rule that is not enforced.

Per-run split (the two runs are the same distribution; nothing about the rules smoke changed
the gear):

| run | rares | affixes/item | rank% | T1/item | median product | p10 |
|---|---|---|---|---|---|---|
| rules-smoke | 174 | 5.06 | 0.54 | 0.60 | 3.2e-08 | 1.1e-09 |
| core14 | 393 | 4.95 | 0.55 | 0.55 | 6.6e-08 | 2.0e-09 |

---

## 5. Method

Read-only throughout; two PoB sessions, never concurrent, used only to list mod pools
(`PobSession.list_item_mods`) — no calc, no trial, no build was loaded.

1. **Items.** Every `*.pob.txt` in the two benchmark folders decoded with
   `junkroan.pob.session.decode_import_code`, the `<Items>` block parsed for the active
   `ItemSet`, swap / flask / jewel slots dropped, `Rarity: RARE` kept. Our rares carry their
   generator lines (`Prefix: {range:0.54}IncreasedLife8`), so every affix is a PoB mod id
   already — no text matching, 0 of 2,824 unresolved. `{crafted}` lines are counted with the
   same decorated-line rule `optimizer/audit.py` uses (`_DECORATED_LINE`, `crafted_families`);
   they are excluded from tier and luck statistics because a bench craft is a deterministic
   choice, not a roll.
2. **Ladders.** For each of the 85 bases, `list_item_mods(base)` gives the full ladder
   (PoB sorts by group then level descending, so position = tier, exactly the convention of
   `scripts/fixture_gear_tiers.py` and `gear_tiers.json`) and `list_item_mods(base, ilvl=70)`
   gives the pool the roller actually drew from (`_RANDOM_RARES_LUA` filters `mod.level <=
   ilvl` and `GetModSpawnWeight > 0`). Tier ilvl = the mod's `level`. `rank70%` ranks within
   the sub-ladder reachable at ilvl 70.
3. **Luck.** share = Σ weight of the group's mods with `level >= chosen level` that exist in
   the ilvl-70 pool, ÷ Σ weight of that affix type in the ilvl-70 pool. The measure follows
   `scripts/gear_rarity_calibration.py` (which uses the mod's own weight; "at or above the
   chosen tier" was the brief here) and is applied to the authors' rares unchanged, each at
   its own item level, with their tiers taken from `gear_tiers.json` and the mod id recovered
   as `ladder[group][tier-1]`. Product = Π share over an item's non-crafted affixes. It is a
   rarity index, not a probability: the roller draws sequentially without replacement with
   family blocking, so the true item probability is smaller and depends on the draw order; the
   index is the right shape for comparing items and for comparing our rares with the authors'.
4. **Logs.** `[<slot>] best of <N>: A -> B (viol a -> b)[; bench <line>: -> C (viol c)]`
   parsed from the 18 rules-smoke logs (1,739 rolls), plus the pipeline's
   `<slot>: incumbent kept` lines (939). A is the build **with the slot empty** in every case
   except the first of the two construction passes of `fill(passes=2)`; the old item competes
   as a trial, so the line never trades down.
5. **Authors.** Item levels and affix counts from all 299 fixture rares
   (`tests/fixtures/tuadh_329/*.pob.txt`); tiers from the 93 of them already resolved in
   `gear_tiers.json`, joined to slots by (build, name, base). 93 of the 94 join; the one that
   does not is Cold DoT's swap wand (Spirit Spire, Quartz Wand), which the slot filter drops
   on both sides.

Numbers regenerable from the scripts in this session's scratchpad; nothing was written to the
repository except this file.
