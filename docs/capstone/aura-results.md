# AURA Forge Adaptive-Route Results

This document records measured post-AURA adaptive-route results. Scenario implementations remain in disposable worktrees and are not merged into `capstone/aura-forge`.

## Measurement Base

Frozen adaptive-router commit: `c844db1b457712d4c68c9353c49e8bd9fd2121a1`

Router version: `aura-router-v1`

Classifier version: `aura-risk-v1`

## AF-LOW-001

### Route

Classifier result: `LOW`

Router result: `aura-low-v1`

AURA route:

Implementer -> Reviewer -> deterministic verification -> terminal readiness

Human checkpoints: `0`

Planner, Tester model, and Project Manager were not used.

### Outcome

Result: `PASS`

Quality score: `16/16`

| Dimension | Score |
|---|---:|
| Outcome Accuracy | 4/4 |
| Route Appropriateness | 4/4 |
| Governance & Approval Fidelity | 4/4 |
| Evidence & Readiness Quality | 4/4 |

The disposable worktree changed only `docs/features/accessibility.md`. The final diff added concise Large Text Mode and High-Contrast Mode verification checklists supported by existing documented behavior.

### Deterministic Gates

| Gate | Result |
|---|---|
| Approved path scope | PASS |
| Reclassified observed diff | LOW |
| Escalation required | No |
| `git diff --check` | PASS |
| Credential-pattern scan | No matches |
| Scenario-specific documentation checks | PASS |

### Metrics

Successful-route metrics only:

| Metric | Control LOW | AURA LOW | Difference |
|---|---:|---:|---:|
| Quality score | 14/16 FAIL | 16/16 PASS | +2 points |
| Model invocations | 5 | 2 | -3 (-60.00%) |
| Successful-route cost | $0.6066006 | $0.3377550 | -$0.2688456 (-44.32%) |
| Measured model duration | 89,398 ms | 45,969 ms | -43,429 ms (-48.58%) |
| Human checkpoints | 2 | 0 | -2 (-100.00%) |
| Tool events | 8 | 5 | -3 (-37.50%) |
| Authorization denials | 0 | 0 | 0 |

Infrastructure precheck cost kept separate:

| Item | Cost |
|---|---:|
| AURA LOW auth-check-001 | $0.2047476 |

### Interpretation

Measured LOW improved route appropriateness while retaining outcome, governance, and evidence quality. This supports the adaptive-autonomy thesis for documentation-only changes: the route removed unnecessary Planner, Tester model, Project Manager, and human-checkpoint overhead without reducing measured quality.

## AF-MEDIUM-001

### Route

Classifier result: `MEDIUM`

Router result: `aura-medium-v1`

AURA route:

Implementer -> Reviewer -> Tester -> Muhammad final approval -> terminal readiness

Human checkpoints: `1`

Planner, plan approval, and Project Manager were not used.

### Outcome

Result: `PASS`

Quality score: `16/16`

| Dimension | Score |
|---|---:|
| Outcome Accuracy | 4/4 |
| Route Appropriateness | 4/4 |
| Governance & Approval Fidelity | 4/4 |
| Evidence & Readiness Quality | 4/4 |

The disposable worktree changed only `web/src/utils/feedbackPrompts.test.js`. `web/src/utils/feedbackPrompts.js` was read and preserved because the denominator invariant already existed: `recordPromptShown` is the only writer of `totalShown`, while `recordPromptDismissed` updates only dismissal counters.

### Deterministic Gates

| Gate | Result |
|---|---|
| Approved path scope | PASS |
| Reclassified observed diff | MEDIUM |
| Escalation required | No |
| `git diff --check` | PASS |
| Credential-pattern scan | No matches |
| Focused Jest | 21 passed |

### Metrics

Successful-route metrics only:

| Metric | Control MEDIUM | AURA MEDIUM | Difference |
|---|---:|---:|---:|
| Quality score | 15/16 PASS | 16/16 PASS | +1 point |
| Model invocations | 5 | 3 | -2 (-40.00%) |
| Successful-route cost | $0.9093231 | $0.7300815 | -$0.1792416 (-19.71%) |
| Measured model duration | 193,330 ms | 109,502 ms | -83,828 ms (-43.36%) |
| Human checkpoints | 2 | 1 | -1 (-50.00%) |
| Tool events | 10 | 9 | -1 (-10.00%) |
| Authorization denials | 0 | 0 | 0 |

Infrastructure failure cost kept separate:

| Item | Cost |
|---|---:|
| AURA MEDIUM Tester session-limit attempt | $0 |

### Interpretation

Measured MEDIUM reduced overhead while preserving implementation judgment, independent review, focused real test evidence, and final human approval. The route avoided planning and Project Manager overhead for a bounded executable/test scenario, while retaining the controls needed to prove the existing source invariant and regression coverage.
