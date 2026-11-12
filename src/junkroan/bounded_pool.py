"""A process pool's map with at most `workers` items in flight, results in completion order.

The scripts whose pool runs one build or skeleton per worker (`search.py`, `replay_bench.py`,
`run_bundles.py`, `repair_calibrate.py`) submit through this instead of submitting every item up
front, so an item is handed to the pool only when a worker is free for it.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, wait
from typing import TypeVar

T = TypeVar("T")


def limited_completions(submit: Callable[[T], Future], items: Iterable[T], workers: int, *,
                        poll: float = 5.0) -> Iterator[tuple[Future, T]]:
    """Submit `items` in order, at most `max(1, workers)` in flight; yield `(future, item)` as each finishes.

    Completion order, like `as_completed`. `poll` bounds each wait so a caller's generator stays responsive.
    """

    limit = max(1, workers)
    pending = list(items)
    running: dict[Future, T] = {}
    while pending or running:
        while pending and len(running) < limit:
            item = pending.pop(0)
            running[submit(item)] = item
        for fut in wait(list(running), timeout=poll, return_when=FIRST_COMPLETED).done:
            yield fut, running.pop(fut)


__all__ = ["limited_completions"]
