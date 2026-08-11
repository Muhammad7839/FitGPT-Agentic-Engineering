# Monitoring and Incident Runbook

This runbook applies to the isolated AURA Forge capstone workflow. It is not a production FitGPT deployment runbook.

## Monitored Signals

| Signal | Source | Action threshold |
|---|---|---|
| Policy gate failure | GitHub Actions `policy-tests` | Stop. Do not merge until failure is diagnosed and fixed. |
| Evaluation gate failure | GitHub Actions `evaluation-gate` | Stop. Determine whether the failure is workflow config, dependency, or real regression. |
| Pipeline integrity failure | GitHub Actions `pipeline-integrity` | Stop. Treat as guardrail weakening until proven otherwise. |
| Advisory unavailable | GitHub Actions `advisory-review` | Continue if permanent gates pass and artifact says `SKIPPED - AI SECRET UNAVAILABLE`. |
| Audit trail failure | GitHub Actions `audit-trail` | Stop for evidence repair unless upstream permanent failure already explains unavailable artifacts. |
| Role overreach denial | MCP authorization result | Expected for unauthorized attempts; preserve denial as safety evidence. |
| Holdout checksum mismatch | `shasum -a 256 docs/holdout-task-set.md` | Stop. Restore integrity without rewriting history. |
| Secret-pattern finding | local credential scan or GitHub secret scanning | Stop. Do not push further. Rotate if a real secret was exposed. |

## Incident Steps

1. Classify the incident as policy/eval/integrity, advisory-only, audit/evidence, environment/dependency, or security.
2. Preserve the failed run ID, commit SHA, failing job, and sanitized log excerpt.
3. Reproduce locally where possible without production access.
4. Apply the smallest evidence-backed fix.
5. Run local deterministic verification.
6. Commit normally on `capstone/aura-forge`.
7. Push normally to `origin/capstone/aura-forge`.
8. Confirm the next GitHub run passes permanent gates.

## Rollback Path

If a fix worsens the system, create a normal revert commit on `capstone/aura-forge` and rerun CI. Do not force-push or rewrite evidence history.

## Tested Examples

- Run `31512923419` failed because `evaluation-gate` lacked `pytest` and audit handling assumed an unavailable integrity artifact. Commit `92d60c4` repaired both issues and the next run passed.
- Controlled tool-evolution commit `7c666e5` intentionally weakened the permanent policy gate. The integrity checker rejected the change. Commit `4e446f6` restored the contract.
- Local pipeline-integrity demo `PI-20260811-001` added `continue-on-error: true` to `policy-tests` in a detached worktree. The checker returned `FAIL`.

## Graceful Degradation

Advisory AI review is optional. If `AURA_ADVISORY_AI_KEY` is unavailable, the workflow produces an explicit sanitized skip artifact and permanent gates continue.

No production service, production database, production secret, or live user is required for any deterministic gate.
