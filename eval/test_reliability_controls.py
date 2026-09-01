"""Behavior checks for deterministic timeout, retry, and budget enforcement."""

from reliability_controls import ExecutionEvidence, ExecutionLimits, evaluate_execution_limits


LIMITS = ExecutionLimits(
    timeout_seconds=600,
    max_attempts=2,
    max_cost_usd=1.50,
    retryable_failures=("provider_timeout", "temporary_tool_failure"),
)


def test_retryable_failure_allows_one_bounded_retry():
    decision = evaluate_execution_limits(
        LIMITS,
        ExecutionEvidence(
            attempt_number=1,
            elapsed_seconds=120,
            cost_usd=0.40,
            outcome="provider_timeout",
        ),
    )

    assert decision.status == "RETRY_ALLOWED"
    assert decision.retry_allowed is True
    assert decision.next_attempt == 2


def test_retry_limit_stops_a_third_attempt():
    decision = evaluate_execution_limits(
        LIMITS,
        ExecutionEvidence(
            attempt_number=2,
            elapsed_seconds=240,
            cost_usd=0.80,
            outcome="provider_timeout",
        ),
    )

    assert decision.status == "RETRY_LIMIT_REACHED"
    assert decision.retry_allowed is False
    assert decision.next_attempt is None


def test_timeout_stops_execution_even_when_failure_is_retryable():
    decision = evaluate_execution_limits(
        LIMITS,
        ExecutionEvidence(
            attempt_number=1,
            elapsed_seconds=600,
            cost_usd=0.40,
            outcome="provider_timeout",
        ),
    )

    assert decision.status == "TIMEOUT_EXCEEDED"
    assert decision.retry_allowed is False


def test_budget_stops_execution_even_when_failure_is_retryable():
    decision = evaluate_execution_limits(
        LIMITS,
        ExecutionEvidence(
            attempt_number=1,
            elapsed_seconds=120,
            cost_usd=1.50,
            outcome="provider_timeout",
        ),
    )

    assert decision.status == "BUDGET_EXCEEDED"
    assert decision.retry_allowed is False


def test_non_retryable_failure_escalates_without_retry():
    decision = evaluate_execution_limits(
        LIMITS,
        ExecutionEvidence(
            attempt_number=1,
            elapsed_seconds=120,
            cost_usd=0.40,
            outcome="policy_denial",
        ),
    )

    assert decision.status == "ESCALATION_REQUIRED"
    assert decision.retry_allowed is False
