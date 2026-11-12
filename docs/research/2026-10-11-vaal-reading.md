# #802 row 1: plain gem vs Vaal version, PoB reading (2026-10-11)

Reader: `tools/rig802/vaal_reading.py` (rerun: `PYTHONPATH=src python tools/rig802/vaal_reading.py --max 6`, ~2 min, 1 slot). Raw rows: `artifacts/rig802/reading.json`.

Build: core14 reference `spark` prepared as the benchmark prepares its author (`benchmark.prepare_author`), main group kept (`Spark + Inspiration + Spell Echo + Pinpoint + Pierce`), one extra group `Probe` (slot Helmet) holding the one gem under test, every gem level 18 / quality 0. Outputs compared = every key of PoB's `main_output` plus the objective's stat keys. Gems: every `is_vaal_gem` record of the game corpus (`active_gems()`) named "Vaal " + a plain active gem tagged `aura` (corpus rule, name order); first three are the acceptance gems, the other three are extra.

States: (a) plain gem, enableGlobal1 true; (b) Vaal gem, enableGlobal1 true / enableGlobal2 false (the harness default); (c) Vaal gem, both true; (d) extra: Vaal gem, enableGlobal1 false / enableGlobal2 true.

Count of differing outputs:

| gem | a vs b | b vs c | a vs c | c vs d | a vs d |
|---|---|---|---|---|---|
| Vaal Clarity | 11 | 7 | 4 | 4 | 0 |
| Vaal Discipline | 33 | 33 | 0 | 0 | 0 |
| Vaal Grace | 42 | 42 | 34 | 34 | 0 |
| Vaal Haste | 19 | 19 | 15 | 15 | 0 |
| Vaal Rejuvenation Totem | 24 | 6 | 24 | 24 | 0 |
| Vaal Smite | 16 | 0 | 16 | 16 | 0 |

**Row 1 stop condition hit: (a) vs (b) differs for all 6 gems, including the 3 acceptance gems (Vaal Clarity, Vaal Discipline, Vaal Grace).**

## Outputs by name

Value pairs are [first state, second state]; headline outputs only (full lists in the json).

### Vaal Clarity
- a vs b (11): ManaCost, ManaCostRaw, ManaPerSecondCost, ManaPerSecondHasCost, ManaRegen, ManaRegenPercent, ManaRegenRecovery, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent
- b vs c (7): ManaRegen, ManaRegenPercent, ManaRegenRecovery, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent

### Vaal Discipline
- a vs b (33): ColdDotEHP, ColdMaximumHitTaken, ColdTotalHitPool, ColdTotalPool, EHPSurvivalTime, EnergyShield, EnergyShieldLeechInstanceRate, EnergyShieldRecharge, EnergyShieldRecoveryCap, EnergyShieldRegenPercent, FireDotEHP, FireMaximumHitTaken, FireTotalHitPool, FireTotalPool, LightningDotEHP, LightningMaximumHitTaken, LightningTotalHitPool, LightningTotalPool, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MaxEnergyShieldLeechInstance, MaxEnergyShieldLeechRate, NumberOfDamagingHits, NumberOfMitigatedDamagingHits, PhysicalDotEHP, PhysicalMaximumHitTaken, PhysicalTotalHitPool, PhysicalTotalPool, SecondMinimalMaximumHitTaken, TotalEHP, TotalNumberOfHits
- b vs c (33): ColdDotEHP, ColdMaximumHitTaken, ColdTotalHitPool, ColdTotalPool, EHPSurvivalTime, EnergyShield, EnergyShieldLeechInstanceRate, EnergyShieldRecharge, EnergyShieldRecoveryCap, EnergyShieldRegenPercent, FireDotEHP, FireMaximumHitTaken, FireTotalHitPool, FireTotalPool, LightningDotEHP, LightningMaximumHitTaken, LightningTotalHitPool, LightningTotalPool, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MaxEnergyShieldLeechInstance, MaxEnergyShieldLeechRate, NumberOfDamagingHits, NumberOfMitigatedDamagingHits, PhysicalDotEHP, PhysicalMaximumHitTaken, PhysicalTotalHitPool, PhysicalTotalPool, SecondMinimalMaximumHitTaken, TotalEHP, TotalNumberOfHits

### Vaal Grace
- a vs b (42): AverageEvadeChance, AverageNotHitChance, ChaosEnemyDamage, ChaosTakenDamage, ChaosTakenHit, ColdEnemyDamage, ColdTakenDamage, ColdTakenHit, ConfiguredEvadeChance, ConfiguredNotHitChance, EHPSurvivalTime, EnemyCritChance, EnemyCritEffect, EvadeChance, Evasion, FireEnemyDamage, FireTakenDamage, FireTakenHit, LightningEnemyDamage, LightningTakenDamage, LightningTakenHit, LowestOfArmourAndEvasion, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MeleeEvadeChance, MeleeEvasion, MeleeNotHitChance, NumberOfDamagingHits, NumberOfMitigatedDamagingHits, PhysicalEnemyDamage, PhysicalTakenDamage, PhysicalTakenHit, ProjectileEvadeChance, ProjectileEvasion, ProjectileNotHitChance, TotalEHP, TotalNumberOfHits, totalEnemyDamage, totalTakenDamage, totalTakenHit
- b vs c (42): AverageEvadeChance, AverageNotHitChance, ChaosEnemyDamage, ChaosTakenDamage, ChaosTakenHit, ColdEnemyDamage, ColdTakenDamage, ColdTakenHit, ConfiguredEvadeChance, ConfiguredNotHitChance, EHPSurvivalTime, EnemyCritChance, EnemyCritEffect, EvadeChance, Evasion, FireEnemyDamage, FireTakenDamage, FireTakenHit, LightningEnemyDamage, LightningTakenDamage, LightningTakenHit, LowestOfArmourAndEvasion, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MeleeEvadeChance, MeleeEvasion, MeleeNotHitChance, NumberOfDamagingHits, NumberOfMitigatedDamagingHits, PhysicalEnemyDamage, PhysicalTakenDamage, PhysicalTakenHit, ProjectileEvadeChance, ProjectileEvasion, ProjectileNotHitChance, TotalEHP, TotalNumberOfHits, totalEnemyDamage, totalTakenDamage, totalTakenHit

