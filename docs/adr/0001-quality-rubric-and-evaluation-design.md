# ADR 0001: Quality Rubric And Evaluation Design

## Context

The capstone needed comparable evidence across PRE-AURA control runs and AURA adaptive-route runs. The measured comparison used `docs/capstone/quality-rubric.md`, control evidence committed through `75dd1f8`, and AURA evidence committed through `6b52ecb`.

## Decision

Use a 16-point rubric with four dimensions: Outcome Accuracy, Route Appropriateness, Governance & Approval Fidelity, and Evidence & Readiness Quality.

## Rejected Alternatives

- Single pass/fail result only. Rejected because LOW control produced correct output but was over-served; this needed a route-quality dimension.
- Cost-only comparison. Rejected because HIGH intentionally preserved governance and should not be optimized only for cost.

## Evidence

- PRE-AURA LOW: `14/16 FAIL`, cost `$0.6066006`, route appropriateness `2/4`.
- AURA LOW: `16/16 PASS`, cost `$0.3377550`.
- AURA aggregate: quality improved from `44/48` to `48/48`.

## Consequences

The rubric supports measured route-quality claims without projecting company-wide savings.

## Open Risks

The rubric is calibrated to three representative scenarios, not every possible future HIGH production change.
