# AURA Forge Rubric Self-Check

Corrected defensible score: `48 / 52`

Calculation: `52 - 1 (criterion 2) - 1 (criterion 4) - 1 (criterion 9) - 1 (criterion 11) = 48`.

This self-check uses the official LaunchCode 13-criterion rubric preserved in `docs/capstone/official-rubric-reference.md`. It does not claim that Canvas has regraded the submission.

| # | Official criterion | Score | Defensible evidence summary |
|---:|---|---:|---|
| 1 | Workflow Scoping | 4/4 | Quantified PRE-AURA comparison, measurable acceptance criteria, and explicit comparison with generic-agent, fixed-automation, and uniform-route alternatives. |
| 2 | Sandboxed Environment | 3/4 | Fresh offline verifier passed 32 tests with no network, read-only root/workspace, no credentials, dropped capabilities, bounded resources, and unique run naming. Historical model-backed runs used bridge networking. |
| 3 | Quality Spec & Baseline | 4/4 | Complete PRD, four-dimension scoring guide with examples and thresholds, plus quality, review-latency proxy, defect-rate proxy, cycle-time proxy, and cost. |
| 4 | Agent, Skills & Memory | 3/4 | Versioned agents and three skills, scoped memory, and before/fix/rerun reflection evidence. No stale memory entry was eligible for a real pruning event. |
| 5 | Orchestration & MCP Tools | 4/4 | Scoped multi-agent route, least-privilege grants, persistent storage, and deterministic semantic-vector retrieval with schema, classification ceilings, and citations. |
| 6 | Evaluation & Calibration | 4/4 | Deterministic and rubric harnesses, tracked holdout, representative runs, red-team evidence, and evidence-linked calibration records. |
| 7 | Governance, Security & CI/CD | 4/4 | Real overreach denial, enforced CI policy/eval/integrity gates, red-team prompts, audit trail, rollback criteria, and sanitized artifacts. |
| 8 | Right-Tool Decisions & ADRs | 4/4 | Reusable agent/deterministic/human matrix, nine evidence-backed ADRs, and quantified deterministic conversion with explicit comparison limitations. |
| 9 | Production Integration & Tool-Evolution Drill | 3/4 | Timeout/retry/budget decisions and rollback/escalation are tested. The preserved tool-evolution fault was intentional, so it is not misrepresented as an unobserved spontaneous regression. |
| 10 | Iteration Narrative & Impact | 4/4 | Multiple before/fix/rerun cycles and a five-metric impact comparison with measured/proxy labels and calculations. |
| 11 | Stakeholder Communication | 3/4 | One-pager translates percentages into measured dollars and time. Canvas reports the current video is about 13 minutes against a 10-minute cap, so video work remains open. |
| 12 | Clarity & Flow | 4/4 | Final Gamma deck and speaking materials preserve a coherent problem-to-evidence narrative. |
| 13 | Design | 4/4 | Final deck uses consistent hierarchy and evidence visuals for routing, governance, CI, and measured impact. |

## Current verification

- Full local evaluation suite: `114 passed`.
- Offline network-disabled container: `32 passed`.
- Pipeline integrity: `PASS`.
- Local path-reference scan: `PASS`.
- Grader-feedback implementation commit: `a7813c453b369dcaf0dd2fe27196d730c1889c67`.
- GitHub governance CI run `33517133584`: `SUCCESS` with policy `27 passed` and evaluation `66 passed`.
- Public access: anonymous branch page and raw grader quickstart returned HTTP `200`.
- Video files and video URL were not edited in the non-video revision.

## Required human actions before resubmission

1. Submit the exact public repository link through the Canvas/LaunchCode path requested on August 31.
2. Confirm the grader received and can open the full repository.
3. Work with Codex on a walkthrough at or below 10 minutes; video work was deliberately deferred.
