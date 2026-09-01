# Governance and CI Results

This document records the final governance and CI evidence for the capstone milestone. It separates local evidence from real GitHub Actions evidence.

## September 1 Grader-Feedback Implementation Run

- Commit: `a7813c453b369dcaf0dd2fe27196d730c1889c67`
- Run: `33517133584`
- URL: https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/33517133584
- Conclusion: `success`
- `change-classifier`: success
- `policy-tests`: success, `27 passed`
- `evaluation-gate`: success, `66 passed`
- `pipeline-integrity`: success
- `advisory-review`: success with explicit `SKIPPED` status because the optional AI secret was unavailable
- `audit-trail`: success

The only annotations were non-failing GitHub warnings that Node.js 20-targeting actions were forced to Node.js 24. No policy, evaluation, integrity, advisory, or audit job failed.

## Local Evidence

Before the first push, local checks proved:

- `.github/workflows/ci.yml` parsed as valid YAML;
- `scripts/check-pipeline-integrity.py` passed on the repaired capstone workflow;
- the deterministic classifier, router, audit-trail, Change Passport, config-conversion, governance-overreach, and CI integrity tests passed;
- governed Docker runtime policy/MCP/coursetools tests passed;
- `git diff --check` passed;
- credential-pattern scan found no suspected secrets in the new local history;
- the locked holdout checksum matched `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32`.

Local regression result before the initial push:

```text
79 passed
18 passed in governed Docker runtime
```

## First GitHub CI Run

Run ID: `31512923419`

Commit: `34863d36b3f030a89105bc9964c950e412848eba`

Result: `failure`

Preserved URL:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31512923419`

Observed job results:

| Job | Result |
|---|---|
| `change-classifier` | success |
| `policy-tests` | success |
| `advisory-review` | success with skip artifact |
| `evaluation-gate` | failure |
| `pipeline-integrity` | skipped |
| `audit-trail` | failure |

Failure classification:

- `evaluation-gate`: workflow dependency issue. The GitHub runner did not have `pytest` installed in that job.
- `audit-trail`: follow-on artifact handling issue. Because `pipeline-integrity` was skipped after the evaluation failure, the expected integrity artifact did not exist.

Exact evaluation failure:

```text
pytest: command not found
```

This was a CI environment/configuration failure, not a product policy or evaluation regression.

## Evidence-Based CI Fix

Commit: `92d60c4 ci: repair GitHub evaluation and audit gates`

Fixes:

- installed `pytest` in `evaluation-gate`;
- added `if: always()` to `pipeline-integrity` while preserving its dependencies;
- made the audit-trail builder mark missing requested artifacts as `not_available` instead of crashing;
- added a focused regression test for missing requested audit artifacts.

Local validation before pushing the fix:

```text
71 passed
YAML_OK
holdout checksum matched
```

## First Repaired Green GitHub CI Run

Run ID: `31513173735`

Commit: `92d60c438039b65e6229eefd7abc607c73393a0f`

Result: `success`

URL:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31513173735`

Observed job results:

| Job | Result |
|---|---|
| `change-classifier` | success |
| `policy-tests` | success |
| `evaluation-gate` | success |
| `pipeline-integrity` | success |
| `advisory-review` | completed with `SKIPPED` artifact |
| `audit-trail` | success |

Uploaded artifact names:

- `change-classification`
- `policy-tests`
- `evaluation-gate`
- `pipeline-integrity`
- `advisory-review`
- `audit-trail`

Policy artifact:

```text
18 passed in 0.69s
```

Evaluation artifact:

```text
60 passed in 0.13s
```

Audit artifact:

```text
Policy result: success
Evaluation result: success
Integrity result: PASS
Advisory result: SKIPPED
```

## Terminal Current Green GitHub CI Run

Run ID: `31513596822`

Commit: `c5e2e5323f6ab46d7eb4003d7112ff41ecf6e72e`

