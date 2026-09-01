"""Deterministic execution-limit decisions for AURA Forge evidence runs.

This module does not invoke an agent or sleep. It evaluates recorded attempt
evidence against explicit limits so timeout, retry, and cost behavior is
machine-checkable and fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionLimits:
    timeout_seconds: float
    max_attempts: int
    max_cost_usd: float
    retryable_failures: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.max_cost_usd <= 0:
            raise ValueError("max_cost_usd must be positive")


@dataclass(frozen=True)
class ExecutionEvidence:
    attempt_number: int
    elapsed_seconds: float
    cost_usd: float
    outcome: str

    def __post_init__(self) -> None:
        if self.attempt_number < 1:
            raise ValueError("attempt_number must be at least 1")
        if self.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds must not be negative")
        if self.cost_usd < 0:
            raise ValueError("cost_usd must not be negative")
        if not self.outcome.strip():
            raise ValueError("outcome must not be empty")


@dataclass(frozen=True)
class ExecutionDecision:
    status: str
    retry_allowed: bool
    next_attempt: int | None
    reason: str


def evaluate_execution_limits(
    limits: ExecutionLimits,
    evidence: ExecutionEvidence,
) -> ExecutionDecision:
    """Return the fail-closed decision for one recorded execution attempt."""
    if evidence.elapsed_seconds >= limits.timeout_seconds:
        return ExecutionDecision(
            status="TIMEOUT_EXCEEDED",
            retry_allowed=False,
            next_attempt=None,
            reason="Elapsed execution time reached or exceeded the configured timeout.",
        )

    if evidence.cost_usd >= limits.max_cost_usd:
        return ExecutionDecision(
            status="BUDGET_EXCEEDED",
            retry_allowed=False,
            next_attempt=None,
            reason="Recorded model cost reached or exceeded the configured budget.",
        )

    if evidence.outcome == "success":
        return ExecutionDecision(
            status="COMPLETED",
            retry_allowed=False,
            next_attempt=None,
            reason="The attempt completed successfully within all configured limits.",
        )

    if evidence.outcome not in limits.retryable_failures:
        return ExecutionDecision(
            status="ESCALATION_REQUIRED",
            retry_allowed=False,
            next_attempt=None,
            reason="The failure is not on the explicit retry allow-list.",
        )

    if evidence.attempt_number >= limits.max_attempts:
        return ExecutionDecision(
            status="RETRY_LIMIT_REACHED",
            retry_allowed=False,
            next_attempt=None,
            reason="The configured attempt limit has been reached.",
        )

    return ExecutionDecision(
        status="RETRY_ALLOWED",
        retry_allowed=True,
        next_attempt=evidence.attempt_number + 1,
        reason="The failure is retryable and timeout, cost, and attempt limits remain.",
    )
