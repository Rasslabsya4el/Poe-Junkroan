# Research brief 2: Path of Exile 1 mechanics (patch 3.26-3.29 era), for a build optimizer

Same rules as brief 1: use web search and page fetches; poewiki.net first, then Reddit
(r/pathofexile, r/PathOfExileBuilds; old.reddit.com and the `.json` suffix often load), the
official forum, poedb.tw, GGG dev posts, Path of Building community issues. Every claim needs a
source URL and the date read; say "not found" rather than guess. For every question: the answer
in 2-6 sentences, the numbers / formula, sources, confidence (high / medium / low). Touch no file
except the report named at the end.

1. Perforate: how the skill hits in Blood Stance and in Sand Stance (number of spikes, overlap /
   multiple hits on one target, area), how its bleed is applied and scaled, what Path of Building
   computes for it and what players type into its config; why a Path of Building number for a
   Perforate bleed build could differ by 3x between two builds with similar gear.
2. Elemental Hit: the element is chosen at random per attack unless jewels / items exclude
   elements (Combat Focus). What does Path of Building compute (one chosen element as a skill
   part?), and how do players estimate real damage when only one element is scaled and none are
   excluded? Is "average of the three parts" the accepted estimate?
3. Necromancer Corpse Pact and the corpse conditions ("spawned a corpse recently", "consumed a
   corpse recently", "corpses consumed recently" count, "nearby corpses"): realistic values for a
   build that hand-casts Desecrate and Volatile Dead (no Arcanist Brand automation), and with
   automation; how Undertaker's "+2 corpses" style nodes change the count.
4. Sigil of Power: maximum stages, mana spent per stage, how long it takes to reach maximum for
   a typical mana cost (e.g. 50, 150, 400 mana per cast at 3 casts per second), what Path of
   Building's "Sigil of Power stages" input expects (range).
5. Withered: stacks cap (15), how fast totems with Wither (or Withering Step, Withering Touch)
   build stacks on one boss, realistic sustained stack count for N totems.
6. Sacrifice Support: its exact text, the life cost per use, whether Path of Building counts the
   cost anywhere (life cost, degen), how builds sustain it.
7. Shrapnel Ballista + Arrow Nova Support: does the combination work, how the arrows land, is it
   used by known builds, any known Path of Building overestimation.
8. Accuracy: what chance to hit do attack builds accept in practice at league start (the owner's
   rule of thumb: 95% minimum), and how the "feel" degrades below that.

Write the final report as markdown to `docs/research/2026-09-18-game-knowledge-2.md` in this
repository (create it; touch no other file), one section per question in order, then a 10-line
summary of the numbers an optimizer should use. English. No filler.
