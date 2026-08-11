# ADR 0005: Governance And Eval-Gated CI

## Context

Before this milestone, `.github/workflows/test.yml` contained ordinary backend/frontend checks but not the official Module 4 governance pattern. Commit `a102a79` added `.github/workflows/ci.yml`, `eval/ci_change_classifier.py`, and pipeline integrity checks.

## Decision

Add a separate capstone CI workflow with jobs for change classification, permanent policy tests, conditional evaluation, pipeline integrity, advisory review, and audit trail.

## Rejected Alternatives

- Replacing `test.yml`. Rejected because the existing application test workflow remains useful and did not need deletion.
- Making AI review blocking. Rejected because the official lesson treats it as advisory and secrets may be unavailable.
- Skipping audit on failure. Rejected because audit evidence is most useful when prior jobs fail.

## Evidence

- Local workflow YAML parsing passed.
- `scripts/check-pipeline-integrity.py` rejects policy `continue-on-error`, missing audit, broad write permissions, production markers, and unsafe secret exposure.
- Docker policy/MCP/coursetools checks reported `18 passed`.

## Consequences

Permanent deterministic gates can fail CI without requiring AI secrets. Advisory review degrades to `SKIPPED -- AI SECRET UNAVAILABLE`.

## Open Risks

Actual GitHub Actions execution is not proven until the branch is pushed with Muhammad's explicit authorization.
