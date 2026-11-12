# Seed divergence in the two 3-seed campaigns (ROADMAP 7.3, first item)

Statistics only. 32 references x 3 seeds = 96 runs, all `ok: true`, all `variant: ""`.
`pct` = `ratio_lane` * 100 = our final CombinedDPS as a percentage of the author's build
under our lane. Per-stage percentages are `stage.value / author_lane * 100` taken from
`results.json`'s `stages` list (it carries a per-stage `value`; the logs were used only for
section 4).

## 1. Per reference: pct per seed, median, spread

Sorted by spread, descending. `*` marks spread > 10 points.

| | reference | campaign | s1 | s2 | s3 | median | spread |
|---|---|---|---|---|---|---|---|
| * | shockwave_cyclone | new18 | 249.7 | 177.6 | 140.7 | 177.6 | 109.1 |
| * | static_strike | new18 | 145.0 | 199.5 | 247.1 | 199.5 | 102.2 |
| * | regular_viper_strike | core14 | 121.7 | 193.8 | 111.5 | 121.7 | 82.3 |
| * | absolution_minions | core14 | 228.6 | 220.2 | 155.2 | 220.2 | 73.4 |
| * | bleed_bow | core14 | 161.3 | 93.9 | 89.4 | 93.9 | 71.9 |
| * | lightning_trap | new18 | 145.1 | 191.8 | 124.4 | 145.1 | 67.4 |
| * | hit_penance_brand | core14 | 189.0 | 163.8 | 229.1 | 189.0 | 65.3 |
| * | spark | core14 | 210.8 | 222.8 | 158.5 | 210.8 | 64.4 |
| * | elemental_hit | new18 | 88.7 | 113.1 | 147.8 | 113.1 | 59.1 |
| * | impale_ballista | new18 | 74.2 | 45.3 | 102.3 | 74.2 | 57.1 |
| * | smite | core14 | 160.1 | 107.8 | 149.0 | 149.0 | 52.3 |
| * | pyroclast_mine | new18 | 123.4 | 166.4 | 174.3 | 166.4 | 50.9 |
| * | summon_raging_spirits | core14 | 204.2 | 247.5 | 197.2 | 204.2 | 50.2 |
| * | kinetic_bolt_wander | new18 | 162.3 | 128.8 | 115.6 | 128.8 | 46.6 |
| * | cold_dot | core14 | 140.9 | 97.9 | 142.4 | 140.9 | 44.5 |
| * | burning_arrow_snipe | new18 | 212.3 | 170.6 | 188.9 | 188.9 | 41.7 |
| * | poison_spark | new18 | 120.0 | 78.4 | 82.3 | 82.3 | 41.6 |
| * | poison_spectral_throw | core14 | 176.3 | 217.7 | 201.8 | 201.8 | 41.4 |
| * | stormbrand | core14 | 171.7 | 180.5 | 144.1 | 171.7 | 36.4 |
| * | soulrend_chaos_dot | new18 | 201.7 | 190.8 | 168.2 | 190.8 | 33.5 |
| * | winter_orb | core14 | 269.0 | 301.0 | 282.4 | 282.4 | 32.0 |
| * | physical_dot | core14 | 237.9 | 265.5 | 240.2 | 240.2 | 27.6 |
| * | kinetic_fusillade | new18 | 198.3 | 212.8 | 185.5 | 198.3 | 27.3 |
| * | exsanguinate_mines | new18 | 144.2 | 162.9 | 170.2 | 162.9 | 26.1 |
| * | spectral_shield_throw | new18 | 184.2 | 168.9 | 170.7 | 170.7 | 15.3 |
| * | arc_archmage | new18 | 102.8 | 90.6 | 105.6 | 102.8 | 15.0 |
| * | archmage_volatile_dead | new18 | 132.9 | 122.3 | 136.2 | 132.9 | 13.9 |
| * | toxic_rain | core14 | 141.7 | 128.8 | 138.5 | 138.5 | 12.9 |
| * | impale_cyclone | new18 | 124.1 | 119.3 | 131.3 | 124.1 | 12.0 |
|  | bleed_perforate | new18 | 32.6 | 36.7 | 42.1 | 36.7 | 9.4 |
|  | ignite_penance_brand | core14 | 307.8 | 301.1 | 299.6 | 301.1 | 8.2 |
|  | vd_spellslinger | new18 | 271.2 | 276.3 | 279.1 | 276.3 | 7.9 |

References with spread > 10: **29 of 32**. Spread over all 32: min 7.9, median 41.6, max 109.1.

## 2. Stage by stage, for every reference with spread > 10

Each cell is that seed's value at that stage as a percentage of the author's number.
`-` = the seed had no such loop pass (it had already stopped). The spread column is
max - min over the seeds that still have a value; `(n=2)` marks a pass where only two
seeds were still running, and a pass left with one seed has no spread (`-  (n=1)`) and
is ignored by the two verdict lines under the table.

### shockwave_cyclone  (spread 109.1; best s1 249.7, worst s3 140.7)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 2.7 | 2.7 | 2.7 | 0.0 |
| config | 2.7 | 2.7 | 2.7 | 0.0 |
| gear 1 | 1.2 | 0.6 | 1.3 | 0.8 |
| tree greedy | 70.5 | 29.9 | 49.1 | 40.5 |
| gear 2 | 79.9 | 57.6 | 58.7 | 22.3 |
| tree rebuilt | 79.9 | 85.4 | 72.8 | 12.6 |
| loop pass 1 | 116.3 | 149.0 | 119.4 | 32.7 |
| loop pass 2 | 117.9 | 149.0 | 119.4 | 31.1 |
| loop pass 3 | 159.2 | - | - | -  (n=1) |
| loop pass 4 | 208.1 | - | - | -  (n=1) |
| loop pass 5 | 212.8 | - | - | -  (n=1) |
| loop pass 6 | 212.8 | - | - | -  (n=1) |
| final | 249.7 | 177.6 | 140.7 | 109.1 |

First stage where the spread exceeds 10 points: **tree greedy** (40.5). Largest spread: **final** (109.1).

### static_strike  (spread 102.2; best s3 247.1, worst s1 145.0)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 4.5 | 4.5 | 4.5 | 0.0 |
| config | 7.5 | 7.5 | 7.5 | 0.0 |
| gear 1 | 4.7 | 4.4 | 4.8 | 0.4 |
| tree greedy | 42.4 | 47.4 | 53.8 | 11.4 |
| gear 2 | 43.0 | 48.3 | 77.6 | 34.6 |
| tree rebuilt | 48.4 | 54.2 | 82.7 | 34.3 |
| loop pass 1 | 141.7 | 116.4 | 151.8 | 35.4 |
| loop pass 2 | 141.7 | 144.1 | 199.8 | 58.1 |
| loop pass 3 | - | 155.5 | 207.8 | 52.3 (n=2) |
| loop pass 4 | - | 184.1 | 243.6 | 59.5 (n=2) |
| loop pass 5 | - | 195.7 | 243.6 | 47.9 (n=2) |
| loop pass 6 | - | 195.7 | - | -  (n=1) |
| final | 145.0 | 199.5 | 247.1 | 102.2 |

First stage where the spread exceeds 10 points: **tree greedy** (11.4). Largest spread: **final** (102.2).

### regular_viper_strike  (spread 82.3; best s2 193.8, worst s3 111.5)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 2.8 | 2.8 | 2.8 | 0.0 |
| config | 5.0 | 5.0 | 5.0 | 0.0 |
| gear 1 | 2.4 | 3.0 | 2.7 | 0.7 |
| tree greedy | 29.8 | 32.8 | 30.5 | 2.9 |
| gear 2 | 56.0 | 36.5 | 58.0 | 21.5 |
| tree rebuilt | 56.0 | 25.7 | 47.3 | 30.3 |
| loop pass 1 | 66.3 | 29.4 | 52.8 | 36.9 |
| loop pass 2 | 117.4 | 34.2 | 54.4 | 83.2 |
| loop pass 3 | 121.7 | 48.1 | 61.9 | 73.7 |
| loop pass 4 | 121.7 | 72.6 | 68.0 | 53.7 |
| loop pass 5 | - | 100.3 | 72.0 | 28.3 (n=2) |
| loop pass 6 | - | 102.5 | 107.4 | 4.8 (n=2) |
| loop pass 7 | - | 171.9 | 110.1 | 61.8 (n=2) |
| loop pass 8 | - | 183.3 | 110.1 | 73.3 (n=2) |
| loop pass 9 | - | 187.5 | - | -  (n=1) |
| loop pass 10 | - | 187.5 | - | -  (n=1) |
| final | 121.7 | 193.8 | 111.5 | 82.3 |

