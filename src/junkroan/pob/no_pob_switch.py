"""The `JUNKROAN_NO_POB` switch: keeps the quick test suite from starting PoB.

Two uses:

- `pob_disabled()`: `tests/conftest.py` turns the switch on for a quick run (`-m "not pob"`) and, while it is
  on, skips every `pob`-marked test and every test whose `skipif` reason says it needs PoB.
- `guard_pob_launch()`: called at the one place that spawns the real headless PoB worker process
  (`PinnedPoBHeadlessRuntimeAdapter.launch_session`), so a test that slips past every marker still cannot
  start PoB while the switch is on -- it raises instead. Each refusal also bumps a process-wide counter
  (`launch_attempts()`): a mis-marked test fails at once (the raise) AND leaves a number > 0 behind, which
  fails the whole session (`tests/conftest.py`).
"""

from __future__ import annotations

import os

ENV_VAR = "JUNKROAN_NO_POB"

_launch_attempts = 0


def pob_disabled() -> bool:
    """True when the switch is on: `JUNKROAN_NO_POB` set to anything but `""`/`"0"`."""

    return os.environ.get(ENV_VAR, "").strip() not in ("", "0")


def guard_pob_launch() -> None:
    """Raise instead of letting the caller start the real PoB worker process.

    Call this at the top of any function that would spawn it -- currently just
    `PinnedPoBHeadlessRuntimeAdapter.launch_session`.
    """

    if pob_disabled():
        global _launch_attempts
        _launch_attempts += 1
        raise RuntimeError(
            f"{ENV_VAR} is set: refusing to launch the PoB worker process."
        )


def launch_attempts() -> int:
    """How many times `guard_pob_launch` has refused a launch in this process so far."""

    return _launch_attempts


def reset_launch_attempts() -> None:
    """Tests only: start a fresh count."""

    global _launch_attempts
    _launch_attempts = 0


__all__ = [
    "ENV_VAR",
    "guard_pob_launch",
    "launch_attempts",
    "pob_disabled",
    "reset_launch_attempts",
]
