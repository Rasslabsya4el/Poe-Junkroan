"""Shared rules for deciding which finished benchmark rows contribute to medians."""

from __future__ import annotations

from typing import Any

VIOLATION_TOLERANCE = 1e-9
FIXED_POINT_CHECK = "fixed point"


def audit_finding_parts(finding: object) -> tuple[str, str] | None:
    """Return ``(severity, check)`` from the persisted ``Finding.__str__`` form.

    Benchmark results store audit findings as strings, so this deliberately mirrors
    ``Finding.__str__`` rather than depending on a live ``Finding`` instance.
    """

    if not isinstance(finding, str) or not finding.startswith("["):
        return None
    severity_end = finding.find("] ")
    check_end = finding.find(":", severity_end + 2)
    if severity_end < 0 or check_end < 0:
        return None
    return finding[1:severity_end], finding[severity_end + 2:check_end]


def audit_errors(row: dict[str, Any]) -> list[str]:
    """Persisted error findings, preserving old rows that have only a count."""

    audit = row.get("audit")
    if isinstance(audit, list):
        errors = []
        for finding in audit:
            if (parts := audit_finding_parts(finding)) is not None and parts[0] == "error":
                errors.append(finding)
        missing = max(0, int(row.get("audit_errors") or 0) - len(errors))
        return errors + ["[error] unknown: persisted audit error"] * missing
    return ["[error] unknown: persisted audit error"] * int(row.get("audit_errors") or 0)


def non_fixed_point_audit_errors(row: dict[str, Any]) -> list[str]:
    """Error findings other than the stability-only fixed-point finding."""

    return [
        finding
        for finding in audit_errors(row)
        if (parts := audit_finding_parts(finding)) is None or parts[1] != FIXED_POINT_CHECK
    ]


def last_stage_violation(row: dict[str, Any]) -> float:
    """The final recorded objective violation, defaulting old rows to feasible."""

    stages = row.get("stages")
    if not isinstance(stages, list) or not stages or not isinstance(stages[-1], dict):
        return 0.0
    violation = stages[-1].get("violation", 0.0)
    return float(violation) if isinstance(violation, (int, float)) else float("inf")


def counted_row(row: dict[str, Any]) -> bool:
    """Whether a benchmark row contributes to its reference median.

    A delivered build remains usable when the only audit error says its final
    improvement pass found more than 1%; that is a stability finding, not an
    infeasibility or a logical error in the build itself.
    """

    return bool(row.get("ok")) and last_stage_violation(row) <= VIOLATION_TOLERANCE and not non_fixed_point_audit_errors(row)


def not_at_fixed_point(row: dict[str, Any]) -> bool:
    """Whether the persisted row says a further pass gained strictly over 1%.

    New rows retain the measured gain, which is authoritative at the exact 1%
    boundary. Older rows without it can still be summarized from the audit
    finding, whose error severity is emitted only for gains above 1%.
    """

    gain = row.get("fixed_point_gain")
    if isinstance(gain, (int, float)):
        return gain > 0.01
    return any(
        audit_finding_parts(finding) == ("error", FIXED_POINT_CHECK)
        for finding in row.get("audit") or []
    )


__all__ = [
    "FIXED_POINT_CHECK",
    "VIOLATION_TOLERANCE",
    "audit_errors",
    "audit_finding_parts",
    "counted_row",
    "last_stage_violation",
    "non_fixed_point_audit_errors",
    "not_at_fixed_point",
]
