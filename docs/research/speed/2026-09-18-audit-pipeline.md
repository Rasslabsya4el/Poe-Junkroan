# Speed audit: the build pipeline around the tree optimizer

Scope: `optimizer/pipeline.py`, `search/generator.py`, `optimizer/config_rules.py`,
`optimizer/loot_gear.py`, `search/skeleton.py`, `scripts/benchmark.py`.
No code changed, nothing written to the repo.

## Sources and baselines

| source | what it is |
|---|---|
| `build.prof` | cProfile of one full stormbrand build, 3,280 s, **before** the `read_state` fix (commit fce90ab). `build2.prof` does not exist; `build_profile2_out.txt` is 2 bytes. |
| `artifacts/benchmark/20260917-0844-core14-frozen/` | 42 builds (14 refs x 3 seeds), `--loop-seconds 5400`, 5 workers, 44,509 s wall. Median build **5,231 s**, mean 4,976 s. Also **pre-fix**. |
| `artifacts/benchmark/20260918-*-restarts-smoke*` | the campaign in flight, **post-fix**; used only to confirm the post-fix cost of the picks move. |

**Post-fix accounting of the profiled build.** The adapter's `read_state` ran 655 times at
1.677 s = 1,098.8 s; at 42 ms that is 27.5 s. So the profiled build is now **~2,209 s**, and its
composition is:

| PoB call | calls | seconds | % of the post-fix build |
|---|---|---|---|
| `trial_stats` (the actual search) | 452 batches, ~88k trials | 1,313.4 | 59.5% |
| `set_skills` | 485 | 395.4 | **17.9%** |
| `load_xml` | 171 | 129.1 | 5.8% |
| `set_config` | 107 | 98.6 | 4.5% |
| `mutate_nodes` | 423 | 59.1 | 2.7% |
| `stats` | 1,893 | 44.1 | 2.0% |
| `read_state` (post-fix) | 655 | 27.5 | 1.2% |
| `random_rares` / `config_options` / `export_xml` / `equip` / `calc` | 76 / 174 / 647 / 97 / 23 | 26.2 / 23.5 / 23.5 / 17.8 / 13.2 | 4.7% |

Python's own work is noise: `copy.deepcopy` 6.8M calls = 14.7 s, everything else under 8 s.
**After the `read_state` fix the largest non-search cost in a build is `set_skills`.**

