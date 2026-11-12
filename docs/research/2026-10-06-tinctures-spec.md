# Tinctures: ramp rule and item rule, spec (#607 unit 3)
Inputs: `2026-10-06-tinctures-pob-modelling.md` (PoB, file:line), `2026-10-06-tinctures-mana-burn.md` (sources). PoB paths relative to vendor/pob/source/src. Probe numbers below are from one PobSession on 2026-10-06 (throwaway script, not committed).

## Rows 1-2 in one paragraph (details in the two notes)
A Tincture sits in a Flask slot; its mods count while the slot flag `active` is on (CalcSetup.lua:943-946). While active it inflicts Mana Burn every `manaBurn` seconds (base 0.5-0.9 s, Bases/tincture.lua; per item (base + 0.01) / (1 + local TinctureManaBurnRate INC), Item.lua:2404-2411). Stacks never expire while active. Each stack drains 1 % of max Mana per second. It ends at 0 Mana or by hand, then a 6-10 s cooldown. Melee Weapon only; the Warden node Seasoned Hunter (TinctureRangedWeapons, tree.lua:83516-83523) adds Ranged Weapons. PoB: stacks are a manual config count (`multiplierManaBurnStacks`, CalcPerform.lua:902-915), drain = stacks x 1 % of the Mana pool (CalcDefence.lua:1288-1291); nothing derives stacks, uptime or time-to-empty.

## Row 3: the ramp rule
Window W = 2.5 s (the current ramp duration). Notation, all PoB outputs of the build with the Tincture slot active:
- M = `Mana` (max pool), U = `ManaUnreserved` (the Mana actually there at t = 0), C = `ManaPerSecondCost`, R = `ManaRegen` + `ManaRecovery` (= `ManaRegenRecovery` while ManaDegen = 0), I = interval = (base manaBurn + 0.01) / (1 + sum of local reduced-rate mods), from the item (tinctureData.manaBurn).

Stacks: `stacks(t) = floor(t / I)` (first stack after one interval) is the lower bound; `1 + floor(t / I)` (first stack at activation) is the upper bound. The sources do not say which (wiki and PoEDB only say "every I seconds"); the rule uses the upper bound so it can only be too strict.

Drain: `burn(W) = 0.01 x M x S(W)`, S(W) = integral of stacks(t) over 0..W (stack-seconds, exact for the step function). Then
`Mana(W) = U - C x W + R x W - burn(W)`; the rule is `Mana(W) > 0`. Mana falls monotonically when C > R, so checking W is enough; when C <= R the burn still grows with t, so check at t = W as well.

Which part is PoB and which is ours:
| part | source |
|---|---|
| M, U, C, R | PoB outputs (read, 0.07 s `stats`) |
| item interval I | PoB item data (Item.lua:2404-2411, tooltip only); we recompute from the raw item |
| `stacks(t)`, S(W), `Mana(W)` | ours: PoB has no derivation (TinctureManaBurnRate is parsed but not used in the degen path) |
| 1 % per stack per second | PoB (CalcSetup.lua:545, CalcDefence.lua:1288-1291); checked below |
| cooldown, uptime, mana leech and on-hit | not modelled by PoB; leech is not in `ManaRecovery` (0 on smite) |

### Worked example: smite, Prismatic Tincture in Flask 4
The item in both builds: Medicinal Prismatic Tincture of Catalysing, Item Level 76, 101 % increased Elemental Damage with Melee Weapons implicit, 17 % increased effect, 8 % penetration, no reduced-rate mod, so I = 0.70 + 0.01 = 0.71 s. Slot flag off vs on, stacks 0:

| build | Mana M | ManaUnreserved U | C /s | R /s | CombinedDPS off | CombinedDPS on |
|---|---|---|---|---|---|---|
| ours: artifacts/benchmark/20261005-1220-gate-20261005/smite-s4.pob.txt (core seed 4) | 956 | 102 | 63.79 | 16.7 | 489 076 | 646 456 (+32 %) |
| author: tests/fixtures/tuadh_329/smite.pob.txt | 596 | 99 | 53.01 | 10.4 | 398 419 | 518 371 (+30 %) |

Stack-seconds over 2.5 s with I = 0.71: lower = 0.71 x 1 + 0.71 x 2 + 0.37 x 3 = 3.24; upper = 0.71 x 1 + 0.71 x 2 + 0.71 x 3 + 0.37 x 4 = 5.74.

