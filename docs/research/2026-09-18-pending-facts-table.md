# Pending research facts: the table to approve from (2026-09-18)

Only decisions (D62 amendment 2). Ramp counts (Sigil stages, Wither stacks, corpses consumed,
Pride's effect) are arithmetic and are never asked. The store is
`src/junkroan/mechanics/pending_facts.json`; approving a row is editing its `"status"` to
`"approved"`, nothing else. `pending` = optimistic lane only, with a "would move the conservative
number by X%" note on the build; `approved` = binding in both lanes; `disputed` = off everywhere.

| # | Fact and number | Sources / confidence | What it moves (measured in PoB) | Approve | Leave |
|---|---|---|---|---|---|
| 1 | **Trauma is a self-hit PoB counts nowhere.** Every attack hit that gains a stack deals you `per stack x stacks` physical damage: **146 per stack at gem 20, 126 at our 18**, Trauma lasts 6.9 s. PoB has the number in the gem's level data and maps it to no modifier -- not the cost, not a degen, not NetLifeRegen. | PoEDB Trauma Support + PoB's own data (both give 146); Reddit: 25-60 stacks are what players sustain, behind ~87-90% physical mitigation; your static_strike s3 reading ("752 physical damage per attack"). **high** | **static_strike** with the Trauma Support our s3 took: 126 x 6 stacks = **756 per attack x 1.99 hits/s = 1,503 life/s** against **+65/s** idle recovery. The "no degen while idle" floor (D63.3) flips by **1,438/s = 41% of the 3,466 life pool per second**. Same for any Boneshatter build. | The optimizer stops taking Trauma on a build that cannot pay for it, as it already does with the Chaos Mastery. Cost: a build that *can* pay (armour, recoup) is priced pessimistically -- the hook charges the raw hit, because PoB gives no readable "damage taken from a hit of size H" per candidate. | Trauma stays free: a build that kills itself with its own attack keeps scoring as if it did not, and your 752 per attack stays invisible. |
| 2 | **At most ~3 Blood Stance spikes reach one boss** (the usual count is 1-2). Our optimistic lane was claiming all 7 the gem makes. | Reddit Blood Stance testing ("4-5 spikes, usually 1-2 hit"; "~3 to beat Blood Stance's less-damage"); PoEDB Perforate (PoB's only cap is the spike count). **medium** | **bleed_perforate**, optimistic lane only: **360,005 -> 193,828, -46.2%**. Conservative (1 spike, 105,434) does not move now or on approval. | The optimistic lane stops claiming a number nobody can play; nothing else changes. Cheap. | A 46% overstatement stays on every Blood Stance build, and the lane gap stops meaning anything there. |
| 3 | **Volatile Dead orbs with a regular Spell Cascade: 6 or 9?** *The sources disagree, and so do your two verdicts.* We compute **9** today (PoB's 3 cascade areas x 3 corpses per cast). | Mechanics (PoEDB VD + Spell Cascade): three areas x up to three corpses, so 9 needs three corpses standing in each area and one five-corpse Desecrate cannot promise it -- 6 defensible, 6-8 practical. Reddit: 9 is the PoB convention when VD has the corpses to itself, 7 when Detonate Dead competes. **medium both ways** | **archmage_volatile_dead, vd_spellslinger**: the count multiplies FullDPS directly, so 9 -> 6 is **-33%** on both. | **9** = leave the code as it is, comparable to the author PoBs, which use it. **6** = the mechanic's floor; both VD references lose a third and stop being comparable to their authors. | The disagreement stays on the record and the code keeps 9. |

## Recorded, not decisions

- **Pyroclast hits per mine on a boss** (3.34 from one 2024 post, range 2-4; the mechanics report
  answers "not found"): PoB has no overlap input for Pyroclast at all, so there is nowhere to put
  a number without inventing a damage multiplier. Disputed, hook off.
- **Shrapnel Ballista shotgunning projectiles** (1-2 on a moving target, 8-14 on a stationary one):
  the two reports contradict each other on whether Arrow Nova can support it. PoB's own
  support-legality readback already settles the legality half, and the count would be an
  assumption about the fight. Disputed, hook off.
- **Shock thresholds (25M / 70M)**: PoB already computes it, with the same formula
  (`CalcOffence.lua:5210-5225`: `threshold = monsterAilmentThresholdTable[enemyLevel] x 7.68 for a
  boss x the map multipliers`, effect `50 x (damage / threshold)^0.4 x effectMod`). Your
  static_strike note ("why is there no shock?") is answered by it: PoB applies the shock the
  build's own hits earn; the checkbox stands only for a *second* source, which is an assumption.

## What the research answered that PoB already carries (arithmetic, not decisions)

Withering Touch's 25% wither chance and 2 s duration (PoB `constantStats`), Corpse Pact's 4% per
corpse and its 200% cap (PoB's own mod text), Desecrate 5 corpses and the 10 cap, Sigil of Power's
400 mana per stage, Spellslinger's 0.60 s cooldown, mine reservation per placed mine, ignite
counting as burning (already `config_rules.AILMENT_PROOF`), Elemental Overload's 8 s window with
proxies-yes / minions-no (already `_crit_recently`), Elemental Hit's mean over three parts (rule
20). Accuracy's 95% floor stays your policy: both reports answer "not found" for any community
threshold.
