# AURA Forge Evidence Index

This index is organized for a grader. It points to the strongest evidence without requiring a repository hunt.

## Top 10 Evidence Items

| # | Evidence | File | Commit / Run | What it proves |
|---:|---|---|---|---|
| 1 | AURA Forge PRD | `docs/capstone/aura-forge-prd.md` | `75dd1f8` lineage | Scoped workflow, stakeholder, trigger, acceptance criteria, exclusions. |
| 2 | Quality rubric and baseline | `docs/capstone/quality-rubric.md`, `docs/capstone/control-baseline-results.md` | `75dd1f8` | Scoring rules and PRE-AURA baseline. |
| 3 | Control vs AURA impact | `docs/capstone/control-vs-aura-impact.md` | `025bcbf` | Measured LOW/MEDIUM/HIGH impact. |
| 4 | Deterministic risk classifier | `eval/risk_classifier.py`, `docs/capstone/risk-classifier.md` | `ed991a8` | LOW/MEDIUM/HIGH classification. |
| 5 | Adaptive router | `eval/adaptive_router.py`, `docs/capstone/adaptive-routing.md` | `c844db1` | Frozen route selection. |
| 6 | Fresh MCP overreach denial | `docs/capstone/governance-overreach-demo.md`, `eval/test_governance_overreach.py` | `8b711d4` | Real least-privilege denial. |
| 7 | Real GitHub governance CI | `.github/workflows/ci.yml`, `docs/capstone/governance-ci-results.md` | run `31513596822` | Policy, eval, integrity, advisory skip, audit. |
| 8 | Change Passport | `scripts/build-change-passport.py`, `docs/capstone/evidence/change-passport-AF-HIGH-001.json` | `13edafc`, run `31513596822` | Evidence aggregation with real CI fields. |
| 9 | Deterministic conversion | `scripts/check-config-docs-consistency.py`, `docs/capstone/deterministic-conversion.md` | `9f9e461` | Right-tool conversion from agentic check to deterministic code. |
| 10 | Tool-evolution drill | `docs/capstone/tool-evolution-drill.md` | `7c666e5`, `4e446f6` | Eval-gated fault and repair history. |
| 11 | Final walkthrough video | https://youtu.be/srFGYvnEd7c | final submission artifact | Recorded stakeholder walkthrough artifact. |

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
| 2. Sandboxed Environment | `Dockerfile`, `.agentic/container/*`, `docs/capstone/foundation-runtime-repair.md`, `README.md` | `31af8c3`, `78110e2` lineage | Governed runtime, read-only `/workspace`, no Claude auth required for deterministic checks. |
| 3. Quality Spec & Baseline | `docs/capstone/quality-rubric.md`, `docs/capstone/control-baseline-results.md`, `.eval-artifacts/capstone/control-baseline/*` | `75dd1f8` | 16-point run rubric and measured control baseline. |
| 4. Agent, Skills & Memory | `.claude/agents/*`, `.claude/skills/*`, `.memory/*`, `docs/memory-architecture.md`, agent iteration logs | course and capstone commits | Versioned agents/skills, memory layout, reflection evidence. |
| 5. Orchestration & MCP Tools | `docs/orchestration-diagram.md`, `docs/routing-and-tool-grant-map.md`, `mcp/coursetools_server.py`, `eval/test_policy.py` | Module 3/4 and capstone commits | Multi-role route, MCP allow-lists, least privilege. |
| 6. Evaluation & Calibration | `eval/test_deterministic.py`, `eval/test_rubric_suite.py`, `docs/calibration-log.md`, `docs/holdout-task-set.md` | Module 3 commits | Deterministic/rubric harness, holdout, calibration evidence. |
| 7. Governance, Security & CI/CD | `.github/workflows/ci.yml`, `scripts/check-pipeline-integrity.py`, `docs/capstone/governance-ci-results.md` | `a102a79`, `92d60c4`, run `31513596822` | Enforced CI gates and audit trail. |
| 8. Right-Tool Decisions & ADRs | `docs/capstone/right-tool-decision-matrix.md`, `docs/capstone/adr-evidence-matrix.md`, `docs/adr/*`, `docs/capstone/deterministic-conversion.md` | `643c455`, `9f9e461` | Agent vs deterministic vs human rationale. |
| 9. Production Integration & Tool-Evolution Drill | `docs/capstone/tool-evolution-drill.md`, `docs/capstone/monitoring-incident-runbook.md`, `docs/capstone/governance-ci-results.md` | `7c666e5`, `4e446f6`, `92d60c4` | Production-like isolated CI, failure handling, drill. |
| 10. Iteration Narrative & Impact | `docs/capstone/iteration-narrative.md`, `docs/capstone/control-vs-aura-impact.md` | packaging commit, `025bcbf` | Chronological improvement and measured impact. |
| 11. Stakeholder Communication | `docs/capstone/stakeholder-one-pager.md`, `docs/capstone/GRADER-QUICKSTART.md`, `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md`, `docs/capstone/submission/VIDEO-EVIDENCE-STAGING.md`, https://youtu.be/srFGYvnEd7c | packaging commits and final video artifact | Non-engineer summary, recording plan, and final walkthrough video now exist. |
| 12. Clarity & Flow | `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`, `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md` | presentation commits | Complete 10-slide Gamma narrative and speaker flow. |
| 13. Design | `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`, `docs/capstone/submission/AURA_Forge_Slide_Preview.png` | presentation commits | Final rendered visual deck and preserved historical contact sheet. |
