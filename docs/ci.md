# CI and heavy runs on GitHub

The test suite and the long Path of Building (PoB) runs go through GitHub Actions, not through a developer's PC.
Everything runs on Linux; there is no Windows job anywhere.

| What | Workflow | Runs on | Started by |
|---|---|---|---|
| the suite without `slow` tests (`-m "not slow"`, `pob` tests included) | `.github/workflows/ci.yml` | `ubuntu-latest`, 8 jobs plus `CI summary` | every push to a pull request; `workflow_dispatch` for `main` or any branch |
| a heavy run: `slow` tests, PoB benchmarks, sweeps | `.github/workflows/run.yml` | `ubuntu-latest` (default) or the self-hosted server `poe-server` | only `heavy_dispatch.py` (below) |

The repository is public. **No `pull_request` job ever runs on the self-hosted server**: `ci.yml` names
`ubuntu-latest` only, and the server is reachable only through `run.yml`, which has no trigger but `workflow_dispatch`
(only someone with write access can start it). Keep it that way when a workflow is added.

A push to `main` starts no CI run. To test `main` (or any ref) on demand: `gh workflow run ci.yml --ref main`.

## What one CI run does

- **Python.** `.github/actions/python` installs uv, makes `.venv` with Python 3.12 and `pip install -e ".[dev,research]"`, and
  puts `.venv/bin` first on the PATH.
- **PoB.** `.github/actions/pob` reads the pin `locks/pob.source.lock.json` (PathOfBuilding v2.67.2, commit
  `b32759ab...`). It restores `vendor/pob/source` from `actions/cache`, keyed by a hash of the pin file, and on a miss
  makes a shallow clone at the pinned tag; either way it then checks that `git rev-parse HEAD` is the pinned commit
  and fails if not. Then it builds the Linux native runtime with `bash scripts/pob_runtime_linux.sh` into
  `vendor/pob/runtime-linux/`, cached by a hash of that script and of the pin (plus the runner's OS and
  architecture). It also puts the pinned portable release (`locks/pob.lock.json`, about 630 MB zipped) at
  `var/cache/pob/<tag>/app`, where the code looks for it: `python -m junkroan.pob.release_manager pob fetch` downloads
  it and checks its size and sha256 against the lock. The zip is cached with the extracted folder, keyed by a hash
  of the lock file, because every PoB launch checks the zip again and downloads it when it is missing; the action
  runs `pob verify` once and fails if the cached zip does not match. A new pin or a changed script is a new key, so the cache follows them without anyone touching CI.
  If the script is missing the step fails with an error that names it; if it leaves `vendor/pob/runtime-linux/`
  empty, the next step fails.
- **Sharding.** The shard options come from the pytest plugin `tests/shard_support.py`. It is **registered on the
  command line**, `-p tests.shard_support`, not from `tests/conftest.py` or `pytest.ini`; every command that uses
  `--shard`, `--shard-durations`, `--record-durations` or `--shard-report` must pass it. `pytest --shard SLOT/TOTAL`
  runs one slot: whole *groups* of tests only, a group being a module, or a module and one value of a module-scoped
  (or wider) parametrized fixture, so an expensive fixture (a PobSession, an evaluated build) is built once, in one
  process. The plan is made after the marker filter (`-m`), so every slot plans over the same tests. Groups are dealt
  out longest first by the seconds in `tests/shard_durations.json`; a group with no stored time counts each test at
  the median stored test, and with no stored time at all (the file starts empty, `{}`) every test counts the same. A
  job runs 4 slots at once (`.github/scripts/run_shard.py`), so 8 jobs x 4 slots = 32 slots.
- **`CI summary`** is the one check to wait for (`.github/scripts/ci_summary.py`). It is green only when all 8 shards
  left their results, no test failed, each shard ran exactly the tests it was given, the shards together hold exactly
  the tests collected, and at least 1000 tests were collected. It prints totals, the skips by reason, the slowest
  shard and the slowest tests (in seconds below 90 s, else minutes). `--forbid-skip TEXT` (repeatable) turns a skip
  whose reason holds TEXT into a failure. CI forbids the skip texts that mean PoB is missing ("PoB runtime",
  "pinned PoB", "PoB skill", "PoB source data", "PoB-needing tests are skipped"), so a broken PoB step cannot pass as
  a green run of skipped tests. A new PoB skip reason must contain one of them.

