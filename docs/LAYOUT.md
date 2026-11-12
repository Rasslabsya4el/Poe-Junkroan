# Layout and commands

## Layout

```
src/junkroan/pob/         Headless PoB runtime + game-data corpora (tag_corpus, mod_corpus, game_corpus).
                          Entry point for new code: session.py (PobSession). Stable; no gates or ledgers.
src/junkroan/optimizer/   Tree graph, Objective, TreeOptimizer (greedy + swap, PoB in the loop), gear fillers,
                          config rules, the improvement loop; pipeline.py turns a Skeleton into a build.
src/junkroan/search/      Skeleton model, request, candidate generation, screen and finalists, Pareto ranking.
src/junkroan/mechanics/   Hand-maintained non-PoB facts, JSON, small.
src/junkroan/cli.py       `junkroan build` (the request entry point).
scripts/                  Runnable entry points: smoke, fixture stats, build-from-skeleton, search, benchmark,
                          replay bench, audits, probes of past tickets.
tests/                    pytest. Fast tests need no PoB; tests that need the runtime carry the mark `pob` and
                          skip when the runtime is missing.
tests/fixtures/           Reference builds (Tuadh 3.29 day-1 snapshots, Zizaran / Maxroll starters) + stats.json.
schemas/pob/              JSON schemas of the corpora and the PoB lock.
locks/pob.lock.json       Pinned PoB release (v2.67.2, PoE 3.29); locks/pob.source.lock.json pins its Lua source.
vendor/pob/source/        PoB Lua data files used to regenerate corpora (fetched by the pin, not committed).
var/                      The runtime and caches (not committed).
artifacts/                Run output (not committed).
docs/                     STATE (what runs now), ARCHITECTURE, LAYOUT, TESTING, POBSESSION, RAILS, REQUEST,
                          HYPOTHESES, BUILD_STEPS; adr/ (decisions D1..), specs/, research/, readings/, rulebook/,
                          agents/ (issue tracker, labels, domain docs).
GLOSSARY.md               The project's vocabulary.
```

## Commands

```bash
python -m pytest -q -m "not slow"   # unit + contract tests, no PoB
python scripts/smoke_pob.py         # boots PoB headless, builds a Fireball Witch, prints stats
python scripts/fixture_stats.py     # loads every reference build, prints/records its stats
python scripts/build_from_skeleton.py --from-fixture stormbrand --author-floors   # rebuild a reference from its skeleton
python scripts/search.py Fireball --ascendancies Elementalist,Inquisitor --top 2  # search (docs/HYPOTHESES.md for LLM input)
python scripts/junkroan.py build --skill "Storm Brand" --mode hit --ascendancy Hierophant,Inquisitor --level 80   # request -> search (docs/REQUEST.md)
python scripts/audit_build.py "artifacts/search-fireball/<YYYYMMDD-HHMM>/*.pob.txt"       # machine audit of finished builds (D31)
python scripts/describe_build.py "artifacts/search-fireball/<YYYYMMDD-HHMM>/01 *.pob.txt"  # read a build like a person
```

`junkroan build` is the same as `scripts/junkroan.py build` once `pip install -e .` has run; `--dry-run` echoes the
request only, `--no-variants` is the cheapest run. Anything past a quick local check (a search, a benchmark, a
bench) runs as a heavy run (`CLAUDE.md`, "Heavy runs"; `docs/ci.md`).

Every search run writes its ranked set (`NN *.pob.txt`, `.json`, `report.md`) into its own dated folder
`artifacts/search-<skill>/<YYYYMMDD-HHMM>/`; a later run deletes nothing of it. The skill root keeps one `report.md`,
the latest run's, whose first line names the folder (`Latest run: <path>`). The request echo prints the folder
(`results: <path>`).

The day-1 gear flag is `--gear` of `scripts/benchmark.py`: `template` is the value and the default; `wishlist` is its
alias and stays as the module and pipeline mode name.

If `var/cache/pob/<tag>/app` is missing, `PobSession` downloads the pinned release via `release_manager.py`
(~630 MB) on first use.

## Bumping PoB

`python -m junkroan.pob.release_manager pob pin --version vX.Y.Z`, re-clone `vendor/pob/source` at that tag, update
`locks/pob.source.lock.json`, run the three corpus `build` CLIs, run `scripts/fixture_stats.py`, run the tests. The
worker's Lua strings call PoB internals (`ImportFromNodeList`, tab APIs); a bump can change signatures. Fix them in
`headless_runtime_worker.py`. A bump changes recorded numbers, so its fixture stats and benches run as heavy runs.

## The objective metric

`CombinedDPS` per instance, and `FullDPS` only for main skills whose instance count is a PoB stat (minions and
totems today, brands next; D57). Elsewhere `FullDPS` is only populated for socket groups flagged "include in full
DPS" and is 0 on many imported builds.
