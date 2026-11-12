# Real day-1 rares: 32 Tuadh characters, 5 Zizaran starter wishlists (2026-09-18)

What the two human standards for day-1 gear actually look like, measured against PoB's own mod
tables: item level, affix counts, tiers, spawn-weight "luck", and how many of each item's mods
the build in fact uses.

- **Realism standard** — `tests/fixtures/tuadh_329/*.pob.txt`, 32 characters, PoB snapshots taken
  right after the two stone bosses. The rares are what dropped or was bought by then, not target
  items. 299 rares, 1322 rolled mods + 226 bench crafts.
- **Readability standard** — `tests/fixtures/zizaran_329/`, 5 league-starter guides, the **early
  item set** of each (`manifest.json` `early_loadout`). These are hand-written wishlists: no item
  levels, mod ranges instead of rolled values, 46 rares, 106 rolled mods + 16 bench crafts.

A deterministic day-1 gearing rail has to sit between them: Tuadh's numbers are what a character
really carries, Zizaran's are what a person writes down as "good enough to clear the campaign".

---

## Summary, the two sources side by side

| measure | Tuadh (real snapshots) | Zizaran (wishlists) |
|---|--:|--:|
| rares measured | 299 | 46 |
| affixes per rare (prefix + suffix, crafts included) | **5.17** | **2.65** |
| prefixes / suffixes per rare | 2.52 / 2.65 | 1.33 / 1.33 |
| items with at least one bench craft | **76%** | **35%** |
| items with a free affix slot (<3 P or <3 S) | 67% | **100%** |
| median tier | T4 (0.50 of the ladder) | T3 (0.48 of the ladder) |
| T1-T2 share of rolled mods | 26% | 26% |
| median item level | 72 (p10 54, p90 79) | not stated in the items |
| median spawn-weight product P | 10^-6.1 | 10^-3.2 |
| mods the build actually uses | **47%** (2.44 of 5.2 per item) | **57%** (1.53 of 2.7 per item) |
| useless mods per item | **2.79** | **1.13** |
| uniques per build | 0.28 (9 over 32 builds) | 0.6 (3 over 5) |

---

## 1. Tuadh's snapshots — per slot

### 1a. Count, item level, affix counts, crafts, free affix slots

"pref"/"suff"/"total" are means per item, bench crafts counted; "<3P" is the share of items with a
free prefix slot.


| slot | n | ilvl min/med/max | pref | suff | total | crafted/item | >=1 craft | <3P | <3S | <3P or <3S |
|---|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 31 | 59 / 75 / 82 | 2.35 | 2.71 | 5.06 | 0.71 | 22 (71%) | 61% | 35% | 77% |
| Helmet | 30 | 34 / 69 / 82 | 2.40 | 2.83 | 5.23 | 0.73 | 22 (73%) | 50% | 10% | 60% |
| Gloves | 30 | 43 / 71 / 79 | 2.50 | 2.67 | 5.17 | 0.77 | 23 (77%) | 43% | 30% | 67% |
| Boots | 32 | 41 / 69 / 81 | 2.66 | 2.66 | 5.31 | 0.81 | 26 (81%) | 34% | 34% | 62% |
| Belt | 28 | 54 / 72 / 83 | 2.29 | 2.57 | 4.86 | 0.57 | 16 (57%) | 57% | 36% | 79% |
| Amulet | 29 | 25 / 72 / 83 | 2.45 | 2.76 | 5.21 | 0.83 | 24 (83%) | 48% | 24% | 59% |
| Ring 1 | 30 | 20 / 70 / 82 | 2.43 | 2.77 | 5.20 | 0.67 | 20 (67%) | 47% | 20% | 67% |
| Ring 2 | 32 | 26 / 66 / 82 | 2.38 | 2.84 | 5.22 | 0.72 | 23 (72%) | 53% | 16% | 59% |
| Weapon 1 | 30 | 10 / 76 / 85 | 2.97 | 2.23 | 5.20 | 0.90 | 27 (90%) | 23% | 67% | 77% |
| Weapon 2 | 7 | 61 / 77 / 83 | 3.29 | 2.14 | 5.43 | 1.00 | 7 (100%) | 14% | 43% | 43% |
| Shield/Quiver | 20 | 47 / 70 / 79 | 2.65 | 2.45 | 5.10 | 0.80 | 16 (80%) | 30% | 45% | 75% |
| ALL | 299 | 10 / 72 / 85 | 2.52 | 2.65 | 5.17 | 0.76 | 76% | 44% | 31% | 67% |

Read across: every slot sits at 4.9-5.4 affixes, so a full 6-mod rare is the exception, not the
norm (34% of items); two thirds still have a free affix slot. Weapons are the one place where the
prefixes are full (2.97 of 3, only 23% with a free prefix) and the suffixes are not (67% under 3);
on every other slot it is the other way round, a free prefix on 34-61% of items.

### 1b. Item level, all 299 rares pooled — the direct evidence for the day-1 ilvl rail

```
n = 299 p10 = 54.0 p25 = 64.5 p50 = 72 p75 = 75.0 p90 = 79.0 min 10 max 85
ilvl histogram (bins of 10): [(10, 1), (20, 3), (30, 4), (40, 14), (50, 18), (60, 79), (70, 161), (80, 19)]
share ilvl >= 68: 66%  >= 75: 34%  < 60: 13%
```

### 1c. Affix-count histogram

```
{3: '4 (1%)', 4: '49 (16%)', 5: '141 (47%)', 6: '103 (34%)', 7: '2 (1%)'}
prefix histogram: {1: 19, 2: 114, 3: 158, 4: 7, 5: 1}  suffix: {0: 1, 1: 13, 2: 80, 3: 202, 4: 3}
crafted mods per item: {0: 73, 1: 226}
```

Exactly one bench craft on 226 of 299 items (76%) and never two, which matches the game's
one-craft rule. 4 items carry 3 affixes and 2 carry 7 (see the legality note in the method).

### 2. Tier distribution per slot

T1 = the best tier of that mod's ladder on that base; "med tier/ladder" is the tier as a fraction
of the ladder's length (0.5 = the middle of the ladder).


