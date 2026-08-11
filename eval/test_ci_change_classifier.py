import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ci_change_classifier import classify_for_ci


def test_reuses_aura_classifier_and_router_for_high_ci_change():
    result = classify_for_ci([".github/workflows/ci.yml"])
    assert result["classifier_version"] == "aura-risk-v1"
    assert result["router_version"] == "aura-router-v1"
    assert result["risk_tier"] == "HIGH"
    assert result["route_id"] == "aura-high-v1"
    assert result["affects_ci"] is True
    assert result["modifies_permanent_guardrails"] is True
    assert result["should_run_evaluation"] is True


def test_low_docs_change_does_not_trigger_expensive_eval():
    result = classify_for_ci(["docs/features/accessibility.md"])
    assert result["risk_tier"] == "LOW"
    assert result["should_run_evaluation"] is False
    assert result["modifies_permanent_guardrails"] is False


def test_eval_path_triggers_agentic_surface_and_evaluation():
    result = classify_for_ci(["eval/test_policy.py"])
    assert result["risk_tier"] == "HIGH"
    assert result["affects_agentic_surface"] is True
    assert result["should_run_evaluation"] is True
    assert result["modifies_permanent_guardrails"] is True