First stage where the spread exceeds 10 points: **gear 2** (21.5). Largest spread: **loop pass 2** (83.2).

### absolution_minions  (spread 73.4; best s1 228.6, worst s3 155.2)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 30.1 | 30.1 | 30.1 | 0.0 |
| config | 33.2 | 33.2 | 33.2 | 0.0 |
| gear 1 | 31.7 | 30.8 | 31.4 | 0.9 |
| tree greedy | 108.2 | 108.5 | 75.1 | 33.5 |
| gear 2 | 108.1 | 111.2 | 102.3 | 9.0 |
| tree rebuilt | 162.2 | 174.3 | 124.9 | 49.4 |
| loop pass 1 | 189.2 | 201.3 | 133.4 | 67.9 |
| loop pass 2 | 194.9 | 206.2 | 137.3 | 68.9 |
| loop pass 3 | 208.8 | 211.2 | 151.2 | 60.0 |
| loop pass 4 | 221.6 | 218.5 | 155.2 | 66.4 |
| loop pass 5 | 228.6 | 220.2 | 155.2 | 73.4 |
| loop pass 6 | - | 220.2 | - | -  (n=1) |
| final | 228.6 | 220.2 | 155.2 | 73.4 |

First stage where the spread exceeds 10 points: **tree greedy** (33.5). Largest spread: **loop pass 5** (73.4).

### bleed_bow  (spread 71.9; best s1 161.3, worst s3 89.4)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 0.5 | 0.5 | 0.5 | 0.0 |
| config | 7.2 | 7.2 | 7.2 | 0.0 |
| gear 1 | 6.9 | 6.3 | 7.7 | 1.5 |
| tree greedy | 65.3 | 40.2 | 68.4 | 28.2 |
| gear 2 | 99.4 | 41.1 | 70.6 | 58.3 |
| tree rebuilt | 99.4 | 57.2 | 70.6 | 42.2 |
| loop pass 1 | 104.9 | 67.3 | 76.6 | 37.6 |
| loop pass 2 | 110.3 | 74.5 | 76.6 | 35.8 |
| loop pass 3 | 131.4 | 75.5 | - | 56.0 (n=2) |
| loop pass 4 | 134.6 | 81.0 | - | 53.6 (n=2) |
| loop pass 5 | 136.4 | 81.0 | - | 55.4 (n=2) |
| loop pass 6 | 139.1 | - | - | -  (n=1) |
| loop pass 7 | 139.1 | - | - | -  (n=1) |
| final | 161.3 | 93.9 | 89.4 | 71.9 |

First stage where the spread exceeds 10 points: **tree greedy** (28.2). Largest spread: **final** (71.9).

### lightning_trap  (spread 67.4; best s2 191.8, worst s3 124.4)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 10.2 | 10.2 | 10.2 | 0.0 |
| config | 10.2 | 10.2 | 10.2 | 0.0 |
| gear 1 | 5.7 | 5.5 | 7.6 | 2.2 |
| tree greedy | 92.1 | 89.4 | 93.3 | 3.9 |
| gear 2 | 92.1 | 104.1 | 87.8 | 16.3 |
| tree rebuilt | 87.3 | 89.6 | 84.1 | 5.4 |
| loop pass 1 | 72.1 | 113.3 | 105.6 | 41.2 |
| loop pass 2 | 100.1 | 127.9 | 107.2 | 27.8 |
| loop pass 3 | 119.9 | 145.5 | 111.3 | 34.2 |
| loop pass 4 | 129.8 | 166.0 | 111.3 | 54.7 |
| loop pass 5 | 129.8 | 170.4 | - | 40.6 (n=2) |
| loop pass 6 | - | 171.5 | - | -  (n=1) |
| loop pass 7 | - | 171.5 | - | -  (n=1) |
| final | 145.1 | 191.8 | 124.4 | 67.4 |

First stage where the spread exceeds 10 points: **gear 2** (16.3). Largest spread: **final** (67.4).

### hit_penance_brand  (spread 65.3; best s3 229.1, worst s2 163.8)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 9.4 | 9.4 | 9.4 | 0.0 |
| config | 10.8 | 10.8 | 10.8 | 0.0 |
| gear 1 | 7.2 | 9.1 | 9.9 | 2.8 |
| tree greedy | 98.2 | 118.3 | 117.8 | 20.1 |
| gear 2 | 111.6 | 127.1 | 110.3 | 16.8 |
| tree rebuilt | 108.4 | 123.5 | 104.4 | 19.2 |
| loop pass 1 | 138.7 | 115.0 | 119.3 | 23.7 |
| loop pass 2 | 158.4 | 161.7 | 124.1 | 37.5 |
| loop pass 3 | 170.1 | 163.8 | 127.7 | 42.5 |
| loop pass 4 | 189.0 | 163.8 | 146.8 | 42.3 |
| loop pass 5 | 189.0 | - | 184.8 | 4.3 (n=2) |
| loop pass 6 | - | - | 198.3 | -  (n=1) |
| loop pass 7 | - | - | 210.0 | -  (n=1) |
| loop pass 8 | - | - | 221.5 | -  (n=1) |
| loop pass 9 | - | - | 229.1 | -  (n=1) |
| loop pass 10 | - | - | 229.1 | -  (n=1) |
| final | 189.0 | 163.8 | 229.1 | 65.3 |

First stage where the spread exceeds 10 points: **tree greedy** (20.1). Largest spread: **final** (65.3).

### spark  (spread 64.4; best s2 222.8, worst s3 158.5)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 8.5 | 8.5 | 8.5 | 0.0 |
| config | 19.4 | 19.4 | 19.4 | 0.0 |
| gear 1 | 11.2 | 11.9 | 15.2 | 3.9 |
| tree greedy | 80.6 | 79.7 | 87.6 | 7.9 |
| gear 2 | 75.5 | 88.5 | 79.2 | 13.0 |
| tree rebuilt | 76.9 | 92.1 | 86.7 | 15.3 |
| loop pass 1 | 101.7 | 122.1 | 103.3 | 20.4 |
| loop pass 2 | 182.6 | 198.5 | 134.5 | 64.0 |
| loop pass 3 | 185.2 | 198.5 | 134.5 | 64.0 |
| loop pass 4 | 191.3 | - | - | -  (n=1) |
| loop pass 5 | 191.3 | - | - | -  (n=1) |
| final | 210.8 | 222.8 | 158.5 | 64.4 |

First stage where the spread exceeds 10 points: **gear 2** (13.0). Largest spread: **final** (64.4).

### elemental_hit  (spread 59.1; best s3 147.8, worst s1 88.7)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 2.9 | 2.9 | 2.9 | 0.0 |
| config | 3.2 | 3.2 | 3.2 | 0.0 |
| gear 1 | 1.9 | 2.0 | 1.9 | 0.1 |
| tree greedy | 41.3 | 42.3 | 39.6 | 2.7 |
| gear 2 | 41.5 | 30.9 | 41.5 | 10.6 |
| tree rebuilt | 44.7 | 47.0 | 45.3 | 2.3 |
| loop pass 1 | 71.6 | 80.6 | 75.3 | 9.0 |
| loop pass 2 | 88.7 | 85.5 | 97.1 | 11.6 |
| loop pass 3 | 88.7 | 98.1 | 99.8 | 11.1 |
| loop pass 4 | - | 109.1 | 112.5 | 3.4 (n=2) |
| loop pass 5 | - | 113.1 | 117.2 | 4.1 (n=2) |
| loop pass 6 | - | 113.1 | 117.8 | 4.7 (n=2) |
| loop pass 7 | - | - | 126.1 | -  (n=1) |
| loop pass 8 | - | - | 129.7 | -  (n=1) |
| loop pass 9 | - | - | 131.8 | -  (n=1) |
| loop pass 10 | - | - | 139.4 | -  (n=1) |
| loop pass 11 | - | - | 147.8 | -  (n=1) |
| final | 88.7 | 113.1 | 147.8 | 59.1 |

First stage where the spread exceeds 10 points: **gear 2** (10.6). Largest spread: **final** (59.1).

