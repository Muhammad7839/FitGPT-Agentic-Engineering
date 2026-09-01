# AURA Forge Evidence Index

This index is organized for a grader. It points to the strongest evidence without requiring a repository hunt.

## Top Evidence Items

| # | Evidence | File | Commit / Run | What it proves |
|---:|---|---|---|---|
| 1 | AURA Forge PRD | `docs/capstone/aura-forge-prd.md` | `75dd1f8` lineage | Scoped workflow, stakeholder, trigger, acceptance criteria, exclusions. |
| 2 | Quality rubric and baseline | `docs/capstone/quality-rubric.md`, `docs/capstone/control-baseline-results.md` | `75dd1f8` | Scoring rules and PRE-AURA baseline. |
| 3 | Control vs AURA impact | `docs/capstone/control-vs-aura-impact.md` | `025bcbf` | Measured LOW/MEDIUM/HIGH impact. |
| 4 | Deterministic risk classifier | `eval/risk_classifier.py`, `docs/capstone/risk-classifier.md` | `ed991a8` | LOW/MEDIUM/HIGH classification. |
| 5 | Adaptive router | `eval/adaptive_router.py`, `docs/capstone/adaptive-routing.md` | `c844db1` | Frozen route selection. |
| 6 | Fresh MCP overreach denial | `docs/capstone/governance-overreach-demo.md`, `eval/test_governance_overreach.py` | `8b711d4` | Real least-privilege denial. |
| 7 | Real GitHub governance CI | `.github/workflows/ci.yml`, `docs/capstone/governance-ci-results.md` | run `33517133584`, commit `a7813c4` | Current policy, eval, integrity, advisory skip, and audit success. |
| 8 | Change Passport | `scripts/build-change-passport.py`, `docs/capstone/evidence/change-passport-AF-HIGH-001.json` | `13edafc`, run `31513596822` | Evidence aggregation with real CI fields. |
| 9 | Deterministic conversion | `scripts/check-config-docs-consistency.py`, `docs/capstone/deterministic-conversion.md` | `9f9e461` | Right-tool conversion from agentic check to deterministic code. |
| 10 | Tool-evolution drill | `docs/capstone/tool-evolution-drill.md` | `7c666e5`, `4e446f6` | Eval-gated fault and repair history. |
| 11 | Governed semantic retrieval | `mcp-servers/retrieval/server.py`, `docs/capstone/retrieval-tool-evidence.md` | current revision | Ranked, schema-validated, classification-tagged, citation-bearing retrieval. |
| 12 | Reliability controls | `eval/reliability_controls.py`, `docs/capstone/reliability-controls.md` | current revision | Timeout, retry, budget, and escalation decisions. |
| 13 | Reflection evidence | `docs/capstone/reflection-log.md` | historical run/fix commits | Before/fix/rerun agent and memory evidence. |
| 14 | Canvas feedback map | `docs/capstone/grader-feedback-resolution.md` | current revision | Direct concern-to-evidence navigation and remaining blockers. |
| 15 | Final walkthrough video | https://youtu.be/srFGYvnEd7c | final submission artifact | Recorded stakeholder walkthrough artifact; duration issue remains open. |

## Five-Minute Navigation

| Question | Start here |
|---|---|
| What problem did Muhammad solve? | `docs/capstone/GRADER-QUICKSTART.md`, `docs/capstone/aura-forge-prd.md` |
| Why an adaptive agentic system? | `docs/capstone/aura-forge-prd.md`, `docs/capstone/right-tool-decision-matrix.md` |
| How do LOW/MEDIUM/HIGH work? | `docs/capstone/risk-classifier.md`, `docs/capstone/adaptive-routing.md` |
| What changed versus baseline? | `docs/capstone/control-baseline-comparison.md`, `docs/capstone/control-vs-aura-impact.md` |
| What are the measured results? | `docs/capstone/control-vs-aura-impact.md`, `docs/capstone/aura-results.md` |
| Where is real governance evidence? | `docs/capstone/governance-overreach-demo.md` |
| Where is CI evidence? | `docs/capstone/governance-ci-results.md` |
| Where is the Change Passport? | `docs/capstone/evidence/change-passport-AF-HIGH-001.json`, `docs/capstone/change-passport.md` |
| Where is the deterministic conversion? | `docs/capstone/deterministic-conversion.md` |
| Where is semantic retrieval proven? | `docs/capstone/retrieval-tool-evidence.md`, `eval/test_retrieval_behavior.py` |
| Where are timeout/retry/budget controls proven? | `docs/capstone/reliability-controls.md`, `eval/test_reliability_controls.py` |
| Where are agent/skill/memory reruns? | `docs/capstone/reflection-log.md` |
| How does this answer Canvas feedback? | `docs/capstone/grader-feedback-resolution.md` |
| How do I reproduce core tests? | `docs/capstone/reproducibility-runbook.md` |
| Where are the ADRs? | `docs/adr/`, `docs/capstone/adr-evidence-matrix.md` |
| Where is the final presentation? | `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf` |
| Where is the final walkthrough video? | https://youtu.be/srFGYvnEd7c |
| What remains human-only? | `docs/capstone/submission/FINAL-HUMAN-CHECKLIST.md` |
| Where is the final dry run? | `docs/capstone/reproducibility-dry-run.md`, `docs/capstone/final-pre-video-verification.md` |
| Where is the sanitization audit? | `docs/capstone/final-security-audit.md` |

