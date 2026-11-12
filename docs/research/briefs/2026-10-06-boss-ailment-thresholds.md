# Brief: the ailment threshold of every Guardian and Pinnacle boss, and the ailment rules (#606)

Context: Path of Exile 3.26+ (the current league). Our optimizer measures builds in Path of Building (PoB) with the
config `Is the enemy a Boss? = Guardian/Pinnacle Boss`, Enemy Level 84. Non-damaging ailments (Shock, Chill, Scorch,
Brittle, Sap) have an effect that depends on the hit's damage against the enemy's AILMENT THRESHOLD. For bosses the
ailment threshold is lower than their life (the wiki's Shock page uses Sirus as its example). We need the real
numbers per boss from game data, to decide which threshold our config should imply.

Questions (each answer: the source URL, date if shown, and a short verbatim quote or the table row as shown; "not
found" is allowed; keep every condition the source attaches, such as map tier, Uber version, area level):
1. For every Pinnacle boss (The Shaper, The Elder, Uber Elder, Sirus Awakener of Worlds, The Maven, The Searing
   Exarch, The Eater of Worlds, Incarnation of Fear/Dread/Neglect if listed, Venarius, Catarina, Kitava if listed)
   and their Uber versions: base Life, the ailment threshold (or "ailment threshold" multiplier / "less ailment
   threshold" stat) and the monster level, as poedb.tw (monster pages, "Ailment Threshold" field) or poewiki.net
   lists them.
2. The same for the Guardians: the four Shaper Guardians (Guardian of the Minotaur/Hydra/Chimera/Phoenix), the four
   Conquerors (Al-Hezmin, Baran, Drox, Veritania), the Elderslayers if listed, and the Eldritch Guardians
   (Black Star, Infinite Hunger, Elder Guardians).
3. The game's general rule for monster ailment threshold: the formula or table (by monster level, rarity, the stat
   `monster_ailment_threshold_+%` or similar, "unique bosses have reduced ailment threshold"), quoted verbatim
   from poewiki "Ailment threshold" / "Ailment" pages or poedb's monster stat pages.
4. Any patch note (3.x) that changed boss ailment thresholds, quoted verbatim with the patch number.

Report: `docs/research/2026-10-06-boss-ailment-thresholds.md`, every answer with URL and verbatim quote, then one
"what it says" line per question; one table at the end: boss, version (normal / Uber), monster level, Life,
ailment threshold, source URL. Sources are game databases and the wiki, not forums.
