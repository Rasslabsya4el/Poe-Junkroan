"""`BuildRecord`: one pipeline build in the form the search and the benchmark both write (#16).

A search worker (`junkroan.search.runner.optimize`) and a benchmark row (`scripts/benchmark.py`) used to copy the
fields of a `BuildResult` by hand, each with its own duplicates (`floors_missed` twice, `moves` and `move_rows` the
same list). Both now take this record's `to_json()` and add only their own fields around it.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from junkroan.optimizer.build_result import BuildResult


@dataclass(slots=True)
class BuildRecord:
    final: dict[str, Any]
    optimistic: float | None
    optimistic_stats: dict[str, Any]
    import_code: str
    xml: str
    summary: str
    stages: list[dict[str, Any]] = field(default_factory=list)
    config_reasons: dict[str, str] = field(default_factory=dict)
    audit: list[str] = field(default_factory=list)
    audit_errors: int = 0
    floors_missed: list[str] | None = None
    keystones: list[str] = field(default_factory=list)
    explanation: str = ""
    picks: list[dict] = field(default_factory=list)
    loop_stop: str = ""
    fixed_point_gain: float = 0.0
    fixed_point_note: str = ""
    castability_calls: int = 0
    castability_seconds: float = 0.0
    dropped_moves: list[dict[str, str]] = field(default_factory=list)
    moves: list[dict[str, Any]] = field(default_factory=list)
    pob_calls: dict[str, dict[str, float | int]] = field(default_factory=dict)
    tree_churn: dict[str, float] = field(default_factory=dict)
    ledger_construction_value: float | None = None
    ledger_value_before_final_lanes: float | None = None
    ledger_identity_error: float | None = None

    @classmethod
    def from_result(cls, res: BuildResult) -> BuildRecord:
        return cls(
            final=res.final_stats, optimistic=res.optimistic_stats.get("CombinedDPS"), optimistic_stats=res.saved_optimistic(),
            import_code=res.import_code, xml=res.xml, summary=res.summary(),
            stages=[{"name": s.name, "seconds": s.seconds, "value": s.score_value, "violation": s.violation, "notes": s.notes} for s in res.stages],
            config_reasons=res.config_reasons, audit=[str(f) for f in res.audit], audit_errors=sum(1 for f in res.audit if f.severity == "error"),
            floors_missed=res.floors_missed, keystones=res.keystones, explanation=res.explanation, picks=res.picks,
            loop_stop=res.loop_stop, fixed_point_gain=res.fixed_point_gain, fixed_point_note=res.fixed_point_note,
            castability_calls=res.castability_calls, castability_seconds=res.castability_seconds,
            dropped_moves=res.dropped_moves, moves=res.moves, pob_calls=res.pob_calls, tree_churn=res.tree_churn,
            ledger_construction_value=res.ledger_construction_value,
            ledger_value_before_final_lanes=res.ledger_value_before_final_lanes,
            ledger_identity_error=res.ledger_identity_error,
        )

    def to_json(self) -> dict[str, Any]:
        """The record as plain data (crosses a process boundary, lands in a JSON file); every field once."""

        return {f.name: getattr(self, f.name) for f in fields(self)}


__all__ = ["BuildRecord"]
