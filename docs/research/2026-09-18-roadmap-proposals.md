# Ranked backlog with evidence (research pass, 2026-09-18)

Read-only pass over `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md` (all 1,536 lines),
`docs/DECISIONS.md` D50-D64, `docs/readings/*` (3 files) and `docs/research/*.md` (6 files,
briefs excluded), plus the code and artifacts named per claim. Nothing was run and nothing
else was written. Every claim carries a file and a line number. Proposals only; every rule,
every game-logic verdict and every PoB conclusion stays with the main model.

Timing context for the whole report (`artifacts/runs/progress.md`, rewritten 09:55):
`rules-smoke` runs until ~12:41, `speed-both-2` 12:41-17:59, then **`new18-rules` 17:59 ->
Sat 09:53 (15.9 h)** and **`core14-rules` -> Sat 22:17 (12.4 h)**, then the ballista pair and
`restarts-smoke3` to Sun 04:47. Since a run now sees one commit (D64.1,
`docs/DECISIONS.md:1389-1400`), anything that changes numbers and lands **after 17:59** costs a
third campaign (28 h). That deadline drives the ranking in section 3.

---

## 1. Open now

### 1a. Phase 7 checkboxes (`docs/ROADMAP.md`, Phase 7 begins at line 548)

| # | item | location | proof / measurement named | modules touched | parallel? |
|---|---|---|---|---|---|
| 1 | **7.1h** speed, then the objective (5 sub-items; (1)-(3) done, (4) partly done, (5) in flight) | 7.1, L902-947 | `compare_runs.py smoke-frozen rules-smoke --min-delta -100`, then `rules-smoke` vs `speed-both-2 --min-delta -5 --revert-commit 5132b6c`; target a build in 15-25 min instead of 61-69 | `pob/session.py`, `headless_runtime_worker.py`, `optimizer/tree_optimizer.py`, `optimizer/pipeline.py` | serialises everything else that changes numbers; the remaining sub-item is "the author's row and ours under one lane" (proposal P5) |
| 2 | Rule 5 **cluster candidates** in the tree optimizer | 7.2, L1059-1070 | smoke set + `impale_ballista` x 3 seeds with and without `--cluster-candidates`; before: ImpaleChance 10, ImpaleDPS 901 on a 61,900 hit (author 90 / 42,486) | `optimizer/tree_optimizer.py` (flag exists, default off), tag corpus | yes (flagged off); but its verdict lands **after** both campaigns in today's queue (`artifacts/runs/queue.txt`, last 6 lines) |
| 3-23 | The **21 reading rules** merged as `[~]` (7df5671, cdd83eb, d4fd350, 45d8dd0) | 7.2, L1163-1220 | "proof = `rules-smoke`" on 18 of them; "proof = the campaign rerun" on EO (L1185), the random-element mean (L1213) and rage (L1218) | `optimizer/config_rules.py`, `objective_select.py`, `keystone_floors.py`, `self_cost.py`, `ramp_inputs.py`, `random_parts.py`, `rails_default.json`, `scripts/build_from_skeleton.py`, `mechanics/*` | code is merged; only the reading of the two gates is left. Three carry an unfinished knowledge half: delivery types (L1189-1191), Trauma / shock / VD orbs (L1192-1194), corpse-cycle conditions (L1215-1217) |
| 24 | **Lane note**, not a rule yet (author's own config 1.7-2.1x our conservative lane on 5 references) | 7.2, L1221-1226 | "the user reads whether a proof rule is too strict (an ask, item 4 of 7.2)" | `optimizer/config_rules.py` (no code yet) | yes, but its numbers predate the ramp arithmetic (section 2j) |
| 25 | **Spread per reference**, stage-by-stage cause | 7.3, L1234-1251 | measured: `docs/research/2026-09-18-seed-divergence.md` (96 builds; 29 of 32 above 10 points, median 41.6, max 109.1) | analysis only | done as measurement; the levers it names (loot N, kicks) are P3/P8 |
| 26 | **Fixed-point audit item** (an extra loop pass inside the audit; >1% gain = audit error) | 7.3, L1252-1254 | none named; definition of done item 3 is "moves the number less than 1%" (L567-569) | `optimizer/audit.py`, `optimizer/pipeline.py` | yes (audit-only), but it costs one loop pass per build |
| 27 | **Restarts** (best of K seeds) | 7.3, L1255-1269 | measured: `docs/research/2026-09-18-restarts-statistics.md` (K=1 153.6 / K=3 171.0 / K=6 178.0; +5.6 for the third seed, <=3.3 after); "remeasure on the rules code once the campaign rerun gives 3 seeds" | `search/runner.py`, `scripts/progress.py` (metric) | yes; blocked on the campaign rerun for the re-measure |
| 28 | **7.4** all fixtures x 3 seeds: >= author, spread <= 10, audit clean, fixed point | 7.4, L1273-1274 | the campaign rerun is the run; spread <= 10 is contradicted by item 25 (see section 2m) | benchmark only | terminal item |
| 29 | **7.4** user reads the top build of every reference | 7.4, L1275-1276 | the fixed three-part request format (L1337-1354) | none | needs the campaign rerun first |
| 30 | **7.4** `junkroan build` on three requests < 2 h each | 7.4, L1277-1279 | the search's finalists pass the same audit and fixed-point check | `src/junkroan/cli.py`, `search/*` | yes; nothing has run the request path since D51/D58 (proposal P11) |
| 31 | **7.4** Phase 6 leftovers closed or moved to "Later": mapping objective, Azadi / Writhing Jar enablers, Cruelty | 7.4, L1280-1281 | none | `optimizer/mapping.py`, `optimizer/config_rules.py` | yes; Cruelty already answered at L490-508 ("clamped to 40 by PoB itself"), mapping has its first step (L1499-1510) |

### 1b. Follow-ups scattered in the State block (`docs/ROADMAP.md:576-784`)

| # | follow-up | location | state today | modules |
|---|---|---|---|---|
| 32 | Finding (3): the benchmark ratio and `gap_decomposition`'s D/A disagree under "one lane" (poison_spark 78 vs 116, bleed_bow 89 vs 104, impale_ballista 45 vs 84) | L649-652, restated in D61 (`DECISIONS.md:1244-1245`) and as next action (2) at L742-744 | open; the only part of 7.1h item (4) not landed | `scripts/benchmark.py`, `optimizer/config_rules.py` |
| 33 | Finding (6): audit warnings that are the authors' groups carried verbatim - dead support groups on 8 references, a non-applying support on 2, **curses above the limit on 4, four golems for a limit of three on cold_dot** | L654-657; next action (3) at L745-747 calls these "knowledge-level rules that need no rerun" | dead groups and non-applying supports landed (D63.7, `DECISIONS.md:1372-1376`); **golems and curses above their limits are audit warnings only** (`optimizer/audit.py:394-454`), the skeleton still carries them (`scripts/build_from_skeleton.py:34-64`) | `scripts/build_from_skeleton.py`, `optimizer/audit.py` |
| 34 | Finding (5): 30 of 132 builds stop on the time budget, 25 of them on a pass that kept nothing | L653-654; restarts doc §4 puts it at 5 of 42 on the newer code | open input for the fixed-point item (#26) and the loop budget question | `optimizer/pipeline.py` |
| 35 | 7.1h remaining **approximate** speed items: fewer kick draws, refine's batch restructured, `max_depth` | L927-947 ("next approximate: fewer kick draws, judged by the same gate") | not started | `optimizer/tree_optimizer.py`, `optimizer/pipeline.py` |
| 36 | The open speed number: 22-27 ms per candidate in campaign logs against 6-7 ms measured alone; "settle with one reference at `--workers 1` on an idle machine" | L933-936 | not started; the machine is never idle today | measurement only |
| 37 | "Runs count from = 20260916-0941"; the stamp is to be reset "when the pipeline's shape changes so stale rows never count" | L776-777 | D63 states "the numbers of the frozen campaigns are not comparable with anything built after this" (`DECISIONS.md:1384-1385`), yet `scripts/progress.py:124-198` still counts those rows as covered | `docs/ROADMAP.md` State, `scripts/progress.py` |
| 38 | Waiting on the user: reading of the frozen campaigns' best seeds | L748-766 | delivered for `new18-frozen` (readings part 1 and part 2); the user asked and was answered that `core14-frozen` need not be read (`readings/2026-09-18-frozen-campaigns-part2.md:4-6, 37`) | none |

### 1c. Open items carried from earlier phases (outside the strict Phase 7 ask, still unchecked)

- `[ ]` Combinatorial candidate generation from corpora; "open for novelty: the multiplier graph over parsed mods (discussed, not built)" - `ROADMAP.md:233-239`.
- `[~]` Corpus retrieval of uniques by PoB item trials (`generator.screen_uniques`) - `ROADMAP.md:250-251`.
- `[~]` Numeric skill options from scratch - `ROADMAP.md:259-261` (its own text is now stale, section 2g).
- `[~]` Archetype coverage (D56): CI / energy shield, low life, Righteous Fire stay uncovered, no run on the channel - `ROADMAP.md:523-538`.
- Harness: Warden (PoB id "Raider") ascendancy nodes do not materialize, the search skips it - `CLAUDE.md:243-244`, `src/junkroan/search/hypothesis.py:109` (verified still true).

---

## 2. Stale or contradicted

Each row: the statement, and the later decision or measurement that overrode it.

| # | statement (location) | overridden by (location) |
|---|---|---|
| a | "Self-degen: net life + ES change per second ... >= -100 (D34)" - `CLAUDE.md:223-224` | D63.3 "No degen while idle", `NetLifeRegen + NetEnergyShieldRegen + SelfCostPerSecond >= 0` without leech or recoup - `DECISIONS.md:1356-1361`, `ROADMAP.md:1171-1172` |
| b | "Sustain: regen + leech + recoup >= 85% of per-second cost per resource" - `CLAUDE.md:228-230` | D63.2: a channelling main skill sustains **100%** (`objective_select.with_skill_floors`) - `DECISIONS.md:1352-1355`, `ROADMAP.md:1173` |
| c | "`set_config` always writes Baseline + Conditional sets and **reloads the build from XML** (slow, ~0.5 s). Do not call it inside optimizer loops." - `CLAUDE.md:237-238` | 7.1h exact wins: "set_skills and set_config in place (469 -> 63 ms, 593 -> 166 ms, byte-identical exports)", landed 4cc3fce/aeb1e72/c591e01 - `ROADMAP.md:919-920, 937-939` |
| d | Judging protocol: "smoke it first on the two most sensitive references (~25 min), run the full 14-reference benchmark (~100 min)" - `CLAUDE.md:127-132` | The smoke set is six references (`ROADMAP.md:796-799`) and measures **5.3 h** (`artifacts/runs/progress.md`, `rules-smoke` 07:23 -> ETA 12:41); the benchmark is 32 references (D56, `DECISIONS.md:1011-1028`) and the two campaigns are 15.9 + 12.4 h |
| e | "Objective metric: use `CombinedDPS` from PoB, not `FullDPS`" - `CLAUDE.md:91-93` | D57: FullDPS **is** the objective for main skills whose instance count is a PoB stat (minions, totems; brands next) - `DECISIONS.md:1103-1110` |
| f | "list options (stance) are judged by PoB (D22/D24)" - `CLAUDE.md:210-212` | D62 amendment 3: "Pride is not a free MIN/MAX choice"; ramp-type list choices are computed from the ramp budget and written as a custom-mod block - `DECISIONS.md:1317-1331`, `ROADMAP.md:1175-1178` |
| g | "Still at PoB defaults: Pinpoint intensity, Momentum stacks, **Sigil stages**" - `ROADMAP.md:259-261` | D62 amendment 3 measured "spark's Sigil of Power 50 -> 1 stage and intensity 50 -> 4" - `DECISIONS.md:1323-1325` |
| h | "Kept behind `BuildPipeline.run(loop=True)` until it beats run E's medians" - `ROADMAP.md:830` | D58: "`loop=True` is no longer a flag", the chain is deleted - `DECISIONS.md:1149-1153`; `CLAUDE.md:219` says `--loop` is a no-op while every queue line still passes it (`artifacts/runs/queue.txt`) |
| i | 7.1h item (4) still lists "the TotalEHP floor at the author's (D61), D60 redone" as to do - `ROADMAP.md:908-909` | D63.1 landed the TotalEHP floor (`DECISIONS.md:1349-1350`) and D60 is marked "Redone (2026-09-18)" with 5 tests (`DECISIONS.md:1212-1228`); only "the author's row and ours under one lane" is left |
| j | Lane note: "the author's own config is 1.7-2.1x our conservative lane (rage 40, endurance + power charges, mines detonated, bleed vs moving, leeching)" - `ROADMAP.md:1221-1226` | Those very inputs became arithmetic since: rage (`ramp_inputs.rage_stacks`, Smite 5 of 30 where the rails typed 15 - `DECISIONS.md:1422-1427`), wither / poisons / mines (`DECISIONS.md:1317-1327`). The note's ratios must be re-measured on `rules-smoke` before it becomes an ask |
| k | "Runs count from: 20260916-0941 ... reset this stamp when the pipeline's shape changes so stale rows never count" - `ROADMAP.md:776-777` | D63's consequence: "every reference moves, so the numbers of the frozen campaigns are not comparable with anything built after this" - `DECISIONS.md:1384-1385`; `scripts/progress.py:124-198` still counts `new18-frozen` / `core14-frozen` as coverage |
| l | "Movement speed: `EffectiveMovementSpeedMod >= 1.2`" - `CLAUDE.md:208-209` | D55: the benchmark's movement floor gets the same 0.97 slack as life (the loot's boots reach 1.19x against an author at exactly 1.20x) - `DECISIONS.md:998-1000` |
| m | 7.4 acceptance "spread at most 10" - `ROADMAP.md:1273-1274`, definition of done item 2 (`ROADMAP.md:565-566`) | Measured: 29 of 32 references above 10 points, median 41.6 (`research/2026-09-18-seed-divergence.md:48`); and 7.3's own answer is best-of-K, not a narrower spread ("the search builds 3 seeds per finalist and keeps the best", `ROADMAP.md:1261-1263`). The two cannot both stand - see question Q1 |
| n | "Pyroclast ~3.3 hits per mine" and the VD orb count treated as settled - `DECISIONS.md:1311-1313` | Two sources disagree with each other and with the first report: PoEDB pass says overlap is **not found** and warns against an invented number (`research/2026-09-18-game-knowledge.md:57-59`), Reddit gives 2.34 + nova = 3.34 from one build (`research/2026-09-18-reddit-practice.md:14-18`); Arrow Nova + Shrapnel Ballista is "incompatible" in report 2 (`game-knowledge-2.md:67`) and "works, position-dependent" on Reddit (`reddit-practice.md:31-34`), and D62 already recorded "Arrow Nova on Shrapnel Ballista works" |

Verified **not** stale, for the reader's benefit: the Warden limitation (`CLAUDE.md:243-244` vs `search/hypothesis.py:109`), `set_items` as a whole-set XML round trip (`CLAUDE.md:239-240`), `equip_item` Boots-only (`CLAUDE.md:241-242`), the gem rails 18/0 (`CLAUDE.md:204-206` vs D23).

---

## 3. Proposed next items, ranked

Ranking rule used: (i) does it have to be in the build before `new18-rules` starts at ~17:59,
(ii) does it unblock a 7.4 acceptance criterion, (iii) hours saved or points moved per
agent-hour. "Queue hours" are benchmark wall hours at the machine's measured pace (a build
3,511 s median, `restarts-statistics.md:244`; 5 workers).

