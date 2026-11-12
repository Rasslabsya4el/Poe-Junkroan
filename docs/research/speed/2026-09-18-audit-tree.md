# Speed audit — passive-tree optimizer

Scope: `src/junkroan/optimizer/tree_optimizer.py`, `tree_graph.py`, `objective.py`, and the
`trial_stats` path of `src/junkroan/pob/session.py`. No repo file was changed; every probe ran
from the scratchpad. 2026-09-18, on the same machine as the running campaign (i5-12400F,
6 physical / 12 logical cores, 5 campaign workers live), so every absolute millisecond below is
a *contended* number — the ratios are what carries.

## Evidence base

| source | what it is |
|---|---|
| `scratchpad/build.prof` | cProfile of a full 3,280 s stormbrand build (pre `read_state` fix) |
| `scratchpad/recover2.prof` | fresh cProfile, `recover_tree.py stormbrand --points 20 --rounds 5`, 32 s |
| `scratchpad/probe_batch.py` / `probe_real.py` | `trial_stats` cost vs batch size, key count, build; primitive costs |
| `scratchpad/probe_refine.py` | every trial batch of a real `refine` round timed on `stormbrand-s2.pob.txt` |
| `scratchpad/probe_stale.py` + `stale_dump_*.json` | every candidate's PoB value at every greedy step, stormbrand and bleed_bow |
| `artifacts/benchmark/20260917-0844-core14-frozen/logs/*.log` | 42 real build logs, 4.33 M candidate evaluations |

### Where the build's seconds are (build.prof, 3,280 s)

Tree stages, top level, no double counting (`allocate` is also called by `swap_subtrees` and
`reoptimize`, so those are attributed to their caller):

| stage | calls | seconds | % build |
|---|---|---|---|
| `allocate` called from the pipeline | 7 | 643.4 | 19.6% |
| `refine` called from the pipeline | 7 | 229.7 | 7.0% |
| `swap_subtrees` | 3 | 409.1 | 12.5% |
| `reoptimize` | 3 | 332.4 | 10.1% |
| **tree slice total** | | **1,614.6** | **49.2%** |

Inside that 1,614.6 s: `trial_stats` 1,080.2 s (67%), the pipeline **enabler hook** 388.2 s (24%),
`after_apply_hook` 30.9 s, `mutate_nodes` 40.5 s, `current_score` 38.9 s, `_restore`'s `load_xml`
22.2 s, `export_xml` 2.5 s, **all Python in the slice ~11 s (0.7%)**.

The already-landed `read_state` fix (1,048 ms → 2.4 ms measured) removes ~1,111 s from this build
and ~268 s from the tree slice (it sat inside `derive_config` under the hook). Post-fix baseline:
**build ~2,170 s, tree slice ~1,346 s = 62% of the build, `trial_stats` alone 50% of the build.**
Savings below are quoted against that post-fix baseline.

---

## Ranked findings

