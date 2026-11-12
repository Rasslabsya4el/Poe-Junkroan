# PoB version audit: release currency, tree versions inside builds, bump risk (2026-09-18)

Read-only audit. No code changed. One PoB session used (three fixture loads).
Sources: the GitHub releases API, `vendor/pob/source` at the pinned tag, `locks/*.json`,
`src/junkroan/pob/`, `src/junkroan/optimizer/tree_graph.py`, the 37 reference fixtures.

---

## 1. Version currency: the pin is the latest release

`locks/pob.lock.json` pins **v2.67.2**, published 2026-08-07.
The GitHub releases list (newest first) is:

| tag | published | prerelease |
|---|---|---|
| **v2.67.2** | 2026-08-07 | no |
| v2.67.1 | 2026-08-06 | no |
| v2.67.0 | 2026-08-05 | no |
| v2.66.2 | 2026-07-25 | no |
| v2.66.0 | 2026-07-25 | no |

**There is no release after v2.67.2.** We are on the newest published build; there is nothing
to bump to. `locks/pob.source.lock.json` pins the same tag
(`refs/tags/v2.67.2`, commit `b32759ab`), and `src/junkroan/pob/corpus_data/manifest.json`
records that same commit with `tree_version = 3_29`, so lock, source clone and corpora agree.

One line each for the three releases of the 3.29 cycle (these are *before* our pin, i.e. all
already in it):

- **v2.67.0** (2026-08-05) — the 3.29 update: new Abyss Timeless Jewels, new uniques, Pacts,
  stat-parsing improvements, Brand DPS auto-calculation, per-item-mod toggling, OAuth2
  character import, plus many calc corrections.
- **v2.67.1** (2026-08-06) — trader pseudo-stats; crash fixes (double-click on small windows,
  equipping quivers/shields that grant skills); calc fixes for Chip Away, Foulgrasp support
  and block-chance interactions.
- **v2.67.2** (2026-08-07) — our pin: Scornful Herald not counting buffs as affecting you;
  The Unblinking Eye evasion not applying to attacks with Arcane Might; Linux icon and
  item drag/double-click fixes.

**What *is* missing is unreleased work.** The `dev` branch has ~40 days of commits since our
tag, through 2026-09-08, several of them real calc corrections that would move our numbers:
Iron Grip double-dipping spell-damage conversion for projectile attacks, Nightblade support
with Windburst, Pact of Beidat not affecting hit-based spells, Consecrated Ground not reducing
curse effect, Mana-infused Staff reservation, Conjoined Spire totem life, invalid mod parsing
for skill-granting mods, plus features (Blood Shrines, pantheon aspect skills, auto-socketing
timeless jewels). None of it is in a release, so **the correct action is to stay on v2.67.2
and re-check the releases page weekly**, not to track `dev`.

**3.29 content is present in the pin.** `TreeData/3_29/tree.lua` carries the new ascendancy
**Luminary** (18 nodes, the Mercenary/Link tree, a Scion ascendancy) and the new bloodline
pools **Abyssal** (11) and **Brinerot** (7); `corpus_data/ascendancies.json` has all 37.
Caveat below (§5).

---

## 2. Tree versions inside builds

### 2a. What the fixtures carry

Counted by decoding every fixture with `junkroan.pob.session.decode_import_code` and reading
each `<Spec treeVersion=…>`:

| treeVersion | `<Spec>` elements | fixture files |
|---|---|---|
| 3_25 | 2 | `arc_archmage`, `spectral_shield_throw` |
| 3_26 | 5 | `lightning_trap`, `soulrend_chaos_dot`, `static_strike`, `summon_raging_spirits`, `toxic_rain` |
| 3_27 | 13 | `archmage_volatile_dead`, `bleed_bow`, `bleed_perforate`, `burning_arrow_snipe`, `elemental_hit`, `exsanguinate_mines`, `impale_ballista`, `impale_cyclone`, `kinetic_bolt_wander`, `kinetic_fusillade`, `poison_spark`, `pyroclast_mine`, `vd_spellslinger` |
| 3_28 | 58 | 12 tuadh files + 4 zizaran files (the zizaran ones carry 10–12 loadout Specs each) |
| 3_29 | 8 | `zizaran_329/occultist_essence_drain` only |

**36 of the 37 reference builds are on a tree older than the game data we optimize against.**
Only one fixture (`occultist_essence_drain`) is actually 3.29.

### 2b. What PoB does with an old treeVersion (source, not guesswork)