### P1. Decide and re-order what the campaign rerun must contain (0.5 h, no code)

- **Problem / evidence.** The queue runs `new18-rules` at ~17:59 and `core14-rules` after it
  (`artifacts/runs/progress.md`), while three number-changing candidates sit **behind** them:
  the cluster-candidates verdict (`queue.txt` lines `ballista-loop`, `ballista-loop-clusters`,
  scheduled Sat 22:17-Sun 01:17), the golem/curse drop (P2), and the one-lane author row (P5).
  Since D64.1 a run is frozen at one commit (`DECISIONS.md:1389-1400`), so anything merged
  after 17:59 does not reach the campaign and costs a third 28 h rerun. The ROADMAP's own work
  order says exactly this: "no situation where two weeks of runs are followed by a pipeline
  change that invalidates them" (`ROADMAP.md:786-794`).
- **What would change.** `artifacts/runs/queue.txt` order and the State block; possibly a
  short delay of the campaigns by the ~3 h ballista pair (2 runs x 3 builds, measured 1.4 h
  each on 3 workers, `progress.md`).
- **Measurement.** None of its own; the proof is that no number-changing commit lands after
  the campaign's start line, and that `ballista-loop` / `ballista-loop-clusters` produce their
  verdict on `impale_ballista` (3 seeds) against the pre-rules median 74.2
  (`seed-divergence.md:24`) before `new18-rules` begins.
