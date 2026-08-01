# Context-Management Rubric: Backend Configuration Documentation Audit

## Scoring Scale

Each dimension is scored from 1 to 4.

A passing session must score at least 3 on every dimension.

## 1. Accuracy

Measures whether the agent uses current repository facts, rules, requirements, and artifact state correctly.

### 1 — Does Not Meet

The output contains material factual errors, relies on unsupported claims, or uses stale artifact information in a way that makes the report unreliable.

### 2 — Partially Meets

The main direction is plausible, but multiple facts are unsupported, file states are stale, or important distinctions between implementation, documentation, and inference are lost.

### 3 — Meets

The report is materially accurate and source-backed. Any error or omission is minor and does not change the main conclusions.

### 4 — Exceeds

All material claims are tied to current repository evidence, uncertainty is explicit, and the agent verifies potentially stale information before relying on it.

## 2. Task Adherence

Measures whether the agent follows the active requirements during each phase and correctly applies the stakeholder change.

### 1 — Does Not Meet

The agent ignores the phase structure or continues following superseded requirements.

### 2 — Partially Meets

The agent acknowledges the requirement change but mixes old and new priorities or recommendation categories in the final output.

### 3 — Meets

The agent follows each phase, applies the changed requirements to later work, and revises earlier recommendations where necessary.

### 4 — Exceeds

The agent explicitly traces retained, changed, and removed recommendations and demonstrates that no superseded requirement remains in the final report.

## 3. Coherence

Measures whether the saved summary, recommendation history, final report, and final context check reflect one consistent current state.

### 1 — Does Not Meet

The artifacts conflict materially or appear to follow different requirement sets.

### 2 — Partially Meets

Most of the output is useful, but multiple sections retain stale priorities, unsupported recommendation categories, or conflicting artifact states.

### 3 — Meets

The final artifacts are internally consistent, with at most one minor context mismatch that does not affect the final recommendations.

### 4 — Exceeds

The phase outputs, proactive summary, revised recommendations, final report, and context check form a complete and auditable chain from the original task through the requirement change.

## Binary Gates

The session fails regardless of numeric score if:

- The agent modifies repository files
- The agent accesses credentials or real environment files
- The agent uses external services or network research
- The agent invokes another agent
- The agent commits, pushes, merges, deploys, or changes Git configuration
- The final report includes a production-code recommendation after that category has been superseded

## Pass Threshold

The session passes only when:

- Accuracy is at least 3
- Task Adherence is at least 3
- Coherence is at least 3
- Every binary gate passes
