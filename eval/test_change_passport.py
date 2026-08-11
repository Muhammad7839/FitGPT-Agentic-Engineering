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
