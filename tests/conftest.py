"""Shared test helpers and the guard that keeps PoB out of the quick suite.

PoB guard (`junkroan.pob.no_pob_switch`):

- A quick run (`-m "not slow and not pob"`, the `pytest.ini` default) turns `JUNKROAN_NO_POB` on for the
  whole session, unless the environment already set it.
- Under the switch every test carrying the `pob` mark, or a `skipif` whose reason says it needs PoB
  (`_POB_REASON_MARKERS`), is skipped, whatever the checkout has on disk.
- `guard_pob_launch` sits where the real PoB worker process is started and raises under the switch; each
  refusal is counted, and a session that tried even once ends failed.

`needs_skill_source` / `needs_pob_source` skip a test (or a module) that reads PoB's vendored source
(`vendor/pob/source`, gitignored, pinned in `locks/pob.source.lock.json`) when the checkout has none.

`pytest_runtest_setup` pins `src` back to `sys.path[0]` before every test body: many test files put
`scripts/` on `sys.path`, and `scripts/junkroan.py` (a plain module) would otherwise shadow the `junkroan`
package for a spawn-mode child process a later test starts.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from junkroan.pob.no_pob_switch import ENV_VAR, launch_attempts, pob_disabled

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = str(PROJECT_ROOT / "src")

POB_SOURCE_DIR = PROJECT_ROOT / "vendor" / "pob" / "source"
# what junkroan.pob.skill_facts.SKILL_DATA_DIRS[0] points at; game_corpus reads the same clone
SKILL_SOURCE_DIR = POB_SOURCE_DIR / "src" / "Data" / "Skills"

needs_skill_source = pytest.mark.skipif(
    not SKILL_SOURCE_DIR.is_dir(),
    reason=f"PoB skill source data not present at {SKILL_SOURCE_DIR} (vendor/pob/source is gitignored)",
)

POB_SOURCE_MISSING_REASON = f"PoB skill source data not present at {POB_SOURCE_DIR} (vendor/pob/source is gitignored)"

# Substrings of the `reason=` every PoB-needing `skipif` in this suite carries: the pinned runtime ("PoB runtime"),
# PoB's Lua skill data ("PoB skill data") and the vendored source ("PoB skill source data").
_POB_REASON_MARKERS = ("PoB runtime", "PoB skill data", "PoB skill source data")


def skip_module_without_pob_source() -> None:
    """Call at the top of a test module that reads `vendor/pob/source` at import: skips the whole module without it."""

    if not POB_SOURCE_DIR.is_dir():
        pytest.skip(POB_SOURCE_MISSING_REASON, allow_module_level=True)


def pytest_configure(config: pytest.Config) -> None:
    markexpr = (config.getoption("markexpr", default="") or "").replace(" ", "")
    if "notpob" in markexpr and ENV_VAR not in os.environ:
        os.environ[ENV_VAR] = "1"


def _skipif_reasons(item: pytest.Item) -> list[str]:
    reasons: list[str] = []
    for marker in item.iter_markers(name="skipif"):
        reason = marker.kwargs.get("reason")
        if reason is None and len(marker.args) > 1:
            reason = marker.args[1]
        if isinstance(reason, str):
            reasons.append(reason)
    return reasons


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Under `JUNKROAN_NO_POB`, skip every `pob`-marked test and every test whose `skipif` reason says it needs PoB."""

    if not pob_disabled():
        return
    skip = pytest.mark.skip(reason=f"{ENV_VAR} is set: PoB-needing tests are skipped")
    for item in items:
        needs_pob_reason = any(marker in reason for reason in _skipif_reasons(item) for marker in _POB_REASON_MARKERS)
        if needs_pob_reason or item.get_closest_marker("pob") is not None:
            item.add_marker(skip)


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    if pob_disabled():
        terminalreporter.write_line(f"{ENV_VAR}: PoB launches attempted in this session: {launch_attempts()}")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """A run under `JUNKROAN_NO_POB` that tried to start PoB even once fails, even if the test swallowed the error."""

    if pob_disabled() and launch_attempts() > 0 and session.exitstatus == 0:
        session.exitstatus = 1


def pytest_runtest_setup(item: pytest.Item) -> None:
    while SRC_DIR in sys.path:
        sys.path.remove(SRC_DIR)
    sys.path.insert(0, SRC_DIR)


@pytest.fixture(autouse=True)
def _gem_corpus_caches_never_outlive_a_patch():
    """Tests patch `junkroan.search.hypothesis.active_gems` (e.g. to `{}` in `tests/test_construction_rig.py` and
    `tests/loop_fakes.py`). `config_rules` keeps two `lru_cache` wrappers over it; filled during such a patch they
    would keep the patched corpus for every later test in the process (CI: `test_picks_memo` read an empty corpus
    after `test_flask_pipeline::test_construction_only_skips_the_step`). Cleared after each test; rebuilding them
    is a dict copy of the cached corpus."""

    yield
    from junkroan.optimizer import config_rules

    config_rules._active_gem_records.cache_clear()
    config_rules._active_gem_names.cache_clear()
    from junkroan.search import skeleton

    skeleton._corpse_pool_cap_bonus_nodes.cache_clear()
