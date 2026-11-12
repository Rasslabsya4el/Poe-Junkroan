# Issue #606: ailments, boss thresholds, the shock ramp, and the drafted implementation sub-issues

Unit 3 of 3 (synthesis). Facts live in two unit notes: `2026-10-06-ailments-pob-modelling.md` (PoB source, file:line, cited here as "modelling note") and `2026-10-06-boss-ailment-thresholds.md` (poedb, cited as "boss note"). Numbers of rows 2-4 were measured on 2026-10-06 in one PoB session (PoB 2.67.2, pinned runtime): our build `artifacts/benchmark/20261005-1220-gate-20261005/hit_penance_brand-s4.pob.txt` (the core seed, Baseline lane) and the author's `tests/fixtures/tuadh_329/hit_penance_brand.pob.txt`. Probe scripts were scratch (not committed); every number below is reproducible by the steps named.

## Row 1. The nine ailments (rule, formula, duration, stacking, PoB)

Full file:line is in the modelling note (Q1, Q2, Q3); this is the summary. CO = vendor/pob/source/src/Modules/CalcOffence.lua, CP = CalcPerform.lua, CFG = ConfigOptions.lua, D = Data.lua.

| ailment | application rule | magnitude | duration | stacking | PoB config / output |
|---|---|---|---|---|---|
| Shock | chance on hit + Enemy ShockChance; 100 % on crit (CO:4125) | `50 * (d/T)^0.4 * ShockEffectMod`, max 50 (D:421), min 5 | 2 s | strongest one (CP:3540); ShockCanStack: `ShockStacks` (CP:3457) | `conditionEnemyShocked` CFG:1917, `conditionShockEffect` CFG:1921 -> ShockVal; outputs ShockChance, CurrentShock |
| Chill | forced 100 on hit (CO:4110); also on crit | same formula, max 30 | 2 s | one | `conditionEnemyChilled`, `conditionEnemyChilledEffect` CFG:1873/1881 |
| Freeze | chance on hit (10 here), 100 on crit (CO:4125) | none: duration only, 0.3 s min .. 3 s max, "no more than baseVal*20*FreezeDurationMod threshold" (CO:5286) | by hit | one | FreezeChance, FreezeDurationMod; no effect input |
| Ignite | chance on hit, 100 on crit | damage: `0.9 * base * effectMod` per s (Data/Misc.lua:260), no threshold | 4 s | one unless IgniteCanStack (CO:4895) | IgniteDPS, TotalIgniteDPS; no value input |
| Scorch | NOT 100 on crit (alt ailment, D:422-424, CO:4121): needs its own Enemy ScorchChance / IgniteCanScorch | `50 * (d/T)^0.4 * mod`, max 30 | 4 s | one; ScorchCanStack | `conditionEnemyScorched` CFG:1858 (ifFlag inflictScorch), effect CFG:1862 |
| Brittle | as Scorch (needs source) | `10 * (d/T)^0.4 * mod`, max 6 | 4 s | one | CFG:1905/1909 (ifFlag inflictBrittle) |
| Sap | as Scorch (needs source) | `(100/3) * (d/T)^0.4 * mod`, max 20 | 4 s | one | CFG:1932/1936 (ifFlag inflictSap) |
| Poison | chance on hit; needs a hit | damage, `0.30 * base` per s, no threshold | 2 s | many (stacks, CO:4602-4618) | PoisonDPS, TotalPoisonDPS, `multiplierPoisonOnEnemy` |
| Bleed | attack only; BleedChance | damage, `70 %` per s, no threshold | 5 s | many (CO:4309-4333) | BleedDPS, BleedStacks, `Multiplier:BleedStacks` |

Two facts matter for the rest of this note:
1. PoB never derives the shock (or Chill / Scorch / Brittle / Sap) a build's own hits earn. `val.effect` (the formula above) runs once, inside `if breakdown` (CO:5323), and sets nothing. The enemy carries a shock only from the typed config value or a guaranteed source (modelling note, headline 1-3).
2. "Is the enemy Shocked?" with no value typed sets only `Condition:Shocked`. Measured on our build: toggle on, no value: `CurrentShock` 0, but `CombinedDPS` 810,564 -> 842,986 (+4.0 %): the build has "against Shocked Enemies" mods that key on the condition. No 1 % shock appears (the owner's recollection is not what PoB does for an enemy; the player's own shock does default to 15, CP:851).

## Row 2. Boss thresholds and the number our config implies