Mana(2.5 s) = U - (C - R) x 2.5 - 0.01 x M x S:
| build | U - (C - R) x 2.5 | burn lower (S 3.24) | Mana(2.5) lower | burn upper (S 5.74) | Mana(2.5) upper | time to 0 with no burn |
|---|---|---|---|---|---|---|
| ours | 102 - 47.09 x 2.5 = -15.7 | 31.0 | -46.7 | 54.9 | -70.6 | 102 / 47.09 = 2.17 s |
| author | 99 - 42.61 x 2.5 = -7.5 | 19.3 | -26.8 | 34.2 | -41.7 | 99 / 42.61 = 2.32 s |

Result (arithmetic, not a strength claim): in both smite builds the unreserved Mana is gone before 2.5 s from the skill cost net of regen alone (2.17 s and 2.32 s), before Mana Burn adds anything. The rule `Mana(2.5) > 0` says NO for both with PoB's C. Mana leech and on-hit are not in C or R; if smite should pass, the rule needs a leech term PoB does not give (open question for the lead, not decided here).

PoB agrees with 1 % per stack (config `multiplierManaBurnStacks`, ManaDegen read):
| build | stacks | ManaDegen read | 0.01 x M x stacks | ManaRegenRecovery read |
|---|---|---|---|---|
| ours | 3 | 28.68 | 28.68 | -11.98 (= 16.7 - 28.68) |
| ours (first probe) | 4 | 38.24 | 38.24 | -21.54 |
| author | 3 | 17.88 | 17.88 | -7.48 |
| author (first probe) | 4 | 23.84 | 23.84 | -13.44 |
Exact match. Two harness facts seen: (a) `set_config` re-applies config and CombinedDPS then differs from the state read before it (ours 646 456 -> 378 085 at stacks 3, Speed 5.04 -> 4.94), so DPS must be read with config untouched between flag off and flag on; ManaDegen is unaffected; (b) ManaDegen reads at stacks > 0 even with the slot off: the degen is the config count alone, the slot flag only applies the Tincture mods.

## Row 4: item rule by loadout
| loadout | useful mods on the Tincture | what is on the item |
|---|---|---|
| day 1 | 0 | the base with its implicit only, no affix; today `optimizer/flask_lines.py:1-8` builds MAGIC candidate lines, so day 1 must not draw affixes |
| T16 | 1 | one affix (a MAGIC item holds one prefix and one suffix, flask_lines.py:9-10), useful by PoB |
| endgame and above | 2 | one prefix + one suffix, both useful (MAGIC limit), or a rare where the loadout's rarity rule allows |

Always under the loadout's ilvl / roll rule (tier ladder via `list_item_mods(base, ilvl=)`; the mod `level` in the file is the ilvl gate). "Useful" is decided by PoB: a mod is useful when the objective rises in a trial with it, never from a hand-written list (principle 1).

Candidate pool, retrieved from Data/ModTincture.lua: 66 entries (18 Prefix, 48 Suffix), 17 groups, weightKey `tincture`. Five examples:
| mod | line | text |
|---|---|---|
| TinctureEffect1 (prefix, level 1) | ModTincture.lua:5 | (11-13)% increased effect |
| TinctureToxicityRate4 (prefix, level 80) | :12 | (24-26)% reduced Mana Burn rate |
| TinctureElementalPenetration5 (suffix, level 85) | :36 | Melee Weapon Damage Penetrates (17-19)% Elemental Resistances |
| TinctureIncreasedAttackSpeed3 (suffix, level 85) | :44 | (25-29)% increased Melee Weapon Attack Speed |
| TinctureManaGainPerTarget1 (suffix, level 45) | :61 | Gain 1 Mana per Enemy Hit with Melee Weapons |

Also: TinctureCriticalStrikeMultiplier5 :41, TinctureDamageOverTimeMultiplier5 :31, TinctureCooldownRecovery4 :16, TinctureEffectFasterToxicity1 :17, TinctureEffectSlowerToxicity3 :22. Two kinds matter: damage mods (DPS) and ramp mods (reduced Mana Burn rate raises I; "Gain 1 Mana per Enemy Hit" lowers C - R). With 1-2 mods the ramp rule and the item search interact: evaluate the rule on each candidate item, then pick by the objective.