### impale_ballista  (spread 57.1; best s3 102.3, worst s2 45.3)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 0.6 | 0.6 | 0.6 | 0.0 |
| config | 1.2 | 1.2 | 1.2 | 0.0 |
| gear 1 | 1.4 | 1.1 | 1.1 | 0.3 |
| tree greedy | 51.4 | 25.8 | 37.9 | 25.7 |
| gear 2 | 65.6 | 30.3 | 51.4 | 35.3 |
| tree rebuilt | 51.5 | 36.7 | 70.3 | 33.6 |
| loop pass 1 | 57.3 | 42.2 | 82.3 | 40.1 |
| loop pass 2 | 60.8 | 42.2 | 84.8 | 42.7 |
| loop pass 3 | 66.3 | - | 85.9 | 19.6 (n=2) |
| loop pass 4 | 66.3 | - | 86.8 | 20.5 (n=2) |
| loop pass 5 | - | - | 88.5 | -  (n=1) |
| loop pass 6 | - | - | 89.0 | -  (n=1) |
| loop pass 7 | - | - | 89.0 | -  (n=1) |
| final | 74.2 | 45.3 | 102.3 | 57.1 |

First stage where the spread exceeds 10 points: **tree greedy** (25.7). Largest spread: **final** (57.1).

### smite  (spread 52.3; best s1 160.1, worst s2 107.8)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 3.0 | 3.0 | 3.0 | 0.0 |
| config | 5.1 | 5.1 | 5.1 | 0.0 |
| gear 1 | 4.9 | 4.9 | 3.4 | 1.5 |
| tree greedy | 77.9 | 84.4 | 55.4 | 29.0 |
| gear 2 | 87.7 | 83.0 | 69.6 | 18.1 |
| tree rebuilt | 98.0 | 82.6 | 88.7 | 15.4 |
| loop pass 1 | 121.2 | 107.8 | 140.0 | 32.2 |
| loop pass 2 | 131.5 | 107.8 | 149.0 | 41.2 |
| loop pass 3 | 153.2 | - | 149.0 | 4.2 (n=2) |
| loop pass 4 | 156.1 | - | - | -  (n=1) |
| loop pass 5 | 160.1 | - | - | -  (n=1) |
| loop pass 6 | 160.1 | - | - | -  (n=1) |
| final | 160.1 | 107.8 | 149.0 | 52.3 |

First stage where the spread exceeds 10 points: **tree greedy** (29.0). Largest spread: **final** (52.3).

### pyroclast_mine  (spread 50.9; best s3 174.3, worst s1 123.4)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 4.1 | 4.1 | 4.1 | 0.0 |
| config | 7.3 | 7.3 | 7.3 | 0.0 |
| gear 1 | 6.4 | 6.4 | 6.1 | 0.2 |
| tree greedy | 54.1 | 83.2 | 48.7 | 34.5 |
| gear 2 | 63.6 | 108.3 | 74.0 | 44.6 |
| tree rebuilt | 95.4 | 108.3 | 125.7 | 30.4 |
| loop pass 1 | 123.4 | 157.5 | 167.4 | 44.1 |
| loop pass 2 | 123.4 | 166.3 | 174.3 | 50.9 |
| loop pass 3 | - | 166.3 | 174.3 | 7.9 (n=2) |
| final | 123.4 | 166.4 | 174.3 | 50.9 |

First stage where the spread exceeds 10 points: **tree greedy** (34.5). Largest spread: **loop pass 2** (50.9).

### summon_raging_spirits  (spread 50.2; best s2 247.5, worst s3 197.2)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 14.6 | 14.6 | 14.6 | 0.0 |
| config | 14.6 | 14.6 | 14.6 | 0.0 |
| gear 1 | 13.6 | 12.1 | 15.3 | 3.2 |
| tree greedy | 76.3 | 82.4 | 85.0 | 8.7 |
| gear 2 | 126.6 | 136.8 | 157.8 | 31.3 |
| tree rebuilt | 144.5 | 155.3 | 174.7 | 30.2 |
| loop pass 1 | 163.7 | 200.4 | 186.5 | 36.7 |
| loop pass 2 | 168.2 | 233.5 | 190.1 | 65.3 |
| loop pass 3 | 195.5 | 238.3 | 190.1 | 48.2 |
| loop pass 4 | 200.2 | 244.6 | - | 44.5 (n=2) |
| loop pass 5 | 200.2 | 244.6 | - | 44.5 (n=2) |
| final | 204.2 | 247.5 | 197.2 | 50.2 |

First stage where the spread exceeds 10 points: **gear 2** (31.3). Largest spread: **loop pass 2** (65.3).

### kinetic_bolt_wander  (spread 46.6; best s1 162.3, worst s3 115.6)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 3.2 | 3.2 | 3.2 | 0.0 |
| config | 6.6 | 6.6 | 6.6 | 0.0 |
| gear 1 | 3.9 | 3.2 | 3.2 | 0.7 |
| tree greedy | 89.7 | 56.2 | 58.4 | 33.5 |
| gear 2 | 98.6 | 77.7 | 68.4 | 30.2 |
| tree rebuilt | 101.1 | 113.7 | 78.1 | 35.6 |
| loop pass 1 | 103.3 | 117.6 | 91.9 | 25.6 |
| loop pass 2 | 115.4 | 123.8 | 104.9 | 18.8 |
| loop pass 3 | 150.3 | 125.2 | 113.6 | 36.7 |
| loop pass 4 | 154.7 | 127.3 | 115.6 | 39.1 |
| loop pass 5 | 158.3 | 128.8 | 115.6 | 42.7 |
| loop pass 6 | 162.3 | - | - | -  (n=1) |
| final | 162.3 | 128.8 | 115.6 | 46.6 |

First stage where the spread exceeds 10 points: **tree greedy** (33.5). Largest spread: **final** (46.6).

### cold_dot  (spread 44.5; best s3 142.4, worst s2 97.9)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 17.3 | 17.3 | 17.3 | 0.0 |
| config | 17.3 | 17.3 | 17.3 | 0.0 |
| gear 1 | 11.4 | 11.4 | 11.5 | 0.1 |
| tree greedy | 56.3 | 51.6 | 43.0 | 13.3 |
| gear 2 | 94.5 | 60.1 | 64.7 | 34.4 |
| tree rebuilt | 113.5 | 71.4 | 103.5 | 42.1 |
| loop pass 1 | 134.8 | 89.0 | 113.6 | 45.8 |
| loop pass 2 | 137.2 | 90.4 | 118.1 | 46.8 |
| loop pass 3 | 140.4 | 97.9 | 128.6 | 42.5 |
| loop pass 4 | 140.4 | 97.9 | 137.9 | 42.5 |
| loop pass 5 | - | - | 140.2 | -  (n=1) |
| loop pass 6 | - | - | 142.4 | -  (n=1) |
| loop pass 7 | - | - | 142.4 | -  (n=1) |
| final | 140.9 | 97.9 | 142.4 | 44.5 |

First stage where the spread exceeds 10 points: **tree greedy** (13.3). Largest spread: **loop pass 2** (46.8).

### burning_arrow_snipe  (spread 41.7; best s1 212.3, worst s2 170.6)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 2.2 | 2.2 | 2.2 | 0.0 |
| config | 13.0 | 13.0 | 13.0 | 0.0 |
| gear 1 | 9.1 | 13.6 | 10.9 | 4.5 |
| tree greedy | 59.7 | 86.9 | 80.7 | 27.3 |
| gear 2 | 83.5 | 80.8 | 92.2 | 11.4 |
| tree rebuilt | 96.3 | 69.1 | 81.9 | 27.2 |
| loop pass 1 | 127.2 | 102.9 | 115.6 | 24.3 |
| loop pass 2 | 142.9 | 120.1 | 130.2 | 22.7 |
| loop pass 3 | 148.6 | 120.1 | 133.5 | 28.5 |
| loop pass 4 | 148.6 | - | 133.5 | 15.1 (n=2) |
| final | 212.3 | 170.6 | 188.9 | 41.7 |

First stage where the spread exceeds 10 points: **tree greedy** (27.3). Largest spread: **final** (41.7).

