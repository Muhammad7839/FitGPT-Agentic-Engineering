# Timeout, Retry, and Budget Enforcement

## Purpose

The grader reported that timeout, retry, and budget controls were described but not demonstrated. `eval/reliability_controls.py` now makes each decision deterministic and testable from recorded execution evidence.

The control is separate from the frozen `aura-router-v1` measurement. It does not rewrite historical scenario results.

## Public Decision Contract

`evaluate_execution_limits(limits, evidence)` accepts:

- a positive timeout;
- an attempt limit of at least one;
- a positive model-cost limit;
- an explicit retryable-failure allow-list;
- the current attempt number, elapsed seconds, recorded cost, and outcome.

It returns one fail-closed decision:

| Decision | Meaning |
|---|---|
| `COMPLETED` | The attempt succeeded within every limit. |
| `RETRY_ALLOWED` | The failure is allow-listed and another bounded attempt remains. |
| `RETRY_LIMIT_REACHED` | The configured attempt count is exhausted. |
| `TIMEOUT_EXCEEDED` | Elapsed time reached or exceeded the limit. |
| `BUDGET_EXCEEDED` | Recorded cost reached or exceeded the limit. |
| `ESCALATION_REQUIRED` | The failure is not explicitly retryable. |

Timeout and budget checks take precedence over retry permission. A retryable provider failure cannot continue once either boundary is reached.

## Demonstrated Cases

`eval/test_reliability_controls.py` proves:

- one retryable failure can receive one bounded retry;
- a third attempt is denied when `max_attempts` is two;
- timeout stops a retryable failure;
- budget exhaustion stops a retryable failure;
- a policy denial escalates without retry.

Run:

```bash
pytest -q -p no:cacheprovider eval/test_reliability_controls.py
```

The permanent GitHub evaluation gate includes this test.

## Limitation

This is deterministic policy enforcement over recorded attempt evidence. It does not claim that a paid model call was rerun for this revision, and it does not alter the locked historical holdouts.
