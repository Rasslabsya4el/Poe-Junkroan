# Poe Junkroan

Machine search for Path of Exile builds. Path of Building (PoB) is the numeric oracle; scripts optimize; the LLM
only proposes hypotheses and explains results.

Read what the task needs: `GLOSSARY.md` (the vocabulary), `docs/STATE.md` (what runs now), `docs/ARCHITECTURE.md`,
`docs/LAYOUT.md` (layout, commands, bumping PoB, the objective metric), `docs/TESTING.md` (which test a change
gets), `docs/POBSESSION.md` (PobSession cheat sheet, harness limits), `docs/RAILS.md` (rails worth remembering),
`docs/ci.md` (CI and heavy runs).

## What this project is

The owner asks for a build ("Fireball", "something around item X", "bow poison"). The system searches over build
*skeletons* (class, ascendancy, main skill, damage mode, supports, keystones, key uniques, auras), and for each
skeleton runs a deterministic optimizer over passive tree, rare gear and config with PoB in the loop. Output is a
ranked Pareto set of PoB import codes with an explanation of why each build is shaped the way it is. The goal is
strong non-meta builds a human would not assemble by hand, not a copy of poe.ninja.

## Principles

1. **PoB is the only judge of strength.** A change to a build is good if PoB's numbers say so under the objective
   function. No prose reasoning about strength, no hand-written scaling weights, no "this should be good".
2. **The LLM never picks passive nodes, item affixes or config toggles.** Those are optimizer decisions. The LLM
   proposes skeleton hypotheses, writes search space definitions, and explains results.
3. **Retrieval over recall.** When candidates are needed (uniques, notables, supports that touch a damage type),
   query the corpora in `src/junkroan/pob/` (`tag_corpus`, `mod_corpus`, `game_corpus`). Game content is read from
   them, never enumerated from model memory.
4. **Interpretations are derived, not authored.** "What does X scale with" comes from PoB's parsed mod data and
   from measured PoB deltas, not from curated prose. The only hand-maintained knowledge is
   `src/junkroan/mechanics/` (facts PoB cannot compute, e.g. corpse supply, overlap breakpoints), kept small and
   machine-readable.
6. **Every optimizer change is proven by the test of its kind, with numbers** (D113, `docs/TESTING.md`). A
   search-space rule by rail tests and the trace counter at the PoB boundary (`generated(x) > 0 and
   evaluated(x) > 0`, or `evaluated(forbidden) = 0`), never by a metric gain; a loop or evaluation fix by a
   bug-specific test plus D84's replay bench on the builds where the defect reproduces; a refactor by an identical
   PoB call transcript (D95). Whether overall quality moved is answered only by the weekly core run. The PR names
   the kind and shows its numbers. A proof run longer than a quick test is a heavy run (section "Heavy runs").
7. **Durations for a human.** Seconds only under ~90 s, then minutes, then hours and minutes past ~90 min; never a
   bare count of seconds in the hundreds or thousands, never a rate per 100 s. Machine files (JSON, logs) keep raw
   seconds; whoever quotes them converts. Every script renders a duration through
   `junkroan.report_format.human_duration`.
8. **Game and PoB terms are written exactly as PoB writes them, never translated.** Messages to the owner are in
   Russian, but every stat, output, config var, mod line, item, base, skill, keystone, mechanic and floor keeps its
   exact PoB / in-game English name: `PhysicalMaximumHitTaken`, `EffectiveMovementSpeedMod`, `Life`,
   `CombinedDPS`, "+% increased Spell Damage", Two-Stone Ring, Mind over Matter. Player slang in Cyrillic (лайф,
   резы) is fine; a Russian translation of a game term is not.

(Principle 5 of the numbering is retired; the numbers stay because code and ADRs cite them.)

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `Rasslabsya4el/Poe-Junkroan` (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

A `#N` in code, tests or docs written before 2026-11-12 names an issue of the private archive
`Rasslabsya4el/Poe-Junkroan-archive`, where this repo's history and old tickets stay; this repo's own issues start at #1.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root; `D<n>` anywhere in the repo is ADR `<nnnn>`. See
`docs/agents/domain.md`.

## How work is split

One chat does one task, start to end: an idea and its tickets, or one ticket, which it reads, codes, tests, opens as
a PR and lands itself. That chat is "the main chat" in this file and in `docs/ci.md`. Its code is not cut into
pieces for coder helpers, and no coders run in parallel: what an agent pays for is mostly reading, and a coder
helper would read again the code the chat already read to brief it. Two helpers in `.claude/agents/`:

- `finder` (Haiku 5.5): wide reading and search; the chat keeps only its facts with `file:line`. Used instead of
  the built-in Explore agent.
- `checker` (Sonnet 5.5): one review of a change against its ticket and `CODING_STANDARDS.md` before it lands.

A helper prompt names its ticket (`#N`) and the files, branch or worktree.

Model: every chat runs on Opus 5.5 with effort medium; the helpers keep their own models.

Landing a ticket: review comes before the expensive part. Once the code and its quick tests pass, the main chat
starts the `checker` on its branch and checks the fix round from its diff (a new mechanism in it goes to the
`checker` again). Only then do the heavy runs (proof runs, re-recorded numbers) run; a code change after them runs
them again. The main chat opens the PR with `Closes #N` and merges it itself once CI is green (Ubuntu), the
`checker` has passed it, the main chat has checked its numbers from the diff, and its tests cover the ticket's
"Done when"; then it runs `git pull --ff-only` in the main folder. Nobody asks the owner about merging. A PR's open
points (findings, placeholders) are filed as issues before it lands, never left in its prose. The check and the
list: `docs/ci.md`.

One task per chat. The state of the work lives in the GitHub issues, so a `/clear` between tasks loses nothing.

Everything this repo needs lives inside this folder: worktrees in `.claude/worktrees/`, scratch files and run
output in `.claude/scratch/`. The main folder stays on the branch `main`, because every new chat reads this file and
`.claude/agents/` from it: a chat reads another branch with `git show` or works in a worktree.

## Heavy runs

Locally only quick, targeted tests (under a minute, one process). The full suite, benches, benchmarks, searches and
re-records go to GitHub: CI, or a heavy run. Heavy runs go **only through the dispatcher**:
`python .github/scripts/heavy_dispatch.py run --ref <branch> --command '...'` (its flags, limits and `status`:
`docs/ci.md`). Long PoB runs land on the dedicated Linux runner once it joins.

Nobody polls a GitHub run inside a turn. The main chat dispatches with `--no-wait` and waits in the background
(`docs/ci.md`). A helper (`finder`, `checker`) starts no heavy run.

## Talking to the owner

The owner is the product owner, not a developer: he decides what he wants and what he accepts, and he comes in cold
between chats. Every reply to him:

- is in Russian, game and PoB terms in English as PoB writes them (principle 8); the first line answers what he
  asked or gives the result;
- says in plain words what physically happens: a path, a function name, a commit id becomes what it does;
- asks only what only he knows (what he wants, his taste, the time and risk he accepts), each question standing
  alone: the context, the options with their consequences, your recommendation; the rest you decide and say in one
  line with its reason;
- names what showed a thing is done: the test, the command, the numbers;
- writes durations for a human (principle 7);
- past three lines, ends with a short **TLDR**: what happened and what needs his answer.

He does no step you can do yourself: a command, a commit, a file edit, a merge.

**Readings.** The owner judges finished builds by reading them in PoB (a Reading, `GLOSSARY.md`). A reading request
is a plain dark page: one row per build with an Open PoB button (its pobb.in link) and one line of what to look at.
Nothing more on it.
