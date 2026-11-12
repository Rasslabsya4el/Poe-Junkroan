# Zizaran league starters 3.25 - 3.29 — PoB collection

33 builds in `tests/fixtures/zizaran_325/` … `zizaran_329/`. The 3.29 league is written up
first; the four earlier leagues follow under "Previous leagues (3.25 - 3.28)".

## 3.29 Curse of the Allflame

Date: 2026-09-18. Data-collection only; no analysis of the gear beyond a rarity count.
Fixtures: `tests/fixtures/zizaran_329/` (5 `.pob.txt` import codes + `manifest.json`).

## Where the codes came from

Zizaran's 3.29 (Curse of the Allflame) starter list was assembled from
[his Maxroll author page](https://maxroll.gg/@zizaran) and
[poebuilds.cc/poe1/author/zizaran](https://www.poebuilds.cc/poe1/author/zizaran?league=allflame),
cross-checked against the YouTube guide titles.

Two fetch routes worked, neither blocked:

- `https://pobb.in/<id>/raw` — HTTP 200, plain `eNrt...` import code.
- `https://planners.maxroll.gg/profiles/poe/<id>` — HTTP 200 JSON. A Maxroll **planner**
  id (`/poe/planner/<id>`) returns Maxroll's own planner format (no PoB code) but carries a
  `pobLinks` array pointing at a Maxroll **pob** id; `/poe/pob/<id>` returns
  `data = {"pobCode": "eNrt..."}`, which is the verbatim PoB import code.
  So: guide page -> planner id -> `pobLinks[].link` -> pob id -> code.

`https://assets-ng.maxroll.gg/poe/planner/<id>` is a 404 (SPA shell); do not use it.

## Builds

| # | Build | Class / Ascendancy | Main skill | PoB source | Saved as |
|---|---|---|---|---|---|
| 1 | Earthquake Gladiator League Starter | Duelist / Gladiator | Earthquake | [pobb.in/CQjwpiUqHfs1](https://pobb.in/CQjwpiUqHfs1) | `gladiator_earthquake.pob.txt` |
| 2 | Explosive Arrow Ballista Champion League Starter | Duelist / Champion | Explosive Arrow (Ballista Totem) | [pobb.in/SS4brAQOXXM9](https://pobb.in/SS4brAQOXXM9) | `champion_explosive_arrow.pob.txt` |
| 3 | Boneshatter Juggernaut League Starter | Marauder / Juggernaut | Boneshatter of Complex Trauma | [maxroll.gg/poe/pob/tcjqpe0t](https://maxroll.gg/poe/pob/tcjqpe0t) | `juggernaut_boneshatter.pob.txt` |
| 4 | Winter Orb Elementalist League Starter | Witch / Elementalist | Winter Orb | [maxroll.gg/poe/pob/p9jndn0t](https://maxroll.gg/poe/pob/p9jndn0t) | `elementalist_winter_orb.pob.txt` |
| 5 | Essence Drain / Contagion Occultist (Goratha, featured by Ziz) | Witch / Occultist | Essence Drain (+ Contagion / Bane) | [maxroll.gg/poe/pob/m5ui4t0x](https://maxroll.gg/poe/pob/m5ui4t0x) | `occultist_essence_drain.pob.txt` |
| — | Luminary Mercenary Support Build | **not a classic class** | aura / Mercenary support | [pobb.in/AwKOubsBxjUi](https://pobb.in/AwKOubsBxjUi) | **not saved** |

All five saved codes decode with `junkroan.pob.session.decode_import_code`.

Maxroll guide URLs (where one exists): Earthquake
`https://maxroll.gg/poe/build-guides/earthquake-gladiator-league-starter`, Explosive Arrow
`https://maxroll.gg/poe/build-guides/explosive-arrow-ballista-champion-league-starter`,
Boneshatter `https://maxroll.gg/poe/build-guides/boneshatter-juggernaut-league-starter`,
Essence Drain planner `https://maxroll.gg/poe/planner/f9mek30t`. Winter Orb has no Maxroll
guide page — its PoB is a bare Maxroll pob upload linked from the video/poebuilds.cc.

### Excluded: Luminary Mercenary Support

Skipped per the task. The PoB fetches fine (HTTP 200) but decodes with
`className="Scion" ascendClassName="None"` — no ascendancy at all — and its tree specs and
item sets are organised around the new 3.29 Mercenary system
(`'^1Endgame Mercenary Gear {6}'`, `'Mercenary Gear - Early {7}'`, …). Not a usable
classic-class fixture; not saved.

### Notes on sources

- Essence Drain is Goratha's build featured in Zizaran's guide series (the Maxroll planner
  records `author.contentCreator = "goratha"`). Included because it sits in Ziz's 3.29
  starter list; flagged in `manifest.json`.
- Two PoBs exist for Essence Drain. `pobb.in/PfrGHW7YkQqU` (from the video description,
  tree version `3_28`, 7 loadouts) and the Maxroll one `m5ui4t0x` (tree `3_29`, dated
  2026-08-01, same 7 loadouts plus an `ALTERNATIVE SETUP`). The newer Maxroll version is
  the one saved.
- Earthquake and Explosive Arrow Maxroll planners carry no `pobLinks`, so pobb.in is the
  only PoB source for those two.
- Tree versions: builds 1–4 are saved on tree `3_28`, build 5 on `3_29`.

## Loadout naming

He does not use one fixed vocabulary. Three patterns show up.

**Pattern A — explicit stage names with `{n}` markers** (Boneshatter, Winter Orb, and
partly Earthquake). The item set, tree spec and skill set that belong together carry the
same `{n}` number in their titles; `^2` / `^4` prefixes are just PoB colour codes. Stage
names: `Early Game` -> `Midgame` -> `Endgame` (+ endgame variants such as
`Endgame - Corrupted Soul`, `Endgame - Cluster`, `Endgame - Suppress`).

**Pattern B — level-banded leveling sets plus unnumbered stage sets** (Earthquake,
Explosive Arrow). The tree specs are `Level 12`, `Level 23`, … `Level 68 - Merc Lab`, with
separator rows like `^2LEVELING` and `----ENDGAME----`; item sets are
`Level 13 example` / `Early Game` / `Midgame {1}` / `Endgame {2,4}`. Here the `Early Game`
item set has **no** `{n}` marker, so its tree/skill pairing is inferred, not stated.

**Pattern C — gear-milestone names, no stage words at all** (Essence Drain). Item set,
spec and skill set share identical titles: `Level 1-12`, `Level 12-28`, `Slinger 28+`,
`Early Cane of Unravelling`, `CI Cane of Unravelling`, `Wands`, `Big Staff`. The
"day 1 / early maps" stage here is `Slinger 28+`.

Full title lists per build are in `manifest.json` under `loadouts`.

## Early loadouts chosen

| Build | item set | tree spec | skill set | level | link |
|---|---|---|---|---|---|
| Earthquake Gladiator | `Early Game` | `Level 68 - Merc Lab (Swap to 1H)` (99 nodes) | `Maps {1,2,3}` | 68 | inferred |
| Explosive Arrow Champion | `Early Game` | `Level 69 - Merciless Lab` (99 nodes) | `Level 38+` | 69 | inferred |
| Boneshatter Juggernaut | `^4Early Game {1}` | `^4Early Game {1}` (114 nodes) | `^4Early Game {1}` | ~81 (est.) | author `{1}` |
| Winter Orb Elementalist | `Early Game {4}` | `Level 80 - Uber Lab {4}` (113 nodes) | `Early Game {4}` | 80 | author `{4}` |
| Essence Drain Occultist | `Slinger 28+` | `Slinger 28+` (99 nodes) | `Slinger 28+` | ~68 (est.) | identical titles |

"inferred" = the item set carries no `{n}`; the spec is the last leveling spec before the
first `Midgame`/`Endgame` tree, the skill set the first maps-stage gem set. Estimated
levels come from `allocated nodes - 33` (start node + 8 ascendancy + 24 quest points),
a formula that reproduces the levels he states in the titles he does label.

## Early loadout: rare vs unique per slot

R = rare, U = unique, `-` = slot empty in that item set.

| slot | Earthquake | Expl. Arrow | Boneshatter | Winter Orb | Essence Drain |
|---|---|---|---|---|---|
| Weapon 1 | R | R | R | R | R |
| Weapon 2 | R | R | – (2H) | R | R |
| Helmet | R | R | R | R | **U** Honourhome |
| Body Armour | R | R | R | R | R |
| Gloves | R | R | R | R | **U** Allelopathy |
| Boots | R | R | R | R | R |
| Belt | R | R | R | R | R |
| Amulet | R | R | R | R | R |
| Ring 1 | R | R | **U** Kaom's Sign | R | R |
| Ring 2 | R | R | R | R | R |
| **rare / unique** | **10 / 0** | **10 / 0** | **8 / 1** | **10 / 0** | **8 / 2** |
| flasks | 5 magic | 5 magic | 5 magic | 5 magic | none in set |

The rare pieces in builds 1–4 are placeholder rares the author wrote by hand — they are
literally named `Early Game Axe`, `Early Game Ring`, `Early Game Chest` and so on. The
Essence Drain early set names its rares `New Item`. Flasks, where present, are all magic
with crafted suffixes.

Gear statistics beyond this rarity count are deliberately out of scope here.

---

# Previous leagues (3.25 - 3.28)

Collected 2026-09-18 into `tests/fixtures/zizaran_325/`, `_326/`, `_327/`, `_328/`, each with the
same `manifest.json` shape as 3.29 plus `league` and `tree_versions` fields.

| league | builds saved | tree versions | not saved |
|---|---|---|---|
| 3.25 Settlers of Kalguur | 7 | `3_25` | — |
| 3.26 Secrets of the Atlas | 8 | `3_26` | — |
| 3.27 Keepers of the Flame | 9 | `3_26` | 2 PoBs (links re-saved for 3.29) |
| 3.28 Mirage | 4 | `3_27`, `3_28` | the Summoner Necromancer (all 4 links re-saved for 3.29) |
| 3.29 Curse of the Allflame | 5 | `3_28`, `3_29` | Luminary Mercenary (not a classic class) |

## How the older guides were found

Maxroll keeps **one** guide page per build and updates it in place, so the live page always shows
the current patch. The per-patch PoB is instead reachable from the **YouTube guide video of that
league**, whose description carries the link the author used at the time. Route used:

1. `https://www.poebuilds.cc/poe1/author/zizaran?league=<slug>` (`settlers`, `secrets`, `keepers`,
   `mirage`) for a first list, then `https://www.youtube.com/results?search_query=…` parsed for
   `videoId`/`title` pairs to fill the gaps. poebuilds.cc lists no 3.25 builds at all and
   mis-files at least one 3.27 video (Storm Burst) under 3.28, so the video list is the
   authority, checked against `ownerChannelName` = `Zizaran` and `publishDate`.
2. The watch page's `"shortDescription"` JSON field holds the links; `pobb.in/<id>/raw`,
   `pobb.in/u/<user>/<slug>/raw` and `planners.maxroll.gg/profiles/poe/<id>` then give the code.

**pobb.in rate-limits**: about 15 raw fetches in quick succession, then HTTP 429 with the body
`rate limited`. A 10 s gap between requests, with backoff on 429, fetches everything; all
originally-429 URLs succeeded on the throttled retry. Nothing else was blocked.

## Two traps in dating a fetched PoB

**Tree version lags the league.** `<Spec treeVersion=…>` records the passive-tree *data* version,
which only bumps when GGG changes the tree. Every 3.27 PoB collected here is on tree `3_26`, and
most 3.28 PoBs on `3_27`. So tree version alone cannot date a build; it is recorded per build in
each manifest and is only used here to detect the second trap.

**Links that were re-saved in place.** A Maxroll pob id can be overwritten by its author, and then
the old video's link serves today's build. Four ids from the Necromancer guides do exactly this —
profile dates 2026-08-16 / 2026-08-30, i.e. after 3.29 launched, and `treeVersion` `3_29`:

| id | linked from | profile date | tree | verdict |
|---|---|---|---|---|
| `54yj0yga` | 3.27 Spectres, 3.28 Summoner | 2026-08-30 | `3_29` | re-saved, not saved as 3.27/3.28 |
| `8r1afp0g` | 3.27 Spectres, 3.28 Summoner | 2026-08-16 | `3_29` | re-saved, not saved as 3.27/3.28 |
| `gm7x80au` | 3.28 Summoner | 2026-08-30 | `3_29` | re-saved, not saved |
| `5ny70a8p` | 3.28 Summoner | 2026-08-30 | `3_29` | re-saved, not saved |
| `t11sg0yu` | 3.27 Spectres | 2025-11-01 | `3_26` | genuine 3.27, **saved** |
| `6kaoo0ce` | 3.28 Boneshatter | 2026-03-06 | `3_28` | genuine 3.28, **saved** |

Consequence: the **3.28 Summoner Necromancer has no recoverable PoB** and is not in the fixture
set. The 3.27 Spectre build survives through `t11sg0yu` only.

A softer version of the same problem affects three 3.26 links, which are *named aliases* under the
author's own pobb.in profile (`pobb.in/u/zizaran%236796/lc-elementalist`, `…/woc-elementalist`,
`…/eq-glad`) rather than immutable ids. They serve tree-`3_26` content that differs from the
dedicated 3.27 codes, which is consistent with them still holding the 3.26 build, but pobb.in
exposes no version history, so this cannot be proved. Saved, with the caveat recorded here.

## 3.25 Settlers of Kalguur — 7 builds

All seven codes come from pobb.in ids in the video descriptions and all are on tree `3_25`.

| build | class / ascendancy | main skill | early item set | lvl | R | U | M | empty | uniques |
|---|---|---|---|---|---|---|---|---|---|
| `hierophant_ice_nova_archmage` | Templar / Hierophant | Ice Nova of Frostbolts (Archmage) | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |
| `gladiator_lacerate` | Duelist / Gladiator | Lacerate of Haemorrhage | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |
| `slayer_ground_slam` | Duelist / Slayer | Vaal Ground Slam of Earthshaking | `Basic gear (Blood magic)` | ~61 | 6 | 3 | 0 | 1 | Hinekora's Sight, Kaom's Sign ×2 |
| `gladiator_eviscerate_retaliate` | Duelist / Gladiator | Sunder / Eviscerate (ft. Goratha) | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |
| `berserker_ground_slam_autocry` | Marauder / Berserker | Ground Slam of Earthshaking | `Early Game {5}` | ~85 | 9 | 0 | 0 | 1 | — |
| `gladiator_spectral_shield_throw` | Duelist / Gladiator | Spectral Shield Throw | `Early {3}` | 74 | 9 | 1 | 0 | 0 | Kaom's Sign |
| `champion_explosive_arrow` | Duelist / Champion | Explosive Arrow (Ballista Totem) | `Early Game` | 69 | 10 | 0 | 0 | 0 | — |

Loadout naming: pattern B dominates — level-banded leveling specs (`Level 12` … `Level 68 - Merc
Lab`) under a `^2LEVELING` / `^2MAPS` separator, with unnumbered `Early Game` / `Midgame` /
`Endgame` / `Minmax` item sets. Two builds deviate: `slayer_ground_slam` names its sets after the
*mana lane* (`Basic gear (Blood magic)` / `Early endgame (Blood Magic)` / `… (Automation)` /
`Super endgame (Automation)`), and `gladiator_spectral_shield_throw` uses `{n}` markers with
`Early {3}` / `Midgame {2,4}` / `MinMax {1}`. `gladiator_eviscerate_retaliate` carries a second
whole leveling lane under `^4RETALIATION LEVELING (NOT A BAIT XD)`.

## 3.26 Secrets of the Atlas — 8 builds

| build | class / ascendancy | main skill | early item set | lvl | R | U | M | empty | uniques |
|---|---|---|---|---|---|---|---|---|---|
| `trickster_blight_of_contagion` | Shadow / Trickster | Blight of Contagion | `Maps {2}` | ~97 | 10 | 0 | 0 | 0 | — |
| `chieftain_righteous_fire` | Marauder / Chieftain | Righteous Fire (w/ Pohx) | `^8Level 61-80 {4}` | 80 | 10 | 0 | 0 | 0 | — |
| `berserker_volcanic_fissure` | Marauder / Berserker | Volcanic Fissure of Snaking (w/ imExile) | `fresh maps` | ~64 | 7 | 1 | 1 | 1 | Carnage Heart |
| `necromancer_zombie_army_early` | Witch / Necromancer | Raise Zombie (minion army, w/ Helm Breaker) | `^2Early 6L Rare {1}` | 92 | 8 | 2 | 0 | 0 | Darkness Enthroned, Bones of Ullr |
| `necromancer_zombie_army_late` | Witch / Necromancer | Raise Zombie (minion army) | — late-game companion PoB, no early stage | — | | | | | |
| `elementalist_lightning_conduit` | Witch / Elementalist | Lightning Conduit | `Early Game {4}` | ~85 | 9 | 1 | 0 | 0 | Berek's Grip |
| `elementalist_wave_of_conviction` | Witch / Elementalist | Wave of Conviction | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |
| `gladiator_earthquake` | Duelist / Gladiator | Earthquake | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |

Loadout naming: the most varied league of the four. Zizaran's own three builds keep patterns A/B
(`Early Game {4}` / `Midgame {3}` / `Endgame {1}`, or level-banded specs with unnumbered stage item
sets). The guest builds each bring their own vocabulary: Pohx's Righteous Fire is banded purely by
level with `{1}`…`{10}` markers (`^4Level 1-20 {1}` … `Lvl 90 Cogwork + Kalandra {10}`); imExile's
Berserker writes lowercase free text (`fresh maps`, `midgame`, `endgame`, a row of dashes as a
separator, then a second `fissure` lane); Helm Breaker's Necromancer uses
`Early` / `Mid` / `Late` prefixed by PoB colour codes with a separate PoB for the late game.
`trickster_blight_of_contagion` has no early-maps set at all — its only maps set is `Maps {2}`,
which is why its "early" row reads level ~97.

Note: `chieftain_righteous_fire` decodes with `ascendClassName="None"` because its *active* spec is
the level 1-20 one; every later spec carries `classId=1 ascendClassId=3` (Marauder / Chieftain).
Both values are recorded in the manifest (`ascendancy` vs `ascendancy_in_pob`).

## 3.27 Keepers of the Flame — 9 builds

| build | class / ascendancy | main skill | early item set | lvl | R | U | M | empty | uniques |
|---|---|---|---|---|---|---|---|---|---|
| `champion_explosive_arrow` | Duelist / Champion | Explosive Arrow (Ballista Totem) | `Early Game` | 69 | 10 | 0 | 0 | 0 | — |
| `elementalist_lightning_conduit` | Witch / Elementalist | Lightning Conduit | `Early Game {4}` | ~85 | 9 | 1 | 0 | 0 | Berek's Grip |
| `gladiator_earthquake` | Duelist / Gladiator | Earthquake | `Early Game` | 68 | 10 | 0 | 0 | 0 | — |
| `juggernaut_boneshatter` | Marauder / Juggernaut | Boneshatter of Complex Trauma | `^4Early Game {1}` | ~82 | 8 | 1 | 0 | 1 | Kaom's Sign |
| `slayer_earthshatter` | Duelist / Slayer | Earthshatter (ft. Carn) | `Basic gear {2}` | ~65 | 9 | 0 | 0 | 1 | — |
| `hierophant_storm_burst` | Templar / Hierophant | Storm Burst (Spell Totem, ft. Oscrix) | `Early Maps {1}` | ~66 | 9 | 0 | 1 | 0 | — |
| `assassin_poison_spark` | Shadow / Assassin | Spark of the Nova, poison (ft. Goratha) | `Poison Spark Maps (Reverse Chill)` | ~87 | 5 | 5 | 0 | 0 | Asenath's Gentle Touch, Whispers of Infinity, Apep's Slumber, Icefang Orbit, Winterweave |
| `assassin_poison_cremation` | Shadow / Assassin | Cremation of the Volcano | — second PoB from the same video, one untitled set | — | | | | | |
| `necromancer_raise_spectre` | Witch / Necromancer | Raise Spectre (ft. Helm Breaker) | `^2Early 6L Rare {1}` | 92 | 8 | 2 | 0 | 0 | Bones of Ullr, Darkness Enthroned |

Loadout naming: Zizaran's own four builds are the 3.29 vocabulary already — `Early Game` /
`Midgame` / `Endgame` with `{n}` markers where he bothered. The guests differ: Carn's Slayer names
item sets after gear tier (`Leveling {1}`, `Basic gear {2}`, `Early endgame`, `Super endgame {3}`)
while its *specs* say `Early Maps {2}`, so the item set and spec names disagree for the same stage;
Oscrix's Hierophant is the cleanest of the whole collection (`Levelling {a,b,c,d}` / `Early Maps
{1}` / `Red Maps {2}` / `Endgame {3}`, with letter markers for leveling and digits for maps);
Goratha's Assassin names every set after the *skill and defence layer* it runs
(`Cobra Lash Act 1`, `Poison Concoction Act 2-10`, `Poison Spark Maps (Reverse Chill)`,
`Poison Spark Herald`, `Poison Spark MOM EB`, `Poison Spark Ward`) — there is no "early/mid/end"
axis at all.

`assassin_poison_spark` is the outlier of the whole collection for gear: 5 rares against 5 uniques
in its first maps set, where every other early set in 3.25-3.29 is 8-10 rares.

## 3.28 Mirage — 4 builds

| build | class / ascendancy | main skill | tree | early item set | lvl | R | U | M | empty | uniques |
|---|---|---|---|---|---|---|---|---|---|---|
| `champion_explosive_arrow` | Duelist / Champion | Explosive Arrow (Ballista Totem) | `3_27` | `Early Game` | 69 | 10 | 0 | 0 | 0 | — |
| `hierophant_kinetic_fusillade` | Templar / Hierophant | Kinetic Fusillade (Ballista Totem, w/ Palsteron) | `3_27` | `EarlyMaps` | ~90 | 9 | 1 | 0 | 0 | Doedre's Tenure |
| `hierophant_shock_nova_archmage` | Templar / Hierophant | Shock Nova (Archmage, ft. Goratha) | `3_27` | `Early Mapping` | ~81 | 7 | 3 | 0 | 0 | Mindspiral, Foulborn Kikazaru, Valako's Sign |
| `juggernaut_boneshatter` | Marauder / Juggernaut | Boneshatter of Complex Trauma | `3_28` | `^4Early Game {1}` | ~81 | 8 | 1 | 0 | 1 | Kaom's Sign |

Loadout naming: Palsteron's Hierophant names every set after the **act** it belongs to — `A1`, `A3`,
`A4BeforeRespec`, `A4AfterRespec`, `A5` … `A10`, `A10CritRespec`, then `EarlyMaps`, `BeforeAegis`,
`AegisRespec`, `Aspirational` — the finest-grained progression in the collection (16 tree specs).
Goratha's Shock Nova is the one naming trap: its item set called **`Early Game` is act 1**
(its spec allocates 31 nodes), and the first maps stage is `Early Mapping`; using the word "early"
as the selector would pick the wrong set here. Zizaran's own two are pattern A/B as in 3.29.

## Reading the early-item-set counts

R / U / M are the ten equipment slots only (weapon 1-2, helmet, body, gloves, boots, belt, amulet,
rings), counted by the `Rarity:` line of each item; `empty` is slots the author left unfilled
(usually a two-handed weapon leaving Weapon 2 empty). Abyssal jewels socketed into a belt appear
in the manifests as `Belt Abyssal Socket N` and are excluded from these counts. Flask counts are
in the manifests, not here.

The pattern across all five leagues: the day-1 / early-maps set is overwhelmingly **rares** — the
author writes placeholder rares named `Early Game Axe`, `Early Game Ring`, `New Item` and so on —
with uniques appearing only where a specific item *is* the build (Kaom's Sign for the Juggernaut
and slam builds, Darkness Enthroned + Bones of Ullr for the minion builds, Berek's Grip for
Lightning Conduit) or where the whole build is unique-driven (Goratha's Poison Spark, 5 uniques).


## What the benchmark makes of them (2026-09-18, D68)

31 early loadouts were extracted; `scripts/benchmark.py --set ziz` runs **26** of them. Five are
older copies of a build PoB reads identically -- an author re-publishes a guide unchanged and the
same build appears under several leagues -- and only the newest league's copy is a reference
(champion_explosive_arrow 327 = 328 = 329, elementalist_lightning_conduit 326 = 327,
gladiator_earthquake 326 = 327, juggernaut_boneshatter 328 = 329; z325 Explosive Arrow, z329
Earthquake and z327 Boneshatter are genuinely different builds and stay). The fixture files all
stay in place; the trimmed list is `ZIZ_REPUBLISHED` in `scripts/benchmark.py`.

Three ways a hand-written guide PoB differs from the Tuadh snapshots, all fixed the same day:

- the author sockets a **support first** in the main group and PoB's `mainActiveSkill` points past
  it (Raise Spectre behind Minion Damage, Shock Nova behind Archmage, Essence Drain behind
  Spellslinger + Contagion). Read as the main skill, the support scored two references 0;
- `ascendClassName="None"` with the **ascendancy allocated** (3.26 Righteous Fire Chieftain), now
  read back from the allocated node ids;
- **20/20 gems**. The benchmark writes the rails' 18/0 onto the author's build before it reads a
  number off it; that is -21.9% of CombinedDPS at the median of this set (-45.6% to +9.0%), against
  +0.0% on the Tuadh set, whose day-1 gems the rails were derived from.

## Sources

- [maxroll.gg/@zizaran](https://maxroll.gg/@zizaran)
- [poebuilds.cc — Zizaran, 3.29 Allflame](https://www.poebuilds.cc/poe1/author/zizaran?league=allflame)
- [Earthquake Gladiator League Starter (Maxroll)](https://maxroll.gg/poe/build-guides/earthquake-gladiator-league-starter)
- [Boneshatter Juggernaut League Starter (Maxroll)](https://maxroll.gg/poe/build-guides/boneshatter-juggernaut-league-starter)
- [Explosive Arrow Ballista Champion League Starter (Maxroll)](https://maxroll.gg/poe/build-guides/explosive-arrow-ballista-champion-league-starter)
- [Winter Orb Elementalist guide video](https://www.youtube.com/watch?v=OZypCJ-5Bog)
- [Boneshatter Juggernaut guide video](https://www.youtube.com/watch?v=ThANqlWYJ98)
- [Explosive Arrow Champion guide video](https://www.youtube.com/watch?v=bD7Bt0UmVlo)
- [Earthquake Gladiator guide video](https://www.youtube.com/watch?v=izLrG4YH3aE)
- [Essence Drain guide video](https://www.youtube.com/watch?v=0YnVnhYCzy8)
- [Luminary Mercenary Support guide video (excluded build)](https://www.youtube.com/watch?v=vq-ui0FGZxE)
- [poebuilds.cc — Zizaran, 3.25 / 3.26 / 3.27 / 3.28](https://www.poebuilds.cc/poe1/author/zizaran)
- 3.25 guide videos: [Ice Nova Archmage](https://www.youtube.com/watch?v=Kbu2hLKek18), [Lacerate Gladiator](https://www.youtube.com/watch?v=3KgSrJiTqoQ), [Ground Slam Slayer](https://www.youtube.com/watch?v=OWdT2nVYBgc), [Eviscerate & Retaliate Gladiator](https://www.youtube.com/watch?v=H3_bpfkWjlY), [Autocry Slammer Berserker](https://www.youtube.com/watch?v=CiMKUZJclcg), [Bleed SST Gladiator](https://www.youtube.com/watch?v=3mGPRKypl6k), [Explosive Arrow Champion](https://www.youtube.com/watch?v=OiYAdPeadXE)
- 3.26 guide videos: [Blight of Contagion Trickster](https://www.youtube.com/watch?v=W9i9i4NZkNA), [Righteous Fire w/ Pohx](https://www.youtube.com/watch?v=K2u4NQpixKM), [Earthshatter Berserker w/ imExile](https://www.youtube.com/watch?v=Apb4AbrLPM4), [Zoo Necromancer w/ Helm Breaker](https://www.youtube.com/watch?v=RLcDuszpBZ8), [Lightning Conduit Elementalist](https://www.youtube.com/watch?v=w3dybIb6rIQ), [Wave of Conviction Elementalist](https://www.youtube.com/watch?v=mgHlvAyG5mA), [Bleed Earthquake Gladiator](https://www.youtube.com/watch?v=I3fGEt9RgKo)
- 3.27 guide videos: [Explosive Arrow Champion](https://www.youtube.com/watch?v=C2LY2sUDfSg), [Lightning Conduit Elementalist](https://www.youtube.com/watch?v=Oh7iDXT_utQ), [Earthquake Gladiator](https://www.youtube.com/watch?v=tSplX1-s-pE), [Bleed Boneshatter Juggernaut](https://www.youtube.com/watch?v=UXPVNIB9mD4), [Earthshatter Slayer ft. Carn](https://www.youtube.com/watch?v=Snwz9rVqSIE), [Storm Burst Totems ft. Oscrix](https://www.youtube.com/watch?v=WTBQFdkdi3M), [Poison Spark Assassin ft. Goratha](https://www.youtube.com/watch?v=KMxa__PnuMs), [Spectres Summoner ft. Helm Breaker](https://www.youtube.com/watch?v=esvfGNythhY)
- 3.28 guide videos: [Explosive Arrow](https://www.youtube.com/watch?v=VNrQ01QjNGE), [Kinetic Fusillade Totems w/ Palsteron](https://www.youtube.com/watch?v=1sbXGxCGw9Y), [Shock Nova Archmage ft. Goratha](https://www.youtube.com/watch?v=UzdZpUlR7Ss), [Boneshatter Juggernaut](https://www.youtube.com/watch?v=D79KG-lJoWU), [Summoner Necromancer ft. Helmbreaker (no recoverable PoB)](https://www.youtube.com/watch?v=_uWHZVHhY6A)
