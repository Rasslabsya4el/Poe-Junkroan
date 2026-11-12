# Deep-research brief: is there a place for a "System One" decision model (TypeSafe AI's Jev) in this project?

You have read access to the repository `poe-junkroan-v2`. You have no other context: everything you need is below or in
the files named. Label every statement [SOURCE] (you opened the page / file; give URL or path and a short verbatim
quote), [DERIVED] (your arithmetic or reasoning from sourced facts) or [UNVERIFIED]. "Not found" beats a guess. Write
the report to `docs/research/inbox/2026-09-20-astra-jev.md` (or return it as a file).

## The project in one paragraph

A machine search for Path of Exile builds. Path of Building (PoB, run headless) is the ONLY judge of strength: one
what-if calculation costs 7 ms, a full calculation 0.1-0.2 s, a finished build ~38 minutes of optimizer time
(construction, then an improvement loop over passive tree, rare gear, gem links and a derived config). Hard rules
(`CLAUDE.md`, "Non-negotiable principles"): no language model ever picks passive nodes, item affixes or config toggles;
no prose reasoning about strength; game facts PoB does not compute are stored as sourced facts, never typed from a
model's memory. Language models are used ONLY around the numeric core: a lead model writes specs and verdicts, code
workers write code, agents turn logs into tables. Read: `CLAUDE.md`, `docs/ARCHITECTURE.md`, the last ten entries of
`docs/DECISIONS.md` (D77-D87), `docs/ROADMAP.md` Phase 7 "State" (the newest entries), `docs/research/2026-09-19-*-plan.md`.

## The candidate: Jev (https://typesafe.ai; launched a few days before 2026-09-20)

What its own site claims (the lead read the home page once, 2026-09-20): "System One Models ... natively used by
machines"; "Send Jev structured questions and get typed decisions with probabilities and confidence that your software
can act on"; trained with "Reinforcement Learning for Calibrated Decisions (RLCD)"; "193.6x Faster, 444.6x Cheaper"
on its own workflow benchmark ("Cost $0.000081, Completed in 0.114s" against "$0.013880 ... 8.566s"); "$42 per billion
input tokens"; FAQ headings: "Is Jev just a smaller LLM?", "How is this different from JSON mode or structured
outputs?", "Is Jev deterministic?", "What is Jev good at? Where does it struggle?". The owner's constraint: nothing in
the pipeline may quietly eat money, and nothing may lower build quality.

## Part A -- what Jev actually is (primary sources only: their docs, blog posts, API reference, pricing, terms; any
## independent evaluation; say when only marketing exists)

1. The API: input format (free text? a schema of typed questions? context length), output types (boolean / enum /
   number / probability distribution?), what "confidence" is next to "probability", batch and latency limits, rate
   limits, determinism, SDKs usable from Python on Windows, data retention / training on customer data.
2. Evidence of CALIBRATION: reliability diagrams, ECE / Brier numbers, on which tasks and distributions; does
   calibration survive out-of-distribution, niche-domain inputs (a video game's item and skill text is exactly that)?
   What does the model know about niche domains at all -- is it a reader of the context you give it, or a store of
   world knowledge? Can it be fine-tuned or given few-shot examples, and at what price?
3. Their own "where does it struggle" answer, verbatim. Independent reports of failures.
4. Real prices (input, output, minimums, free tier), and what a million decisions of ~500 input tokens costs.

## Part B -- where it could fit HERE (judge each; add your own; kill the ones that do not survive)

The numeric core is closed to it by rule AND by arithmetic: PoB's what-if answers in 7 ms exactly, Jev in ~100-500 ms
approximately. So only TEXT-shaped or TRIAGE decisions are candidates:

1. **Mechanics text triage.** `src/junkroan/optimizer/config_rules.py` decides which config inputs a build has PROVEN
   (D77: "a buff is proven by a line PoB parses as its source"; amendment: "a buff ended by skill use proves nothing";
   D75: warcry rules; D80: a totem's / trap's / mine's hits are not the player's). Today: PoB's parsed mods + small
   hand-authored tables + the lead model reading wiki extracts. Could a calibrated classifier label mod / gem text into
   our taxonomy (condition kind: on kill / on hit / while stationary / on skill use / permanent; who benefits: player /
   proxy / minion) with a confidence, so that only low-confidence lines reach the expensive model or the user? What
   accuracy would be needed given that a wrong "proven" inflates a build's number (the worst error this project has)?
2. **Worker and log triage.** `scripts/gpt_worker.py` decides from a transcript tail whether a code worker finished
   with a report, stalled, or hit a provider outage (regex + markers today; see its tests). Agents turn benchmark logs
   into tables. Is a typed-decision model a better or cheaper judge of "what state is this log in" than rules?
3. **Request intake.** `docs/REQUEST.md`: a user's free-text request becomes typed fields (skill, damage mode,
   ascendancy limits, uniques to build around). Once per request, so cost is irrelevant either way: is there any gain?
