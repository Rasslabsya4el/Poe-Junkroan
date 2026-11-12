# Day-1 red lines (#1119, unit 4)

A red line is a line on a day-1 item, unique, flask or passive node that PoB reads only in part, or not at all. In this report a line is red when its outcome is `partial` (PoB reads part of it) or `none` (PoB reads none of it); `full` lines are read whole. 1165 of 9873 day-1 lines are red (199 partial, 966 none), so the tables below show where PoB stops understanding what the day-1 rails allow.

## (a) Surface x outcome

| surface | full | partial | none | missing | total |
| --- | ---: | ---: | ---: | ---: | ---: |
| notable | 1616 | 19 | 119 | 0 | 1754 |
| mastery | 1543 | 83 | 389 | 0 | 2015 |
| ascendancy | 878 | 25 | 161 | 0 | 1064 |
| keystone | 10 | 18 | 29 | 0 | 57 |
| unique | 1479 | 37 | 135 | 0 | 1651 |
| unique_jewel | 0 | 0 | 0 | 0 | 0 |
| gear_affix | 2969 | 5 | 110 | 0 | 3084 |
| flask | 213 | 12 | 23 | 0 | 248 |
| total | 8708 | 199 | 966 | 0 | 9873 |

## (b) Group x surface (line counts)

| group | notable | mastery | ascendancy | keystone | unique | unique_jewel | gear_affix | flask | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| item_text | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| cannot_immune | 16 | 163 | 48 | 21 | 34 | 0 | 10 | 2 | 294 |
| minion | 107 | 100 | 89 | 3 | 91 | 0 | 120 | 4 | 514 |
| jewel_conditional | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| trigger | 17 | 79 | 17 | 1 | 32 | 0 | 13 | 4 | 163 |
| on_kill | 40 | 52 | 18 | 0 | 43 | 0 | 93 | 0 | 246 |
| reflect | 1 | 32 | 1 | 0 | 16 | 0 | 5 | 0 | 55 |
| steal | 1 | 4 | 0 | 0 | 3 | 0 | 0 | 0 | 8 |
| self_cost | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 4 | 7 |
| conversion | 1 | 22 | 12 | 2 | 12 | 0 | 29 | 0 | 78 |
| recovery | 159 | 205 | 77 | 4 | 115 | 0 | 212 | 82 | 854 |
| charges | 67 | 101 | 89 | 1 | 45 | 0 | 61 | 18 | 382 |
| buff | 43 | 61 | 28 | 1 | 22 | 0 | 29 | 0 | 184 |
| defence | 205 | 205 | 117 | 9 | 225 | 0 | 458 | 8 | 1227 |
| on_hit | 76 | 140 | 53 | 1 | 54 | 0 | 94 | 0 | 418 |
| ground | 5 | 0 | 7 | 1 | 9 | 0 | 1 | 0 | 23 |
| ailment | 205 | 227 | 58 | 4 | 85 | 0 | 220 | 74 | 873 |
| flask | 11 | 0 | 17 | 0 | 6 | 0 | 26 | 0 | 60 |
| skill_specific | 319 | 322 | 181 | 6 | 263 | 0 | 705 | 4 | 1800 |
| plain_stat | 461 | 207 | 199 | 2 | 483 | 0 | 821 | 39 | 2212 |
| other | 20 | 95 | 51 | 0 | 112 | 0 | 187 | 9 | 474 |
| total | 1754 | 2015 | 1064 | 57 | 1651 | 0 | 3084 | 248 | 9873 |

## (c) Per group