- `src/Classes/TreeTab.lua:511` — `Load`: `new("PassiveSpec", self.build, node.attrib.treeVersion or defaultTreeVersion)`.
  The spec is constructed **at the version the XML declares**. If PoB does not know the
  version at all it refuses the build (`:507`, "Unknown Passive Tree Version") — it never
  silently upgrades.
- `src/Classes/PassiveSpec.lua:30` — `Init(treeVersion)` does `self.tree = main:LoadTree(treeVersion)`,
  and `main:LoadTree` (`src/Modules/Main.lua:315`) lazily builds a whole `PassiveTree` object
  from `src/TreeData/<version>/tree.lua`. **Every spec keeps its own tree object.**
- `src/Classes/PassiveSpec.lua:245` — `ImportFromNodeList(..., treeVersion)` re-Inits only when
  the caller passes a *different* version, and then sets `treeTab.showConvert` — i.e. it
  offers the UI button, it does not convert.
- `src/Classes/TreeTab.lua:588` — `ConvertToVersion` is the conversion, and it is reachable
  **only from the "Convert" / "Copy + Convert" buttons** (`:653`, `:657`) and
  `ConvertAllToVersion`. It builds a new spec at the target version and replays the old
  hash list onto it (`newSpec:RestoreUndoState(build.spec:CreateUndoState(), version)`);
  ids that no longer exist are simply dropped, and the popup warns that passives may have
  been de-allocated. There is **no name-based remapping**.

**Our worker never converts.** `headless_runtime_worker.py:3195` (`ensure_spec`) is the only
place a spec is created, and it copies the source spec's version:
`new('PassiveSpec', build, source_spec.treeVersion)`. Nothing in the worker or in
`headless_wrapper.lua` calls `ConvertToVersion` or references `latestTreeVersion`.

**Live confirmation** (one PoB session, `PobSession.load_import_code` → `export_xml` → `read_state`):

| fixture | declared | exported after a headless round trip | CombinedDPS |
|---|---|---|---|
| `arc_archmage` | 3_25 | **3_25** | 535,630 |
| `stormbrand` | 3_28 | **3_28** | 898,678 |
| `occultist_essence_drain` | 3_29 | **3_29** (all 8 Specs) | 2,141,187 |

So: **the old tree is kept, and PoB scores the build with that tree's node stats.**

Also worth recording: `read_state()["tree_state"]` contains **no tree-version field at all**
(`headless_runtime_worker.py:5423-5443`). The harness is blind to which tree a loaded build
is on. Every tool that wants to know has to parse the XML itself, as `scripts/fixture_stats.py`
and `scripts/reference_drift.py` do.

### 2c. Are node ids stable 3_25 → 3_29?

Parsed `tree.lua` for each version and diffed by node id:

| version | nodes | ids absent in 3_29 | same id, different name |
|---|---|---|---|
| 3_25 | 3142 | **0** | 44 |
| 3_26 | 3159 | **0** | 30 |
| 3_27 | 3287 | **0** | 21 |
| 3_28 | 3344 | **0** | 44 |
| 3_29 | 3396 | — | — |

**Ids are strictly additive: nothing was removed between 3.25 and 3.29.** A 3_25 hash list
therefore allocates in 3_29 without losing a single node — conversion would be lossless in
*count*. What is **not** stable is what an id *means*.

Per fixture, comparing the allocated ids' name and stat text on the fixture's own tree vs 3_29:

| | 3_25 | 3_26 | 3_27 | 3_28 |
|---|---|---|---|---|
| allocated nodes whose **stats** differ on 3_29 (sum over fixtures) | 14 | 18 | 62 | 124 |
| worst single fixture | `arc_archmage` 12 of 112 | `static_strike` 12 of 109 | `impale_cyclone` 11 of 106 | `shockwave_cyclone` 12 of 116 |
| fixtures with zero divergence | — | `lightning_trap`, `soulrend_chaos_dot` | `exsanguinate_mines`, `poison_spark`, `pyroclast_mine` | the 3 zizaran short specs |

Three kinds of change, in order of how much they matter:

1. **The 3.29 cost rework — a real mechanic swap.**
   `Attack Mana Cost` (42086): 3_28 `8% reduced Mana Cost of Attacks` → 3_29
   `15% increased Cost Efficiency of Attacks`. Same for `Dreamer`, `Righteous Decree`,
   `Spirit of War`, `Tireless`, `Cannibalistic Rite`, and every `Life and Reduced Cost` /
   `Mana and Reduced Mana Cost` node. Different stat, different magnitude, different stacking.
   Mana-hungry references (`arc_archmage`, `archmage_volatile_dead`, `vd_spellslinger`) sit
   squarely on these.
