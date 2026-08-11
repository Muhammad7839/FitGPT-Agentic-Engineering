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

## Failure Response Matrix

| Failure type | Signal | Severity | Immediate action | Owner/role | Rollback/escalation step | Evidence to capture | Recovery verification |
|---|---|---|---|---|---|---|---|
| Classifier failure | `eval/test_risk_classifier.py` failure or unexpected `risk_tier` in CI classification artifact | High | Stop routing. Treat unknown or malformed evidence as HIGH until fixed. | Tester, then Reviewer | Revert classifier rule change or route to HIGH with `ESCALATION REQUIRED`. | Paths, metadata, triggered rules, failing test output. | `pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_ci_change_classifier.py` |
| Router malformed output | `eval/test_adaptive_router.py` failure, missing route ID, missing gates, or unknown tier | High | Stop. Do not allow role execution from malformed plan. | Tester | Revert router change or preserve failed evidence and require plan approval. | Classifier result, route dict, failing assertion. | `pytest -q -p no:cacheprovider eval/test_adaptive_router.py` |
| Policy gate failure | GitHub `policy-tests` failure or local policy/MCP failure | Blocking | Stop. Do not merge or mark ready. | Tester, Reviewer | Revert permission widening or repair allow-list/test mismatch. | Run ID, job log, changed grant files, policy report. | Governed Docker `eval/test_policy.py eval/test_mcp_runtime.py eval/test_coursetools_runtime.py` |
| Evaluation failure | GitHub `evaluation-gate` failure or local eval regression | Blocking | Stop. Separate environment failure from real regression. | Tester | Revert the change if regression is real; repair workflow if environment/config failure. | Run ID, failing test names, sanitized log excerpt. | Relevant focused pytest plus CI green evaluation gate. |
| MCP authorization denial | Denial from governed MCP layer | Expected when unauthorized; high if unexpected for an allowed role | Preserve denial. Confirm no external state changed. | Reviewer, Project Manager for allowed-role disputes | If denial is expected, keep as safety evidence. If unexpected, escalate to HIGH and inspect allow-list. | Role, tool, decision, reason, external-state flag. | `pytest -q -p no:cacheprovider eval/test_governance_overreach.py eval/test_policy.py` |
| GitHub CI environment failure | Missing command, missing dependency, skipped required artifact | Medium to blocking depending on job | Preserve run. Repair workflow prerequisites without changing measured results. | Tester | Normal fix commit; do not force-push. | Run ID, job name, exact missing prerequisite, artifact behavior. | Next GitHub Actions run passes permanent gates. |
| Advisory AI unavailable | Advisory artifact says `SKIPPED - AI SECRET UNAVAILABLE` | Low if permanent gates pass | Continue. Do not fabricate model review. | Reviewer | None unless advisory becomes blocking or secret is exposed. | Advisory artifact and audit-trail summary. | Permanent gates pass and audit records advisory skip. |
| Change Passport producer missing | `scripts/build-change-passport.py` or `eval/test_change_passport.py` reports missing producer | High for submission evidence | Stop. Do not manually fill missing fields. | Tester, Project Manager | Regenerate from real producers or leave field absent with explanation. | Missing producer path, scenario ID, builder error. | `pytest -q -p no:cacheprovider eval/test_change_passport.py` and successful Passport generation. |
| Secret or forbidden file finding | Secret scan or forbidden-file scan flags submission-facing artifact | Blocking | Stop. Do not push. Remove or sanitize; rotate if a real secret was exposed. | Project Manager | If already pushed, follow credential rotation/history remediation outside this capstone run. | File path only; do not print secret value. | Secret scan returns zero findings. |

## Rollback Path

If a fix worsens the system, create a normal revert commit on `capstone/aura-forge` and rerun CI. Do not force-push or rewrite evidence history.

## Tested Examples

- Run `31512923419` failed because `evaluation-gate` lacked `pytest` and audit handling assumed an unavailable integrity artifact. Commit `92d60c4` repaired both issues and the next run passed.
- Controlled tool-evolution commit `7c666e5` intentionally weakened the permanent policy gate. The integrity checker rejected the change. Commit `4e446f6` restored the contract.
- Local pipeline-integrity demo `PI-20260811-001` added `continue-on-error: true` to `policy-tests` in a detached worktree. The checker returned `FAIL`.
- Local escalation regression `eval/test_adaptive_router.py::test_low_route_observing_high_sensitive_path_fails_closed_with_escalation` proves a LOW route observing `mcp/coursetools_server.py` returns `ESCALATION REQUIRED` evidence instead of silently continuing.

## Graceful Degradation

Advisory AI review is optional. If `AURA_ADVISORY_AI_KEY` is unavailable, the workflow produces an explicit sanitized skip artifact and permanent gates continue.

No production service, production database, production secret, or live user is required for any deterministic gate.
