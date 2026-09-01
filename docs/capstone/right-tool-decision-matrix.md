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
| Governed document retrieval | Deterministic semantic-vector search plus policy enforcement | The synthetic corpus, similarity rules, classification ceilings, and citation contract must be reproducible without an external model. | `mcp-servers/retrieval/server.py`, `eval/test_retrieval_behavior.py`, `docs/capstone/retrieval-tool-evidence.md` |
| Retry, timeout, and cost decision | Deterministic code | Continuation authority is a policy boundary. Identical attempt evidence must produce the same stop, retry, or escalation result. | `eval/reliability_controls.py`, `eval/test_reliability_controls.py`, `docs/capstone/reliability-controls.md` |
| Offline grader verification | Deterministic container script | Reproduction should require no model credential or network access and should isolate parallel runs. | `scripts/run-offline-governance-verification.sh`, `eval/test_sandbox_contract.py` |

## Decision Rule

Use deterministic code when the input is stable, machine-readable, and policy-like. Use agentic roles when judgment, synthesis, or implementation tradeoffs matter. Use human approval when the result changes sensitive governance, production-adjacent behavior, or final readiness for a higher-risk route.

## Reusable Decision Questions

Use deterministic code when:

- Are the rules stable enough to encode directly?
- Is the result objectively verifiable from files, paths, JSON, tests, or CI output?
- Should repeated identical inputs produce identical output?
- Would model judgment add little value but add cost or variability?

Use an agentic role when:

- Does the task require interpretation, synthesis, implementation judgment, or tradeoff analysis?
- Is the solution path not mechanically fixed?
- Is bounded tool use useful, with a reviewer/tester able to check the result?
- Can the role be scoped to only the files, tests, or evidence it needs?

Use a human when:

- Is there irreversible or sensitive approval?
- Does accountability need to stay with Muhammad or a maintainer?
- Does policy require explicit plan or final approval?
- Would delegating the decision blur responsibility for governance, readiness, or submission?

## AURA Stage Mapping

| AURA stage | Tool type | Why | Evidence |
|---|---|---|---|
| Changed-path normalization | Deterministic | Path handling must be repeatable and fail closed on malformed input. | `eval/risk_classifier.py`, `eval/test_risk_classifier.py` |
| Risk tier classification | Deterministic | HIGH-sensitive paths must outrank LOW labels every time. | `docs/capstone/risk-classifier.md` |
| Route plan selection | Deterministic | Route IDs and role lists are policy outputs. | `eval/adaptive_router.py`, `eval/test_adaptive_router.py` |
| Mid-run observed-path escalation | Deterministic | A LOW plan observing HIGH-sensitive paths must output `ESCALATION REQUIRED`, not silently continue. | `eval/test_adaptive_router.py::test_low_route_observing_high_sensitive_path_fails_closed_with_escalation` |
| LOW implementation | Agentic | The document still needs semantic editing and independent review. | `docs/capstone/aura-results.md` |
| MEDIUM implementation and testing | Agentic plus deterministic tests | Executable/test work needs implementation judgment and focused verification. | `.eval-artifacts/capstone/aura-runs/AF-MEDIUM-001/`, `docs/capstone/aura-results.md` |
| HIGH plan/final approval | Human | Sensitive governance work requires accountability before implementation and before PM closure. | `.eval-artifacts/capstone/aura-runs/AF-HIGH-001/` |
| Policy/MCP enforcement | Deterministic | Authorization and allow-list behavior must be machine-checkable. | `eval/test_policy.py`, `eval/test_mcp_runtime.py`, `docs/capstone/governance-overreach-demo.md` |
| Change Passport | Deterministic | Readiness fields must come from producers and hashes, not from memory. | `scripts/build-change-passport.py`, `eval/test_change_passport.py` |
| Semantic retrieval ranking | Deterministic | Search results, ceilings, and citations must be reproducible and policy-testable. | `mcp-servers/retrieval/server.py`, `eval/test_retrieval_behavior.py` |
| Attempt continuation decision | Deterministic | Timeout, cost, retry count, and failure class are explicit evidence fields. | `eval/reliability_controls.py`, `eval/test_reliability_controls.py` |

## Quantitative Conversion Evidence

The converted config/docs consistency check runs deterministically with `$0` model cost and a measured local runtime around `0.156 ms`. The original historical auditor path required an agentic documentation review and model cost. The deterministic replacement is cheaper, easier to audit, and more repeatable for this narrow factual check.
