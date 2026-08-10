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