PoB's own number (read from the live data tables in the same runtime; products: modelling note Q3). Formula (CO:5208-5218): `monsterAilmentThresholdTable[lvl] * 7.68 * mapLevelBossLifeMult[lvl] * mapLevelBossAilmentMult[lvl] * (1 + AilmentThreshold MORE/100)`, Guardian/Pinnacle preset MORE = 404 (CFG:2131), so factor 5.04.

| enemy level | table | BossLifeMult | BossAilmentMult | PoB threshold (Guardian/Pinnacle) |
|---:|---:|---:|---:|---:|
| 82 | 14,425 | 17.20 | 0.47 | 4,513,712 |
| 83 | 15,319 | 19.64 | 0.47 | 5,473,455 |
| **84 (our config)** | 16,265 | 21.46 | 0.47 | **6,349,995** (read, exact; identical on both builds) |
| 85 | 17,268 | 21.46 | 0.47 | 6,741,575 |

poedb records (boss note, "Final Reference Table"): Shaper, Uber Elder, Sirus, Maven at level 84: 6,957,767 (504 %); Elder, 4 Shaper Guardians, 4 Conquerors' "Uber" records, level 83: 6,002,899; Catarina 6,014,809; Elder Guardians level 82: 4,957,252; Black Star 3,501,691 (294 %); Infinite Hunger 4,525,995 (380 %); Exarch 4,155,333 (301 %); Eater 4,058,698 (294 %); three Incarnations level 83: 9,528,410 (800 %), level 85: 11,766,571. Level-85 Uber rows exist only for the Incarnations.

Comparison at equal level: poedb 504 % records / PoB: level 82 4,957,252 / 4,513,712 (-8.9 %); level 83 6,002,899 / 5,473,455 (-8.8 %); level 84 6,957,767 / 6,349,995 (-8.7 %). PoB's Guardian/Pinnacle preset sits a uniform ~8.8 % below the 504 % records; it is below the 800 % Incarnations and above the 294-380 % Exarch, Eater, Black Star, Infinite Hunger.

The average Guardian / Pinnacle (one vote per boss, 24 boss records, levels 82-85 as published): mean 6,065,423, median 6,002,899. Pinnacles only (10 records): mean 6,969,027, median 6,957,767. Guardians only (14): mean 5,419,992, median 6,002,899.

Proposal: PoB's own value is already fair. 6,349,995 is +4.7 % over the all-boss mean (6,065,423) and +5.8 % over the median; shock scales as threshold^-0.4, so the gap moves a 16.5 % shock to 16.2 %. Keep `enemyIsBoss = Pinnacle` at level 84 and add no `AilmentThreshold` override. The number our config implies is 6,349,995 (and the optimizer must read it from PoB, not type it). If the owner prefers the exact average: a MORE of 381 % instead of 404 % gives 6,065,000; not recommended (a second number that must follow every PoB bump). Caveat: the level-84 rows are 504 % bosses only; the lower records (Exarch, Eater) and the 800 % Incarnations cancel out in the average.

## Row 3. The shock ramp inside 2.5 s

Inputs, all read from PoB (Baseline lane, toggle on with value 0, so the `Condition:Shocked` mods count): `LightningHitAverage` 51,084.54, `LightningCritAverage` 352,024.88 (at crit chance 73.815 %), `ShockChanceOnHit` 10, `ShockChanceOnCrit` 100, `ShockEffectMod` 1, `MaximumShock` 50, `HitTime` 0.8368 s (`HitSpeed` 1.195), threshold T = 6,349,995.

Per-hit damage that PoB feeds to the formula (CO:4209-4218, 5306) is the chance-weighted blend: `d0 = (Hit * 10 * (1-c) + Crit * 100 * c) / (10*(1-c) + 100*c)` with c = crit chance = 355,314. A typed shock adds to the other enemy DamageTaken increase, so hit k is `d_k = d0 * (1 + S_{k-1}/(100 + D))`, D = the enemy's other DamageTaken increase, measured by typing 40: LightningHitAverage 51,084.54 -> 66,802.86 gives 1 + 40/130, D = 30 (author's build: 25).

