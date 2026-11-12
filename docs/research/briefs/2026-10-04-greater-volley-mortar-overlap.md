# Brief: Greater Volley on mortar spectres (Forged Frostbearer / Ice Mortar): how many projectiles land on one boss (#44)

Context: Path of Exile 3.29. A Raise Spectre build raises Forged Frostbearer, whose skill Ice Mortar fires a mortar
projectile that explodes in an area on landing. With Greater Volley Support the spectre fires 5 mortars at once
(4 additional projectiles) in a spread. Our optimizer measures the build in Path of Building, where the
`Projectile count` input decides how many of the 5 explosions are assumed to overlap the target: at `count` 2 the
build's `FullDPS` is 274,542, at 4 it is 491,971, at the author's 20 it is 2,231,401. PoB cannot compute the real
overlap; it is a game fact we need from sources. The question is how many of the 5 mortars actually land on a
boss-size target in practice, so the search assumes the right count instead of rejecting Greater Volley.

Questions (each answer: the source URL, date, author and a short verbatim quote; "not found" is allowed; keep every
condition the source attaches, such as distance to the target, target size, Volley vs Greater Volley vs GMP):
1. How Ice Mortar's projectiles behave with Greater Volley Support: are the 5 mortars fired in a fan / parallel
   spread, what is the spread width, and do their explosions overlap on one target? Sources: poewiki pages for
   Ice Mortar, Forged Frostbearer, Greater Volley Support, Volley Support; GGG patch notes or developer posts on
   mortar projectiles and on the "projectiles from one cast cannot shotgun, but their area explosions can overlap"
   rule (quote the exact wording of the rule and the patch it came from).
2. Reddit (r/PathOfExileBuilds, r/pathofexile) or forum (pathofexile.com forums, poe-vault, maxroll) reports from
   spectre players using Forged Frostbearer / Ice Mortar or other mortar spectres with Greater Volley: how many of
   the projectiles hit one boss-size target (all 5, 2-3, 1), at what distance, and whether they recommend
   Greater Volley, Volley, GMP or none for mortar spectres. Quote the count and the condition.
3. Any measured or stated per-target overlap number for mortar-type monster projectiles in general (e.g. from
   other mortar spectres, Ice Mortar on Frostbearers, "Mortar" skills of monsters), including PoB community
   threads on which `Projectile count` value players set for mortar spectres with Greater Volley.

Report: `docs/research/2026-10-04-greater-volley-mortar-overlap.md`, every answer with URL, date, author, verbatim
quote and the attached conditions, then one "what it says" line per question; the count per source in one table at
the end (source, URL, count on one boss, condition). At least one reddit.com URL is required.