## Criteria Map

| Criterion | Evidence | Commit / run | What it proves |
|---|---|---|---|
| 1. Workflow Scoping | `docs/capstone/aura-forge-prd.md`, `docs/capstone/representative-scenarios.md`, `docs/capstone/baseline-results.md` | `75dd1f8` lineage | Real workflow, stakeholder, triggers, acceptance criteria, baseline pain. |
| 2. Sandboxed Environment | `Dockerfile`, `scripts/run-offline-governance-verification.sh`, `eval/test_sandbox_contract.py`, `docs/capstone/reproducibility-runbook.md` | current revision plus `31af8c3`, `78110e2` lineage | Offline network boundary, read-only root/workspace, no credentials, unique parallel run name, bounded resources. |
| 3. Quality Spec & Baseline | `docs/capstone/quality-rubric.md`, `docs/capstone/control-baseline-results.md`, `.eval-artifacts/capstone/control-baseline/*` | `75dd1f8` | 16-point run rubric and measured control baseline. |
| 4. Agent, Skills & Memory | `.claude/agents/*`, `.claude/skills/*`, `.memory/*`, `docs/memory-architecture.md`, `docs/capstone/reflection-log.md` | course and capstone commits | Versioned agents/skills, scoped memory, before/fix/rerun reflection evidence. |
| 5. Orchestration & MCP Tools | `docs/orchestration-diagram.md`, `docs/routing-and-tool-grant-map.md`, `mcp/coursetools_server.py`, `mcp-servers/retrieval/server.py`, `eval/test_retrieval_behavior.py` | Module 3/4 and current revision | Multi-role route, MCP allow-lists, least privilege, governed semantic retrieval and citations. |
| 6. Evaluation & Calibration | `eval/test_deterministic.py`, `eval/test_rubric_suite.py`, `docs/calibration-log.md`, `docs/holdout-task-set.md` | Module 3 commits | Deterministic/rubric harness, holdout, calibration evidence. |
| 7. Governance, Security & CI/CD | `.github/workflows/ci.yml`, `scripts/check-pipeline-integrity.py`, `docs/capstone/governance-ci-results.md` | run `33517133584`, commit `a7813c4` | Current enforced CI gates and audit trail. |
| 8. Right-Tool Decisions & ADRs | `docs/capstone/right-tool-decision-matrix.md`, `docs/capstone/adr-evidence-matrix.md`, `docs/adr/*`, `docs/capstone/deterministic-conversion.md` | `643c455`, `9f9e461` | Agent vs deterministic vs human rationale. |
| 9. Production Integration & Tool-Evolution Drill | `docs/capstone/tool-evolution-drill.md`, `docs/capstone/monitoring-incident-runbook.md`, `eval/reliability_controls.py`, `eval/test_reliability_controls.py` | `7c666e5`, `4e446f6`, `92d60c4`, current revision | Production-like isolated CI, failure handling, drill, timeout/retry/budget enforcement. |
| 10. Iteration Narrative & Impact | `docs/capstone/iteration-narrative.md`, `docs/capstone/control-vs-aura-impact.md`, `docs/capstone/reflection-log.md` | packaging commit, `025bcbf`, historical fix commits | Chronological improvement, measured five-metric impact, and rerun evidence. |
| 11. Stakeholder Communication | `docs/capstone/stakeholder-one-pager.md`, `docs/capstone/GRADER-QUICKSTART.md`, `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md`, `docs/capstone/submission/VIDEO-EVIDENCE-STAGING.md`, https://youtu.be/srFGYvnEd7c | packaging commits and final video artifact | Non-engineer summary, recording plan, and final walkthrough video now exist. |
| 12. Clarity & Flow | `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`, `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md` | presentation commits | Complete 10-slide Gamma narrative and speaker flow. |
| 13. Design | `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`, `docs/capstone/submission/AURA_Forge_Slide_Preview.png` | presentation commits | Final rendered visual deck and preserved historical contact sheet. |
