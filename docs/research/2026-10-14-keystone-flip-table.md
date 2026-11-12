# Keystone flip table (#1030)

- date: 2026-10-14
- parent: #1028; this table: #1030 (unit 3, report)
- parse JSON: `artifacts\keystone_flip\parse.json`
- flip JSON spark: `artifacts\keystone_flip\spark.json`
- flip JSON cold_dot: `artifacts\keystone_flip\cold_dot.json`
- flip JSON smite: `artifacts\keystone_flip\smite.json`
- Total wall time: 4.7 min (the recorded run seconds of the flip rows and of each baseline; the parse run is not recorded in its JSON)

## Columns

- `parsed kinds`: the kinds of the keystone's stat lines from PoB's parse (`zero`, `redirect`, `add`, `unparsed`); `-` when the parse JSON has no such keystone.
- `flip`: `add` = the keystone allocated in state 2 by `mutate_nodes(add=...)`; `remove` = the build already held it and state 2 removes it.
- `status`: `ok`, or the status PoB gave with its reason (`pob_refused`, `skill_dead`, `not_flipped`).
- `CombinedDPS, %` ... `objective, %`: change from state 1 to state 2 in percent of the absolute state 1 value; `-` where no percentage exists.
- `collapsed nodes v` / `p`: share of the allocated passive nodes worth something in state 1 (value != 0) that fell by more than half or changed sign in state 2; `v` on the maximized stat, `p` on the priced score; `-` where there is no such reading (`p` None).
- `collapsed lines v` / `p`: the same share over the rare-gear affix lines (`line` marginals of the baseline, lines state 2 no longer holds count as 0).
- `time`: wall time of the row.

## spark

- main skill: Spark; mode: -; objective: maximize CombinedDPS subject to Life >= 4500, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, EffectiveMovementSpeedMod >= 1.2, MoMCastsAfterMaxHit >= 3, ElementalOverloadUptime >= 0.9, RampBudget >= RampStages, FireResist >= FireResistMax, ColdResist >= ColdResistMax, LightningResist >= LightningResistMax, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaOverReserved, ManaCostPool >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaSustainPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifeSustainPerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup+EnergyShieldRechargeForCosts >= 0.85*ESSustainPerSecondCost
- baseline (state 1): CombinedDPS 1053483.5, Life 4053, EnergyShield 317, Mana 884, ManaUnreserved 53, TotalEHP 9263.9, PhysicalMaximumHitTaken 4635, ChaosResist -52; objective (CombinedDPS) 1053483.5
- baseline nodes 99; baseline rare-gear lines 31; keystones 57
- run time: 1.5 min

