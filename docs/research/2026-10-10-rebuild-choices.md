# Rebuild choices: how the search judges a choice that pays off only after the build is rebuilt around it (#682)

Part 1 (Q1) and part 2 (Q2) read by a helper agent from code and existing run logs, 2026-10-10; no new PoB run.

## Q1. Today's treatment per choice kind

| choice kind | treatment today | file:line | note |
|---|---|---|---|
| Structural keystone (Blood Magic, Crimson Dance, Mind over Matter, Chaos Inoculation, Eldritch Battery) | full rebuild WITHOUT it (D40): the finished build is re-run through the whole pipeline with `forbid_keystones=[k]`, screened, then built in full if the screen holds | `docs/adr/0040-structural-keystones-are-decided-by-rebuilding-without-them.md:10-18`; `scripts/search.py:370-381`; `src/junkroan/optimizer/pipeline.py:299`, `:1619`; benchmark `scripts/benchmark.py:1420-1432`, `:1439` | no "with it forced" counterpart; request-fixed keystones are not varied (`scripts/search.py:373-376`) |
| Build-defining / stacker unique | two stages: (1) greedy selection, each unique as one `trial_stats` item trial on the unchanged build, must beat the current item by `min_gain`; (2) the winner goes into a variant skeleton rebuilt through `pipeline.run` (screen, then full) | (1) `src/junkroan/search/generator.py:1242-1286` (trial `:1273-1284`); (2) `scripts/search.py:283-288`, `:398-413`, `:416-437`; `src/junkroan/search/runner.py:98-122`, `:147-160` | the owner's observation is partly refuted: a picked unique is rebuilt around; the gap is selection: a unique with no gain on the OLD build's tree and gear never reaches the variant stage |
| Unique rails | at most `max_uniques` = 2, only "core" availability, req level <= 70 | `src/junkroan/optimizer/rails.py:169`, `:216-217`, `:285-290`; `generator.py:1257-1263` | whether Mageblood / Darkness Enthroned pass the "core" filter: not known |
| Unique variant survival | the variant's screen value must reach 0.5 x the best finalists' screen, else dropped without a full build | `scripts/search.py:418-437`; `runner.py:184-197` | can drop a unique whose build comes together slowly at screen depth (comment cites a Smite sceptre, `search.py:416-417`) |
| Ascendancy | whole-skeleton enumeration: one skeleton per ascendancy, all screened, top K built in full; ascendancy nodes picked greedily per skeleton | `src/junkroan/search/request.py:211-227`, `:276-287`; `scripts/search.py:226-263`, `:275-276`; `generator.py:470` | no ascendancy variant is made later from a finished build |
| Main-skill supports | greedy swap on the finished build, no rebuild: `repick_supports` once at full depth, then the loop's `picks` move re-judges one support at a time (keeps a swap at `min_gain`) | `pipeline.py:534-544`; `improvement_loop.py:1332-1354`; `generator.py:1092-1131`; `scripts/search.py:303` | tree and gear not rebuilt per support |
| Aura / utility set | same: one greedy `pick_utilities`, then `rejudge_picks` and `drop_reserving_group` | `pipeline.py:546-555`; `generator.py:900`, `:1008`, `:1092`; `improvement_loop.py:1347-1352` | Blood Magic / aura coupling handled only through the D40 keystone rebuild |
| Mind over Matter / CI / Eldritch Battery | as keystones (first row); with MoM a floor rail `MoMCastsAfterMaxHit` constrains it; CI: no separate treatment found | `src/junkroan/optimizer/keystone_floors.py:10`, `:38`; `rails.py:219`, `:320-333`; `generator.py:1017` | no "rebuild with MoM forced"; whether the tree optimizer ever considers taking MoM / CI: not known (`tree_optimizer` candidate logic not read) |
| Weapon type | whole-build rebuild for the 2 runner-up weapon types (D41) | `scripts/search.py:382-396`; `runner.py:163-181` | same machinery as keystone variants |

What Q1 says: a rebuild around a choice exists for keystones (only "without"), unique mutations and weapon alternatives, all through one path (copy the finished skeleton, forbid or change one thing, screen, full build; `scripts/search.py:362-437`). Selection of a unique is greedy on the old build. Supports and auras are greedy swaps on the built tree and gear. Not known: whether Mageblood / Darkness Enthroned pass the "core" filter; whether the tree optimizer ever forces in MoM / CI.