## Row 5: drafted sub-issue (not posted; parent #424)
Title: `Tinctures: use one when Mana survives the 2.5 s ramp, items by loadout` (70 characters)

## For the human
- **What:** the optimizer equips a Tincture and turns it on only when the unreserved Mana lasts through the ramp window; the author's PoB gets the same switch.
- **Why:** the owner's word 2026-10-06: a Tincture is a burst button that drains Mana; use it when it fits the 2.5 s ramp.
- **Plan:** compute Mana after 2.5 s from PoB's numbers, switch the slot on only when above 0, roll the item by loadout (0 / 1 / 2 useful mods).
- **Result:** on smite today the rule says NO for both builds (Mana(2.5 s) = -46.7 ours, -26.8 author); see the acceptance table.
- **Undo:** two-way door (one revert).

## For the agent
Kind: search-space rule (D113); proof = rail tests plus the trace counter at the PoB boundary, in minutes; no metric gain claimed.
Rule: (1) a Tincture slot flag is `active` only when `Mana(W) > 0` per the formula above (W = the ramp window constant, today 2.5 s; read it, never retype it), with I from the item raw and M/U/C/R from `stats`; (2) the same switch for the author's PoB (`set_flasks_active` after `equip`, `keep_flask_flags=True`, see flask_probe.py:90-91); (3) the Tincture item: 0 / 1 / 2 useful mods by loadout under the ilvl rule; (4) Warden with Seasoned Hunter needs no special case (PoB copies melee buff mods to ranged, CalcPerform.lua:1882-1891); (5) `multiplierManaBurnStacks` is a check input only, never set on the real build.
Files the researchers named: `src/junkroan/optimizer/flask_lines.py` (:1-8, 25, 77, 94), `optimizer/flask_probe.py:90-91`, `pob/headless_runtime_worker.py:1697-1710, 1752-1761, 3196-3254` (`flask_uptimes_for`, `derive_flask_flags`, `set_flasks_active`), `optimizer/item_bases.py:30`, `optimizer/trace.py:115-116`.

Acceptance table:
| row | what | number | how |
|---|---|---|---|
| 1 | formula | smite-s4 Mana(2.5) = -46.7 (lower stacks), -70.6 (upper); author -26.8 / -41.7 | unit test with PoB's M, U, C, R, I |
| 2 | 1 % check | ManaDegen = 0.01 x Mana x stacks: 28.68 at 3 stacks ours, 17.88 author | PobSession test with `multiplierManaBurnStacks` |
| 3 | trace counter | `evaluated(Tincture active with Mana(2.5) <= 0) = 0`; `generated(Tincture active) > 0` and `evaluated(Tincture active, Mana(2.5) > 0) > 0` on a test build where the rule passes | trace at the PoB boundary |
| 4 | author's PoB | same switch: author smite Flask 4 flag follows the rule (off today) | transcript of `set_flasks_active` calls |
| 5 | item rule | day 1: affix count 0; T16 <= 1; endgame <= 2; every mod `level` <= ilvl | rail test per loadout |
| 6 | smite before/after | CombinedDPS ours 646 456 (flag on, today) vs 489 076 (off under the rule); author 518 371 vs 398 419 | two reads, config unchanged between; stated as the consequence of the rule, not a gain |

Note for the lead (decision, not mine): with PoB's C the rule turns smite's Tincture off in both builds (CombinedDPS -24 % ours, -23 % author), the opposite of "use tinctures". Decide whether leech / on-hit Mana enters R (a derived term), or the window or cost basis changes.

## What PoB does not model, and our duty
| not in PoB | consequence |
|---|---|
| stack derivation (stacks from I, uptime) | config count is manual; we compute stacks(t) from I |
| TinctureManaBurnRate not in the degen path (tooltip only, Item.lua:2406) | reduced-rate mods do not change ManaDegen unless the stack count is changed; we apply them through I |
| uptime, cooldown, time-to-empty | not computed (flask uptime skips Tincture, headless_runtime_worker.py:1702); we compute Mana(W) and, if wanted, uptime = time-to-zero / (time-to-zero + cooldown) |
| mana leech, on-hit mana | not in ManaRecovery here; a leech term is ours and open |
| derived-flag path (#575, :1752-1761) never sets a Tincture flag | the rule owns the Tincture flag |
Principle 4: all of it is derived from PoB's numbers (M, U, C, R, item raw); nothing curated by hand.
