"""The search (#16): `junkroan.search.run(options)` is its one entry; the stages live in `junkroan.search.flow`."""

from __future__ import annotations

from typing import Any


def run(*args: Any, **kwargs: Any) -> Any:
    """`junkroan.search.flow.run`: one search, start to end, ranked builds out (imported on call: the package's
    other modules stay light)."""

    from junkroan.search.flow import run as _run

    return _run(*args, **kwargs)