For the benchmark set I estimate the post-fix median build at **~4,600 s** (5,231 minus ~210 s of
`derive_config`'s `build_text`, ~300 s of picks weighted over the 12 brand logs, ~120 s elsewhere).
One post-fix core14 log would replace that estimate; percentages below use it.

## Ranked findings

| # | finding | file:line | evidence (numbers) | saving | kind | how to prove |
|---|---|---|---|---|---|---|
| 1 | `rejudge_picks` evaluates every candidate support through a whole-build XML round trip | `search/generator.py:418` -> `pob/session.py:226` -> `pob/headless_runtime_worker.py:1924` | 485 `set_skills` = 395 s of the profile (**17.9% of the post-fix build**); 483 of them from `_set_main_link_raw`. 0.815 s each. Benchmark: picks = 659 s/build (30 non-brand logs) and 1,699 s/build (12 brand logs); 185-283 s per run, 227-283 candidates per run. Live post-fix campaign: 101-238 s per picks run. The readback after the setter is free (`generator._score` 480 calls = 0.7 s). | **600-850 s/build, 13-18%** | exact (if the gem trial reproduces the numbers) | for every legal support of 3-4 finished fixtures, compare the gem-trial stats with the `set_skills` stats; identical -> exact |
| 2 | `judge_stack_options` re-runs a 9-probe binary search inside **every** `derive_config` | `optimizer/config_rules.py:483`, called at `:646` | ceiling 50 -> `value(0)`, `value(50)`, `value(49)` + 6 bisection steps = 9 x (`set_config` 0.92 s + `stats` 0.10 s) **per stack var per call**. Spark has 2 (`intensifyIntensity`, `sigilOfPowerStages`) = ~19 s per `derive_config`. spark-s1 has 51 judged moves -> >=86 `derive_config` calls -> **>=1,600 s**. Spark is the only core14 reference with stack options and the slowest: 6,951 s median vs 5,231 s. | **>=1,600 s on stack-option builds**, 0 on the rest of core14 | exact with a memo; approximate if cut to a 2-probe re-verify | count the probes with a counter; compare the caps returned with and without the memo on one spark build |
| 3 | the two kicks: 452 draws per campaign, 12.8% kept | `optimizer/pipeline.py:480-507` | kick joint 47,848 s = **1,139 s/build**, 34 kept of 251 (13.5%), **1,407 s per kept move**. kick tree 31,726 s = **755 s/build**, 24 of 201 (11.9%), 1,322 s per kept move. 135 of 177 reverted kick-tree draws (**76%**) returned *exactly* the incumbent number. | 3->2 and 4->3 draws = **537 s/build, 12%** | approximate | 3-seed medians on the two most sensitive references, then the full 14 |
| 4 | `_value_with_enabled`: 86% of calls answer "nothing enabled" after a full derive + XML restore | `optimizer/pipeline.py:597`, driven from `optimizer/tree_optimizer.py:293-307` | 127 calls, 388 s pre-fix (~165 s post-fix); only 18 reached `_apply_config`, and those 18 were **3 distinct nodes** re-judged 5 / 8 / 5 times, because `hooked` is a local of one `allocate` call. Restore is `load_xml` 0.746 s where `mutate_nodes(remove=added)` is 0.129 s. Across 42 logs: 1,255 successful judgements = 30/build; "Caster Mastery" alone 316 times = 7.5/build. | **~140 s/build, 3%** | exact | assert the cheap pre-filter's verdict equals the current one on every call of one build |
| 5 | the picks move re-scans all ~85 legal supports per slot every run; the shortlist it builds is dead code | `search/generator.py:656, 679, 687`; caller `optimizer/pipeline.py:458-460` | `max_sweeps=1`, so the sweep loop runs once and `shortlists[i]` (written at `:687`) is **never read**; a new `SkeletonGenerator` per pass discards it anyway. 101 of 150 picks runs kept nothing (25,894 s); 60 of those followed another fruitless run (13,982 s = **333 s/build**). Legal-support lists are 76-96 entries. | 333-600 s/build | approximate (a support that only became good after the tree/gear moved can fall outside the top 12) | 3-seed medians, plus a log line counting how often the kept swap came from outside the previous top 12 |
| 6 | the rebuild regrows the tree twice and throws one regrow away | `optimizer/pipeline.py:781-827` | median **502 s/build** (10.3% of all stage seconds); in the profile `allocate` x2 = 358 s + `refine` x2 = 83 s. `sum` wins 22, `cover` 19, tie 1 -> neither mode can simply be dropped. 6 of 42 rebuilds are reverted whole (3,015 s = 72 s/build thrown away outright). | ~250 s/build if the second mode runs only when the first fails to beat the incumbent | approximate | 3-seed medians |
| 7 | `_apply_config` rewrites the identical config, and a revert re-derives lanes the snapshot already carries | `optimizer/pipeline.py:652` and `:389`; `pob/session.py:311` | `set_config` 107 calls = 98.6 s (0.92 s each: `config_inputs` -> `export_xml` + ElementTree parse, then a whole-build reload). Every revert path is `load_xml(snapshot)` (`:416, :439-444, :493, :502`) and the exported XML carries `<Config>`; 724 reverted moves across 42 logs. | ~100 s/build (skip identical writes) + ~21 s/build (drop the post-revert reconfigure) | exact | a counter over one run: how many `set_config` payloads equal the previous one; assert the derived lanes equal the snapshot's config after a `load_xml` |
| 8 | gear moves that end with the incumbent | `optimizer/pipeline.py:418-426`, `optimizer/loot_gear.py:152` | 1,791 of 1,940 gear-slot moves (**92%**) logged "incumbent kept": 5,029 s = **120 s/build for no change**. `fill_slot` = `random_rares` 0.43 s + a 200-trial batch **3.74 s** + `equip` 0.21 s; the trial batch is 85% of it. No roll is repeated: seeds are `seed + 977p + 17i` (loop), `seed + 17i` / `seed + 7 + 17i` / `seed + 1007 + 17i` (construction), and 17 x 9 < 977, so no two passes collide. | up to 120 s/build | approximate | 3-seed medians |
| 9 | `build_text` is recomputed 707 times from a fresh `read_state` | `optimizer/config_rules.py:292`; `pob/session.py:407` | 707 calls; its own Python work is 0.4 s **total**, so it is pure re-reading. Post-fix ~56 ms each (42 ms worker + ~14 ms deepcopy of the state) = ~40 s/build. `read_state` deep-copies the whole state for every caller. 531 of the 707 calls come from `derived_counts` (`search/skeleton.py:91`) and only compute a **brand** count that depends on tree and items, not on the support link being trialled. | ~35 s/build | exact | byte-compare `build_text` with and without the cache across one build |
| 10 | benchmark: the author's row is recomputed per seed; 5 workers on 6 cores | `scripts/benchmark.py:98-171`, `:191`, `:225` | fixed overhead per build = wall - sum(stages) = **54 s median (1.0%)**: PoB boot, fixture load, unique normalisation, author `derive_config` + `set_config` + `_tune_choice_inputs`, and `_finish`'s post-stage work. `run_one` is submitted per (slug, seed) and repeats the identical author preamble 3 times. 42 builds = 209,000 s of work in 44,509 s wall on 5 workers (94% efficiency); each PoB worker is ~1.2 GB RSS. | ~72 s per 3-seed reference; +20% campaign throughput at 6 workers | exact / measurable | cache the author row per slug; time a 6-build set at 5 vs 6 workers |

Taken together, 1 + 2 + 4 + 7 + 9 are **exact** and worth roughly **900-1,100 s/build** (20-24%) on an
ordinary reference and more on a stack-option one; 3 + 5 + 6 + 8 are **approximate** and worth a
further ~1,240 s/build (27%) if the benchmark accepts them.

---

## 1. `rejudge_picks`: what one candidate costs, and why it need not

Per candidate the code does exactly this (`search/generator.py:684` and `:715`):
`set_trial(skeleton, trial)` then `self._score()`. `set_trial` is `_set_main_link` when the build has
instance counts and `_set_main_link_raw` otherwise (`:661`). `_set_main_link_raw` calls
`PobSession.set_skills`, which the worker implements as **export the whole build XML, parse it,
rewrite the `<Skills>` node, reload the build** (`headless_runtime_worker.py:1924-1926`). That is
0.815 s (485 calls, 395.4 s). No `reconfigure` happens per candidate -- lanes are re-derived only for
the accepted candidate, through `honest()` (`:647`) -- and the score readback itself is free
(`_score` 480 calls, 0.7 s), because the recalc already happened inside `set_skills`.

The extra cost on brand builds is `_set_main_link`'s `refresh_minion_counts`
(`search/skeleton.py:198` -> `derived_counts:40`), which calls `build_text` **only when the link
contains a brand** (`:88-91`). That is why the split is so sharp: picks cost **1,699 s/build on the
12 brand logs and 659 s/build on the other 30**. The `read_state` fix removes that gap; it does not
touch the 0.815 s.

Candidate counts per sweep: `legal_supports` returns 76-96 names per skill
(`artifacts/cache/legal_supports-*.json`), and the sweep tries every one of them in every non-fixed,
non-enabler support slot (`:674-685`), then every utility candidate in every picked group
(`:707-718`). Measured: 227-283 candidates per run, 150 runs over 42 builds.

**Repeats across passes.** `changed_since_picks` (`pipeline.py:372, 451, 463`) skipped 57 of 207
opportunities (27.5%) -- it works, but it only catches a build that did not move at all. The
remaining 150 runs each rescan everything: 101 kept nothing (25,894 s), and 60 of those followed
another run that had also kept nothing (13,982 s = 333 s/build). The obvious memo exists in the code
already and is dead: `shortlists` (`:656`) is written at `:687` and never read, because the loop
passes `max_sweeps=1` and a fresh `SkeletonGenerator` is built every pass (`pipeline.py:458`).

**Cheap pre-filter.** Legality is already cached to disk per skill (`:380-385`, 0.0 s in the
profile), so it is not a cost after the first search of a skill; on a cold cache it costs ~85
`set_skills` (~70 s) which PoB could answer in one round trip with its own predicate
`calcLib.canGrantedEffectSupportActiveSkill` (`CalcTools.lua:85`).

**The fast trial calculator has no gem kind -- but PoB's does.** `session.trial_stats`
(`session.py:603`) and the fast Lua (`headless_runtime_worker.py:960-1032`) accept `add`, `remove`,
`mastery` and `item` (`override.repSlotName` / `override.repItem`, `:1011-1017`). There is no gem
override in `CalcSetup.lua`. PoB does not need one: `calcs.getMiscCalculator` is documented as the
"calculator for other changes (adding/removing nodes, items, **gems**, etc)" (`Calcs.lua:122`), and
`GemSelectControl:CalcOutputWithThisGem` (`GemSelectControl.lua:59-99`) swaps the gem instance in
`displayGroup.gemList` **in place**, calls `calcFunc(nil, useFullDPS)` and puts the old gem back --
which is exactly how PoB's own gem dropdown shows a DPS delta for every candidate
(`GemSelectControl.lua:418`). A `gem` trial kind built the same way would cost one `calcs.perform`
pass: measured item trials are 17 ms (76 batches / ~12,600 trials / 217 s) and node trials 14.5 ms
(214 batches / ~53k trials / 774 s), so **~15-30 ms instead of 815 ms, 27-54x**. Caveats to prove:
the count a link implies (D57 rule 2, a Spell Cascade leaving a Volatile Dead link) is a Python
derivation and must ride along with the trial, and `main_part` must be preserved.

## 2. `derive_config`: what it costs now, and the one part that is unbounded

Post-fix a `derive_config` call is about **0.26 s**, made of `config_options` 135 ms
(174 calls / 23.5 s -- now more than half of it), `config_inputs` 38 ms (`export_xml` + an
ElementTree parse), `build_text` ~56 ms, `_gem_names` + `_main_skill_name` ~29 ms (cached
`read_state`, but two more deep copies), `stats` ~5 ms. `_reconfigure` (`pipeline.py:638`) adds
`refresh_minion_counts` (~50 ms) and `_apply_config` (**0.92 s**), so **`set_config` is now 3.5x the
whole derivation**. `_reconfigure` ran 45 times in the profiled build at 2.45 s; post-fix ~1.2 s.

**How often per pass.** `judge` (`:376`) reconfigures once before scoring and once more after a
revert (`:389`), so a kept move costs 1 and a reverted move 2. Gear moves reconfigure themselves
(`:427`, again after a repair at `:436`) and pass `reconfigured=True`; `_joint_round` reconfigures at
its end (`:330`). A pass that reaches the kicks therefore spends roughly: refine 2 + swaps 2 + gear
slots 0-2 each (the 92% that keep the incumbent `continue` at `:426` **before** any reconfigure --
that is already right) + 3 tree kicks x2 + 4 joint kicks x2 (+1 inside each round) = **~22 per kick
pass**.

**Which moves cannot change a proof: none.** The conservative lane is a function of
`config_options`, `stats` and `build_text` = items + allocated passives + gem names
(`config_rules.py:292-335`). Tree moves change passives, gear moves change items, picks change gem
names. So "skip the derivation for move class X" is not available. Two things are available instead:

* **exact:** `_apply_config` can compare the payload it is about to write with the one it last wrote
  and skip `set_config` when they are equal. The lane changes a handful of times per build (the logs
  show "6 inputs on" at construction and "11 conservative / 30 optimistic" at the end), so most of
  the 107 writes are identical. Worth most of ~100 s/build.
* **exact:** drop the `_reconfigure` at `:389`. Every `revert()` is a `load_xml(snapshot)`
  (`:416, :439-444, :493, :502`) and the exported XML carries its own `<Config>`, so the lanes are
  already back. 724 reverted moves across 42 logs.

**The unbounded part.** `judge_stack_options` (`config_rules.py:483`) is called unconditionally at
`:646`, and with `prefer_rules=True` (which the pipeline always passes) a stack option can never take
the `has_own` shortcut at `:577` -- it falls through `_numeric_rule` to `pending_stacks` at `:595`
on **every** call. Each pending var then costs `value(0)`, `value(ceiling)`, `value(ceiling-1)` plus
`ceil(log2(50)) = 6` bisection steps = **9 `set_config` + 9 `stats`**, at 0.92 + 0.10 s, around a
`export_xml`/`load_xml` pair. Spark carries two such vars (`intensifyIntensity`,
`sigilOfPowerStages`) = ~19 s **per `derive_config` call**. spark-s1 logs 51 judged moves, so at
least ~86 derivations, so at least **1,600 s per spark build** -- and spark is both the only core14
reference with stack options and the slowest of the fourteen (6,951 s median against 5,231 s).
`STACK_OPTION_LABEL` matches `intensity|stages?|stacks?` in any Skill Options section
(`config_rules.py:126`), so this grows with the reference set, not shrinks.

## 3. Loot: what dominates `fill_slot`

`fill_slot` (`loot_gear.py:152`) costs 4.42 s per call (58 calls, 256.3 s): `random_rares` 0.43 s
(76 calls, 26.2 s), the **200-item trial batch plus the bench batch 3.74 s** (76 batches, 217.2 s),
`equip` 0.21 s (58 calls, 12.1 s), `stats` ~7 ms. The trial batch is 85% of it, at ~17 ms per item
trial; the bench batch is a second, much smaller batch (`:194`) and `list_bench_mods` is cached
(`:139-142`, 8 calls, 0.1 s).

**No roll is ever repeated.** Construction pass 1 uses `seed + 17i`, pass 2 `seed + 7 + 17i` and
`seed + 1007 + 17i` (`pipeline.py:187, 213`; `loot_gear.py:225`), the loop's gear move
`seed + 977p + 17i` (`pipeline.py:422`), the joint round `seed + 7919p + 977(d+1) + j`
(`pipeline.py:306, 499`). Since 17 x 9 = 153 < 977, no two passes can produce the same slot seed.
So the 1,791 "incumbent kept" outcomes (92% of gear-slot moves, 5,029 s = 120 s/build) are honest
fresh draws that lost -- not deterministic repeats. The lever there is statistical, not structural:
a slot whose incumbent has survived two consecutive passes could be skipped for a pass, or `n`
lowered for it. Approximate, needs 3-seed medians.

## 4. The loop's structure: where the seconds go and what they buy

42 logs, every judged move counted:

| move | kept | reverted | keep rate | seconds | s/build | **s per kept move** | share of loop |
|---|---|---|---|---|---|---|---|
| kick joint | 34 | 217 | 13.5% | 47,848 | 1,139 | **1,407** | 29.0% |
| picks | 49 runs | 101 runs | 32.7% | 40,151 | 956 | 819 | 24.3% |
| tree path swaps | 62 | 148 | 29.5% | 32,846 | 782 | 530 | 19.9% |
| kick tree | 24 | 177 | 11.9% | 31,726 | 755 | **1,322** | 19.2% |
| tree refine | 56 | 154 | 26.7% | 5,922 | 141 | **106** | 3.6% |
| gear slot (incumbent kept) | - | 1,791 | - | 5,029 | 120 | - | 3.0% |
| gear slot (judged) | 121 | 28 | 81.2% | 1,521 | 36 | **13** | 0.9% |

The order of value is unambiguous: **gear slots are 100x cheaper per kept move than the kicks, and
tree refine 13x cheaper.** The kicks are 48% of the loop's time and produce 58 of the 346 kept moves.

The kick draws also repeat visibly: **135 of the 177 reverted kick-tree draws (76%) returned exactly
the incumbent number, viol included** -- because `TreeOptimizer.reoptimize` keeps or restores by its
own objective inside (`tree_optimizer.py:558-566`) and, having restored, hands the loop an unchanged
build to judge. That is 21,279 s of the 27,382 s spent on reverted tree draws. The draw itself is
real search; what is provably wasted is the outer `judge`'s reconfigure and score on an unchanged
build (an exact fix: have `reoptimize` report that it restored). Joint draws never repeat (0 of 217),
as expected -- they re-roll gear.

12 of 42 builds stopped on the 5,400 s time budget rather than at a fixed point, and the loop's own
passes are 85% of a build's wall time. Every second saved in findings 1, 2, 4, 7, 9 is a second the
loop spends on moves instead.

## 5. `_value_with_enabled`

`pipeline.py:597` is the tree optimizer's `enabler_hook`: for a candidate node whose text generates
charges, it allocates the node **for real**, re-derives the lanes, applies them, scores, and restores
by `load_xml`. 127 calls, 388 s pre-fix (`export_xml` 4.2 + `mutate_nodes` 16.4 + `derive_config`
249.7 + `_apply_config` 18.0 + `load_xml` 94.8), about **165 s post-fix**, of which `load_xml`
(94.8 s) is now the largest piece.

Only **18 of the 127 calls** got as far as `_apply_config`, i.e. 86% paid the whole cost to return
`None` at `:613`. And those 18 were three distinct nodes -- Caster Mastery 5, Charge Mastery 8, Pain
Forger 5 -- because `hooked` (`tree_optimizer.py:264`) is a local of one `allocate` call and is
cleared again whenever a generator node is applied (`:328`); the profile has 35 `allocate` calls.
Across the 42 logs the same shape holds: 1,255 successful judgements, 30 per build, "Caster Mastery"
alone 316 times.

Three exact fixes stack: (a) a pre-filter -- `charge_sources` already knows *which* kind a node
generates (`tree_optimizer.py:224`), so if every kind it generates is already `True` in the current
conservative lane the answer is `None` with no PoB call at all, which is precisely the test at
`:613`; (b) memoise per `(node_id, effect, charge-lane signature)` on the pipeline instead of per
`allocate` call; (c) restore with `mutate_nodes(remove=applied["added_node_ids"])` (0.129 s) rather
than `load_xml` (0.746 s) on the path where no config was applied.

## 6. Construction: the stage table and what is thrown away

Medians over the 42 logs (the two-space stage lines):

| stage | n | median s | mean s | share of all stage seconds |
|---|---|---|---|---|
| skeleton applied | 42 | 9 | 10 | 0.2% |
| config (conservative lane) | 42 | 8 | 9 | 0.2% |
| gear pass 1 (empty tree) | 42 | 26 | 28 | 0.6% |
| tree greedy | 42 | **196** | 207 | 4.2% |
| gear pass 2 (with tree) | 42 | 58 | 61 | 1.2% |
| tree rebuilt on gear | 42 | **502** | 508 | 10.3% |
| loop pass 1..11 | 42..1 | - | - | 71.6% |
| config (final lanes) | 42 | 39 | 45 | 0.9% |

**Thrown away by construction:**

* The **greedy tree (196 s)** is discarded in 36 of 42 builds: `_rebuild_tree` resets the spec to
  ascendancy + fixed keystones and regrows from scratch (`pipeline.py:798-803`). Its only surviving
  contribution is giving gear pass 2 a tree to optimise against; the rebuild is kept 36/42 and
  reverted 6/42.
* The **rebuild runs two full regrows** ("sum" then "cover", `:794-819`) and keeps one, so roughly
  half of its 502 s -- **~250 s/build** -- is discarded by construction. Dropping a mode is not free:
  sum wins 22, cover 19, tie 1. Running the cheaper mode first and the second only when the first
  fails to beat the incumbent would recover most of it, approximately.
* In 6 of 42 builds the rebuild is reverted whole: 3,015 s, 72 s/build amortised.
* `gear pass 1` (26 s) is re-rolled in pass 2, but the incumbent competes (`loot_gear.py:163-165`),
  so it is not wasted.

## 7. `scripts/benchmark.py`

* **Per-build fixed overhead** = wall minus the sum of the stage seconds = **54 s median, 57 s mean,
  range 36-78 s, 1.0% of a build**. It covers the PoB boot (`:120`), fixture decode, unique
  re-normalisation through `pob.unique_item` + `equip` (`:139-145`), the author's `derive_config` +
  `set_config` (`:148-150`), `_tune_choice_inputs` for the author (`:159`, a `set_config` per list
  value), the author stats, and the part of `_finish` that falls outside any stage record
  (`_prune_optimistic` 30.4 s in the profile, two `calc` lanes, export, `audit_build`, `explain`).
* **The author's row is recomputed per seed.** `run_one` is submitted once per `(slug, seed)`
  (`:225`) and the whole author preamble is seed-independent, so `--seeds 3` does it three times:
  ~72 s of redundant work per reference, ~0.5% of a 3-seed reference. Caching the author row per slug
  (it is a pure function of the fixture + rails) is exact and trivial.
* **Loop budget.** `--loop-seconds` default 2400; the frozen campaign used 5400 and 12 of 42 builds
  stopped on it rather than at a fixed point. The budget is only checked between moves
  (`pipeline.py:398, 484`), so a single 300 s kick draw overruns it -- loop pass seconds sum to
  4,422 s median against a 5,400 s budget with the final pass running past the edge.
* **Workers vs cores.** default `--workers 5` (`:191`) on 6 physical / 12 logical cores. The frozen
  campaign did 209,000 s of work in 44,509 s of wall on 5 workers = 4.70 effective workers (94%).
  A PoB worker is single-threaded and ~1.2 GB resident (measured on the running campaign), so 6
  workers is ~+20% campaign throughput for ~7 GB, and hyperthreading past 6 is worth measuring rather
  than assuming. This changes campaign throughput, never a single build's wall time.