| slot | mods | T1 | T2 | T3 | T4 | T5 | T6 | T7+ | med tier | med tier/ladder | T1-2 share |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 136 | 5 (4%) | 21 (15%) | 34 (25%) | 24 (18%) | 21 (15%) | 14 (10%) | 17 (12%) | 4 | 0.50 | 19% |
| Helmet | 135 | 17 (13%) | 20 (15%) | 23 (17%) | 29 (21%) | 22 (16%) | 11 (8%) | 13 (10%) | 4 | 0.50 | 27% |
| Gloves | 132 | 14 (11%) | 26 (20%) | 26 (20%) | 28 (21%) | 18 (14%) | 11 (8%) | 9 (7%) | 4 | 0.50 | 30% |
| Boots | 144 | 20 (14%) | 26 (18%) | 27 (19%) | 24 (17%) | 18 (12%) | 17 (12%) | 12 (8%) | 3 | 0.50 | 32% |
| Belt | 120 | 12 (10%) | 17 (14%) | 24 (20%) | 20 (17%) | 13 (11%) | 15 (12%) | 19 (16%) | 4 | 0.50 | 24% |
| Amulet | 127 | 7 (6%) | 17 (13%) | 28 (22%) | 26 (20%) | 15 (12%) | 10 (8%) | 24 (19%) | 4 | 0.56 | 19% |
| Ring 1 | 136 | 25 (18%) | 18 (13%) | 28 (21%) | 21 (15%) | 18 (13%) | 11 (8%) | 15 (11%) | 3 | 0.50 | 32% |
| Ring 2 | 144 | 15 (10%) | 24 (17%) | 14 (10%) | 33 (23%) | 19 (13%) | 15 (10%) | 24 (17%) | 4 | 0.60 | 27% |
| Weapon 1 | 131 | 11 (8%) | 19 (15%) | 15 (11%) | 24 (18%) | 23 (18%) | 9 (7%) | 30 (23%) | 4 | 0.62 | 23% |
| Weapon 2 | 31 | 2 (6%) | 5 (16%) | 5 (16%) | 3 (10%) | 3 (10%) | 2 (6%) | 11 (35%) | 5 | 0.62 | 23% |
| Shield/Quiver | 86 | 6 (7%) | 19 (22%) | 18 (21%) | 17 (20%) | 11 (13%) | 5 (6%) | 10 (12%) | 4 | 0.50 | 29% |
| ALL | 1322 | 134 (10%) | 212 (16%) | 242 (18%) | 249 (19%) | 181 (14%) | 120 (9%) | 184 (14%) | 4 | 0.50 | 26% |


Tier as a fraction of its ladder (p25 / p50 / p75):

```
  Body Armour    p25=0.38 p50=0.50 p75=0.61
  Helmet         p25=0.33 p50=0.50 p75=0.67
  Gloves         p25=0.33 p50=0.50 p75=0.70
  Boots          p25=0.33 p50=0.50 p75=0.67
  Belt           p25=0.30 p50=0.50 p75=0.67
  Amulet         p25=0.38 p50=0.56 p75=0.76
  Ring 1         p25=0.33 p50=0.50 p75=0.75
  Ring 2         p25=0.38 p50=0.60 p75=0.78
  Weapon 1       p25=0.41 p50=0.62 p75=0.83
  Weapon 2       p25=0.44 p50=0.62 p75=0.88
  Shield/Quiver  p25=0.33 p50=0.50 p75=0.67
  ALL            p25=0.33 p50=0.50 p75=0.75
```

The authors' rares sit in the middle of every ladder: a median of T4 and 0.50 of the ladder,
with 26% of mods at T1-T2 and 14% at T7 or worse. Weapons are the worst-rolled slot
(median 0.62 of the ladder, 23% at T7+); boots and rings the best (0.50, 32% at T1-T2).

### 3. How "lucky" are these items — spawn-weight share

For each rolled mod: P(mod) = the spawn weight of every mod of its family at or above its tier and
legal at the item's ilvl, over the total weight of that affix pool (prefix pool for a prefix,
suffix pool for a suffix) at the same base and ilvl. The item's P is the product over its rolled
mods; bench crafts are chosen, not rolled, and are excluded. "min P (rarest)" is the least likely
item of that slot, "max P (plainest)" the most ordinary.


| slot | items | median P | median -log10 P | min P (rarest) | max P (plainest) | median per-mod share | median -log10 P (ladder) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 31 | 10^-5.5 | 5.55 | 10^-8.8 | 10^-3.2 | 0.045 (1 in 22) | 5.55 |
| Helmet | 30 | 10^-6.2 | 6.20 | 10^-8.9 | 10^-3.5 | 0.041 (1 in 24) | 6.20 |
| Gloves | 30 | 10^-6.0 | 5.97 | 10^-9.1 | 10^-2.6 | 0.047 (1 in 21) | 5.97 |
| Boots | 32 | 10^-5.5 | 5.51 | 10^-8.9 | 10^-3.8 | 0.049 (1 in 21) | 5.51 |
| Belt | 28 | 10^-5.4 | 5.43 | 10^-8.9 | 10^-3.3 | 0.055 (1 in 18) | 5.46 |
| Amulet | 29 | 10^-6.7 | 6.72 | 10^-10.1 | 10^-4.4 | 0.027 (1 in 37) | 6.72 |
| Ring 1 | 30 | 10^-6.8 | 6.82 | 10^-11.2 | 10^-3.7 | 0.028 (1 in 35) | 6.82 |
| Ring 2 | 32 | 10^-6.2 | 6.24 | 10^-10.3 | 10^-4.0 | 0.032 (1 in 32) | 6.24 |
| Weapon 1 | 30 | 10^-6.0 | 6.01 | 10^-8.4 | 10^-2.9 | 0.039 (1 in 26) | 6.65 |
| Weapon 2 | 7 | 10^-6.2 | 6.20 | 10^-7.4 | 10^-2.3 | 0.053 (1 in 19) | 7.41 |
| Shield/Quiver | 20 | 10^-6.3 | 6.31 | 10^-8.9 | 10^-4.4 | 0.034 (1 in 30) | 6.36 |
| ALL | 299 | 10^-6.1 | 6.07 | 10^-11.2 | 10^-2.3 | 0.040 (1 in 25) | 6.13 |
pooled -log10 P: p10=4.56 p50=6.07 p90=8.10


A typical Tuadh rare is a 10^-6 draw on its affix pool — about one in a million *if* you rolled
that exact set of families-at-that-tier in one go, i.e. roughly 1 in 25 per mod, five mods deep.
Jewellery is the rarest (rings 10^-6.8, amulets 10^-6.7: the biggest affix pools), armour and
belts the plainest (10^-5.4 to 10^-5.5).

### 4. Top mod families per slot (frequency, median tier)