2. **Real stat replacements.**
   `Gravepact` (27308): 3_26 `30% increased Minion Accuracy Rating` + `6% chance to deal
   Double Damage` → 3_29 `+7% to Chaos Resistance` + `8% chance to deal Double Damage`.
   `Minion Damage and Accuracy` (23185/43133/54267): minion accuracy → `+3% to Chaos Resistance`.
   Two ascendancy notables were renamed outright: 258 `Elemancer` → `Bringer of Ruin`
   (Elementalist), 1945 `Noxious Strike` → `Mystical Infusion`.
3. **Cosmetic.** `Global Accuracy Rating` → `Accuracy Rating` (3.29 wording), and stat-line
   reordering. Most of the 3_26–3_28 counts above are this; PoB parses both spellings.

### 2d. Which of our data is tied to what

`src/junkroan/pob/corpus_data/manifest.json` records every family's source files:

| corpus family | source | pinned to |
|---|---|---|
| `passives` (2421), `keystones` (57), `masteries` (353), `ascendancies` (37) | `vendor/pob/source/src/TreeData/**3_29**/tree.lua` | **one tree version** |
| `items` (1106) | `src/Data/Bases/*.lua` | the release |
| `active_gems` (558), `support_gems` (263) | `src/Data/Gems.lua` | the release |
| `config_surfaces` (578) | `src/Modules/ConfigOptions.lua`, `ConfigVisibility.lua` | the release |
| `mod_data/` (mod_families, stat_families), `tag_data/` | derived from the game corpus above | inherits both |
| `corpus_data/unique_tiers.json` | the wiki, refreshed per league by hand | neither (D31) |

`TreeGraph.load()` (`src/junkroan/optimizer/tree_graph.py:63`) reads
`passives/keystones/masteries.json` plus `canonical_active_tree_corpus()`, so
`TreeGraph.tree_version == "3_29"` — asserted in `tests/test_tree_graph.py:20`. It holds 2831
nodes against tree.lua's 3396; the 565 missing are **ascendancy nodes**, which the graph
excludes on purpose (verified: every absent id has an `ascendancyName`). That is why a 3_29
build shows "20 allocated ids not in TreeGraph" — those are its ascendancy points, not a
version problem.

### 2e. The consequence nobody has measured

Generated builds start from `newBuild()` → PoB's `TreeTab` constructor
(`TreeTab.lua:32`, `new("PassiveSpec", build, latestTreeVersion)`) → **3_29**.
References keep 3_25–3_28. `scripts/benchmark.py` re-scores the author's build under our
conservative lane and derives the floors (`author_floors`: Life, TotalEHP, max-hit, resists)
**from the author's build on the author's tree**, then demands our 3_29 build clear them.

So "% of author" is a comparison **across two different passive trees**, and the floors are
set on the old one. This is a systematic, unquantified bias in the benchmark — small for the
3_28 references, largest for `arc_archmage` (3_25, archmage, 12 changed nodes) and the minion
references (`summon_raging_spirits`, `absolution_minions`: Gravepact and the minion-accuracy
nodes changed).

**The measurement to run** (not run here — one-session limit): for the 4–5 worst fixtures,
score the author's build twice, once as-is and once with the Spec's `treeVersion` rewritten to
`3_29` (ids are lossless, §2c), and record the delta in CombinedDPS / Life / TotalEHP.
If the delta is small everywhere, record it in `docs/DECISIONS.md` and move on; if it is not,
either convert the fixtures once or score both sides on the fixture's own tree.

---

## 3. Does switching tree version change anything but the tree?

**Almost nothing, and the one exception does not reach us.**

- **Per tree version** (`src/TreeData/<version>/`): `tree.lua` (nodes, groups, connections,
  masteries and their effects, classes and ascendancy layouts, start nodes) and `sprites.lua`.
  That is the whole per-version payload. `PassiveSpec:Init` (`PassiveSpec.lua:30-32`) rebuilds
  only `self.tree` and `self.nodes` from it.
- **The one global side effect**: `TreeTab:SetActiveSpec` calls
  `data.setJewelRadiiGlobally(curSpec.treeVersion)` (`TreeTab.lua:547`), and `main:LoadTree`
  does the same (`Main.lua:316/320`). `Data.lua:577` picks `data.jewelRadii["3_15"]` for
  versions ≤ 3.15 and `["3_16"]` for everything newer. Every version we use is ≥ 3.25, so the
  same table is selected either way — **no effect for us**. It is worth knowing that it is a
  *global*, not a per-spec value: with mixed-version specs in one build the last activated
  spec wins.