### Rebalancing the shards

`CI summary` uploads the measured seconds per group as the artifact `shard-durations`. To rebalance, download it from
a green run and commit it as `tests/shard_durations.json`:

    gh run download <run id> --name shard-durations --dir merged
    cp merged/shard_durations.json tests/shard_durations.json

A test added later costs the median until the file is refreshed; refresh it when the slowest shard is clearly longer
than the others.

## Running a shard on your own machine

Only quick, targeted tests run locally. A shard can be reproduced the way CI does it (PoB tests need the pinned
source and runtime in `vendor/pob/`):

    python .github/scripts/run_shard.py --shard 3/8 --procs 4 --out out -- -p tests.shard_support -m "not slow" --shard-durations tests/shard_durations.json

To look at a plan without running anything: `python -m pytest --co -q -p tests.shard_support -m "not slow" --shard 3/32`.

## Heavy runs: `run.yml` and the dispatcher

`run.yml` checks out a branch, sets up Python and the pinned PoB with the same actions as CI, runs a bash command from
the repository root on 1 to 16 runners and uploads what the command wrote into `$OUT_DIR` (plus `output.log`, its
console output) as the artifacts `run-<runner>-<n>`. The command sees `RUNNER_INDEX` (1..N) and `RUNNER_COUNT`, so N
runners can split the work; for slow tests, `--shard $RUNNER_INDEX/$RUNNER_COUNT -p tests.shard_support` does that.
GitHub lets a workflow be started by hand only when its file is on the default branch; the code that runs is the code
of `--ref`. Every input reaches a shell only through `env:`.

**Every heavy run goes through the dispatcher, never `gh workflow run run.yml`:**

    python .github/scripts/heavy_dispatch.py run --ref my-branch --runners 4 --command 'python -m pytest -p tests.shard_support -m slow --shard $RUNNER_INDEX/$RUNNER_COUNT --junitxml $OUT_DIR/junit.xml'
    python .github/scripts/heavy_dispatch.py run --ref my-branch --runner poe-server --timeout-minutes 600 --command '...'
    python .github/scripts/heavy_dispatch.py status

(Any Python 3.10+; the script is standard library only. The token comes from `GH_TOKEN`, else `gh auth token`, else
`git credential fill`. A bad request, such as a timeout out of range, is refused before any token is looked for.)

### The two budgets

**Hosted (`--runner ubuntu-latest`, the default).** The account has 20 hosted runner jobs at once, shared by all its
repositories (Crafting system among them). One CI run
takes 8 of them for its duration; a heavy run takes up to 16, so unchecked heavy runs would stall every pull request.
The dispatcher starts a hosted run only while

    hosted_heavy_in_flight + requested <= HEAVY_BUDGET
    HEAVY_BUDGET = max(HEAVY_FLOOR, 20 - CI_RESERVE - ci_jobs_queued_or_running - shared_jobs)

`shared_jobs` is the hosted jobs queued or running in the repositories named by `SHARED_REPOS` (jobs on their own
self-hosted machines do not count). Each is read once per 90-second snapshot; one that cannot be read (no access, an API error) counts
0 and `status` says so. A shared run whose jobs are not created yet also counts 0, so the count can run low. `status` lists the jobs of each shared repository.

