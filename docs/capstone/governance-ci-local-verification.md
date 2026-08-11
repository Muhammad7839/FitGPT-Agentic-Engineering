# Governance and CI Local Verification

This document records what was proven locally before any GitHub remote contact. It does not claim that GitHub Actions has run yet.

## Proven Locally

### Workflow Structure

`.github/workflows/ci.yml` defines the capstone governance pipeline with these jobs:

- `change-classifier`
- `policy-tests`
- `evaluation-gate`
- `pipeline-integrity`
- `advisory-review`
- `audit-trail`

The older `.github/workflows/test.yml` remains present and unchanged.

### Deterministic Change Classification

`eval/ci_change_classifier.py` adapts the existing deterministic AURA risk rules for CI-facing decisions. It emits machine-readable fields for:

- changed paths;
- triggered rules;
- risk tier;
- whether expensive evaluation should run;
- whether permanent guardrails were modified.

Local tests passed:

```text
pytest -q -p no:cacheprovider eval/test_ci_change_classifier.py
```

### Permanent Policy Gate

The `policy-tests` job is blocking. It does not use `continue-on-error: true` and does not require model credentials.

The intended deterministic commands are:

```text
python -m pytest -q eval/test_policy.py eval/test_mcp_runtime.py eval/test_coursetools_runtime.py
```

The governed Docker runtime passed the policy, MCP runtime, and coursetools runtime suite:

```text
18 passed
```

### Evaluation Gating Logic

The `evaluation-gate` job depends on `change-classifier` and `policy-tests`.

When the classifier reports agent, prompt, skill, tool, governance, or CI behavior changes, it runs deterministic AURA checks:

```text
python -m pytest -q eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py
```

When expensive evaluation is not required, it writes an explicit skipped status. It does not claim a skipped agentic evaluation passed.

### Pipeline Integrity Enforcement

`scripts/check-pipeline-integrity.py` checks the capstone workflow for deterministic guardrail weakening. It rejects:

- missing `policy-tests`;
- `continue-on-error: true` on `policy-tests`;
- missing `pipeline-integrity`;
- missing `audit-trail`;
- missing policy dependencies;
- missing audit dependencies;
- workflow-level secrets;
- secrets outside advisory review;
- production deployment markers;
- broad write permissions.

Local integrity checks passed for the repaired workflow:

```text
python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml
```

### Advisory Review Graceful Degradation

`scripts/run-advisory-review.py` is advisory only. The workflow marks only this job as non-blocking.

If `AURA_ADVISORY_AI_KEY` is unavailable, the job writes:

```text
SKIPPED - AI SECRET UNAVAILABLE
```

No AI output is fabricated.

### Audit Trail Construction

`scripts/build-audit-trail.py` builds sanitized JSON and Markdown summaries from available local or workflow artifacts. The workflow runs the audit job with dependencies on prior jobs and `if: always()`.

Missing optional producers are represented as unavailable instead of being fabricated.

Local tests passed:

```text
pytest -q -p no:cacheprovider eval/test_audit_trail.py
```

### Fresh Overreach Denial

The capstone-era governance overreach demo `GO-20260811-001` used the real governed MCP authorization layer. An `implementer` role attempted to use the Project-Manager-only `task_tracker` tool and was denied.

Sanitized denial:

```text
Authorization error: role 'implementer' is not on the allow-list for task_tracker. Allowed roles: ['project-manager'].
```

The demo recorded zero model cost and no external state change.

### Change Passport

`scripts/build-change-passport.py` generated evidence-backed passports for:

- `AF-LOW-001`
- `AF-MEDIUM-001`
- `AF-HIGH-001`

The passport is an evidence aggregator. It omits optional fields that do not have real producers and does not include GitHub CI fields before GitHub Actions runs.

Local passport tests passed:

```text
pytest -q -p no:cacheprovider eval/test_change_passport.py
```

### Deterministic Conversion

`scripts/check-config-docs-consistency.py` converts the stable `DATABASE_URL` configuration/documentation consistency check from the historical `backend-config-docs-auditor` work into deterministic code.

The deterministic run produced a PASS result with `$0` model cost.

### Regression Barrier

The broad local deterministic suite passed:

```text
79 passed
```

The governed Docker runtime suite passed:

```text
18 passed
```

Additional local checks passed:

- YAML structural parsing for `.github/workflows/test.yml` and `.github/workflows/ci.yml`;
- JSON parsing for deterministic eval fixtures;
- shell syntax checks for repository shell scripts;
- `git diff --check`;
- locked holdout checksum.

## Not Yet Proven Until GitHub

These claims require an authorized push to the isolated course repository and an actual GitHub Actions run:

- GitHub Actions runner execution;
- real GitHub job status checks;
- real workflow artifact upload and retention behavior;
- real advisory-review secret availability or skip behavior in GitHub;
- real audit-trail artifact from GitHub;
- branch-protection or required-check enforcement;
- real status-check visibility on the remote capstone branch.

No GitHub CI success is claimed before that run exists.
