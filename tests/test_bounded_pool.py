"""`junkroan.bounded_pool.limited_completions`: never more than `workers` items in flight, every item done once."""

from __future__ import annotations

import threading
from concurrent.futures import Future

from junkroan.bounded_pool import limited_completions

ITEMS = [f"build-{n}" for n in range(6)]


class TimedPool:
    """Stands in for a ProcessPoolExecutor: each submitted item finishes `delay` seconds later."""

    def __init__(self, delays: dict[str, float] | None = None, delay: float = 0.03) -> None:
        self.delays = delays or {}
        self.delay = delay
        self.lock = threading.Lock()
        self.live = 0
        self.peak = 0
        self.submitted: list[str] = []

    def submit(self, item: str) -> Future:
        fut: Future = Future()
        with self.lock:
            self.live += 1
            self.peak = max(self.peak, self.live)
            self.submitted.append(item)

        def finish() -> None:
            with self.lock:
                self.live -= 1
            fut.set_result(item)

        threading.Timer(self.delays.get(item, self.delay), finish).start()
        return fut


def test_at_most_workers_in_flight_and_every_item_done_once() -> None:
    pool = TimedPool()
    done = [item for _fut, item in limited_completions(pool.submit, ITEMS, 2, poll=0.01)]
    assert sorted(done) == sorted(ITEMS)
    assert pool.submitted == ITEMS
    assert pool.peak == 2


def test_results_come_in_completion_order() -> None:
    pool = TimedPool(delays={"slow": 0.2, "fast": 0.01})
    done = [item for _fut, item in limited_completions(pool.submit, ["slow", "fast"], 2, poll=0.01)]
    assert done == ["fast", "slow"]


def test_zero_workers_still_runs_one_at_a_time() -> None:
    pool = TimedPool()
    done = [item for _fut, item in limited_completions(pool.submit, ITEMS[:3], 0, poll=0.01)]
    assert sorted(done) == sorted(ITEMS[:3])
    assert pool.peak == 1


def test_future_result_is_the_submitted_work() -> None:
    pool = TimedPool()
    assert {fut.result() for fut, _item in limited_completions(pool.submit, ITEMS, 3, poll=0.01)} == set(ITEMS)
