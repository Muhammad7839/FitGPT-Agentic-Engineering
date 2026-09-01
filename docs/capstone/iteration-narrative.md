# Iteration Narrative

This is the actual AURA Forge engineering story. Infrastructure failures are separated from agent-quality failures.

## 1. Course Workflow Foundation

Problem: the existing course work needed a governed foundation before capstone changes could be measured.

Evidence: Module 3/4 docs, MCP files, policy tests, and sandbox verification.

Decision: preserve the course workflow and build AURA Forge around it in the isolated course repository.

Verification: policy and MCP runtime tests passed in the governed container.

Impact: the capstone started from a reproducible governed baseline.

## 2. Sandbox and MCP Dependency Failures

Problem: the initial Module 4 sandbox path was blocked by Docker/runtime and dependency issues.

Evidence: `docs/capstone/foundation-runtime-repair.md`.

Decision: repair only the course runtime foundation, not production code.

Verification: `eval/test_mcp_runtime.py` and `eval/test_policy.py` passed.

Impact: deterministic governance tests became reproducible.

## 3. MCP/Pydantic Compatibility and FastMCP Failure

Problem: MCP runtime imports and postponed annotations failed under the local environment.

Evidence: foundation repair notes and runtime tests.

Decision: pin and verify the governed runtime with `mcp==1.12.0` and `pydantic==2.9.2`.

Verification: governed Docker runtime checks passed.

Impact: MCP storage, retrieval, and course tools could be tested safely.

## 4. Coursetools Runtime Repair

Problem: role-scoped MCP authorization had to be executable, not just documented.

Evidence: `eval/test_coursetools_runtime.py`, `mcp/coursetools_server.py`.

Decision: verify the real coursetools runtime in the governed sandbox.

Impact: AURA Forge could later prove real overreach denial.

## 5. 0/3 Fresh-Scenario Workflow-Fit Baseline

Problem: the historical fixed route was not a general paved road for fresh representative changes.

Evidence: `docs/capstone/baseline-results.md`.

Decision: define three representative scenarios and a generalized control harness.

Impact: future improvement claims had a fair comparison point.

## 6. PRE-AURA Fixed-Route Control Harness

Problem: every scenario needed the same fixed route before adaptive routing existed.

Evidence: `docs/capstone/pre-aura-control-harness.md`, `docs/capstone/control-baseline-results.md`.

Decision: route LOW, MEDIUM, and HIGH through the same Planner -> approval -> Implementer -> Reviewer -> Tester -> approval -> Project Manager path.

Verification: control scenario evidence and final quality scores.

Impact: LOW was over-served, MEDIUM/HIGH were governed, and baseline cost was measurable.

## 7. LOW Over-Service Discovery

Problem: LOW documentation work received the full route.

Evidence: LOW control result `14/16 FAIL`, route appropriateness `2/4`, cost `$0.6066006`.

Decision: LOW should keep verification but drop unnecessary heavy governance.

Impact: AURA LOW later reached `16/16 PASS` at `$0.3377550`.

## 8. MEDIUM Toolchain Failure and Repair

Problem: MEDIUM testing needed the local JavaScript toolchain repaired.

Evidence: `.eval-artifacts/capstone/aura-runs/AF-MEDIUM-001/toolchain-setup-001/`.

Decision: repair the test environment with `npm ci` evidence, not by weakening tests.

Impact: focused Jest evidence became valid.

## 9. Provider Session Limit Separation

Problem: one Claude provider limit occurred before a tester attempt.

Evidence: AURA MEDIUM evidence and `docs/capstone/control-vs-aura-impact.md`.

Decision: classify it separately as infrastructure failure, not scenario quality.

Impact: successful-route cost stayed honest.

## 10. HIGH Control Result

Problem: governance-sensitive changes needed a full control comparison.

Evidence: HIGH control `15/16 PASS`, cost `$1.1753241`.

Decision: preserve full governance for HIGH unless evidence proved otherwise.

Impact: AURA HIGH intentionally retained full governance.

## 11. Deterministic Risk Classifier

Problem: route selection could not depend on model judgment.

Evidence: `eval/risk_classifier.py`, `eval/test_risk_classifier.py`.

Decision: implement `aura-risk-v1` as deterministic path/rule classification.

Verification: classifier tests passed.

Impact: LOW/MEDIUM/HIGH tier decisions became reproducible.

## 12. Frozen Adaptive Router

Problem: the router could not be tuned after seeing scenario results.

Evidence: frozen router commit `c844db1b457712d4c68c9353c49e8bd9fd2121a1`.

Decision: freeze `aura-router-v1` before post-AURA measurements.

Impact: measured AURA results are credible.

## 13. AURA LOW/MEDIUM/HIGH Measurement

Problem: the thesis needed measured post-AURA runs.

Evidence: `docs/capstone/aura-results.md`, `.eval-artifacts/capstone/aura-runs/*`.

Decision: run all three scenarios through the frozen router.

