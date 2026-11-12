# Brief: every source of overleech in Path of Exile, the non-obvious ones too (#610)

Context: Path of Exile 3.25 and later. "Overleech" here means leech that is NOT removed when the pool is full
("Life Leech effects are not removed when Unreserved Life is Filled", "Energy Shield Leech effects are not removed
when Energy Shield is Filled", and variants), so the character is always "Leeching" and every "while Leeching" effect
works all the time. Our optimizer turns Path of Building's config "Are you Leeching?" on for a build that has such
a source. We already know four sources from PoB's own data: Slayer's Brutal Fervour, Trickster's Soul Drinker, the
unique claw Essentia Sanguis ("Energy Shield Leech Effects from Attacks are not removed at Full Energy Shield"), the
unique Offering to the Serpent gloves ("Life Leech effects are not removed when Unreserved Life is Filled"), and a
mod family "VillageESLeechFromAttacksNotRemovedOnFullES" on items. The owner says there are non-obvious sources
(his unsure examples: the shield Mahuxotl's Machination with Timeless Jewel keystones giving Energy Shield overleech;
a belt with a timeless keystone). The unique Mahuxotl's Machination in our data lists the keystones Corrupted Soul,
Divine Flesh, Eternal Youth, Everlasting Sacrifice, Immortal Ambition, Vaal Pact.

Questions (each answer: the source URL, date, author and a short verbatim quote; "not found" is allowed; keep every
condition the source attaches):
1. Is there any overleech effect among the keystones Corrupted Soul, Divine Flesh, Eternal Youth, Everlasting
   Sacrifice, Immortal Ambition, Vaal Pact (poewiki pages), and the exact stat line if so?
2. A complete list of overleech sources by kind: ascendancy notables, unique items, passive tree notables or
   keystones, Timeless / Legion jewel keystones, Eldritch / Searing Exarch or Eater of Worlds implicits, crafted
   or Harvest / Heist / Betrayal mods, Pantheon, and support gems. Each with the exact in-game stat line. The
   poewiki Cargo search "not removed" on mods and on items is the first place to look.
3. For each source from 2: does it work for Life, Energy Shield, or Mana leech, and does Path of Building model it
   (poewiki and PoB's issue tracker on github.com/PathOfBuildingCommunity/PathOfBuilding: search "not removed at
   Full" and "Leeching")?
4. How players talk about overleech in practice (Reddit r/pathofexile, r/PathOfExileBuilds, poe forum): which builds
   treat "while Leeching" effects as always on and through which source.

Report: `docs/research/2026-10-10-overleech-sources.md`, every answer with URL, date, author, verbatim quote and the
attached conditions, then one "what it says" line per question. At least one reddit.com URL is required.
