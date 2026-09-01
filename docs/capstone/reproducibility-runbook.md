# Reproducibility Runbook

This runbook lets a grader verify AURA Forge without paid model calls, production access, or secrets.

## Fast Path - Under 5 Minutes

From repository root:

```bash
pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py
pytest -q -p no:cacheprovider eval/test_ci_change_classifier.py eval/test_pipeline_integrity.py eval/test_audit_trail.py eval/test_change_passport.py
pytest -q -p no:cacheprovider eval/test_config_docs_consistency.py eval/test_governance_overreach.py
pytest -q -p no:cacheprovider eval/test_retrieval_behavior.py eval/test_reliability_controls.py eval/test_sandbox_contract.py
python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml
python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json
```

Expected local result from the final packaging run:

```text
Run the commands above and use their current output as the result. The historical `82 passed` count is no longer authoritative because permanent coverage has expanded.
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

Run the complete governed verification with a read-only root filesystem, read-only workspace, no network, no Linux capabilities, no credential mount, bounded CPU/memory/processes, and a unique container name:

```bash
./scripts/run-offline-governance-verification.sh
```

Expected final local result:

```text
Current revision result:

```text
32 passed
```

The earlier `18 passed` count predates the retrieval, reliability, and sandbox-contract tests.
```

Host Python may not have the MCP package installed. The governed runtime is the authoritative path for MCP/policy verification.

For parallel sessions, each invocation generates a unique container name from UTC time and its process ID. A caller may provide a unique `AURA_VERIFY_RUN_ID`; duplicate active names fail instead of sharing a container.

The offline verifier needs no Claude authentication volume and performs no paid model call.

## Scenario Demonstration Path

Show deterministic classification and routing:

```bash
PYTHONPATH=eval python3 - <<'PY'
from risk_classifier import classify_change
from adaptive_router import build_route_plan
scenarios = {
    "LOW": ["docs/features/accessibility.md"],
    "MEDIUM": ["web/src/utils/feedbackPrompts.test.js"],
    "HIGH": ["eval/risk_classifier.py", "mcp/coursetools_server.py"],
}
for label, paths in scenarios.items():
    classification = classify_change(paths)
    route = build_route_plan(classification)
    print(label, classification.tier, route.route_id, " -> ".join(route.model_roles))
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

## Escalation / Rollback Check

The adaptive router has a fail-closed escalation test for LOW work that observes a HIGH-sensitive path during implementation:

```bash
pytest -q -p no:cacheprovider eval/test_adaptive_router.py::test_low_route_observing_high_sensitive_path_fails_closed_with_escalation
```

Expected result:

```text
1 passed
```

This is regression/governance coverage only. It does not change the frozen measured AURA scenario results.

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
