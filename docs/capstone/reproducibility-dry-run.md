# Final Reproducibility Dry Run

Date: 2026-08-11

Scope: safe deterministic verification only. No paid agent workflows, no production access, no LaunchCode portal interaction, and no locked holdout conversations were run.

## Commands and results

| Check | Command | Result |
|---|---|---|
| Risk classifier, router, control harness, CI integrity/audit, Change Passport, deterministic conversion, governance denial | `pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py eval/test_ci_change_classifier.py eval/test_pipeline_integrity.py eval/test_audit_trail.py eval/test_change_passport.py eval/test_config_docs_consistency.py eval/test_governance_overreach.py` | `82 passed` |
| Pipeline integrity | `python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml` | `PASS` |
| Change Passport generation | `python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json` | Passed and emitted valid JSON |
| Demo helper | `bash -n scripts/capstone-demo.sh && ./scripts/capstone-demo.sh all` | Passed |
| Governed Docker runtime | `docker run --rm -i -e PYTHONDONTWRITEBYTECODE=1 -v "$PWD:/workspace:ro" -w /workspace agentic_engineer_4:latest pytest -q -p no:cacheprovider eval/test_policy.py eval/test_mcp_runtime.py eval/test_coursetools_runtime.py` | `18 passed` |
| JSON parse | Parse all repository JSON files outside ignored dependency/cache folders | `224` files valid |
| GitHub workflow YAML parse | Parse `.github/workflows/*.yml` | `2` files valid |
| PPTX structure | Inspect final PowerPoint zip for slides and notes | `10` slides, `10` notes |
| PDF and contact sheet | `file docs/capstone/submission/AURA_Forge_Final_Presentation.pdf docs/capstone/submission/AURA_Forge_Slide_Preview.png` | PDF has `10 pages`; contact sheet is PNG |
| Secret scan | Submission-facing docs/scripts scanned for common token/key patterns | `SECRET_FINDINGS 0` |
| Forbidden file scan | Submission-facing docs checked for `.env`, key/cert files, and credential/token filenames | `FORBIDDEN_FILES 0` |
| Whitespace | `git diff --check` | Passed |
| Holdout integrity | `shasum -a 256 docs/holdout-task-set.md` | `e3aa9cdcec7b643507b7dd6f03ea15d92cfb6ed5fcacc4f56f5b2a8631631f32` |

## Missing prerequisite or workaround

No missing prerequisite blocked the safe deterministic dry run. The governed Docker path requires local image `agentic_engineer_4:latest`; it was available during this pass.

## Unclear instruction found

No runbook ambiguity blocked the fast path. The runbook was updated to include the new LOW-to-HIGH escalation regression.

## Not run

- Locked holdout conversations.
- Paid model or advisory AI calls.
- Production smoke tests.
- LaunchCode portal actions.
- Video recording or upload.
