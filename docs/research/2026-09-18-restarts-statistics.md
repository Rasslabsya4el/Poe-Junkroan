# Restarts: how much a second seed buys (ROADMAP 7.3)

Date: 2026-09-18. Statistics only, no code and no benchmark was run for this note.
Score = `pct_of_author` = our `CombinedDPS` / the author's `CombinedDPS` under our lane x 100
(`ratio_lane * 100` in `results.json`).

Sources (all from one code generation, before the rules merge of 2026-09-18 04:47):

| run | folder | references x seeds | builds used |
|---|---|---|---|
| smoke-frozen | `artifacts/benchmark/20260916-0941-smoke-frozen` | 6 x seeds 1-3 | 18 |
| restarts-smoke2 | `artifacts/benchmark/20260917-2237-restarts-smoke2` | cold_dot, bleed_bow x seeds 4-6 | 6 |
| restarts-smoke4 | `artifacts/benchmark/20260918-0128-restarts-smoke4` | 6 x seeds 7-9 | 18 |
| restarts-smoke3 | `artifacts/benchmark/20260918-0035-restarts-smoke3` | 5 logs, killed run | 0 (none finished) |

Total: **42 finished builds**, 6 references, seeds 1-9 (cold_dot and bleed_bow n=9; the other four n=6).

## 0. Check: log-derived pct is the same number results.json holds

For every build present in both a `results.json` and its log, `value` of the
`  config (final lanes)` line divided by the log's `under our lane N` was compared with
`ratio_lane * 100` from the JSON.

| run | reference | seed | under our lane (log) | author_lane (json) | final value (log) | ours (json) | pct (log) | pct (json) |
|---|---|---|---|---|---|---|---|---|
| smoke-frozen | bleed_bow | 1 | 623444 | 623444 | 949348 | 949348 | 152.3 | 152.3 |
| smoke-frozen | bleed_bow | 2 | 623444 | 623444 | 796025 | 796025 | 127.7 | 127.7 |
| smoke-frozen | bleed_bow | 3 | 623444 | 623444 | 531662 | 531662 | 85.3 | 85.3 |

n = 42 builds checked, max |pct(log) - pct(json)| = **0.000 pp** (identical to floating-point printing precision). The log-derived ratio is therefore usable wherever a `results.json` row is missing.

Of the 5 logs in `20260918-0035-restarts-smoke3` (impale_ballista s4, s5; summon_raging_spirits
s4, s5, s6) **none** contains a `  config (final lanes)` line - all five were killed during the
improvement loop. They contribute 0 builds to every table below.

## 1. Per-seed pct_of_author

### bleed_bow (n=9)

| seed | pct | run |
|---|---|---|
| 1 | 152.3 | smoke-frozen |
| 2 | 127.7 | smoke-frozen |
| 3 | 85.3 | smoke-frozen |
| 4 | 140.9 | restarts-smoke2 |
| 5 | 51.2 | restarts-smoke2 |
| 6 | 150.8 | restarts-smoke2 |
| 7 | 107.8 | restarts-smoke4 |
| 8 | 150.7 | restarts-smoke4 |
| 9 | 117.0 | restarts-smoke4 |

### burning_arrow_snipe (n=6)

| seed | pct | run |
|---|---|---|
| 1 | 214.4 | smoke-frozen |
| 2 | 215.6 | smoke-frozen |
| 3 | 205.5 | smoke-frozen |
| 7 | 207.3 | restarts-smoke4 |
| 8 | 213.5 | restarts-smoke4 |
| 9 | 223.0 | restarts-smoke4 |

### cold_dot (n=9)

| seed | pct | run |
|---|---|---|
| 1 | 148.6 | smoke-frozen |
| 2 | 176.9 | smoke-frozen |
| 3 | 142.4 | smoke-frozen |
| 4 | 163.1 | restarts-smoke2 |
| 5 | 112.5 | restarts-smoke2 |
| 6 | 154.0 | restarts-smoke2 |
| 7 | 122.2 | restarts-smoke4 |
| 8 | 127.0 | restarts-smoke4 |
| 9 | 136.6 | restarts-smoke4 |

### impale_ballista (n=6)

| seed | pct | run |
|---|---|---|
| 1 | 83.4 | smoke-frozen |
| 2 | 44.1 | smoke-frozen |
| 3 | 92.9 | smoke-frozen |
| 7 | 62.7 | restarts-smoke4 |
| 8 | 80.4 | restarts-smoke4 |
| 9 | 80.5 | restarts-smoke4 |