| keystone | parsed kinds | flip | status | CombinedDPS, % | Life, % | EnergyShield, % | TotalEHP, % | ManaUnreserved, % | objective, % | collapsed nodes v, count | collapsed nodes v, value | collapsed nodes p, count | collapsed nodes p, value | collapsed lines v, count | collapsed lines v, value | collapsed lines p, count | collapsed lines p, value | time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Acrobatics | zero | add | ok | +0.0% | +0.0% | +5.7% | +0.4% | +56.6% | +0.0% | 0.0% | 0.0% | 10.1% | 51.7% | 0.0% | 0.0% | 9.7% | 7.4% | 2.6 s |
| Ancestral Bond | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +0.6% | +0.0% | +5.7% | -100.0% | - | - | - | - | - | - | - | - | 1 s |
| Arrow Dancing | add | add | ok | +0.6% | +3.2% | +0.0% | +3.8% | +0.0% | +0.6% | 0.0% | 0.0% | 27.3% | 13.0% | 0.0% | 0.0% | 41.9% | 74.3% | 1.9 s |
| Arsenal of Vengeance | unparsed | add | ok | +1.5% | +4.2% | +0.0% | +3.9% | +0.0% | +1.5% | 0.0% | 0.0% | 24.2% | 5.4% | 0.0% | 0.0% | 3.2% | 1.2% | 2 s |
| Avatar of Fire | zero, redirect | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.5% | +0.0% | +0.5% | +0.0% | -100.0% | - | - | - | - | - | - | - | - | 0.9 s |
| Bitter Frost | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +0.6% | +0.0% | +5.7% | -100.0% | - | - | - | - | - | - | - | - | 1 s |
| Blood Magic | zero, redirect, add | add | ok | +1.7% | +12.3% | +0.0% | -49.6% | - | +1.7% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.2 s |
| Bloodsoaked Blade | add, unparsed | add | ok | +0.4% | +2.9% | +0.0% | +3.6% | +0.0% | +0.4% | 0.0% | 0.0% | 21.2% | 7.7% | 0.0% | 0.0% | 41.9% | 74.3% | 2 s |
| Call to Arms | zero, add | add | ok | +1.7% | +4.5% | +0.0% | +4.2% | +0.0% | +1.7% | 0.0% | 0.0% | 26.3% | 7.4% | 0.0% | 0.0% | 12.9% | 5.3% | 1.4 s |
| Chaos Inoculation | zero | add | ok | -27.0% | -100.0% | +3.2% | -89.8% | +32.1% | -27.0% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.4 s |
| Conduit | unparsed | add | ok | +2.1% | +0.0% | +30.3% | +2.2% | +18.9% | +2.1% | 0.0% | 0.0% | 24.2% | 16.1% | 0.0% | 0.0% | 9.7% | 7.4% | 1.9 s |
| Crimson Dance | zero, add | add | ok | +1.5% | +4.2% | +0.0% | +3.9% | +0.0% | +1.5% | 0.0% | 0.0% | 24.2% | 5.4% | 0.0% | 0.0% | 3.2% | 1.2% | 1.7 s |
| Disciple of Kitava | add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.7 s |
| Divine Shield | add | add | ok | +0.8% | +1.0% | +0.0% | +1.0% | +0.0% | +0.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.2% | 1.2% | 1.7 s |
| Eldritch Battery | redirect, add, unparsed | add | ok | +0.0% | +0.0% | +1.9% | -7.3% | +18.9% | +0.0% | 0.0% | 0.0% | 28.3% | 49.3% | 0.0% | 0.0% | 3.2% | 2.1% | 2.2 s |
| Elemental Equilibrium | unparsed | add | ok | +0.4% | +2.9% | +0.0% | +3.6% | +0.0% | +0.4% | 0.0% | 0.0% | 21.2% | 7.7% | 0.0% | 0.0% | 41.9% | 74.3% | 1.3 s |
| Elemental Overload | zero, add | remove | ok | -24.9% | +0.0% | +0.0% | +0.0% | +0.0% | -24.9% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.2 s |
| Eternal Youth | redirect, add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.8 s |
| Ghost Dance | add, unparsed | add | ok | +0.0% | +0.0% | +5.0% | -3.5% | +50.9% | +0.0% | 0.0% | 0.0% | 25.3% | 44.3% | 0.0% | 0.0% | 0.0% | 0.0% | 1.6 s |
| Ghost Reaver | zero, add | add | ok | +0.0% | +0.0% | +4.4% | +0.3% | +43.4% | +0.0% | 0.0% | 0.0% | 7.1% | 44.1% | 0.0% | 0.0% | 0.0% | 0.0% | 1.3 s |
| Glancing Blows | add | add | ok | +0.4% | +0.5% | +0.0% | -2.7% | +0.0% | +0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.2% | 1.2% | 1.9 s |
| Hex Master | add | add | ok | -3.3% | +0.0% | +13.6% | +1.0% | +56.6% | -3.3% | 0.0% | 0.0% | 9.1% | 47.9% | 0.0% | 0.0% | 6.5% | 3.7% | 1.5 s |
| Hollow Palm Technique | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Imbalanced Guard | zero, add | add | ok | +1.5% | +4.2% | +0.0% | +8.1% | +0.0% | +1.5% | 0.0% | 0.0% | 30.3% | 15.2% | 0.0% | 0.0% | 29.0% | 13.5% | 2 s |
| Iron Grip | add | add | ok | +0.2% | +2.6% | +0.0% | +2.5% | +0.0% | +0.2% | 0.0% | 0.0% | 18.2% | 0.2% | 0.0% | 0.0% | 3.2% | 1.2% | 1.4 s |
| Iron Reflexes | zero | add | ok | +2.1% | +5.0% | +0.0% | +5.1% | +0.0% | +2.1% | 0.0% | 0.0% | 29.3% | 15.0% | 0.0% | 0.0% | 22.6% | 12.7% | 1.7 s |
| Iron Will | add | remove | ok | -4.4% | +0.0% | +0.0% | +0.0% | +0.0% | -4.4% | 14.3% | 1.2% | 0.0% | 0.0% | 20.0% | 2.3% | 0.0% | 0.0% | 1.6 s |
| Kineticism | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.5 s |
| Lethe Shade | add, unparsed | add | ok | +0.0% | +0.0% | +4.4% | +0.3% | +43.4% | +0.0% | 0.0% | 0.0% | 7.1% | 44.1% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Lone Messenger | zero, add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Magebane | zero, add | add | ok | +0.4% | +2.9% | +0.0% | +6.0% | +0.0% | +0.4% | 0.0% | 0.0% | 21.2% | 7.7% | 0.0% | 0.0% | 41.9% | 74.3% | 1.2 s |
| Mind Over Matter | redirect | add | ok | +0.0% | +0.0% | +0.6% | +1.3% | +5.7% | +0.0% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2.3 s |
| Minion Instability | add | add | ok | +0.0% | +0.0% | +12.6% | +0.9% | +50.9% | +0.0% | 0.0% | 0.0% | 7.1% | 44.1% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Nature's Patience | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.9 s |
| Necromantic Aegis | unparsed | add | ok | +0.0% | +0.0% | +0.6% | +0.0% | +5.7% | +0.0% | 0.0% | 0.0% | 2.0% | 3.1% | 0.0% | 0.0% | 0.0% | 0.0% | 1.3 s |
| Pain Attunement | add | add | ok | +0.0% | +0.0% | +12.6% | +0.9% | +50.9% | +0.0% | 0.0% | 0.0% | 9.1% | 47.9% | 0.0% | 0.0% | 6.5% | 3.7% | 2.4 s |
| Perfect Agony | zero, add | add | ok | +0.0% | +0.0% | +5.7% | +0.4% | +56.6% | +0.0% | 0.0% | 0.0% | 10.1% | 51.7% | 0.0% | 0.0% | 9.7% | 7.4% | 1.3 s |
| Pitfighter | unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Point Blank | add | add | ok | +0.4% | +2.9% | +0.0% | +3.6% | +0.0% | +0.4% | 0.0% | 0.0% | 21.2% | 7.7% | 0.0% | 0.0% | 41.9% | 74.3% | 2 s |
| Precise Technique | zero, add | add | ok | -28.3% | +2.9% | +0.0% | +3.6% | +0.0% | -28.3% | 1.8% | 16.8% | 22.2% | 12.2% | 0.0% | 0.0% | 16.1% | 9.6% | 1.6 s |
| Resolute Technique | zero | add | ok | -28.0% | +1.0% | +0.0% | +1.0% | +0.0% | -28.0% | 1.8% | 16.8% | 1.0% | 4.5% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Roiling Tempest | zero, add | remove | ok | -17.5% | +0.0% | +0.0% | +0.0% | +0.0% | -17.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Runebinder | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.2 s |
| Secrets of Suffering | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.7 s |
| Solipsism | zero, add | add | ok | +0.0% | +0.0% | +9.1% | +0.7% | +13.2% | +0.0% | 0.0% | 0.0% | 21.2% | 8.5% | 0.0% | 0.0% | 0.0% | 0.0% | 1.4 s |
| Supreme Ego | add | add | ok | +8.1% | +0.0% | +30.3% | +2.2% | -615.1% | +8.1% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2.5 s |
| The Agnostic | zero, add | add | ok | +0.0% | +0.0% | -100.0% | -7.3% | +13.2% | +0.0% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.6 s |
| The Impaler | unparsed | add | ok | +1.5% | +4.2% | +0.0% | +3.9% | +0.0% | +1.5% | 0.0% | 0.0% | 24.2% | 5.4% | 0.0% | 0.0% | 3.2% | 1.2% | 1.7 s |
| Unwavering Stance | zero | add | ok | +0.8% | +3.5% | +0.0% | +3.2% | +0.0% | +0.8% | 0.0% | 0.0% | 18.2% | 0.2% | 0.0% | 0.0% | 3.2% | 1.2% | 1.4 s |
| Vaal Pact | zero, add | add | ok | +0.4% | +2.9% | +0.0% | +3.6% | +0.0% | +0.4% | 0.0% | 0.0% | 24.2% | 8.8% | 0.0% | 0.0% | 41.9% | 74.3% | 2.3 s |
| Versatile Combatant | add | add | ok | +2.1% | +5.0% | +0.0% | +4.7% | +0.0% | +2.1% | 0.0% | 0.0% | 26.3% | 7.4% | 0.0% | 0.0% | 12.9% | 5.3% | 1.7 s |
| Veteran's Awareness | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.7 s |
| Voracious Flame | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +0.0% | +0.0% | +0.0% | -100.0% | - | - | - | - | - | - | - | - | 0.9 s |
| Wicked Ward | add, unparsed | add | ok | +0.0% | +0.0% | +1.9% | +0.1% | +18.9% | +0.0% | 0.0% | 0.0% | 3.0% | 8.4% | 0.0% | 0.0% | 0.0% | 0.0% | 3.2 s |
| Wind Dancer | add | add | ok | +0.0% | +0.0% | +5.7% | +11.6% | +56.6% | +0.0% | 0.0% | 0.0% | 34.3% | 59.6% | 0.0% | 0.0% | 19.4% | 11.5% | 2 s |
| Worship the Blightheart | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.1 s |
| Zealot's Oath | add | add | ok | +0.0% | +0.0% | +0.6% | +0.0% | +5.7% | +0.0% | 0.0% | 0.0% | 4.0% | 3.5% | 0.0% | 0.0% | 0.0% | 0.0% | 3.3 s |