| group | lines | by surface | distinct sources (node id / unique name / mod id) | red | partial share (partial / all lines of the group) | partial of red (partial / red lines) | examples |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| item_text | 1 | unique 1 | 1 | 1 | 0.0% | 0.0% | [none] Maximum Quality is 200% |
| cannot_immune | 294 | notable 16, mastery 163, ascendancy 48, keystone 21, unique 34, gear_affix 10, flask 2 | 225 | 132 | 4.4% | 9.8% | [partial] 25% more Damage with Hits against Enemies that cannot have Life Leeched from them; [partial] 25% more Maximum Lightning Damage 50% less Minimum Lightning Damage Cannot deal non-Lightning Damage; [none] Attack Projectiles always inflict Bleeding and Maim, and Knock Back Enemies Projectiles cannot Pierce, Fork or Chain |
| minion | 514 | notable 107, mastery 100, ascendancy 89, keystone 3, unique 91, gear_affix 120, flask 4 | 263 | 81 | 2.7% | 17.3% | [partial] -1 to maximum number of Summoned Totems You can have an additional Brand Attached to an Enemy; [partial] 1% of Damage Dealt by your Minions is Leeched to you as Life; [partial] 1% of Physical Attack Damage dealt by your Totems is Leeched to you as Life |
| jewel_conditional | 0 | - | 0 | 0 | - | - | - |
| trigger | 163 | notable 17, mastery 79, ascendancy 17, keystone 1, unique 32, gear_affix 13, flask 4 | 104 | 137 | 16.0% | 19.0% | [none] 10% Chance for Traps to Trigger an additional time; [none] 10% chance to Blind nearby Enemies when you use an Elemental Skill; [partial] 10% chance to Recover 10% of Mana when you use a Skill |
| on_kill | 246 | notable 40, mastery 52, ascendancy 18, unique 43, gear_affix 93 | 225 | 61 | 4.1% | 16.4% | [partial] +3 seconds to Duration of Frenzy and Power Charges on Culling Strike; [none] 10% chance to create Consecrated Ground on Melee Kill, lasting 4 seconds; [none] 10% chance to create a Smoke Cloud on Kill |
| reflect | 55 | notable 1, mastery 32, ascendancy 1, unique 16, gear_affix 5 | 39 | 54 | 10.9% | 11.1% | [partial] 10% of Damage you Reflect to Enemies when Hit is leeched as Life; [partial] 20% chance on Hit to remove all Impales from Enemy Impales removed this way multiply their Reflected Damage for this Hit by the number of Hits they have left; [none] Blind you inflict is Reflected to you |
| steal | 8 | notable 1, mastery 4, unique 3 | 7 | 8 | 0.0% | 0.0% | [none] 10% chance to Steal Power, Frenzy, and Endurance Charges on Hit; [none] 25% chance to Steal Power, Frenzy, and Endurance Charges on Hit; [none] 25% chance to Steal Power, Frenzy, and Endurance Charges on Hit with Claws |
| self_cost | 7 | ascendancy 2, keystone 1, flask 4 | 6 | 6 | 57.1% | 66.7% | [partial] Removes 10% of Life Recovered from Mana when used; [none] Removes all Energy Shield While not on Full Life, Sacrifice 20% of Mana per Second to Recover that much Life; [none] You have Sacrifice of Blood if at least 8 Corrupted Items are Equipped |
| conversion | 78 | notable 1, mastery 22, ascendancy 12, keystone 2, unique 12, gear_affix 29 | 69 | 1 | 1.3% | 100.0% | [partial] 50% of Physical, Cold and Lightning Damage Converted to Fire Damage Deal no Non-Fire Damage; [full] 10% of Physical Damage Converted to Chaos Damage; [full] 10% of Physical Damage from Hits taken as Chaos Damage |
| recovery | 854 | notable 159, mastery 205, ascendancy 77, keystone 4, unique 115, gear_affix 212, flask 82 | 615 | 82 | 2.7% | 28.0% | [partial] 1.5% of Physical Damage prevented from Hits in the past 10 seconds is Regenerated as Life per second; [partial] 10% chance for Energy Shield Recharge to start when you Link to a target; [partial] 10% of Damage taken from Stunning Hits is Recovered as Life |
| charges | 382 | notable 67, mastery 101, ascendancy 89, keystone 1, unique 45, gear_affix 61, flask 18 | 266 | 102 | 1.3% | 4.9% | [none] +3 to Maximum Fanatic Charges; [none] 10% chance to gain a Frenzy Charge when you Hit your Marked Enemy; [none] 10% chance to gain a Power Charge on Critical Strike |
| buff | 184 | notable 43, mastery 61, ascendancy 28, keystone 1, unique 22, gear_affix 29 | 132 | 27 | 1.6% | 11.1% | [partial] +10% to all Elemental Resistances and maximum Elemental Resistances while affected by a Non-Vaal Guard Skill 20% additional Physical Damage Reduction while affected by a Non-Vaal Guard Skill 20% more Damage taken if a Non-Vaal Guard Buff was lost Recently; [partial] 20% increased Buff Effect of your Links for which 50% of Link Duration has Expired; [none] Auras from your Skills grant 2% increased Attack and Cast Speed to you and Allies |
| defence | 1227 | notable 205, mastery 205, ascendancy 117, keystone 9, unique 225, gear_affix 458, flask 8 | 968 | 37 | 2.3% | 75.7% | [partial] +3% Chance to Block Attack Damage if there are at least 5 nearby Enemies; [partial] +5% Chance to Block Attack Damage if there are at least 5 nearby Enemies; [partial] -10% to maximum Chance to Block Attack Damage -10% to maximum Chance to Block Spell Damage +2% Chance to Block Spell Damage for each 1% Overcapped Chance to Block Attack Damage |
| on_hit | 418 | notable 76, mastery 140, ascendancy 53, keystone 1, unique 54, gear_affix 94 | 340 | 130 | 2.9% | 9.2% | [none] 10% Global chance to Blind Enemies on hit; [none] 10% chance to Aggravate Bleeding on targets you Hit with Attacks; [none] 10% chance to Blind Enemies on Hit |
| ground | 23 | notable 5, ascendancy 7, keystone 1, unique 9, gear_affix 1 | 15 | 7 | 8.7% | 28.6% | [none] 15% chance to create Chilled Ground when you Freeze an Enemy; [partial] 40% increased Effect of Chilled Ground; [none] Consecrated Ground you create also grants 50% reduced duration of Damaging Ailments on you |
| ailment | 873 | notable 205, mastery 227, ascendancy 58, keystone 4, unique 85, gear_affix 220, flask 74 | 650 | 98 | 2.5% | 22.4% | [partial] 100% chance to Avoid being Chilled or Frozen if you have used a Fire Skill Recently; [partial] 100% increased Blind duration; [partial] 100% increased Duration of Curses on you |
| flask | 60 | notable 11, ascendancy 17, unique 6, gear_affix 26 | 53 | 4 | 5.0% | 75.0% | [partial] Gain 20% of Physical Damage as Extra Cold Damage if you've used a Sapphire Flask Recently; [partial] Gain 20% of Physical Damage as Extra Fire Damage if you've used a Ruby Flask Recently; [partial] Gain 20% of Physical Damage as Extra Lightning Damage if you've used a Topaz Flask Recently |
| skill_specific | 1800 | notable 319, mastery 322, ascendancy 181, keystone 6, unique 263, gear_affix 705, flask 4 | 1365 | 53 | 0.7% | 22.6% | [partial] +4% to Critical Strike Multiplier for each Mine Detonated Recently, up to 40%; [partial] 10% increased Critical Strike Chance for each Mine Detonated Recently, up to 100%; [partial] 100% increased Cost Efficiency of Retaliation Skills |
| plain_stat | 2212 | notable 461, mastery 207, ascendancy 199, keystone 2, unique 483, gear_affix 821, flask 39 | 1664 | 71 | 0.5% | 16.9% | [partial] 1% increased Fishing Line Strength; [none] 10% chance to Cause Monsters to Flee; [partial] 10% increased Effect of Arcane Surge on you per 200 Mana spent Recently, up to 50% |
| other | 474 | notable 20, mastery 95, ascendancy 51, unique 112, gear_affix 187, flask 9 | 393 | 73 | 0.6% | 4.1% | [none] Call of Steel has +4 to maximum Steel Shards; [none] Can Allocate Passives from the Duelist's starting point; [none] Can Allocate Passives from the Marauder's starting point |

## Notes

- Distinct sources can be fewer than lines in a group: one line text sits on several sources (node ids, unique names, mod ids), and 4025 of the 9873 rows repeat a text another row already has (5848 distinct texts in all).
- jewel_conditional: 0 lines. Its lines are jewel lines (a radius or a socketed jewel), which only the unique_jewel surface would carry; that surface is empty, so the group is empty too.
- unique_jewel: 0 rows. Only a unique jewel whose entry in the owner's form (`docs/rulebook/2026-09-19-unique-jewels.json`) has the `day1` loadout reaches this surface, and the form has none yet (rails, not the reader).

## (d) How to regenerate

Script `scripts/day1_red_lines_report.py` (file reads only, no PoB session). Command, from the repo root: `python scripts/day1_red_lines_report.py`; it writes this file.
