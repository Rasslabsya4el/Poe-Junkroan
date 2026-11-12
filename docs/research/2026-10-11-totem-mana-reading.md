# #808 row 1: the totem numbers read before any rule change

Base 85233cf9 (no optimizer change since the #794 table at 308ed746). Reader: `tools/rig808/totem_reading.py` (the authors prepared as `tools/rig794/mana_table.py` prepares them; ours = `impale_ballista-s4.pob.txt` of smoke run `20261004-0020-smoke-14-11`). Raw: `artifacts/rig808/reading.json`.
Rule read: new cost = `ManaCost x TotemsSummoned / TotemDuration`; pass = `ManaRegenRecovery + ManaLeechGainRate + ManaRecoup >= 0.85 x cost`. No other per-second source: on all 6 builds `ManaPerSecondCost == ManaCost x TotemPlacementSpeed` exactly (119.0, 57.2, 74.8, 198.9, 51.0, 49.5), `Cooldown` null, `Repeats` 1.

| build | ManaCost | TotemsSummoned | ActiveTotemLimit | TotemDuration (s) | new cost /s | old ManaPerSecondCost | regen+leech+recoup | old ratio | new ratio | rule (0.85) |
|---|---|---|---|---|---|---|---|---|---|---|
| impale_ballista (author) | 35 | 6 | 6 | 8.019 | 26.19 | 119.0 | 20.6 | 0.173 | 0.787 | FAIL (needs 22.26) |
| z325_champion_explosive_arrow | 26 | 5 | 5 | 12.012 | 10.82 | 57.2 | 8.9 | 0.156 | 0.822 | FAIL (needs 9.20) |
| z329_champion_explosive_arrow | 34 | 5 | 5 | 12.012 | 14.15 | 74.8 | 8.9 | 0.119 | 0.629 | FAIL (needs 12.03) |
| z328_hierophant_kinetic_fusillade | 39 | 5 | 5 | 20.031 | 9.73 | 198.9 | 88.1 | 0.443 | 9.05 | pass |
| z327_hierophant_storm_burst (5th totem author, today pass) | 12 | 3 | 3 | 20.031 | 1.80 | 51.0 | 69.0 | 1.353 | 38.39 | pass |
| ours impale_ballista (smoke final) | 15 | 4 | 4 | 8.019 | 7.48 | 49.5 | 46.2 (36.2 regen + 10.0 recoup) | 0.933 | 6.175 | pass |

Also read on ours: `ManaUnreserved` 93, `Mana` 1118, `LifeCost` 7.2 (LifePerSecondCost 23.76), `CombinedDPS` 32604. Author impale_ballista: `ManaUnreserved` 186, `Mana` 769, `CombinedDPS` 71172.

Findings against the issue text:
1. Under the rule as written 1 of the 4 failing totem authors passes (z328_hierophant_kinetic_fusillade); 3 still fail (0.787, 0.822, 0.629), against "the 4 totem authors pass".
2. The table of #794 holds 5 totem authors, not 4: `z327_hierophant_storm_burst` (totem yes, ratio 1.353 today) is in the "other 54 of 58"; its ratio changes to 38.393 under the rule, so "54 of 54 equal to 3 decimals" cannot hold (53 of 54 can: every non-totem row).