### Vaal Haste
- a vs b (19): CastRate, CombinedAvg, CombinedDPS, EffectiveMovementSpeedMod, FullDPS, IgniteRollAverage, IgniteStackPotential, ManaPerSecondCost, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MovementSpeedMod, Speed, Time, TotalDPS, WithBleedDPS, WithIgniteDPS, WithPoisonDPS
- b vs c (19): CastRate, CombinedAvg, CombinedDPS, EffectiveMovementSpeedMod, FullDPS, IgniteRollAverage, IgniteStackPotential, ManaPerSecondCost, ManaReserved, ManaReservedPercent, ManaUnreserved, ManaUnreservedPercent, MovementSpeedMod, Speed, Time, TotalDPS, WithBleedDPS, WithIgniteDPS, WithPoisonDPS

### Vaal Rejuvenation Totem
- a vs b (24): ChaosMaximumHitTaken, ChaosTotalHitPool, ColdMaximumHitTaken, ColdTotalHitPool, EHPSurvivalTime, EnergyShieldRecovery, EnergyShieldRegenPercent, EnergyShieldRegenRecovery, FireMaximumHitTaken, FireTotalHitPool, LifeRegen, LifeRegenPercent, LifeRegenRecovery, LightningMaximumHitTaken, LightningTotalHitPool, NumberOfDamagingHits, NumberOfMitigatedDamagingHits, PhysicalMaximumHitTaken, PhysicalTotalHitPool, SecondMinimalMaximumHitTaken, TotalEHP, TotalNumberOfHits, TotalVaalRejuvenationTotemLife, VaalRejuvenationTotemAllyDamageMitigation
- b vs c (6): EnergyShieldRecovery, EnergyShieldRegenPercent, EnergyShieldRegenRecovery, LifeRegen, LifeRegenPercent, LifeRegenRecovery

### Vaal Smite
- a vs b (16): AverageBurstDamage, AverageDamage, AverageHit, CombinedAvg, CombinedDPS, FullDPS, LightningCritAverage, LightningHitAverage, LightningMaxBase, LightningMinBase, TotalDPS, TotalMax, TotalMin, WithBleedDPS, WithIgniteDPS, WithPoisonDPS
- b vs c (0): 

## What it means

- The XML round trip carries enableGlobal2: the exported `<Gem ... enableGlobal1="true" enableGlobal2="false">` / `"true"` matches what was set, and PoB's calc moves with it (b vs c nonzero for 5 of 6 gems).
- The flag is not 'the Vaal half'. PoB (`vendor/pob/source/src/Modules/CalcSetup.lua:1652`) takes `enableGlobal<index>` per entry of `gemData.grantedEffectList` (`Data.lua:1078`); for a Vaal gem the list is [grantedEffectId = the Vaal skill, secondaryGrantedEffectId = the plain skill] (`Gems.lua:3504-3510`, Vaal Clarity: `VaalClarity` / `Clarity`). So enableGlobal1 = the Vaal skill's own effect, enableGlobal2 = the plain gem's effect.
- Hence (b) = Vaal skill effect on, plain aura OFF: it differs from (a) by the whole plain aura (e.g. Vaal Clarity ManaReserved 209 -> 0; Vaal Discipline EnergyShield 802 -> 498). (c) = both. For Vaal Discipline (c) equals (a) exactly (0 outputs differ): the Vaal skill adds nothing there; for Vaal Haste, Vaal Grace, Vaal Smite, Vaal Rejuvenation Totem (c) differs from (a) (15, 34, 16, 24 outputs; e.g. Vaal Haste CastRate 6.08 (a) / 6.92 (c); CombinedDPS 139,165 (a) / 158,228 (c)): enableGlobal1 true counts the Vaal skill's effect as always on (c vs d, enableGlobal1 off, equals the same count).
- So the harness default (enableGlobal1 true, enableGlobal2 false) counts the Vaal half and drops the plain half, the reverse of the issue's premise. State (d) (enableGlobal1 false, enableGlobal2 true) is the candidate for 'plain gem only'; compared to (a) directly (column a vs d): 0 outputs differ on 6 of 6 gems (rerun with `a_vs_d` in reading.json). Row 1 pass criterion met: the Vaal half = enableGlobal1 false, enableGlobal2 true equals the plain gem.