## cold_dot

- main skill: Cold Snap; mode: -; objective: maximize CombinedDPS subject to Life >= 4500, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, EffectiveMovementSpeedMod >= 1.2, MoMCastsAfterMaxHit >= 3, ElementalOverloadUptime >= 0.9, RampBudget >= RampStages, FireResist >= FireResistMax, ColdResist >= ColdResistMax, LightningResist >= LightningResistMax, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaOverReserved, ManaCostPool >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaSustainPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifeSustainPerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup+EnergyShieldRechargeForCosts >= 0.85*ESSustainPerSecondCost
- baseline (state 1): CombinedDPS 264639.5, Life 4794, EnergyShield 1136, Mana 1131, ManaUnreserved 282, TotalEHP 17422.2, PhysicalMaximumHitTaken 7274, ChaosResist -18; objective (CombinedDPS) 264639.5
- baseline nodes 104; baseline rare-gear lines 29; keystones 57
- run time: 1.7 min

| keystone | parsed kinds | flip | status | CombinedDPS, % | Life, % | EnergyShield, % | TotalEHP, % | ManaUnreserved, % | objective, % | collapsed nodes v, count | collapsed nodes v, value | collapsed nodes p, count | collapsed nodes p, value | collapsed lines v, count | collapsed lines v, value | collapsed lines p, count | collapsed lines p, value | time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Acrobatics | zero | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.7 s |
| Ancestral Bond | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +2.7% | +0.5% | +3.5% | -100.0% | - | - | - | - | - | - | - | - | 0.8 s |
| Arrow Dancing | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 2.3 s |
| Arsenal of Vengeance | unparsed | add | ok | +0.0% | +2.6% | +3.7% | +2.8% | +4.3% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 1.8 s |
| Avatar of Fire | zero, redirect | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +1.6% | +3.5% | +2.0% | +4.3% | -100.0% | - | - | - | - | - | - | - | - | 0.8 s |
| Bitter Frost | zero, add | remove | ok | -15.9% | +0.0% | +0.0% | +0.0% | +0.0% | -15.9% | 1.6% | 1.2% | 1.5% | 0.9% | 0.0% | 0.0% | 0.0% | 0.0% | 1.7 s |
| Blood Magic | zero, redirect, add | add | ok | -2.8% | +12.3% | +5.4% | -57.1% | - | -2.8% | 7.7% | 2.6% | - | - | 12.5% | 0.8% | - | - | 2 s |
| Bloodsoaked Blade | add, unparsed | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.5 s |
| Call to Arms | zero, add | add | ok | +0.0% | +2.3% | +3.6% | +2.6% | +4.3% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 2.2 s |
| Chaos Inoculation | zero | add | ok | +0.0% | -100.0% | -16.1% | -79.7% | +0.7% | +0.0% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.7 s |
| Conduit | unparsed | add | ok | +0.0% | +0.0% | +1.6% | +0.3% | +2.1% | +0.0% | 1.5% | 0.2% | 7.5% | 27.8% | 12.5% | 0.8% | 11.8% | 5.7% | 1.5 s |
| Crimson Dance | zero, add | add | ok | +0.0% | +0.9% | +0.1% | +0.8% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 17.6% | 9.4% | 2.1 s |
| Disciple of Kitava | add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1 s |
| Divine Shield | add | add | ok | +0.0% | +0.7% | +3.3% | -15.0% | +4.3% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 1.7 s |
| Eldritch Battery | redirect, add, unparsed | add | ok | +0.0% | +0.0% | +0.5% | -19.2% | +0.7% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.3 s |
| Elemental Equilibrium | unparsed | add | ok | +0.0% | +0.2% | +0.0% | +0.2% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 17.6% | 9.4% | 1.6 s |
| Elemental Overload | zero, add | add | ok | +2.8% | +0.0% | +2.1% | +0.4% | +2.8% | +2.8% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 5.9% | 0.1% | 1.4 s |
| Eternal Youth | redirect, add | add | ok | +0.0% | +1.6% | +3.5% | +2.0% | +4.3% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 2.6 s |
| Ghost Dance | add, unparsed | add | ok | +0.0% | +0.0% | +0.5% | -16.6% | +0.7% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.7 s |
| Ghost Reaver | zero, add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Glancing Blows | add | add | ok | +0.0% | +0.9% | +3.4% | -6.3% | +4.3% | +0.0% | 4.6% | 0.5% | 9.0% | 16.0% | 12.5% | 0.8% | 23.5% | 9.5% | 3.7 s |
| Hex Master | add | add | ok | -6.5% | +0.0% | +0.0% | +0.0% | +0.0% | -6.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.2 s |
| Hollow Palm Technique | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.6 s |
| Imbalanced Guard | zero, add | add | ok | +0.0% | +3.0% | +3.8% | +4.1% | +4.3% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 7.3 s |
| Iron Grip | add | add | ok | +0.7% | +0.5% | +1.7% | +4.4% | +2.1% | +0.7% | 3.1% | 0.6% | 9.0% | 28.1% | 12.5% | 0.8% | 41.2% | 43.5% | 3.7 s |
| Iron Reflexes | zero | add | ok | +0.0% | +0.0% | +0.0% | +0.4% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.7 s |
| Iron Will | add | add | ok | +4.8% | +0.5% | +20.0% | +4.2% | +2.8% | +4.8% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 1.9 s |
| Kineticism | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.3 s |
| Lethe Shade | add, unparsed | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.4 s |
| Lone Messenger | zero, add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Magebane | zero, add | add | ok | +0.0% | +0.0% | +1.6% | +5.8% | +2.1% | +0.0% | 1.5% | 0.2% | 7.5% | 27.8% | 12.5% | 0.8% | 11.8% | 5.7% | 1.9 s |
| Mind Over Matter | redirect | add | ok | +0.0% | +0.2% | +1.1% | +5.2% | +1.4% | +0.0% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2.1 s |
| Minion Instability | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.4 s |
| Nature's Patience | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.9 s |
| Necromantic Aegis | unparsed | add | ok | -1.1% | -6.1% | +10.5% | -23.0% | +2.1% | -1.1% | 1.5% | 0.2% | 1.5% | 0.1% | 12.5% | 0.8% | 5.9% | 5.6% | 2 s |
| Pain Attunement | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.4 s |
| Perfect Agony | zero, add | add | ok | -0.1% | +0.0% | +0.0% | +0.0% | +0.0% | -0.1% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.8 s |
| Pitfighter | unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.4 s |
| Point Blank | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.3 s |
| Precise Technique | zero, add | add | ok | -0.1% | +0.0% | +0.0% | +0.0% | +0.0% | -0.1% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.3 s |
| Resolute Technique | zero | add | ok | -0.1% | +1.2% | +3.4% | +1.6% | +4.3% | -0.1% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 17.6% | 3.9% | 2 s |
| Roiling Tempest | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +0.0% | +0.0% | +0.0% | -100.0% | - | - | - | - | - | - | - | - | 1.1 s |
| Runebinder | add | add | ok | +0.0% | +0.2% | +2.2% | +0.6% | +2.8% | +0.0% | 4.6% | 0.5% | 9.0% | 16.0% | 12.5% | 0.8% | 23.5% | 9.5% | 1.5 s |
| Secrets of Suffering | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.6 s |
| Solipsism | zero, add | add | ok | +0.0% | +0.0% | -16.5% | -3.2% | +1.4% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.6 s |
| Supreme Ego | add | add | ok | +4.7% | +0.2% | +0.0% | +0.2% | -120.2% | +4.7% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2.1 s |
| The Agnostic | zero, add | add | ok | +0.0% | +0.0% | -100.0% | -19.2% | +4.3% | +0.0% | 4.6% | 0.5% | - | - | 12.5% | 0.8% | - | - | 1.4 s |
| The Impaler | unparsed | add | ok | +0.0% | +0.9% | +0.1% | +0.8% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 17.6% | 9.4% | 2.1 s |
| Unwavering Stance | zero | add | ok | +0.7% | +1.2% | +1.8% | +5.0% | +2.1% | +0.7% | 3.1% | 0.6% | 9.0% | 28.1% | 12.5% | 0.8% | 52.9% | 82.3% | 1.6 s |
| Vaal Pact | zero, add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.5 s |
| Versatile Combatant | add | add | ok | +0.0% | +0.2% | +0.0% | +0.2% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 17.6% | 9.4% | 2.4 s |
| Veteran's Awareness | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Voracious Flame | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +0.0% | +0.0% | +0.0% | -100.0% | - | - | - | - | - | - | - | - | 0.7 s |
| Wicked Ward | add, unparsed | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Wind Dancer | add | add | ok | +0.0% | +0.0% | +0.0% | +11.1% | +0.0% | +0.0% | 0.0% | 0.0% | 6.0% | 27.7% | 0.0% | 0.0% | 5.9% | 5.6% | 1.6 s |
| Worship the Blightheart | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1.3 s |
| Zealot's Oath | add | add | ok | +0.0% | +0.0% | +2.1% | +0.4% | +2.8% | +0.0% | 4.6% | 0.5% | 4.5% | 0.4% | 12.5% | 0.8% | 5.9% | 0.1% | 1.4 s |