### stormbrand (n=6)

| seed | pct | run |
|---|---|---|
| 1 | 143.8 | smoke-frozen |
| 2 | 168.3 | smoke-frozen |
| 3 | 186.7 | smoke-frozen |
| 7 | 127.0 | restarts-smoke4 |
| 8 | 192.2 | restarts-smoke4 |
| 9 | 168.8 | restarts-smoke4 |

### summon_raging_spirits (n=6)

| seed | pct | run |
|---|---|---|
| 1 | 219.6 | smoke-frozen |
| 2 | 253.0 | smoke-frozen |
| 3 | 195.8 | smoke-frozen |
| 7 | 223.6 | restarts-smoke4 |
| 8 | 221.8 | restarts-smoke4 |
| 9 | 225.7 | restarts-smoke4 |

### Summary

| reference | n | median | mean | min | max | spread (max-min) | stdev |
|---|---|---|---|---|---|---|---|
| bleed_bow | 9 | 127.7 | 120.4 | 51.2 | 152.3 | 101.1 | 34.5 |
| burning_arrow_snipe | 6 | 213.9 | 213.2 | 205.5 | 223.0 | 17.5 | 6.3 |
| cold_dot | 9 | 142.4 | 142.6 | 112.5 | 176.9 | 64.5 | 20.5 |
| impale_ballista | 6 | 80.4 | 74.0 | 44.1 | 92.9 | 48.7 | 17.6 |
| stormbrand | 6 | 168.5 | 164.4 | 127.0 | 192.2 | 65.2 | 25.0 |
| summon_raging_spirits | 6 | 222.7 | 223.2 | 195.8 | 253.0 | 57.2 | 18.2 |

Across the 6 references (n=6 references): spread median 60.8 pp, min 17.5, max 101.1; stdev median 19.4 pp, min 6.3, max 34.5.
Relative stdev (stdev / median) per reference: bleed_bow 27.0%, burning_arrow_snipe 2.9%, cold_dot 14.4%, impale_ballista 21.9%, stormbrand 14.8%, summon_raging_spirits 8.2%.

## 2. Best-of-K (bootstrap)

Method: for each reference, resample K values with replacement from that reference's observed
seeds, take the max, average over 20,000 draws. `random.Random(0)`, re-seeded to 0 for every
(reference, K) cell, so the table is reproducible. K=1 is by construction the mean of the
observed seeds up to Monte-Carlo noise.

| reference | n obs | K=1 | K=2 | K=3 | K=4 | K=5 | K=6 |
|---|---|---|---|---|---|---|---|
| bleed_bow | 9 | 120.5 | 137.9 | 144.6 | 147.5 | 149.2 | 150.2 |
| burning_arrow_snipe | 6 | 213.2 | 216.4 | 218.0 | 219.0 | 219.8 | 220.4 |
| cold_dot | 9 | 142.8 | 153.7 | 159.4 | 163.0 | 165.7 | 167.4 |
| impale_ballista | 6 | 74.0 | 82.5 | 85.8 | 87.4 | 88.6 | 89.4 |
| stormbrand | 6 | 164.5 | 177.3 | 182.7 | 185.7 | 187.5 | 188.7 |
| summon_raging_spirits | 6 | 223.3 | 231.8 | 236.3 | 239.4 | 241.9 | 243.8 |
| **median over the 6 references** | - | **153.6** | **165.5** | **171.0** | **174.4** | **176.6** | **178.0** |

Machine-wide expected best-of-K (median across the 6 references), K=1..6:

**153.6 / 165.5 / 171.0 / 174.4 / 176.6 / 178.0**

| K | machine-wide | gain vs K=1 | gain vs K-1 |
|---|---|---|---|
| 1 | 153.6 | +0.0 | - |
| 2 | 165.5 | +11.8 | +11.8 |
| 3 | 171.0 | +17.4 | +5.6 |
| 4 | 174.4 | +20.7 | +3.3 |
| 5 | 176.6 | +22.9 | +2.2 |
| 6 | 178.0 | +24.4 | +1.5 |

Per-reference gain from K=1 to K=3: bleed_bow +24.1, burning_arrow_snipe +4.8, cold_dot +16.6, impale_ballista +11.8, stormbrand +18.2, summon_raging_spirits +13.0.
Per-reference gain from K=3 to K=6: bleed_bow +5.6, burning_arrow_snipe +2.4, cold_dot +8.0, impale_ballista +3.6, stormbrand +6.0, summon_raging_spirits +7.5.

## 3. Where the spread is born

