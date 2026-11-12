"""The one door for heavy runs: start `run.yml` only while there is room for it.

    python .github/scripts/heavy_dispatch.py run --ref my-branch --runners 4 --command 'python -m pytest -p tests.shard_support -m slow --shard $RUNNER_INDEX/$RUNNER_COUNT'
    python .github/scripts/heavy_dispatch.py run --ref my-branch --runner poe-server --timeout-minutes 600 --command '...'
    python .github/scripts/heavy_dispatch.py status

Two kinds of runner (`--runner`):

- `ubuntu-latest` (default): GitHub's hosted runners. The repository gets 20 runner jobs at once; CI (`ci.yml`, Linux
  only) takes 8 per run, for pull requests and dispatched runs alike, and heavy runs take 1 to 16. The dispatcher
  starts a hosted heavy run only while

      hosted_heavy_in_flight + requested <= HEAVY_BUDGET,
      HEAVY_BUDGET = max(HEAVY_FLOOR, 20 - CI_RESERVE - ci_jobs - shared_jobs)

  `HEAVY_FLOOR` (default 4) and `CI_RESERVE` (default 4) are GitHub Actions repository variables, so they can be
  turned without a commit; `ci_jobs` is the CI jobs queued or running now. The 20 hosted jobs belong to the account,
  not the repository: `shared_jobs` is the hosted jobs queued or running in the repositories named by the variable
  `SHARED_REPOS` (comma-separated `owner/name`; unset or empty = none). Heavy jobs are kept short so runners free
  up: `--timeout-minutes` above 60 needs `--long`, which is for a single indivisible job (one runner).
- `poe-server`: the self-hosted server (runner label `poe-server`). CI never runs there, so its budget is simply the
  number of server runners, the repository variable `SERVER_RUNNERS` (default 1):
  `server_heavy_in_flight + requested <= SERVER_RUNNERS`. A timeout up to 24 hours is allowed without `--long`.

`--runners` is a maximum: with `--min-runners` below it the run starts smaller when only that many fit (the command
must then split its work by RUNNER_INDEX/RUNNER_COUNT and still finish inside `--timeout-minutes`).

The dispatcher waits on the developer's machine (no runner is used while it waits); with `--no-wait` it exits 3 at
once when the run does not fit now. `status` prints both budgets, the runner jobs in use by kind, the queue with
waiting times, and the runs that are older than their own timeout or silent for 30 minutes (candidates to cancel).

The token comes from GH_TOKEN / GITHUB_TOKEN, else `gh auth token`, else `git credential fill`. Standard library only.
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_REPO = "Rasslabsya4el/Poe-Junkroan"
HOSTED = "ubuntu-latest"
SERVER = "poe-server"  # the self-hosted runner label; run.yml asks for [self-hosted, poe-server]
RUNNER_KINDS = (HOSTED, SERVER)
TOTAL_RUNNERS = 20  # concurrent hosted jobs the free plan gives the account, shared by its repositories (SHARED_REPOS)
CI_JOBS_PER_RUN = 8  # a CI run (pull request or dispatch): 8 Linux shards; counted for a CI run whose jobs are not created yet
DEFAULT_FLOOR = 4
DEFAULT_RESERVE = 4
DEFAULT_SERVER_RUNNERS = 1
MAX_RUNNERS = 16  # run.yml's own limit
SHORT_MINUTES = 60  # longest hosted timeout without --long
LONG_MINUTES = 360  # longest hosted timeout (GitHub's own limit for a hosted job)
SERVER_MINUTES = 1440  # longest server timeout: 24 hours
CI_TIMEOUT_MINUTES = 45  # a CI job times out at 30 minutes; a run older than this is stuck
SILENT_MINUTES = 30
ACTIVE = ("queued", "in_progress")  # job statuses that hold or wait for a runner
PENDING_RUN = ("pending", "waiting", "requested")  # run statuses before any job exists, e.g. held by a concurrency group
# The 5,000 GitHub API calls an hour are shared by every agent and session of the owner. One waiting dispatcher costs
# about 3 + 10 + N calls per look (N = runs in flight), so it looks every 3 minutes, and the processes on one machine
# share one snapshot (SNAPSHOT_SECONDS) instead of each fetching its own.
POLL_SECONDS = 180
SNAPSHOT_SECONDS = 90  # a look within this long of the stored snapshot reuses it and calls nothing
RATE_LIMIT_CAP_SECONDS = 3600  # the longest wait for a rate-limit reset
RETRY_AFTER_CAP_SECONDS = 600  # the longest wait for GitHub's secondary limit (its Retry-After is normally 60 s)
STATE_DIR = Path(tempfile.gettempdir()) / "poe-junkroan-heavy-dispatch"  # shared by every session on this machine
LOCK_STALE_SECONDS = 300
LEDGER_HOURS = 25  # a server run may take 24 hours

LOG_STAMP = r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}[:][0-9]{2}[:][0-9]{2})"  # [:] keeps the drive-letter scan quiet
RUN_NAME = re.compile(r"^heavy (\d+)x (\S+) t(\d+)")


def now() -> float:
    """The clock of this script (seconds since the epoch); a seam so the tests can run it on a fake clock."""
    return time.time()


def pause(seconds: float) -> None:
    """Every wait of this script goes through here, for the same reason."""
    time.sleep(seconds)


# ---- pure decisions (tested on recorded API responses) -------------------------------------------------------------


def heavy_budget(floor: int, reserve: int, ci_jobs: int, total: int = TOTAL_RUNNERS, shared_jobs: int = 0) -> int:
    """Runners heavy runs may hold at once: what CI, its reserve and the shared repositories' hosted jobs leave, but
    never below the floor."""
    return max(floor, total - reserve - ci_jobs - shared_jobs)


def parse_shared_repos(text: str | None, own: str = "") -> list[str]:
    """`owner/name` entries of the SHARED_REPOS variable: comma or whitespace separated, duplicates and this
    repository itself dropped, order kept. Anything without exactly one slash is ignored."""
    found: list[str] = []
    for item in re.split(r"[,\s]+", text or ""):
        parts = item.split("/")
        if len(parts) != 2 or not all(parts):
            continue
        if item.lower() == own.lower() or item.lower() in (f.lower() for f in found):
            continue
        found.append(item)
    return found


def hosted_jobs(jobs: list[dict]) -> dict[str, int]:
    """Running and queued jobs of another repository that hold or wait for a hosted runner (a job whose labels name
    `self-hosted` runs on that repository's own machines and is not counted)."""
    hosted = [job for job in jobs if job.get("status") in ACTIVE and "self-hosted" not in (job.get("labels") or [])]
    return {"running": sum(1 for job in hosted if job["status"] == "in_progress"),
            "queued": sum(1 for job in hosted if job["status"] == "queued")}


def runners_to_start(heavy_in_flight: int, requested: int, minimum: int, budget: int) -> int:
    """How many runners to dispatch now: all `requested` if they fit, else as many as fit when that is at least
    `minimum`, else 0 (wait)."""
    room = budget - heavy_in_flight
    if room >= requested:
        return requested
    if room >= minimum:
        return room
    return 0


def parse_run_name(title: str) -> tuple[int, str, int] | None:
    """(runners, runner kind, timeout minutes) from the run name `heavy 4x ubuntu-latest t60 ...` that run.yml sets."""
    found = RUN_NAME.match(title or "")
    return (int(found[1]), found[2], int(found[3])) if found else None


def parse_time(stamp: str | None) -> dt.datetime | None:
    return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else None


def run_occupancy(run: dict, jobs: list[dict], ledger_runners: int = 0) -> dict:
    """Runner jobs one run holds: running, queued, and the total counted against the budget.

    A run whose matrix is not created yet (the `plan` job still queued or running) counts as the runners it asked for,
    read from its name or from the dispatcher's ledger, so a fresh heavy run is never invisible."""
    running = sum(1 for job in jobs if job["status"] == "in_progress")
    queued = sum(1 for job in jobs if job["status"] == "queued")
    is_ci = run["path"].endswith("ci.yml")
    matrix_made = any(job["name"].startswith(("tests (", "run (")) for job in jobs)
    expected = 0
    if not matrix_made:
        if is_ci:
            expected = CI_JOBS_PER_RUN
        else:
            named = parse_run_name(run.get("display_title", ""))
            expected = named[0] if named else ledger_runners
    return {"running": running, "queued": queued, "counted": max(running + queued, expected)}


def runner_kind(run: dict) -> str:
    """The runner kind a heavy run asked for, read from its run name; a name that does not parse counts as hosted."""
    named = parse_run_name(run.get("display_title", ""))
    return SERVER if named and named[1] == SERVER else HOSTED


def totals(occupancies: list[tuple[dict, dict]]) -> dict[str, int]:
    """CI jobs, hosted heavy jobs and server heavy jobs counted against the budgets, from (run, occupancy) pairs."""
    counted = {"ci": 0, HOSTED: 0, SERVER: 0}
    for run, occ in occupancies:
        if run["path"].endswith("ci.yml"):
            counted["ci"] += occ["counted"]
        elif run["path"].endswith("run.yml"):
            counted[runner_kind(run)] += occ["counted"]
    return counted


def budget_for(kind: str, floor: int, reserve: int, server_runners: int, counted: dict[str, int]) -> int:
    """Runners heavy runs of this kind may hold at once: the hosted formula, or the number of server runners."""
    return server_runners if kind == SERVER else heavy_budget(floor, reserve, counted["ci"], shared_jobs=counted.get("shared", 0))


def shared_total(shared: dict[str, dict]) -> int:
    """Hosted jobs (running + queued) of all shared repositories in a raw snapshot's `shared` entry."""
    return sum(item["running"] + item["queued"] for item in shared.values())


def stale_reason(run: dict, jobs: list[dict], now: dt.datetime, last_output: dt.datetime | None) -> str | None:
    """Why a run is a candidate to cancel (older than its own timeout, or silent for 30 minutes), else None."""
    is_ci = run["path"].endswith("ci.yml")
    named = parse_run_name(run.get("display_title", ""))
    limit = CI_TIMEOUT_MINUTES if is_ci else (named[2] if named else LONG_MINUTES)
    started = parse_time(run.get("run_started_at") or run["created_at"])
    # a heavy run may wait in the queue; only time since its first job began counts
    began = [parse_time(job.get("started_at")) for job in jobs if job.get("started_at")]
    if not is_ci and began:
        started = min(began)
    elif not is_ci:
        started = None
    if started is not None:
        age = (now - started).total_seconds() / 60
        if age > limit + 5:
            return f"running {age:.0f} min, its timeout is {limit} min"
    if last_output is not None and any(job["status"] == "in_progress" for job in jobs):
        silent = (now - last_output).total_seconds() / 60
        if silent > SILENT_MINUTES:
            return f"no log output for {silent:.0f} min"
    return None


# ---- GitHub API ----------------------------------------------------------------------------------------------------


def find_token() -> str:
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    attempts = (
        (["gh", "auth", "token"], None, lambda out: out.strip()),
        (["git", "credential", "fill"], "protocol=https\nhost=github.com\n\n", lambda out: next((line[9:] for line in out.splitlines() if line.startswith("password=")), "")),
    )
    for command, stdin, parse in attempts:
        if shutil.which(command[0]) is None:
            continue
        try:
            done = subprocess.run(command, input=stdin, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            continue
        token = parse(done.stdout)
        if done.returncode == 0 and token:
            return token
    sys.exit("heavy_dispatch: no GitHub token (set GH_TOKEN, or log in with `gh auth login`)")


def find_repo() -> str:
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, timeout=15).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return DEFAULT_REPO
    found = re.search(r"github\.com[:/]([^/]+/[^/.]+)", url)
    return found[1] if found else DEFAULT_REPO


def sleep_keeping_lock(wait: float) -> None:
    """Sleep `wait` seconds in steps of a minute, touching the lock this process holds after each step, or another
    session would take it over after LOCK_STALE_SECONDS."""
    end = now() + wait
    while now() < end:
        pause(min(60.0, end - now()))
        DispatchLock.keep_fresh()


def wait_for_rate_limit(method: str, path: str, reset: str | None) -> None:
    """The hourly limit is spent: sleep until X-RateLimit-Reset (at most an hour), say so in one line, and go on.
    Retrying earlier only spends calls that are not there."""
    try:
        wait = float(reset) - now() + 2  # 2 s past the reset: the clocks differ a little
    except (TypeError, ValueError):
        wait = 60.0  # no usable reset time: a minute, never a tight loop
    wait = min(max(wait, 2.0), RATE_LIMIT_CAP_SECONDS)
    print(f"{stamp()} GitHub API rate limit used up ({method} {path}); waiting {wait / 60:.0f} min until its reset", flush=True)
    sleep_keeping_lock(wait)


def wait_for_secondary_limit(method: str, path: str, retry_after: str | None) -> None:
    """GitHub's secondary limit (too many calls close together): a refusal with Retry-After seconds and requests still
    left in the hour. Sleep that long (at most RETRY_AFTER_CAP_SECONDS), say so in one line, and go on."""
    try:
        wait = float(retry_after)
    except (TypeError, ValueError):
        wait = 60.0  # a date, or nothing usable: a minute
    wait = min(max(wait, 1.0), RETRY_AFTER_CAP_SECONDS)
    print(f"{stamp()} GitHub secondary rate limit ({method} {path}); waiting {wait:.0f} s as Retry-After says", flush=True)
    sleep_keeping_lock(wait)


class Api:
    def __init__(self, repo: str, token: str):
        self.repo = repo
        self.base = f"https://api.github.com/repos/{repo}"
        self.token = token

    def call(self, path: str, method: str = "GET", body: dict | None = None, tries: int = 4):
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method)
        request.add_header("Authorization", f"Bearer {self.token}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        attempt = 0
        limited = 0  # waits for the rate limit so far; each ends past the reset time, so a third means something else is wrong
        while True:
            attempt += 1
            DispatchLock.keep_fresh()  # before and after every try (the finally below): a slow call inside the lock must not make it stale
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as error:
                if error.code == 404 and method == "GET":
                    return None
                if error.code in (403, 429) and limited < 3:
                    if error.headers.get("X-RateLimit-Remaining") == "0":  # the hourly limit
                        limited += 1
                        attempt -= 1  # a wait for the reset is not one of the failed tries
                        wait_for_rate_limit(method, path, error.headers.get("X-RateLimit-Reset"))
                        continue
                    if error.headers.get("Retry-After") is not None:  # the secondary limit
                        limited += 1
                        attempt -= 1
                        wait_for_secondary_limit(method, path, error.headers.get("Retry-After"))
                        continue
                if error.code < 500 and error.code != 429 or attempt == tries:
                    raise RuntimeError(f"{method} {path}: HTTP {error.code} {error.read()[:300]!r}") from None
            except (urllib.error.URLError, TimeoutError):
                if attempt == tries:
                    raise
            finally:
                DispatchLock.keep_fresh()
            pause(3 * attempt)

    def variable(self, name: str, default: int) -> int:
        found = self.call(f"/actions/variables/{name}")
        try:
            return int(found["value"]) if found else default
        except (KeyError, ValueError):
            return default

    def text_variable(self, name: str) -> str:
        found = self.call(f"/actions/variables/{name}")
        return str(found.get("value", "")) if found else ""

    def shared_jobs(self, repo: str) -> dict[str, int] | None:
        """Hosted jobs running or queued in another repository of the account: one run list per status, then the jobs
        of each active run. None when the repository cannot be read (no access, a typo)."""
        other = Api(repo, self.token)
        runs, readable = {}, False
        for status in ACTIVE:
            page = other.call(f"/actions/runs?status={status}&per_page=100")
            if page is not None:
                readable = True
                runs.update({run["id"]: run for run in page.get("workflow_runs", [])})
        if not readable:
            return None
        jobs = []
        for run_id in runs:
            page = other.call(f"/actions/runs/{run_id}/jobs?per_page=100&filter=latest")
            jobs.extend(page["jobs"] if page else [])
        return hosted_jobs(jobs)

    def active_runs(self) -> list[dict]:
        runs = []
        for workflow in ("ci.yml", "run.yml"):
            for status in (*ACTIVE, *PENDING_RUN):
                page = self.call(f"/actions/workflows/{workflow}/runs?status={status}&per_page=100")
                runs.extend(page["workflow_runs"] if page else [])
        unique = {run["id"]: run for run in runs}
        return list(unique.values())

    def jobs(self, run_id: int) -> list[dict]:
        page = self.call(f"/actions/runs/{run_id}/jobs?per_page=100&filter=latest")
        return page["jobs"] if page else []

    def last_output(self, job_id: int) -> dt.datetime | None:
        """Time of the newest log line of a running job, if GitHub serves the log of a running job. The log lives
        behind a redirect to another host, which must not get the token."""

        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None

        try:
            request = urllib.request.Request(f"{self.base}/actions/jobs/{job_id}/logs")
            request.add_header("Authorization", f"Bearer {self.token}")
            try:
                with urllib.request.build_opener(NoRedirect).open(request, timeout=60) as response:
                    text = response.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as error:
                if error.code not in (301, 302, 303, 307, 308) or not error.headers.get("Location"):
                    return None
                with urllib.request.urlopen(error.headers["Location"], timeout=60) as response:
                    text = response.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return None
        stamps = re.findall(LOG_STAMP, text, re.MULTILINE)
        return parse_time(stamps[-1] + "Z") if stamps else None


def fetch_raw(api: Api, own: str = "") -> dict:
    """What the API says now, unprocessed: the variables, every active run with its jobs, and the hosted jobs of
    each shared repository (`shared`: {repo: {running, queued}}; a repository that cannot be read is listed in
    `unreadable` and counts 0)."""
    floor = api.variable("HEAVY_FLOOR", DEFAULT_FLOOR)
    reserve = api.variable("CI_RESERVE", DEFAULT_RESERVE)
    server = api.variable("SERVER_RUNNERS", DEFAULT_SERVER_RUNNERS)
    runs = [{"run": run, "jobs": api.jobs(run["id"])} for run in api.active_runs()]
    shared, unreadable = {}, []
    for repo in parse_shared_repos(api.text_variable("SHARED_REPOS"), own):
        try:
            found = api.shared_jobs(repo)
        except (RuntimeError, OSError):  # a 403, a 5xx after the retries, a dropped connection (URLError is an OSError)
            found = None
        if found is None:
            unreadable.append(repo)
        else:
            shared[repo] = found
    return {"floor": floor, "reserve": reserve, "server": server, "runs": runs, "shared": shared, "unreadable": unreadable}


def occupancies(raw_runs: list[dict], ledger: dict[str, int]) -> list[tuple[dict, list[dict], dict]]:
    """(run, jobs, occupancy) of raw {run, jobs} entries, counted with the ledger as it is now."""
    return [(item["run"], item["jobs"], run_occupancy(item["run"], item["jobs"], ledger.get(str(item["run"]["id"]), 0))) for item in raw_runs]


def snapshot(api: Api, ledger: dict[str, int]) -> list[tuple[dict, list[dict], dict]]:
    """(run, jobs, occupancy) of every queued or running run of ci.yml and run.yml, fetched live."""
    return occupancies(fetch_raw(api)["runs"], ledger)


def read_shared_snapshot() -> dict | None:
    """The raw snapshot an earlier look on this machine stored, if it is younger than SNAPSHOT_SECONDS. Lock held."""
    try:
        stored = json.loads((STATE_DIR / "snapshot.json").read_text(encoding="utf-8"))
        age = now() - stored["at"]
        if 0 <= age < SNAPSHOT_SECONDS and {"floor", "reserve", "server", "runs"} <= stored.keys():
            return stored
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    return None


def write_shared_snapshot(raw: dict, at: float) -> None:
    """Store a raw snapshot for the next look. Lock held."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        part = STATE_DIR / f"snapshot.{os.getpid()}.tmp"
        part.write_text(json.dumps({**raw, "at": at}), encoding="utf-8")
        os.replace(part, STATE_DIR / "snapshot.json")
    except OSError:
        pass  # only a saving of calls is lost


def drop_shared_snapshot() -> None:
    """Delete the stored snapshot. Lock held."""
    path = STATE_DIR / "snapshot.json"
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    except OSError:  # cannot delete it (a sharing violation on Windows): make it too old to be used
        try:
            path.write_text(json.dumps({"at": 0}), encoding="utf-8")
        except OSError:
            pass


# ---- state shared by the sessions on this machine -----------------------------------------------------------------------


def read_ledger() -> dict[str, int]:
    """Runners of the runs this script dispatched, for the minutes before their matrix jobs exist."""
    try:
        entries = json.loads((STATE_DIR / "ledger.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    cutoff = now() - LEDGER_HOURS * 3600
    return {run_id: item["runners"] for run_id, item in entries.items() if item["at"] > cutoff}


def write_ledger(run_id: int, runners: int) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        path = STATE_DIR / "ledger.json"
        try:
            entries = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            entries = {}
        entries[str(run_id)] = {"runners": runners, "at": now()}
        path.write_text(json.dumps(entries), encoding="utf-8")
    except OSError:
        pass  # the ledger only covers a few minutes; the run name covers the same ground


class LockBusy(Exception):
    """The dispatch lock is held by another session and this one may not wait for it (--no-wait), or has waited as
    long as --max-wait allows. The message names the holder."""


def touch(path: Path) -> None:
    """Set the modification time of `path` to this script's clock. The lock's age is read against the same clock
    (now() - mtime), so the two always agree: in production both are the real time, in the tests both are the fake."""
    moment = now()
    os.utime(path, (moment, moment))


class DispatchLock:
    """Two sessions on this machine must not both see free runners and both dispatch: one holds this lock from the
    decision until its run shows up in the API. The lock is a directory in the PC's temp folder; it belongs to the
    process that made it (a token file inside) and is taken over only when older than LOCK_STALE_SECONDS.

    A second session waits for it, but not past `deadline` (--max-wait) and not at all with `no_wait` (--no-wait): it
    raises LockBusy then. While it waits it prints one line saying who holds the lock and since when."""

    def __init__(self, no_wait: bool = False, deadline: float | None = None, what: str = ""):
        self.path = STATE_DIR / "dispatch.lock"
        self.token = f"{os.getpid()}-{time.time_ns()}"
        self.no_wait = no_wait
        self.deadline = deadline
        self.what = what

    held: "DispatchLock | None" = None  # the lock this process holds now, if any

    @classmethod
    def keep_fresh(cls) -> None:
        """Touch the held lock, so a long wait inside it is not taken for a dead owner."""
        lock = cls.held
        try:
            if lock is not None and (lock.path / "owner").read_text(encoding="utf-8") == lock.token:
                touch(lock.path)
        except OSError:
            pass

    def holder(self) -> str:
        """Who holds the lock now and since when, for the one line a waiting session prints."""
        try:
            info = json.loads((self.path / "info").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            info = {}
        since = info.get("at")
        if since is None:
            try:
                since = self.path.stat().st_mtime
            except OSError:
                pass
        who = f"process {info['pid']}" if info.get("pid") else "another process"
        who += f" ({info['what']})" if info.get("what") else ""
        when = f" since {dt.datetime.fromtimestamp(since).strftime('%H:%M:%S')}" if since is not None else ""
        return f"dispatch lock held by {who}{when}"

    def __enter__(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        told = False
        while True:
            try:
                os.mkdir(self.path)
            except OSError:  # FileExistsError, or PermissionError while another process removes it (Windows)
                try:
                    if now() - self.path.stat().st_mtime > LOCK_STALE_SECONDS:
                        shutil.rmtree(self.path, ignore_errors=True)
                        continue
                except OSError:
                    pass
                if self.no_wait or (self.deadline is not None and now() >= self.deadline):
                    raise LockBusy(self.holder()) from None
                if not told:
                    print(f"{stamp()} {self.holder()} -> waiting for it", flush=True)
                    told = True
                pause(2)
                continue
            # The directory is ours now. A failure from here on is not a busy lock: take the half-made lock away, so
            # this session does not wait on it until it goes stale, and raise the error itself.
            try:
                (self.path / "owner").write_text(self.token, encoding="utf-8")
                (self.path / "info").write_text(json.dumps({"pid": os.getpid(), "at": now(), "what": self.what}), encoding="utf-8")
                touch(self.path)  # last: writing the files above moves the directory's time by the file system's clock
            except BaseException:
                shutil.rmtree(self.path, ignore_errors=True)
                raise
            DispatchLock.held = self
            return self

    def __exit__(self, *exc):
        if DispatchLock.held is self:
            DispatchLock.held = None
        try:
            if (self.path / "owner").read_text(encoding="utf-8") == self.token:
                shutil.rmtree(self.path, ignore_errors=True)
        except OSError:
            pass


# ---- commands ------------------------------------------------------------------------------------------------------


def stamp() -> str:
    return dt.datetime.now().strftime("%H:%M:%S")


def check_args(args) -> None:
    if args.runner not in RUNNER_KINDS:
        sys.exit(f"--runner must be one of {', '.join(RUNNER_KINDS)}, not {args.runner}")
    if not 1 <= args.runners <= MAX_RUNNERS:
        sys.exit(f"--runners must be 1 to {MAX_RUNNERS}, not {args.runners}")
    if args.min_runners is None:
        args.min_runners = args.runners
    if not 1 <= args.min_runners <= args.runners:
        sys.exit(f"--min-runners must be 1 to --runners ({args.runners}), not {args.min_runners}")
    if args.runner == SERVER:
        if not 1 <= args.timeout_minutes <= SERVER_MINUTES:
            sys.exit(f"--timeout-minutes on {SERVER} must be 1 to {SERVER_MINUTES}, not {args.timeout_minutes}")
        return
    if not 1 <= args.timeout_minutes <= LONG_MINUTES:
        sys.exit(f"--timeout-minutes on {HOSTED} must be 1 to {LONG_MINUTES}, not {args.timeout_minutes}")
    if args.timeout_minutes > SHORT_MINUTES:
        if not args.long:
            sys.exit(
                f"--timeout-minutes {args.timeout_minutes} is over {SHORT_MINUTES}: long jobs hold a hosted runner for hours. "
                f"Split the work into more, shorter parts (--runners, RUNNER_INDEX/RUNNER_COUNT); --long is only for a "
                f"single indivisible job on one runner, and --runner {SERVER} takes long runs."
            )
        if args.runners != 1:
            sys.exit("--long is for a single indivisible job: it needs --runners 1")


def cmd_run(api: Api, args) -> int:
    check_args(args)
    if args.runner == SERVER:
        server = api.variable("SERVER_RUNNERS", DEFAULT_SERVER_RUNNERS)
        if args.min_runners > server:
            sys.exit(f"{args.min_runners} runners can never fit: the server has {server} (SERVER_RUNNERS). Ask for fewer.")
    else:
        floor = api.variable("HEAVY_FLOOR", DEFAULT_FLOOR)
        reserve = api.variable("CI_RESERVE", DEFAULT_RESERVE)
        if args.min_runners > TOTAL_RUNNERS - reserve and args.min_runners > floor:
            sys.exit(
                f"{args.min_runners} runners can never fit: the most hosted heavy runs ever get is "
                f"{max(floor, TOTAL_RUNNERS - reserve)} (CI_RESERVE={reserve}, HEAVY_FLOOR={floor}). Ask for fewer."
            )
    deadline = now() + args.max_wait * 60 if args.max_wait else None
    while True:
        try:
            with DispatchLock(no_wait=args.no_wait, deadline=deadline, what=f"run on {args.ref}"):
                decided = decide(api, args)
                if decided["count"] and not args.dry_run:
                    print(f"{stamp()} {decided['line']} -> starting {decided['count']} runner(s)", flush=True)
                    return dispatch(api, args, decided["count"])
        except LockBusy as busy:  # another session holds the lock and we may not wait for it, or have waited enough
            if args.no_wait:
                print(f"{stamp()} {busy} -> does not fit now", flush=True)
                return 3
            print(f"{stamp()} gave up after {args.max_wait} min of waiting for the dispatch lock", flush=True)
            return 2
        except (RuntimeError, urllib.error.URLError, TimeoutError, OSError) as error:
            decided = {"count": 0, "line": f"GitHub API error ({str(error)[:120]}), will retry"}
        if decided["count"]:
            print(f"{stamp()} {decided['line']} -> would start {decided['count']} runner(s); dry run: nothing dispatched")
            return 0
        line = decided["line"]
        if deadline and now() > deadline:
            print(f"{stamp()} {line} -> gave up after {args.max_wait} min of waiting", flush=True)
            return 2
        if args.no_wait:
            print(f"{stamp()} {line} -> does not fit now", flush=True)
            return 3
        print(f"{stamp()} {line} -> waiting", flush=True)
        pause(POLL_SECONDS)


def decide(api: Api, args) -> dict:
    """One look at the counts: how many runners to start now (0 = wait) and the status line.

    Call it with DispatchLock held. The raw snapshot is shared by the processes on this machine in STATE_DIR/snapshot.json:
    a look within SNAPSHOT_SECONDS of it reuses it and calls nothing. Occupancy is counted from the raw
    runs with the ledger as it is now. dispatch() drops the snapshot before the lock is released."""
    raw = read_shared_snapshot()
    if raw is None:
        fetched_at = now()
        raw = fetch_raw(api, getattr(api, "repo", ""))
        write_shared_snapshot(raw, fetched_at)
    floor, reserve, server = raw["floor"], raw["reserve"], raw["server"]
    seen = occupancies(raw["runs"], read_ledger())
    counted = totals([(run, occ) for run, _, occ in seen])
    counted["shared"] = shared_total(raw.get("shared", {}))
    budget = budget_for(args.runner, floor, reserve, server, counted)
    count = runners_to_start(counted[args.runner], args.runners, args.min_runners, budget)
    if args.runner == SERVER:
        line = f"{SERVER}: heavy in flight {counted[SERVER]}, budget {budget} (SERVER_RUNNERS={server})"
    else:
        line = (
            f"{HOSTED}: CI jobs {counted['ci']}, shared repos {counted['shared']}, heavy in flight {counted[HOSTED]}, budget {budget} "
            f"(HEAVY_FLOOR={floor}, CI_RESERVE={reserve})"
        )
    line += f", wanted {args.runners}" + (f" (at least {args.min_runners})" if args.min_runners != args.runners else "")
    return {"count": count, "line": line}


def dispatch(api: Api, args, count: int) -> int:
    """Start the run. Called with the caller's DispatchLock held; the stored snapshot is dropped on every way out,
    before that lock is released, so the next decision sees the run just started."""
    try:
        return start_run(api, args, count)
    finally:
        drop_shared_snapshot()


def start_run(api: Api, args, count: int) -> int:
    before = {run["id"] for run in find_runs(api, args.ref)}
    started = dt.datetime.now(dt.timezone.utc)
    inputs = {
        "command": args.command,
        "runners": str(count),
        "runner": args.runner,
        "timeout_minutes": str(args.timeout_minutes),
    }
    api.call("/actions/workflows/run.yml/dispatches", "POST", {"ref": args.ref, "inputs": inputs})
    # From here the run exists: never raise, or the caller would dispatch it a second time.
    for _ in range(30):  # the run shows up within seconds; holding the lock until then keeps the next session honest
        pause(4)
        try:
            fresh = [run for run in find_runs(api, args.ref) if run["id"] not in before]
        except (RuntimeError, urllib.error.URLError, TimeoutError, OSError):
            continue
        fresh = [run for run in fresh if parse_time(run["created_at"]) >= started - dt.timedelta(seconds=30)]
        if fresh:
            run = max(fresh, key=lambda item: item["id"])
            write_ledger(run["id"], count)
            print(f"dispatched run {run['id']} on {args.ref} with {count} {args.runner} runner(s): {run['html_url']}")
            return 0
    print("dispatched, but the run did not show up in 2 minutes; check `heavy_dispatch.py status`")
    return 0


def find_runs(api: Api, branch: str) -> list[dict]:
    page = api.call(f"/actions/workflows/run.yml/runs?event=workflow_dispatch&per_page=30&branch={urllib.request.quote(branch)}")
    return page["workflow_runs"] if page else []


def minutes_since(stamp_text: str | None, now: dt.datetime) -> float:
    moment = parse_time(stamp_text)
    return (now - moment).total_seconds() / 60 if moment else 0.0


def cmd_status(api: Api, args) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    raw = fetch_raw(api, getattr(api, "repo", ""))  # reads each variable once, with the runs
    floor, reserve, server = raw["floor"], raw["reserve"], raw["server"]
    seen = occupancies(raw["runs"], read_ledger())
    counted = totals([(run, occ) for run, _, occ in seen])
    ci_jobs, hosted = counted["ci"], counted[HOSTED]
    shared = raw.get("shared", {})
    shared_jobs = shared_total(shared)
    budget = heavy_budget(floor, reserve, ci_jobs, shared_jobs=shared_jobs)
    in_use = sum(occ["running"] for run, _, occ in seen if not (run["path"].endswith("run.yml") and runner_kind(run) == SERVER))
    in_use += sum(item["running"] for item in shared.values())
    print(f"Hosted runner jobs: {in_use} running of {TOTAL_RUNNERS}; CI {ci_jobs} (running or queued), shared repos {shared_jobs}, heavy {hosted}")
    for repo, item in shared.items():
        print(f"  shared {repo}: {item['running']} running, {item['queued']} queued")
    for repo in raw.get("unreadable", []):
        print(f"  shared {repo}: cannot be read (no access or no such repository), counted as 0")
    print(f"Hosted heavy budget {budget} = max(HEAVY_FLOOR={floor}, {TOTAL_RUNNERS} - CI_RESERVE={reserve} - CI jobs {ci_jobs} - shared {shared_jobs}); room for {max(0, budget - hosted)} more")
    print(f"Server heavy budget {server} (SERVER_RUNNERS), heavy {counted[SERVER]}; room for {max(0, server - counted[SERVER])} more")
    print("\nIn use / queued, by kind:")
    if not seen:
        print("  nothing running or queued")
    for run, jobs, occ in sorted(seen, key=lambda item: (item[0]["path"], item[0]["id"])):
        is_ci = run["path"].endswith("ci.yml")
        kind = "CI   " if is_ci else "heavy"
        what = f"PR {run['pull_requests'][0]['number']} " if is_ci and run.get("pull_requests") else ""
        label = f"{what}{run['head_branch']}"
        if not is_ci:
            named = parse_run_name(run.get("display_title", ""))
            if named:
                label += f" ({named[0]} runners, {named[1]}, timeout {named[2]} min)"
        waited = f"; oldest queued job waited {max((minutes_since(job['created_at'], now) for job in jobs if job['status'] == 'queued'), default=0):.0f} min" if occ["queued"] else ""
        print(f"  {kind} {label}: {occ['running']} running, {occ['queued']} queued, {occ['counted']} counted, run {run['id']}{waited}")
    queued_runs = [(run, occ) for run, _, occ in seen if occ["queued"] or (occ["counted"] and not occ["running"])]
    print("\nQueue (waiting for a runner):")
    if not queued_runs:
        print("  empty")
    for run, occ in sorted(queued_runs, key=lambda item: item[0]["created_at"]):
        print(f"  {run['path'].split('/')[-1]} {run['head_branch']}: {occ['queued'] or occ['counted']} job(s), run created {minutes_since(run['created_at'], now):.0f} min ago")
    print("\nCandidates to cancel (older than their timeout, or silent for 30 minutes):")
    flagged = 0
    for run, jobs, _ in seen:
        running = [job for job in jobs if job["status"] == "in_progress"]
        output = api.last_output(running[0]["id"]) if running and not args.no_logs else None
        reason = stale_reason(run, jobs, now, output)
        if reason:
            flagged += 1
            print(f"  run {run['id']} ({run['path'].split('/')[-1]}, {run['head_branch']}): {reason}  ->  gh run cancel {run['id']}")
    if not flagged:
        print("  none")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="action", required=True)
    run = commands.add_parser("run", help="wait for room, then dispatch run.yml")
    run.add_argument("--ref", required=True, help="branch whose code runs")
    run.add_argument("--command", required=True, help="bash command (see docs/ci.md); write results into $OUT_DIR")
    run.add_argument("--runners", type=int, default=1, help="most runners to use, 1 to 16 (on poe-server at most SERVER_RUNNERS)")
    run.add_argument("--min-runners", type=int, help="start smaller than --runners when only this many fit (default: --runners, never smaller)")
    run.add_argument("--runner", default=HOSTED, choices=RUNNER_KINDS, help="hosted runners (default) or the self-hosted server")
    run.add_argument("--timeout-minutes", type=int, default=SHORT_MINUTES, help=f"on {HOSTED} over 60 needs --long (at most {LONG_MINUTES}); on {SERVER} up to {SERVER_MINUTES}")
    run.add_argument("--long", action="store_true", help=f"on {HOSTED}, allow a timeout over 60 minutes: one runner, one indivisible job")
    run.add_argument("--max-wait", type=int, default=0, help="give up after this many minutes of waiting (default: wait for ever)")
    run.add_argument("--no-wait", action="store_true", help="exit with 3 instead of waiting when it does not fit now")
    run.add_argument("--dry-run", action="store_true", help="decide and print, dispatch nothing")
    status = commands.add_parser("status", help="show the runner queue")
    status.add_argument("--no-logs", action="store_true", help="skip the log check for silent runs")
    for sub in (run, status):
        sub.add_argument("--repo", default=None, help=f"owner/name (default: the git remote, else {DEFAULT_REPO})")
    args = parser.parse_args(argv)
    if args.action == "run":
        check_args(args)  # a bad request is refused before any token or network is needed
    api = Api(args.repo or find_repo(), find_token())
    return cmd_run(api, args) if args.action == "run" else cmd_status(api, args)


if __name__ == "__main__":
    sys.exit(main())