**Body Armour** (31 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 19 | 61% | T6 |
| ColdResistance | 16 | 52% | T3 |
| DefencesPercent | 16 | 52% | T4 |
| BaseLocalDefences | 15 | 48% | T3 |
| LightningResistance | 14 | 45% | T3 |
| FireResistance | 11 | 35% | T4 |
| IncreasedMana | 9 | 29% | T7 |
| LifeRegeneration | 8 | 26% | T6 |
| StunRecovery | 6 | 19% | T5 |
| (craft) ColdResistance | 5 | 16% | craft |
| LocalAttributeRequirements | 5 | 16% | T2 |
| (craft) BaseLocalDefences | 4 | 13% | craft |

**Helmet** (30 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 27 | 90% | T3 |
| FireResistance | 14 | 47% | T4 |
| ColdResistance | 13 | 43% | T5 |
| BaseLocalDefences | 12 | 40% | T6 |
| LightningResistance | 10 | 33% | T4 |
| DefencesPercent | 8 | 27% | T4 |
| Intelligence | 7 | 23% | T7 |
| LifeRegeneration | 7 | 23% | T4 |
| IncreasedMana | 6 | 20% | T5 |
| (craft) ColdResistance | 5 | 17% | craft |
| AttackerTakesDamageNoRange | 5 | 17% | T1 |
| (craft) DefencesPercent | 4 | 13% | craft |

**Gloves** (30 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 22 | 73% | T2 |
| ColdResistance | 17 | 57% | T4 |
| LightningResistance | 15 | 50% | T4 |
| FireResistance | 13 | 43% | T5 |
| BaseLocalDefences | 10 | 33% | T2 |
| LifeRegeneration | 7 | 23% | T4 |
| (craft) IncreasedLife | 6 | 20% | craft |
| DefencesPercent | 6 | 20% | T4 |
| Dexterity | 5 | 17% | T7 |
| FireDamage | 5 | 17% | T3 |
| LightningDamage | 5 | 17% | T2 |
| (craft) FireResistance | 4 | 13% | craft |

**Boots** (32 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 24 | 75% | T2 |
| MovementVelocity | 22 | 69% | T3 |
| LightningResistance | 16 | 50% | T6 |
| ColdResistance | 15 | 47% | T4 |
| FireResistance | 15 | 47% | T5 |
| (craft) MovementVelocity | 10 | 31% | craft |
| DefencesPercent | 9 | 28% | T4 |
| StunRecovery | 9 | 28% | T2 |
| BaseLocalDefences | 6 | 19% | T2 |
| LifeRegeneration | 6 | 19% | T4 |
| (craft) IncreasedLife | 5 | 16% | craft |
| Dexterity | 4 | 12% | T5 |

**Belt** (28 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 28 | 100% | T3 |
| IncreasedMana | 14 | 50% | T5 |
| LightningResistance | 12 | 43% | T4 |
| Strength | 8 | 29% | T6 |
| BeltFlaskRecoveryRate | 7 | 25% | T3 |
| FireResistance | 7 | 25% | T3 |
| LifeRegeneration | 7 | 25% | T6 |
| ColdResistance | 6 | 21% | T4 |
| StunRecovery | 6 | 21% | T3 |
| (craft) FireResistance | 5 | 18% | craft |
| IncreasedEnergyShield | 5 | 18% | T7 |
| IncreasedPhysicalDamageReductionRating | 5 | 18% | T6 |

**Amulet** (29 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 19 | 66% | T3 |
| AllResistances | 8 | 28% | T3 |
| CriticalStrikeMultiplier | 8 | 28% | T2 |
| EvasionRatingPercent | 8 | 28% | T6 |
| LightningResistance | 8 | 28% | T3 |
| (craft) IncreasedLife | 6 | 21% | craft |
| LifeRegeneration | 6 | 21% | T6 |
| LightningDamage | 6 | 21% | T6 |
| ColdResistance | 5 | 17% | T6 |
| CriticalStrikeChanceIncrease | 5 | 17% | T4 |
| Dexterity | 5 | 17% | T3 |
| IncreasedEnergyShield | 5 | 17% | T7 |

**Ring 1** (30 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 21 | 70% | T1 |
| LightningResistance | 11 | 37% | T5 |
| ColdResistance | 10 | 33% | T5 |
| PhysicalDamage | 10 | 33% | T2 |
| IncreasedEnergyShield | 9 | 30% | T5 |
| AllResistances | 7 | 23% | T2 |
| IncreasedCastSpeed | 7 | 23% | T2 |
| Strength | 7 | 23% | T3 |
| (craft) IncreasedLife | 6 | 20% | craft |
| ItemFoundRarityIncreasePrefix | 5 | 17% | T3 |
| LightningDamage | 5 | 17% | T7 |
| Dexterity | 4 | 13% | T5 |

**Ring 2** (32 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 22 | 69% | T2 |
| ColdResistance | 11 | 34% | T5 |
| FireResistance | 11 | 34% | T4 |
| IncreasedMana | 10 | 31% | T8 |
| IncreasedEnergyShield | 8 | 25% | T8 |
| LightningResistance | 8 | 25% | T6 |
| AllResistances | 6 | 19% | T4 |
| ColdDamage | 6 | 19% | T6 |
| Dexterity | 6 | 19% | T6 |
| Strength | 6 | 19% | T5 |
| (craft) FireResistance | 5 | 16% | craft |
| (craft) IncreasedLife | 5 | 16% | craft |

**Weapon 1** (30 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| WeaponCasterDamagePrefix | 16 | 53% | T7 |
| CriticalStrikeMultiplier | 10 | 33% | T4 |
| (craft) WeaponCasterDamagePrefix | 8 | 27% | craft |
| ColdDamage | 8 | 27% | T4 |
| IncreasedAttackSpeed | 8 | 27% | T3 |
| IncreasedMana | 8 | 27% | T7 |
| SpellAddedElementalDamage | 8 | 27% | T4 |
| PhysicalDamage | 7 | 23% | T4 |
| FireDamage | 6 | 20% | T4 |
| CriticalStrikeChanceIncrease | 5 | 17% | T4 |
| IncreaseSpecificSocketedGemLevel | 5 | 17% | T1 |
| LightningDamage | 5 | 17% | T6 |

**Weapon 2** (7 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| SpellAddedElementalDamage | 5 | 71% | T4 |
| WeaponCasterDamagePrefix | 4 | 57% | T7 |
| (craft) WeaponCasterDamagePrefix | 3 | 43% | craft |
| IncreaseSpecificSocketedGemLevel | 2 | 29% | T2 |
| IncreasedAccuracy | 2 | 29% | T2 |
| IncreasedAttackSpeed | 2 | 29% | T7 |
| IncreasedCastSpeed | 2 | 29% | T5 |
| IncreasedMana | 2 | 29% | T6 |
| PhysicalDamage | 2 | 29% | T4 |
| (craft) CriticalStrikeChanceIncrease | 1 | 14% | craft |
| (craft) IncreasedCastSpeed | 1 | 14% | craft |
| (craft) LocalPhysicalDamagePercent | 1 | 14% | craft |

**Shield/Quiver** (20 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 9 | 45% | T3 |
| IncreasedShieldBlockPercentage | 9 | 45% | T4 |
| BaseLocalDefences | 6 | 30% | T4 |
| FireResistance | 6 | 30% | T6 |
| LightningResistance | 6 | 30% | T4 |
| AllResistances | 5 | 25% | T2 |
| ColdResistance | 5 | 25% | T3 |
| (craft) FireResistance | 4 | 20% | craft |
| DefencesPercent | 4 | 20% | T6 |
| WeaponCasterDamagePrefix | 4 | 20% | T5 |
| (craft) IncreasedLife | 3 | 15% | craft |
| (craft) IncreasedShieldBlockPercentage | 3 | 15% | craft |

### 5. Per build


| build | rare | unique | magic | empty | affixes/rare | mean tier | med tier | ilvl range | med -log10 P |
|---|--:|--:|--:|--:|--:|--:|--:|---|--:|
| stormbrand | 9 | 0 | 1 | 0 | 5.2 | 3.9 | 4 | 20-81 | 6.3 |
| smite | 9 | 0 | 1 | 0 | 5.6 | 3.7 | 3 | 64-77 | 6.5 |
| spark | 9 | 0 | 1 | 0 | 4.9 | 4.5 | 4 | 50-83 | 5.1 |
| ignite_penance_brand | 9 | 1 | 0 | 0 | 5.2 | 4.0 | 3 | 42-75 | 7.3 |
| hit_penance_brand | 10 | 0 | 0 | 0 | 5.2 | 5.0 | 4 | 34-83 | 6.1 |
| poison_spectral_throw | 8 | 2 | 0 | 0 | 5.1 | 4.2 | 3 | 36-75 | 5.8 |
| regular_viper_strike | 10 | 0 | 0 | 0 | 4.8 | 4.1 | 4 | 45-78 | 5.2 |
| winter_orb | 9 | 1 | 0 | 0 | 5.1 | 4.2 | 4 | 59-78 | 5.9 |
| physical_dot | 10 | 0 | 0 | 0 | 4.9 | 4.2 | 4 | 10-75 | 6.6 |
| cold_dot | 10 | 0 | 0 | 0 | 5.3 | 4.6 | 5 | 47-85 | 6.0 |
| bleed_bow | 10 | 0 | 0 | 0 | 4.8 | 3.7 | 3 | 65-79 | 5.8 |
| toxic_rain | 9 | 0 | 1 | 0 | 4.8 | 4.5 | 4 | 34-79 | 5.6 |
| absolution_minions | 9 | 1 | 0 | 0 | 5.1 | 4.2 | 4 | 54-78 | 5.8 |
| summon_raging_spirits | 10 | 0 | 0 | 0 | 5.4 | 4.1 | 4 | 62-78 | 7.1 |
| impale_ballista | 10 | 0 | 0 | 0 | 5.1 | 3.8 | 4 | 54-76 | 6.0 |
| pyroclast_mine | 10 | 0 | 0 | 0 | 5.5 | 3.8 | 4 | 59-82 | 6.6 |
| lightning_trap | 10 | 0 | 0 | 0 | 5.1 | 4.0 | 4 | 69-79 | 5.4 |
| vd_spellslinger | 9 | 0 | 1 | 0 | 5.6 | 4.2 | 4 | 43-78 | 7.1 |
| arc_archmage | 10 | 0 | 0 | 0 | 5.3 | 4.4 | 4 | 55-80 | 6.3 |
| impale_cyclone | 9 | 0 | 0 | 1 | 4.9 | 3.8 | 4 | 60-79 | 5.7 |
| spectral_shield_throw | 10 | 0 | 0 | 0 | 5.1 | 4.2 | 4 | 33-82 | 5.7 |
| kinetic_bolt_wander | 8 | 2 | 0 | 0 | 5.4 | 3.8 | 4 | 26-79 | 6.7 |
| soulrend_chaos_dot | 10 | 0 | 0 | 0 | 4.9 | 4.3 | 4 | 45-81 | 5.8 |
| shockwave_cyclone | 9 | 0 | 0 | 1 | 5.3 | 3.7 | 4 | 54-82 | 6.0 |
| static_strike | 9 | 0 | 0 | 1 | 5.3 | 4.1 | 4 | 45-76 | 6.3 |
| bleed_perforate | 7 | 0 | 2 | 1 | 5.3 | 4.0 | 4 | 41-77 | 5.8 |
| kinetic_fusillade | 10 | 0 | 0 | 0 | 5.4 | 3.5 | 4 | 48-78 | 6.8 |
| burning_arrow_snipe | 7 | 2 | 1 | 0 | 5.6 | 4.0 | 4 | 25-79 | 7.0 |
| poison_spark | 10 | 0 | 0 | 0 | 5.3 | 3.6 | 3 | 63-82 | 6.5 |
| elemental_hit | 10 | 0 | 0 | 0 | 5.0 | 4.0 | 4 | 64-83 | 6.2 |
| archmage_volatile_dead | 10 | 0 | 0 | 0 | 4.9 | 4.2 | 4 | 63-80 | 5.6 |
| exsanguinate_mines | 10 | 0 | 0 | 0 | 5.2 | 4.0 | 4 | 43-82 | 6.3 |
| **all 32** | 299 | 9 | 8 | 4 | 5.2 | 4.1 | 4 | 10-85 | 6.1 |


### 6. Uniques

```
builds with >=1 unique: 6 / 32 | total uniques: 9
by slot: {'Helmet': 1, 'Weapon 1': 2, 'Amulet': 1, 'Belt': 3, 'Gloves': 1, 'Weapon 2': 1}
  ignite_penance_brand     Helmet: Honourhome
  poison_spectral_throw    Weapon 1: The Wasp Nest, Amulet: Natural Hierarchy
  winter_orb               Belt: Dyadian Dawn
  absolution_minions       Weapon 1: Sign of the Sin Eater
  kinetic_bolt_wander      Gloves: Doedre's Tenure, Belt: Belt of the Deceiver
  burning_arrow_snipe      Belt: Prismweave, Weapon 2: The Poised Prism

magic / normal items:
  stormbrand               magic=['Amulet'] normal=[]
  smite                    magic=['Body Armour'] normal=[]
  spark                    magic=['Gloves'] normal=[]
  toxic_rain               magic=['Ring 1'] normal=[]
  vd_spellslinger          magic=['Ring 1'] normal=[]
  bleed_perforate          magic=['Belt', 'Amulet'] normal=[]
  burning_arrow_snipe      magic=['Helmet'] normal=[]
```

---

## 7. How many of the mods does the build actually use?

PoB judges, one mod at a time: the item is re-evaluated through PoB's item-override what-if with
that mod's lines deleted, and the mod counts as **useful** when the build loses at least 0.5% of
its objective value **or** breaks a floor it was meeting (life, the four maximum-hit-taken floors,
the three resistance floors, movement speed, attribute requirements, mana/life cost and the
per-second sustain relations — the rails objective, `objective_for(Rails.load(), <main skill>)`).


items judged: 299 of 299 | builds whose calc failed: none
| slot | items | mods | useful | useless | useful/item mean | median | useless/item mean | 0 useful | >=4 useful |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 31 | 158 | 60 (38%) | 98 (62%) | 1.94 | 2 | 3.16 | 13% | 13% |
| Helmet | 30 | 157 | 68 (43%) | 89 (57%) | 2.27 | 2 | 2.97 | 10% | 17% |
| Gloves | 30 | 156 | 66 (42%) | 90 (58%) | 2.20 | 2 | 3.00 | 13% | 17% |
| Boots | 32 | 171 | 83 (49%) | 88 (51%) | 2.59 | 3 | 2.75 | 3% | 22% |
| Belt | 28 | 141 | 55 (39%) | 86 (61%) | 1.96 | 2 | 3.07 | 18% | 7% |
| Amulet | 29 | 152 | 75 (49%) | 77 (51%) | 2.59 | 3 | 2.66 | 10% | 21% |
| Ring 1 | 30 | 157 | 67 (43%) | 90 (57%) | 2.23 | 2 | 3.00 | 10% | 20% |
| Ring 2 | 32 | 167 | 80 (48%) | 87 (52%) | 2.50 | 2 | 2.72 | 3% | 22% |
| Weapon 1 | 30 | 163 | 102 (63%) | 61 (37%) | 3.40 | 4 | 2.03 | 0% | 53% |
| Weapon 2 | 7 | 39 | 29 (74%) | 10 (26%) | 4.14 | 4 | 1.43 | 0% | 71% |
| Shield/Quiver | 20 | 104 | 46 (44%) | 58 (56%) | 2.30 | 2 | 2.90 | 10% | 30% |
| ALL | 299 | 1565 | 731 (47%) | 834 (53%) | 2.44 | 2 | 2.79 | 9% | 23% |

useful-mods-per-item histogram (all slots): {0: '26 (9%)', 1: '41 (14%)', 2: '89 (30%)', 3: '74 (25%)', 4: '55 (18%)', 5: '14 (5%)'}
useless-mods-per-item histogram: {0: '8 (3%)', 1: '47 (16%)', 2: '73 (24%)', 3: '85 (28%)', 4: '54 (18%)', 5: '22 (7%)', 6: '10 (3%)'}


#### Families most often useless (Tuadh, families with 4+ occurrences)


| family | n | useless share |
|---|--:|--:|
| StunRecovery | 23 | 100% |
| ItemFoundRarityIncreasePrefix | 15 | 100% |
| LocalAttributeRequirements | 14 | 100% |
| AttackerTakesDamageNoRange | 10 | 100% |
| IncreasedShieldBlockPercentage | 9 | 100% |
| EvasionRatingPercent | 8 | 100% |
| BeltFlaskRecoveryRate | 7 | 100% |
| ItemFoundRarityIncrease | 7 | 100% |
| StunDurationIncreasePercent | 7 | 100% |
| ChaosResistance | 5 | 100% |
| StunThresholdReduction | 5 | 100% |
| LifeGainedFromEnemyDeath | 4 | 100% |
| EnergyShieldDelay | 4 | 100% |
| (craft) DefencesPercent | 9 | 89% |
| IncreasedEvasionRating | 8 | 88% |
| DefencesPercentAndStunRecovery | 12 | 83% |
| (craft) BaseLocalDefences | 6 | 83% |
| IncreasedPhysicalDamageReductionRating | 5 | 80% |
| BaseLocalDefences | 49 | 78% |
| DamageTakenGainedAsLife | 4 | 75% |
| IncreasedEnergyShield | 27 | 74% |
| FireDamage | 18 | 72% |
| LifeRegeneration | 49 | 71% |
| IncreasedWeaponElementalDamagePercent | 7 | 71% |
| (unresolved) | 17 | 71% |

families always useful (n >= 4): ['(craft) WeaponCasterDamagePrefix', '(craft) MovementVelocity', '(craft) IncreasedCastSpeed', '(craft) IncreasedMana', '(craft) LightningDamage', 'GlobalDamageOverTimeMultiplier', 'SpellCriticalStrikeChanceIncrease', '(craft) Intelligence', '(craft) PhysicalDamage', '(craft) LocalPhysicalDamagePercent']


#### Useful share by tier, affix type and craft (Tuadh)

```
by tier: {'T1': '54/134 = 40%', 'T2': '101/212 = 48%', 'T3': '118/242 = 49%', 'T4': '100/249 = 40%', 'T5': '72/181 = 40%', 'T6': '48/120 = 40%', 'T7+': '80/184 = 43%'}
by affix: {'Prefix': '289/640 = 45%', 'Suffix': '284/682 = 42%'}
bench crafts: 153/226 = 68% useful
```


**More than half of what a real day-1 character carries does nothing for its build.** 2.79 dead
mods per item, and only 23% of items have 4 or more live ones. The weapon is the exception (63%
useful, 3.40 live mods) because every offensive mod on it feeds the main skill; body armour and
belts are the worst (38-39%). Resistances and life count as useful only while a floor is still
missed, which is why a resist family can be 0% useless on one slot and high on another.

Tier does not predict usefulness at all (T1 40%, T3 49%, T7+ 43%): what matters is whether the
family touches the build, not how well it rolled. The one mod a person chose is the one that lands:
bench crafts are 68% useful (153 of 226) against 43% for the rolled mods (573 of 1322), and
prefixes and suffixes are equally dead (45% / 42%).

---

## 8. Zizaran's early-game wishlists — the readability standard

Five league-starter guides, the author's own "Early Game" item set. These are written by hand: no
`Item Level` line, mod ranges instead of rolled values, and bench crafts often typed as plain
lines.

### 8a. Count, affix counts, crafts, free affix slots


| slot | n | ilvl min/med/max | pref | suff | total | crafted/item | >=1 craft | <3P | <3S | <3P or <3S |
|---|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 5 | n/a | 1.40 | 1.20 | 2.60 | 0.40 | 2 (40%) | 80% | 100% | 100% |
| Helmet | 4 | n/a | 1.00 | 1.75 | 2.75 | 0.25 | 1 (25%) | 100% | 100% | 100% |
| Gloves | 4 | n/a | 1.25 | 1.50 | 2.75 | 0.50 | 2 (50%) | 100% | 100% | 100% |
| Boots | 5 | n/a | 2.00 | 0.80 | 2.80 | 0.20 | 1 (20%) | 100% | 100% | 100% |
| Belt | 5 | n/a | 1.60 | 1.00 | 2.60 | 0.40 | 2 (40%) | 80% | 100% | 100% |
| Amulet | 5 | n/a | 1.00 | 1.80 | 2.80 | 0.40 | 2 (40%) | 100% | 80% | 100% |
| Ring 1 | 4 | n/a | 1.00 | 1.25 | 2.25 | 0.50 | 2 (50%) | 100% | 100% | 100% |
| Ring 2 | 5 | n/a | 1.00 | 1.40 | 2.40 | 0.60 | 3 (60%) | 100% | 100% | 100% |
| Weapon 1 | 5 | n/a | 1.60 | 1.20 | 2.80 | 0.20 | 1 (20%) | 100% | 100% | 100% |
| Shield/Quiver | 4 | n/a | 1.25 | 1.50 | 2.75 | 0.00 | 0 (0%) | 100% | 100% | 100% |
| ALL | 46 | n/a | 1.33 | 1.33 | 2.65 | 0.35 | 35% | 96% | 98% | 100% |


```
{1: '2 (4%)', 2: '14 (30%)', 3: '28 (61%)', 4: '2 (4%)'}
prefix histogram: {1: 33, 2: 11, 3: 2}  suffix: {0: 5, 1: 22, 2: 18, 3: 1}
crafted mods per item: {0: 30, 1: 16}
```

**Every single wishlist item has a free affix slot**, and the median item asks for 3 mods, not 5.
33 of 46 items ask for exactly one prefix (almost always life).

### 8b. Tier distribution


| slot | mods | T1 | T2 | T3 | T4 | T5 | T6 | T7+ | med tier | med tier/ladder | T1-2 share |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 11 | 0 (0%) | 1 (9%) | 2 (18%) | 4 (36%) | 2 (18%) | 1 (9%) | 1 (9%) | 4 | 0.50 | 9% |
| Helmet | 10 | 0 (0%) | 0 (0%) | 6 (60%) | 2 (20%) | 2 (20%) | 0 (0%) | 0 (0%) | 3 | 0.39 | 0% |
| Gloves | 9 | 0 (0%) | 3 (33%) | 2 (22%) | 3 (33%) | 1 (11%) | 0 (0%) | 0 (0%) | 3 | 0.44 | 33% |
| Boots | 13 | 0 (0%) | 6 (46%) | 4 (31%) | 2 (15%) | 1 (8%) | 0 (0%) | 0 (0%) | 3 | 0.33 | 46% |
| Belt | 11 | 0 (0%) | 3 (27%) | 4 (36%) | 1 (9%) | 2 (18%) | 1 (9%) | 0 (0%) | 3 | 0.33 | 27% |
| Amulet | 12 | 0 (0%) | 2 (17%) | 4 (33%) | 2 (17%) | 4 (33%) | 0 (0%) | 0 (0%) | 4 | 0.47 | 17% |
| Ring 1 | 7 | 0 (0%) | 2 (29%) | 2 (29%) | 2 (29%) | 1 (14%) | 0 (0%) | 0 (0%) | 3 | 0.50 | 29% |
| Ring 2 | 9 | 0 (0%) | 3 (33%) | 2 (22%) | 2 (22%) | 2 (22%) | 0 (0%) | 0 (0%) | 3 | 0.50 | 33% |
| Weapon 1 | 13 | 5 (38%) | 1 (8%) | 0 (0%) | 2 (15%) | 5 (38%) | 0 (0%) | 0 (0%) | 4 | 0.62 | 46% |
| Shield/Quiver | 11 | 0 (0%) | 2 (18%) | 3 (27%) | 1 (9%) | 4 (36%) | 1 (9%) | 0 (0%) | 4 | 0.50 | 18% |
| ALL | 106 | 5 (5%) | 23 (22%) | 29 (27%) | 21 (20%) | 24 (23%) | 3 (3%) | 1 (1%) | 3 | 0.48 | 26% |


```
  Body Armour    p25=0.38 p50=0.50 p75=0.58
  Helmet         p25=0.38 p50=0.39 p75=0.50
  Gloves         p25=0.38 p50=0.44 p75=0.50
  Boots          p25=0.33 p50=0.33 p75=0.50
  Belt           p25=0.28 p50=0.33 p75=0.45
  Amulet         p25=0.33 p50=0.47 p75=0.56
  Ring 1         p25=0.45 p50=0.50 p75=0.56
  Ring 2         p25=0.40 p50=0.50 p75=0.62
  Weapon 1       p25=0.50 p50=0.62 p75=0.71
  Shield/Quiver  p25=0.38 p50=0.50 p75=0.52
  ALL            p25=0.33 p50=0.48 p75=0.56
```

### 8c. Spawn-weight share


| slot | items | median P | median -log10 P | min P (rarest) | max P (plainest) | median per-mod share | median -log10 P (ladder) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 5 | 10^-2.9 | 2.88 | 10^-4.3 | 10^-1.1 | 0.069 (1 in 15) | 2.88 |
| Helmet | 4 | 10^-3.7 | 3.68 | 10^-4.1 | 10^-1.1 | 0.056 (1 in 18) | 3.68 |
| Gloves | 4 | 10^-3.2 | 3.22 | 10^-4.2 | 10^-1.4 | 0.043 (1 in 23) | 3.22 |
| Boots | 5 | 10^-3.1 | 3.09 | 10^-4.1 | 10^-2.4 | 0.061 (1 in 16) | 3.09 |
| Belt | 5 | 10^-2.5 | 2.46 | 10^-4.3 | 10^-0.9 | 0.058 (1 in 17) | 2.46 |
| Amulet | 5 | 10^-3.4 | 3.39 | 10^-4.5 | 10^-3.0 | 0.033 (1 in 30) | 3.39 |
| Ring 1 | 4 | 10^-3.1 | 3.11 | 10^-3.3 | 10^-1.2 | 0.033 (1 in 30) | 3.11 |
| Ring 2 | 5 | 10^-3.0 | 3.02 | 10^-3.3 | 10^-1.2 | 0.033 (1 in 30) | 3.02 |
| Weapon 1 | 5 | 10^-3.8 | 3.82 | 10^-5.7 | 10^-3.0 | 0.018 (1 in 57) | 4.78 |
| Shield/Quiver | 4 | 10^-3.9 | 3.85 | 10^-4.3 | 10^-2.1 | 0.053 (1 in 19) | 3.85 |
| ALL | 46 | 10^-3.2 | 3.25 | 10^-5.7 | 10^-0.9 | 0.051 (1 in 20) | 3.31 |
pooled -log10 P: p10=1.23 p50=3.25 p90=4.29


A wishlist item is a 10^-3.2 draw against 10^-6.1 for a real one: **about a thousand times easier
to obtain**, because it asks for three middling mods instead of five.

### 8d. Top mod families per slot


**Body Armour** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| DefencesPercent | 3 | 60% | T3 |
| IncreasedLife | 3 | 60% | T6 |
| ColdResistance | 2 | 40% | T4 |
| (craft) BlockPercent | 1 | 20% | craft |
| (craft) FireAndLightningResistance | 1 | 20% | craft |
| ChaosResistance | 1 | 20% | T4 |
| FireResistance | 1 | 20% | T4 |
| LightningResistance | 1 | 20% | T4 |

**Helmet** (4 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 4 | 100% | T4 |
| LightningResistance | 3 | 75% | T3 |
| (craft) ColdAndLightningResistance | 1 | 25% | craft |
| ChanceToSuppressSpells | 1 | 25% | T3 |
| ColdResistance | 1 | 25% | T3 |
| FireResistance | 1 | 25% | T5 |

**Gloves** (4 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 4 | 100% | T3 |
| FireResistance | 2 | 50% | T4 |
| (craft) AreaDamageAndAreaOfEffect | 1 | 25% | craft |
| (craft) FireAndColdResistance | 1 | 25% | craft |
| ColdResistance | 1 | 25% | T3 |
| IncreasedAttackSpeed | 1 | 25% | T2 |
| LightningResistance | 1 | 25% | T4 |

**Boots** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 5 | 100% | T3 |
| MovementVelocity | 5 | 100% | T2 |
| (craft) ColdAndLightningResistance | 1 | 20% | craft |
| ChanceToSuppressSpells | 1 | 20% | T2 |
| ColdResistance | 1 | 20% | T4 |
| LightningResistance | 1 | 20% | T2 |

**Belt** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 5 | 100% | T4 |
| (craft) ColdAndLightningResistance | 1 | 20% | craft |
| (craft) FireAndLightningResistance | 1 | 20% | craft |
| ColdResistance | 1 | 20% | T3 |
| FireResistance | 1 | 20% | T5 |
| IncreasedEnergyShield | 1 | 20% | T3 |
| IncreasedPhysicalDamageReductionRating | 1 | 20% | T2 |
| IncreasedWeaponElementalDamagePercent | 1 | 20% | T2 |
| Strength | 1 | 20% | T3 |

**Amulet** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 5 | 100% | T4 |
| Dexterity | 2 | 40% | T4 |
| FireResistance | 2 | 40% | T4 |
| (craft) Dexterity | 1 | 20% | craft |
| (craft) FireAndColdResistance | 1 | 20% | craft |
| AllResistances | 1 | 20% | T2 |
| GlobalDamageOverTimeMultiplier | 1 | 20% | T3 |
| LightningResistance | 1 | 20% | T3 |

**Ring 1** (4 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 4 | 100% | T4 |
| (craft) Intelligence | 1 | 25% | craft |
| (craft) LightningAndChaosDamageResistance | 1 | 25% | craft |
| AllAttributes | 1 | 25% | T3 |
| AllResistances | 1 | 25% | T2 |
| ChaosResistance | 1 | 25% | T3 |

**Ring 2** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 5 | 100% | T4 |
| (craft) FireAndColdResistance | 1 | 20% | craft |
| (craft) Intelligence | 1 | 20% | craft |
| (craft) LightningAndChaosDamageResistance | 1 | 20% | craft |
| AllAttributes | 1 | 20% | T3 |
| AllResistances | 1 | 20% | T2 |
| ChaosResistance | 1 | 20% | T3 |
| LightningResistance | 1 | 20% | T5 |

**Weapon 1** (5 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreaseSpecificSocketedGemLevel | 3 | 60% | T1 |
| IncreasedAttackSpeed | 3 | 60% | T4 |
| LocalPhysicalDamagePercent | 2 | 40% | T4 |
| PhysicalDamage | 2 | 40% | T2 |
| (craft) MinionAttackSpeedAndCastSpeed | 1 | 20% | craft |
| DamageOverTimeMultiplier | 1 | 20% | T5 |
| IncreasedCastSpeed | 1 | 20% | T5 |
| WeaponCasterDamagePrefix | 1 | 20% | T5 |

**Shield/Quiver** (4 items)
| family | n | % of items | med tier |
|---|--:|--:|--:|
| IncreasedLife | 4 | 100% | T5 |
| FireResistance | 3 | 75% | T3 |
| ColdResistance | 2 | 50% | T4 |
| IncreasedAttackSpeed | 1 | 25% | T2 |
| IncreasedShieldBlockPercentage | 1 | 25% | T5 |

### 8e. Per build


| build | rare | unique | magic | empty | affixes/rare | mean tier | med tier | ilvl range | med -log10 P |
|---|--:|--:|--:|--:|--:|--:|--:|---|--:|
| gladiator_earthquake | 10 | 0 | 0 | 0 | 3.0 | 3.7 | 4 | 0-0 | 3.7 |
| champion_explosive_arrow | 10 | 0 | 0 | 0 | 2.8 | 3.6 | 4 | 0-0 | 3.7 |
| juggernaut_boneshatter | 8 | 1 | 0 | 1 | 2.6 | 3.4 | 3 | 0-0 | 2.5 |
| elementalist_winter_orb | 10 | 0 | 0 | 0 | 2.9 | 2.9 | 3 | 0-0 | 3.8 |
| occultist_essence_drain | 8 | 2 | 0 | 0 | 1.8 | 4.0 | 4 | 0-0 | 2.7 |
| **all 32** | 46 | 3 | 0 | 1 | 2.7 | 3.5 | 3 | 0-0 | 3.2 |


```
builds with >=1 unique: 2 / 5 | total uniques: 3
by slot: {'Ring 1': 1, 'Helmet': 1, 'Gloves': 1}
  juggernaut_boneshatter   Ring 1: Kaom's Sign
  occultist_essence_drain  Helmet: Honourhome, Gloves: Allelopathy

magic / normal items:
```

### 8f. How many of the wishlist's mods does the build use?


items judged: 38 of 46 | builds whose calc failed: ['juggernaut_boneshatter']
| slot | items | mods | useful | useless | useful/item mean | median | useless/item mean | 0 useful | >=4 useful |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Body Armour | 4 | 11 | 4 (36%) | 7 (64%) | 1.00 | 1 | 1.75 | 25% | 0% |
| Helmet | 3 | 9 | 6 (67%) | 3 (33%) | 2.00 | 2 | 1.00 | 0% | 0% |
| Gloves | 3 | 9 | 6 (67%) | 3 (33%) | 2.00 | 2 | 1.00 | 0% | 0% |
| Boots | 4 | 11 | 8 (73%) | 3 (27%) | 2.00 | 2 | 0.75 | 0% | 0% |
| Belt | 4 | 10 | 5 (50%) | 5 (50%) | 1.25 | 1 | 1.25 | 25% | 0% |
| Amulet | 4 | 11 | 8 (73%) | 3 (27%) | 2.00 | 2 | 0.75 | 0% | 0% |
| Ring 1 | 4 | 9 | 4 (44%) | 5 (56%) | 1.00 | 1 | 1.25 | 25% | 0% |
| Ring 2 | 4 | 9 | 4 (44%) | 5 (56%) | 1.00 | 1 | 1.25 | 25% | 0% |
| Weapon 1 | 4 | 11 | 7 (64%) | 4 (36%) | 1.75 | 2 | 1.00 | 25% | 0% |
| Shield/Quiver | 4 | 11 | 6 (55%) | 5 (45%) | 1.50 | 2 | 1.25 | 0% | 0% |
| ALL | 38 | 101 | 58 (57%) | 43 (43%) | 1.53 | 2 | 1.13 | 13% | 0% |

useful-mods-per-item histogram (all slots): {0: '5 (13%)', 1: '13 (34%)', 2: '15 (39%)', 3: '5 (13%)'}
useless-mods-per-item histogram: {0: '11 (29%)', 1: '15 (39%)', 2: '9 (24%)', 3: '2 (5%)', 4: '1 (3%)'}


#### Families most often useless (Zizaran)


| family | n | useless share |
|---|--:|--:|
| IncreasedAttackSpeed | 4 | 100% |
| IncreasedLife | 32 | 56% |
| FireResistance | 9 | 33% |
| LightningResistance | 7 | 14% |
| ColdResistance | 8 | 0% |
| MovementVelocity | 4 | 0% |

families always useful (n >= 4): ['ColdResistance', 'MovementVelocity']


#### Useful share by tier, affix type and craft (Zizaran)

```
by tier: {'T1': '3/5 = 60%', 'T2': '6/17 = 35%', 'T3': '20/27 = 74%', 'T4': '7/20 = 35%', 'T5': '16/19 = 84%', 'T6': '2/3 = 67%', 'T7+': '0/1 = 0%'}
by affix: {'Suffix': '28/43 = 65%', 'Prefix': '26/49 = 53%'}
bench crafts: 4/9 = 44% useful
```


The hand-written items are cleaner but not clean: 43% of the mods a guide author asks for still do
nothing for the objective, 1.13 dead mods per item against Tuadh's 2.79. The single biggest source
is life above the floor (IncreasedLife, 32 occurrences, 56% of them useless — every wishlist item
asks for life) and resistance beyond 75%. Here the crafts are the *worst* mods on the item (44%
useful, 4 of 9), the opposite of Tuadh's 68%: a guide's craft is a generic dual-resistance or
attribute fix, a real character's craft was picked for the character.

---

## 9. Method

**Items.** Each build's PoB import code is decoded (`junkroan.pob.session.decode_import_code`) and
the active `<ItemSet>` is read; `Swap`, `Abyssal Socket`, `Flask` and `Graft` slots are skipped, so
the slot count per build is 10 (body, helmet, gloves, boots, belt, amulet, 2 rings, weapon, offhand).
`Weapon 2` is reported as `Shield/Quiver` when PoB's base type for it is a shield or a quiver. For
the Zizaran set the item set / tree spec / skill set named in `manifest.json` `early_loadout` are
made active before loading, the build level is set to the loadout's level, and `mainSocketGroup` is
re-pointed at the group holding the manifest's main skill (the author's own pointer indexes the
endgame skill set).

**Mod resolution.** For each base, `PobSession.list_item_mods(base)` gives every prefix/suffix PoB
allows on it with its spawn weight, required level and PoB group; tier = rank of the mod's required
level within its group, T1 = highest, ladder length = number of distinct levels in the group. Each
explicit line is matched against the mods' text templates with the rolled value required inside the
template's range; a mod claims all of its template lines at once (a hybrid is one mod, not two), the
cheapest match wins and ties go to the **lowest** required level, so the tier reported is never more
lucky than the text proves. Families come from `junkroan.pob.mod_families.families_of` (the game's
mod family, not PoB's group), falling back to `pob:<group>`. Bench crafts are resolved with
`audit.crafted_families` / `bench_mod_ids.crafted_text_mods`: all `{crafted}` lines are tried as one
mod first, then one by one.

Four corrections were needed and are all measured:

1. *Straddling values.* A day-1 3.29 item can print a value that sits between two of the pinned
   PoB's tier ranges (a "+75 to Armour / +45 to Evasion Rating" hybrid whose lines fall in T4 and
   T3). Such a line is assigned to the **nearest** tier by relative distance, capped at 0.35 of the
   range's magnitude. 23 of 1322 Tuadh mods (1.7%) are nearest-tier rather than exact; 0 in the
   Zizaran set.
2. *Split hybrids.* Two entries resolving to one PoB group are one roll printed on two lines and
   are merged, keeping the worse tier (1 case).
3. *Prefix/suffix variants.* Several texts exist as both a prefix and a suffix mod (rarity of items
   found, elemental damage percent). The variant is chosen so the item stays inside 3 prefixes and
   3 suffixes (this fixes 8 items); where no assignment does, the item is reported as-is. **11 of
   299 Tuadh items (3.7%)
   cannot be expressed as a legal 3/3 rare by the pinned PoB's explicit table** (nine of them
   weapons with four prefix-only damage mods) — they carry influence/essence/fossil mods the
   explicit pool does not name, or the author typed them. 0 such items in the Zizaran set.
4. *Untagged bench crafts.* A wishlist writes its crafts as plain lines, so any leftover line
   that matches a crafting-bench mod is counted as a craft — but only on an item carrying no
   `{crafted}` line at all, since the game allows one bench craft per item. All 16 Zizaran crafts
   come in this way; in the Tuadh set the rule fires on nothing (the 4 lines that match a craft's
   text all sit on items that already carry a craft, so they stay unresolved as influence/veiled
   mods).

**Unresolved.** 16 distinct Tuadh lines (18 occurrences, 1.2% of 1548 mods) match no mod PoB gives
a positive spawn weight on that base: influence and veiled mods (`16% increased Cooldown Recovery
Rate`, `6% chance to deal Double Damage`, `34% increased Effect of Non-Damaging Ailments`,
`15% chance to gain Arcane Surge when you Kill an Enemy`, `22% increased Damage`), plus weapon and
armour lines PoB weights at 0 for that base. They are counted in the affix totals and in the
usefulness pass, and excluded from the tier and weight-share numbers. **0 unresolved lines in the
Zizaran set.**

```
   3  Regenerate 5.3 Mana per second
   1  35% increased Stun Duration on Enemies
   1  26% increased Rarity of Items found
   1  +32 to Strength and Dexterity
   1  22% increased Damage
   1  +32 to Strength and Intelligence
   1  +18% to Fire Resistance
   1  19% increased Stun Duration on Enemies
   1  38% increased Stun and Block Recovery
   1  29% increased Lightning Damage
   1  16% increased Cooldown Recovery Rate
   1  33% increased Cold Damage
   1  15% chance to gain Arcane Surge when you Kill an Enemy
   1  6% chance to deal Double Damage
   1  {crafted} Adds 3 to 74 Lightning Damage to Spells
   1  34% increased Effect of Non-Damaging Ailments
```

**Item level.** Tuadh items carry their real `Item Level:`; the weight-share pool is capped at it.
Zizaran items carry none, so their pools are uncapped (ilvl 100) — their P values are therefore a
lower bound on how easy those items are.

**Usefulness.** One PobSession, one build at a time. The build is loaded, the rails objective is
built for its main gem with `objective_for` (FullDPS for minion/totem/brand skills — 7 of 32 Tuadh
builds; the main socket group is flagged "include in full DPS" first, and any build whose chosen
stat comes back 0 falls back to the first of FullDPS / CombinedDPS / TotalDotDPS / TotalDPS PoB
fills). For each rare, one `trial_stats(..., mode="fast")` batch holds the untouched item plus one
trial per mod with that mod's lines deleted; the build itself is never modified. A mod is useful if
removing it costs >= 0.5% of the objective's value or increases `objective.violations`. 1565 Tuadh
trials + 101 Zizaran trials, ~7 ms each.

`juggernaut_boneshatter` (Zizaran) does not calculate in the pinned PoB at all — every loadout,
including the author's own default, leaves `mainEnv` nil — so its 8 rares are in the static tables
and out of the usefulness tables (38 of 46 items judged).

**What "useful" does not mean.** It is usefulness *to this objective*: chaos resistance, item
rarity, stun recovery and flask-recovery mods score 0% useful because nothing in the rails asks for
them, and resistance or life above a floor that is already met scores 0 as well. That is the same
verdict the optimizer would give, which is the point of the measurement.

**Reproduce.** `scratchpad/author_rares.py` (resolution) + `scratchpad/rares_full.py` (per set,
one PoB session) + `scratchpad/tables.py <set>`; raw data in `scratchpad/rares_tuadh_329.json` and
`scratchpad/rares_zizaran_329.json`.
