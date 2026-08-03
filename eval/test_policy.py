"""Static policy checks for the Module 4 governance baseline."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "governance-policy.md"
STORAGE_ALLOW_LIST = ROOT / "mcp-servers" / "storage" / "allow-list.json"
RETRIEVAL_ALLOW_LIST = ROOT / "mcp-servers" / "retrieval" / "allow-list.json"
RUN_AGENT = ROOT / "scripts" / "run-agent.sh"
SKILL_DIR = ROOT / ".claude" / "skills"


def _json_block(path: Path, start: str, end: str) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"{re.escape(start)}\s*(.*?)\s*{re.escape(end)}", text, re.S)
    assert match, f"missing JSON block in {path}"
    return json.loads(match.group(1))


def policy() -> dict:
    return _json_block(POLICY_PATH, "GOVERNANCE_POLICY_JSON_START", "GOVERNANCE_POLICY_JSON_END")


def skill_scope(skill: str) -> dict:
    return _json_block(SKILL_DIR / skill / "SKILL.md", "ACTIVATION_SCOPE_JSON_START", "ACTIVATION_SCOPE_JSON_END")


def role_policy(role: str) -> dict:
    return policy()["roles"][role]


def test_policy_json_is_valid_and_complete():
    data = policy()
    assert data["version"] == "v1.0.0"
    assert data["classification_order"] == ["public", "internal", "confidential"]
    assert set(data["storage_operations"]) == {
        "write_entry",
        "read_entry",
        "list_entries",
        "update_entry",
        "delete_entry",
        "audit_read",
    }
    assert set(data["skills"]) == {"run-tests", "draft-pr-description", "summarize-session"}
    assert "orchestrator" in data["roles"]


def test_every_governed_role_has_definition():
    for role, spec in policy()["roles"].items():
        defined_in = ROOT / spec["defined_in"]
        assert defined_in.exists(), f"{role} definition missing: {spec['defined_in']}"


def test_active_agent_definitions_have_policy_when_in_governed_workflow():
    governed = set(policy()["roles"])
    for path in (ROOT / ".claude" / "agents").glob("*.md"):
        name = path.stem
        if name in {"planner", "implementer", "reviewer", "tester", "project-manager"}:
            assert name in governed


def test_storage_allow_list_matches_policy():
    allow = json.loads(STORAGE_ALLOW_LIST.read_text(encoding="utf-8"))
    expected = {
        role: {op: bool(details["grant"]) for op, details in spec["mcp_storage"].items()}
        for role, spec in policy()["roles"].items()
    }
    assert allow == expected


def test_retrieval_allow_list_matches_policy():
    allow = json.loads(RETRIEVAL_ALLOW_LIST.read_text(encoding="utf-8"))
    expected = {
        role: {
            "retrieve": bool(spec["mcp_retrieval"]["retrieve"]),
            "ceiling": spec["mcp_retrieval"]["ceiling"],
        }
        for role, spec in policy()["roles"].items()
    }
    assert allow == expected


def test_skill_scopes_match_policy():
    for skill in policy()["skills"]:
        scope = skill_scope(skill)
        expected_allowed = sorted(
            role
            for role, spec in policy()["roles"].items()
            if spec["skills"][skill]["grant"]
        )
        expected_denied = sorted(set(policy()["roles"]) - set(expected_allowed))
        assert sorted(scope["allowed_roles"]) == expected_allowed
        assert sorted(scope["denied_roles"]) == expected_denied


def test_container_workspace_modes_match_policy():
    script = RUN_AGENT.read_text(encoding="utf-8")
    for role, spec in policy()["roles"].items():
        workspace = spec["container"]["workspace"]
        expected_mode = "rw" if workspace == "read-write" else "ro"
        assert re.search(rf"(^|\|)\s*{re.escape(role)}(\)|\|).*?WORKSPACE_MODE=\"{expected_mode}\"", script, re.S | re.M), role


def test_container_memory_decisions_match_policy():
    script = RUN_AGENT.read_text(encoding="utf-8")
    for role, spec in policy()["roles"].items():
        assert spec["container"]["memory"] == "omitted", role
    assert 'MEMORY_MODE="omit"' in script
    assert "/memory" in script


def test_unknown_roles_are_denied_by_startup_script():
    script = RUN_AGENT.read_text(encoding="utf-8")
    assert "Unknown or ungoverned role" in script
    assert "exit 66" in script


def test_no_role_receives_undocumented_storage_operation():
    documented = set(policy()["storage_operations"])
    for role, grants in json.loads(STORAGE_ALLOW_LIST.read_text(encoding="utf-8")).items():
        assert role in policy()["roles"]
        assert set(grants) == documented


def test_no_role_exceeds_classification_ceiling():
    order = policy()["classification_order"]
    allow = json.loads(RETRIEVAL_ALLOW_LIST.read_text(encoding="utf-8"))
    for role, rule in allow.items():
        ceiling = rule["ceiling"]
        if rule["retrieve"]:
            assert ceiling in order
        else:
            assert ceiling == "none"


def test_read_only_roles_have_no_state_changing_storage_grants():
    read_only_roles = [
        role
        for role, spec in policy()["roles"].items()
        if spec["container"]["workspace"] == "read-only"
    ]
    allow = json.loads(STORAGE_ALLOW_LIST.read_text(encoding="utf-8"))
    for role in read_only_roles:
        assert allow[role]["write_entry"] is False
        assert allow[role]["update_entry"] is False
        assert allow[role]["delete_entry"] is False


def test_project_manager_cannot_run_tests():
    assert role_policy("project-manager")["skills"]["run-tests"]["grant"] is False


def test_reviewer_cannot_run_tests():
    assert role_policy("reviewer")["skills"]["run-tests"]["grant"] is False


def test_tester_cannot_update_external_state():
    tester = role_policy("tester")
    assert tester["mcp_storage"]["write_entry"]["grant"] is False
    assert tester["mcp_storage"]["update_entry"]["grant"] is False
    assert tester["mcp_storage"]["delete_entry"]["grant"] is False
    assert tester["skills"]["draft-pr-description"]["grant"] is False


def test_implementer_cannot_delete_stored_state():
    assert role_policy("implementer")["mcp_storage"]["delete_entry"]["grant"] is False