### poison_spark  (spread 41.6; best s1 120.0, worst s2 78.4)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 3.2 | 3.2 | 3.2 | 0.0 |
| config | 5.7 | 5.7 | 5.7 | 0.0 |
| gear 1 | 1.9 | 2.5 | 2.1 | 0.6 |
| tree greedy | 25.4 | 31.2 | 32.7 | 7.3 |
| gear 2 | 28.4 | 29.9 | 30.3 | 1.9 |
| tree rebuilt | 37.6 | 36.3 | 32.7 | 4.9 |
| loop pass 1 | 56.5 | 51.9 | 45.0 | 11.5 |
| loop pass 2 | 68.4 | 61.1 | 53.5 | 14.9 |
| loop pass 3 | 70.7 | 61.9 | 54.2 | 16.5 |
| loop pass 4 | 72.5 | 67.1 | 60.9 | 11.6 |
| loop pass 5 | 73.3 | 69.9 | 61.3 | 12.0 |
| loop pass 6 | 93.4 | 73.6 | 64.4 | 29.0 |
| loop pass 7 | 103.7 | 76.1 | 65.9 | 37.8 |
| loop pass 8 | 104.7 | 76.1 | 66.8 | 37.9 |
| loop pass 9 | 112.4 | - | 79.6 | 32.8 (n=2) |
| loop pass 10 | 117.8 | - | 79.6 | 38.3 (n=2) |
| loop pass 11 | 117.8 | - | - | -  (n=1) |
| final | 120.0 | 78.4 | 82.3 | 41.6 |

First stage where the spread exceeds 10 points: **loop pass 1** (11.5). Largest spread: **final** (41.6).

### poison_spectral_throw  (spread 41.4; best s2 217.7, worst s1 176.3)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 2.0 | 2.0 | 2.0 | 0.0 |
| config | 3.5 | 3.5 | 3.5 | 0.0 |
| gear 1 | 2.9 | 2.9 | 2.9 | 0.1 |
| tree greedy | 113.3 | 126.4 | 118.5 | 13.1 |
| gear 2 | 112.6 | 124.6 | 121.4 | 12.0 |
| tree rebuilt | 120.4 | 123.0 | 126.9 | 6.4 |
| loop pass 1 | 142.7 | 155.9 | 144.4 | 13.2 |
| loop pass 2 | 142.7 | 162.4 | 146.8 | 19.7 |
| loop pass 3 | - | 167.8 | 154.5 | 13.3 (n=2) |
| loop pass 4 | - | 168.7 | 163.9 | 4.8 (n=2) |
| loop pass 5 | - | 175.1 | 163.9 | 11.2 (n=2) |
| loop pass 6 | - | 176.0 | - | -  (n=1) |
| loop pass 7 | - | 176.0 | - | -  (n=1) |
| final | 176.3 | 217.7 | 201.8 | 41.4 |

First stage where the spread exceeds 10 points: **tree greedy** (13.1). Largest spread: **final** (41.4).

### stormbrand  (spread 36.4; best s2 180.5, worst s3 144.1)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 7.9 | 7.9 | 7.9 | 0.0 |
| config | 9.0 | 9.0 | 9.0 | 0.0 |
| gear 1 | 7.5 | 6.8 | 9.3 | 2.5 |
| tree greedy | 88.1 | 89.0 | 103.5 | 15.4 |
| gear 2 | 99.1 | 134.4 | 87.2 | 47.1 |
| tree rebuilt | 99.1 | 134.4 | 91.3 | 43.1 |
| loop pass 1 | 135.2 | 162.0 | 132.8 | 29.3 |
| loop pass 2 | 144.4 | 165.2 | 133.5 | 31.7 |
| loop pass 3 | 156.9 | 177.5 | 144.1 | 33.4 |
| loop pass 4 | 168.1 | 180.5 | 144.1 | 36.4 |
| loop pass 5 | 168.1 | 180.5 | - | 12.4 (n=2) |
| final | 171.7 | 180.5 | 144.1 | 36.4 |

First stage where the spread exceeds 10 points: **tree greedy** (15.4). Largest spread: **gear 2** (47.1).

### soulrend_chaos_dot  (spread 33.5; best s1 201.7, worst s3 168.2)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 12.4 | 12.4 | 12.4 | 0.0 |
| config | 19.0 | 19.0 | 19.0 | 0.0 |
| gear 1 | 27.6 | 27.4 | 25.0 | 2.6 |
| tree greedy | 149.8 | 148.8 | 136.6 | 13.2 |
| gear 2 | 150.7 | 150.2 | 136.2 | 14.5 |
| tree rebuilt | 157.5 | 155.2 | 145.9 | 11.6 |
| loop pass 1 | 179.0 | 164.7 | 124.7 | 54.4 |
| loop pass 2 | 189.8 | 183.2 | 127.6 | 62.2 |
| loop pass 3 | 201.7 | 188.6 | 160.3 | 41.4 |
| loop pass 4 | 201.7 | 188.6 | 165.8 | 35.9 |
| loop pass 5 | - | - | 165.8 | -  (n=1) |
| final | 201.7 | 190.8 | 168.2 | 33.5 |

First stage where the spread exceeds 10 points: **tree greedy** (13.2). Largest spread: **loop pass 2** (62.2).

### winter_orb  (spread 32.0; best s2 301.0, worst s1 269.0)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 6.9 | 6.9 | 6.9 | 0.0 |
| config | 9.1 | 9.1 | 9.1 | 0.0 |
| gear 1 | 6.2 | 4.9 | 5.2 | 1.3 |
| tree greedy | 68.7 | 61.9 | 62.7 | 6.8 |
| gear 2 | 86.7 | 75.7 | 84.3 | 11.0 |
| tree rebuilt | 98.3 | 77.6 | 88.7 | 20.8 |
| loop pass 1 | 203.9 | 199.0 | 188.5 | 15.4 |
| loop pass 2 | 213.9 | 204.0 | 211.3 | 9.9 |
| loop pass 3 | 246.6 | 226.3 | 213.9 | 32.7 |
| loop pass 4 | 252.8 | 272.2 | 233.1 | 39.0 |
| loop pass 5 | 262.9 | 296.3 | 235.3 | 61.0 |
| loop pass 6 | 265.7 | 296.3 | 250.0 | 46.3 |
| loop pass 7 | 265.7 | - | 253.1 | 12.6 (n=2) |
| loop pass 8 | - | - | 272.5 | -  (n=1) |
| loop pass 9 | - | - | 275.4 | -  (n=1) |
| loop pass 10 | - | - | 279.5 | -  (n=1) |
| loop pass 11 | - | - | 279.5 | -  (n=1) |
| final | 269.0 | 301.0 | 282.4 | 32.0 |

First stage where the spread exceeds 10 points: **gear 2** (11.0). Largest spread: **loop pass 5** (61.0).

### physical_dot  (spread 27.6; best s2 265.5, worst s1 237.9)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 24.5 | 24.5 | 24.5 | 0.0 |
| config | 24.5 | 24.5 | 24.5 | 0.0 |
| gear 1 | 19.2 | 15.9 | 19.2 | 3.4 |
| tree greedy | 174.2 | 178.0 | 132.6 | 45.5 |
| gear 2 | 201.5 | 178.0 | 154.5 | 47.1 |
| tree rebuilt | 201.5 | 139.8 | 160.3 | 61.8 |
| loop pass 1 | 194.8 | 197.4 | 144.1 | 53.3 |
| loop pass 2 | 194.8 | 203.4 | 179.5 | 23.9 |
| loop pass 3 | - | 219.2 | 185.6 | 33.6 (n=2) |
| loop pass 4 | - | 219.2 | 198.8 | 20.3 (n=2) |
| loop pass 5 | - | - | 198.8 | -  (n=1) |
| final | 237.9 | 265.5 | 240.2 | 27.6 |

First stage where the spread exceeds 10 points: **tree greedy** (45.5). Largest spread: **tree rebuilt** (61.8).

### kinetic_fusillade  (spread 27.3; best s2 212.8, worst s3 185.5)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 6.2 | 6.2 | 6.2 | 0.0 |
| config | 9.4 | 9.4 | 9.4 | 0.0 |
| gear 1 | 6.5 | 7.7 | 7.0 | 1.2 |
| tree greedy | 101.1 | 118.1 | 103.8 | 17.0 |
| gear 2 | 112.1 | 138.4 | 127.2 | 26.3 |
| tree rebuilt | 119.9 | 125.5 | 134.9 | 15.0 |
| loop pass 1 | 172.9 | 148.2 | 157.0 | 24.7 |
| loop pass 2 | 178.6 | 149.1 | 164.0 | 29.5 |
| loop pass 3 | 188.8 | 191.3 | 174.8 | 16.5 |
| loop pass 4 | 190.5 | 212.8 | 182.9 | 29.9 |
| loop pass 5 | 194.7 | 212.8 | 185.5 | 27.3 |
| loop pass 6 | 197.8 | - | 185.5 | 12.3 (n=2) |
| loop pass 7 | 197.8 | - | - | -  (n=1) |
| final | 198.3 | 212.8 | 185.5 | 27.3 |