4. **Pre-screen ordering.** A broad request screens 20-200 skeletons at 2-3 minutes each (the screen itself is the
   wall-clock bottleneck at 200). We already log every evaluation (`artifacts/search-*/evaluations.jsonl`). Compare
   three priors for ORDERING the screen: Jev reading the skeleton's text, a small model trained on our own rows
   (random forest), and no prior. Which is better on first principles, and what experiment would settle it?
5. **Audit of finished builds.** `src/junkroan/optimizer/audit.py` has machine checks; "a line no player would buy"
   is caught today by PoB deltas (a zero-delta line). Is there any check that is text-shaped and that PoB cannot see?
6. **Far sight: proposing PACKAGES (the owner's question).** PoB evaluates any package of changes exactly in ONE 7 ms
   what-if (an item + a set of tree nodes + a keystone; the fast what-if does not even require the nodes to be
   connected) -- what the system lacks is knowing WHICH packages to try: `SkeletonGenerator.screen_uniques`
   (`src/junkroan/search/generator.py`) tries every unique ALONE, so a build-around unique whose parts are worthless
   one by one (an attribute-stacking item + the nodes that feed it) is never found; the tree has the idea in small
   (`TreeOptimizer._cluster_trials`: notables that share a mechanic tag are tried as one trial). Candidate proposers:
   (a) a deterministic stat graph from PoB's own parsed mods ("per X" / threshold consumers on the item <-> sources of
   X on the tree, gems and gear; the corpora in `src/junkroan/pob/`), (b) exhaustive pair probes at 7 ms (item x
   notable cluster), (c) a large LLM's hypotheses once per request (`docs/HYPOTHESES.md`), (d) Jev asked "does this
   item pay off together with these nodes?". Judge (d) against (a)-(c) honestly: what would Jev have to KNOW about
   Path of Exile 3.29 to order such packages better than a stat graph, does it know it, and is a 100-500 ms approximate
   answer ever worth more than a 7 ms exact one? If the honest answer is "only as a prior over millions of packages
   that (a) cannot enumerate", say how large that space really is after (a)'s filtering.
7. Anything else you find in the repository that is a cheap, frequent, text-shaped decision with a checkable answer.

For each candidate: what the input and the typed output would be; how often it is called per build / per day and what
that costs at the real price; what it replaces and what that costs today (lead-model tokens, regex maintenance, wrong
verdicts); the failure mode and who catches it; the OFFLINE experiment that decides it, on data the repository
already holds (name the files: e.g. the 58 reference builds' conservative-lane verdicts as labels; worker transcripts
with known outcomes in `artifacts/runs/gpt-worker-*.out`; `evaluations.jsonl`), with the metric and the bar it must
clear (accuracy AND calibration: a threshold above which it never needs review, and the share of cases under it).

## Part C -- the verdict

A table: candidate | fits the project's rules yes/no | expected saving (tokens, minutes, or none) | risk to build
quality | experiment and its cost | recommendation (do / test / skip). Then three sentences: is Jev worth ONE
afternoon of integration for this project now, later (what would have to change), or never; and what would make you
change that verdict. Do not recommend anything that puts a language model between PoB and a build's number.
