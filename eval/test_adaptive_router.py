import pytest

from adaptive_router import (
    AdaptiveRouterError,
    ROUTER_VERSION,
    build_route_plan,
    check_for_escalation,
    route_to_dict,
)
from risk_classifier import ClassificationResult, classify_change


def route_for(paths, metadata=None, risk_label=None):
    classifier = classify_change(paths, metadata=metadata)
    route_metadata = {"risk_label": risk_label} if risk_label else None
    return build_route_plan(classifier, scenario_metadata=route_metadata)


def role_names(plan):
    return plan.model_roles


def checkpoint_kinds(plan):
    return tuple(checkpoint.kind for checkpoint in plan.human_checkpoints)


def gate_names(plan):
    return tuple(gate.name for gate in plan.deterministic_gates)


def profile_for(plan, role):
    return next(profile for profile in plan.capability_profile if profile.role == role)


def test_low_classifier_result_maps_to_exact_low_route():
    plan = route_for(["docs/features/accessibility.md"])

    assert plan.router_version == ROUTER_VERSION
    assert plan.tier == "LOW"
    assert plan.route_id == "aura-low-v1"
    assert role_names(plan) == ("implementer", "reviewer")


def test_medium_classifier_result_maps_to_exact_medium_route():
    plan = route_for(["web/src/utils/feedbackPrompts.js"])

    assert plan.tier == "MEDIUM"
    assert plan.route_id == "aura-medium-v1"
    assert role_names(plan) == ("implementer", "reviewer", "tester")


def test_high_classifier_result_maps_to_exact_high_route():
    plan = route_for(["eval/test_policy.py"])

    assert plan.tier == "HIGH"
    assert plan.route_id == "aura-high-v1"
    assert role_names(plan) == ("planner", "implementer", "reviewer", "tester", "project-manager")


def test_low_has_zero_human_checkpoints():
    assert route_for(["docs/features/accessibility.md"]).human_checkpoints == ()


def test_medium_has_exactly_one_final_human_checkpoint():
    plan = route_for(["web/src/utils/feedbackPrompts.js"])

    assert checkpoint_kinds(plan) == ("final",)
    assert plan.human_checkpoints[0].after_role == "tester"


def test_high_has_plan_and_final_human_checkpoints():
    plan = route_for(["eval/test_policy.py"])

    assert checkpoint_kinds(plan) == ("plan", "final")
    assert plan.human_checkpoints[0].before_role == "implementer"
    assert plan.human_checkpoints[1].before_role == "project-manager"


def test_low_excludes_planner():
    assert "planner" not in role_names(route_for(["docs/features/accessibility.md"]))


def test_low_excludes_tester_model():
    assert "tester" not in role_names(route_for(["docs/features/accessibility.md"]))


def test_low_excludes_project_manager():
    assert "project-manager" not in role_names(route_for(["docs/features/accessibility.md"]))


def test_medium_excludes_planner():
    assert "planner" not in role_names(route_for(["web/src/utils/feedbackPrompts.js"]))


def test_medium_excludes_project_manager():
    assert "project-manager" not in role_names(route_for(["web/src/utils/feedbackPrompts.js"]))


def test_high_retains_planner():
    assert "planner" in role_names(route_for(["eval/test_policy.py"]))


def test_high_retains_project_manager():
    assert "project-manager" in role_names(route_for(["eval/test_policy.py"]))


def test_low_deterministic_gates_are_present():
    gates = gate_names(route_for(["docs/features/accessibility.md"]))

    assert "approved-path-scope" in gates
    assert "git-diff-check" in gates
    assert "credential-pattern-scan" in gates
    assert "scenario-specific-checks" in gates
    assert "no-executable-or-high-sensitive-paths" in gates


def test_high_policy_eval_gate_is_present():
    assert "policy-eval-gates" in gate_names(route_for(["eval/test_policy.py"]))


