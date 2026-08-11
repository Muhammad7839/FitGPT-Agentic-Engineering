#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'USAGE'
AURA Forge capstone demo helper.

Usage:
  ./scripts/capstone-demo.sh --help
  ./scripts/capstone-demo.sh classifier
  ./scripts/capstone-demo.sh routes
  ./scripts/capstone-demo.sh denial
  ./scripts/capstone-demo.sh ci
  ./scripts/capstone-demo.sh passport
  ./scripts/capstone-demo.sh all

This helper is deterministic. It does not call paid models, contact upstream,
modify files, expose secrets, or deploy anything.
USAGE
}

classifier() {
  cd "$ROOT_DIR"
  PYTHONPATH="$ROOT_DIR/eval" python3 - <<'PY'
from risk_classifier import classify_change

examples = [
    ("AF-LOW-001", ["docs/features/accessibility.md"]),
    ("AF-MEDIUM-001", ["web/src/utils/feedbackPrompts.js", "web/src/utils/feedbackPrompts.test.js"]),
    ("AF-HIGH-001", ["eval/test_policy.py", "mcp-servers/storage/allow-list.json"]),
]

for name, paths in examples:
    result = classify_change(paths, metadata={"scenario_id": name})
    print(f"{name}: {result.tier} ({result.classifier_version})")
PY
}

routes() {
  cd "$ROOT_DIR"
  PYTHONPATH="$ROOT_DIR/eval" python3 - <<'PY'
from adaptive_router import build_route_plan
from risk_classifier import classify_change

examples = [
    ("AF-LOW-001", ["docs/features/accessibility.md"]),
    ("AF-MEDIUM-001", ["web/src/utils/feedbackPrompts.js", "web/src/utils/feedbackPrompts.test.js"]),
    ("AF-HIGH-001", ["eval/test_policy.py", "mcp-servers/storage/allow-list.json"]),
]

for name, paths in examples:
    classification = classify_change(paths, metadata={"scenario_id": name})
    route = build_route_plan(classification, scenario_metadata={"scenario_id": name}, relevant_paths=paths)
    print(f"{name}: {route.route_id}")
    print(f"  roles: {', '.join(route.model_roles)}")
    print(f"  human checkpoints: {len(route.human_checkpoints)}")
    print(f"  deterministic gates: {', '.join(g.name for g in route.deterministic_gates)}")
PY
}

denial() {
  cat <<'DENIAL'
Governance denial evidence
Demo ID: GO-20260811-001
Role: implementer
Attempted tool: task_tracker
Decision: DENIED
Reason: only project-manager is allow-listed
External state changed: No
Model cost: $0

Sanitized denial:
Authorization error: role 'implementer' is not on the allow-list for task_tracker. Allowed roles: ['project-manager'].

Source:
docs/capstone/governance-overreach-demo.md
DENIAL
}

ci() {
  cat <<'CI'
GitHub Actions evidence
Workflow: AURA Forge Governance CI
Final run: 31517900793
Run URL: https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31517900793

Permanent gates:
- change-classifier: PASS
- policy-tests: PASS
- evaluation-gate: PASS
- pipeline-integrity: PASS
- audit-trail: PASS
- advisory-review: safe graceful skip when AI secret unavailable

Source:
docs/capstone/governance-ci-results.md
CI
}

passport() {
  cd "$ROOT_DIR"
  python3 - <<'PY'
import json
from pathlib import Path

path = Path("docs/capstone/evidence/change-passport-AF-HIGH-001.json")
data = json.loads(path.read_text(encoding="utf-8"))

print("Change Passport evidence")
print(f"Path: {path}")
print(f"Scenario: {data['change']['scenario_id']}")
print(f"Readiness: {data['change']['final_readiness_result']}")
print(f"Quality: {data['change']['quality_score']}")
print(f"Risk tier: {data['classification']['risk_tier']}")
print(f"Route: {data['route']['route_id']}")
print(f"Roles: {', '.join(data['route']['ordered_roles'])}")
print(f"Human checkpoints: {data['route']['human_checkpoint_count']}")
print(f"Policy result: {data['policy_result']}")
print(f"CI status: {data['ci']['github_actions']['conclusion']}")
PY
}

case "${1:-}" in
  --help|-h|"")
    usage
    ;;
  classifier)
    classifier
    ;;
  routes)
    routes
    ;;
  denial)
    denial
    ;;
  ci)
    ci
    ;;
  passport)
    passport
    ;;
  all)
    classifier
    printf '\n'
    routes
    printf '\n'
    denial
    printf '\n'
    ci
    printf '\n'
    passport
    ;;
  *)
    echo "Unknown command: $1" >&2
    usage >&2
    exit 2
    ;;
esac