First stage where the spread exceeds 10 points: **tree greedy** (17.0). Largest spread: **loop pass 4** (29.9).

### exsanguinate_mines  (spread 26.1; best s3 170.2, worst s1 144.2)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 5.7 | 5.7 | 5.7 | 0.0 |
| config | 5.7 | 5.7 | 5.7 | 0.0 |
| gear 1 | 3.7 | 3.4 | 5.0 | 1.5 |
| tree greedy | 72.1 | 75.7 | 59.9 | 15.8 |
| gear 2 | 92.0 | 91.0 | 70.5 | 21.5 |
| tree rebuilt | 89.1 | 105.2 | 105.8 | 16.7 |
| loop pass 1 | 124.2 | 127.6 | 170.2 | 46.1 |
| loop pass 2 | 124.8 | 157.0 | 170.2 | 45.4 |
| loop pass 3 | 125.8 | 162.9 | - | 37.1 (n=2) |
| loop pass 4 | 144.2 | 162.9 | - | 18.7 (n=2) |
| loop pass 5 | 144.2 | - | - | -  (n=1) |
| final | 144.2 | 162.9 | 170.2 | 26.1 |

First stage where the spread exceeds 10 points: **tree greedy** (15.8). Largest spread: **loop pass 1** (46.1).

### spectral_shield_throw  (spread 15.3; best s1 184.2, worst s2 168.9)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 4.1 | 4.1 | 4.1 | 0.0 |
| config | 10.5 | 10.5 | 10.5 | 0.0 |
| gear 1 | 4.0 | 5.8 | 5.9 | 1.9 |
| tree greedy | 67.7 | 96.3 | 97.4 | 29.7 |
| gear 2 | 116.2 | 97.3 | 97.4 | 18.9 |
| tree rebuilt | 119.1 | 100.2 | 97.1 | 22.0 |
| loop pass 1 | 155.2 | 107.1 | 129.3 | 48.1 |
| loop pass 2 | 155.2 | 115.5 | 130.4 | 39.7 |
| loop pass 3 | - | 116.9 | 131.6 | 14.7 (n=2) |
| loop pass 4 | - | 132.6 | 133.5 | 0.9 (n=2) |
| loop pass 5 | - | 141.4 | 138.1 | 3.3 (n=2) |
| loop pass 6 | - | 141.4 | 144.9 | 3.5 (n=2) |
| loop pass 7 | - | - | 144.9 | -  (n=1) |
| final | 184.2 | 168.9 | 170.7 | 15.3 |

First stage where the spread exceeds 10 points: **tree greedy** (29.7). Largest spread: **loop pass 1** (48.1).

### arc_archmage  (spread 15.0; best s3 105.6, worst s2 90.6)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 11.6 | 11.6 | 11.6 | 0.0 |
| config | 11.6 | 11.6 | 11.6 | 0.0 |
| gear 1 | 7.8 | 8.5 | 8.7 | 0.9 |
| tree greedy | 51.9 | 60.6 | 53.2 | 8.7 |
| gear 2 | 53.4 | 63.7 | 52.2 | 11.5 |
| tree rebuilt | 55.7 | 70.6 | 56.5 | 14.8 |
| loop pass 1 | 62.1 | 71.2 | 65.4 | 9.1 |
| loop pass 2 | 64.5 | 77.8 | 69.4 | 13.2 |
| loop pass 3 | 76.3 | 81.2 | 70.1 | 11.1 |
| loop pass 4 | 80.6 | 83.6 | 71.7 | 11.9 |
| loop pass 5 | 84.9 | 84.1 | 76.7 | 8.2 |
| loop pass 6 | 86.6 | 84.1 | 79.4 | 7.1 |
| loop pass 7 | 89.4 | - | 95.3 | 5.9 (n=2) |
| loop pass 8 | 95.1 | - | 98.0 | 2.9 (n=2) |
| loop pass 9 | 95.1 | - | 98.0 | 2.9 (n=2) |
| final | 102.8 | 90.6 | 105.6 | 15.0 |

First stage where the spread exceeds 10 points: **gear 2** (11.5). Largest spread: **final** (15.0).

### archmage_volatile_dead  (spread 13.9; best s3 136.2, worst s2 122.3)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 5.4 | 5.4 | 5.4 | 0.0 |
| config | 10.2 | 10.2 | 10.2 | 0.0 |
| gear 1 | 9.3 | 8.5 | 9.2 | 0.9 |
| tree greedy | 91.7 | 84.2 | 84.6 | 7.5 |
| gear 2 | 87.5 | 88.3 | 80.7 | 7.6 |
| tree rebuilt | 94.3 | 95.7 | 85.3 | 10.3 |
| loop pass 1 | 104.0 | 108.3 | 97.6 | 10.7 |
| loop pass 2 | 105.7 | 112.6 | 106.8 | 7.0 |
| loop pass 3 | 108.7 | 114.0 | 108.8 | 5.3 |
| loop pass 4 | 109.2 | 114.0 | 119.9 | 10.6 |
| loop pass 5 | 124.3 | - | 126.6 | 2.3 (n=2) |
| loop pass 6 | 124.3 | - | 126.6 | 2.3 (n=2) |
| final | 132.9 | 122.3 | 136.2 | 13.9 |

First stage where the spread exceeds 10 points: **tree rebuilt** (10.3). Largest spread: **final** (13.9).

### toxic_rain  (spread 12.9; best s1 141.7, worst s2 128.8)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 0.5 | 0.5 | 0.5 | 0.0 |
| config | 4.7 | 4.7 | 4.7 | 0.0 |
| gear 1 | 4.7 | 4.9 | 3.5 | 1.4 |
| tree greedy | 71.3 | 52.4 | 56.6 | 18.9 |
| gear 2 | 88.5 | 74.1 | 99.9 | 25.9 |
| tree rebuilt | 98.2 | 83.8 | 98.3 | 14.5 |
| loop pass 1 | 123.6 | 114.6 | 127.6 | 13.0 |
| loop pass 2 | 126.0 | 117.6 | 131.9 | 14.4 |
| loop pass 3 | 137.2 | 122.2 | 135.9 | 15.0 |
| loop pass 4 | 138.3 | 126.6 | 135.9 | 11.7 |
| loop pass 5 | 138.3 | 126.6 | - | 11.7 (n=2) |
| final | 141.7 | 128.8 | 138.5 | 12.9 |

First stage where the spread exceeds 10 points: **tree greedy** (18.9). Largest spread: **gear 2** (25.9).

### impale_cyclone  (spread 12.0; best s3 131.3, worst s2 119.3)

| stage | s1 | s2 | s3 | spread at this stage |
|---|---|---|---|---|
| skeleton | 1.2 | 1.2 | 1.2 | 0.0 |
| config | 1.2 | 1.2 | 1.2 | 0.0 |
| gear 1 | 0.6 | 0.7 | 0.8 | 0.2 |
| tree greedy | 22.9 | 31.3 | 22.3 | 9.0 |
| gear 2 | 63.6 | 33.2 | 72.7 | 39.6 |
| tree rebuilt | 71.6 | 43.9 | 72.7 | 28.9 |
| loop pass 1 | 84.8 | 58.5 | 106.1 | 47.6 |
| loop pass 2 | 100.3 | 60.5 | 106.1 | 45.7 |
| loop pass 3 | 100.3 | 94.5 | - | 5.7 (n=2) |
| loop pass 4 | - | 94.5 | - | -  (n=1) |
| final | 124.1 | 119.3 | 131.3 | 12.0 |

First stage where the spread exceeds 10 points: **gear 2** (39.6). Largest spread: **loop pass 1** (47.6).

## 3. Summary over the 29 references with spread > 10

### 3a. First stage whose spread exceeds 10 points

| stage | references |
|---|---|
| tree greedy | 19 |
| gear 2 | 8 |
| tree rebuilt | 1 |
| loop pass 1 | 1 |

### 3b. Stage holding the largest spread

| stage | references |
|---|---|
| gear 2 | 2 |
| tree rebuilt | 1 |
| loop pass 1 | 3 |
| loop pass 2 | 5 |
| loop pass 4 | 1 |
| loop pass 5 | 2 |
| final | 15 |

