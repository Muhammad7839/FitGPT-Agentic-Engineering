# Module 2 Lab Plan — Backend Configuration Documentation Auditor

## Primary Track

Track 2: Calibrate One Defined Agent.

## Agent

`backend-config-docs-auditor`

Starting version:

`v0.1.2`

## Real Project Need

FitGPT has backend startup and configuration behavior distributed across implementation, tests, environment examples, deployment files, and contributor documentation.

A new contributor needs an accurate, prioritized, and patch-ready plan showing which documentation should change and why.

The agent must be able to produce that plan without modifying files, reopening excluded production-code recommendations, exposing sensitive data, or overstating what focused evidence proves.

## Calibration Task

Each run will use the same task:

Produce a patch-ready onboarding documentation correction plan for FitGPT backend startup and configuration using only committed repository evidence.

The task must identify no more than five highest-impact gaps.

For each recommendation, the agent must provide:

- Stable recommendation ID
- Contributor symptom or likely confusion
- Current documentation claim
- Current implementation or focused-test evidence
- Exact target file and section
- Proposed documentation change
- Human validation step
- Confidence and limitations

## Controlled Variables

Across all three runs:

- The same task prompt will be used.
- The same repository application and documentation state will be used.
- The repository will be mounted read-only.
- No tests, builds, application code, or validation commands will run.
- No external services or network research will be used.
- The same rubric will be applied.
- Each run will use a fresh Claude Code session.
- No run will use `--continue` or `--resume`.

Only the agent definition may change between runs.

## Run Sequence

### Run 1

Use `v0.1.2` as the baseline.

Preserve the complete report and score it without changing the agent first.

### Run 2

Implement one meaningful correction supported by Run 1 evidence.

Use a fresh session and the same task.

### Run 3

Implement a second meaningful correction supported by Run 2 evidence.

Use a fresh session and the same task.

## Evidence-Based Revision Rule

A version change must address a documented weakness from the previous run.

Do not change instructions merely to create another version number.

Potential calibration areas include:

- Role clarity
- Evidence collection
- Recommendation prioritization
- Patch readiness
- Output structure
- Scope control
- Self-verification
- Limitation reporting

The actual change will be selected only after reviewing the preceding run.

## Expected Final State

By Run 3, the agent should produce a reliable, evidence-backed, contributor-focused, patch-ready report that a human could use to update documentation without repeating the audit.

## Safety

- Work only in the course repository.
- Never access the original FitGPT repository.
- Never expose secrets or real environment values.
- Never modify application code or tests during calibration runs.
- Never push without explicit authorization.
- Treat focused evidence as narrow in scope.
- Preserve every run and revision in Git.