Construction = `  tree rebuilt on gear` (last construction stage, before the improvement loop).
Final = `  config (final lanes)`. Both divided by the log's `under our lane N`. Finished logs
only, n=42 builds.

| reference | seed | construction pct | final pct | final / construction |
|---|---|---|---|---|
| bleed_bow | 1 | 69.3 | 152.3 | 2.20 |
| bleed_bow | 2 | 82.3 | 127.7 | 1.55 |
| bleed_bow | 3 | 69.4 | 85.3 | 1.23 |
| bleed_bow | 4 | 83.3 | 140.9 | 1.69 |
| bleed_bow | 5 | 39.3 | 51.2 | 1.30 |
| bleed_bow | 6 | 91.2 | 150.8 | 1.65 |
| bleed_bow | 7 | 79.3 | 107.8 | 1.36 |
| bleed_bow | 8 | 90.8 | 150.7 | 1.66 |
| bleed_bow | 9 | 74.8 | 117.0 | 1.56 |
| burning_arrow_snipe | 1 | 94.9 | 214.4 | 2.26 |
| burning_arrow_snipe | 2 | 86.5 | 215.6 | 2.49 |
| burning_arrow_snipe | 3 | 81.9 | 205.5 | 2.51 |
| burning_arrow_snipe | 7 | 71.8 | 207.3 | 2.89 |
| burning_arrow_snipe | 8 | 111.0 | 213.5 | 1.92 |
| burning_arrow_snipe | 9 | 93.9 | 223.0 | 2.38 |
| cold_dot | 1 | 98.0 | 148.6 | 1.52 |
| cold_dot | 2 | 104.3 | 176.9 | 1.70 |
| cold_dot | 3 | 103.5 | 142.4 | 1.38 |
| cold_dot | 4 | 69.8 | 163.1 | 2.34 |
| cold_dot | 5 | 67.7 | 112.5 | 1.66 |
| cold_dot | 6 | 98.9 | 154.0 | 1.56 |
| cold_dot | 7 | 97.0 | 122.2 | 1.26 |
| cold_dot | 8 | 76.2 | 127.0 | 1.67 |
| cold_dot | 9 | 60.3 | 136.6 | 2.27 |
| impale_ballista | 1 | 47.4 | 83.4 | 1.76 |
| impale_ballista | 2 | 32.3 | 44.1 | 1.37 |
| impale_ballista | 3 | 69.7 | 92.9 | 1.33 |
| impale_ballista | 7 | 36.5 | 62.7 | 1.72 |
| impale_ballista | 8 | 49.9 | 80.4 | 1.61 |
| impale_ballista | 9 | 53.4 | 80.5 | 1.51 |
| stormbrand | 1 | 112.2 | 143.8 | 1.28 |
| stormbrand | 2 | 126.3 | 168.3 | 1.33 |
| stormbrand | 3 | 83.2 | 186.7 | 2.24 |
| stormbrand | 7 | 105.7 | 127.0 | 1.20 |
| stormbrand | 8 | 133.9 | 192.2 | 1.44 |
| stormbrand | 9 | 84.5 | 168.8 | 2.00 |
| summon_raging_spirits | 1 | 156.8 | 219.6 | 1.40 |
| summon_raging_spirits | 2 | 155.3 | 253.0 | 1.63 |
| summon_raging_spirits | 3 | 166.6 | 195.8 | 1.18 |
| summon_raging_spirits | 7 | 144.4 | 223.6 | 1.55 |
| summon_raging_spirits | 8 | 161.9 | 221.8 | 1.37 |
| summon_raging_spirits | 9 | 146.6 | 225.7 | 1.54 |

| reference | n | constr median | constr min | constr max | **constr spread** | final median | final min | final max | **final spread** | Spearman(constr, final) |
|---|---|---|---|---|---|---|---|---|---|---|
| bleed_bow | 9 | 79.3 | 39.3 | 91.2 | 52.0 | 127.7 | 51.2 | 152.3 | 101.1 | 0.52 |
| burning_arrow_snipe | 6 | 90.2 | 71.8 | 111.0 | 39.3 | 213.9 | 205.5 | 223.0 | 17.5 | 0.43 |
| cold_dot | 9 | 97.0 | 60.3 | 104.3 | 44.1 | 142.4 | 112.5 | 176.9 | 64.5 | 0.55 |
| impale_ballista | 6 | 48.6 | 32.3 | 69.7 | 37.5 | 80.4 | 44.1 | 92.9 | 48.7 | 0.83 |
| stormbrand | 6 | 108.9 | 83.2 | 133.9 | 50.7 | 168.5 | 127.0 | 192.2 | 65.2 | 0.09 |
| summon_raging_spirits | 6 | 156.1 | 144.4 | 166.6 | 22.2 | 222.7 | 195.8 | 253.0 | 57.2 | -0.71 |