## 4. What the best and the worst seed did at the divergence stage

The divergence stage = the first stage whose spread exceeds 10 points (section 2).
Quoted verbatim from `logs/<slug>-s<seed>.log`. For a loop pass the quoted line is the
pass's own summary line (it carries the refine / swaps / kick / picks notes). For a
construction stage the first quoted line is the stage's own summary line and the second,
where one exists, is the detail line inside that stage's block with the largest absolute
change in value.

### shockwave_cyclone

Divergence stage: `tree greedy`.  best = s1, worst = s3.

**best  s1**

```
  tree greedy                    157s  value      344,934  viol 0.033  ramp 0.0s/2.5s  budget spent  [+5819.1% vs gear pass 1 (empty tree)]
  + 5 notable   Merciless Skewering              value 257,432 -> 293,316 (viol 1.001 -> 1.001) [276 cands, 2.2s]
```

**worst s3**

```
  tree greedy                    120s  value      240,345  viol 0.000  ramp 0.0s/2.5s  budget spent  [+3574.5% vs gear pass 1 (empty tree)]
  + 4 notable   Titanic Impacts                  value 176,858 -> 207,129 (viol 1.068 -> 1.068) [260 cands, 2.6s]
```

### static_strike

Divergence stage: `tree greedy`.  best = s3, worst = s1.

**best  s3**

```
  tree greedy                    127s  value       99,208  viol 0.047  ramp 0.0s/2.5s  budget spent  [+1029.5% vs gear pass 1 (empty tree)]
  + 6 notable   Titanic Impacts                  value 77,032 -> 88,252 (viol 2.498 -> 2.484) [150 cands, 2.1s]
```

**worst s1**

```
  tree greedy                    135s  value       78,187  viol 0.093  ramp 0.0s/2.5s  budget spent  [+806.7% vs gear pass 1 (empty tree)]
  + 6 notable   Lava Lash                        value 42,259 -> 47,127 (viol 2.669 -> 2.655) [150 cands, 2.7s]
```

### regular_viper_strike

Divergence stage: `gear pass 2 (with tree)`.  best = s2, worst = s3.

**best  s2**

```
  gear pass 2 (with tree)         62s  value      244,076  viol 0.527  ramp 3.4s/3.5s    [+11.3% vs tree greedy]
[Weapon 1] best of 200: 0 -> 244,076 (viol 0.042 -> 0.031) [2.4s]
```

**worst s3**

```
  gear pass 2 (with tree)         68s  value      387,759  viol 0.219  ramp 3.4s/3.4s    [+90.0% vs tree greedy]
[Weapon 1] best of 200: 0 -> 387,759 (viol 0.000 -> 0.000) [2.6s]
```

### absolution_minions

Divergence stage: `tree greedy`.  best = s1, worst = s3.

**best  s1**

```
  tree greedy                    238s  value      651,531  viol 0.019  ramp 0.0s/2.5s  budget spent  [+241.1% vs gear pass 1 (empty tree)]
  + 5 notable   Influence                        value 460,603 -> 522,651 (viol 1.273 -> 1.185) [249 cands, 5.6s]
```

**worst s3**

```
  tree greedy                    196s  value      451,844  viol 0.000  ramp 0.0s/2.5s  budget spent  [+138.8% vs gear pass 1 (empty tree)]
  + 3 notable   Crackling Speed                  value 412,648 -> 451,844 (viol 0.000 -> 0.000) [202 cands, 5.2s]
```

### bleed_bow

Divergence stage: `tree greedy`.  best = s1, worst = s3.

**best  s1**

```
  tree greedy                    302s  value      407,015  viol 0.085  ramp 1.4s/2.5s  budget spent  [+839.7% vs gear pass 1 (empty tree)]
  + 3 notable   Defiant Stand                    value 251,805 -> 289,207 (viol 2.974 -> 2.752) [297 cands, 45.4s]
```

**worst s3**

```
  tree greedy                    269s  value      426,255  viol 0.023  ramp 1.4s/2.5s  budget spent  [+786.4% vs gear pass 1 (empty tree)]
  + 3 notable   Defiant Stand                    value 309,072 -> 356,189 (viol 1.875 -> 1.530) [300 cands, 38.6s]
```

### lightning_trap

Divergence stage: `gear pass 2 (with tree)`.  best = s2, worst = s3.

**best  s2**

```
  gear pass 2 (with tree)         36s  value      485,054  viol 0.483  ramp 0.0s/2.5s    [+16.5% vs tree greedy]
[Weapon 2] best of 200: 380,418 -> 485,054 (viol 1.291 -> 0.483) [1.5s]
```

**worst s3**

```
  gear pass 2 (with tree)         36s  value      408,894  viol 0.227  ramp 0.0s/2.5s    [-5.9% vs tree greedy]
[Weapon 1] best of 200: 399,519 -> 485,820 (viol 0.586 -> 0.246); bench +12 to all Attributes: -> 485,820 (viol 0.230) [1.9s]
```

### hit_penance_brand

Divergence stage: `tree greedy`.  best = s3, worst = s2.

**best  s3**

```
  tree greedy                    130s  value    1,764,686  viol 0.762  ramp 0.0s/2.5s  budget spent  [+1085.4% vs gear pass 1 (empty tree)]
  + 5 notable   Force Shaper                     value 1,426,392 -> 1,642,915 (viol 3.800 -> 3.800) [279 cands, 3.1s]
```

**worst s2**

```
  tree greedy                    137s  value    1,772,525  viol 0.311  ramp 0.0s/2.5s  budget spent  [+1203.9% vs gear pass 1 (empty tree)]
  + 5 notable   Assassination                    value 1,201,342 -> 1,398,109 (viol 3.099 -> 3.090) [274 cands, 4.2s]
```

### spark

Divergence stage: `gear pass 2 (with tree)`.  best = s2, worst = s3.

**best  s2**

```
  gear pass 2 (with tree)         61s  value      462,939  viol 0.007  ramp 0.6s/2.5s    [+11.0% vs tree greedy]
[Weapon 2] best of 200: 389,773 -> 462,939 (viol 0.020 -> 0.007) [1.8s]
```

**worst s3**

```
  gear pass 2 (with tree)         58s  value      414,409  viol 0.062  ramp 0.6s/2.5s    [-9.6% vs tree greedy]
[Weapon 1] best of 200: 363,959 -> 414,409 (viol 0.072 -> 0.062) [1.8s]
```

### elemental_hit

Divergence stage: `gear pass 2 (with tree)`.  best = s3, worst = s1.

**best  s3**

```
  gear pass 2 (with tree)         33s  value      144,918  viol 0.282  ramp 0.0s/2.5s    [+4.8% vs tree greedy]
[Weapon 1] best of 200: 0 -> 144,918 (viol 0.111 -> 0.030) [1.5s]
```

**worst s1**

```
  gear pass 2 (with tree)         33s  value      144,794  viol 0.860  ramp 0.0s/2.5s    [+0.4% vs tree greedy]
[Weapon 1] best of 200: 0 -> 144,794 (viol 0.061 -> 0.526) [1.3s]
```

### impale_ballista

Divergence stage: `tree greedy`.  best = s3, worst = s2.

**best  s3**

```
  tree greedy                    184s  value      386,685  viol 1.009  ramp 0.0s/2.5s  budget spent  [+3499.9% vs gear pass 1 (empty tree)]
  + 6 notable   Master Fletcher                  value 203,241 -> 249,136 (viol 3.013 -> 3.013) [237 cands, 5.7s]
```

**worst s2**

```
  tree greedy                    193s  value      262,643  viol 0.941  ramp 0.0s/2.5s  budget spent  [+2267.0% vs gear pass 1 (empty tree)]
  + 6 notable   Multishot                        value 196,560 -> 237,252 (viol 3.204 -> 3.204) [215 cands, 5.2s]
```

### smite

Divergence stage: `tree greedy`.  best = s1, worst = s2.

**best  s1**

```
  tree greedy                    155s  value      287,231  viol 0.417  ramp 0.0s/2.5s  budget spent  [+1486.8% vs gear pass 1 (empty tree)]
  + 6 notable   Dismembering                     value 240,067 -> 267,079 (viol 3.662 -> 3.640) [229 cands, 21.7s]
```

**worst s2**

```
  tree greedy                    205s  value      311,266  viol 0.485  ramp 0.0s/2.5s  budget spent  [+1633.1% vs gear pass 1 (empty tree)]
  + 1 mastery   Elemental Mastery                effect=17942 value 188,313 -> 224,242 (viol 1.138 -> 1.138) [300 cands, 3.5s]
```

