# Boss Ailment Thresholds, PoE 3.26+
**Research date:** 2026-10-06  
**Scope:** PoE 1 game database / official sources only. No workspace files were changed, per instruction.

## Method and Caveats
- **Primary database:** [PoEDB US](https://poedb.tw/us/), live record pages inspected 2026-10-06. PoEDB currently identifies its data set as `Allflame v3.29`; it does not display a per-record publish or revision date.
- **PoEDB condition attached to every absolute stat row:** “**The following values do not include map affix bonuses, monster buff bonuses, altar bonuses, atlas skill bonuses.**”
- `Life 2560%` and `Ailment Threshold 504%` are the monster record’s displayed base multipliers. The concrete `Life` and `Ailment Threshold` figures in each row below are PoEDB’s resulting absolute values for the stated monster level.
- A level-85 “Uber” arena does **not** always mean PoEDB has a separate level-85 monster stat record. Where it does not, no value has been calculated or inferred; it is reported as **not published separately**.
- “Uber Elder” below means the combined Elder/Shaper encounter. A level-85 fragment variant is separately called “Uber Uber Elder” by PoEDB’s fragment data.
- The four Conquerors are the Elderslayers. PoEDB has records named `...ApparitionUber` for level-83 encounters, but that database naming should not be conflated with the level-85 Uber-pinnacle fragment system.

## 1. Pinnacle Bosses

### The Shaper
**Source:** [PoEDB: The Shaper](https://poedb.tw/us/The_Shaper)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `TheShaperBoss`; The Shaper’s Realm; normal area level 84.

> `Life 2560%`  
> `Ailment Threshold 504%`  
> `Level 84`  
> `Life 75,193,704`  
> `Ailment Threshold 6,957,767`

**Uber condition source:** [PoEDB: Cosmic Fragment](https://poedb.tw/us/Cosmic_Fragment)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`  
> “The Shaper's full power is unleashed”

**Uber absolute Life / threshold:** not published as a separate level-85 monster row on the Shaper page.

### The Elder
**Source:** [PoEDB: The Elder](https://poedb.tw/us/The_Elder)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `TheElder`; Absence of Value and Meaning; level 83.

> `Life 1860%`  
> `Ailment Threshold 504%`  
> `Level 83`  
> `Life 47,135,222`  
> `Ailment Threshold 6,002,899`

The independent wiki result agrees on the level and multipliers:

**Source:** [PoE Wiki: The Elder](https://www.poewiki.net/wiki/The_Elder)  
**Date / author:** page result dated 2026-08-14; author not shown.  
**Conditions:** Absence of Value and Meaning.

> `Level | 83`  
> `Health | 1860% life, 504% ailment threshold; 2000% of life as Energy Shield`

**Uber Elder:** Elder has no standalone level-85 “Uber Elder” form; the relevant combined encounter is below.

### Uber Elder: Shaper and Elder components
**Source:** [PoEDB: The Shaper](https://poedb.tw/us/The_Shaper), record `TheShaperBossUberElder`; [PoEDB: The Elder](https://poedb.tw/us/The_Elder), record `TheElderUber`  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** normal combined Shaper’s Realm encounter, area / monster level 84.

> `Level 84`  
> `Life 48,405,947`  
> `Ailment Threshold 6,957,767`  
> `Life 1648%`  
> `Ailment Threshold 504%`

**Level-85 condition source:** [PoEDB: Decaying Fragment](https://poedb.tw/us/Decaying_Fragment)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`  
> “The Shaper and Elder's full power is unleashed”

**Level-85 absolute Life / threshold:** not published as a distinct stat row.

### Sirus, Awakener of Worlds
**Source:** [PoEDB: Sirus, Awakener of Worlds](https://poedb.tw/us/Sirus%2C_Awakener_of_Worlds)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `AtlasExile5`; Eye of the Storm; level 84.

> `Life 2400%`  
> `Ailment Threshold 504%`  
> `Level 84`  
> `Life 70,494,097`  
> `Ailment Threshold 6,957,767`

**Uber condition source:** [PoEDB: Awakening Fragment](https://poedb.tw/us/Awakening_Fragment)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`

**Uber absolute Life / threshold:** not published as a separate level-85 Sirus monster row.

### The Maven
**Source:** [PoEDB: The Maven](https://poedb.tw/us/The_Maven)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `TheMaven`; Absence of Mercy and Empathy; normal level 84.

> `Life 1755%`  
> `Ailment Threshold 504%`  
> `Level 84`  
> `Life 51,548,809`  
> `Ailment Threshold 6,957,767`

The wiki result agrees:

**Source:** [PoE Wiki: The Maven](https://www.poewiki.net/wiki/The_Maven)  
**Date / author:** page result dated 2026-08-12; author not shown.  
**Conditions:** regular Maven’s Writ versus Uber.

> `Level | 84 (Regular ...) 85 (Uber)`  
> `Health | 1755% life, 504% ailment threshold; 100% of life as Energy Shield`

**Uber absolute Life / threshold:** the source identifies level 85 but does not publish a separate level-85 absolute stat row.

### The Searing Exarch
**Source:** [PoEDB: The Searing Exarch](https://poedb.tw/us/The_Searing_Exarch)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `CleansingBoss`; Absence of Patience and Wisdom; normal level 84.

> `Life 1430%`  
> `Ailment Threshold 301%`  
> `Level 84`  
> `Life 42,002,733`  
> `Ailment Threshold 4,155,333`

**Uber condition source:** [PoEDB: Blazing Fragment](https://poedb.tw/us/Blazing_Fragment)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`

**Uber absolute Life / threshold:** not published separately by the monster page.

### The Eater of Worlds
**Source:** [PoEDB: The Eater of Worlds](https://poedb.tw/us/The_Eater_of_Worlds)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `ConsumeBoss`; Absence of Symmetry and Harmony; normal level 84.

> `Life 1400%`  
> `Ailment Threshold 294%`  
> `Level 84`  
> `Life 41,121,557`  
> `Ailment Threshold 4,058,698`

**Uber condition source:** [PoEDB: Devouring Fragment](https://poedb.tw/us/Devouring_Fragment)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`

**Uber absolute Life / threshold:** not published separately by the monster page.

### Incarnation of Fear
**Source:** [PoEDB: Incarnation of Fear](https://poedb.tw/us/Incarnation_of_Fear)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** normal `AngerZanaBoss`, Moment of Trauma, level 83.

> `Life 2000%`  
> `Ailment Threshold 800%`  
> `Level 83`  
> `Life 50,683,034`  
> `Ailment Threshold 9,528,410`

**Uber condition:** `AngerZanaBossUBER`, Moment of Trauma opened with four Traumatic Fragments; level 85.

> `Life 1440%`  
> `Ailment Threshold 800%`  
> `Level 85`  
> `Life 45,063,462`  
> `Ailment Threshold 11,766,571`

### Incarnation of Dread
**Source:** [PoEDB: Incarnation of Dread](https://poedb.tw/us/Incarnation_of_Dread)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** normal `BenevolenceZanaBoss`, Moment of Reverence, level 83.

> `Life 2000%`  
> `Ailment Threshold 800%`  
> `Level 83`  
> `Life 50,683,034`  
> `Ailment Threshold 9,528,410`

**Uber condition:** `BenevolenceZanaBossUBER`, Moment of Reverence opened with four Reverent Fragments; level 85.

> `Life 1440%`  
> `Ailment Threshold 800%`  
> `Level 85`  
> `Life 45,063,462`  
> `Ailment Threshold 11,766,571`

### Incarnation of Neglect
**Source:** [PoEDB: Incarnation of Neglect](https://poedb.tw/us/Incarnation_of_Neglect)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** normal `Ignorance`, Moment of Loneliness, level 83.

> `Life 2000%`  
> `Ailment Threshold 800%`  
> `Level 83`  
> `Life 50,683,034`  
> `Ailment Threshold 9,528,410`

**Uber condition:** `IgnoranceUber`, Moment of Loneliness opened with four Lonely Fragments; level 85.

> `Life 1440%`  
> `Ailment Threshold 800%`  
> `Level 85`  
> `Life 45,063,462`  
> `Ailment Threshold 11,766,571`

### Venarius
**Source:** [PoEDB: Venarius](https://poedb.tw/us/Venarius)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** `SynthesisVenariusBoss`; Cortex’s base monster record level is 79. Cortex itself has a monster-level override of 83.

> `Life 400%`  
> `Ailment Threshold 400%`  
> `Level 79`  
> `Life 4,610,269`  
> `Ailment Threshold 2,212,929`

**Uber condition source:** [PoEDB: Memento Mori](https://poedb.tw/us/Memento_Mori)  
**Date / author:** no per-page date or named author shown.

> `Area Level: 85`  
> “Venarius' full power is unleashed”

**Uber absolute Life / threshold:** not published separately. Cortex also has random Synthesis modifiers, and Memento Mori states that it doubles the effect of additional modifiers; static values are not the final effective encounter values when those modifiers apply.

### Catarina, Master of Undeath
**Source:** [PoEDB: Catarina, Master of Undeath](https://poedb.tw/us/Catarina%2C_Master_of_Undeath)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.  
**Conditions:** Mastermind’s Lair, level 83. Catarina has separate phase records.

> `BetrayalCatarina1`  
> `Life 938%`  
> `Ailment Threshold 505%`  
> `Level 83`  
> `Life 23,770,343`  
> `Ailment Threshold 6,014,809`

> `BetrayalCatarina2`  
> `Life 1425%`  
> `Ailment Threshold 505%`  
> `Level 83`  
> `Life 36,111,662`  
> `Ailment Threshold 6,014,809`

**Uber version:** not found. No explicit Uber metadata or level-85 route was found on the current PoEDB records.

### Kitava
**Source:** [PoEDB: Kitava, the Insatiable](https://poedb.tw/us/Kitava%2C_the_Insatiable)  
**Date / author:** no per-page date or named author shown; PoEDB database, inspected 2026-10-06.

**Act 5 condition:** `Kitava1`, The Cathedral Rooftop, level 45.

> `Life 7200%`  
> `Ailment Threshold 3000%`  
> `Level 45`  
> `Life 99,000`  
> `Ailment Threshold 41,250`

**Act 10 condition:** `KitavaFinal`, The Feeding Trough, level 67.

> `Life 5500%`  
> `Ailment Threshold 3000%`  
> `Level 67`  
> `Life 326,077`  
> `Ailment Threshold 177,860`

**Uber version:** not found.

**What it says:** Current high-end normal boss records commonly use a 504% displayed ailment-threshold multiplier, but current absolute thresholds vary by the boss record; Exarch and Eater are lower, and the three Incarnations use 800%. The requested level-85 variants have independently published absolute rows only for Fear, Dread, and Neglect.

## 2. Guardians

### Shaper Guardians
**Source family:** PoEDB monster and map pages.  
**Date / author:** no per-page dates or named authors shown; inspected 2026-10-06.  
**Conditions:** current Guardian maps are `Tier: 16`, `Area Level: 83`. No normal level-84 stat table is published.

| Boss | Source | Verbatim record fields |
|---|---|---|
| Guardian of the Minotaur | [Monster](https://poedb.tw/us/Guardian_of_the_Minotaur#GuardianoftheMinotaurMinotaurBoss), [Maze of the Minotaur](https://poedb.tw/us/Maze_of_the_Minotaur) | `Tier: 16`; `Area Level: 83`; `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |
| Guardian of the Hydra | [Monster](https://poedb.tw/us/Guardian_of_the_Hydra#GuardianoftheHydraHydraBoss), [Lair of the Hydra](https://poedb.tw/us/Lair_of_the_Hydra) | `Tier: 16`; `Area Level: 83`; `Life 1000%`; `Ailment Threshold 504%`; `Level 83`; `Life 25,341,517`; `Ailment Threshold 6,002,899` |
| Guardian of the Chimera | [Monster](https://poedb.tw/us/Guardian_of_the_Chimera#GuardianoftheChimeraChimeraBoss), [Pit of the Chimera](https://poedb.tw/us/Pit_of_the_Chimera) | `Tier: 16`; `Area Level: 83`; `Life 1000%`; `Ailment Threshold 504%`; `Level 83`; `Life 25,341,517`; `Ailment Threshold 6,002,899` |
| Guardian of the Phoenix | [Monster](https://poedb.tw/us/Guardian_of_the_Phoenix#GuardianofthePhoenixPhoenixBoss), [Forge of the Phoenix](https://poedb.tw/us/Forge_of_the_Phoenix) | `Tier: 16`; `Area Level: 83`; `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |

**Uber versions:** not found. PoEDB exposes standalone, scarab, Gauntlet, and Elder-encounter variants, but no Shaper-Guardian monster record labelled Uber.

### Conquerors / Elderslayers
**Source family:** PoEDB boss and area pages.  
**Date / author:** no per-page dates or named authors shown; inspected 2026-10-06.  
**Conditions:** normal records are level 68 areas; distinct PoEDB `ApparitionUber` and `AtlasExilesBoss#Uber` records are level 83.

| Boss | Version / condition | Source | Verbatim record fields |
|---|---|---|---|
| Al-Hezmin, The Hunter | Normal; Hunter’s Ambush `AtlasExilesBoss3`; area level 68 | [Monster](https://poedb.tw/us/Al-Hezmin%2C_The_Hunter#Al-HezminTheHunterAtlasExile3Apparition), [area](https://poedb.tw/us/Hunters_Ambush) | `Life 1300%`; `Ailment Threshold 504%`; `Level 68`; `Life 1,811,503`; `Ailment Threshold 442,453` |
| Al-Hezmin, The Hunter | `AtlasExile3ApparitionUber`; `AtlasExilesBoss3Uber`; area level 83 | [Monster](https://poedb.tw/us/Al-Hezmin%2C_The_Hunter#Al-HezminTheHunterAtlasExile3ApparitionUber), [area](https://poedb.tw/us/Hunters_Ambush) | `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |
| Baran, The Crusader | Normal; Crusader’s Sanctum `AtlasExilesBoss1`; area level 68 | [Monster](https://poedb.tw/us/Baran%2C_The_Crusader#BaranTheCrusaderAtlasExile1Apparition), [area](https://poedb.tw/us/Crusaders_Sanctum) | `Life 1300%`; `Ailment Threshold 504%`; `Level 68`; `Life 1,811,503`; `Ailment Threshold 442,453` |
| Baran, The Crusader | `AtlasExile1ApparitionUber`; `AtlasExilesBoss1Uber`; area level 83 | [Monster](https://poedb.tw/us/Baran%2C_The_Crusader#BaranTheCrusaderAtlasExile1ApparitionUber), [area](https://poedb.tw/us/Crusaders_Sanctum) | `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |
| Drox, The Warlord | Normal; Warlord’s Keep `AtlasExilesBoss4`; area level 68 | [Monster](https://poedb.tw/us/Drox%2C_The_Warlord#DroxTheWarlordAtlasExile4Apparition), [area](https://poedb.tw/us/Warlords_Keep) | `Life 1300%`; `Ailment Threshold 504%`; `Level 68`; `Life 1,811,503`; `Ailment Threshold 442,453` |
| Drox, The Warlord | `AtlasExile4ApparitionUber`; `AtlasExilesBoss4Uber`; area level 83 | [Monster](https://poedb.tw/us/Drox%2C_The_Warlord#DroxTheWarlordAtlasExile4ApparitionUber), [area](https://poedb.tw/us/Warlords_Keep) | `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |
| Veritania, The Redeemer | Normal; Redeemer’s Eyrie `AtlasExilesBoss2`; area level 68 | [Monster](https://poedb.tw/us/Veritania%2C_The_Redeemer#VeritaniaTheRedeemerAtlasExile2Apparition), [area](https://poedb.tw/us/Redeemers_Eyrie) | `Life 1300%`; `Ailment Threshold 504%`; `Level 68`; `Life 1,811,503`; `Ailment Threshold 442,453` |
| Veritania, The Redeemer | `AtlasExile2ApparitionUber`; `AtlasExilesBoss2Uber`; area level 83 | [Monster](https://poedb.tw/us/Veritania%2C_The_Redeemer#VeritaniaTheRedeemerAtlasExile2ApparitionUber), [area](https://poedb.tw/us/Redeemers_Eyrie) | `Life 1300%`; `Ailment Threshold 504%`; `Level 83`; `Life 32,943,972`; `Ailment Threshold 6,002,899` |

**Source:** [PoEDB: Maven’s Invitation: The Elderslayers](https://poedb.tw/us/Mavens_Invitation%3A_The_Elderslayers)  
**Date / author:** no per-page date or named author shown.  
**Condition:** Maven invitation, area level 68.

> `Area Level: 68`  
> “The Maven must Witness: Baran, The Crusader, Veritania, The Redeemer, Al-Hezmin, The Hunter, Drox, The Warlord.”

### Eldritch Guardians: The Black Star and The Infinite Hunger
**Source family:** PoEDB monster / area pages.  
**Date / author:** no per-page date or named authors shown; inspected 2026-10-06.  
**Conditions:** PoEDB exposes a concrete level-83 boss area. Invitation recipes also exist at levels 79 and 83, but PoEDB does not publish separate concrete level-79 boss stat rows.

| Boss | Source | Conditions and verbatim record fields |
|---|---|---|
| The Black Star | [Monster](https://poedb.tw/us/The_Black_Star#TheBlackStarBlackStarBoss), [Polaric Void](https://poedb.tw/us/Polaric_Void) | `Id: MapWorldsPrimordialBoss2`; `Area Level: 83`; `Life 1400%`; `Ailment Threshold 294%`; `Level 83`; `Life 35,478,124`; `Ailment Threshold 3,501,691` |
| The Infinite Hunger | [Monster](https://poedb.tw/us/The_Infinite_Hunger#TheInfiniteHungerDoomBoss_), [Seething Chyme](https://poedb.tw/us/Seething_Chyme) | `Id: MapWorldsPrimordialBoss1`; `Area Level: 83`; `Life 1800%`; `Ailment Threshold 380%`; `Level 83`; `Life 45,614,731`; `Ailment Threshold 4,525,995` |

**Uber versions:** not found. Current PoEDB has no distinct Uber monster record or Uber area ID for either boss.

### Elder Guardians
**Source family:** PoEDB monster / area pages.  
**Date / author:** no per-page dates or named authors shown; inspected 2026-10-06.  
**Conditions:** level-82 Elder-Guardian areas; no map tier shown.

| Boss | Source | Conditions and verbatim record fields |
|---|---|---|
| The Purifier | [Monster](https://poedb.tw/us/The_Purifier#ThePurifierElderGuardian4_), [Pits of Sorrow](https://poedb.tw/us/Pits_of_Sorrow) | `Id: MapWorldsElder_Reliquary`; `Area Level: 82`; `Life 1200%`; `Ailment Threshold 504%`; `Level 82`; `Life 25,112,725`; `Ailment Threshold 4,957,252` |
| The Constrictor | [Monster](https://poedb.tw/us/The_Constrictor#TheConstrictorElderGuardian3), [Sea of Isolation](https://poedb.tw/us/Sea_of_Isolation) | `Id: MapWorldsElder_Reef`; `Area Level: 82`; `Life 1200%`; `Ailment Threshold 504%`; `Level 82`; `Life 25,112,725`; `Ailment Threshold 4,957,252` |
| The Eradicator | [Monster](https://poedb.tw/us/The_Eradicator#TheEradicatorElderGuardian2), [Manor of Madness](https://poedb.tw/us/Manor_of_Madness) | `Id: MapWorldsElder_Sceptre`; `Area Level: 82`; `Life 1200%`; `Ailment Threshold 504%`; `Level 82`; `Life 25,112,725`; `Ailment Threshold 4,957,252` |
| The Enslaver | [Monster](https://poedb.tw/us/The_Enslaver#TheEnslaverElderGuardian1), [Desert of Dementia](https://poedb.tw/us/Desert_of_Dementia) | `Id: MapWorldsElder_Desert`; `Area Level: 82`; `Life 1200%`; `Ailment Threshold 504%`; `Level 82`; `Life 25,112,725`; `Ailment Threshold 4,957,252` |

**Uber versions:** not found. `Standalone`, `StandaloneScarab`, and Maven records exist, but no monster record labelled Uber. Uber Elder is a separate combined pinnacle encounter.

**What it says:** Guardians do not have one shared absolute threshold: level and record determine it. At current level 83, Shaper Guardians and the PoEDB-labelled Conqueror Uber records use `6,002,899`; Black Star and Infinite Hunger have lower custom thresholds; Elder Guardians at level 82 use `4,957,252`.

## 3. General Monster Ailment-Threshold Rule

### Official 3.9.0 rule and formula
**Source:** [GGG, Content Update 3.9.0: Conquerors of the Atlas](https://www.pathofexile.com/forum/view-thread/2687400)  
**Date:** 2019-12-10  
**Author:** Natalia_GGG / Grinding Gear Games.

> “In general, it is much easier to Shock and Chill monsters with low values of the ailment, but harder to reach high values of Shock and Chill. The formula used to calculate Shock and Chill magnitudes is now: **1/2*[Damage % of Ailment Threshold (see below) ]^0.4**”

> “We've added an Ailment Threshold to monsters. **In the great majority of cases, the Ailment Threshold matches the monster's Maximum Life. It primarily differs for especially high-life monsters (such as The Shaper), where the threshold is reduced** to allow ailments to be applied with hits that wouldn't ordinarily reach the required Life thresholds.”

> “The minimum Shock and Chill value is now 5% (from 1%). To reach the minimum, you must deal **0.4% of a monster's Ailment Threshold** with the associated element in a single hit. To inflict a 10% Chill you must deal **1.8%** of a monster's Ailment Threshold with the associated element in a single hit. A 30% Chill requires a hit of **28%** of the monster's Ailment Threshold.”

> “The alternate ailments Sap, Scorch and Brittle have a slightly different calculation as they have lower caps on their magnitudes.”

### Wiki formulation
**Source:** [PoE Wiki: Ailment](https://www.poewiki.net/wiki/Elemental_Ailments)  
**Date / author:** no date or author shown in accessible live result.  
**Conditions:** non-damaging ailments.

> “Non-damaging ailments have the magnitude of their effect (or their duration, in the case of freeze) calculated based on the hit's damage divided by the enemy's ailment threshold.”

> “In the great majority of cases, the ailment threshold is the same as the monster's maximum life. It primarily differs for endgame bosses (such as the Shaper) and other high-life monsters, where the threshold is reduced to allow ailments to be applied with hits that wouldn't ordinarily reach the required life thresholds.”

> “Ailment threshold has a maximum of approximately 800 million.”

> “The magnitude (or effect) of a non-damaging ailment is dependent on the damage the enemy takes from the hit, not the base damage of the hit.”

### Game-database examples of default versus custom thresholds
**Source:** [PoEDB: Swarming Rat](https://poedb.tw/us/Swarming_Rat)  
**Date / author:** no per-page date or named author shown.

> `Level 68`  
> `Life 4,503`  
> `Ailment Threshold 4,503`

**Source:** [PoEDB: Gruthkul, Mother of Despair](https://poedb.tw/us/Gruthkul%2C_Mother_of_Despair)  
**Date / author:** no per-page date or named author shown.

> `Level 53`  
> `Life 42,300`  
> `Ailment Threshold 42,300`

**Source:** [PoEDB: Venarius](https://poedb.tw/us/Venarius)  
**Date / author:** no per-page date or named author shown.  
**Condition:** Cortex base monster record, level 79.

> `Life 4,610,269`  
> `Ailment Threshold 2,212,929`

### Monster level, rarity, and stat-name result
**Sources checked:** [PoE Wiki: Ailment threshold](https://www.poewiki.net/wiki/Ailment_threshold), [PoE Wiki: Ailment](https://www.poewiki.net/wiki/Ailment), [PoE Wiki: Elemental ailment](https://www.poewiki.net/wiki/Elemental_Ailments), [PoEDB: Monster level](https://poedb.tw/us/Monster_level), and [PoEDB: Monster](https://poedb.tw/us/Monster).  
**Date / author:** pages inspected 2026-10-06; no relevant per-page author/date exposed.

**Finding:** No general PoE 1 formula or table was found that derives ailment threshold from monster level and rarity. The monster-level page documents life scaling, not a generic ailment-threshold progression. The explicit general rule is maximum Life, unless the individual monster has a different threshold.

**Stat name:** the requested exact internal-style spelling `monster_ailment_threshold_+%` was not exposed in the inspected sources. PoEDB renders the applied field as:

> `Ailment Threshold 504%`

and its modifier listing style as:

> `ailment threshold +%`

**What it says:** For a normal monster, use maximum Life as threshold. For special high-life records, including bosses, use the record’s actual Ailment Threshold instead; no published level-and-rarity formula replaces that per-monster value.

## 4. PoE 1 3.x Changes to Boss Ailment Thresholds

### 3.9.0, Conquerors of the Atlas
**Source:** [GGG patch notes](https://www.pathofexile.com/forum/view-thread/2687400)  
**Date:** 2019-12-10  
**Author:** Natalia_GGG / Grinding Gear Games.

> “We've added an Ailment Threshold to monsters. In the great majority of cases, the Ailment Threshold matches the monster's Maximum Life. It primarily differs for especially high-life monsters (such as The Shaper), where the threshold is reduced to allow ailments to be applied with hits that wouldn't ordinarily reach the required Life thresholds.”

**Supporting source:** [GGG balance manifesto](https://www.pathofexile.com/forum/view-thread/2686983)  
**Date:** 2019-12-10  
**Author:** Natalia_GGG / Grinding Gear Games.

> “For many monsters, the Ailment Threshold and the monster's life will be the same, but very high health targets like map bosses and end-game bosses will now have a significantly lower Ailment Threshold than they do life. This should make shocking or chilling the Shaper much easier, as you'll be applying the effect as if they had approximately half the life they have now.”

**Condition:** “approximately half” is an example for the Shaper, not a universal boss multiplier.

### 3.9.2, Metamorph
**Source:** [GGG 3.9.2 Patch Notes](https://www.pathofexile.com/forum/view-thread/2735273)  
**Date:** 2020-01-08  
**Author:** Natalia_GGG / Grinding Gear Games.

> “Fixed a bug which caused Metamorph bosses to become unfreezable. They can once again be frozen, however they have a higher ailment threshold relative to map bosses with similar amounts of Life.”

**Condition:** Metamorph bosses. No numeric value is stated.

### 3.15.0, Expedition
**Source:** [GGG, Game Balance in Path of Exile: Expedition](https://www.pathofexile.com/forum/view-thread/3147157)  
**Date:** 2021-07-20  
**Author:** Community_Team / Grinding Gear Games.

> “We've also lowered the Ailment Threshold of particularly tough endgame encounters so that Chill or Shock investment is worthwhile on these encounters. Their threshold is now only slightly higher than regular map bosses.”

**Condition:** “particularly tough endgame encounters.” Named encounters and exact numeric values are not stated.

### 3.16.0, Scourge
**Source:** [GGG 3.16.0 Patch Notes](https://www.pathofexile.com/forum/view-thread/3186390#uniquemapbossailmentthreshold)  
**Date:** 2021-10-14  
**Author:** no author is stated on the patch-note post.

> “Lowered the Ailment Thresholds of the Putrid Cloister, Vinktar Square, Doryani’s Machinarium, and Hallowed Ground Unique Bosses (as they were too far above other Bosses on a fully Watchstoned Atlas).”

**Condition:** only those four Unique Map bosses; comparator is “other Bosses on a fully Watchstoned Atlas.” No numeric values are stated.

**What it says:** 3.9 introduced separate monster ailment thresholds and reduced high-life-boss thresholds; 3.15 reduced thresholds again for unnamed tough endgame encounters; 3.16 specifically reduced four Unique Map bosses. No further relevant PoE 1 3.x official patch-note or manifesto change was found in the searched corpus.

## Final Reference Table

| Boss | Version | Monster level | Life | Ailment threshold | Source URL |
|---|---|---:|---:|---:|---|
| The Shaper | Normal | 84 | 75,193,704; 2560% | 6,957,767; 504% | [PoEDB](https://poedb.tw/us/The_Shaper) |
| The Shaper | Uber, arena level 85 | 85 arena | Not published separately | Not published separately | [Cosmic Fragment](https://poedb.tw/us/Cosmic_Fragment) |
| The Elder | Normal | 83 | 47,135,222; 1860% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/The_Elder) |
| Uber Elder, Shaper | Normal combined encounter | 84 | 48,405,947; 1648% | 6,957,767; 504% | [PoEDB](https://poedb.tw/us/The_Shaper) |
| Uber Elder, Elder | Normal combined encounter | 84 | 48,405,947; 1648% | 6,957,767; 504% | [PoEDB](https://poedb.tw/us/The_Elder) |
| Uber Elder, Shaper + Elder | Level-85 fragment arena | 85 arena | Not published separately | Not published separately | [Decaying Fragment](https://poedb.tw/us/Decaying_Fragment) |
| Sirus | Normal | 84 | 70,494,097; 2400% | 6,957,767; 504% | [PoEDB](https://poedb.tw/us/Sirus%2C_Awakener_of_Worlds) |
| Sirus | Uber, arena level 85 | 85 arena | Not published separately | Not published separately | [Awakening Fragment](https://poedb.tw/us/Awakening_Fragment) |
| The Maven | Normal | 84 | 51,548,809; 1755% | 6,957,767; 504% | [PoEDB](https://poedb.tw/us/The_Maven) |
| The Maven | Uber, arena level 85 | 85 arena | Not published separately | Not published separately | [PoE Wiki](https://www.poewiki.net/wiki/The_Maven) |
| The Searing Exarch | Normal | 84 | 42,002,733; 1430% | 4,155,333; 301% | [PoEDB](https://poedb.tw/us/The_Searing_Exarch) |
| The Searing Exarch | Uber, arena level 85 | 85 arena | Not published separately | Not published separately | [Blazing Fragment](https://poedb.tw/us/Blazing_Fragment) |
| The Eater of Worlds | Normal | 84 | 41,121,557; 1400% | 4,058,698; 294% | [PoEDB](https://poedb.tw/us/The_Eater_of_Worlds) |
| The Eater of Worlds | Uber, arena level 85 | 85 arena | Not published separately | Not published separately | [Devouring Fragment](https://poedb.tw/us/Devouring_Fragment) |
| Incarnation of Fear | Normal | 83 | 50,683,034; 2000% | 9,528,410; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Fear) |
| Incarnation of Fear | Uber | 85 | 45,063,462; 1440% | 11,766,571; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Fear) |
| Incarnation of Dread | Normal | 83 | 50,683,034; 2000% | 9,528,410; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Dread) |
| Incarnation of Dread | Uber | 85 | 45,063,462; 1440% | 11,766,571; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Dread) |
| Incarnation of Neglect | Normal | 83 | 50,683,034; 2000% | 9,528,410; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Neglect) |
| Incarnation of Neglect | Uber | 85 | 45,063,462; 1440% | 11,766,571; 800% | [PoEDB](https://poedb.tw/us/Incarnation_of_Neglect) |
| Venarius | Normal, Cortex base record | 79 | 4,610,269; 400% | 2,212,929; 400% | [PoEDB](https://poedb.tw/us/Venarius) |
| Venarius | Uber, Memento Mori | 85 arena | Not published separately | Not published separately | [Memento Mori](https://poedb.tw/us/Memento_Mori) |
| Catarina, phase 1 | Normal | 83 | 23,770,343; 938% | 6,014,809; 505% | [PoEDB](https://poedb.tw/us/Catarina%2C_Master_of_Undeath) |
| Catarina, phase 2 | Normal | 83 | 36,111,662; 1425% | 6,014,809; 505% | [PoEDB](https://poedb.tw/us/Catarina%2C_Master_of_Undeath) |
| Kitava | Act 5 | 45 | 99,000; 7200% | 41,250; 3000% | [PoEDB](https://poedb.tw/us/Kitava%2C_the_Insatiable) |
| Kitava | Act 10 | 67 | 326,077; 5500% | 177,860; 3000% | [PoEDB](https://poedb.tw/us/Kitava%2C_the_Insatiable) |
| Guardian of the Minotaur | Normal, T16 / area 83 | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Guardian_of_the_Minotaur#GuardianoftheMinotaurMinotaurBoss) |
| Guardian of the Hydra | Normal, T16 / area 83 | 83 | 25,341,517; 1000% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Guardian_of_the_Hydra#GuardianoftheHydraHydraBoss) |
| Guardian of the Chimera | Normal, T16 / area 83 | 83 | 25,341,517; 1000% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Guardian_of_the_Chimera#GuardianoftheChimeraChimeraBoss) |
| Guardian of the Phoenix | Normal, T16 / area 83 | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Guardian_of_the_Phoenix#GuardianofthePhoenixPhoenixBoss) |
| Al-Hezmin | Normal | 68 | 1,811,503; 1300% | 442,453; 504% | [PoEDB](https://poedb.tw/us/Al-Hezmin%2C_The_Hunter#Al-HezminTheHunterAtlasExile3Apparition) |
| Al-Hezmin | PoEDB `Uber` record | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Al-Hezmin%2C_The_Hunter#Al-HezminTheHunterAtlasExile3ApparitionUber) |
| Baran | Normal | 68 | 1,811,503; 1300% | 442,453; 504% | [PoEDB](https://poedb.tw/us/Baran%2C_The_Crusader#BaranTheCrusaderAtlasExile1Apparition) |
| Baran | PoEDB `Uber` record | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Baran%2C_The_Crusader#BaranTheCrusaderAtlasExile1ApparitionUber) |
| Drox | Normal | 68 | 1,811,503; 1300% | 442,453; 504% | [PoEDB](https://poedb.tw/us/Drox%2C_The_Warlord#DroxTheWarlordAtlasExile4Apparition) |
| Drox | PoEDB `Uber` record | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Drox%2C_The_Warlord#DroxTheWarlordAtlasExile4ApparitionUber) |
| Veritania | Normal | 68 | 1,811,503; 1300% | 442,453; 504% | [PoEDB](https://poedb.tw/us/Veritania%2C_The_Redeemer#VeritaniaTheRedeemerAtlasExile2Apparition) |
| Veritania | PoEDB `Uber` record | 83 | 32,943,972; 1300% | 6,002,899; 504% | [PoEDB](https://poedb.tw/us/Veritania%2C_The_Redeemer#VeritaniaTheRedeemerAtlasExile2ApparitionUber) |
| The Black Star | Normal, area 83 | 83 | 35,478,124; 1400% | 3,501,691; 294% | [PoEDB](https://poedb.tw/us/The_Black_Star#TheBlackStarBlackStarBoss) |
| The Infinite Hunger | Normal, area 83 | 83 | 45,614,731; 1800% | 4,525,995; 380% | [PoEDB](https://poedb.tw/us/The_Infinite_Hunger#TheInfiniteHungerDoomBoss_) |
| The Purifier | Normal, area 82 | 82 | 25,112,725; 1200% | 4,957,252; 504% | [PoEDB](https://poedb.tw/us/The_Purifier#ThePurifierElderGuardian4_) |
| The Constrictor | Normal, area 82 | 82 | 25,112,725; 1200% | 4,957,252; 504% | [PoEDB](https://poedb.tw/us/The_Constrictor#TheConstrictorElderGuardian3) |
| The Eradicator | Normal, area 82 | 82 | 25,112,725; 1200% | 4,957,252; 504% | [PoEDB](https://poedb.tw/us/The_Eradicator#TheEradicatorElderGuardian2) |
| The Enslaver | Normal, area 82 | 82 | 25,112,725; 1200% | 4,957,252; 504% | [PoEDB](https://poedb.tw/us/The_Enslaver#TheEnslaverElderGuardian1) |