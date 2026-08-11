import json
import sys
import importlib.util
from pathlib import Path


def _load_script(name):
    script = Path(__file__).resolve().parents[1] / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build_audit_trail = _load_script("build-audit-trail.py")
run_advisory_review = _load_script("run-advisory-review.py")


def test_audit_trail_uses_available_machine_evidence(tmp_path):
    classification = tmp_path / "classification.json"
    classification.write_text(json.dumps({"risk_tier": "HIGH", "route_id": "aura-high-v1"}), encoding="utf-8")
    integrity = tmp_path / "integrity.json"
    integrity.write_text(json.dumps({"status": "PASS", "failures": []}), encoding="utf-8")
    advisory = tmp_path / "advisory.json"
    advisory.write_text(json.dumps({"status": "SKIPPED", "reason": "AI SECRET UNAVAILABLE"}), encoding="utf-8")

    audit = build_audit_trail.build_audit_trail(
        output_dir=tmp_path / "audit",
        classification=classification,
        integrity=integrity,
        advisory=advisory,
        policy_status="success",
        evaluation_status="success",
    )

    assert audit["change_classification"]["risk_tier"] == "HIGH"
    assert audit["integrity_result"]["status"] == "PASS"
    assert audit["advisory_result"]["status"] == "SKIPPED"
    assert "github_status" not in audit


def test_audit_trail_marks_unavailable_producers_without_fabricating(tmp_path):
    audit = build_audit_trail.build_audit_trail(output_dir=tmp_path / "audit")
    assert audit["policy_result"] == "not_available"
    assert "change_classification" not in audit
    assert "integrity_result" not in audit


def test_advisory_review_gracefully_skips_without_secret(tmp_path, monkeypatch):
    monkeypatch.delenv("AURA_ADVISORY_AI_KEY", raising=False)
    artifact = run_advisory_review.build_advisory(tmp_path)
    assert artifact["status"] == "SKIPPED"
    assert artifact["reason"] == "AI SECRET UNAVAILABLE"
    assert artifact["blocking"] is False
