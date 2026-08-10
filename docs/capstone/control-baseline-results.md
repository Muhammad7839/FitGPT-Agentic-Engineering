# AURA Forge Fixed-Route Control Baseline Results

This file records sanitized, tracked evidence summaries for measured PRE-AURA fixed-route control runs. Disposable scenario implementations remain in isolated worktrees and are not merged into `capstone/aura-forge`.

## AF-LOW-001

Scenario request:

Update `docs/features/accessibility.md` to add concise verification checklists for Large Text Mode and High-Contrast Mode using behavior already described in the document. Do not change application code, tests, governance documents, agent definitions, CI, MCP files, or evaluation files.

Fixed route used:

Planner -> Muhammad plan approval -> Implementer -> Reviewer -> Tester -> Muhammad final approval -> Project Manager

Final rubric score:

| Dimension | Score |
|---|---:|
| Outcome Accuracy | 4/4 |
| Route Appropriateness | 2/4 |
| Governance & Approval Fidelity | 4/4 |
| Evidence & Readiness Quality | 4/4 |
| Total | 14/16 |

Rubric result: FAIL.

Route Appropriateness scored 2 because the PRE-AURA fixed route sent a LOW, documentation-only checklist update through Planner, Implementer, Reviewer, Tester, two human checkpoints, and Project Manager. The result was correct and governed, but the route was materially heavier than the scenario required.

AF-LOW-001 demonstrates that the fixed pre-AURA workflow can produce a correct and governed LOW-risk result, but it over-serves the change with unnecessary agentic and human-review overhead.

Successful-route quantitative metrics:

| Metric | Value |
|---|---:|
| Model invocations | 5 |
| Successful-route cost | $0.6066006 |
| Measured model duration | 89,398 ms |
| API duration | 89,282 ms |
| Turns | 13 |
| Tool events | 8 |
| Authorization denials | 0 |
| Human checkpoints | 2 |

Per-role cost:

| Role | Cost |
|---|---:|
| Planner | $0.140052 |
| Implementer | $0.1269798 |
| Reviewer | $0.1092114 |
| Tester | $0.1219572 |
| Project Manager | $0.1084002 |

Infrastructure-failure costs kept separate from the successful route:

| Attempt | Cost |
|---|---:|
| MCP-blocked Planner | $0.108051 |
| Local-MCP Implementer retry-001 | $0.087951 |
| Other authentication failures | $0 |

Project Manager disclosure:

The Project Manager stage used the simulated course `task_tracker`. No real external ticket was updated.

Final result:

- The disposable AF-LOW implementation changed only `docs/features/accessibility.md`.
- The implementation added 15 documentation-only insertions.
- `git diff --check`, approved-file scope validation, credential-pattern scan, Reviewer, and Tester all passed.
- No scenario implementation was merged into `capstone/aura-forge`.

Terminal artifact paths:

- `.eval-artifacts/capstone/control-baseline/AF-LOW-001/final-successful-route-metrics.json`
- `.eval-artifacts/capstone/control-baseline/AF-LOW-001/final-quality-score.json`
- `.eval-artifacts/capstone/control-baseline/AF-LOW-001/terminal-control-summary.json`

## AF-MEDIUM-001

Scenario request:

Add a bounded rule to the feedback prompt utility so dismissed prompts do not increase the engagement rate denominator twice when a prompt was already recorded as shown. Preserve the existing public API and update the focused Jest tests for the feedback prompt utility.

Fixed route used:

Planner -> Muhammad plan approval -> Implementer -> Reviewer -> Tester -> Muhammad final approval -> Project Manager

Final rubric score:

| Dimension | Score |
|---|---:|
| Outcome Accuracy | 4/4 |
| Route Appropriateness | 3/4 |
| Governance & Approval Fidelity | 4/4 |
| Evidence & Readiness Quality | 4/4 |
| Total | 15/16 |

Rubric result: PASS.

Route Appropriateness scored 3 because the PRE-AURA fixed route was defensible for a MEDIUM executable utility/test scenario, but it was still not minimal. The scenario benefited from implementation, review, and focused test evidence; however, the uniform route also required two human checkpoints and Project Manager despite a bounded two-file scope.

AF-MEDIUM-001 demonstrates that the fixed pre-AURA workflow can handle a bounded executable utility/test change correctly and with strong governance evidence, but it still does not scale route weight based on risk.

Successful-route quantitative metrics:

| Metric | Value |
|---|---:|
| Model invocations | 5 |
| Successful-route cost | $0.9093231 |
| Measured model duration | 193,330 ms |
| API duration | 193,209 ms |
| Turns | 15 |
| Tool events | 10 |
| Authorization denials | 0 |
| Human checkpoints | 2 |

Per-role cost:

| Role | Cost |
|---|---:|
| Planner | $0.2017755 |
| Implementer | $0.2830794 |
| Reviewer | $0.1732734 |
| Tester retry | $0.1357572 |
| Project Manager | $0.1154376 |

Infrastructure-failure costs kept separate from the successful route:

| Attempt | Cost |
|---|---:|
| Tester toolchain failure: `react-scripts` unavailable before dependency restoration | $0.1410483 |

Toolchain repair disclosure:

The initial Tester attempt failed before Jest assertions executed because the disposable worktree did not have `web/node_modules` installed. `react-scripts` was already declared in `web/package.json` and `web/package-lock.json`; running `npm ci` from `web/` restored committed lockfile dependencies without changing source, manifest, or lockfile files. The subsequent direct focused Jest run passed: 1 suite passed, 23 tests passed, runtime 0.621 s.

Project Manager disclosure:

The Project Manager stage used the simulated course `task_tracker`. No real external ticket was updated.

Final result:

- The disposable AF-MEDIUM implementation changed only `web/src/utils/feedbackPrompts.test.js`.
- The implementation added 69 focused regression-test insertions.
- `web/src/utils/feedbackPrompts.js` was not modified because the source already kept dismissal tracking separate from `totalShown`.
- `git diff --check`, approved-file scope validation, credential-pattern scan, Reviewer, direct focused Jest, Tester retry, and Project Manager all passed.
- No scenario implementation was merged into `capstone/aura-forge`.

Terminal artifact paths:

- `.eval-artifacts/capstone/control-baseline/AF-MEDIUM-001/final-successful-route-metrics.json`
- `.eval-artifacts/capstone/control-baseline/AF-MEDIUM-001/final-quality-score.json`
- `.eval-artifacts/capstone/control-baseline/AF-MEDIUM-001/terminal-control-summary.json`
