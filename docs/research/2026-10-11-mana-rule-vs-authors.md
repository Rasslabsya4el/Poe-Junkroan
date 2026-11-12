# #794: the mana sustain rule against the authors' own builds

Main head 308ed74 (table: job j-20261011-0120-7462; why: tools/rig794/mana_why.py). Raw rig output, no verdict on the rule.

# #794 mana sustain rule vs the authors

rule: ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85 x ManaPerSecondCost; our config lane and flask handling (flags derived from PoB's flask uptime).

## Row 1: every author

| fixture | main skill | totem | trap | mine | brand | minion | ManaRegenRecovery | ManaLeechGainRate | ManaRecoup | ManaPerSecondCost | ManaUnreserved | ratio | rule |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| absolution_minions | Absolution | no | no | no | no | yes | 89.2 | 0.0 | 0.0 | 110.0 | 100 | 0.811 | FAIL |
| arc_archmage | Arc | no | no | no | no | no | 494.7 | 0.0 | 20.0 | 919.5 | 5666 | 0.560 | FAIL |
| archmage_volatile_dead | Volatile Dead | no | no | no | no | no | 378.1 | - | 10.0 | 441.9 | 4088 | 0.878 | pass |
| bleed_bow | Puncture | no | no | no | no | no | 11.2 | 40.9 | 0.0 | 7.7 | 159 | 6.783 | pass |
| bleed_perforate | Perforate | no | no | no | no | no | 9.5 | 72.8 | 0.0 | 18.8 | 33 | 4.369 | pass |
| burning_arrow_snipe | Burning Arrow | no | no | no | no | no | 51.6 | 0.0 | 0.0 | 13.2 | 145 | 3.903 | pass |
| cold_dot | Cold Snap | no | no | no | no | no | 103.5 | 0.0 | 0.0 | 16.8 | 251 | 6.167 | pass |
| elemental_hit | Elemental Hit | no | no | no | no | no | 17.9 | 122.6 | 0.0 | 133.2 | 102 | 1.055 | pass |
| exsanguinate_mines | Exsanguinate | no | no | yes | no | no | 15.5 | 0.0 | 0.0 | 0.0 | 6 | - | pass |
| hit_penance_brand | Penance Brand | no | no | no | yes | no | 25.7 | 0.0 | 0.0 | 0.0 | 77 | - | pass |
| ignite_penance_brand | Penance Brand | no | no | no | yes | no | 92.3 | 0.0 | 0.0 | 78.4 | 252 | 1.177 | pass |
| impale_ballista | Shrapnel Ballista | yes | no | no | no | no | 20.6 | 0.0 | 0.0 | 119.0 | 186 | 0.173 | FAIL |
| impale_cyclone | Cyclone | no | no | no | no | no | 14.2 | 108.4 | 0.0 | 27.3 | 73 | 4.487 | pass |
| kinetic_bolt_wander | Kinetic Bolt | no | no | no | no | no | 22.3 | 255.2 | 0.0 | 91.4 | 193 | 3.038 | pass |
| kinetic_fusillade | Kinetic Fusillade | no | no | no | no | no | 80.4 | 254.8 | 0.0 | 82.0 | 214 | 4.088 | pass |
| lightning_trap | Lightning Trap | no | yes | yes | no | no | 18.2 | 0.0 | 0.0 | 0.0 | -11 | - | pass |
| physical_dot | Corrupting Fever | no | no | no | no | no | 31.6 | 0.0 | 0.0 | 0.0 | 97 | - | pass |
| poison_spark | Spark | no | no | no | no | no | 20.6 | 0.0 | 0.0 | 0.0 | 48 | - | pass |
| poison_spectral_throw | Spectral Throw | no | no | no | no | no | 9.7 | 120.5 | 0.0 | 103.9 | 138 | 1.253 | pass |
| pyroclast_mine | Pyroclast Mine | no | no | yes | no | no | 24.0 | 0.0 | 0.0 | 22.8 | 19 | 1.051 | pass |
| regular_viper_strike | Viper Strike | no | no | no | no | no | 12.1 | 150.9 | 0.0 | 32.0 | 173 | 5.101 | pass |
| shockwave_cyclone | Cyclone | no | no | no | no | no | 13.7 | 156.4 | 0.0 | 28.0 | 128 | 6.083 | pass |
| smite | Smite | no | no | no | no | no | 10.4 | 178.8 | 0.0 | 53.0 | 99 | 3.569 | pass |
| soulrend_chaos_dot | Soulrend | no | no | no | no | no | 16.0 | 0.0 | 0.0 | 0.0 | 0 | - | pass |
| spark | Spark | no | no | no | no | no | 108.8 | 0.0 | 0.0 | 117.2 | 117 | 0.929 | pass |
| spectral_shield_throw | Spectral Shield Throw | no | no | no | no | no | 21.2 | 76.6 | 0.0 | 35.1 | 147 | 2.785 | pass |
| static_strike | Static Strike | no | no | no | no | no | 11.8 | 38.5 | 0.0 | 31.5 | 96 | 1.597 | pass |
| stormbrand | Storm Brand | no | no | no | yes | no | 30.4 | 0.0 | 0.0 | 0.0 | 82 | - | pass |
| summon_raging_spirits | Summon Raging Spirit | no | no | no | no | yes | 20.2 | 0.0 | 0.0 | 0.0 | 99 | - | pass |
| toxic_rain | Toxic Rain | no | no | no | no | no | 110.6 | 0.0 | 0.0 | 48.1 | 111 | 2.299 | pass |
| vd_spellslinger | Volatile Dead | no | no | no | no | no | 202.7 | 0.0 | 0.0 | 40.1 | 92 | 5.061 | pass |
| winter_orb | Winter Orb | no | no | no | no | no | 79.2 | 0.0 | 0.0 | 60.5 | 111 | 1.310 | pass |
| z325_berserker_ground_slam_autocry | Ground Slam of Earthshaking | no | no | no | no | no | 10.3 | 0.0 | 0.0 | 23.7 | -16 | 0.435 | FAIL |
| z325_champion_explosive_arrow | Explosive Arrow | yes | no | no | no | no | 8.9 | - | 0.0 | 57.2 | 180 | 0.156 | FAIL |
| z325_gladiator_eviscerate_retaliate | Sunder | no | no | no | no | no | 0.0 | 0.0 | 0.0 | 0.0 | - | - | pass |
| z325_gladiator_lacerate | Sunder | no | no | no | no | no | 0.0 | 0.0 | 0.0 | 0.0 | - | - | pass |
| z325_gladiator_spectral_shield_throw | Spectral Shield Throw | no | no | no | no | no | 0.0 | 0.0 | 0.0 | 0.0 | - | - | pass |
| z325_hierophant_ice_nova_archmage | Firestorm | no | no | no | no | no | 672.0 | 0.0 | 10.0 | 547.0 | 4932 | 1.247 | pass |
| z325_slayer_ground_slam | Vaal Ground Slam of Earthshaking | no | no | no | no | no | 7.9 | 0.0 | 0.0 | 103.1 | 286 | 0.077 | FAIL |
| z326_berserker_volcanic_fissure | Earthshatter | no | no | no | no | no | 8.1 | 0.0 | 0.0 | 0.0 | -64 | - | pass |
| z326_chieftain_righteous_fire | Righteous Fire | no | no | no | no | no | 11.0 | 0.0 | 0.0 | 0.0 | 39 | - | pass |
| z326_elementalist_wave_of_conviction | Wave of Conviction | no | no | no | no | no | 53.6 | 0.0 | 0.0 | 0.0 | 18 | - | pass |
| z326_necromancer_zombie_army_early | Raise Zombie | no | no | no | no | yes | 41.4 | 0.0 | 0.0 | 115.2 | 75 | 0.359 | FAIL |
| z326_trickster_blight_of_contagion | Blight of Contagion | no | no | no | no | no | 20.7 | 0.0 | 0.0 | 91.1 | 142 | 0.227 | FAIL |
| z327_assassin_poison_spark | Spark of the Nova | no | no | no | no | no | 9.7 | 0.0 | 0.0 | 0.0 | 59 | - | pass |
| z327_elementalist_lightning_conduit | Lightning Conduit | no | no | no | no | no | 115.5 | 0.0 | 0.0 | 122.2 | 147 | 0.945 | pass |
| z327_gladiator_earthquake | Earthquake | no | no | no | no | no | 0.0 | - | 0.0 | 0.0 | - | - | pass |
| z327_hierophant_storm_burst | Storm Burst | yes | no | no | no | no | 69.0 | 0.0 | 0.0 | 51.0 | 767 | 1.353 | pass |
| z327_juggernaut_boneshatter | Boneshatter of Complex Trauma | no | no | no | no | no | 9.9 | 101.6 | 0.0 | 0.0 | -16 | - | pass |
| z327_necromancer_raise_spectre | Raise Spectre | no | no | no | no | yes | 36.4 | 0.0 | 0.0 | 149.9 | 144 | 0.243 | FAIL |
| z327_slayer_earthshatter | Earthshatter | no | no | no | no | no | 14.9 | 121.4 | 0.0 | 5.2 | 65 | 26.380 | pass |
| z328_hierophant_kinetic_fusillade | Kinetic Fusillade | yes | no | no | no | no | 88.1 | 0.0 | 0.0 | 198.9 | 100 | 0.443 | FAIL |
| z328_hierophant_shock_nova_archmage | Shock Nova | no | no | no | no | no | 1067.7 | 0.0 | 25.0 | 940.2 | 7081 | 1.162 | pass |
| z329_champion_explosive_arrow | Explosive Arrow | yes | no | no | no | no | 8.9 | - | 0.0 | 74.8 | 171 | 0.119 | FAIL |
| z329_elementalist_winter_orb | Winter Orb | no | no | no | no | no | 71.8 | 0.0 | 0.0 | 0.0 | 18 | - | pass |
| z329_gladiator_earthquake | Earthquake | no | no | no | no | no | 0.0 | - | 0.0 | 0.0 | - | - | pass |
| z329_juggernaut_boneshatter | Boneshatter of Complex Trauma | no | no | no | no | no | 9.8 | 100.5 | 0.0 | 0.0 | 55 | - | pass |
| z329_occultist_essence_drain | Essence Drain | no | no | no | no | no | 18.9 | 0.0 | 0.0 | 0.0 | 190 | - | pass |

**failing 11 of 58 read**

## Row 4: failing authors with every Flask slot switched on (set_flasks_active(True), read with keep_flask_flags)

| fixture | flasks (PoB uptime line) | ManaRegenRecovery | ManaLeechGainRate | ManaRecoup | ManaPerSecondCost | ratio | rule |
|---|---|---|---|---|---|---|---|
| absolution_minions | Flask 1: no uptime line; Flask 2: no uptime line; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: no uptime line; Flask 5: no uptime line | 89.2 | 0.0 | 0.0 | 110.0 | 0.811 | FAIL |
| arc_archmage | Flask 1: no uptime line; Flask 2: no uptime line; Flask 3: Flask uptime: 16% average, 14% minimum; Flask 4: no uptime line; Flask 5: no uptime line | 494.7 | 0.0 | 20.0 | 919.5 | 0.560 | FAIL |
| impale_ballista | Flask 1: no uptime line; Flask 2: no uptime line; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: no uptime line | 20.6 | 0.0 | 0.0 | 119.0 | 0.173 | FAIL |
| z325_berserker_ground_slam_autocry | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 115.2 | 0.0 | 0.0 | 23.7 | 4.870 | pass |
| z325_champion_explosive_arrow | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 8.9 | - | 0.0 | 57.2 | 0.156 | FAIL |
| z325_slayer_ground_slam | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 7.9 | 0.0 | 0.0 | 103.1 | 0.077 | FAIL |
| z326_necromancer_zombie_army_early | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 42.8 | 0.0 | 0.0 | 115.2 | 0.372 | FAIL |
| z326_trickster_blight_of_contagion | Flask 1: no uptime line; Flask 2: no uptime line; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 20.7 | 0.0 | 0.0 | 91.1 | 0.227 | FAIL |
| z327_necromancer_raise_spectre | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 36.4 | 0.0 | 0.0 | 149.9 | 0.243 | FAIL |
| z328_hierophant_kinetic_fusillade | Flask 1: Flask uptime: 0% average, 0% minimum; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: no uptime line | 88.1 | 0.0 | 0.0 | 198.9 | 0.443 | FAIL |
| z329_champion_explosive_arrow | Flask 1: no uptime line; Flask 2: Flask uptime: 0% average, 0% minimum; Flask 3: Flask uptime: 0% average, 0% minimum; Flask 4: Flask uptime: 0% average, 0% minimum; Flask 5: Flask uptime: 0% average, 0% minimum | 8.9 | - | 0.0 | 74.8 | 0.119 | FAIL |

**1 of 11 failing fixtures pass with every flask on**: z325_berserker_ground_slam_autocry

## Row 5: the six smoke builds, ours (final, -s4) beside the author

smoke run: 20261004-0020-smoke-14-11

| build | author ManaUnreserved | author ratio | author rule | our ManaUnreserved | our regen+leech+recoup | our ManaPerSecondCost | our ratio | our rule |
|---|---|---|---|---|---|---|---|---|
| cold_dot | 251 | 6.167 | pass | 280 | 62.4 | 25.3 | 2.466 | pass |
| bleed_bow | 159 | 6.783 | pass | 148 | 10.4 | 5.8 | 1.804 | pass |
| summon_raging_spirits | 99 | - | pass | 1094 | 89.9 | 71.6 | 1.255 | pass |
| impale_ballista | 186 | 0.173 | FAIL | 93 | 46.2 | 49.5 | 0.933 | pass |
| stormbrand | 82 | - | pass | 429 | 25.6 | 0.0 | - | pass |
| burning_arrow_snipe | 145 | 3.903 | pass | 65 | 34.0 | 6.2 | 5.522 | pass |


---

# #794 unit 2: why the failing authors fail

ManaPerSecondCost is the MAIN skill's ManaCost x its use rate only (CalcOffence.lua:5796-5830, sum at l.5824; no other skill adds to it). The headless worker does not hand out PoB's breakdown table, so the breakdown lines are rebuilt from PoB's outputs (CalcOffence.lua:5827-5830 format) and the product is checked against PoB's number.

## Row 2: what ManaPerSecondCost is made of

| fixture | skill | ManaCost | rate PoB multiplies by | breakdown lines (PoB format) | product | ManaPerSecondCost (PoB) | ManaRegenRecovery+Leech+Recoup | seconds ManaUnreserved lasts |
|---|---|---|---|---|---|---|---|---|
| absolution_minions | Absolution | 55 (raw 55.98) | 2.00 (attack/cast speed; Repeats 2) | x 2.00 ^8(attack/cast speed); = 110.00 per second | 110.00 | 110 | 89.2 | 4.8 s (ManaUnreserved 100 / net drain 20.8/s) |
| arc_archmage | Arc | 237 (raw 236.54) | 3.88 (attack/cast speed; Repeats 1) | x 3.88 ^8(attack/cast speed); = 919.53 per second | 919.53 | 919.53 | 514.7 | 14.0 s (ManaUnreserved 5666 / net drain 404.8/s) |
| impale_ballista | Shrapnel Ballista | 35 (raw 35.28) | 3.40 (totem placement speed; Repeats 1) | x 3.40 ^8(totem placement speed); = 119.00 per second | 119.00 | 119 | 20.6 | 1.9 s (ManaUnreserved 186 / net drain 98.4/s) |
| z325_berserker_ground_slam_autocry | Ground Slam of Earthshaking | 20 (raw 21.08) | 1.18 (attack/cast speed; Repeats 1) | x 1.18 ^8(attack/cast speed); = 23.66 per second | 23.66 | 23.66 | 10.3 | 0 s (ManaUnreserved -16 is not above 0; net drain 13.4/s) |
| z325_champion_explosive_arrow | Explosive Arrow | 26 (raw 26.36) | 2.20 (totem placement speed; Repeats 1) | x 2.20 ^8(totem placement speed); = 57.20 per second | 57.20 | 57.20 | 8.9 | 3.7 s (ManaUnreserved 180 / net drain 48.3/s) |
| z325_slayer_ground_slam | Vaal Ground Slam of Earthshaking | 60 (raw 60.29) | 1.72 (attack/cast speed; Repeats 1) | x 1.72 ^8(attack/cast speed); = 103.08 per second | 103.08 | 103.08 | 7.9 | 3.0 s (ManaUnreserved 286 / net drain 95.2/s) |
| z326_necromancer_zombie_army_early | Raise Zombie | 72 (raw 72.40) | 1.60 (attack/cast speed; Repeats 1) | x 1.60 ^8(attack/cast speed); = 115.20 per second | 115.20 | 115.20 | 41.4 | 1.0 s (ManaUnreserved 75 / net drain 73.8/s) |
| z326_trickster_blight_of_contagion | Blight of Contagion | 12 (raw 12.53) | 7.59 (attack/cast speed; Repeats 1) | x 7.59 ^8(attack/cast speed); = 91.10 per second | 91.10 | 91.10 | 20.7 | 2.0 s (ManaUnreserved 142 / net drain 70.4/s) |
| z327_necromancer_raise_spectre | Raise Spectre | 108 (raw 108.66) | 1.39 (attack/cast speed; Repeats 2) | x 1.39 ^8(attack/cast speed); = 149.93 per second | 149.93 | 149.93 | 36.4 | 1.3 s (ManaUnreserved 144 / net drain 113.5/s) |
| z328_hierophant_kinetic_fusillade | Kinetic Fusillade | 39 (raw 39.55) | 5.10 (totem placement speed; Repeats 1) | x 5.10 ^8(totem placement speed); = 198.90 per second | 198.90 | 198.90 | 88.1 | 0.9 s (ManaUnreserved 100 / net drain 110.8/s) |
| z329_champion_explosive_arrow | Explosive Arrow | 34 (raw 34.27) | 2.20 (totem placement speed; Repeats 1) | x 2.20 ^8(totem placement speed); = 74.80 per second | 74.80 | 74.80 | 8.9 | 2.6 s (ManaUnreserved 171 / net drain 65.9/s) |

## Row 3: what the author carries that restores mana and the judging does not count

| fixture | PoB outputs | mana flask(s): name, base, PoB uptime | mana lines found (exact PoB text, where) |
|---|---|---|---|
| absolution_minions | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 9.60, LifePerSecondCost 19.20 | nothing found | [Life Cost / paid from Life] "Skills Cost Life instead of 15% of Mana Cost" (passive mastery 43818) |
| arc_archmage | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | Flask 2: Startled Hallowed Hybrid Flask of Interference () uptime: no uptime line; Flask 5: Concentrated Eternal Mana Flask of Insulation () uptime: no uptime line | [Mana Recovery] "10% chance to Recover 10% of Mana when you use a Skill" (passive mastery 63559) |
| impale_ballista | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | nothing found | nothing found |
| z325_berserker_ground_slam_autocry | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 7.27, LifePerSecondCost 8.60 | Flask 5: Enduring Eternal Mana Flask () uptime: Flask uptime: 0% average, 0% minimum | [Life Cost / paid from Life] "Attack Skills Cost Life instead of 10% of Mana Cost" (passive Cannibalistic Rite); [Life Cost / paid from Life] "40% increased Physical Damage with Skills that Cost Life" (passive mastery 12169); [Life Cost / paid from Life] "Skills Cost Life instead of 15% of Mana Cost" (passive mastery 48505) |
| z325_champion_explosive_arrow | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | nothing found | nothing found |
| z325_slayer_ground_slam | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | Flask 1: The Writhing Jar (Hallowed Hybrid Flask) uptime: no uptime line | nothing found |
| z326_necromancer_zombie_army_early | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 12.80, LifePerSecondCost 20.48 | nothing found | [Life Cost / paid from Life] "Skills Cost Life instead of 15% of Mana Cost" (passive mastery 32241) |
| z326_trickster_blight_of_contagion | ManaOnHit 0, ManaOnKill 119, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | Flask 2: Foreboding Eternal Mana Flask of Alleviation () uptime: no uptime line mods: Mana Recovery occurs instantly at the end of Effect | [Mana gained on Hit/Kill/Block/Mana Recovery] "Recover 1% of Mana on Kill for each different type of Mastery you have Allocated" (passive Polymath); [Mana gained on Hit/Kill/Block/Mana Recovery] "Recover 2% of Mana on Kill" (passive Mind Drinker) |
| z327_necromancer_raise_spectre | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | nothing found | nothing found |
| z328_hierophant_kinetic_fusillade | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | nothing found | nothing found |
| z329_champion_explosive_arrow | ManaOnHit 0, ManaOnKill 0, ManaOnBlock 0, ManaRecovery 0, LifeCost 0, LifePerSecondCost 0 | nothing found | nothing found |
