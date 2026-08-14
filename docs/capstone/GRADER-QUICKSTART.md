# Grader Quickstart

## 60-second overview

AURA Forge is a governed adaptive engineering workflow around FitGPT. It classifies each repository change as `LOW`, `MEDIUM`, or `HIGH`, routes the change through the minimum justified mix of agents, deterministic gates, and human approvals, and produces machine-checkable evidence.

The measured capstone claim is bounded: across three representative scenarios, quality improved from `44/48` to `48/48`, successful-route cost dropped `19.22%`, model roles dropped `33.33%`, and human checkpoints dropped `50%`.

## Top evidence

- Rubric audit: `docs/capstone/final-rubric-audit.md`
- Evidence index: `docs/capstone/evidence-index.md`
- PRD: `docs/capstone/aura-forge-prd.md`
- Impact report: `docs/capstone/control-vs-aura-impact.md`
- Final presentation: `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`
- Final walkthrough video: https://youtu.be/WxEXCWC75vs

## Fast deterministic verification

```bash
pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py
pytest -q -p no:cacheprovider eval/test_ci_change_classifier.py eval/test_pipeline_integrity.py eval/test_audit_trail.py eval/test_change_passport.py
pytest -q -p no:cacheprovider eval/test_config_docs_consistency.py eval/test_governance_overreach.py
python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml
python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json
```

## Real governance denial

Evidence: `docs/capstone/governance-overreach-demo.md`

Command:

```bash
./scripts/capstone-demo.sh denial
```

Expected story: role `implementer` attempted `task_tracker`; the governed authorization layer returned `DENIED`; external state changed `No`; model cost `$0`.

## Real GitHub CI

Evidence: `docs/capstone/governance-ci-results.md`

Known passed governance runs include:

- run `31513596822`: CI-backed Change Passport source run.
- run `31520499134`: verified submission-package evidence run used in the deck.
- run `31527786959`: passed after the final presentation visual repair commit.

Use the latest run on branch `capstone/aura-forge` for current branch health.

## Measured impact

Evidence: `docs/capstone/control-vs-aura-impact.md`

No production-wide savings are claimed. The numbers apply only to the three local representative capstone scenarios.

## Change Passport

Evidence file: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`

Generator:

```bash
python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json
```

## Right-tool conversion

Evidence: `docs/capstone/deterministic-conversion.md`

The stable `DATABASE_URL` docs/config check was converted from agentic review to deterministic code with `$0` model cost.

## ADRs

- ADR folder: `docs/adr/`
- Evidence matrix: `docs/capstone/adr-evidence-matrix.md`
- Tool-choice matrix: `docs/capstone/right-tool-decision-matrix.md`

## Final presentation

- Gamma PDF: `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`
- Teleprompter: `docs/capstone/submission/AURA_Forge_TELEPROMPTER.md`
- Video staging: `docs/capstone/submission/VIDEO-EVIDENCE-STAGING.md`

## Limitations

- The sandbox is bounded and uses read-only verification paths, but network egress is not proven airtight.
- The tool-evolution drill includes intentional fault injection; it should not be misrepresented as an unobserved spontaneous regression.
- No production deployment or live FitGPT mutation is part of this capstone.
