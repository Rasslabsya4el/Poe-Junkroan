# Path of Exile 1 mechanics research (3.26-3.29)

> NOTE (2026-09-18 18:10): this report predates the Reddit-capable route and the verbatim-quote rule; PoEDB tooltips only, its numbers are arithmetic, not sources. Kept for the record; do not cite it.

Read date for every URL below: 2026-09-18. `poewiki.net` was attempted first for the relevant pages, but its JavaScript proof-of-work page prevented fetching; readable PoEDB pages are therefore the primary retrieved source. Claims marked **not found** are intentionally not filled from memory.

## 1. Volatile Dead, Spell Cascade, and Spellslinger

Volatile Dead consumes up to three corpses per affected area, while regular Spell Cascade creates the original area plus one in front and one behind: three VD areas, not five. With an available 5-corpse Desecrate pool and ordinary spatial overlap, that makes six orbs a defensible guaranteed model and 6-8 a plausible practical range when the cascade areas include more corpses; 9 requires three corpses in each of all three areas and is not guaranteed by one five-corpse Desecrate. I found no sourced guide evidence establishing the requested “average 7” or an authoritative PoB convention; the repository's existing intake note records authors entering 8 and 6, but that is not a web source and is not treated as game fact. Spellslinger triggers all linked spells simultaneously after a non-triggered wand projectile, so Desecrate and VD compete in the same trigger event; it does not establish corpses before VD resolves, making a self-contained two-spell setup unsuitable for a guaranteed six-orb model without pre-existing corpses or a separate corpse source.

Numbers/formula: `orbs = min(3, corpses in each VD area)` summed over the three regular-Cascade areas; with only five newly-created corpses, guaranteed total is source/placement dependent, not `3 x 3`. Model regular self-cast as 6 conservative / 7 expected only after a measured in-game corpus test; model same-trigger Spellslinger VD as 0 new-corpse contribution unless the engine order is measured, then add pre-existing corpses only. **Confidence: medium** for gem mechanics, **low** for the practical averages and guide convention.

Sources: https://poedb.tw/us/Volatile_Dead ; https://poedb.tw/us/Spell_Cascade_Support ; https://poedb.tw/us/Spellslinger

## 2. Ignite and burning

Yes. Ignite is fire damage over time and is a burning effect, so an enemy affected only by ignite is a burning enemy for conditions such as Immolate's “against Burning Enemies” and “damage against Burning Enemies.” Burning Damage Support scales burning damage from a supported skill; it does not turn a non-burning hit into burning damage, but it does scale an ignite caused by that supported hit. This distinction matters: “against burning enemies” improves the qualifying hit, while “burning damage” improves the ignite/other burning DoT itself.

Numbers/formula: normal ignite duration is 4 seconds in the displayed game data; damage modifiers apply according to their wording, not merely because the source hit was fire. **Confidence: high.**

Sources: https://poedb.tw/us/Burning ; https://poedb.tw/us/Elemental_Overload

## 3. Shock

For a non-critical lightning hit that can shock, the standard ailment formula is `shock magnitude = 0.5 x (damage / ailment threshold)^0.4`, then scaled by modifiers to effect and clamped by the minimum and maximum shock rules. Ordinary damaging shocks below the minimum do not apply; the normal minimum is 5% and the normal maximum is 50%, before explicit changes to minimum/maximum effect. A later shock replaces the current shock only if it has greater magnitude; shocks do not add or “ramp,” and each application has its own duration.

Numbers/formula: use `min(maxShock, effectMultiplier x 0.5 x (lightningHit / threshold)^0.4)` and reject a result below the applicable minimum. The commonly documented pinnacle / Uber thresholds are 25,000,000 / 70,000,000 respectively, but I could not retrieve a current primary page that exposes those figures, so treat them as **low-confidence pending an in-game/PoB corpus confirmation**. For a 25m threshold, a 1m qualifying hit gives `0.5 x (0.04)^0.4 = 13.8%` before effect modifiers; solve the same formula from PoB `AverageHit`/the relevant lightning hit, not total DPS. PoB exposes “Effect of Shock” as a configuration assumption; it does not simulate a hit sequence to derive boss shock automatically, so set it only from this calculation or a forced-shock source. **Confidence: medium** for formula/replacement, **low** for thresholds and the precise current PoB UI behavior.

Sources: https://poedb.tw/us/Shock ; https://www.poewiki.net/wiki/Shock (attempted; fetch blocked by proof-of-work) ; https://github.com/PathOfBuildingCommunity/PathOfBuilding/issues (no single current issue documenting the requested threshold was found)

## 4. Mines, mine-thrown traps, and proxy attribution

Mines reserve a base amount equal to the supported skill's base mana/life cost when placed, then release that reservation when they detonate, expire, or are removed. Blastchain and High-Impact Mine both explicitly set that reservation rule, have a five-second mine lifetime, and a 0.25-second base detonation time; Pyroclast Mine itself displays 4-6 mana reservation by gem level. Thus N placed mines require at least `N x reservation per mine` unreserved mana (or life where applicable), plus the ability to pay the next throw; the correct N is build-specific rather than a fixed optimizer constant.