### pyroclast_mine

Divergence stage: `tree greedy`.  best = s3, worst = s1.

**best  s3**

```
  tree greedy                     93s  value      103,528  viol 0.032  ramp 0.0s/2.5s  budget spent  [+692.7% vs gear pass 1 (empty tree)]
  + 4 notable   High Voltage                     value 85,138 -> 93,574 (viol 1.660 -> 1.656) [163 cands, 1.6s]
```

**worst s1**

```
  tree greedy                     77s  value      114,976  viol 0.051  ramp 0.0s/2.5s  budget spent  [+747.4% vs gear pass 1 (empty tree)]
  + 1 mastery   Fire Mastery                     effect=6216 value 62,785 -> 75,684 (viol 1.514 -> 1.514) [207 cands, 1.9s]
```

### summon_raging_spirits

Divergence stage: `gear pass 2 (with tree)`.  best = s2, worst = s3.

**best  s2**

```
  gear pass 2 (with tree)        103s  value      980,183  viol 0.379  ramp 0.0s/2.5s    [+65.9% vs tree greedy]
[Weapon 1] best of 200: 521,740 -> 586,562 (viol 0.990 -> 0.269) [5.5s]
```

**worst s3**

```
  gear pass 2 (with tree)        102s  value    1,131,175  viol 1.000  ramp 0.0s/2.5s    [+85.7% vs tree greedy]
[Weapon 1] best of 200: 501,545 -> 676,976 (viol 1.000 -> 1.000) [7.1s]
```

### kinetic_bolt_wander

Divergence stage: `tree greedy`.  best = s1, worst = s3.

**best  s1**

```
  tree greedy                    425s  value      622,074  viol 0.595  ramp 0.9s/2.5s  budget spent  [+2216.9% vs gear pass 1 (empty tree)]
  + 6 notable   Prism Weave                      value 208,578 -> 253,395 (viol 0.732 -> 0.721) [227 cands, 35.7s]
```

**worst s3**

```
  tree greedy                    276s  value      404,908  viol 0.579  ramp 0.6s/2.5s  budget spent  [+1712.8% vs gear pass 1 (empty tree)]
  + 5 keystone  Resolute Technique               value 42,002 -> 86,655 (viol 1.781 -> 1.753) [91 cands, 1.8s]
```

### cold_dot

Divergence stage: `tree greedy`.  best = s3, worst = s2.

**best  s3**

```
  tree greedy                    117s  value       98,114  viol 0.065  ramp 0.0s/2.5s  budget spent  [+273.4% vs gear pass 1 (empty tree)]
  + 5 notable   Acrimony                         value 52,922 -> 61,679 (viol 1.819 -> 1.809) [186 cands, 6.2s]
```

**worst s2**

```
  tree greedy                    125s  value      117,638  viol 0.000  ramp 0.0s/2.5s  budget spent  [+351.7% vs gear pass 1 (empty tree)]
  + 3 notable   Snowforged                       value 100,336 -> 109,796 (viol 0.787 -> 0.787) [261 cands, 7.9s]
```

### burning_arrow_snipe

Divergence stage: `tree greedy`.  best = s1, worst = s2.

**best  s1**

```
  tree greedy                    176s  value      612,240  viol 0.086  ramp 1.7s/2.5s  budget spent  [+555.8% vs gear pass 1 (empty tree)]
  + 5 notable   Breath of Lightning              value 257,810 -> 308,748 (viol 1.909 -> 1.909) [186 cands, 3.7s]
```

**worst s2**

```
  tree greedy                    154s  value      891,944  viol 0.000  ramp 1.3s/2.5s  budget spent  [+540.5% vs gear pass 1 (empty tree)]
  + 5 notable   Elemental Focus                  value 623,824 -> 713,695 (viol 1.664 -> 1.656) [268 cands, 4.8s]
```

### poison_spark

Divergence stage: `loop pass 1`.  best = s1, worst = s2.

**best  s1**

```
  loop pass 1                    330s  value      329,571  viol 0.000  ramp 2.7s/3.8s  refine -15.6%; swaps +0.7%; Weapon 1 +7.9%; picks: support Faster Projectiles -> Sacrifice (+44.3%); support Efficacy -> Cruelty (+13.7%)  [+50.3% vs tree rebuilt on gear]
```

**worst s2**

```
  loop pass 1                    362s  value      302,851  viol 0.000  ramp 2.7s/3.8s  refine -28.4%; Weapon 1 +10.4%; picks: support Faster Projectiles -> Sacrifice (+59.3%); support Efficacy -> Cruelty (+13.6%)  [+43.2% vs tree rebuilt on gear]
```

### poison_spectral_throw

Divergence stage: `tree greedy`.  best = s2, worst = s1.

**best  s2**

```
  tree greedy                    413s  value      188,540  viol 0.726  ramp 2.8s/3.8s  budget spent  [+4189.7% vs gear pass 1 (empty tree)]
  + 6 notable   Claws of the Magpie              value 48,586 -> 85,628 (viol 2.114 -> 2.114) [277 cands, 26.0s]
```

**worst s1**

```
  tree greedy                    176s  value      169,013  viol 0.821  ramp 2.8s/3.8s  budget spent  [+3840.4% vs gear pass 1 (empty tree)]
  + 6 notable   Claws of the Magpie              value 47,169 -> 82,892 (viol 2.449 -> 2.449) [280 cands, 15.9s]
```

### stormbrand

Divergence stage: `tree greedy`.  best = s2, worst = s3.

**best  s2**

```
  tree greedy                    186s  value    1,236,011  viol 0.375  ramp 0.0s/2.5s  budget spent  [+1203.1% vs gear pass 1 (empty tree)]
  + 1 mastery   Caster Mastery                   effect=33089 value 762,398 -> 895,649 (viol 3.748 -> 3.748) [265 cands, 15.3s]
```

**worst s3**

```
  tree greedy                    232s  value    1,436,964  viol 0.173  ramp 0.0s/2.5s  budget spent  [+1009.7% vs gear pass 1 (empty tree)]
  + 1 mastery   Caster Mastery                   effect=33089 value 944,158 -> 1,108,418 (viol 3.808 -> 3.808) [265 cands, 16.5s]
```

### soulrend_chaos_dot

Divergence stage: `tree greedy`.  best = s1, worst = s3.

**best  s1**

```
  tree greedy                    105s  value      361,124  viol 0.187  ramp 0.0s/2.5s  budget spent  [+443.0% vs gear pass 1 (empty tree)]
  + 5 notable   Heart of Darkness                value 276,749 -> 312,362 (viol 1.819 -> 1.815) [270 cands, 10.4s]
```

**worst s3**

```
  tree greedy                    110s  value      329,281  viol 0.142  ramp 0.0s/2.5s  budget spent  [+445.9% vs gear pass 1 (empty tree)]
  + 5 notable   Heart of Darkness                value 250,716 -> 283,748 (viol 1.744 -> 1.741) [256 cands, 10.8s]
```

### winter_orb

Divergence stage: `gear pass 2 (with tree)`.  best = s2, worst = s1.

**best  s2**

```
  gear pass 2 (with tree)         43s  value       79,430  viol 0.000  ramp 0.0s/2.5s    [+22.3% vs tree greedy]
[Weapon 1] best of 200: 69,580 -> 79,196 (viol 0.121 -> 0.000) [2.5s]
```

**worst s1**

```
  gear pass 2 (with tree)         39s  value       90,945  viol 0.000  ramp 0.0s/2.5s    [+26.3% vs tree greedy]
[Weapon 1] best of 200: 65,850 -> 85,531 (viol 0.019 -> 0.000) [2.0s]
```

### physical_dot

Divergence stage: `tree greedy`.  best = s2, worst = s1.

**best  s2**

```
  tree greedy                    110s  value      149,990  viol 0.741  ramp 0.0s/2.5s  budget spent  [+1022.9% vs gear pass 1 (empty tree)]
  + 6 notable   Spiritual Aid                    value 101,059 -> 127,171 (viol 1.070 -> 1.066) [234 cands, 2.2s]
```

**worst s1**

```
  tree greedy                    116s  value      146,729  viol 0.680  ramp 0.0s/2.5s  no candidate improves the objective  [+806.8% vs gear pass 1 (empty tree)]
  + 6 notable   Spiritual Aid                    value 106,242 -> 132,354 (viol 1.033 -> 1.028) [234 cands, 2.0s]
```

