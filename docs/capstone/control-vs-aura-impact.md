# Control vs AURA Forge Impact

This document records measured impact for the three representative capstone scenarios. It uses only local PRE-AURA control evidence and post-AURA adaptive-route evidence already recorded in `docs/capstone/control-baseline-comparison.md` and `docs/capstone/aura-results.md`.

No company-wide, production, or future-scenario savings are inferred from these three measurements.

## Measurement Scope

| Label | Meaning |
|---|---|
| MEASURED | Directly observed in the three local capstone scenario runs. |
| PROJECTED | Not used for savings claims in this document. |

All values below are `MEASURED` unless explicitly labeled otherwise.

## Scenario Impact

### AF-LOW-001

| Metric | PRE-AURA Control | AURA | Change |
|---|---:|---:|---:|
| Quality score | 14/16 FAIL | 16/16 PASS | +2 points |
| Route appropriateness | 2/4 | 4/4 | +2 points |
| Successful-route cost | $0.6066006 | $0.3377550 | -$0.2688456 (-44.32%) |
| Model roles | 5 | 2 | -3 (-60.00%) |
| Human checkpoints | 2 | 0 | -2 (-100.00%) |

LOW shows the clearest adaptive-autonomy gain. The documentation-only change retained review and deterministic verification while removing unnecessary Planner, Tester model, Project Manager, and human-checkpoint overhead.

### AF-MEDIUM-001

| Metric | PRE-AURA Control | AURA | Change |
|---|---:|---:|---:|
| Quality score | 15/16 PASS | 16/16 PASS | +1 point |
| Successful-route cost | $0.9093231 | $0.7300815 | -$0.1792416 (-19.71%) |
| Model roles | 5 | 3 | -2 (-40.00%) |
| Human checkpoints | 2 | 1 | -1 (-50.00%) |

MEDIUM shows a smaller but still meaningful reduction. AURA preserved implementation, independent review, focused test evidence, and final human approval while removing Planner, plan approval, and Project Manager for a bounded utility/test change.

The provider session-limit failure before one MEDIUM Tester attempt remains classified separately as infrastructure failure and is not counted as successful-route cost.

### AF-HIGH-001

| Metric | PRE-AURA Control | AURA | Change |
|---|---:|---:|---:|
| Quality score | 15/16 PASS | 16/16 PASS | +1 point |
| Successful-route cost | $1.1753241 | $1.1061042 | -$0.0692199 (-5.89%) |
| Model roles | 5 | 5 | 0 (0.00%) |
| Human checkpoints | 2 | 2 | 0 (0.00%) |

HIGH deliberately preserved full governance because the scenario touched evaluation and MCP/governance-sensitive paths. AURA did not optimize away Planner, human approvals, Tester, or Project Manager for this sensitive scenario.

## Aggregate Measured Impact

| Metric | PRE-AURA Total | AURA Total | Change |
|---|---:|---:|---:|
| Quality score | 44/48 | 48/48 | +4 points |
| Successful-route cost | $2.6912478 | $2.1739407 | -$0.5173071 (-19.22%) |
| Model roles | 15 | 10 | -5 (-33.33%) |
| Human checkpoints | 6 | 3 | -3 (-50.00%) |

## Thesis Assessment

The adaptive-autonomy thesis is supported by the measured capstone evidence.

AURA Forge reduced route weight when deterministic risk classification showed lower risk, while retaining strong governance for HIGH. LOW saw the largest reduction in agentic and human overhead while quality improved. MEDIUM saw a smaller reduction while preserving engineering rigor. HIGH saw little cost reduction because strong governance was intentionally retained.

This evidence is bounded to the three representative scenarios. It does not project savings across all FitGPT work, all LaunchCode work, or future production operations.
