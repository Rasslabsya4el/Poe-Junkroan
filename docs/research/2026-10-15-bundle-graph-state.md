# Bundle graph (#18, #19): state on main at f6002872 and the parse-outcome count (2026-10-15)

Read-only research. "Read" = in a file at the cited line; "counted" = my Python one-off over the cited file (scratch, `python -I`, no PoB); "inference" = marked.

## Part A. The state

### A1. Corpora and what each holds
- `game_corpus` (`src/junkroan/pob/game_corpus.py:26-35`): 8 families extracted from `vendor/pob/source` text: items (BASES only, with `implicit_text`), active_gems, support_gems, passives, masteries, ascendancies, keystones, config_surfaces. Node records carry `stats` text, flags (`is_notable`, `is_keystone`, `is_mastery`), graph edges (`incoming_node_ids`/`outgoing_node_ids`) -- `corpus_data/passives.json` (2421 records = 784 notables + 1637 small; keystones, masteries, ascendancies are separate files). No parse outcome in any of them.
- `tag_corpus` (`tag_corpus.py:36-50`) and `mod_corpus` (`mod_corpus.py:27-28`): text-derived tags/facets and regex "families" (NUMBER_RE, OPERATOR_PATTERNS, `mod_corpus.py:34-47`) over items/passives/keystones/masteries. No PoB parse. mod_corpus covers base implicits only (`SURFACE_KINDS` = item_implicit, passive_node, keystone_node, mastery_effect). Counted: no module outside the two files (and `tag_data/manifest.json`) imports either (grep over src, scripts, tools, tests). They are built and committed, not read at runtime.
- `corpus_data/uniques.json` (1332 uniques, 11,247 lines; mtime Sep 12): built by `scripts/build_unique_index.py:57-92` through `PobSession.parse_mods` (400 lines per call). PER LINE it keeps the parsed mods (`name`, `type`, `value`, `flags`, `tags`) and `unsupported_lines` (= PoB's `unsupported` flag, `headless_runtime_worker.py:610`: not ok, or no mods, or `extra` non-nil). It does NOT keep `extra` text itself; partial vs none is recoverable only as "unsupported line with mods present" vs "without" (my method, counted below).
- `corpus_data/scaling_vectors.json` (477 vectors, 3611 payoffs; mtime Oct 1): `scripts/build_scaling_vectors.py:40-135`. Sources: uniques, notables, keystones, masteries, ascendancies, supports (not small nodes, `:47-49`). Keeps ONLY mods carrying a PerStat/Multiplier/Condition tag (payoffs, `:121-127`) and "enablers" = untagged BASE/INC/MORE mods by stat name (`provided`, `:118,135`). Lines with no tag, flag-only, unparsed: dropped. No outcome per line.
- `corpus_data/mod_families.json`, `bench_mods.json` (repoe, 1601 mods), `mod_data/poedb_affix_catalog/`: affix ladders from repoe/poedb text, no PoB parse. Read by `pob/mod_families.py` (loot_gear.py:30, audit.py:26, wishlist_gear.py:30).
- `artifacts/keystone_flip/parse.json` (untracked, 57 keystones, 125 lines): `src/junkroan/keystone_parse.py:75-120`. Per line: kind zero/redirect/add/unparsed + PoB's mods. `extra` is read for classification (`:73-80`) but collapsed into "unparsed".
- **PoB's own cache `vendor/pob/source/src/Data/ModCache.lua`** (13,174 entries, counted): `c["line"]={mods|nil, extra|nil}` = exactly the parse OUTCOME per line. Loaded at start unless regenerated (`Modules/Main.lua:130-133`); written by `main:SaveModCache` (`Main.lua:293-310`), which drops JewelFunc/ExtraJewelFunc lines (`:298`). Parser keeps the pair `{modList, extra}` after a second pass (`ModParser.lua:6930-6941`). Full = `,nil}` tail, partial = mods + extra string, none = `{nil,` or `{{},`. Counted: 10,335 full, 416 partial, 2,423 none. Limits: keys with ranges "(10-15)%" are always none (range not substituted; counted entries with RANGE in key are skipped in form-matching); a line missing from the cache is NOT unparsed, it is "not known" (PoB parses it live); the cache reflects the generating PoB commit, and on 9,351 rolled unique lines present in both it disagrees with uniques.json's `unsupported_lines` on 88 (0.9%; cause not known; inference: drift between the Sep 12 uniques parse and the cache).

### A2. `src/junkroan/mechanics/` (hand-maintained; README.md:1-16 says only what PoB does not compute)
| file | rows | readers |
|---|---|---|
| `notes.json` | 6 notes (4 constraint, 2 note: pride, perforate, volatile_dead, detonate_dead / fireball, brands) | `optimizer/ramp_inputs.py:46` |
| `pending_facts.json` + `.py` | 8 facts (4 pending, 1 approved, 3 disputed) | `ramp_inputs.py:232`, `self_cost.py:117,145`, `spectre_overlap.py:15`, `build_result.py:70` |
| `unsupported_lines.json` | 8 kinds (on_kill_generator, on_block_generator, steal_charges, chance_enemy_debuff, self_cost_on_use, cruelty_effect, first_seconds_only, no_representation), regex `pattern` + lane + named `enablers` items (Squirming Terror, The Writhing Jar...) | `config_rules.py:190,455`, `self_cost.py:2` |
| `self_cost_gems.json` | 1 gem | `self_cost.py:48` |
| `skill_use_ending_buffs.json` + `.py` | 2 effects | `buff_gems.py:45`, `config_rules.py:1151` |
| `bench_unlocks.json` + `.py` | 806 by_mod_id + 23 by_name (wiki cargo) | `loot_gear.py:29`, `rails.py:21`, `session.py:35`, `trace.py:53` |
| `day1_gear_templates.json` | 11 templates, 13 by_type | `wishlist_gear.py:34` |
Not a graph: no edge/"provides"/"requires" record exists in any of them. Mageblood, Master Surgeon, Inextricable Fate: `grep -rniE "abyss|timeless|Megalomaniac|Mageblood" src/junkroan/optimizer` finds no Mageblood/abyss/Megalomaniac code; I did not grep the mechanics JSON for those names beyond reading its row ids (listed above).

### A3. Proof rules, the "provides" side today (D77)
- `config_rules.py:282-300` `_parsed_sources`: a source = a parsed FLAG mod named `Condition:<X>` with Condition-tag preconditions, read from `parse_mods_batch` (`:247-265`, one batched memoised call per build). `parsed_buff_proof` (`:389`) resolves preconditions recursively, fail-closed (ADR D77 `docs/adr/0077-...md:12-18`). Leech conditions stand on PoB's computed leech rates (`:403-417`).
- Text-path proofs remain for charges/generators: `charge_sources` (`:477`), `generator_source_contexts` (`:1293`), `_generator_proof` (`:2105`); D77 left "the `condition*` generator proofs still use the word path" for an amendment (`0077...md:25`).
- So "provides" is: per BUILD, from parsed lines of the build's own items/tree/gems. There is no corpus-wide provides index except `scaling_vectors` enablers (A1), which no code reads except `scripts/reshaping_inventory.py:13,88`.

### A4. Does the optimizer pick flasks, tinctures, jewels, abyss, cluster?
- Flasks and tinctures: yes. `pipeline.py:644` calls `_flask_step`; `pipeline.py:1743` bases = every obtainable base with drop level <= base level max, tinctures allowed (`rails.py:178-181`, `rails_default.json:72` slots 5); `flask_step.py:1-28` picks by PoB score, magic items only (<= 1 prefix + 1 suffix, `flask_lines.py:1-10`, mods from `ModFlask.lua`/`ModTincture.lua`). Skipped on the screen (`pipeline.py:638-639`). Unique flasks: not in the step (inference from `flask_lines.py:1`: "MAGIC flask"; a unique flask enters only as the build's input/skeleton). The flask slot count is a fixed 5; "Mageblood + 4 magic utility flasks" has no code.
- Rare jewels: yes. `pipeline.py:1646` `run_jewel_step`, 1-line rare jewels on 3 bases only (`jewel_lines.py:19` Crimson/Viridian/Cobalt) from `ModJewel.lua`; `rails_default.json:70` `count_max 2, lines 1`; `repick_jewels` `pipeline.py:1707`.
- Cluster jewels: code exists (`pipeline.py:1603`, `cluster_lines.py`), but `rails_default.json:71` sets `count_max 0, sizes []` = OFF in the default rails (#433 closed with large/medium 12/6 rails; where it is switched on: not found in `rails_default.json`, not known).
- Abyss jewels (ModJewelAbyss), timeless jewels, Megalomaniac: no picker. grep over `src/junkroan/optimizer` for abyss finds nothing; `overleech.py:20` only reads LegionPassives.lua. Anoint: yes (`anoint_step.py`, `pipeline.py:642`). Enchants: 414 enchant lines in Data/Enchantment*.lua; the rulebook ticket #631 (open) lists Harvest enchants as missing.

### A5. "Saved bundles" (#1028 round 4 / #1040 Notes)
- Read: #1040 Notes say "a stored list of WHAT TO TRY FIRST with its PoB numbers, never a model and never a ban; PoB re-measures it in every build"; "bundles that work only together are #18 (parked)". #1028 comment 2026-10-14 11:26 gives the owner's frame (flags for what PoB cannot count; bridges tried as hypotheses; working bundles saved and later reused as skeleton parts).
- Code/data: none. `grep -rniE bundle src scripts --include=*.py` hits only `pob/artifacts.py` (artifact bundle layout), not build bundles. No file under `src/junkroan/mechanics/`, `var/` or `corpus_data/` stores bundles.

### A6. ADRs and closed issues since 2026-09-26
- New ADRs since 2026-09-26 (git log --diff-filter=A): D108-D118. Touching this area: D115 (Flask uptime = PoB's own 100% line), D113 (test by kind). None about graph/bundle/corpus. Older relevant: D8 (0008: hand-maintained knowledge only for non-PoB facts), D14, D48 (0048: unparsed lines named in the audit), D62 (knowledge loop/pending facts), D77.
- Code touching this area since 2026-09-26 (git log): #1030 `keystone_parse.py` (2026-10-14), #1042/#1065 `scripts/reshaping_inventory.py` (2026-10-14/15, uses uniques.json + scaling_vectors + passives), #542 pending fact, #433 cluster corpus fields (expansion_size). `scaling_vectors.json` regenerated 2026-10-01 with every provider kept (#22 closed, child of #18).
- Closed, flask-related: #575 (flask active only at 100% uptime), #604, #436 (day-1 flasks and tinctures), #589, #529, #596, #616, #705, #607 (tinctures). Closed, corpus/graph: #22, #433, #533, #1030, #1042, #1065, #1028 (merged into map #1040).
- Map #503 "the endgame loadout" (open, `parked`, area:builds, no parent): children #440 (alternate ascendancies), #18, #631 (Harvest/Heist enchants). Body says "Child tickets now: 2, both open" -- stale, 3 children exist. Its Not-yet-specified line names "the far-sight packages". #18 children: #22 (closed). #18 comment 2026-10-14: split from #1028, owner's frame.
- Map #476 "after the prototype" (open): children #19, #29, #12 (closed), #955, #965, #1039. Body says "5 child tickets, 4 open" -- stale, 7 exist (6 open). #19 has no children and no body beyond the Phase 5 quote.
- Both #18 and #19 carry the 2026-10-11 comment: parked with their map until the day-1 prototype (#1) is accepted.

## Part B. The number: how PoB parses mod LINES

Method (counted). Exact-line sources: uniques via `uniques.json` (PobSession outcome), keystones via the same file's twin `parse.json`; tree classes and ladders via ModCache lookup of the exact node/ladder line. "hit" = lines found in ModCache. None includes `{nil,..}` and `{{},..}`; partial = mods and a non-empty `extra`.
| source class | lines | with an outcome on disk | full | partial | none |
|---|---|---|---|---|---|
| unique item lines (PobSession, uniques.json) | 11,247 | 11,247 (100%) | 10,225 (90.9%) | 145 (1.3%) | 877 (7.8%) |
| passive notable (784 nodes) | 1,768 | 1,759 | 1,616 (91.9%) | 19 (1.1%) | 124 (7.0%) |
| passive small (1,637 nodes) | 2,109 | 2,109 | 2,082 (98.7%) | 4 (0.2%) | 23 (1.1%) |
| keystone (57 nodes; parse.json, PobSession) | 125 | 125 | 108 (86.4%) | 2 | 15 (12.0%) |
| mastery effects | 2,041 | 2,037 | 1,543 (75.7%) | 78 (3.8%) | 416 (20.4%) |
| ascendancy nodes | 1,098 | 1,032 (94%) | 872 (84.5%) | 23 (2.2%) | 137 (13.3%) |
| ALL of the above (keystone taken from ModCache hits 108/2/14 for the total) | 18,388 | 18,308 | 16,446 (89.8%) | 271 (1.5%) | 1,591 (8.7%) |

**The one number: 89.8% of the 18,308 unique + tree lines parse fully, 1.5% partially, 8.7% not at all** (about one line in ten is not a full PoB mod; unique lines 90.9%, masteries 75.7% worst).

Item affix ladders, flask mods, enchants: exact-line ModCache lookup is poor (ladder lines carry ranges: Explicit 9% hit, Flask 4%, Tincture 0%, Enchants 0%, `count.py` run). Form-level estimate (numbers replaced by #, range-keyed cache entries excluded; validated on unique lines: 10,957 agree vs 88 disagree with PobSession, 99.2%):
| class | lines | form found in ModCache | full | partial | none |
|---|---|---|---|---|---|
| Explicit affixes (ModExplicit.lua) | 5,126 | 4,474 (87%) | 4,364 (97.5%) | 4 | 106 (2.4%) |
| flask mods (ModFlask.lua) | 340 | 153 (45%) | 145 | 0 | 8 |
| tincture mods | 72 | 21 (29%) | 21 | 0 | 0 |
| jewel mods (Jewel + Abyss + Charm) | 1,428 | 948 (66%) | 870 (91.8%) | 15 | 63 (6.6%) |
| cluster notables (ModJewelCluster) | 558 | 339 (61%) | 338 | 0 | 1 |
| bench (ModMaster) | 958 | 921 (96%) | 911 | 0 | 10 |
| enchants (7 Enchantment files, 2,006 pieces split on "/") | 2,006 | 83 (4%) | 73 | 2 | 8 |
For flasks, tinctures and enchants the hit rate is too low to state a share: NOT KNOWN. The "none" shares quoted are over hits only; unhit lines may differ.

Flag vs numeric (full lines only; flag = every mod FLAG, ignoring Multiplier/Condition/PerStat tag types; list = only LIST mods like ExtraSupport/GemProperty/ClusterJewelNotable; numeric = at least one BASE/INC/MORE/OVERRIDE):
| class | full | numeric | flag-only | list-only | other |
|---|---|---|---|---|---|
| uniques | 10,225 | 6,724 (65.8%) | 428 (4.2%) | 2,843 (27.8%) | 230 (2.2%: FLAG+LIST 105, no-mod 88, MAX/MIN/CHANCE 31, ...) |
| notables | 1,616 | 1,576 (97.5%) | 29 (1.8%) | 11 | 0 |
| small | 2,082 | 2,072 | 10 | 0 | 0 |
| keystones | 108 | 62 | 43 (39.8%) | 2 | 1 |
| mastery effects | 1,543 | 1,387 | 140 (9.1%) | 16 | 0 |
| ascendancy | 872 | 764 | 82 (9.4%) | 24 | 2 |
A FLAG type includes `Condition:X` flags that PoB sets as conditions, not only calc rule flags; the two are not separated here (not known without reading each name).

### What is NOT on disk, and the run that would settle it
Not on disk: PoB's outcome for the item-affix ladders (ranges unsubstituted), flask/tincture/jewel/abyss/cluster mods at rolled values, all 414 enchant lines, small gaps in tree classes (ascendancy 6% not in the cache). A run to settle it (not started; a heavy run):
- Call: `PobSession.parse_mods(lines)` (`pob/session.py:676`), batches of 400-500 as `scripts/build_unique_index.py:67`; row = `{line, ok, unsupported, extra, mods[]}` (Lua at `headless_runtime_worker.py:608-623`).
- Input: the ladder lines from `Data/ModExplicit.lua`, `ModFlask.lua`, `ModTincture.lua`, `ModJewel*.lua`, `ModJewelCluster.lua`, `Enchantment*.lua`, each with every range replaced by its midpoint (the way PoB rolls a line, `jewel_lines.py:21` RANGE_VALUE 0.5) plus the ~800 tree/ascendancy lines missing from the cache. About 14k to 20k distinct lines; PoB startup plus batches. Duration: NOT measured in the repo (build_unique_index.py prints `parsed N lines in X s` but no log of it is on disk); stays unknown until the first run.
- Output: write ONE new file `corpus_data/parse_outcomes.json` keyed by line with `{ok, unsupported, extra, mod_types}` (the missing piece: `extra`, which `uniques.json` drops). Then the count above is one `python -I` pass.
- Cheaper alternative without a new run: add `extra` to `build_unique_index.py`'s record (`:92`) on the next regeneration.

## Gaps and cautions for the grill (read vs inferred)
- Read: the repo holds PoB's parse per line in 3 places (uniques.json mods, ModCache.lua, parse.json), but the two corpora named in #18's text (`tag_corpus`, `mod_corpus`) hold none and have no readers.
- Read: no data structure of edges ("provides"/"requires"), no bundle store, no Mageblood/Master Surgeon/Inextricable Fate row exists; `mechanics/` holds 8 pending facts + 6 notes, none about items providing a condition for another item.
- Inference: for "script-built graph over what PoB parses and counts", the two inputs present today are `uniques.json` (Sep 12, PobSession) and ModCache.lua (PoB's own); `scaling_vectors.json` already has the PerStat/Condition tag payoffs but drops untagged and flag-only lines, i.e. the 4.2% flag-only unique lines (Master Surgeon-like rule flags) are not in it.
- Not known: the `extra` text for partial lines in uniques (dropped at generation), the duration of a full parse run, why cluster jewels are `count_max 0` by default, whether ModCache drift vs the pinned PoB explains the 88 disagreements.
