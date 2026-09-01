# Canvas Grader Feedback Resolution Map

This file maps the August 27 Canvas feedback to the current repository. It separates repository fixes from external actions and the deferred video work.

## Latest LaunchCode Request

On August 31, 2026, Learn at LaunchCode emailed Muhammad that the grader asked for the full repository and can grade the work after it is submitted. This confirms repository delivery is the immediate priority. The email does not specify whether LaunchCode prefers a public repository, collaborator access, or another private-repository submission method, so repository visibility must be resolved without guessing.

| Rubric area | Grader concern | Current resolution | Strongest evidence | Remaining action |
|---|---|---|---|---|
| Workflow Scoping | Explain why a custom pipeline beats simpler automation or a prebuilt agent. | The PRD compares a generic coding agent, fixed deterministic CI, the prior uniform multi-agent route, and AURA Forge using measured route evidence. | `docs/capstone/aura-forge-prd.md`, `docs/capstone/right-tool-decision-matrix.md` | None in repository. |
| Sandboxed Environment | Fork/run readiness, network egress, and parallel-session isolation were unclear. | A one-command offline verifier now uses no network, a read-only root and workspace, no capabilities, no credential mount, bounded resources, tmpfs, and a unique container name. The fresh offline container run passed `32` tests. | `scripts/run-offline-governance-verification.sh`, `eval/test_sandbox_contract.py`, `docs/capstone/reproducibility-runbook.md` | Historical model-backed runs still used ordinary bridge networking and retain that limitation. |
| Quality Spec & Baseline | PRD/rubric inaccessible; review latency and cycle time missing. | PRD and four-dimension rubric are directly indexed. The impact report now shows quality, review-latency proxy, defect-rate proxy, cycle-time proxy, and cost with calculations and limitations. | `docs/capstone/quality-rubric.md`, `docs/capstone/control-vs-aura-impact.md` | None in repository. |
| Agent, Skills & Memory | Skills and reflection evidence were not visible. | Three versioned skills are committed and a concise reflection index now links real before/fix/rerun evidence. Memory scope and the no-stale-entry review are explicit. | `.claude/skills/*/SKILL.md`, `docs/capstone/reflection-log.md`, `docs/memory-architecture.md`, `.memory/SCOPE.md` | Full historical stale-pruning events cannot be invented; current index has no stale entry. |
| Orchestration & MCP Tools | Semantic document search was absent. | The governed retrieval tool now performs deterministic semantic-vector ranking, validates inputs, applies role classification ceilings, and returns citations. | `mcp-servers/retrieval/server.py`, `eval/test_retrieval_behavior.py`, `docs/capstone/retrieval-tool-evidence.md` | Fresh GitHub CI after push. |
| Evaluation & Calibration | Holdout content and evidence-linked calibration were inaccessible. | Holdout, calibration log, calibration answers, deterministic harness, and red-team results are tracked and directly indexed. Locked historical holdouts were not rerun. | `docs/holdout-task-set.md`, `docs/calibration-log.md`, `docs/calibration-answers.md`, `eval/red-team-results.md` | None in repository. |
| Governance, Security & CI/CD | Eval-gated history and red-team prompts were inaccessible. | CI gates, integrity checker, fault/fix commits, red-team prompts/results, and real overreach denial are tracked and linked. | `.github/workflows/ci.yml`, `docs/capstone/tool-evolution-drill.md`, `eval/red-team-prompts.md`, `docs/capstone/governance-overreach-demo.md` | Fresh GitHub CI after push. |
| Right-Tool Decisions & ADRs | Pre-conversion latency/dollar cost and contemporaneous reasoning were weak. | The conversion record now quotes the preserved Run 5 cycle and displayed cost, shows the deterministic runtime/cost calculation, and labels the historical full-run comparison as an upper bound. ADR evidence remains commit-linked. | `docs/capstone/deterministic-conversion.md`, `docs/capstone/adr-evidence-matrix.md` | None in repository. |
| Production Integration & Tool Evolution | Timeout, retry, and budget enforcement were described but not demonstrated. | A deterministic execution-limit controller and focused tests now demonstrate retry allow-listing, retry exhaustion, timeout, budget stop, and fail-closed escalation. | `eval/reliability_controls.py`, `eval/test_reliability_controls.py`, `docs/capstone/reliability-controls.md` | The historical intentional fault remains intentional and is not called spontaneous. |
| Iteration Narrative & Impact | Two visible cycles and five baseline metrics were missing. | Reflection evidence surfaces multiple before/fix/rerun cycles. The impact report now provides all five requested metrics, using clearly labeled proxies where direct measurements were unavailable. | `docs/capstone/reflection-log.md`, `docs/capstone/iteration-narrative.md`, `docs/capstone/control-vs-aura-impact.md` | None in repository. |
| Stakeholder Communication | Video exceeds 10 minutes; percentages need business translation. | The one-pager now translates cost and model time into dollars and seconds/minutes. | `docs/capstone/stakeholder-one-pager.md` | Video remains intentionally untouched and must be handled with Muhammad. |
| Clarity & Flow | Full credit. | Existing narrative preserved. | Final Gamma presentation and speaker materials. | Preserve during later video work. |
| Design | No written grader comment. | Existing design package preserved. | Final Gamma presentation and assets. | Revisit only if later feedback is specific. |

## Submission-Provenance Blocker

The local branch is `capstone/aura-forge` in `Muhammad7839/FitGPT-Agentic-Engineering`. On August 28, 2026, the authenticated GitHub repository API reported `visibility: PRIVATE`, and an unauthenticated request to the branch returned `404`. A logged-out grader cannot currently inspect the evidence.

Before resubmission, the owner must verify the canonical repository in a logged-out browser, make it grader-accessible if appropriate, push this revision, wait for current CI, and submit that exact repository link. Do not claim this blocker is resolved from local Git access alone.

## Deliberately Deferred

No video file, upload, URL, script timing, or recording was edited in this revision. The video-length issue remains open by Muhammad's instruction.