Lightning Trap plus a mine support is mechanically legal because mine supports accept mineable spells and bow/wand attacks, and Trap is mineable; gameplay is two-stage proxy use: throw mine, detonate mine, mine deploys/uses the trap, then an enemy triggers the trap. The retrieved sources establish legality but I found no credible source showing it as a current mainstream archetype, so “who uses it” is **not found**. Attribution is wording-specific: proxy hits normally belong to the player for damage, ailments, kills, and leech from the supported skill, but effects explicitly requiring “you use/hit/kill” often exclude proxies; for example Ice Bite and Innervate explicitly require a skill “you use ... yourself” and exclude totems/traps/mines, while Arcane Surge explicitly excludes skills used by totems/traps/mines. Do not apply any generic player on-hit/on-kill/charge rule without parsing its wording; sources establish exceptions, not a universal table.

Numbers/formula: `available resource after N mines = unreserved resource - N x base reservation`; reserve N as a build configuration/skill-cap input, not a hard-coded “typical” value. **Confidence: high** for reservation and explicit exclusions, **medium** for the general attribution rule, **low** for popularity/typical N.

Sources: https://poedb.tw/us/Blastchain_Mine_Support ; https://poedb.tw/us/High-Impact_Mine_Support ; https://poedb.tw/us/Pyroclast_Mine ; https://poedb.tw/us/Mine

## 5. Imbalanced Guard

Current text is “100% chance to Defend with 200% of Armour” and “Maximum Damage Reduction for any Damage Type is 50%.” It doubles armour only for the armour mitigation calculation and caps damage reduction, not resistance or “less/reduced damage taken”; without Transcendence/Doryani's Prototype this is principally a physical-hit decision. With armour `A` and raw physical hit `H`, normal armour DR is `A/(A+5H)`; Imbalanced Guard is `min(50%, 2A/(2A+5H))`.

It is strictly better while normal DR is below 50%, equal at normal 50%, and worse above 50% because it caps at 50%; the crossover is `A = 5H`. The practical consensus implied by that math is take it for modest armour versus the hit sizes you are optimizing, and reject it for already high-armour characters or where another physical reduction source frequently exceeds 50%; no sourced community-poll consensus was found. **Confidence: high** for text/formula, **medium** for practical recommendation.

Sources: https://poedb.tw/us/Imbalanced_Guard ; https://www.poewiki.net/wiki/Armour (attempted; fetch blocked by proof-of-work)

## 6. Clever Construction

The question's stated historical behavior is no longer current. Current PoEDB data gives Clever Construction exactly “10% Chance for Traps to Trigger an additional time,” and no trap/mine immunity text; therefore there is no current immunity clause for PoB to render red. If the pinned PoB shows red text for an imported legacy description, that identifies a version/data mismatch rather than a current Clever Construction mechanic.

Numbers/formula: a trigger probability of 10% is an expected `1.10` trigger events per trap, subject to the trap's own repeat/trigger rules; it is not 10% more hit damage in every case. Its practical worth is a probabilistic extra activation and must be measured by PoB only if PoB models the skill's trigger multiplicity; otherwise flag it as unsupported rather than assigning a hand-made multiplier. **Confidence: high** for current text, **medium** for PoB support status because the pinned runtime was not inspected in this research pass.

Sources: https://poedb.tw/us/Clever_Construction

## 7. Pyroclast Mine overlap

Pyroclast Mine fires three projectiles at baseline and gains one projectile for every three prior mines in its detonation sequence; it also has a direct mine detonation hit and a fire-exposure aura. The source does not state a fixed number of mortar explosions that can strike one boss, so a universal overlap count is **not found**: it varies with target size, mine/boss placement, projectile count, and area of effect. Current data also does not prove that every displayed projectile can shotgun a single target.

Numbers/formula: projectile count for mine number `n` in a sequence is `3 + floor((n - 1)/3)`, before quality/other projectiles; use a separately measured hit-count multiplier `k` constrained to `0 <= k <= projectile count`. No sourced guide consensus for a PoB value was found, so the optimizer should keep PoB's native value and attach a measurement-required overlap note rather than use an invented 3/5/etc. **Confidence: high** for projectile formula, **low** for real overlap count.

Sources: https://poedb.tw/us/Pyroclast_Mine

## 8. Trauma Support

Trauma is a self-hit, not a per-second degeneration: when the first supported attack hit gains a Trauma stack, the player takes physical damage per Trauma stack. At gem level 20 this is 146 physical damage per stack gained, Trauma lasts 6.9 seconds, and the attack gains 10-17 added physical damage per stack. The self-hit is physical and therefore is mitigated by the player's physical-hit defenses such as armour, physical damage reduction, block where applicable, and other hit mitigation; builds survive through those layers, recovery, stack/rate limits, and sometimes reduced duration.