| # | finding | file:line | evidence | saving (% of build) | kind | how to prove |
|---|---|---|---|---|---|---|
| 1 | Every greedy step re-evaluates candidates PoB has already reported as completely inert (no DPS change, no violation change) | `tree_optimizer.py:266-279`, `407-416` | stormbrand 4,786 evals: 74.2% zero-DPS, 32.9% fully inert; bleed_bow 5,728 evals: 89.6% / 57.2%. A skip-once-inert rule removes 29.9% / 53.3% of **all** trials | **15-26%** | approximate | 3-seed medians, smoke pair, then core14 |
| 2 | The enabler hook is re-derived per `allocate()` call and 86% of its calls do a full config re-derivation only to return `None` | `tree_optimizer.py:264,293-307,326-328`; `pipeline.py:179,597` | 127 calls, 388.2 s = 11.8% of the pre-fix build (24% of the tree slice); only 18 got past the early return; 1,255 "generator … judged" lines over 42 logs ⇒ ~8,900 hook calls per campaign | **6-7%** | exact (variant a), near-exact (variant b) | identical PoB output on `recover_tree` + one reference rebuild |
| 3 | Two PoB workers per build: the batch splits perfectly, but the machine is already saturated | `session.py:603-631` | `trial_stats` is exactly linear: N=1 → 5.65 ms/trial, N=400 → 5.60 ms/trial (zero fixed overhead) ⇒ a 2-way split is ~2× on 80% of the tree slice | **up to 25%** single-build; ~0% fleet | exact (same trials) | wall time of one reference with `--workers 1`, before/after |
| 4 | `max_depth=6` buys 40% more trials than `max_depth=4` | `tree_graph.py:177-195`; `tree_optimizer.py:268-272` | stormbrand 319 vs 228 trials, bleed_bow 380 vs 287, absolution 240 vs 177 | **12-14%** | approximate (changes the reachable set) | 3-seed medians; expect a DPS cost |
| 5 | `swap_subtrees` has no memory: the same subtrees are re-tried, and re-fail, on an identical tree every improvement-loop pass | `tree_optimizer.py:589-638` | stormbrand-s2: passes 1/2/3 each re-try the same three subtrees at 24-58 s per failed swap; 613 s over 4 passes, every pass reverted | **5-7%** | exact (fingerprint the allocated set) | same log, count re-tries → 0 |
| 6 | `refine` burns a 300-trial batch purely to rank the 80 it then evaluates properly | `tree_optimizer.py:412-440` | 300 add-only + 80 combined = 380 trials where 300 combined trials are cheaper *and* a better ranking | **~2%** | approximate (decision improves) | 3-seed medians |
| 7 | `_restore` reloads the whole build from XML where an inverse `mutate_nodes` would do | `tree_optimizer.py:161-177`; `session.py:156` vs `207` | `load_xml` 467-723 ms measured vs `mutate_nodes` 140 ms; 171 `load_xml` calls = 129 s in the profiled build | **1-3%** (stacks with #2) | exact only for tree-only moves | byte-compare `export_xml` before/after a restore |
| 8 | `FullDPS` in the objective doubles every tree trial | `session.py:603`; worker `_TRIAL_STATS_FAST_LUA:968,1018` | 200 trials: 6 keys 4.31 ms/trial, 6 keys + FullDPS 8.87 ms/trial (fixture 5.11 → 9.44) | 2× on minion references only | exact if FullDPS is present by accident | print `objective.stat_keys` per reference |
| 9 | `swap_subtrees` overruns its `max_seconds` by a whole candidate | `tree_optimizer.py:615` | log: `budget 120s` → passes take 126, 134, 144 s | <1% | exact | log |
| 10 | Negative result: lazy greedy on stale values is not available | `tree_optimizer.py:279-308` | of 4,477 same-path candidates only 25 (0.5%) kept their value; the winner sat outside the previous top-80 in 7/18 (stormbrand) and 6/18 (bleed_bow) steps | 0 | — | — |
| 11 | Negative result: Python, batching and serialisation are not the bottleneck | `tree_optimizer.py`, `tree_graph.py`, `objective.py` | whole tree slice in Python ≈ 11 s of 3,280 s (0.3%); 1 key vs 18 keys: 6.02 vs 4.63 ms/trial (noise) | 0 | — | — |

---

## Finding 1 — inert candidates are re-evaluated every step

`allocate` (`tree_optimizer.py:266-279`) rebuilds the whole trial batch from scratch on every step
and hands all ~270-400 of them to PoB; `refine` (`407-416`) does the same for its add batch. Nothing
remembers what PoB said last time.

I instrumented `_choose` to record every candidate's PoB value and violation at every greedy step of
a real `recover_tree` run (40 points stripped, 19 steps). On stormbrand, **74.2% of the 4,786
candidate evaluations returned a value *exactly* equal to the current build's** — the node and its
path change the DPS by literally nothing. 32.9% were fully inert: same DPS **and** same violation.
On bleed_bow the numbers are 89.6% and 57.2% (a bow build carries far more dead spell/minion/aura
nodes in reach).

A rule "once a candidate has come back inert, stop sending it" would have skipped 29.9% of all
evaluations on stormbrand and 53.3% on bleed_bow. I checked every skipped evaluation against what
PoB actually returned: 1.05% / 1.41% of the skipped ones had become live, **and every one of them
was a violation-only change** — a `+Life` or `+resist` node that became relevant the moment a floor
broke at step 13. The chosen candidate was never among the skipped ones in either run. So the
invalidation rule is not a timer: re-admit the whole skipped set whenever the set of missed
constraints changes (`Objective.violations(stats).keys()` differs from the last step), and on any
event that changes the build outside the tree (gear swap, config lane change, a keystone or a new
damage type taken). With that rule both runs are error-free.

This is the biggest single lever in the slice: trials are 80% of the post-fix tree slice and 50% of
the build, and this removes a third to a half of them. It is approximate — a node can in principle
go from inert to live through an interaction that leaves the constraint set untouched (a keystone
changing a conversion, a mastery unlocking a tag) — which is why the constraint-set trigger must be
paired with a full refresh every M steps (M = 10 costs back only 3-5% of the saving) and why it must
be judged on 3-seed medians of the two most sensitive references before the full core14 run.

Note the trap: a *DPS-only* filter is wrong. 74% of evaluations are zero-DPS but only 33% are inert
— the 41% difference is exactly the repair candidates the greedy needs while a floor is missed, and
in the instrumented run **0 of 19 steps started from a feasible state**. In the real benchmark 25%
of the 381 logged steps start feasible (`stormbrand-s2.log`), and in a feasible state `_choose`
(`tree_optimizer.py:685-691`) can only pick a positive-gain candidate, so during those steps the
zero-DPS group can be dropped wholesale for a further ~18% of all evaluations.

## Finding 2 — the enabler hook

`allocate` calls `self.enabler_hook` for every candidate whose text generates charges
(`tree_optimizer.py:293-307`), memoising the answer in `hooked` — a dict **local to one `allocate()`
call** (line 264), additionally cleared whenever a generator node is applied (line 328). `allocate`
is called 35 times in one build (25 of them from `swap_subtrees`), so the same nodes are re-judged
over and over.

The hook is `pipeline._value_with_enabled` (`pipeline.py:597`). Per call it does
`config_inputs` + `export_xml` + `mutate_nodes` + `derive_config` + (sometimes) `set_config` +
`stats`, and always `load_xml(snapshot)` in a `finally`. Profile: **127 calls, 388.2 s** —
`derive_config` 249.7 s, `load_xml` 94.8 s, `_apply_config` 18.0 s, `mutate_nodes` 16.4 s,
`config_inputs` 4.9 s, `export_xml` 4.2 s. **Only 18 of the 127 calls got past the early return**;
the other 109 paid ~2.9 s each — 315 s — to learn that allocating the node flips no charge toggle.
That is 11.8% of the profiled build and 24% of its tree slice; the campaign's 42 logs carry 1,255
"generator … judged with" lines, which at the same 14% hit rate implies ~8,900 hook calls.

The `read_state` fix already takes ~240 s off this (almost all of `derive_config` was
`read_state` via `config_rules.build_text`), leaving ~148 s ≈ 6.8% of a post-fix build. Two fixes:

- **(a) exact.** The early return only asks "does some `use<Kind>Charges` go from not-True to True".
  `generator_effects` (`tree_optimizer.py:214-230`) already knows the node's text generates charges;
  it just does not record *which* kind. If it did, the hook can be skipped without touching PoB
  whenever every kind the node generates already has its toggle on — which is the common case late
  in a build, precisely where `allocate` is called most often.
- **(b) near-exact.** Hoist `hooked` from a local to an optimizer attribute keyed by a config
  generation counter bumped by `after_apply_hook` and by any `set_config`. Exact whenever the lanes
  and the gear have not moved; that covers all 25 `allocate` calls inside one `swap_subtrees` pass.

Proof is cheap and does not need a benchmark: the same run must produce byte-identical PoB output
and the same kept steps, with the hook call count down.

## Finding 3 — two workers, and why the batch itself is already optimal

`trial_stats` is exactly linear in the batch size, with no measurable fixed cost: 200 trials one at
a time cost 5.65 ms each; 400 in one batch cost 5.60 ms each (`probe_batch_out.txt`). Key count does
not matter (1 key 6.02 ms/trial, 18 keys 4.63 ms/trial — noise), so neither the two Python JSON hops
nor the two pure-Lua `dkjson` passes inside the worker are visible; the whole 5 ms is
`calcFunc` (`headless_runtime_worker.py:1018`). Consequences: nothing is to be gained by changing
the batch size, trimming the `"mastery": {}` / `"item": null` fields, or shrinking `stat_keys`.

The same linearity means a 2-way split is close to a perfect 2×. State sync for the tree stages is
mechanically simple: they only ever change the build through `mutate_nodes`, `load_xml` and
`set_config`, so a mirror session replaying the same three calls stays bit-identical, and the split
batch needs no ordering guarantee (each trial restores the build itself). That is up to 40% off the
tree slice, ~25% off a build.

The catch is the machine, not the code. This is a 6-core i5-12400F and the campaign runs
`benchmark.py --workers 5`, i.e. 5 PoB processes at ~1.1 GB each already. A second worker per build
doubles the process count and trades fleet throughput for single-build latency roughly 1:1. Worth
doing for the single-build workflows (`recover_tree`, one skeleton, the smoke pair) or paired with
dropping campaign parallelism to 3; not worth doing inside a 5-wide campaign.

## Finding 4 — search depth

`max_depth=6` (`pipeline.py:112`) reaches every notable, keystone and mastery within six points.
Measured on three finished reference trees, trials per step: stormbrand 319 (depth 6) vs 228
(depth 4), bleed_bow 380 vs 287, absolution_minions 240 vs 177 — 26-40% more trials for the nodes at
distance 5-6. This is the cheapest single knob in the file and the most dangerous: it is exactly the
"re-path to a distant payoff notable" ability the greedy was given depth for. If tried, try it as
depth 6 on the first N steps and depth 4 afterwards, and judge on 3-seed medians.

## Finding 5 — `swap_subtrees` and `refine` repeat rejected work across passes

`swap_subtrees` enumerates every hanging subtree ≤ `max_size`, ranks them in one trial batch
(`tree_optimizer.py:601` — correctly one round trip), then for each one removes it, re-runs the full
greedy `allocate` over the freed points, and either keeps or `_restore`s. Nothing is remembered
between calls.

In `stormbrand-s2.log` the improvement loop runs the pass once per loop pass and the pipeline reverts
the whole pass each time (`judge` at `pipeline.py:375-397` re-derives the lanes and the pass loses),
so pass N+1 starts from *exactly* the tree of pass N — and re-tries the same subtrees:
`-4 [Elemental Damage]`, `-8 [Intelligence, Mental Rapidity, Caster Mastery, Cast Speed, Cast Speed]`
and `-4 [Lightning Damage, Storm Weaver, Intelligence, Cold and Lightning Damage]` fail in pass 1, 2
and 3, at 24-58 s per failed swap. Path swaps cost 613 s over 4 passes in that one build; three
quarters of it re-derives a known answer. A memo of `(fingerprint(allocated set), frozenset(subtree))
→ rejected` is exact.

`refine` has a smaller version of the same problem: its leaf-removal batch (`:398`) and add batch
(`:416`) are rebuilt every round though only one swap changed between rounds, and a `refine` call
that keeps nothing still pays a full round. In the same log `loop pass N tree refine` kept nothing in
passes 1, 2 and 3 (identical before/after values) at 27-28 s each.

`reoptimize` I checked for duplicate ruin draws: the pipeline seeds it `seed + 7919*p + d`
(`pipeline.py:492`), so the draws are distinct. Its cost is the nested `allocate` (229.8 s of its
332.4 s) and the nested `refine` (98.9 s), plus a second full `refine` when the recreate left the
build infeasible but higher (`tree_optimizer.py:548-552`). Findings 1, 2 and 4 all apply to it
transitively — it is not a separate target.

## Finding 6 — `refine`'s ranking batch

`refine` evaluates up to 300 add-only trials (`:416`) whose values are used only to sort candidates
by `_rank_key`, then re-evaluates the top 80 with the removals attached (`:440`). That is 380 trials
where 300 combined trials would be both fewer and a strictly better ranking: the removal set is
determined up front (the cheapest leaves by the batch-1 ordering, minus any leaf on the candidate's
own path, `:431`), so the combined trial can be built for all 300 candidates without the pre-pass.
21% of refine's add/swap trials, and the decision improves rather than degrades.

## Finding 7 — `_restore` cost, and what is *not* worth touching

Measured primitives on a finished build: `export_xml` 9-11 ms, `load_xml` **467-723 ms**,
`mutate_nodes` ~140 ms, `stats()` on a clean build 0.2 ms, on a dirty build ~130-150 ms,
`tree_light()` 0.3 ms, `read_state()` 2.4 ms. `_restore` is therefore ~0.6-0.8 s a time; the
profiled build made 28 of them (22 s) plus the hook's 127 (95 s). For a move that changed only tree
nodes and mastery selections, `mutate_nodes(add=old−new, remove=new−old)` is 4-5× cheaper and exact;
`load_xml` must stay wherever `after_apply_hook` may have rewritten the config.

Two things I checked and would leave alone:

- **`current_score()` after every apply** (`tree_optimizer.py:329`) looks like a wasted round trip,
  but the next trial batch opens with `if build.buildFlag then runCallback('OnFrame') end`
  (`headless_runtime_worker.py:964`) and would pay the same recalc. Removing it saves one IPC hop,
  not the ~150 ms.
- **`mutate_nodes` at 140 ms** is `spec:BuildAllDependsAndPaths()` plus `itemsTab:UpdateSockets()`
  (`headless_runtime_worker.py:1154-1155`). The path rebuild is required — the next batch reads
  `node.path`. At ~423 applies per build it is 1.8% and not the place to look.

## Finding 11 — the Python side, measured, is 0.3%

The brief's premise was ~4 ms of non-PoB time per candidate. It is not there. In the fresh
`recover_tree` profile `allocate` spends 12.84 s of 15.48 s in `trial_stats` (83%), 1.13 s in
`mutate_nodes` and 1.47 s in the real recalcs; **Python totals 0.05 s — 0.3%**. Across the whole
3,280 s build: `graph.candidates` 261 calls / 1.34 s, `_trials_for` 261 calls / 0.55 s,
`objective.score` 83,669 calls / 7.7 s, `_choose` 0.92 s, `_rank_key` 0.03 s, `summary()` (rebuilt in
full on every step, O(n²)) 0.016 s. Eleven seconds, all told. The `_readline_with_timeout` thread
spawned per worker call (`headless_runtime_adapter.py:110-128`, 5,554 threads in one build) costs
1.1 s. None of it is worth a line of code.

What a logged step's seconds actually contain is *per-step*, not per-candidate: one trial batch
(N × ~5 ms) + `mutate_nodes` (140 ms) + one real recalc (~150 ms), plus — on an `allocate` step that
touches a generator — the enabler hook at ~3 s.

## One number I could not close

Re-measuring `refine` today on the very build the log came from (`stormbrand-s2.pob.txt`, 6-key
objective, campaign running alongside) gives **6.0-7.7 ms per counted candidate**, 83% of it inside
`trial_stats` at 5-7 ms/trial. The same build's benchmark log shows a **median of 22.5 ms** per
counted candidate for `refine` steps and 24.2 ms (p90 100 ms, max 165 ms) for `allocate` steps; over
all 42 logs, 4.33 M candidate evaluations in 119,126 s = 27.5 ms each. The `allocate` spread is
explained by the enabler hook (finding 2). The residual ~3× on `refine` is not, and I could not
reproduce it: batch size, key count, build complexity, socket-group count and `FullDPS` were all
tested and none of them accounts for it. The most likely remaining cause is contention during the
5-worker campaign on 6 physical cores. It is worth settling before sizing any of the savings above,
and it is cheap to settle: rebuild one reference with `--workers 1` and compare the `[N cands, Xs]`
lines against the same reference in the core14 run. If the gap is contention, finding 3's conclusion
(do not add a second worker inside a 5-wide campaign; consider *reducing* campaign width) becomes the
largest lever in this audit, ahead of everything in the table.

## Suggested order

1. Finding 2 (exact, cheap to prove, no benchmark needed) — ~6-7%.
2. Finding 5 (exact, log-provable) — ~5-7%.
3. Settle the contention question above (one run) — decides finding 3 and re-sizes everything.
4. Finding 1 (approximate, biggest) behind a 3-seed smoke on the two most sensitive references — 15-26%.
5. Findings 6 and 7 — ~3-5% together.
6. Finding 4 last, only if the target is still short; it is the one that trades DPS for time.

Findings 2 + 5 + 1 together are ~30% of a build with no change to the search's shape; adding 4 takes
it to ~42%. A several-fold cut needs finding 3 (or fewer, wider builds) on top of them.
