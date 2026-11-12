# Jev (TypeSafe AI's "System One" model): the lead's verdict (2026-09-20)

Report read in full: `inbox/2026-09-20-astra-jev.md` (38 KB, 21 web sources + the repository; nothing was spent or
run). Checked by the lead in the repository: the report's one finding about OUR code is true --
`scripts/build_scaling_vectors.py:129` keeps only the first 50 providers of a stat (`provided.get(stat, [])[:50]`), in
source order, so for Str / Dex / Int the list is all uniques and no tree node ever reaches it.

## What Jev is (their own docs)

Three question types over a text "state": yes-probability, a choice among <= 255 options with the full distribution,
a score over 2-10 described levels. $42 per billion input tokens, output free, 64k context, no fine-tuning ("the same
weights serve every account"), "designed for consistency", not determinism (their own repeat test: 90.8% raw
agreement). Their own list of weaknesses: "Jev is not a calculator", unreliable at math and counting, degraded by
irrelevant context, cannot keep invariants between separate questions. Calibration evidence: no reliability diagram
from the vendor; one independent 108-claim grounding test (accuracy 96.3%, ECE 0.066 -- the two cheap chat models it
was compared with had ECE 0.061 and 0.067). Nothing on any game's text. $5 buys ~119,000 calls of 1,000 tokens.

## Verdict by candidate

| candidate | verdict | why |
|---|---|---|
| package proposals ("far sight") | NO | PoB answers a package exactly in 7 ms; the space after a stat graph is small: 88 consumer uniques x 374 notable groups = 32,912 pairs = ~230 s of PoB trials; "not a calculator" |
| mechanics text triage | not now | the worst error of the project is a false "proven"; no evidence on PoE text; at most a review ROUTER after a 500-line labelled test with zero false-proven in the confident lane |
| worker / log triage | maybe later | cheap, reversible, rules stay the authority; only for rows the rules cannot decide |
| request intake, screen ordering, finished-build audit | NO | the schema + corpus validation, a model on our own `evaluations.jsonl`, and PoB deltas do these better |

## What we take from the report

1. Fix the stat graph FIRST (`scaling_vectors.json`: 477 vectors exist; the provider lists are truncated to 50 in
   source order): keep every provider, grouped by family (tree node / mastery / unique / support / gear line). This is
   the base of the "unique packages" spec (ROADMAP State 07:00).
2. Size of the package search, for that spec: item x notable group is exhaustive-able (~230 s, cacheable per
   skeleton); item x PAIRS of groups is 6.1 M = ~12 h and needs the stat graph's filtering.
3. Nothing is integrated. A log-triage pilot only if the regex rules start costing the lead's time again.
