"""Fixed-route pre-AURA control harness.

This module is an experimental baseline instrument. It generalizes the old
COURSE-FITGPT-001 route just enough to accept a bounded scenario definition
while preserving the same role order, checkpoints, and tool grants for every
scenario.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FIXED_ROUTE = ("planner", "implementer", "reviewer", "tester", "project-manager")
PLAN_APPROVAL_AFTER = "planner"
FINAL_APPROVAL_AFTER = "tester"
CONTROL_WORKTREE_ROOT = Path("/Users/muhammad/course-projects/aura-forge-control").resolve()
PRIMARY_REPOSITORY = Path("/Users/muhammad/course-projects/FitGPT-Agentic-Engineering").resolve()
PROTECTED_OR_PRODUCTION_MARKERS = (
    "fitgpt.tech",
    "render.com",
    "vercel.app",
    "postgres://",
    "postgresql://",
    "mongodb://",
    "mysql://",
)
PROTECTED_RELATIVE_PREFIXES = (
    ".git/",
    ".github/workflows/",
    ".env",
    "backend/.env",
)
DEFAULT_TOOL_GRANTS = {
    "orchestrator": ("Agent",),
    "planner": ("mcp__coursetools__file_read",),
    "implementer": ("mcp__coursetools__file_read", "mcp__coursetools__file_write"),
    "reviewer": ("mcp__coursetools__file_read",),
    "tester": ("mcp__coursetools__file_read", "mcp__coursetools__test_runner"),
    "project-manager": ("mcp__coursetools__task_tracker",),
}


class ControlHarnessError(ValueError):
    """Raised when a scenario is outside the fixed-route control boundary."""


@dataclass(frozen=True)
class ScenarioInput:
    scenario_id: str
    request: str
    acceptance_criteria: tuple[str, ...]
    worktree: Path
    relevant_paths: tuple[str, ...]
    risk_label: str | None = None


def load_scenario(path: Path) -> ScenarioInput:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return scenario_from_dict(payload)


def scenario_from_dict(payload: dict[str, Any]) -> ScenarioInput:
    required = ("scenario_id", "request", "acceptance_criteria", "worktree")
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ControlHarnessError(f"missing required scenario field(s): {', '.join(missing)}")

    criteria = payload["acceptance_criteria"]
    if not isinstance(criteria, list) or not all(isinstance(item, str) and item.strip() for item in criteria):
        raise ControlHarnessError("acceptance_criteria must be a non-empty list of strings")

    relevant_paths = payload.get("relevant_paths", [])
    if not isinstance(relevant_paths, list) or not all(isinstance(item, str) and item.strip() for item in relevant_paths):
        raise ControlHarnessError("relevant_paths must be a list of strings")

    scenario = ScenarioInput(
        scenario_id=str(payload["scenario_id"]).strip(),
        request=str(payload["request"]).strip(),
        acceptance_criteria=tuple(item.strip() for item in criteria),
        worktree=Path(str(payload["worktree"])).expanduser().resolve(),
        relevant_paths=tuple(item.strip() for item in relevant_paths),
        risk_label=str(payload["risk_label"]).strip() if payload.get("risk_label") else None,
    )
    validate_scenario(scenario)
    return scenario


def validate_scenario(scenario: ScenarioInput) -> None:
    if not scenario.scenario_id:
        raise ControlHarnessError("scenario_id is required")
    if not scenario.request:
        raise ControlHarnessError("request is required")
    if scenario.worktree == PRIMARY_REPOSITORY:
        raise ControlHarnessError("control runs must not target the primary capstone worktree")
    if not _is_relative_to(scenario.worktree, CONTROL_WORKTREE_ROOT):
        raise ControlHarnessError(f"worktree must be under {CONTROL_WORKTREE_ROOT}")

    check_text = " ".join(
        [scenario.request, str(scenario.worktree), *scenario.relevant_paths]
    ).lower()
    if any(marker in check_text for marker in PROTECTED_OR_PRODUCTION_MARKERS):
        raise ControlHarnessError("scenario references a protected production target")

    for path in scenario.relevant_paths:
        normalized = path.replace("\\", "/").lstrip("/")
        if normalized.startswith("..") or "/../" in normalized:
            raise ControlHarnessError(f"relevant path escapes repository boundary: {path}")
        if any(normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in PROTECTED_RELATIVE_PREFIXES):
            raise ControlHarnessError(f"relevant path is protected for control execution: {path}")


def build_control_contract(scenario: ScenarioInput) -> dict[str, Any]:
    validate_scenario(scenario)
    return {
        "schema_version": "pre-aura-control-v1",
        "scenario_id": scenario.scenario_id,
        "task_request": scenario.request,
        "acceptance_criteria": list(scenario.acceptance_criteria),
        "worktree": str(scenario.worktree),
        "relevant_paths": list(scenario.relevant_paths),
        "measurement_metadata": {
            "risk_label": scenario.risk_label,
            "risk_label_used_for_routing": False,
        },
        "route": list(FIXED_ROUTE),
        "human_checkpoints": [
            {
                "kind": "plan",
                "after_role": PLAN_APPROVAL_AFTER,
                "before_role": "implementer",
                "required": True,
            },
            {
                "kind": "final",
                "after_role": FINAL_APPROVAL_AFTER,
                "before_role": "project-manager",
                "required": True,
            },
        ],
        "tool_grants": {role: list(tools) for role, tools in DEFAULT_TOOL_GRANTS.items()},
        "runtime_behavior": {
            "risk_classification": "not implemented",
            "adaptive_routing": False,
            "route_varies_by_risk_label": False,
        },
    }


def build_plan_approval_packet(contract: dict[str, Any]) -> str:
    criteria = "\n".join(f"- {item}" for item in contract["acceptance_criteria"])
    paths = "\n".join(f"- {item}" for item in contract["relevant_paths"]) or "- None supplied"
    route = " -> ".join(contract["route"])
    return (
        "# Plan Approval Required\n\n"
        f"Scenario: `{contract['scenario_id']}`\n\n"
        f"Worktree: `{contract['worktree']}`\n\n"
        f"Fixed route: {route}\n\n"
        "Risk label is measurement metadata only and was not used for routing.\n\n"
        "## Request\n\n"
        f"{contract['task_request']}\n\n"
        "## Relevant paths\n\n"
        f"{paths}\n\n"
        "## Acceptance criteria\n\n"
        f"{criteria}\n\n"
        "## Required human action\n\n"
        "Approve or reject the plan before the Implementer role runs."
    )


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