## Q2. What a D40 variant costs and how far it moves (source: `artifacts/benchmark/20261005-1220-gate-20261005/`, rows and decoded `*.pob.txt`)

- Count: 19 `-no-` variants in the weekly gate (Roiling Tempest 6, Mind over Matter 4, Eldritch Battery 3, Imbalanced Guard 3, Bitter Frost 1, Arrow Dancing 1, Versatile Combatant 1) next to 42 base rows (14 builds x 3 seeds). `20261001-2027-392-before-s4` holds 23 `-no-` rows among 65 (not tabulated).
- Minutes: row field `seconds` = 58 to 101 min, median about 70 min; a base build takes 48 to 95 min, so a variant costs about a full base build. 14 of 19 ended on `loop_stop=time` (the 40 min loop budget, `loop_seconds` 2400 in `args.json`) = 40 min loop + about 30 min construction; 5 converged, 58-70 min vs 65-101 min for the rest.

| variant | min | nodes changed | gear slots changed | gems | value change | tree-greedy stage vs base |
|---|---|---|---|---|---|---|
| poison_spectral_throw s6 no Arrow Dancing | 74 | 2/108 | 0/11 | 0 | 0.0 % | 1.00 |
| smite s4 no Versatile Combatant | 58 | 29/109 | 3/10 | 0 | +4.7 % | 1.00 |
| stormbrand s6 no Roiling Tempest | 69 | 62/110 | 7/12 | 2 | -0.6 % | 0.87 |
| stormbrand s4 no Roiling Tempest | 65 | 68/110 | 7/12 | 2 | -2.6 % | 0.87 |
| spark s5 no Roiling Tempest | 67 | 47/107 | 7/12 | 1 | -2.6 % | 0.72 |
| spark s4 no Roiling Tempest | 70 | 48/107 | 6/12 | 0 | -17.2 % | 0.57 |
| cold_dot s4 no Bitter Frost | 70 | 66/112 | 9/12 | 1 | -16.1 % | 0.61 |
| bleed_bow s4 no Imbalanced Guard | 60 | 62/110 | 5/10 | 0 | -21.4 % | 1.00 |
| bleed_bow s5 no Imbalanced Guard | 62 | 64/110 | 5/10 | 0 | -17.1 % | 1.00 |
| absolution_minions s5 no Eldritch Battery | 86 | 81/109 | 9/12 | 0 | +25.8 % | 1.22 |
| absolution_minions s4 no Mind over Matter | 88 | 96/108 | 9/12 | 0 | +93.0 % | 0.97 |
| summon_raging_spirits s5 no Mind over Matter | 78 | 82/109 | 3/10 | 2 | +176.6 % | 1.00 |