- **Per release, loaded once at startup and never keyed by tree version** — all of
  `src/Modules/Data.lua`: item bases (`Data/Bases/*`, `:1214`), uniques (`Data/Uniques/*`,
  `:1352`), gems (`Data/Gems`, `:1055`), active skills (`Data/Skills/*`, `:1018`),
  every mod pool (`Data/ModExplicit`, `ModCorrupted`, `ModJewel*`, `ModMaster`, …, `:647-664`),
  essences, bench/master crafts, costs, cluster jewels, minions, spectres, bosses, pantheons,
  and the timeless-jewel data (`Data/TimelessJewelData/*`, `:926-929`).
- Even the things a `PassiveTree` object *thinks* are its own are release-level:
  `PassiveTree.lua:56-57` loads `Data/TimelessJewelData/LegionPassives` and
  `Data/TattooPassives` into **every** tree object, whatever its version.
- The calc engine (`src/Modules/Calc*.lua`, `ModParser.lua`) has no tree-version branch at all.

**Answer for the user:** switching the tree version in the PoB app changes the passive tree and
nothing else. Items, uniques, gems, supports, mods, crafting and the whole calculation engine
come from the installed PoB release (`src/Data/`, `src/Modules/`) and are identical on every
tree. Concretely: a 3.25 tree loaded in PoB 2.67.2 still uses 3.29 gem values, 3.29 unique
rolls, 3.29 mod tiers and the 3.29 calc — only the node stats are the old ones.

---

## 4. Risk list

### If PoB is bumped

The coupling is much deeper than the lock file. In order of how loudly it would fail:

1. **`src/junkroan/pob/headless_wrapper.lua` monkey-patches PoB internals.** It replaces
   `CalcsTab:BuildOutput` and `CalcsTab:GetNodeCalculator`, installs its own
   `calcsTabClass.__index` to build the CALCS lane lazily, and wraps `calcs.perform` to publish
   an Elemental Overload witness out of `env.keystonesAdded` / `env.player.output`. It reaches
   `common.classes["CalcsTab"]`, `mainObject.main:SetMode`, `mainObject.main.modes["BUILD"]`,
   and the import tab's controls (`importCodeIn`, `importCodeMode`, `importCodeGo`,
   `importCodeValid`, `importCodeXML`, `importCodeDetail`). A refactor of CalcsTab or ImportTab
   breaks the harness, possibly *silently* (a replaced method that no longer matches upstream's
   contract still runs).
2. **The boot-time JIT guard reads `Launch.lua`.** `check_jit_guard` requires
   `jit.opt.start('maxtrace>=4000','maxmcode>=8192')` to have been applied and fails the boot
   otherwise (worth 2.4x on the trial loop). A release that changes those numbers refuses to
   start — by design, but it is a bump blocker.
3. **~55 PoB methods called from the worker's Lua strings.** Tree:
   `spec:AllocNode`, `DeallocNode`, `DeallocSingleNode`, `ResetNodes`, `SelectClass`,
   `SelectAscendClass`, `SelectSecondaryAscendClass`, `ImportFromNodeList`, `ReplaceNode`,
   `BuildAllDependsAndPaths`, `BuildClusterJewelGraphs`, `CountAllocNodes`,
   `AddMasteryEffectOptionsToNode`, `CreateUndoState`, `RestoreUndoState`,
   `spec.tree:ProcessStats`. Calcs: `calcsTab:GetMiscCalculator`, `BuildPower`,
   `treeTab:BuildPowerReportList`, `SetPowerCalc`, `SetActiveSpec`. Items:
   `itemsTab:AddItem`, `CreateDisplayItemFromRaw`, `SetDisplayItem`, `IsItemValidForSlot`,
   `NewItemSet`, `SetActiveItemSet`, `PopulateSlots`, `UpdateSockets`, `slot:SetSelItemId`,
   `item:BuildAndParseRaw`, `BuildRaw`, `Craft`, `GetModSpawnWeight`, `CheckModLineVariant`,
   `itemLib.applyRange`, `modLib.parseMod`. Skills/config: `skillsTab:NewSkillSet`,
   `SetActiveSkillSet`, `ProcessSocketGroup`, `ResetUndo` and four named UI controls
   (`defaultLevel`, `defaultQuality`, `showSupportGemTypes`, `sortGemsByDPSFieldControl`);
   `configTab:NewConfigSet`, `SetActiveConfigSet`, `GetDefaultState`, `BuildModList`.
   Plus globals `build:SaveDB('code')`, `build:RefreshStatList`, `runCallback('OnFrame')`,
   `new('PassiveSpec'|'Item')`, `data.itemBases`, `data.itemMods`, `data.masterMods`,
   `data.powerStatList`, `main.uniqueDB`.
   CLAUDE.md already flags this ("a bump can change signatures"); this is the list to check.
