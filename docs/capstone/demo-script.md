# Demo Script

Target length: 5-7 minutes.

## 0:00-0:30 - Problem and Thesis

Open: `README.md`

Say: "AURA Forge is not another FitGPT consumer feature. It is a governed engineering paved road around FitGPT. The problem is that a fixed AI workflow gives the same amount of autonomy to a small docs change and a high-risk governance change."

Expected result: grader sees the thesis and safety boundary.

Backup: `docs/capstone/stakeholder-one-pager.md`.

## 0:30-1:10 - Classifier and Routes

Open: `docs/capstone/final-architecture.md`

Say: "The system starts with a deterministic risk classifier, then the router selects LOW, MEDIUM, or HIGH. The router was frozen before the AURA measurements."

Expected result: Mermaid system architecture and route comparison render in GitHub.

Backup: `docs/capstone/adaptive-routing.md`.

## 1:10-1:55 - LOW Result

Open: `docs/capstone/control-vs-aura-impact.md`

Say: "LOW was the clearest over-service case. The fixed route scored 14 out of 16 and cost about 61 cents. AURA scored 16 out of 16, reduced cost by 44.32 percent, cut model roles by 60 percent, and removed human checkpoints."

Expected result: LOW impact table visible.

## 1:55-2:35 - MEDIUM Result

Open: same file.

Say: "MEDIUM still needed implementation, review, and testing. AURA removed planner and project-manager overhead while preserving rigor. Cost dropped 19.71 percent and quality improved from 15 to 16."

Expected result: MEDIUM row visible.

## 2:35-3:10 - HIGH Governance Preservation

Open: same file.

Say: "HIGH intentionally kept full governance. Cost only dropped 5.89 percent because the system preserved the full route and human checkpoints for sensitive evaluation and MCP paths."

Expected result: HIGH row visible.

## 3:10-3:50 - Overreach Denial

Open: `docs/capstone/governance-overreach-demo.md`

Command:

```bash
pytest -q -p no:cacheprovider eval/test_governance_overreach.py
```

Say: "This is the safety story. An implementer attempted the Project-Manager-only task tracker, and the real governed MCP authorization layer denied it."

Expected result: test passes and denial text is visible in the doc.

Backup: `GO-20260811-001` section in the document.

## 3:50-4:35 - Real GitHub CI

Open: `docs/capstone/governance-ci-results.md`

Say: "The first GitHub run failed because the evaluation job lacked pytest. I preserved that failed run, repaired the workflow, and the terminal run passed policy, evaluation, integrity, advisory skip, and audit."

Expected result: run `31513596822` and job table visible.

Backup: GitHub Actions URL in the doc.

## 4:35-5:10 - Change Passport

Open: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`

Say: "The Change Passport is not a new decision system. It aggregates real producer evidence: classifier, route, approvals, costs, tests, and GitHub CI."

Expected result: JSON with `aura-risk-v1`, `aura-router-v1`, `aura-high-v1`, and CI run fields.

## 5:10-5:40 - Right-Tool Conversion

Open: `docs/capstone/deterministic-conversion.md`

Say: "One stable factual auditor task was converted from an agentic check to deterministic code. That narrow check now costs zero model dollars and is easier to audit."

Expected result: conversion evidence visible.

## 5:40-6:30 - Close

Open: `docs/capstone/final-evidence-snapshot.md`

Say: "Measured across three representative scenarios only, AURA improved quality from 44 to 48 out of 48, reduced successful-route cost by 19.22 percent, cut model roles by a third, and cut human checkpoints in half. The limitation is deliberate: this is isolated course engineering evidence, not a production FitGPT deployment claim."

Expected result: final snapshot visible.
