"""CI-facing adapter for deterministic AURA Forge classification.

This module reuses ``aura-risk-v1`` and ``aura-router-v1``. It adds CI-specific
booleans used by the workflow without creating a second risk system.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import PurePosixPath
from typing import Iterable

from adaptive_router import build_route_plan, route_to_dict
from risk_classifier import classify_change


AGENTIC_PREFIXES = (
    ".claude/agents/",
    ".claude/skills/",
    "mcp/",
    "mcp-servers/",
    "eval/",
)

EVALUATION_PREFIXES = (
    ".claude/agents/",
    ".claude/skills/",
    "mcp/",
    "mcp-servers/",
    "eval/",
    "scripts/",
)

PERMANENT_GUARDRAIL_PATHS = {
    ".github/workflows/ci.yml",
    ".github/workflows/test.yml",
    "eval/test_policy.py",
    "eval/test_mcp_runtime.py",
    "eval/test_coursetools_runtime.py",
    "eval/risk_classifier.py",
    "eval/adaptive_router.py",
    "eval/ci_change_classifier.py",
    "scripts/check-pipeline-integrity.py",
    "scripts/build-audit-trail.py",
}

PERMANENT_GUARDRAIL_PREFIXES = (
    ".github/workflows/",
    "mcp/",
    "mcp-servers/",
)


def classify_for_ci(changed_paths: Iterable[str]) -> dict[str, object]:
    paths = tuple(changed_paths)
    classification = classify_change(paths)
    route = build_route_plan(classification)
    normalized = classification.normalized_paths

    affects_agentic_surface = any(_starts_with(path, AGENTIC_PREFIXES) for path in normalized)
    affects_governance_or_ci = any(
        _is_guardrail(path) or path.startswith("docs/capstone/") or path.startswith("docs/adr/")
        for path in normalized
    )
    should_run_evaluation = classification.tier == "HIGH" or any(
        _starts_with(path, EVALUATION_PREFIXES) for path in normalized
    )
    modifies_permanent_guardrails = any(_is_guardrail(path) for path in normalized)
    affects_ci = any(path.startswith(".github/workflows/") for path in normalized)

    return {
        "schema_version": "ci-change-classification-v1",
        "classifier_version": classification.classifier_version,
        "router_version": route.router_version,
        "risk_tier": classification.tier,
        "route_id": route.route_id,
        "triggered_rules": list(classification.triggered_rules),
        "normalized_paths": list(normalized),
        "affects_agentic_surface": affects_agentic_surface,
        "affects_governance_or_ci": affects_governance_or_ci,
        "affects_ci": affects_ci,
        "should_run_evaluation": should_run_evaluation,
        "modifies_permanent_guardrails": modifies_permanent_guardrails,
        "route": route_to_dict(route),
    }


def _starts_with(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefix) for prefix in prefixes)


def _is_guardrail(path: str) -> bool:
    name = PurePosixPath(path).name
    return (
        path in PERMANENT_GUARDRAIL_PATHS
        or _starts_with(path, PERMANENT_GUARDRAIL_PREFIXES)
        or name in {"ci.yml", "test.yml"}
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Classify changed paths for AURA Forge CI.")
    parser.add_argument("paths", nargs="*", help="Changed paths. If omitted, newline paths are read from stdin.")
    parser.add_argument("--output", help="Write JSON output to this path.")
    args = parser.parse_args(argv)

    paths = args.paths or [line.strip() for line in sys.stdin if line.strip()]
    result = classify_for_ci(paths)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