def test_malformed_tier_fails_closed():
    malformed = ClassificationResult(
        tier="",
        classifier_version="aura-risk-v1",
        triggered_rules=("bad",),
        rationale="malformed",
        normalized_paths=("docs/features/accessibility.md",),
    )

    with pytest.raises(AdaptiveRouterError, match="unknown classifier tier"):
        build_route_plan(malformed)


def test_unknown_tier_fails_closed():
    unknown = ClassificationResult(
        tier="CRITICAL",
        classifier_version="aura-risk-v1",
        triggered_rules=("bad",),
        rationale="unknown",
        normalized_paths=("docs/features/accessibility.md",),
    )

    with pytest.raises(AdaptiveRouterError, match="unknown classifier tier"):
        build_route_plan(unknown)


def test_route_capability_profiles_differ_by_tier():
    low = route_for(["docs/features/accessibility.md"])
    medium = route_for(["web/src/utils/feedbackPrompts.js"])
    high = route_for(["eval/test_policy.py"])

    assert low.capability_profile != medium.capability_profile
    assert medium.capability_profile != high.capability_profile
    assert low.capability_profile != high.capability_profile


def test_low_profile_cannot_use_pm_tracker():
    low = route_for(["docs/features/accessibility.md"])

    assert "task_tracker" in profile_for(low, "implementer").denied
    assert all("mcp__coursetools__task_tracker" not in profile.grants for profile in low.capability_profile)


def test_medium_profile_cannot_use_pm_tracker():
    medium = route_for(["web/src/utils/feedbackPrompts.js"])

    assert all("mcp__coursetools__task_tracker" not in profile.grants for profile in medium.capability_profile)
    assert "task_tracker" in profile_for(medium, "tester").denied


def test_high_uses_established_governed_grants_not_unrestricted_profile():
    high = route_for(["eval/test_policy.py"])
    grants = {grant for profile in high.capability_profile for grant in profile.grants}
    denied = {denial for profile in high.capability_profile for denial in profile.denied}

    assert "mcp__coursetools__task_tracker" in grants
    assert "unrestricted_shell" in denied
    assert "general_shell" in denied


def test_classifier_high_precedence_cannot_be_overridden_by_scenario_metadata():
    plan = route_for(
        ["docs/features/accessibility.md"],
        metadata={"request": "document production credential handling"},
    )

    assert plan.tier == "HIGH"
    assert plan.route_id == "aura-high-v1"


def test_caller_low_label_cannot_force_high_classifier_result_into_low():
    plan = route_for(["eval/test_policy.py"], risk_label="LOW")

    assert plan.tier == "HIGH"
    assert plan.route_id == "aura-high-v1"


def test_route_output_is_deterministic_for_identical_input():
    first = route_to_dict(route_for(["web/src/utils/feedbackPrompts.js"]))
    second = route_to_dict(route_for(["web/src/utils/feedbackPrompts.js"]))

    assert first == second


def test_observed_higher_risk_path_requires_escalation():
    planned = route_for(["docs/features/accessibility.md"])
    escalation = check_for_escalation(
        planned,
        ["docs/features/accessibility.md", "web/src/utils/feedbackPrompts.js"],
    )

    assert escalation is not None
    assert escalation.original_tier == "LOW"
    assert escalation.required_higher_tier == "MEDIUM"
    assert escalation.reason.startswith("Observed changed paths")


def test_low_route_observing_high_sensitive_path_fails_closed_with_escalation():
    planned = route_for(["docs/features/accessibility.md"])
    escalation = check_for_escalation(
        planned,
        ["docs/features/accessibility.md", "mcp/coursetools_server.py"],
    )

    assert planned.escalation_policy.required_output == "ESCALATION REQUIRED"
    assert escalation is not None
    assert escalation.original_tier == "LOW"
    assert escalation.observed_tier == "HIGH"
    assert escalation.required_higher_tier == "HIGH"
    assert "mcp/coursetools_server.py" in escalation.newly_observed_paths


def test_observed_same_tier_path_does_not_escalate():
    planned = route_for(["web/src/utils/feedbackPrompts.js"])

    assert check_for_escalation(planned, ["web/src/utils/feedbackPrompts.test.js"]) is None
