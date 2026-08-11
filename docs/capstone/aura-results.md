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

## AF-HIGH-001

### Route

Classifier result: `HIGH`

Router result: `aura-high-v1`

AURA route:

Planner -> Muhammad plan approval -> Implementer -> Reviewer -> Tester -> Muhammad final approval -> Project Manager -> terminal readiness

Human checkpoints: `2`

The HIGH route retained Planner, both human approval checkpoints, Tester, and Project Manager because the scenario touched evaluation and MCP/governance-sensitive paths.

### Outcome

Result: `PASS`

Quality score: `16/16`

| Dimension | Score |
|---|---:|
| Outcome Accuracy | 4/4 |
| Route Appropriateness | 4/4 |
| Governance & Approval Fidelity | 4/4 |
| Evidence & Readiness Quality | 4/4 |

The disposable worktree changed only `eval/test_policy.py`. The final diff added a direct policy test proving storage and retrieval MCP allow-list role keys stay synchronized in both directions. No allow-list grant, governance policy, holdout, production, CI, auth, database, or router file changed.

### Deterministic Gates

| Gate | Result |
|---|---|
| Approved path scope | PASS |
| Reclassified observed diff | HIGH |
| Escalation required | No |
| `git diff --check` | PASS |
| Credential-pattern scan | No matches |
| Policy tests | 17 passed |
| MCP runtime test | 1 passed |
| Holdout checksum | Unchanged |

### Metrics

Successful-route metrics only:

| Metric | Control HIGH | AURA HIGH | Difference |
|---|---:|---:|---:|
| Quality score | 15/16 PASS | 16/16 PASS | +1 point |
| Model invocations | 5 | 5 | 0 |
| Successful-route cost | $1.1753241 | $1.1061042 | -$0.0692199 (-5.89%) |
| Measured model duration | 248,666 ms | 158,510 ms | -90,156 ms (-36.26%) |
| Human checkpoints | 2 | 2 | 0 |
| Tool events | 28 | 23 | -5 (-17.86%) |
| Authorization denials | 0 | 0 | 0 |

Per-role cost:

| Role | Cost |
|---|---:|
| Planner | $0.3386442 |
| Implementer | $0.2415507 |
| Reviewer | $0.2109459 |
| Tester | $0.1809213 |
| Project Manager | $0.1340421 |

Infrastructure failure cost kept separate:

| Item | Cost |
|---|---:|
| AURA HIGH model-role infrastructure failures | $0 |

Project Manager disclosure:

The Project Manager stage used the simulated course `task_tracker`. No real external ticket was updated.

### Interpretation

Measured HIGH preserved the full governance path for a sensitive evaluation/MCP-policy scenario while still improving outcome score, cost, duration, and tool-event count relative to the pre-AURA fixed-route control. Unlike LOW and MEDIUM, AURA did not remove Planner, human approvals, Tester, or Project Manager for HIGH; the improvement came from deterministic route selection, narrower role prompts, bounded scope, and focused deterministic gates.

## LOW/MEDIUM/HIGH Adaptive Comparison

### Summary Table

| Scenario | Tier | Result Type | AURA Route | Quality Score | Cost | Model Invocations | Model Duration | Human Checkpoints | Tool Events | Denials |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| AF-LOW-001 | LOW | Documentation checklist | `aura-low-v1` | 16/16 PASS | $0.3377550 | 2 | 45,969 ms | 0 | 5 | 0 |
| AF-MEDIUM-001 | MEDIUM | Focused regression test | `aura-medium-v1` | 16/16 PASS | $0.7300815 | 3 | 109,502 ms | 1 | 9 | 0 |
| AF-HIGH-001 | HIGH | Governance policy test | `aura-high-v1` | 16/16 PASS | $1.1061042 | 5 | 158,510 ms | 2 | 23 | 0 |

### Aggregate Comparison To Control

| Metric | Control Total | AURA Total | Difference |
|---|---:|---:|---:|
| Quality score | 44/48 | 48/48 | +4 points |
| Successful-route cost | $2.6912478 | $2.1739407 | -$0.5173071 (-19.22%) |
| Model invocations | 15 | 10 | -5 (-33.33%) |
| Measured model duration | 531,394 ms | 313,981 ms | -217,413 ms (-40.91%) |
| Human checkpoints | 6 | 3 | -3 (-50.00%) |
| Tool events | 46 | 37 | -9 (-19.57%) |
| Authorization denials | 0 | 0 | 0 |

### Findings

1. LOW received the largest autonomy gain. AURA removed Planner, Tester model, Project Manager, and both human checkpoints while improving the measured quality score from 14/16 to 16/16.

2. MEDIUM kept implementation, review, testing, and final approval, but removed Planner, plan approval, and Project Manager. This matched the bounded executable/test risk better than the fixed pre-AURA route.

3. HIGH kept the full governance route. That is the expected conservative behavior for `eval/**` and MCP/governance-sensitive paths. The adaptive router did not under-serve the sensitive scenario.

4. The measured comparison supports the AURA Forge thesis for these three representative scenarios: deterministic routing reduced overhead where risk allowed it, preserved controls where risk required them, and improved total measured quality without any authorization denials, push, merge, production contact, or holdout modification.

5. The evidence remains bounded to these three scenarios. It does not prove safety for every future HIGH class such as deployment, auth, database migration, or production configuration changes; those would need their own scenario evidence and deterministic gates.

Terminal artifact paths:

- `.eval-artifacts/capstone/aura-runs/AF-LOW-001/final-successful-route-metrics.json`
- `.eval-artifacts/capstone/aura-runs/AF-LOW-001/final-quality-score.json`
- `.eval-artifacts/capstone/aura-runs/AF-MEDIUM-001/final-successful-route-metrics.json`
- `.eval-artifacts/capstone/aura-runs/AF-MEDIUM-001/final-quality-score.json`
- `.eval-artifacts/capstone/aura-runs/AF-HIGH-001/final-successful-route-metrics.json`
- `.eval-artifacts/capstone/aura-runs/AF-HIGH-001/final-quality-score.json`
- `.eval-artifacts/capstone/aura-runs/AF-HIGH-001/terminal-aura-summary.json`
