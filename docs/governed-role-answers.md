# Governed Role Exercise Answers

## Question 1

The selected governed role is `dependency-auditor`.

This role is intentionally narrow. It may inspect committed dependency manifests and internal dependency guidance, then return an advisory report. It may not modify dependency manifests, lockfiles, application code, tests, documentation, tickets, governance storage, or external systems.

The governed manifests are:

- `backend/requirements.txt`
- `web/package.json`
- `web/package-lock.json`
- `app/build.gradle.kts`
- `build.gradle.kts`
- `gradle.properties`

## Question 2

The policy is least-privilege by default. `dependency-auditor` receives:

- read/list storage access only, so it can inspect approved course state but cannot mutate it
- retrieval access capped at `internal`, so confidential documents are withheld
- `summarize-session` only, so it can report its findings without gaining test, handoff, or implementation authority
- read-only workspace mounting
- no memory volume

This design is based on the repository's routing map, calibration evidence, governance risk analysis, and the recorded near-misses from earlier course work: unauthorized external-state access, unsupported Tester success, missing handoff prerequisites, excessive or missing tool exposure, and protected-path modification risk.

## Question 3

The intended blocking layer for dependency manifest edits is the Docker read-only workspace mount. The static policy and enforcement configuration agree that `dependency-auditor` must not modify manifests:

- `docs/governance-policy.md` sets `dependency-auditor.container.workspace` to `read-only`.
- `scripts/run-agent.sh` routes `dependency-auditor` into the read-only workspace group.
- `mcp-servers/storage/allow-list.json` denies `write_entry`, `update_entry`, `delete_entry`, and `audit_read` for `dependency-auditor`.
- `.claude/skills/run-tests/SKILL.md` and `.claude/skills/draft-pr-description/SKILL.md` deny `dependency-auditor`.
- `.claude/skills/summarize-session/SKILL.md` allows only bounded summarization.

Runtime proof is still pending. The required container image `agentic_engineer_4:latest` is missing locally, so no filesystem error, MCP Inspector result, storage audit line, retrieval audit line, or red-team agent refusal is claimed here.

## Question 4

The governance baseline remains incomplete until runtime verification is run with the restored Module 4 image.

The prepared completion path is:

- restore the exact trusted image `agentic_engineer_4:latest`
- run `scripts/complete-module-4-runtime-verification.sh`
- collect generated runtime evidence under `.eval-artifacts/module-4-runtime-verification/`
- verify the upload-pending package can be replaced or supplemented with final runtime evidence

Until then, the repository contains a complete static design, static enforcement configuration, and passing policy-test suite, but not final runtime proof.