4. **Corpora must be regenerated and every sha256 in the three manifests changes.**
   `manifest.json` stores the size and sha256 of each vendor source file, so a bump invalidates
   the whole chain: game corpus → tag corpus → mod corpus.
5. **Every benchmark number moves.** `tests/fixtures/*/stats.json`, the author floors and the
   whole "% of author" history are release-relative. Any bump needs a full
   `scripts/fixture_stats.py` re-run and a re-baselined benchmark before a single optimizer
   conclusion carries over. The dev-branch fixes listed in §1 (Iron Grip, Nightblade,
   Consecrated Ground, Pact of Beidat) would each move specific references.
6. **Known-broken thing that a bump might or might not fix**: Warden (PoB id `Raider`) —
   `set_tree(ascendancy_nodes=…)` reports the nodes did not materialize, and the search skips
   Warden. Re-test on any bump.
7. **A new tree version arrives with the release.** `latestTreeVersion` would become 3_30,
   new builds would be created on it, and the whole tree corpus plus `TreeGraph` would move
   under the references — which stay where they are. Everything in §2 gets one league worse.

### If PoB is *not* bumped

- **Nothing from the releases page.** v2.67.2 is current; not bumping costs zero today.
- **Calc bugs stay.** The ~40 unreleased `dev` commits are real corrections we do not have:
  Iron Grip double-dipping spell-damage conversion for projectile attacks, Nightblade +
  Windburst, Pact of Beidat not affecting hit-based spells, Consecrated Ground not reducing
  curse effect, Mana-infused Staff reservation. Where a candidate build leans on one of these,
  PoB — our only judge — is wrong, and the optimizer will happily exploit the wrong number.
- **Game-side drift.** GGG hotfixes 3.29 without touching PoB's version string; the pinned
  data is a snapshot of 2026-08-07. Divergence is invisible from inside the harness.
- **Wiki-sourced data ages independently.** `corpus_data/unique_tiers.json` is per league and
  hand-refreshed (D31); it is not covered by either lock.

### Recommended (no action taken)

1. Check the releases page weekly; bump only on a release, never on `dev`.
2. Add the spec's `treeVersion` to `read_state()["tree_state"]` — one field, and the harness
   stops being blind to it.
3. Run the §2e measurement and record the verdict in `docs/DECISIONS.md`.
4. Measure, do not assume, the Luminary / Reliquarian exclusion (§5).

---

## 5. Side finding: the Luminary / Reliquarian exclusion is asserted, not measured

`src/junkroan/search/hypothesis.py:107` says:

> Trees PoB stores next to the player ascendancies that are not player ascendancies
> (their nodes change nothing on the player: Luminary / Reliquarian "Display" trees).
> `NOT_PLAYER_ASCENDANCIES = {"luminary", "reliquarian"}`

Against `TreeData/3_29/tree.lua` this is half right:

- **Luminary** — defensible. Its 18 nodes are Mercenary nodes ("Your Mercenary can equip
  Unique Amulets", "Your Mercenary and their Minions deal 15% increased Damage") and
  `ModParser.lua` contains the string "Mercenary" **zero times** — PoB does not model a
  mercenary, so those lines are numerically dead. Two lines would parse
  ("50% less Cost of Link Skills", "Link Skills have 10% increased Cast Speed").
- **Reliquarian** — the claim is wrong. Its 36 nodes carry full unique-item stat blocks that
  ModParser handles: `Kaom's Roots` = `+100 to maximum Life` / `Cannot be Knocked Back`;
  `Elevore` = `+25% chance to Suppress Spell Damage` / `25% chance to Avoid Elemental Ailments`;
  `The Apostate`, `Dawnbreaker`, `Arakaali's Fang`, `Femurs of the Saints`, and so on. It is
  also a live tree: GGG rotated four of its nodes between 3_28 and 3_29 (2768 `Tear of Purity`
  → `Melding of the Flesh`, 8081 `Replica Heartbreaker` → `The Sands of Time`, 8967
  `The Burden of Truth` → `Screams of the Desiccated`, 10108 `Scavenger` → `Reliquarian`).

Both are listed under Scion in `tree.lua`'s `classes` block, alongside Ascendant. Per the
project's own first principle, whether a Scion Reliquarian is worth searching is a question
for PoB, not for a comment. The cheap check: build one Scion skeleton with
`ascendancy_id = "Reliquarian"` and read CombinedDPS / Life; if the nodes are inert the number
will say so.