(7 more variants follow the same pattern; "value" = the row's `ours`, taken as the CombinedDPS-based lane value, not checked.)

What Q2 says: 1 of 19 ended almost identical to its base (Arrow Dancing, 2 nodes, 0 slots, 0.0 %); 3 more moved under 5 % in value; the other 15 changed 46-96 of ~108 nodes and 3-9 slots, a near-total rebuild; value moved -21 % to +177 %, in both directions (MoM / Eldritch Battery variants on absolution and summon_raging_spirits came out far above the base, so the base was not at its optimum). Cheap signal: none found; the stage values (`tg`, `g1`) and `tree_churn` do not separate the identical one from the far-moved ones; one near-identical sample cannot show a stage-based predictor. Not known: whether a small first-stage delta predicts a small final move.

## Q3. Outside research (GPT-5.6 Terra, `--no-reddit`; full report `docs/research/2026-10-10-rebuild-choices-gpt.md`, brief `docs/research/briefs/2026-10-10-rebuild-choices.md`)

What the sources say, one line per question of the report:
1. Bilevel / two-stage: systems model the rebuild explicitly, but practical AutoML cuts the cost by truncating the inner solve (Franceschi 2017), relaxing the outer choice (DARTS: 1.5-4 GPU-days) or sharing inner state across candidates (ENAS, about 1,000x cheaper than standard NAS in its setting); each is credible only under conditions the source states (differentiable inner loss, a shared supergraph, a final retrain).
2. Cheap proxies: they work when a fidelity relationship, a learning curve or a calibrated surrogate exists (multi-fidelity Bayesian optimization, BOHB, MFES-HB 3.3-8.9x over BOHB); the sources give no universal proxy for a discrete, rebuild-dependent game choice.
3. Screening before the full run: Successive Halving / Hyperband pay when low-budget scores separate winners from losers (SH: over an order of magnitude wall-clock on a 100-arm task); they mis-rank when the eventual value is delayed, close, noisy or structurally different at higher fidelity, which is the shape of a rebuild-dependent choice.
4. Game tools: Path of Building = high-fidelity what-if per edit, no whole-build outer search; POEMOOTREES = passive tree only; poega = genetic search (rebuild behaviour not documented); Genshin Optimizer = exact combinations with symbolic pruning; poe2-build-mcp = explicit whole-build commit-and-max (about 1-3k engine evaluations, 1-3 minutes in its example). No opened source gives a benchmarked general answer.
5. Fit: no common candidate-count threshold; the table at the end of the report gives cost, needs and the source's own failure mode per method.

## One table: choice kind x treatment x cost x count

| choice kind | today (Q1) | measured minutes per candidate | candidates in the latest weekly run (gate-20261005) |
|---|---|---|---|
| keystone the finished tree took | full rebuild without it (D40) | 58-101, median about 70 (a base build 48-95) | 19 variants (+42 base rows) |
| build-defining unique | greedy item trial on the old build; winner rebuilt as a variant | not measured here (no unique-variant rows tabulated) | not counted |
| ascendancy | one skeleton each, screened, top K built | not measured here | not counted |
| main-skill supports / auras | greedy swaps on the built build (`rejudge_picks`), no rebuild | not measured here | not counted |
| Mind over Matter / CI | as keystones (drop only, never forced in) | as keystones | 4 MoM variants of the 19 |

## Q4. Proposed rule and its cost (a proposal from the facts above, not a measured result)

- Keep the full rebuild for a keystone variant: 15 of 19 variants changed 46-96 of about 108 nodes and 3-9 gear slots and moved the value from -21 % to +177 %, so a full rebuild was what answered; only 1 of 19 (about 5 %) was a near-copy (2 nodes, 0 slots, 0.0 %). A cheap check that spares that one saves about 70 minutes of 19 x 70 = about 22 hours of variants in a run (about 5 %) and no cheap signal separating it was found (stage values and `tree_churn` do not), so it is not worth a rule today.
- The gap is the unique: its selection (`generator.py:1273-1284`) is a trial on the old build's tree and gear, so a stacker that needs its build built around it never reaches the variant stage. Rule: a unique that fails `min_gain` on the old build gets one cheap repair trial (re-run the tree-greedy stage on the build with the unique forced) before the test is decided; only a unique whose repaired trial beats the current item goes on to the existing variant path (screen at 0.5 x the best finalists, then full build). Cost per candidate: one tree-greedy stage on top of today's trial (its minutes are not known: no per-stage timing was read), plus one variant (about 70 minutes) only for the few that pass; at most `max_uniques` = 2 variants per finalist.
- Supports and auras: no change proposed; the sources and the logs here give no evidence that they need a rebuild.
- The one measurement the rule rests on: the minutes of the tree-greedy stage inside a variant (per-stage seconds are in the rows' `stages`, not read here).

## Draft tickets for the lead (write-ticket format to be applied by the lead)

1. **Time the stages of a D40 variant** (`area:builds`, research, no code): from the 19 variant rows of gate-20261005 and their logs, minutes per stage (tree greedy, gear pass 1, tree rebuilt, loop) so the cost of a cheap repair trial is a number; result: a table, 19 rows.
2. **A unique gets a repair trial before `min_gain` decides it** (`area:builds`, kind B/A by D113): the rule above; test: a bug-specific test on a stacker-style unique that fails `min_gain` on the old build and wins after repair, plus the trace counter (generated and evaluated of the repair trial > 0) and the replay bench on one stacker build; waits for ticket 1's number.
3. **Is Mageblood / Darkness Enthroned inside the "core" availability filter?** (`area:builds`, find): read `uniques.json` availability and `rails.py:285-290` for both and say whether either can be tried at all; one-line answer per unique.