## smite

- main skill: Smite; mode: -; objective: maximize CombinedDPS subject to Life >= 4500, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, EffectiveMovementSpeedMod >= 1.2, MoMCastsAfterMaxHit >= 3, HitChance >= 95, ElementalOverloadUptime >= 0.9, RampBudget >= RampStages, FireResist >= FireResistMax, ColdResist >= ColdResistMax, LightningResist >= LightningResistMax, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaOverReserved, ManaCostPool >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaSustainPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifeSustainPerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup+EnergyShieldRechargeForCosts >= 0.85*ESSustainPerSecondCost
- baseline (state 1): CombinedDPS 322844.7, Life 4062, EnergyShield 233, Mana 930, ManaUnreserved 99, TotalEHP 13517.4, PhysicalMaximumHitTaken 5230, ChaosResist -40; objective (CombinedDPS) 322844.7
- baseline nodes 101; baseline rare-gear lines 33; keystones 57
- run time: 1.6 min

| keystone | parsed kinds | flip | status | CombinedDPS, % | Life, % | EnergyShield, % | TotalEHP, % | ManaUnreserved, % | objective, % | collapsed nodes v, count | collapsed nodes v, value | collapsed nodes p, count | collapsed nodes p, value | collapsed lines v, count | collapsed lines v, value | collapsed lines p, count | collapsed lines p, value | time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Acrobatics | zero | add | ok | +1.1% | +0.0% | +0.0% | +0.3% | +0.0% | +1.1% | 0.0% | 0.0% | 2.9% | 1.1% | 0.0% | 0.0% | 3.7% | 0.4% | 1.9 s |
| Ancestral Bond | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +2.1% | +2.6% | +2.1% | +3.0% | -100.0% | - | - | - | - | - | - | - | - | 0.7 s |
| Arrow Dancing | add | add | ok | +0.5% | +0.0% | +0.0% | +0.5% | +0.0% | +0.5% | 4.1% | 1.5% | 2.9% | 1.1% | 0.0% | 0.0% | 0.0% | 0.0% | 1.8 s |
| Arsenal of Vengeance | unparsed | add | ok | +0.0% | +0.5% | +0.0% | +0.5% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.8 s |
| Avatar of Fire | zero, redirect | add | ok | -12.8% | +0.8% | +0.0% | +0.7% | +0.0% | -12.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2 s |
| Bitter Frost | zero, add | add | skill_dead: CombinedDPS = 0.0 in state 2 | -100.0% | +0.0% | +7.7% | +0.4% | +8.1% | -100.0% | - | - | - | - | - | - | - | - | 0.7 s |
| Blood Magic | zero, redirect, add | add | ok | +0.1% | +11.1% | +0.0% | -94.6% | - | +0.1% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.3 s |
| Bloodsoaked Blade | add, unparsed | add | ok | +0.5% | +0.0% | +0.0% | +0.0% | +0.0% | +0.5% | 4.1% | 1.5% | 2.9% | 1.1% | 0.0% | 0.0% | 0.0% | 0.0% | 2 s |
| Call to Arms | zero, add | add | ok | +0.1% | +0.8% | +0.0% | +0.7% | +0.0% | +0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.9 s |
| Chaos Inoculation | zero | add | ok | +1.6% | -100.0% | +4.3% | -92.4% | +4.0% | +1.6% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 1.4 s |
| Conduit | unparsed | add | ok | +2.8% | +0.0% | +0.0% | +0.0% | +0.0% | +2.8% | 0.0% | 0.0% | 2.9% | 1.1% | 0.0% | 0.0% | 7.4% | 1.6% | 2 s |
| Crimson Dance | zero, add | add | ok | +0.0% | +0.5% | +0.0% | +0.5% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.6 s |
| Disciple of Kitava | add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.7 s |
| Divine Shield | add | add | ok | +0.1% | +1.6% | +0.9% | +1.5% | +1.0% | +0.1% | 0.0% | 0.0% | 2.9% | 5.2% | 0.0% | 0.0% | 3.7% | 2.2% | 1.5 s |
| Eldritch Battery | redirect, add, unparsed | add | ok | +1.6% | +0.0% | +6.0% | -5.4% | +6.1% | +1.6% | 0.0% | 0.0% | 11.4% | 46.8% | 0.0% | 0.0% | 11.1% | 6.7% | 2 s |
| Elemental Equilibrium | unparsed | add | ok | +0.5% | +0.0% | +0.9% | +0.0% | +1.0% | +0.5% | 4.1% | 1.5% | 5.7% | 6.4% | 0.0% | 0.0% | 3.7% | 2.2% | 1.7 s |
| Elemental Overload | zero, add | add | ok | +17.3% | +1.3% | +6.9% | +1.6% | +7.1% | +17.3% | 6.1% | 3.6% | 10.0% | 17.2% | 0.0% | 0.0% | 7.4% | 6.3% | 1.4 s |
| Eternal Youth | redirect, add | add | ok | +0.0% | +0.5% | +0.9% | +0.5% | +1.0% | +0.0% | 0.0% | 0.0% | 2.9% | 5.2% | 0.0% | 0.0% | 3.7% | 2.2% | 2 s |
| Ghost Dance | add, unparsed | add | ok | +1.6% | +0.0% | +1.7% | +0.1% | +2.0% | +1.6% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 1.6 s |
| Ghost Reaver | zero, add | add | ok | +1.6% | +0.0% | +2.6% | +0.1% | +3.0% | +1.6% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 1.5 s |
| Glancing Blows | add | add | ok | +0.1% | +1.3% | +0.9% | -18.5% | +1.0% | +0.1% | 0.0% | 0.0% | 2.9% | 5.2% | 0.0% | 0.0% | 3.7% | 2.2% | 2.2 s |
| Hex Master | add | add | ok | +0.2% | +0.2% | +4.3% | +0.5% | +4.0% | +0.2% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 1.8 s |
| Hollow Palm Technique | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.7 s |
| Imbalanced Guard | zero, add | remove | ok | +0.0% | +0.0% | +0.0% | -3.5% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.3 s |
| Iron Grip | add | add | ok | +0.1% | +0.8% | +0.0% | +0.7% | +0.0% | +0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.2 s |
| Iron Reflexes | zero | add | ok | +0.0% | +0.0% | +0.0% | +2.3% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5 s |
| Iron Will | add | add | ok | +0.1% | +1.3% | +0.9% | +1.3% | +1.0% | +0.1% | 0.0% | 0.0% | 2.9% | 5.2% | 0.0% | 0.0% | 3.7% | 2.2% | 1.4 s |
| Kineticism | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 1 s |
| Lethe Shade | add, unparsed | add | ok | +2.3% | +0.0% | +2.6% | +0.1% | +3.0% | +2.3% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 1.8 s |
| Lone Messenger | zero, add, unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.6 s |
| Magebane | zero, add | add | ok | +1.6% | +0.0% | +0.9% | +4.9% | +1.0% | +1.6% | 0.0% | 0.0% | 5.7% | 6.4% | 0.0% | 0.0% | 7.4% | 2.5% | 1.2 s |
| Mind Over Matter | redirect | add | ok | +6.3% | +12.6% | +12.9% | +16.1% | +4.0% | +6.3% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2 s |
| Minion Instability | add | add | ok | +2.8% | +0.2% | +5.2% | +0.5% | +5.1% | +2.8% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 14.8% | 7.9% | 1.4 s |
| Nature's Patience | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.6 s |
| Necromantic Aegis | unparsed | add | ok | +0.1% | +1.6% | +2.6% | +1.6% | +3.0% | +0.1% | 0.0% | 0.0% | 8.6% | 21.5% | 0.0% | 0.0% | 7.4% | 6.3% | 1.5 s |
| Pain Attunement | add | add | ok | +2.3% | +0.2% | +3.4% | +0.4% | +4.0% | +2.3% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 2.6 s |
| Perfect Agony | zero, add | add | ok | -9.7% | +0.0% | +0.0% | +0.0% | +0.0% | -9.7% | 2.0% | 2.1% | 4.3% | 1.9% | 0.0% | 0.0% | 3.7% | 0.4% | 1.5 s |
| Pitfighter | unparsed | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.6 s |
| Point Blank | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2 s |
| Precise Technique | zero, add | add | ok | -16.5% | +0.0% | +0.0% | +0.0% | +0.0% | -16.5% | 2.0% | 2.1% | 1.4% | 0.8% | 0.0% | 0.0% | 0.0% | 0.0% | 2.1 s |
| Resolute Technique | zero | add | ok | -12.2% | +1.6% | +0.9% | +1.5% | +1.0% | -12.2% | 8.2% | 5.0% | 11.4% | 14.6% | 18.2% | 9.7% | 11.1% | 3.7% | 1.3 s |
| Roiling Tempest | zero, add | add | ok | -53.4% | +0.0% | +8.6% | +0.5% | +9.1% | -53.4% | 0.0% | 0.0% | 5.7% | 15.3% | 18.2% | 17.3% | 14.8% | 7.6% | 1.4 s |
| Runebinder | add | add | ok | +0.6% | +1.3% | +3.4% | +1.4% | +4.0% | +0.6% | 4.1% | 1.5% | 8.6% | 16.4% | 0.0% | 0.0% | 7.4% | 6.3% | 2.2 s |
| Secrets of Suffering | zero, add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.6 s |
| Solipsism | zero, add | add | ok | +6.6% | +0.0% | -12.4% | -0.7% | +2.0% | +6.6% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 14.8% | 7.9% | 1.9 s |
| Supreme Ego | add | add | ok | +11.3% | +0.0% | +0.0% | +0.0% | -335.4% | +11.3% | 0.0% | 0.0% | - | - | 0.0% | 0.0% | - | - | 2 s |
| The Agnostic | zero, add | add | ok | +0.2% | +2.1% | -100.0% | -3.5% | +2.0% | +0.2% | 0.0% | 0.0% | 15.7% | 16.2% | 0.0% | 0.0% | 7.4% | 3.6% | 2.4 s |
| The Impaler | unparsed | add | ok | +0.0% | +0.5% | +0.0% | +0.5% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.1 s |
| Unwavering Stance | zero | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.2 s |
| Vaal Pact | zero, add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 1.4% | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% | 2.4 s |
| Versatile Combatant | add | add | ok | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.6 s |
| Veteran's Awareness | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Voracious Flame | zero, add | add | ok | -40.9% | +0.0% | +9.4% | +0.5% | +9.1% | -40.9% | 22.4% | 0.2% | 5.7% | 15.3% | 18.2% | 10.9% | 11.1% | 7.1% | 2.4 s |
| Wicked Ward | add, unparsed | add | ok | +2.3% | +0.0% | +6.0% | +0.3% | +6.1% | +2.3% | 0.0% | 0.0% | 8.6% | 16.4% | 0.0% | 0.0% | 11.1% | 6.7% | 2.9 s |
| Wind Dancer | add | add | ok | +0.0% | +0.0% | +0.0% | -9.1% | +0.0% | +0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.9 s |
| Worship the Blightheart | add | add | pob_refused: PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] | - | - | - | - | - | - | - | - | - | - | - | - | - | - | 0.8 s |
| Zealot's Oath | add | add | ok | +0.2% | +2.1% | +3.4% | +2.1% | +4.0% | +0.2% | 0.0% | 0.0% | 7.1% | 15.7% | 0.0% | 0.0% | 7.4% | 6.3% | 2.2 s |