Iteration (hit k at t = (k-1) * HitTime; 3 hits start before 2.5 s, the 4th at 2.51 s; shock lasts 2 s, so each hit meets the previous one's shock):

    S_0 = 0
    d_k = d0 * (1 + S_{k-1}/(100+D))
    S_k = min(MaximumShock, 50 * (d_k/T)^0.4 * ShockEffectMod)

Worked example, hit_penance_brand (our s4):

| hit k | t (s) | shock it meets S_{k-1} | damage d_k | shock it earns S_k |
|---:|---:|---:|---:|---:|
| 1 | 0.00 | 0 | 355,314 | 15.78 |
| 2 | 0.84 | 15.78 | 398,443 | 16.52 |
| 3 | 1.67 | 16.52 | 400,466 | 16.55 |
| steady (k -> inf) | | 16.55 | | 16.55 |

Effective average over the window: mean shock met per hit 10.77; time-weighted over 2.5 s 10.74; steady state 16.55. A crit-only sequence (d = CritAverage) gives 10.80 and 16.72, so the blend is not the driver. The ramp converges after 2-3 hits because the exponent is 0.4: hit 1 gives 95 % of the steady value.

Typed check (set `conditionEnemyShocked` true and `conditionShockEffect` in the same session, read PoB):

| typed shock | LightningHitAverage | CombinedDPS | note |
|---:|---:|---:|---|
| (toggle off, today's Baseline) | 49,119.75 | 810,564 | no `Condition:Shocked` |
| 0 (toggle on) | 51,084.54 | 842,986 | condition mods only |
| 11 (ramp mean, rounded) | 55,407.08 | 914,316 | +8.5 % over 0; +12.8 % over today |
| 16 (about S_1) | blend 399,045 | 946,738 | ratio to 0: 1.12308 = 1 + 16/130 exactly; ramp's d_2 at 16.00 is 399,046 |
| 17 (steady, rounded) | | 953,223 | |

So the typed shock moves the damage exactly as the iteration says (d_2 check: 399,045 read vs 399,046 computed). DPS is damage x rate, so the number to type for a window-average CombinedDPS is the mean shock met per hit (11); the steady value (17) is the upper bound PoB would show for a long fight.

Same iteration on the author's build (D = 25, 4 hits, HitTime 0.646): S = 12.05, 12.51, 12.52; mean 9.27, steady 12.52. The author typed 11, between mean and steady: CombinedDPS 822,633 at 11, 810,535 at the mean (9), 834,730 at steady (13). The author's hand-typed shock agrees with the derived range.

Proposal: type `round(mean shock met per hit inside the ramp window)` as `conditionShockEffect` (11 here), keep the toggle on only when the shock uptime is high: uptime = 1 - (1 - ShockChance/100)^(hits per Duration), which here is 1 - 0.2357^2 = 94.4 % (2 whole hits fit into 2 s; ShockChance 76.43 %). The lead decides the uptime cut-off; this note does not set one.

## Row 4. Why the search did not take High Voltage

High Voltage (node 58168, PoB tree 3_29, `vendor/pob/source/src/TreeData/3_29/tree.lua:69723-69735`): "100% increased Critical Strike Chance against Shocked Enemies". It keys on `Condition:Shocked`, not on a shock value, and costs 1 point: it is adjacent to allocated node 54645 (points_used 98 -> 99). Under today's Baseline lane the toggle `conditionEnemyShocked` is off (the lane gating at `src/junkroan/optimizer/config_rules.py:2044-2055` allows it only with a second lightning skill, on the claim that PoB applies the main skill's own shock; modelling note headline 3 shows PoB does not), so the node's text never fires: CombinedDPS 810,564 with and without it (+0.0 %); the search could not see any value. With the toggle on (value 0): crit chance 73.8 -> 83.3 %, CombinedDPS 842,986 -> 931,908 (+10.55 %). With the ramp's shock typed (11): 914,316 -> 1,010,761 (+10.55 %, +96,445), and against today's 810,564 the combined lane is +24.7 %. For scale, in the typed-11 config removing 54 of the 56 DPS-bearing allocated nodes costs less than High Voltage's +96,445 (smallest nonzero losses 2,795, 9,645, 11,035; median 24,111); in today's config HV beats none. The owner's reading is confirmed: shock was not configured, and the cause is the config rule, not the tree search.

## Row 5. Drafted implementation sub-issues (not posted)

### F2. Derive own-hit shock and Chill, Scorch, Brittle, Sap from PoB's hit numbers (title, 79 chars)
`Derive own-hit Shock, Chill, Scorch, Brittle, Sap from PoB hit numbers and set them`

## For the human
- **What:** when a build's own hits shock (or chill, scorch, brittle, sap) the enemy, the optimizer types that effect into the config, computed from PoB's own hit damage and the boss threshold, including the ramp inside 2.5 s.
- **Why:** PoB never applies an own-hit shock itself; High Voltage and every "against Shocked Enemies" node was invisible (+10.6 % and +12.8 % on hit_penance_brand).
- **Plan:** one function reads the per-hit outputs, iterates the ramp, and writes `conditionEnemyShocked` + `conditionShockEffect` (and the other four) into the lane.
- **Result:** hit_penance_brand Baseline CombinedDPS 810,564 -> 914,316 with no change to the build.
- **Undo:** two-way door; the function is one call site in the lane builder.

## For the agent
- **Kind (D113):** evaluation fix (config of the lane): a bug-specific test plus D84's replay bench on hit_penance_brand and one other hit build; no whole-set run.
- **Rule:** after PoB reads the build (toggle on, value 0 to include `Condition:` mods), for each ailment A in Shock, Chill, Scorch, Brittle, Sap with `<A>ChanceOnHit + <A>ChanceOnCrit > 0` (inflict flag): threshold T from PoB (data tables, CO:5208-5218; never typed); `d0` = chance-weighted blend of the source types' HitAverage / CritAverage (CO:4191-4218); D = the enemy's other DamageTaken increase (measure with one typed value, or read the modDB); n = hits starting before the ramp budget (`rails_default.json` 2.5 s, `ramp.py`); iterate `S_k = min(Maximum<A>, K_A * (d_k/T)^0.4 * <A>EffectMod)` with K = 50 (Shock, Chill, Scorch), 10 (Brittle), 100/3 (Sap) and `d_k = d0*(1+S_{k-1}/(100+D))` (for Shock; Chill with Bonechill likewise, others do not feed damage); type `round(mean S_{k-1} over the n hits)`; set the toggle only when uptime `1-(1-<A>Chance/100)^(hits per <A>Duration)` clears the lead's cut-off. Scorch, Brittle, Sap need their own chance mods (not 100 % on crit): use `<A>Chance`, not "crit".
- **Files:** `src/junkroan/optimizer/config_rules.py` (gating :2044-2055, lane inputs :1566, durations :1815), a new small module next to `ramp.py` for the iteration, `src/junkroan/pob/headless_runtime_worker.py:55-61` (defaults, shock_effect read-back :5602-5655; shock_effect needs is_shocked).
- **Acceptance (hit_penance_brand-s4, Baseline, PoB 2.67.2):**

| check | value | tolerance |
|---|---|---|
| T (level 84, Pinnacle) | 6,349,995 | exact |
| d0 / D | 355,314 / 30 | 0.5 |
| S_1, S_2, S_3 | 15.78, 16.52, 16.55 | 0.01 |
| steady state | 16.55 | 0.01 |
| typed value | 11 | exact |
| CombinedDPS with typed 11 | 914,316 | 1 |
| author fixture (D 25, 4 hits) mean / steady | 9.27 / 12.52 -> typed 9 -> 810,535 | 1 |
| generated(x)>0 and evaluated(x)>0 | `conditionShockEffect` in the trace counter | > 0 |
| replay bench | High Voltage enters on hit_penance_brand: `evaluated(HV) > 0`; gain +10.55 % when taken | numbers pasted |

### F3. Fix the config_rules comment, gating and pending fact that claim PoB applies hit shock (title, 78 chars)
`Fix config_rules comment and gating that claim PoB applies the hit's shock itself`

## For the human
- **What:** three places say PoB applies the shock a build's own hits earn; the PoB source says it does not.
- **Why:** the claim kept the shock toggle off for every lightning build and hid High Voltage (Row 4).
- **Plan:** correct the text and the gating so the toggle's absence is not justified by a wrong fact.
- **Result:** no number moves by itself (F2 sets the values); the wrong sentence is gone.
- **Undo:** two-way door.

## For the agent
- **Kind (D113):** bug (wrong stated fact driving a rule); bug-specific test.
- **Rule:** replace the comment at `src/junkroan/optimizer/config_rules.py:103-108` and the two reasons at `:2044-2055` ("the main skill's own ailment PoB applies by itself") with the vendor facts: `val.effect` only fills the breakdown (`CalcOffence.lua:5230, 5323`), ShockVal is written only by config `conditionShockEffect` (`ConfigOptions.lua:1921`) and guaranteed sources (`CalcPerform.lua:3500-3540`); fix `src/junkroan/mechanics/pending_facts.json` (~:143, "applies the shock its own hits earn (CalcPerform ShockVal)") the same way and keep its formula param (`0.5*(hit/threshold)^0.4`, min 5); the gating must no longer return "applies by itself" for Shocked, Chilled, Scorched, Brittle, Sapped of the main skill.
- **Files:** `src/junkroan/optimizer/config_rules.py`, `src/junkroan/mechanics/pending_facts.json`, `tests/test_config_rules.py`, `tests/test_pending_facts.py`.
- **Acceptance:**

| check | value |
|---|---|
| search the three files for "applies by itself" / "PoB applies" claims about hit shock | 0 hits |
| unit test: lane for hit_penance_brand explains `conditionEnemyShocked` as derivable from own hits (inflict flag), not as "PoB applies" | passes; fails on main |
| `tests/test_config_rules.py`, `tests/test_pending_facts.py` | pass |

### F4. Pin PoB's boss ailment threshold with a canary test (title, 68 chars)
`Pin PoB's Guardian/Pinnacle ailment threshold (6,349,995 at L84) in a test`

## For the human
- **What:** a test that fails if a PoB bump changes the threshold the shock numbers rest on.
- **Why:** F2 reads the threshold from PoB; a silent change would move every shock value.
- **Plan:** read the threshold through the same data tables in a short PoB session and compare.
- **Result:** the number is guarded; no override is added (Row 2: PoB's value is within +5 % of the average boss).
- **Undo:** two-way door.

## For the agent
- **Kind (D113):** refactor-free guard: a test with numbers (`-m pob`, 1 slot, under a minute).
- **Rule:** assert `monsterAilmentThresholdTable[84] * 7.68 * mapLevelBossLifeMult[84] * mapLevelBossAilmentMult[84] * 5.04` equals 6,349,995 (rounded) for `enemyIsBoss=Pinnacle`, level 84; also levels 83 (5,473,455) and 85 (6,741,575). On a failure the message names `CalcOffence.lua:5208-5218` and the poedb comparison of this note.
- **Files:** a new `tests/test_ailment_threshold_pob.py`; `docs/POBSESSION.md` one line.
- **Acceptance:** 3 levels match exactly; runtime < 60 s.

### F5. Replay hit_penance_brand with derived shock: does High Voltage enter? (title, 70 chars)
`Replay hit_penance_brand with derived own-hit shock (High Voltage check)`

## For the human
- **What:** after F2, rerun the search on the one build where the defect shows and see whether High Voltage is taken.
- **Why:** the owner's expectation; the search never saw the node.
- **Plan:** D84 replay bench, not a whole-set run.
- **Result:** the node taken or not, with the DPS number either way.
- **Undo:** reading only.

## For the agent
- **Kind (D113):** loop/evaluation fix proven by D84's replay bench on the builds where the defect reproduces (hit_penance_brand, and the other lightning hit builds if any); a full paired run only on an alert.
- **Rule:** F2 merged; bench as a heavy run if longer than ~5 min.
- **Files:** none (a run and a comment).
- **Acceptance:** `evaluated(node 58168) > 0`; gain of HV under the lane >= +10 % at the typed 11 (this note: +10.55 %); CombinedDPS of the result >= 1,010,761 or a node that beats it, with the numbers pasted.

## Principles (row of the lead's list, 5)

Config toggles and effect values are optimizer decisions derived from PoB's numbers (principles 2 and 4): `conditionEnemyShocked`, `conditionShockEffect`, the Chill / Scorch / Brittle / Sap effect inputs, the ramp's hit count and the uptime test are computed by scripts from PoB's per-hit outputs, the PoB-read threshold and the ramp budget in `rails_default.json`. The threshold itself is never typed (principle 1; PoB's number is within +5 % of the poedb average). The LLM never picks a node (High Voltage), a toggle, an effect value, the threshold or the hit count; it proposes skeletons (Penance Brand + Physical to Lightning) and explains the result. The only hand-maintained facts stay small and machine-readable: the formulas' constants (`50`, `0.4`, caps) live in PoB, not in our files.

## Not verified here
- That the in-game shock uses only Lightning damage of the hit (PoB's rule, CO:4191-4206) is PoB's model; the boss note's wiki page was not compared on that.
- Ailment uptime assumes hits arrive at a steady `HitTime`; Penance Brand activation timing was taken from PoB's `HitSpeed`.
- The ramp ignores that non-crit hits (26 %) shock only 10 % of the time; the blend and the crit-only variant differ by 0.03-0.2 percentage points.