Impact: aggregate quality improved `44/48 -> 48/48`, cost dropped `19.22%`, roles dropped `33.33%`, human checkpoints dropped `50%`.

## 14. Fresh Governance Overreach Denial

Problem: least privilege needed a real denial, not a claim.

Evidence: `docs/capstone/governance-overreach-demo.md`, `GO-20260811-001`.

Decision: have an `implementer` attempt Project-Manager-only `task_tracker`.

Verification: real authorization denial, `$0` model cost.

Impact: governance became demo-visible.

## 15. Change Passport

Problem: final readiness evidence needed machine-readable aggregation.

Evidence: `scripts/build-change-passport.py`, `eval/test_change_passport.py`, tracked example JSON.

Decision: build a deterministic evidence aggregator, not a new decision subsystem.

Impact: classifier, router, approvals, tests, CI, and evidence hashes became inspectable in one artifact.

## 16. Agent-to-Deterministic Conversion

Problem: one stable factual agentic subtask was better as code.

Evidence: `scripts/check-config-docs-consistency.py`, `docs/capstone/deterministic-conversion.md`.

Decision: convert `DATABASE_URL` docs/config consistency checking to deterministic code.

Impact: `$0` model cost and repeatable runtime for that narrow check.

## 17. Controlled Tool-Evolution Fault Injection

Problem: the project needed to show guardrails catch plausible tool-contract weakening.

Evidence: `docs/capstone/tool-evolution-drill.md`, commits `7c666e5` and `4e446f6`.

Decision: intentionally weaken `policy-tests`, preserve failure, then repair.

Impact: eval-gated history shows change -> gate failure -> fix.

## 18. First GitHub CI Failure

Problem: first real GitHub run failed.

Evidence: run `31512923419`.

Decision: diagnose honestly. `evaluation-gate` lacked `pytest`; audit expected an unavailable integrity artifact.

Verification: failure preserved.

Impact: real CI iteration evidence exists.

## 19. CI Repair

Problem: GitHub CI needed to pass permanent gates.

Evidence: commit `92d60c4`.

Decision: install `pytest`, keep integrity dependencies, add `if: always()`, and make audit missing-artifact handling explicit.

Verification: run `31513173735` passed.

Impact: permanent gates became green.

## 20. Terminal Green CI

Problem: final documentation state also needed CI evidence.

Evidence: terminal run `31513596822`.

Verification: policy `18 passed`, eval `60 passed`, integrity `PASS`, advisory `SKIPPED`, audit `success`.

Impact: final capstone branch has real green governance CI.

## 21. Semantic Retrieval Contract

Problem: Canvas feedback said semantic document search was absent from all available evidence.

Evidence: `mcp-servers/retrieval/server.py`, `eval/test_retrieval_behavior.py`, `docs/capstone/retrieval-tool-evidence.md`.

Decision: add bounded deterministic semantic-vector ranking to the existing governed retrieval server, preserve classification ceilings, and require path/section citations on returned matches.

Verification: the new behavior tests cover synonym-based ranking, citation output, above-ceiling withholding, and empty-query denial.

Impact: retrieval is now directly inspectable as schema-versioned, classification-tagged, and citation-bearing instead of only documented as an allow-list concept.

## 22. Timeout, Retry, and Budget Enforcement

Problem: Canvas feedback said reliability controls were described but not demonstrated.

Evidence: `eval/reliability_controls.py`, `eval/test_reliability_controls.py`, `docs/capstone/reliability-controls.md`.

Decision: keep the frozen measured router unchanged and add a deterministic decision seam over recorded attempt evidence.

Verification: tests demonstrate one bounded retry, retry exhaustion, timeout stop, budget stop, and non-retryable escalation.

Impact: reliability decisions are machine-checkable without rerunning paid model workflows or rewriting historical holdouts.

## 23. Offline Sandbox Boundary

Problem: fork/run readiness, egress, and parallel-session isolation were hard to verify.

Evidence: `scripts/run-offline-governance-verification.sh`, `eval/test_sandbox_contract.py`, `docs/capstone/reproducibility-runbook.md`.

Decision: provide one offline verification command with network disabled, read-only root/workspace, no credential mount, dropped capabilities, bounded resources, tmpfs, and a unique container name.

Verification: static contract tests and shell syntax checks passed. The fresh network-disabled, read-only container run reported `32 passed`.

Impact: a grader has an explicit isolated path that cannot contact external services during deterministic verification.

## 24. Canvas Feedback Resolution and Score Correction

Problem: grader evidence was inaccessible, the concern-to-file map was missing, and the prior self-audit total was arithmetically wrong.

Evidence: `docs/capstone/grader-feedback-resolution.md`, `docs/capstone/evidence-index.md`, `docs/capstone/final-rubric-audit.md`.

Decision: map every Canvas comment to evidence and remaining action, and correct `49/52` to `48/52` because four criteria are one point below full credit.

Verification: `52 - 1 - 1 - 1 - 1 = 48`.

Impact: the submission package is easier to grade and no longer overstates its defensible score.
