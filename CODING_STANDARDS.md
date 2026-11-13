# Coding standards

What the `checker` reads, and what every change is written against. One rule per line, each ending with its source
in parentheses.

## 1. General

- The code carries no ledgers, proof surfaces, waivers, blocker taxonomies or publication gates: a function returns a result or raises. (CLAUDE.md, principle 6)
- Validation is a test that measures the outcome, here a test that measures build strength, never a schema check. (CLAUDE.md, principle 6)
- No parallel registry of tasks or decisions beside GitHub issues, `GLOSSARY.md` and `docs/adr/`. (CLAUDE.md, "Agent skills")
- A decision becomes an ADR only when it is hard to reverse, surprising and a real trade-off; the rest lives in the commit message or PR with its numbers. (docs/agents/domain.md)
- A new ADR takes the highest number in `docs/adr/` plus one; an amendment lives inside its ADR; ADR numbers are never reused: 0117 and 0118 were process decisions of the archive and stay unused here. (docs/agents/domain.md)
- Human-facing text writes a duration in a unit a human reads: seconds only under ~90 s, then minutes, then hours and minutes past ~90 min; machine files keep raw seconds. (CLAUDE.md, principle 7)
- A rate is quoted per minute, never per 100 s. (CLAUDE.md, principle 7)
- A red suite is never merged around: fix the code, or the data the failing tests read. (CLAUDE.md, "How work is split")
- A test that judges built data judges data built from the code being merged, never stale data left in a checkout. (docs/TESTING.md)
- A domain term in code, tests or a report uses the word `GLOSSARY.md` defines. (docs/agents/domain.md)

## 2. Product

"PoB" is Path of Building, the numeric oracle.

- PoB is the only judge of strength: no prose reasoning about strength, no hand-written scaling weights, no "this should be good". (CLAUDE.md, principle 1)
- The LLM never picks passive nodes, item affixes or config toggles; those are optimizer decisions. (CLAUDE.md, principle 2)
- When candidates are needed (uniques, notables, supports that touch a damage type), query the corpora in `src/junkroan/pob/` (`tag_corpus`, `mod_corpus`, `game_corpus`); game content is never enumerated from model memory. (CLAUDE.md, principle 3)
- "What does X scale with" comes from PoB's parsed mod data and from measured PoB deltas, not from curated prose. (CLAUDE.md, principle 4)
- The only hand-maintained knowledge is `src/junkroan/mechanics/` (facts PoB cannot compute), kept small and machine-readable; if PoB computes it, it does not belong there. (CLAUDE.md, principle 4)
- Every stat, output, config var, mod line, item, base, skill, keystone, mechanic and floor keeps its exact PoB / in-game English name, never translated. (CLAUDE.md, principle 8)
- Every duration a script renders goes through `junkroan.report_format.human_duration`. (CLAUDE.md, principle 7; src/junkroan/report_format.py)
- The objective metric is `CombinedDPS` per instance, `FullDPS` only for main skills whose instance count is a PoB stat. (docs/LAYOUT.md; D57)
- A Flask slot is `active` only when it reads "Flask uptime: 100%"; the flag is derived by the PoB worker on every evaluation and never set by hand. (GLOSSARY.md, "Flask uptime"; D115)

## 3. Code shape

- Write the measurement first: which PoB metric proves the change, on which build. (docs/TESTING.md)
- Keep modules small and pure; `PobSession` is the only stateful thing. (docs/ARCHITECTURE.md)
- One calc is ~0.1 s: budget thousands per skeleton and prefer incremental mutations to a full re-apply. (docs/ARCHITECTURE.md)
- When a task needs game knowledge, write a corpus query, not a paragraph. (CLAUDE.md, principle 3)
- `src/junkroan/pob/` is stable: a feature lands there only through a ticket about the harness, and never as a gate or a ledger. (docs/LAYOUT.md)
- v1 concepts (rails reports, decision ledgers, proof packets, skill passports) are not resurrected. (D1)
- Every new kind of error becomes an audit check and a general rule, never a patch for one build. (GLOSSARY.md, "Reading"; D31)
- Every search run writes its ranked set into its own dated folder `artifacts/search-<skill>/<YYYYMMDD-HHMM>/`; a later run deletes nothing of it. (docs/LAYOUT.md)
- Fast tests need no PoB; a test that opens a PobSession or the PoB runtime carries the mark `pob` and skips when the runtime is missing. (docs/LAYOUT.md; pytest.ini)

## 4. The test of a change's kind

Decide the kind before choosing the test (CLAUDE.md principle 6, `docs/TESTING.md`, D113).

- A change that is kind A (search space) but also touches selection, loop control, evaluation values or termination is kind B. (docs/TESTING.md, section 1)
- Kind A: rail tests plus the trace counter at the PoB boundary, `generated(x) > 0 and evaluated(x) > 0` or `evaluated(forbidden) = 0`; never a before/after set run or a metric gain. (docs/TESTING.md, section 2; D113)
- Kind B: a test that encodes the defect plus the replay bench (`replay_bench.py --move <m>`) on the smoke six; a paired set run only when the bench alerts or the whole loop changes. (docs/TESTING.md, section 2; D84)
- Kind C (refactor): an identical PoB call transcript, base against head (`--record-calls`, `compare_calls.py`), finals equal to the digit; any difference makes the change A or B. (docs/TESTING.md, section 2; D95)
- Kind D (speed only): the suite, the same transcript and interleaved base/head timings; no quality claim. (docs/TESTING.md, section 2)
- Kind none (no optimizer code): the suite and no PoB run. (docs/TESTING.md, section 2)
- Whether overall quality moved is answered only by the weekly core run; no ticket is judged by it. (docs/TESTING.md, section 4)
- The PR names the kind and shows its numbers (A move x class counts, B paired table, C "identical, N calls, finals equal", D timings, none the suite line). (docs/TESTING.md, section 3)

## 5. Runs

- Locally only quick, targeted tests: under a minute, one process. (CLAUDE.md, "Heavy runs")
- Every longer PoB run (a bench, a benchmark, a search, a re-record, the full suite) goes through `python .github/scripts/heavy_dispatch.py`; nobody polls a run inside a turn. (CLAUDE.md, "Heavy runs"; docs/ci.md)
- Worktrees live in `.claude/worktrees/`, scratch files and run output in `.claude/scratch/` or `artifacts/`; nothing of this repo is written outside its folder. (CLAUDE.md, "How work is split")