n per Spearman cell = the reference's n in the same row (9, 6, 9, 6, 6, 6).

| pooled | n | Spearman(constr, final) |
|---|---|---|
| all finished builds, raw values | 42 | 0.75 |
| all finished builds, each value / its reference's median | 42 | 0.42 |

Construction-to-final multiplier over all 42 builds: median 1.59, min 1.18, max 2.89.

Spread at construction vs spread at the end, per reference (n=6 references): construction median 41.7 pp, final median 60.8 pp. References where the loop widened the spread: bleed_bow, cold_dot, impale_ballista, stormbrand, summon_raging_spirits. References where the loop narrowed it: burning_arrow_snipe.

## 4. Time per build

Seconds = the `seconds` field of each `results.json` row (wall clock for the whole build).
Time-budget marker = a log line matching `^stopped: time budget` (the same event also appears
as the `; stopped: time budget` suffix on the last `loop pass N` line). No other `stopped:`
reason occurs in any of the 42 logs; the remaining builds ended because an improvement pass
kept nothing.

| reference | n | median s | min s | max s | ended on time budget | share |
|---|---|---|---|---|---|---|
| bleed_bow | 9 | 3204 | 1621 | 6599 | 1 / 9 | 11% |
| burning_arrow_snipe | 6 | 3334 | 2725 | 3956 | 0 / 6 | 0% |
| cold_dot | 9 | 3951 | 2049 | 6159 | 3 / 9 | 33% |
| impale_ballista | 6 | 3495 | 2000 | 4762 | 0 / 6 | 0% |
| stormbrand | 6 | 2962 | 1127 | 6267 | 1 / 6 | 17% |
| summon_raging_spirits | 6 | 4154 | 3040 | 5450 | 0 / 6 | 0% |
| **all** | 42 | 3511 | 1127 | 6599 | 5 / 42 | 12% |

All 42 builds: median 3511 s, mean 3696 s, min 1127 s, max 6599 s, stdev 1281 s. The configured budget seen in the stop lines is 5400 s.
Cost of K seeds of one reference at the machine-wide median (3511 s): K=1 1.0 h, K=2 2.0 h, K=3 2.9 h, K=4 3.9 h, K=5 4.9 h, K=6 5.9 h.

## 5. Method

Every pct in this note is `ratio_lane * 100` from `results.json` (field `ratio_lane` = `ours` / `author_lane`, where `ours` is the build's final `CombinedDPS` and `author_lane` is the author's `CombinedDPS` re-measured under our config lane). 42 rows were read: 18 from `20260916-0941-smoke-frozen/results.json` (6 references x seeds 1-3), 6 from `20260917-2237-restarts-smoke2/results.json` (cold_dot, bleed_bow x seeds 4-6) and 18 from `20260918-0128-restarts-smoke4/results.json` (6 references x seeds 7-9); every row has `ok = true` and `variant = ""`, so nothing was dropped for failure. Stage values for section 3 were parsed out of the matching `logs/<slug>-s<seed>.log`: the author's number from the `under our lane N` capture in the header, and the `value` column of the lines `  tree rebuilt on gear` and `  config (final lanes)`; the log-derived ratio was verified against `ratio_lane` on all 42 builds and agrees to 0.000 pp. The five logs in `20260918-0035-restarts-smoke3/logs/` (impale_ballista s4-s5, summon_raging_spirits s4-s6) were **skipped entirely**: that run was killed before any of them reached `  config (final lanes)`, so they have no final score; the run also never produced a `results.json`. Seeds are therefore unbalanced - cold_dot and bleed_bow have 9 seeds each, burning_arrow_snipe, impale_ballista, stormbrand and summon_raging_spirits 6 each - and the machine-wide best-of-K line is a median over the 6 per-reference bootstrap expectations, not a pooled resample, so the unbalanced n affects only the precision of each reference's own curve. The bootstrap uses `random.Random(0)`, re-seeded to 0 for each (reference, K) cell, 20,000 draws, sampling with replacement from that reference's observed seeds only. Spearman is computed with average ranks on ties (there are no ties in this data). Times come from the `seconds` field of the same `results.json` rows; the time-budget share comes from the logs.

