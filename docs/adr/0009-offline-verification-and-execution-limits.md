# ADR 0009: Offline Verification And Execution Limits

## Context

Canvas feedback asked for stronger network/parallel-session boundaries and demonstrated timeout, retry, and budget enforcement. Historical AURA measurements and holdouts must remain unchanged.

## Decision

Add two independent deterministic controls:

- an offline Docker verifier with network disabled, read-only root/workspace, no credentials, dropped capabilities, bounded resources, tmpfs state, and unique container naming;
- an execution-limit decision function that evaluates recorded attempt count, elapsed time, cost, and failure class.

## Rejected Alternatives

- Rerunning paid historical workflows. Rejected because it would spend model budget and change the evidence envelope without user approval.
- Modifying frozen `aura-router-v1`. Rejected because the measured route must remain frozen.
- Document-only reliability claims. Rejected because the grader requested demonstrated enforcement.

## Evidence

- `eval/test_sandbox_contract.py` checks the container boundary contract.
- `eval/test_reliability_controls.py` covers retry allowance, retry exhaustion, timeout, budget stop, and escalation.
- `.github/workflows/ci.yml` includes both test families in permanent gates.

## Consequences

Graders can verify deterministic governance without model credentials or egress. Attempt continuation decisions become reproducible and fail closed.

## Open Risks

Docker Desktop must be running for the offline command. The fresh offline run passed `32` tests. Historical model-backed runs used bridge networking and remain labeled with that limitation.
