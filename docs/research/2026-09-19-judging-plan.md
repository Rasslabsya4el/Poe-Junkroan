# Judging a change with few expensive runs: what the literature offers and what we take (the lead's reading, 2026-09-19)

Reports, read in full: `inbox/2026-09-19-chatgpt-judging-few-runs.md` (75 KB), `inbox/2026-09-19-astra-judging-few-runs.md`
(38 KB). Quotes checked by the lead against the primary pages, verbatim matches: Campelo & Takahashi, J. Heuristics 2020
("the effective sample size to be considered when testing the hypotheses of interest is the number of instances",
"can be modelled out of our analysis by pairing or blocking", "arbitrarily-set numbers of repeated runs, usually 30 or
50"). Not opened by the lead (paywall / bot check): Wright & Ramsay 1979, Glasserman & Yao 1992 (both reports agree on
them; nothing below rests on them alone). The two reports disagree on one source only: ChatGPT could not open Johnson
2002 and marks it unverified, Astra quotes it; we do not use it.

## Our own numbers

No new runs. Scripts: `scripts/2026-09-19-judging-noise.py`, `scripts/2026-09-19-anytime-traces.py`; inputs: the
`new18-rules` + `core14-rules` results.json, the frozen campaigns' table in `2026-09-18-seed-divergence.md`, the per-seed
tables of `2026-09-18-restarts-statistics.md` (the A/A pair: one code generation, seeds 1-3 and 7-9).

| question | number |
|---|---|
| noise of ONE build inside a reference (pooled over 32 references x 3 seeds, log space) | sd 0.140 = about 15% of the value |
| what best-of-3 adds over the median seed | median +10.7%, mean +11.7% |
| does the same seed carry over between code versions? (frozen vs rules, 96 pairs, residuals inside the reference) | r = +0.10, permutation band -0.28 .. +0.27; the best seed is the same seed on 14 of 32 references (chance 10.7): NO |
| smallest effect the smoke protocol can see (six references x 3 seeds, median of medians, 2 sd) | about 15% |
| the same for the full 32 x 3 | about 6% |
| A/A test: the SAME code, seeds 1-3 against seeds 7-9, smoke six | "median -2.0%", 4 of 6 references "worse", cold_dot -14.5%, bleed_bow -8.4% |
| a six-reference subset as an estimate of the 32-reference median change (frozen -> rules, a RULE change, so heterogeneous on purpose) | 90% band -30.7 .. +38.7 around the true -1.4; wrong sign for 44% of random subsets; our smoke six says -22.2 |
| 14 / 20 references instead of six | 90% band -18.7 .. +11.1 / -14.9 .. +3.1 |

## What both reports agree on, in our terms

1. Three seeds are an estimate, not evidence: with 3 paired observations the smallest exact two-sided p is 0.25; six are
   needed to reach 0.03. The unit of evidence is the REFERENCE, seeds only average the noise inside it.
2. Pairing removes what two runs share. Same seeds help only while the two trajectories stay correlated; ours do not
   (r = +0.10): the code branches at the first changed decision.
3. A "not worse on any smoke reference" rule lets one noisy reference veto a good change (our A/A: identical code fails
   it on cold_dot).
4. A small subset must be validated against the full set on past changes before it is trusted; random six-subsets have
   no guarantee (SPEC study: 4 chosen benchmarks reach tau 0.95, 14 random ones are needed for the same).
5. Partial runs may be used to drop obvious losers only after a replay on history shows a low false-kill rate.
6. Automatic tuning of ~30 knobs (irace, SMAC, ParamILS, BOHB) needs hundreds to thousands of evaluations; 100 full
   evaluations are 28 campaign-hours for us.

## What we take, in order

1. **The replay bench (the strongest pairing we have is the same STARTING BUILD, not the same seed).** A change to a
   move of the improvement loop (tree moves, gear re-rolls, picks, kicks) is judged by running that move from a fixed
   set of finished builds (the 96 delivered builds of the two rules campaigns + the smoke runs), before / after, same
   start, PoB the judge: gain, seconds, kept / reverted. Minutes per build instead of 38; noise only from the move's
   own randomness. The MIP experiment is already built this way. This is where the time is saved and where an effect
   of 2-5% becomes visible.
2. **Whole-pipeline campaigns become confirmation, not the daily judge.** Verdict = per-reference log ratio of medians,
   bootstrap interval over REFERENCES, win / loss counts, the worst reference named; a margin declared before the run
   (2 sd of the A/A noise: 15% smoke, 6% full). The smoke verdict is "no alarm / alarm", never "better".
3. **An A/A run is the yardstick**: whenever the protocol changes, run the same commit twice and report the fake
   difference next to the real one.
4. **Anytime traces, for the product only** (`junkroan build` delivers best-of-3): dropping the trailing seed after
   loop pass 1 costs 76% of the time of three seeds and loses 0.6% on average (worst 10%, nothing on 27 of 32);
   dropping two costs 49% and loses 3.2% (worst 29%). Campaigns keep all seeds: they measure. NOT before the tree
   plan's item C (union of seeds) is measured: there the three seeds are MATERIAL (alternative trunks that compete in
   one re-solve), not three lottery tickets, and a seed stopped at pass 1 brings a poorer tree to the union. The two
   are judged together: union of three full seeds / union of one full + two stopped / best-of-3 / early kill.
5. **Smoke set**: keep six for alarms; when three or more campaign pairs exist, choose the six by replay against the
   32 (906,192 subsets, no runs needed). Until then no claim from the smoke alone.

## How this fits the tree-search plan (`2026-09-19-tree-search-plan.md`)

- The replay bench is the tree plan's experiment A made general: A already judges one move (the whole-tree MIP) from
  six delivered builds with PoB as the judge. The bench is built FROM that worker's harness, not next to it.
- **The tree plan's step B changes its acceptance**: it was "accepted on the smoke six: value, seconds, seed spread,
  never-reconsidered share 22% -> below 5%, trunk churn". The structural numbers (never-reconsidered share, trunk
  churn, reverted moves and their seconds) are counts, not noisy values: they stay. "Value on the smoke six" cannot
  carry a verdict (it sees ~15%; identical code shows -14.5% on cold_dot): B's value is judged on the bench -- the new
  moves run from the 96 delivered builds, gain and seconds per build -- and the smoke run is only the alarm.
  The same holds for the judge fix in work now (`tree-moves-see-proof-holders`): its acceptance is the count of
  reverted path-swap moves and their seconds and Minion Life gone for good, NOT winter_orb's one-seed final value.
- The tree plan's reporting rule stands and is confirmed by both reports: all three seed values, never the best
  alone; "best-known", never "x% from optimal".
- The tree plan's optional yardstick (tiny instances with exhaustive search) is the only place a TRUE gap can be
  measured; nothing in these reports replaces it.

## What we do not take now

Automatic configurators (irace / SMAC / BOHB): unaffordable on whole builds (100 evaluations = 28 h, effects under 6%
invisible); they become realistic ON the replay bench (an evaluation = minutes), not before it. Sequential tests with
alpha spending: our n is too small for them to stop early; the margin + confirmation split does the same job.

## Tests that tell whether we need it

- Replay bench sanity: take two past changes whose campaign verdict we know (the judge fix once merged; D58's loop)
  and check the bench gives the same sign with a fraction of the machine time.
- A/A on the bench itself: same code twice -> the fake difference must be under 1%.
- For item 4: replay on the next finished campaign before switching it on in the product.
