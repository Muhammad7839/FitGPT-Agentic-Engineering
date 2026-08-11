import json
import sys
import importlib.util
from pathlib import Path


def _load_builder():
    script = Path(__file__).resolve().parents[1] / "scripts" / "build-change-passport.py"
    spec = importlib.util.spec_from_file_location("build_change_passport", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load_builder()


def test_real_high_evidence_produces_expected_fields():
    passport = builder.build_passport(Path("."), "AF-HIGH-001")
    builder.validate_passport(passport, Path("."))

    assert passport["schema_version"] == "change-passport-v1"
    assert passport["classification"]["classifier_version"] == "aura-risk-v1"
    assert passport["classification"]["risk_tier"] == "HIGH"
    assert passport["route"]["router_version"] == "aura-router-v1"
    assert passport["route"]["route_id"] == "aura-high-v1"
    assert passport["change"]["quality_score"] == "16/16"
    assert passport["measurements"]["total_cost_usd"] == 1.1061042
    assert passport["tooling"]["authorization_denial_count"] == 0
    assert passport["human_approval_events"]


def test_unavailable_ci_evidence_is_not_fabricated():
    passport = builder.build_passport(Path("."), "AF-LOW-001")
    assert "ci" not in passport
    assert "github_actions" not in passport


def test_real_ci_metadata_adds_github_actions_fields(tmp_path):
    run_root = tmp_path / ".eval-artifacts/capstone/aura-runs/AF-X/precheck-001"
    run_root.mkdir(parents=True)
    scenario_root = tmp_path / ".eval-artifacts/capstone/aura-runs/AF-X"
    (scenario_root / "final-successful-route-metrics.json").write_text(
        json.dumps(
            {
                "route": ["Implementer", "Reviewer"],
                "human_checkpoints": 0,
                "tool_event_count": 2,
                "authorization_denial_count": 0,
                "total_cost_usd": 0.01,
                "duration_ms": 10,
                "duration_api_ms": 9,
                "deterministic_gates": {"focused_tests": "PASS"},
            }
        ),
        encoding="utf-8",
    )
    (scenario_root / "final-quality-score.json").write_text(
        json.dumps({"result": "PASS", "total": 16, "maximum": 16}),
        encoding="utf-8",
    )
    (run_root / "classifier-router-output.json").write_text(
        json.dumps(
            {
                "classifier": {
                    "classifier_version": "aura-risk-v1",
                    "tier": "LOW",
                    "triggered_rules": [],
                    "normalized_paths": ["docs/example.md"],
                },
                "router": {"router_version": "aura-router-v1", "route_id": "aura-low-v1"},
            }
        ),
        encoding="utf-8",
    )
    artifact_root = tmp_path / "ci" / "artifacts"
    (artifact_root / "advisory-review").mkdir(parents=True)
    (artifact_root / "policy-tests").mkdir()
    (artifact_root / "evaluation-gate").mkdir()
    (artifact_root / "pipeline-integrity").mkdir()
    (artifact_root / "audit-trail").mkdir()
    (artifact_root / "advisory-review" / "advisory-review.json").write_text(
        json.dumps({"status": "SKIPPED", "reason": "AI SECRET UNAVAILABLE"}),
        encoding="utf-8",
    )
    (artifact_root / "policy-tests" / "policy-tests.txt").write_text("18 passed\n", encoding="utf-8")
    metadata = tmp_path / "ci" / "run-view.json"
    metadata.write_text(
        json.dumps(
            {
                "databaseId": 123,
                "url": "https://github.com/example/actions/runs/123",
                "headSha": "abc123",
                "status": "completed",
                "conclusion": "success",
                "jobs": [
                    {"name": "policy-tests", "conclusion": "success"},
                    {"name": "evaluation-gate", "conclusion": "success"},
                    {"name": "pipeline-integrity", "conclusion": "success"},
                    {"name": "audit-trail", "conclusion": "success"},
                ],
            }
        ),
        encoding="utf-8",
    )

    passport = builder.build_passport(
        tmp_path,
        "AF-X",
        ci_run_metadata=str(metadata),
        ci_artifact_root=str(artifact_root),
    )

    github = passport["ci"]["github_actions"]
    assert github["workflow_run_id"] == 123
    assert github["policy_status"] == "success"
    assert github["evaluation_status"] == "success"
    assert github["integrity_status"] == "success"
    assert github["advisory_status"] == "SKIPPED"


def test_missing_required_producer_fails(tmp_path):
    (tmp_path / ".eval-artifacts/capstone/aura-runs/AF-X/precheck-001").mkdir(parents=True)
    try:
        builder.build_passport(tmp_path, "AF-X")
    except builder.PassportError as exc:
        assert "missing required producer" in str(exc)
    else:
        raise AssertionError("missing producer should fail")


def test_path_traversal_reference_is_rejected(tmp_path):
    try:
        builder._safe_ref(tmp_path, "../outside.json")
    except builder.PassportError as exc:
        assert "escapes repository" in str(exc)
    else:
        raise AssertionError("path traversal should fail")


def test_output_is_deterministic_for_same_evidence_set():
    first = builder.build_passport(Path("."), "AF-MEDIUM-001")
    second = builder.build_passport(Path("."), "AF-MEDIUM-001")
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first["classification"]["classifier_version"] == "aura-risk-v1"
    assert first["measurements"]["total_cost_usd"] == 0.7300815