### kinetic_fusillade

Divergence stage: `tree greedy`.  best = s2, worst = s3.

**best  s2**

```
  tree greedy                    312s  value      315,360  viol 0.306  ramp 0.8s/2.5s  budget spent  [+1432.3% vs gear pass 1 (empty tree)]
  + 6 notable   Prism Weave                      value 115,046 -> 140,264 (viol 1.546 -> 1.495) [187 cands, 3.8s]
```

**worst s3**

```
  tree greedy                    330s  value      277,190  viol 0.200  ramp 0.8s/2.5s  budget spent  [+1373.0% vs gear pass 1 (empty tree)]
  + 6 notable   Prism Weave                      value 112,292 -> 136,733 (viol 2.110 -> 2.065) [187 cands, 3.6s]
```

### exsanguinate_mines

Divergence stage: `tree greedy`.  best = s3, worst = s1.

**best  s3**

```
  tree greedy                    123s  value      198,980  viol 0.196  ramp 0.0s/2.6s  budget spent  [+1107.1% vs gear pass 1 (empty tree)]
  + 6 notable   Throatseeker                     value 162,343 -> 177,500 (viol 1.814 -> 1.804) [172 cands, 1.0s]
```

**worst s1**

```
  tree greedy                    112s  value      239,735  viol 0.580  ramp 0.0s/2.5s  budget spent  [+1830.0% vs gear pass 1 (empty tree)]
  + 4 notable   Master Sapper                    value 89,867 -> 134,951 (viol 1.428 -> 1.428) [151 cands, 13.6s]
```

### spectral_shield_throw

Divergence stage: `tree greedy`.  best = s1, worst = s2.

**best  s1**

```
  tree greedy                    238s  value      152,044  viol 0.073  ramp 0.3s/2.5s  budget spent  [+1571.6% vs gear pass 1 (empty tree)]
  + 3 notable   Defiant Stand                    value 97,422 -> 110,847 (viol 2.319 -> 2.016) [284 cands, 34.9s]
```

**worst s2**

```
  tree greedy                    231s  value      216,342  viol 0.107  ramp 0.3s/2.5s  budget spent  [+1567.1% vs gear pass 1 (empty tree)]
  + 3 notable   Defiant Stand                    value 139,695 -> 159,005 (viol 2.401 -> 2.103) [284 cands, 34.1s]
```

### arc_archmage

Divergence stage: `gear pass 2 (with tree)`.  best = s3, worst = s2.

**best  s3**

```
  gear pass 2 (with tree)         40s  value      291,751  viol 0.462  ramp 0.0s/2.5s    [-1.9% vs tree greedy]
[Weapon 1] best of 200: 241,835 -> 291,751 (viol 0.606 -> 0.462) [1.4s]
```

**worst s2**

```
  gear pass 2 (with tree)         41s  value      355,933  viol 0.520  ramp 0.0s/2.5s    [+5.1% vs tree greedy]
[Weapon 1] best of 200: 303,523 -> 366,129 (viol 0.577 -> 0.529) [1.5s]
```

### archmage_volatile_dead

Divergence stage: `tree rebuilt on gear`.  best = s3, worst = s2.

**best  s3**

```
  tree rebuilt on gear           597s  value      784,912  viol 0.361  ramp 1.0s/2.5s  741,770 (viol 0.016) -> 784,912 (viol 0.000) kept [sum 784,912 (viol 0.000); cover 784,454 (viol 0.000)]  [+5.8% vs gear pass 2 (with tree)]
  + 6 notable   Heart of Thunder                 value 449,271 -> 512,560 (viol 1.824 -> 1.821) [233 cands, 36.4s]
```

**worst s2**

```
  tree rebuilt on gear           624s  value      880,028  viol 0.372  ramp 1.0s/2.5s  811,981 (viol 0.000) -> 880,028 (viol 0.000) kept [sum 880,028 (viol 0.000); cover 863,262 (viol 0.000)]  [+8.4% vs gear pass 2 (with tree)]
  + 6 notable   Heart of Thunder                 value 470,436 -> 537,423 (viol 1.546 -> 1.543) [227 cands, 37.1s]
```

### toxic_rain

Divergence stage: `tree greedy`.  best = s1, worst = s2.

**best  s1**

```
  tree greedy                    230s  value      260,327  viol 0.065  ramp 0.0s/2.6s  budget spent  [+1411.0% vs gear pass 1 (empty tree)]
  + 4 notable   Swift Venoms                     value 208,519 -> 225,479 (viol 1.945 -> 1.945) [162 cands, 3.4s]
```

**worst s2**

```
  tree greedy                    229s  value      191,439  viol 0.086  ramp 0.0s/2.5s  budget spent  [+974.0% vs gear pass 1 (empty tree)]
  + 5 notable   Wasting                          value 72,430 -> 85,198 (viol 2.352 -> 2.345) [129 cands, 4.0s]
```

### impale_cyclone

Divergence stage: `gear pass 2 (with tree)`.  best = s3, worst = s2.

**best  s3**

```
  gear pass 2 (with tree)         31s  value      506,839  viol 0.000  ramp 0.0s/2.5s    [+226.7% vs tree greedy]
[Weapon 1] best of 200: 0 -> 450,779 (viol 0.000 -> 0.000) [2.2s]
```

**worst s2**

```
  gear pass 2 (with tree)         32s  value      231,034  viol 0.000  ramp 0.0s/2.5s    [+5.9% vs tree greedy]
[Weapon 1] best of 200: 0 -> 227,083 (viol 0.000 -> 0.000) [1.7s]
```

## 5. Method

Files read:

- `artifacts/benchmark/20260916-1929-new18-frozen/results.json` (54 rows, 18 references x seeds 1-3)
- `artifacts/benchmark/20260917-0844-core14-frozen/results.json` (42 rows, 14 references x seeds 1-3)
- `artifacts/benchmark/<campaign>/logs/<slug>-s<seed>.log`, only for section 4 and only the
  block of the one divergence stage.

The two slug sets are disjoint, so 18 + 14 = 32 references and 96 rows. All 96 have
`ok: true` and `variant: ""`; nothing was filtered out and nothing was skipped.

Fields used: `slug`, `seed`, `variant`, `ok`, `ratio_lane`, `author_lane`, `ours`, and
`stages` (a list of `{name, seconds, value, violation, notes}`).

Per-stage percentages come from `results.json`'s `stages`, not from the logs: the list holds
a numeric `value` for every stage. Three checks were run before using it. (a) `author_lane` is
identical across the three seeds of every slug, so one denominator per reference. (b) the value
of the last stage, `config (final lanes)`, equals `ours` in all 96 rows. (c) `ours / author_lane`
equals `ratio_lane` in all 96 rows. So the final row of every stage table equals that seed's
pct in section 1.

Stage order is the chronological order in `stages`: six construction stages, then
`loop pass 1..N`, then `config (final lanes)` (the "final" row). Loop passes are aligned by
number across seeds. A seed whose loop stopped earlier shows `-`; its spread column is then
max - min over the two seeds that remain, marked `(n=2)`. No carry-forward of a stopped seed's
last value was applied, so a `(n=2)` spread is not comparable with a three-seed one. A pass
down to one seed has no spread at all; those rows print `-  (n=1)` and take no part in either
verdict line. `seconds` was not used.

Ties: "first stage above 10" cannot tie (the first match in stage order wins). "largest spread"
tied in 2 of the 29 references and was broken towards the earlier stage:
`absolution_minions` (loop pass 5 = final = 73.4) and `pyroclast_mine`
(loop pass 2 = final = 50.9); in both the last loop pass and the final lane hold the same
spread, so the count in 3b reads `loop pass 5` and `loop pass 2` rather than `final`.

In the logs each stage's work lines *precede* its summary line (the gear `[Slot] best of 200`
lines come before the `  gear pass 1` line, the tree `+ N notable` lines before
`  tree greedy`). A stage's block is therefore taken as the lines between the previous stage's
summary line and its own. The detail line quoted for a construction stage is picked
deterministically: within that block, the line with the largest absolute `A -> B` change.
Loop passes carry their notes on the summary line itself, so only that one line is quoted.
Line 2 of each log ("under our lane N") was not needed, since `author_lane` is in the JSON.

Nothing under `src/`, `scripts/`, `tests/` or `artifacts/` was modified; no benchmark was run.
