# Reproducibility Runbook

This runbook lets a grader verify AURA Forge without paid model calls, production access, or secrets.

## Fast Path - Under 5 Minutes

From repository root:

```bash
pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py
pytest -q -p no:cacheprovider eval/test_ci_change_classifier.py eval/test_pipeline_integrity.py eval/test_audit_trail.py eval/test_change_passport.py
pytest -q -p no:cacheprovider eval/test_config_docs_consistency.py eval/test_governance_overreach.py
python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml
python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json
```

Expected local result from the final packaging run:

```text
81 passed
```

## Governed Runtime Path

The trusted local course image is:

```bash
agentic_engineer_4:latest
```

If needed, rebuild from the trusted repository Dockerfile:

```bash
docker build -t agentic_engineer_4:latest -f Dockerfile .
```

Run governed verification with a read-only workspace:

```bash
docker run --rm -i \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/workspace:ro" \
  -w /workspace \
  agentic_engineer_4:latest \
  pytest -q -p no:cacheprovider eval/test_policy.py eval/test_mcp_runtime.py eval/test_coursetools_runtime.py
```

Expected final local result:

```text
18 passed
```

Host Python may not have the MCP package installed. The governed runtime is the authoritative path for MCP/policy verification.

## Scenario Demonstration Path

Show deterministic classification and routing:

```bash
python3 - <<'PY'
from eval.risk_classifier import classify_change
from eval.adaptive_router import route_for_classification
scenarios = {
    "LOW": ["docs/features/accessibility.md"],
    "MEDIUM": ["web/src/utils/feedbackPrompts.test.js"],
    "HIGH": ["eval/risk_classifier.py", "mcp/coursetools_server.py"],
}
for label, paths in scenarios.items():
    classification = classify_change(paths)
    route = route_for_classification(classification)
    print(label, classification["tier"], route["route_id"], " -> ".join(route["roles"]))
PY
```

Expected route IDs:

- `LOW` -> `aura-low-v1`
- `MEDIUM` -> `aura-medium-v1`
- `HIGH` -> `aura-high-v1`

## Governance Denial Demo

Inspect the real denial:

```bash
sed -n '1,180p' docs/capstone/governance-overreach-demo.md
pytest -q -p no:cacheprovider eval/test_governance_overreach.py
```

The denial ID is `GO-20260811-001`.

## GitHub CI Evidence

Terminal verified run:

`https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31513596822`

Expected statuses:

- `policy-tests`: success
- `evaluation-gate`: success
- `pipeline-integrity`: success
- `advisory-review`: success with `SKIPPED - AI SECRET UNAVAILABLE`
- `audit-trail`: success

## Safety

No production environment is required. No deterministic gate requires secrets. Advisory AI review safely skips when its optional secret is unavailable. Do not deploy to Render or Vercel for grading.
