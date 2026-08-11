# Right-Tool Decision Matrix

This matrix records the AURA Forge rule for choosing deterministic code, an agentic role, or Muhammad/human approval. It is intended to be reusable by a new maintainer.

| Workflow step | Default tool | Why | Evidence |
|---|---|---|---|
| Risk tier classification | Deterministic code | Path and governance sensitivity are stable, inspectable facts. A model would add cost and variability. | `eval/risk_classifier.py`, `eval/test_risk_classifier.py`, `docs/capstone/risk-classifier.md` |
| Route selection | Deterministic code | A route is a policy decision from tier and triggered rules. It should be reproducible. | `eval/adaptive_router.py`, `eval/test_adaptive_router.py`, `docs/capstone/adaptive-routing.md` |
| LOW non-executable doc change | Bounded agent plus deterministic checks | Lightweight review is enough when no executable or governance-sensitive path changes. | `docs/capstone/aura-results.md`, `docs/capstone/control-vs-aura-impact.md` |
| MEDIUM executable app/test change | Implementer, Reviewer, Tester | Engineering judgment is useful, but Planner and Project Manager overhead was not justified for the measured bounded utility/test case. | `.eval-artifacts/capstone/aura-runs/AF-MEDIUM-001/`, `docs/capstone/aura-results.md` |
| HIGH governance/eval/tool change | Planner, approval, Implementer, Reviewer, Tester, approval, Project Manager | Sensitive paths need plan review, explicit approvals, policy checks, and full governance. | `.eval-artifacts/capstone/aura-runs/AF-HIGH-001/`, `docs/capstone/aura-results.md` |
| Policy and MCP runtime checks | Deterministic tests | Authorization and import/runtime boundaries should fail predictably. | `eval/test_policy.py`, `eval/test_mcp_runtime.py`, `eval/test_coursetools_runtime.py` |
| CI integrity | Deterministic checker | The workflow guardrails are structured YAML and should not rely on a model. | `scripts/check-pipeline-integrity.py`, `eval/test_pipeline_integrity.py` |
| Advisory code review | Optional advisory model | Useful for human review, but unavailable model credentials must not block permanent gates. | `scripts/run-advisory-review.py`, `.github/workflows/ci.yml` |
| Final approval for MEDIUM/HIGH | Human | Risk-sensitive or executable changes still require human accountability. | `.eval-artifacts/capstone/aura-runs/*/final-approval-001/` |
| Change Passport | Deterministic evidence aggregation | Evidence must be read from producers, not summarized from memory. | `scripts/build-change-passport.py`, `eval/test_change_passport.py` |
| Config/docs consistency check | Deterministic code | The `DATABASE_URL` surfaces are stable text/config facts. | `scripts/check-config-docs-consistency.py`, `docs/capstone/deterministic-conversion.md` |

## Decision Rule

Use deterministic code when the input is stable, machine-readable, and policy-like. Use agentic roles when judgment, synthesis, or implementation tradeoffs matter. Use human approval when the result changes sensitive governance, production-adjacent behavior, or final readiness for a higher-risk route.

## Quantitative Conversion Evidence

The converted config/docs consistency check runs deterministically with `$0` model cost and a measured local runtime around `0.156 ms`. The original historical auditor path required an agentic documentation review and model cost. The deterministic replacement is cheaper, easier to audit, and more repeatable for this narrow factual check.