Result: `success`

URL:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31513596822`

This later run exists because commit `c5e2e53 docs: record real governance CI results` documented the first repaired green CI result and then validated that final governance-CI documentation state.

Observed terminal job results:

| Job | Result |
|---|---|
| `change-classifier` | success |
| `policy-tests` | success |
| `evaluation-gate` | success |
| `pipeline-integrity` | success |
| `advisory-review` | success with `SKIPPED` artifact |
| `audit-trail` | success |

Terminal policy artifact:

```text
18 passed in 0.73s
```

Terminal evaluation artifact:

```text
60 passed in 0.13s
```

Terminal audit artifact:

```text
Policy result: success
Evaluation result: success
Integrity result: PASS
Advisory result: SKIPPED
```

## Advisory Review

The advisory-review job is non-blocking by design.

The terminal green run produced a real graceful-degradation artifact:

```text
SKIPPED - AI SECRET UNAVAILABLE
```

No model output was fabricated and no secret was added.

## Audit Trail

The audit-trail job ran with `if: always()` and collected available artifacts.

Final result:

```text
success
```

The audit trail contains no secrets and marks unavailable producer data honestly.

## Pipeline Integrity Protection

The terminal green GitHub run reported pipeline integrity as:

```text
PASS
```

## Controlled Pipeline-Integrity Demo

Demo ID: `PI-20260811-001`

This was a local-only demonstration after the green GitHub baseline. It was not pushed because the authorization only allowed pushes to `capstone/aura-forge`, not a separate demonstration branch.

In a detached temporary worktree, `continue-on-error: true` was added to the permanent `policy-tests` job. The real integrity checker rejected the weakened workflow.

Failure:

```text
policy-tests must not use continue-on-error
```

Local evidence:

`.eval-artifacts/capstone/pipeline-integrity-demo/PI-20260811-001/`

The final `capstone/aura-forge` branch does not contain the weakened workflow.

## Fresh Role Overreach Denial

Demo ID: `GO-20260811-001`

The real governed MCP authorization layer denied an `implementer` role attempting to use the Project-Manager-only `task_tracker` tool.

Sanitized denial:

```text
Authorization error: role 'implementer' is not on the allow-list for task_tracker. Allowed roles: ['project-manager'].
```

External state changed: no.

Model cost: `$0`.

## Change Passport With CI Evidence

A CI-backed terminal Passport was generated from real producers for `AF-HIGH-001`.

Local ignored output:

`.eval-artifacts/capstone/change-passports/AF-HIGH-001-with-final-ci.json`

Real CI fields included:

- CI commit: `c5e2e5323f6ab46d7eb4003d7112ff41ecf6e72e`
- policy status: `success`
- evaluation status: `success`
- integrity status: `success`
- audit status: `success`
- advisory status: `SKIPPED`
- artifact references and hashes from the downloaded GitHub run artifacts

## Secrets and Data Classification

No production credentials, real user data, Claude authentication, OAuth material, cookies, service-account material, or production deployment secrets were added.

The workflow grants only read repository contents permission globally.

The only model-related secret reference is scoped to the advisory-review step:

```text
AURA_ADVISORY_AI_KEY
```

When unavailable, the advisory job skips gracefully.

## Escalation and Rollback Guidance

Permanent policy, evaluation, or pipeline-integrity failures must block promotion until diagnosed and fixed with evidence.

Advisory-review failures or unavailable AI credentials are non-blocking but must remain visible in the audit artifact.

If production deployment steps, broad write permissions, or secret exposure are introduced, pipeline integrity should fail and the change should be rejected before merge.

## Final Status

Permanent gates are green on GitHub for `capstone/aura-forge`.

The first failed run and first repaired green run are preserved. The terminal current green run proves:

- policy gate passes;
- evaluation gate passes;
- pipeline integrity passes;
- advisory review degrades safely;
- audit trail completes.
