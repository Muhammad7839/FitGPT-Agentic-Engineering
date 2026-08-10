from pathlib import Path

import pytest

from pre_aura_control import (
    CONTROL_WORKTREE_ROOT,
    DEFAULT_TOOL_GRANTS,
    FIXED_ROUTE,
    ControlHarnessError,
    build_control_contract,
    build_plan_approval_packet,
    scenario_from_dict,
)


def scenario_payload(risk_label="LOW", worktree=None):
    return {
        "scenario_id": "AF-LOW-001",
        "request": "Update a bounded documentation checklist.",
        "acceptance_criteria": ["Only the approved file changes."],
        "worktree": str(worktree or CONTROL_WORKTREE_ROOT / "AF-LOW-001"),
        "relevant_paths": ["docs/features/accessibility.md"],
        "risk_label": risk_label,
    }


def test_arbitrary_bounded_scenario_replaces_hard_coded_ticket():
    scenario = scenario_from_dict(
        {
            "scenario_id": "AF-CUSTOM-777",
            "request": "Make a bounded local-only documentation update.",
            "acceptance_criteria": ["Document the requested behavior."],
            "worktree": str(CONTROL_WORKTREE_ROOT / "AF-CUSTOM-777"),
            "relevant_paths": ["docs/features/system_overview.md"],
        }
    )
    contract = build_control_contract(scenario)

    assert contract["scenario_id"] == "AF-CUSTOM-777"
    assert contract["task_request"] == "Make a bounded local-only documentation update."
    assert "COURSE-FITGPT-001" not in str(contract)


def test_role_order_and_human_checkpoints_are_fixed():
    contract = build_control_contract(scenario_from_dict(scenario_payload()))

    assert tuple(contract["route"]) == FIXED_ROUTE
    assert contract["human_checkpoints"] == [
        {
            "kind": "plan",
            "after_role": "planner",
            "before_role": "implementer",
            "required": True,
        },
        {
            "kind": "final",
            "after_role": "tester",
            "before_role": "project-manager",
            "required": True,
        },
    ]


def test_risk_metadata_does_not_change_route():
    contracts = [
        build_control_contract(scenario_from_dict(scenario_payload(label)))
        for label in ("LOW", "MEDIUM", "HIGH")
    ]

    assert {tuple(contract["route"]) for contract in contracts} == {FIXED_ROUTE}
    assert all(
        contract["measurement_metadata"]["risk_label_used_for_routing"] is False
        for contract in contracts
    )


def test_same_task_with_three_risk_labels_has_same_contract_controls():
    fields = ("route", "human_checkpoints", "tool_grants", "runtime_behavior")
    contracts = [
        build_control_contract(scenario_from_dict(scenario_payload(label)))
        for label in ("LOW", "MEDIUM", "HIGH")
    ]

    for field in fields:
        assert contracts[0][field] == contracts[1][field] == contracts[2][field]


def test_existing_tool_grants_remain_unchanged():
    contract = build_control_contract(scenario_from_dict(scenario_payload()))

    assert contract["tool_grants"] == {
        role: list(tools) for role, tools in DEFAULT_TOOL_GRANTS.items()
    }


def test_scenario_worktree_boundary_is_required():
    with pytest.raises(ControlHarnessError, match="primary capstone worktree"):
        scenario_from_dict(
            scenario_payload(
                worktree=Path("/Users/muhammad/course-projects/FitGPT-Agentic-Engineering")
            )
        )


def test_production_targets_are_rejected():
    payload = scenario_payload()
    payload["request"] = "Deploy this to fitgpt.tech."

    with pytest.raises(ControlHarnessError, match="protected production"):
        scenario_from_dict(payload)


def test_protected_relative_paths_are_rejected():
    payload = scenario_payload()
    payload["relevant_paths"] = [".github/workflows/deploy.yml"]

    with pytest.raises(ControlHarnessError, match="protected"):
        scenario_from_dict(payload)


def test_plan_approval_packet_preserves_human_checkpoint():
    contract = build_control_contract(scenario_from_dict(scenario_payload()))
    packet = build_plan_approval_packet(contract)

    assert packet.startswith("# Plan Approval Required")
    assert "Approve or reject the plan before the Implementer role runs." in packet
    assert "Risk label is measurement metadata only" in packet
