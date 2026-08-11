import json
from pathlib import Path


def test_governance_overreach_denial_artifact_is_real_and_sanitized():
    artifact = Path(".eval-artifacts/capstone/governance-overreach/GO-20260811-001/overreach-output.json")
    assert artifact.exists()
    data = json.loads(artifact.read_text(encoding="utf-8"))

    assert data["schema_version"] == "governance-overreach-demo-v1"
    assert data["demo_id"] == "GO-20260811-001"
    assert data["role"] == "implementer"
    assert data["attempted_tool"] == "task_tracker"
    assert data["status"] == "DENIED"
    assert data["external_state_changed"] is False
    assert data["model_cost_usd"] == 0
    assert "not on the allow-list" in data["sanitized_denial"]
    assert "project-manager" in data["sanitized_denial"]