- **Cost.** 0.5 agent-hour; +3 h of queue if the ballista pair moves ahead.
- **Kind.** A main-model decision plus a queue edit.
- **Must not overlap with.** Any other agent appending to `queue.txt` while it is being
  re-ordered; and with the `speed-both-2` gate line, whose `--revert-commit 5132b6c` needs a
  clean working tree (`ROADMAP.md:1316-1321`).

### P2. Drop golem and curse gems above their PoB limits at skeleton derivation (2-3 h, 1.2 h queue)

- **Problem / evidence.** The audit only warns: "PoB applies every enabled golem's buff
  whatever `ActiveGolemLimit` says ... so a build over the limit is scored on buffs it cannot
  have" (`optimizer/audit.py:426-430`), and the same for curses beyond `EnemyCurseLimit`
  (`audit.py:394-398`, "The Spark reference runs Conductivity and Sniper's Mark on a limit of
  1"). The frozen scan counted these live in our builds: "curses above the limit on 4, four
  golems for a limit of three on cold_dot" (`ROADMAP.md:654-657`). D63.7 dropped dead groups
  and non-applying supports at derivation (`DECISIONS.md:1372-1376`) but not these
  (`scripts/build_from_skeleton.py:34-64` drops only swap slots and `dead_support_group`).
  The State itself files it as a knowledge-level rule still to do (`ROADMAP.md:745-747`).
- **What would change.** `scripts/build_from_skeleton.py` (derivation keeps at most
  `ActiveGolemLimit` golem gems and `EnemyCurseLimit` curse/mark skills, lowest-value ones
  dropped by PoB's own judgement, not by name); the two audit checks become errors for our
  builds once the derivation cannot produce them.
- **Measurement.** `cold_dot` and `spark` x 3 seeds: the "golem limit" / "curse limit"
  warnings go to 0, and the honest number is recorded (a fall on `cold_dot` is the expected,
  correct direction - it currently counts a fourth golem's buff). Threshold: no audit warning
  of these two kinds in 6 builds; the ratio change is reported, not gated.
- **Cost.** 2-3 agent-hours of code + tests; 1.2 h of queue (6 builds / 5 workers).
- **Kind.** Code from a spec (the limits come from PoB stats, no game knowledge to invent).
- **Must not overlap with.** Any other task editing `build_from_skeleton.py` (P5 does not).

### P3. Fewer / cheaper kick draws (4-6 h, 5.3 h queue, gated)

- **Problem / evidence.** The two kicks cost more than half the loop and keep one draw in
  eight: kick joint 1,139 s per build, 34 kept of 251 (13.5%), **1,407 s per kept move**; kick
  tree 755 s per build, 24 of 201 (11.9%), 1,322 s per kept move
  (`research/speed/2026-09-18-audit-pipeline.md:169-177`). 7.1h already names this as the next
  approximate item ("next approximate: fewer kick draws, judged by the same gate",
  `ROADMAP.md:946-947`). Every draw currently runs by construction (D58,
  `DECISIONS.md:1144-1147`), which was the fix for a real starvation bug, so the change is a
  budget rule, not a removal.
- **What would change.** `optimizer/pipeline.py` `_improvement_loop` kick policy (draw count
  per kick, or a stop rule that spends the kick budget where the last kept draw came from);
  plus tree-audit finding 5, `swap_subtrees` re-trying the same subtrees every pass with no
  memory (613 s over 4 passes in one build, `speed/2026-09-18-audit-tree.md:52`), which is an
  exact win inside the same file.
- **Measurement.** `scripts/compare_runs.py rules-smoke <candidate> --min-delta -5` on the
  smoke set x 3 seeds (the standing gate shape, `ROADMAP.md:1459-1463`), plus median build
  seconds from `results.json`; accept at medians within 5 points and >= 20% less wall time.
- **Cost.** 4-6 agent-hours; 5.3 h of queue for the gate.
- **Kind.** Code from a spec, gated by an existing script.
- **Must not overlap with.** The `speed-both-2` flags (`--fulldps-shortcut`, `--skip-inert`,
  default-on in 5132b6c, `optimizer/pipeline.py:115-130`) whose gate is still pending: run
  after that verdict, or the two changes cannot be attributed.

### P4. Exact speed-ups left in the picks move (4-6 h, no gate)

- **Problem / evidence.** `rejudge_picks` evaluates every candidate support through a
  whole-build XML round trip: `set_skills` is 485 calls and **17.9%** of the post-fix build
  (`speed/2026-09-18-audit-pipeline.md:22, 41`), and the picks move costs 956 s per build at a
  32.7% keep rate (`:172`); the shortlist it builds is dead code (`:45`, `search/generator.py:656,
  679, 687`). These are exact wins (byte-identical exports), the class 7.1h already landed four
  of (`ROADMAP.md:937-939`).
- **What would change.** `search/generator.py` (shortlist actually used or deleted) and the
  `set_skills` path in `pob/session.py` / the worker, reusing the in-place setter that already
  brought `set_skills` 469 -> 63 ms.
- **Measurement.** Equality first: `export_xml` byte-identical before/after on one reference,
  and the same picks chosen; then wall time of one `stormbrand` build at `--workers 1`. No
  benchmark gate needed for an exact change (the precedent is `ROADMAP.md:937-939`).
- **Cost.** 4-6 agent-hours; ~1 h of machine time for the equality run (can share a core).
- **Kind.** Code from a spec.
- **Must not overlap with.** P3 (same loop, different files - coordinate the merge order),
  and any agent touching `pob/session.py` concurrently.

### P5. The author's row and ours under literally one lane (3 h measurement first, then 3-4 h code)

- **Problem / evidence.** The last open piece of 7.1h item (4): "the benchmark's ratio and
  `gap_decomposition`'s D/A disagree under 'one lane': poison_spark s2 78% vs 116%, bleed_bow
  s3 89% vs 104%, impale_ballista s2 45% vs 84% (per totem): the author's row keeps numeric
  inputs our build does not get" (`ROADMAP.md:649-652`; D61, `DECISIONS.md:1244-1245`). The
  author's row is re-scored under our lane through `derive_config` (`scripts/benchmark.py:239-247`),
  and `prefer_rules=True` only overrides where a rule exists (D50, `DECISIONS.md:874-878`).
- **What would change.** Possibly nothing: D62's ramp arithmetic now derives rage, wither,
  poisons-applied, mines-detonated and stack options on **both** sides
  (`DECISIONS.md:1317-1327`), which is exactly the asymmetry those three rows were made of. So
  the first task is a statistics pass over `rules-smoke`'s author rows against
  `new18-frozen`'s, not code.
- **Measurement.** For the three named references: `|ratio_lane - D/A from
  scripts/gap_decomposition.py| <= 5 points`. If the gap survives, the code change is in
  `scripts/benchmark.py` (the author's inputs the rules do not derive are listed in the report
  line, then zeroed on both sides).
- **Cost.** 3 agent-hours of statistics (no machine time: read `results.json` and the author
  memo), then 3-4 agent-hours of code and a 5.3 h gate only if the gap survives.
- **Kind.** Statistics, then code from a spec; the "which inputs may an author keep" part is a
  user decision (Q4).
- **Must not overlap with.** P2 (different file), P11 (uses the same script).

### P6. Restarts as the delivered product, and the stability metric that follows (1 h code, decision)

- **Problem / evidence.** Measured: expected best-of-K (median over six references) 153.6 /
  165.5 / 171.0 / 174.4 / 176.6 / 178.0 for K=1..6 - the third seed is worth +5.6 points and
  every seed after it +3.3 or less (`restarts-statistics.md:131-152`); construction-to-final
  rank correlation is 0.42 and the loop **widens** the spread on 5 of 6 references (41.7 ->
  60.8 points, `:208-226`), so a loop-only restart saves nothing. 7.3 already concludes "the
  search builds 3 seeds per finalist and keeps the best" and that "the benchmark's median-of-3
  understates what a request receives by ~17 points" (`ROADMAP.md:1261-1263`).
- **What would change.** `search/runner.py` (K=3 per finalist, if not already), and
  `scripts/progress.py:197-198`, whose stability unit is "references with seed spread <= 10
  points" - the quantity 7.4 demands (`ROADMAP.md:1273`) and that the data says is unreachable
  (29 of 32 above 10, `seed-divergence.md:48`).
- **Measurement.** Re-run the bootstrap on `new18-rules` + `core14-rules` (96 builds) and
  report best-of-3 per reference; the acceptance number becomes best-of-3 >= 100% of the
  author, with the spread reported, not gated (subject to Q1).
- **Cost.** 1-2 agent-hours of code + 2 h of statistics after the campaigns; no extra machine
  time (the campaigns already build 3 seeds).
- **Kind.** A user decision (Q1) plus small code and statistics.
- **Must not overlap with.** Nothing; but the decision must precede 7.4's acceptance run.

### P7. The fixed-point audit check (3-4 h code, 1 loop pass per build)

- **Problem / evidence.** Definition of done item 3 is "the improvement loop run again on a
  finished build moves the number less than 1%" (`ROADMAP.md:567-569`) and the item is open
  (`:1252-1254`). Two measurements say it is not free: 30 of 132 frozen builds stopped on the
  time budget (`:653`), and on the newer code 5 of 42 (`restarts-statistics.md:236-246`); the
  very first loop measurement found a "finished" chain build 12.8% short of its own fixed
  point (`ROADMAP.md:837-839`).
- **What would change.** `optimizer/audit.py` gains a check fed by one extra
  `_improvement_loop` pass at the end of `optimizer/pipeline.py`; a gain above 1% is an error.
- **Measurement.** First a statistics pass: run one extra pass on the finished builds of
  `rules-smoke` (6 references x 3 seeds) and report the gain distribution; only if the median
  gain is below ~1% does the check become an error (otherwise the finding is that the loop
  stops too early, which is P3's subject).
- **Cost.** 3-4 agent-hours; the extra pass costs ~120-800 s per build after the speed work
  (a pass of local moves went ~800 s -> ~120 s, `ROADMAP.md:941-943`).
- **Kind.** Statistics first, then code from a spec.
- **Must not overlap with.** P3 (both touch the loop); run P7's statistics on P3's output.

### P8. The loot roll as the origin of the spread (2 h code, 5.3 h queue, gated)

- **Problem / evidence.** "The tree greedy itself has no randomness ... 26 regrowths of six
  starting builds were bit-identical (Jaccard 1.000) ... The spread is born in gear pass 1
  (`loot.fill(seed=)`, the only thing the seed touches before the greedy) and amplified by the
  deterministic greedy" (`ROADMAP.md:1243-1251`); the first stage above 10 points is `tree
  greedy` on 19 of 29 references and `gear 2` on 8 (`seed-divergence.md:659-667`). Gear is
  cheap: gear pass 1 median 26 s, gear pass 2 58 s of a ~3,500 s build
  (`speed/2026-09-18-audit-pipeline.md:224-226`), and 92% of loop gear moves end with the
  incumbent (`:48`).
- **What would change.** `rails_default.json` `gear.loot_best_of_n` (200 today, line 76) or a
  best-of-M construction in `optimizer/pipeline.py`; D21's calibration (N=100 86%, N=200 111%,
  N=300 105%, `ROADMAP.md:150-154`) was measured on the author's tree, never against the
  spread.
- **Measurement.** Smoke set x 3 seeds at N=400 against `rules-smoke`: median of medians
  within -5 (the standing gate) **and** the per-reference spread; accept only if the spread
  median falls by >= 10 points at < 10% more build time.
- **Cost.** 2 agent-hours; 5.3 h of queue.
- **Kind.** Code from a spec + statistics; the accept/reject is a numbers call.
- **Must not overlap with.** P3 and P7 (the same gate slot - one gate at a time on one
  machine).

### P9. The research answers that still have no hook (4-6 h code + one brief)

- **Problem / evidence.** Three `[~]` rules carry an unfinished knowledge half:
  `mechanics/delivery_types.json` for mines/proxies/trigger breakpoints
  (`ROADMAP.md:1189-1191`), **Trauma's self-damage in the degen floor** (`:1192-1194`;
  static_strike carries "752 physical damage per attack at 3,478 life",
  `readings/2026-09-18-frozen-campaigns-part1.md:20`), and the corpse-cycle conditions
  (`:1215-1217`). The research now gives numbers with sources: Trauma is a self-hit of
  `146 x stacks` at gem 20, not a per-second degen, and "no source establishes that PoB
  includes Trauma in NetLifeRegen; test it in the pinned runtime"
  (`research/2026-09-18-game-knowledge.md:65-67`); the shock formula
  `0.5 x (hit/threshold)^0.4` with min 5% / max 50% (`:23-25`); Corpse Pact
  `4% x min(consumed in 4 s, 50)` and Desecrate 5 per cast, cap 10, Undertaker 12
  (`game-knowledge-2.md:27-29`).
- **What would change.** `mechanics/notes.json` + `self_cost.py` (Trauma into the D63.3 idle
  floor after a PoB probe of whether PoB already counts it), `config_rules.py` (corpse
  conditions behind creator+consumer), and the shock magnitude as a derived value rather than
  an assumption.
- **Measurement.** `static_strike` and `archmage_volatile_dead` x 3 seeds: the degen floor
  binds where the self-hit is real (static_strike's number falls or its tree changes), corpse
  conditions appear only with a creator in the build; thresholds are "no audit error, no
  unproven toggle", the ratio is reported.
- **Cost.** 4-6 agent-hours; 1.2-2 h of queue; one GPT brief if the PoB probe shows Trauma is
  not modelled (`scripts/gpt_research.py`, the D62 procedure).
- **Kind.** Code from a spec, plus a research brief for GPT, plus the PoB probe (a main-model
  verdict on what the probe means).
- **Must not overlap with.** P2 (`build_from_skeleton.py`) and P5 (`benchmark.py`); this one
  lives in `mechanics/` + `config_rules.py`.

### P10. Unblock Warden in the harness (3-5 h, no gate)

- **Problem / evidence.** "`set_tree(ascendancy_nodes=...)` reports the nodes did not
  materialize; the search skips Warden until fixed" (`CLAUDE.md:243-244`), still true in
  `src/junkroan/search/hypothesis.py:109` ("plus Warden (PoB id 'Raider'), whose nodes the
  worker cannot yet allocate"); the worker already knows the legacy-id quirk
  (`pob/headless_runtime_worker.py:3214`). The search's own acceptance says "all 20 ascendancy
  candidates (Warden skipped)" (`ROADMAP.md:265-266`), so 1 of 19 ascendancies is invisible to
  every request.
- **What would change.** `pob/headless_runtime_worker.py` Lua strings + `session.set_tree`;
  `hypothesis.py`'s skip list.
- **Measurement.** A readback test: after `set_tree(ascendancy_nodes=...)` for Warden the
  allocated ascendancy node ids equal the requested ones (a fast test, no benchmark); then one
  search that includes Warden finishes with a number.
- **Cost.** 3-5 agent-hours; no queue hours.
- **Kind.** Code from a spec (harness).
- **Must not overlap with.** P4 (also touches the worker) - sequence them.

### P11. Re-measure the request path once on the rules code (0.5 h setup, 2-3 h queue)

- **Problem / evidence.** 7.4 item 3 requires `junkroan build` on three requests under 2 h
  each (`ROADMAP.md:1277-1279`); the last search acceptance numbers are from 2026-09-13/14 and
  D51 explicitly says they were measured at 107 passive points and "are to be re-measured"
  (`DECISIONS.md:904-906`); `ROADMAP.md:453-461` records only Smite as re-measured, "the other
  four skills still to re-measure". Since then the chain was deleted (D58), the floors changed
  (D63) and a build costs 61-69 min (`research/2026-09-17-build-speed-hardware.md:10`), so a
  10-skeleton request is two waves on 5 workers (`:421-432`).
- **What would change.** Nothing in the code; this is a measurement that tells 7.4 whether the
  request path is anywhere near 2 h, and whether restarts (P6) fit inside it.
- **Measurement.** One request (`python -m junkroan.cli build --skill ... --level 80`) of ~10
  skeletons, 1 seed, wall time and the finalists' audit; threshold = the 7.4 criterion (2 h)
  and audit-clean finalists.
- **Cost.** 0.5 agent-hour to queue; 2-3 h of machine time; it competes with the campaigns, so
  it belongs after `core14-rules` or on the idle Sunday slot.
- **Kind.** A queue run plus statistics.
- **Must not overlap with.** The campaign rerun (same 5 workers).

### P12. Imbalanced Guard and armour as a mapping-view number (2-3 h, no rerun)

- **Problem / evidence.** The user asked for it twice in the reading ("нужен ресерч и
  аналитика на основе разных хитов чтобы понимать когда этот кистоун действительно
  использовать", `readings/2026-09-18-frozen-campaigns-part1.md:17`), and D62's amendment
  already settled the form: "Imbalanced Guard is not a fact but a mapping-view number:
  physical damage reduction against a 1,000 and a 3,000 hit from the build's armour, with and
  without the keystone (`A/(A+5H)` against `min(0.5, 2A/(2A+5H))`)" (`DECISIONS.md:1313-1315`;
  the same formula and the crossover `A = 5H` in `research/2026-09-18-game-knowledge.md:41-43`,
  the community numbers in `reddit-practice.md:47-50`).
- **What would change.** `optimizer/mapping.py` (a line in the "Mapping (not scored)" section
  that already exists, `ROADMAP.md:1499-1510`) and `optimizer/explain.py`.
- **Measurement.** Two arithmetic lines per build from PoB's `Armour`; a fast test with a
  known armour value. No benchmark, no objective change, so it can land during a campaign.
- **Cost.** 2-3 agent-hours; 0 queue hours.
- **Kind.** Code from a spec (the formula is already decided; nothing new to judge).
- **Must not overlap with.** Nothing.

### Parallelism summary

Non-overlapping lanes that can run at once (at most ~4 PoB-heavy agents beside the 5 benchmark
workers, `ROADMAP.md:1408-1414`): **A** = P2 (`build_from_skeleton.py`) · **B** = P4 + P10
(`session.py` / worker, sequenced) · **C** = P3 + P7 (`pipeline.py`, sequenced, one gate slot)
· **D** = P9 (`mechanics/` + `config_rules.py`) · **E** = P5 + P11 (`benchmark.py`, statistics
first) · **F** = P12 + P6 (`mapping.py`, `progress.py`; no PoB). P1 is the main model's own
decision and gates A, C, D.

---

## 4. Questions only the user can answer

**Q1. Stability: per-seed spread, or the best of three?**
7.4 demands "spread at most 10" per reference (`ROADMAP.md:1273-1274`); the measurement says 29
of 32 references are above 10 (median 41.6, max 109.1, `seed-divergence.md:48`) and that the
loop widens the spread on 5 of 6 references (`restarts-statistics.md:226`), while the answer
7.3 adopted is to build 3 seeds and keep the best (`ROADMAP.md:1261-1263`).
*If the criterion stays per-seed*: the prototype cannot be declared done without a research
programme against variance that the data says lives in the loot roll and the loop's draws -
weeks, and the 7.3 restart decision becomes pointless. *If the criterion becomes best-of-3*:
7.4 is measurable on the campaigns already queued, the delivered build is what a request
returns anyway, and the risk is that a reference with one lucky seed passes while its typical
build is weak (mitigated by also reporting the median).

**Q2. The loop's wall-clock budget after the speed work: faster campaigns, or better builds?**
`--loop-seconds 5400` is a wall-clock budget (`hardware.md:131-144`); 20% of builds hit it
(`:148-153`), and after the speed work a pass of local moves costs ~120 s instead of ~800 s
(`ROADMAP.md:941-943`), so the same 5,400 s now buys ~6 passes instead of 3 on the same build
(2,238,757 -> 2,289,728, +2.3%). *Keep 5,400*: campaigns stay 28 h, the builds at the cap get
better. *Cut it proportionally (~2,000-3,000 s)*: campaigns fall towards 10-15 h and iteration
doubles, at the cost of the 20% of builds that were still improving. This is a trade the
numbers cannot settle alone - it is about how fast the project wants to iterate.

**Q3. Money for machine time.**
D61 recorded "no money for a server" (`DECISIONS.md:1247`), but the research gives concrete
figures: a campaign of 96 builds costs about **13 USD** on an hourly 48-core box, a one-day
trial about **26 USD**, throughput 9-12x, single-build latency at most 1.36x
(`hardware.md:10-20`, `:403-419`). *No*: the cadence stays one campaign per 28 h and every
gate costs 5.3 h, which is what makes P1's sequencing painful. *Yes, hourly for campaigns
only*: the 28 h campaign becomes ~2.7 h, gates become ~30 min, and rules can be proven one at
a time instead of in bundles - the single biggest change available to the schedule. (The
runtime is Windows-only, `hardware.md:17`, which the price above already includes.)

**Q4. What may the author's row keep that our build does not derive?**
The benchmark re-scores the author under our lane, but any numeric input no rule derives
survives from the author's own build (D50, `DECISIONS.md:874-878`); that is the whole of the
78 vs 116 / 89 vs 104 / 45 vs 84 disagreements (`ROADMAP.md:649-652`). D62's ramp arithmetic
removed most of them, and what remains are play assumptions PoB cannot compute (e.g.
`multiplierPoisonAppliedRecently` 20 typed by the poison_spark author,
`readings/...part2.md:46`). *Both sides derived, nothing typed*: like-for-like, but we may
score the author below what they actually played. *Author keeps their typed numbers*: our
ratio understates by up to 38 points and the acceptance criterion is measured against an
assumption we forbid ourselves. A third option is to report both and gate on the derived one.

**Q5. The two pending hit-count facts: keep them pending, or approve a conservative number?**
Sources disagree and PoB cannot compute either. Pyroclast overlap: PoEDB-based pass says "not
found ... do not use an invented 3/5" (`game-knowledge.md:57-59`), Reddit gives 2.34 + nova =
3.34 from a single build (`reddit-practice.md:14-18`), D62 recorded ~3.3 "pending generality"
(`DECISIONS.md:1312-1313`). Perforate Blood Stance overlap: Reddit says 1-2 usually, 3 when
optimized (`reddit-practice.md:39-42`), PoB's default input is 3, `mechanics/notes.json`
records 1 (`DECISIONS.md:1329-1331`). *Keep pending (optimistic lane only, per D62)*: these
two references are scored at the conservative floor and will read as weak against their
authors. *Approve a conservative number (say 2 and 1)*: both references move by a factor of
2-3 and the number carries a source but not generality. Approving also sets the precedent for
every future multi-hit skill.

---

## 5. Method

I read the four instructed documents end to end (`CLAUDE.md`, `docs/ARCHITECTURE.md`,
`docs/ROADMAP.md` in four passes covering all 1,536 lines, and `docs/DECISIONS.md` lines
798-1428, which is D50 through D64), all three files under `docs/readings/`, and the six
top-level files under `docs/research/` (the 64 KB hardware report by its summary, sections
A3-бис, A4, B3 and B4; the briefs folder was excluded as instructed). Every open checkbox was
located mechanically (`grep -n -- "- \[ \]\|- \[~\]"` over the ROADMAP) so no item was missed,
and each was then read in place for its named proof. Claims about the current code were
verified by reading the code rather than the prose: `optimizer/audit.py` (which limits are
errors and which warnings), `scripts/build_from_skeleton.py:34-84` (what skeleton derivation
drops), `optimizer/pipeline.py:115-130` (the two speed flags and their defaults),
`optimizer/rails_default.json` (loot N, bandit, ramp), `scripts/benchmark.py:59-260` (how the
author's row is built), `scripts/progress.py:124-198` (how coverage and stability are counted)
and `search/hypothesis.py:109` (Warden). Run state came from `artifacts/runs/queue.txt` and
`artifacts/runs/progress.md` as of 09:55 today. Numbers are quoted from the documents that
measured them, never recomputed or estimated: where two documents disagree (Pyroclast overlap,
Arrow Nova) both are cited and the disagreement is raised as a question rather than resolved
here. No PoB run, no git command and no edit to an existing file was made; cost estimates are
my own judgement from the sizes of comparable landed changes and the measured machine pace
(3,511 s per build, 5 workers) and are the least reliable figures in this report.
