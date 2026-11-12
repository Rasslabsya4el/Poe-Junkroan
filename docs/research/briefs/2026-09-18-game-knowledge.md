# Research brief: Path of Exile 1 mechanics (patch 3.26-3.29 era), for a build optimizer

You are a researcher. Use web search and page fetches. Primary sources in this order:
poewiki.net (the community wiki), then Reddit (r/pathofexile, r/PathOfExileBuilds; old.reddit.com
and the `.json` suffix often load when the main site does not), the official forum, poedb.tw,
GGG dev posts (Mark_GGG), Path of Building community issues. Do NOT answer from memory alone:
every claim needs a source URL. If sources disagree or you find nothing, say so plainly; a wrong
number is worse than "not found". Do not modify any file except the report named at the end.

For every question give: the answer in 2-6 sentences, the numbers / formula, the source URLs
with the date you read them, and a confidence (high / medium / low).

1. Volatile Dead + Spell Cascade Support (regular, NOT Greater / Awakened): VD consumes up to 3
   corpses per cast, Spell Cascade repeats the cast in extra areas. With Desecrate (5 corpses per
   cast, cap 10) as the corpse source, how many orbs per VD cast do players realistically get
   (the owner's memory: random 6-8, average ~7; 9-10 only with Greater / Awakened Spell Cascade or
   more Desecrate investment)? Same question for a Spellslinger setup (Desecrate and VD both
   triggered). What count do build guides type into Path of Building?
2. Is an ignited enemy "burning"? Do Immolate Support ("against burning enemies"), Burning Damage
   Support and "damage against burning enemies" work against an enemy that is only ignited?
3. Shock: the exact formula for shock effect from a lightning hit vs the enemy's ailment
   threshold; the ailment threshold of pinnacle bosses / Uber bosses; minimum and maximum shock;
   whether successive shocks "ramp" (only the strongest applies? duration?); how Path of Building
   models it (config "Effect of Shock", any automatic calculation); how to estimate the expected
   shock on a pinnacle boss from a build's average lightning hit.
4. Mines (Blastchain, High-Impact, Pyroclast Mine, Exsanguinate via mines): the mana
   RESERVATION mechanic of mines (how much each placed mine reserves, when it is released), and
   what it implies for the unreserved mana a mine build needs to keep N mines out; typical N.
   Trap thrown by a mine (a trap skill linked to a mine support, e.g. Lightning Trap + High-Impact
   Mine): does it work, who uses it, how does it play. For traps, mines, totems and minions as
   proxies: which "on hit", "on kill", "when you hit a marked enemy", charge-generation and leech
   effects work for the player and which do not.
5. Imbalanced Guard keystone: exact current text; with the armour formula (DR = A / (A + 5 x
   damage), and the 90% cap), for which armour values and incoming hit sizes is it better or worse
   than normal armour; community consensus on when to take it.
6. "Clever Construction" (passive skill, trap cluster): exact current text; which part Path of
   Building does not support (shown red); what it is worth to a trap build in practice.
7. Pyroclast Mine: how many of its projectiles / explosions hit a single large boss per
   detonation (overlap / shotgun), typical numbers people use in Path of Building.
8. Trauma Support: the self-inflicted physical damage per Trauma stack, per hit or per second,
   how it is mitigated, how builds survive it, and whether Path of Building counts it in net
   recovery / degen.
9. Pride aura: how long until its maximum effect on an enemy (the ramp), initial vs maximum
   value. Elemental Overload: the "crit recently" window (8 seconds?), the uptime as a function
   of crit chance and hit rate, whether totems / traps / mines / minions proc it for the player.
10. Kinetic Fusillade: how attack speed and projectile / skill effect duration interact (why
    players balance attack speed against reduced duration), and what the Tornado (Tornado skill
    gem) adds to projectile builds and how people estimate its damage.
11. Spellslinger and other trigger setups: how the trigger cooldown and attack speed interact
    (effective trigger rate breakpoints: why more attack speed can LOWER damage), the formula
    and the breakpoints for the default 0.15 s-class cooldowns with cooldown recovery.

Write the final report as markdown to `docs/research/2026-09-18-game-knowledge.md` in this
repository (create it; touch no other file), one section per question in the order above, then a
10-line summary of the numbers an optimizer should use. English. No filler.