With the defaults, heavy runs may use 16 runners when no CI run is waiting (20 - 4 - 0), 8 while one CI run is
(20 - 4 - 8), and only the floor, 4, while two are. Hosted heavy jobs are kept short so runners free up:
`--timeout-minutes` defaults to 60 and is refused above 60 unless `--long` is given, which needs `--runners 1` and is
for one indivisible job (at most 6 hours, GitHub's limit for a hosted job). Split a long sweep into more, shorter
parts, or send it to the server.

**Server (`--runner poe-server`).** The self-hosted server carries the label `poe-server`; `run.yml` asks for
`[self-hosted, poe-server]`. CI never runs there, so the budget is simply the number of server runners:
`server_heavy_in_flight + requested <= SERVER_RUNNERS`. A timeout of up to 24 hours is allowed without `--long`. A
request for more runners than `SERVER_RUNNERS` is refused at once.

| Variable (repository, Actions variables) | Default | Meaning |
|---|---|---|
| `HEAVY_FLOOR` | 4 | Hosted runners heavy runs always may use, even when CI is busy. |
| `CI_RESERVE` | 4 | Hosted runners kept free for CI on top of the jobs it already has. |
| `SERVER_RUNNERS` | 1 | Runners registered on the server with the label `poe-server`. |
| `SHARED_REPOS` | empty | Other repositories of the account whose hosted jobs take from the same 20 (comma-separated `owner/name`, e.g. `Rasslabsya4el/crafting-system`). Empty: none counted. |

They are turned without a commit (`gh variable set SERVER_RUNNERS --body 2`); the next look of every waiting
dispatcher sees the new value. A heavy run counts against its budget from the moment it is dispatched (its run name,
`heavy 4x poe-server t600: ...`, carries the runners, the runner kind and the timeout, so it is counted before its
jobs exist); sessions on one machine also share a lock while they decide, so two cannot take the same free runners.

The 5,000 GitHub API calls an hour are one limit for every agent and session: dispatchers on one machine share a
snapshot of the runs for 90 seconds, a dispatcher waits for the rate-limit reset (at most an hour, one line printed)
instead of retrying, and for GitHub's secondary limit it waits the `Retry-After` it was given (at most 10 minutes).

Options of `run`: `--runners N` is a maximum, `--min-runners M` lets it start smaller when only M to N fit (the work
must then be split by `RUNNER_INDEX`/`RUNNER_COUNT`); `--max-wait MINUTES` (give up), `--no-wait` (exit 3 if it does
not fit now), `--dry-run` (decide, dispatch nothing). `status` shows both budgets, the runner jobs in use by kind, the
queue with how long it has waited, and the runs older than their own timeout or silent for 30 minutes (each with its
`gh run cancel` line).

### Nobody polls a run inside a turn

A session dispatches with `--no-wait` and notes the run id and what the run must show:

    python .github/scripts/heavy_dispatch.py run --no-wait --ref my-branch --runners 4 --command '...'

Exit 0 prints `dispatched run <id> on <branch> with N <runner> runner(s)`; exit 3 means there is no room now: run the
command again later instead of waiting for room. Wait for a run in the background, so its exit is the notification:

    python .github/scripts/wait_runs.py <run id> [<run id> ...] [--timeout-minutes 90]

`wait_runs.py` takes runs of any workflow. It reads each run's `node_id` once (a run id that is not a run of the
repository exits 2 at once), then makes one GraphQL call per poll for all the runs, at least 4 minutes apart. When a
run completes it prints one line: `run <id>  <branch>  <workflow>  <conclusion>  jobs: success 8`. Exit codes: 0
every run succeeded, 1 one did not, 2 a bad argument, 3 `--timeout-minutes` ran out. It never reads or prints a
token; it calls `gh api`. Then download the files:

    gh run download <run id> --dir results        # one folder per runner: run-ubuntu-latest-1, -2, ...

## The scripts and their tests

| Script | Test |
|---|---|
| `tests/shard_support.py` (the pytest plugin) | `tests/test_shard_support.py` |
| `.github/scripts/run_shard.py` | `tests/test_run_shard.py` |
| `.github/scripts/ci_summary.py` | `tests/test_ci_summary.py` |
| `.github/scripts/heavy_dispatch.py` | `tests/test_heavy_dispatch.py` (a fake API and a fake clock; no network) |
| `.github/scripts/wait_runs.py` | `tests/test_wait_runs.py` (a fake `gh`; no network) |

They need no PoB and run in under a minute.