## Keystones PoB could not flip on this tree

### spark

| keystone | flip | status | reason |
| --- | --- | --- | --- |
| Ancestral Bond | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Avatar of Fire | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Bitter Frost | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Disciple of Kitava | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] |
| Hollow Palm Technique | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] |
| Kineticism | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] |
| Lone Messenger | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] |
| Nature's Patience | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] |
| Pitfighter | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] |
| Secrets of Suffering | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] |
| Veteran's Awareness | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] |
| Voracious Flame | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Worship the Blightheart | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] |

### cold_dot

| keystone | flip | status | reason |
| --- | --- | --- | --- |
| Ancestral Bond | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Avatar of Fire | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Disciple of Kitava | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] |
| Hollow Palm Technique | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] |
| Kineticism | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] |
| Lone Messenger | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] |
| Nature's Patience | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] |
| Pitfighter | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] |
| Roiling Tempest | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Secrets of Suffering | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] |
| Veteran's Awareness | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] |
| Voracious Flame | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Worship the Blightheart | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] |

### smite

| keystone | flip | status | reason |
| --- | --- | --- | --- |
| Ancestral Bond | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Bitter Frost | add | skill_dead | CombinedDPS = 0.0 in state 2 |
| Disciple of Kitava | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [12953] |
| Hollow Palm Technique | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [60069] |
| Kineticism | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [40561] |
| Lone Messenger | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [3354] |
| Nature's Patience | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [30847] |
| Pitfighter | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [37081] |
| Secrets of Suffering | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [57280] |
| Veteran's Awareness | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: unknown node id(s): [32118] |
| Worship the Blightheart | add | pob_refused | PoBHeadlessHostContractError: mutate_tree_nodes: node id(s) have no path from the allocated tree: [27781] |

