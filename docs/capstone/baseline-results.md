# AURA Forge Pre-AURA Baseline Results

## Baseline Summary

The current pre-AURA workflow was inspected and found to be real but fixed to the historical controlled issue `COURSE-FITGPT-001`. It does not currently provide a safe executable route for the three fresh capstone representative scenarios without adapting the workflow.

Because this milestone forbids implementing the AURA Forge classifier or adaptive routing, no scenario implementation was attempted and no model was invoked. The baseline result is a documented executable-workflow gap.

## Scenario Results

| Scenario | Expected tier | Actual pre-AURA route | Quality score | Cycle time | Review latency | Agent/model invocations | Cost | Human checkpoints | Notable failures | Key observation |
|---|---|---|---|---|---|---:|---|---:|---|---|
| `AF-LOW-001` | `LOW` | Not executed; current route fixed to `COURSE-FITGPT-001` | Not scored | Not available | Not available | 0 | Not reliably measurable | 0 | Workflow-fit gap | A useful doc-only change cannot be run through the current route without adaptation. |
| `AF-MEDIUM-001` | `MEDIUM` | Not executed; current route fixed to `COURSE-FITGPT-001` | Not scored | Not available | Not available | 0 | Not reliably measurable | 0 | Workflow-fit gap | A bounded executable web utility change cannot be run through the current route without adaptation. |
| `AF-HIGH-001` | `HIGH` | Not executed; current route fixed to `COURSE-FITGPT-001` | Not scored | Not available | Not available | 0 | Not reliably measurable | 0 | Workflow-fit gap | A governance-policy test change cannot be run through the current route without adaptation. |

## Interpretation

### 1. Does the pre-AURA workflow treat all three scenarios similarly?

The three scenarios were treated similarly at the baseline-preparation layer: all were blocked before execution because the only verified route is fixed to the old controlled issue. This is workflow-fit evidence, not performance evidence.

### 2. Does LOW appear over-served by the current agentic route?

Not measured. The current route appears structurally heavier than needed for `AF-LOW-001`, but no run occurred, so over-service cannot be claimed as measured.

### 3. Does HIGH receive enough additional governance/human treatment?

Not measured. The current fixed route has human checkpoints and governance boundaries for `COURSE-FITGPT-001`, but it has no scenario-aware high-risk treatment for `AF-HIGH-001`.

### 4. Which measured metric gives the strongest justification for adaptive routing?

The strongest current evidence is not a timing or cost metric. It is the executable-workflow gap: the existing pre-AURA route cannot safely execute fresh low, medium, and high capstone scenarios without adaptation.

### 5. What cannot yet be concluded?

This baseline does not prove cycle-time savings, cost savings, quality improvement, or better review latency from AURA Forge. Those claims require a later executable route and measured runs.

## Evidence Paths

- `.eval-artifacts/capstone/baseline/AF-LOW-001/run-metadata.json`
- `.eval-artifacts/capstone/baseline/AF-MEDIUM-001/run-metadata.json`
- `.eval-artifacts/capstone/baseline/AF-HIGH-001/run-metadata.json`

## Safety Notes

- No production service was contacted.
- No production data was used.
- No secrets or authentication material were stored.
- No locked holdout task was modified or executed.
- No disposable worktree implementation changes were made.