Numbers/formula: incoming raw self-hit on gaining the next stack is `146 x current Trauma stacks` at level 20; at a sustained hit rate `r`, raw incoming self-hit rate rises approximately with the stacks maintained, bounded by duration and actual successful hits. I found no primary/community source establishing that PoB includes Trauma in `NetLifeRegen`/net recovery; it should be tested directly in the pinned runtime before becoming an optimizer rail. **Confidence: high** for tooltip values, **medium** for mitigation statement, **low** for PoB net-recovery accounting.

Sources: https://poedb.tw/us/Trauma_Support

## 9. Pride and Elemental Overload

Pride ramps an enemy from 19% more physical damage taken to 39% at level 20 after that enemy has remained in the aura for four seconds; the exact start/max values scale with gem level and aura effect. Elemental Overload's current text is skill-local: skills that have dealt a critical strike in the past eight seconds deal 40% more elemental hit and ailment damage; the triggering crit itself is not enhanced. Its uptime for independent hit/crit rolls is `1 - (1 - c)^(8r)`, where `c` is effective crit chance per hit and `r` hits per second; the useful threshold for approximately one expected crit per 8 seconds is `r = 1/(8c)`.

Only skills used by the player can activate EO; traps, mines, and totems can benefit after the player activates it, while minions do not interact with it. **Confidence: high.**

Sources: https://poedb.tw/us/Pride ; https://poedb.tw/us/Elemental_Overload

## 10. Kinetic Fusillade and Tornado

Kinetic Fusillade creates one hovering projectile per attack, resets every existing hover duration whenever it is used again, has a 0.5-second base duration in 3.29, a maximum of 12 hovers, and fires projectiles in sequence with 50 ms base delay. More attack speed therefore increases the number available before the first release only until the duration/reset behavior and 12-projectile cap; excessive recasting can postpone firing indefinitely, while reduced duration lowers the fill window. Later projectiles deal 8% more damage per prior projectile at level 20, so the launch order and achieved stored count matter more than naïve attack DPS.

Tornado can take up to 20 player-projectile hits during its initial 1.5-second duration and reflects 10% of damage taken from those projectiles to enemies in addition to its own hit every 0.25 seconds; it is a bounded auxiliary damage sink, not a generic full projectile-DPS duplicate. Estimate it as its own PoB skill plus at most `0.10 x projectile damage actually dealt to Tornado`, constrained by 20 valid collisions and targeting geometry; do not add a blanket 10% of total projectile DPS. **Confidence: high** for displayed limits, **medium** for live-use optimization because no guide measurement was retrieved.

Sources: https://poedb.tw/us/Kinetic_Fusillade ; https://poedb.tw/us/Tornado

## 11. Spellslinger and trigger breakpoints

Spellslinger currently has a 0.60-second cooldown, while the support grants up to 38% increased cooldown recovery at level 20. Its effective maximum trigger rate is `1 / (0.60 / (1 + CDR))`, capped by actual qualifying wand attack rate; at 0% CDR this is 1.667 triggers/s and at 38% it is 2.300 triggers/s. Any attack beyond that cap fires normal wand shots while the linked spell is unavailable, so it cannot lower the spell's theoretical rate, but it can lower practical damage if it displaces another attack/trigger timing or increases costs without increasing spell triggers.

Numbers/formula: cooldown `t = baseCooldown / (1 + total increased CDR)`; useful attack-rate breakpoints are `1/t`. For a 0.15-second trigger cooldown, the corresponding rates are 6.667/s at 0% CDR, 7.333/s at 10%, 8.000/s at 20%, 8.667/s at 30%, and 9.333/s at 40%; choose an attack rate at or just below the relevant breakpoint after server/timing testing. **Confidence: high** for Spellslinger values and formula, **medium** for the generic 0.15-second practical warning.

Sources: https://poedb.tw/us/Spellslinger

## Optimizer Summary: numbers to use

1. Regular Spell Cascade has three areas; do not hard-code 9 VD orbs from one five-corpse Desecrate.
2. Use VD 6 orbs only after a source/placement proof; same-trigger Spellslinger needs pre-existing corpses or a measured ordering proof.
3. Ignite satisfies “burning enemy”; Burning Damage scales burning DoT, not a generic hit condition.
4. Shock estimate: `0.5 x (hit/threshold)^0.4`, apply effect modifiers and min/max clamps; current boss thresholds need corpus verification.
5. Mine resource floor: `unreserved >= N x per-mine base reservation + next throw cost`.
6. Imbalanced Guard: compare `A/(A+5H)` to `min(0.5,2A/(2A+5H))`; crossover `A=5H`.
7. Clever Construction is now 10% additional trap trigger, expected multiplier 1.10 only if supported/modeled.
8. Pyroclast projectiles per mine: `3 + floor((n-1)/3)`; overlap count requires a measured skill gate.
9. Trauma level 20 raw self-hit: `146 x stacks` per stack gained, not per second.
10. Pride maxes after 4 s; EO is 8 s and uptime is `1-(1-c)^(8r)` from self-used skills only.
