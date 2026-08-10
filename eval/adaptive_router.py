"""Deterministic AURA Forge adaptive router.

The router maps a classifier result to a structured execution plan. It does not
invoke agents, run tests, edit files, or tune routes during measurement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from risk_classifier import ClassificationResult, classify_change


ROUTER_VERSION = "aura-router-v1"
ROUTE_IDS = {
    "LOW": "aura-low-v1",
    "MEDIUM": "aura-medium-v1",
    "HIGH": "aura-high-v1",
}
TIER_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}


class AdaptiveRouterError(ValueError):
    """Raised when routing evidence cannot safely produce a route."""


@dataclass(frozen=True)
class HumanCheckpoint:
    kind: str
    after_role: str
    before_role: str | None
    required: bool


@dataclass(frozen=True)
class DeterministicGate:
    name: str
    required: bool
    description: str


@dataclass(frozen=True)
class CapabilityProfile:
    role: str
    grants: tuple[str, ...]
    denied: tuple[str, ...]
    scope: str


@dataclass(frozen=True)
class EscalationPolicy:
    behavior: str
    triggers: tuple[str, ...]
    required_output: str


@dataclass(frozen=True)
class RoutePlan:
    router_version: str
    classifier_version: str
    tier: str
    route_id: str
    model_roles: tuple[str, ...]
    human_checkpoints: tuple[HumanCheckpoint, ...]
    deterministic_gates: tuple[DeterministicGate, ...]
    capability_profile: tuple[CapabilityProfile, ...]
    rationale: str
    escalation_policy: EscalationPolicy
    relevant_paths: tuple[str, ...]


@dataclass(frozen=True)
class EscalationRequired:
    original_tier: str
    observed_tier: str
    newly_observed_paths: tuple[str, ...]
    required_higher_tier: str
    reason: str


def build_route_plan(
    classifier_result: ClassificationResult,
    scenario_metadata: Mapping[str, object] | None = None,
    relevant_paths: Iterable[str] | None = None,
) -> RoutePlan:
    """Build a deterministic route plan from the classifier result."""
    if not isinstance(classifier_result, ClassificationResult):
        raise AdaptiveRouterError("classifier_result must be a ClassificationResult")
    tier = classifier_result.tier
    if tier not in ROUTE_IDS:
        raise AdaptiveRouterError(f"unknown classifier tier: {tier!r}")

    paths = _paths_from(classifier_result, relevant_paths)
    metadata = dict(scenario_metadata or {})
    caller_label = str(metadata.get("risk_label", "")).upper()
    if caller_label and caller_label in TIER_ORDER and TIER_ORDER[caller_label] < TIER_ORDER[tier]:
        metadata["caller_label_ignored"] = caller_label

    if tier == "LOW":
        return _low_route(classifier_result, paths)
    if tier == "MEDIUM":
        return _medium_route(classifier_result, paths)
    return _high_route(classifier_result, paths)


def check_for_escalation(
    planned_route: RoutePlan,
    observed_paths: Iterable[str],
    metadata: Mapping[str, object] | None = None,
) -> EscalationRequired | None:
    """Return escalation evidence if implementation expands above the planned tier."""
    observed = classify_change(tuple(observed_paths), metadata=dict(metadata or {}))
    if TIER_ORDER[observed.tier] > TIER_ORDER[planned_route.tier]:
        return EscalationRequired(
            original_tier=planned_route.tier,
            observed_tier=observed.tier,
            newly_observed_paths=observed.normalized_paths,
            required_higher_tier=observed.tier,
            reason="Observed changed paths require a higher risk tier than the frozen route.",
        )
    return None


def route_to_dict(plan: RoutePlan) -> dict[str, object]:
    """Serialize a route plan for evidence artifacts."""
    return {
        "router_version": plan.router_version,
        "classifier_version": plan.classifier_version,
        "tier": plan.tier,
        "route_id": plan.route_id,
        "model_roles": list(plan.model_roles),
        "human_checkpoints": [checkpoint.__dict__ for checkpoint in plan.human_checkpoints],
        "deterministic_gates": [gate.__dict__ for gate in plan.deterministic_gates],
        "capability_profile": [profile.__dict__ for profile in plan.capability_profile],
        "rationale": plan.rationale,
        "escalation_policy": plan.escalation_policy.__dict__,
        "relevant_paths": list(plan.relevant_paths),
    }


def _paths_from(
    classifier_result: ClassificationResult,
    relevant_paths: Iterable[str] | None,
) -> tuple[str, ...]:
    if relevant_paths is None:
        return classifier_result.normalized_paths
    paths = tuple(str(path).strip().replace("\\", "/") for path in relevant_paths if str(path).strip())
    if not paths:
        raise AdaptiveRouterError("relevant_paths cannot be empty when supplied")
    return paths


def _low_route(classifier_result: ClassificationResult, paths: tuple[str, ...]) -> RoutePlan:
    return RoutePlan(
        router_version=ROUTER_VERSION,
        classifier_version=classifier_result.classifier_version,
        tier="LOW",
        route_id=ROUTE_IDS["LOW"],
        model_roles=("implementer", "reviewer"),
        human_checkpoints=(),
        deterministic_gates=(
            DeterministicGate("approved-path-scope", True, "Changed files must stay within the scenario-approved LOW-safe path list."),
            DeterministicGate("git-diff-check", True, "Whitespace and conflict-marker checks must pass."),
            DeterministicGate("credential-pattern-scan", True, "Diff must not introduce credential-looking material."),
            DeterministicGate("scenario-specific-checks", True, "Documentation checklist evidence must satisfy the scenario acceptance criteria."),
            DeterministicGate("no-executable-or-high-sensitive-paths", True, "Actual changed paths must remain LOW when reclassified."),
        ),
        capability_profile=(
            CapabilityProfile(
                "implementer",
                ("bounded_file_read", "bounded_file_write_low_safe_paths"),
                ("planner", "tester_model", "project_manager", "task_tracker", "general_shell", "permission_mutation"),
                "May read bounded evidence and write only approved LOW-safe paths.",
            ),
            CapabilityProfile(
                "reviewer",
                ("bounded_file_read",),
                ("file_write", "tester_model", "task_tracker", "general_shell", "permission_mutation"),
                "Read-only independent semantic review.",
            ),
        ),
        rationale="LOW changes are non-executable and mechanically verifiable, so planning, tester, PM, and human approval overhead are removed.",
        escalation_policy=_escalation_policy(),
        relevant_paths=paths,
    )


def _medium_route(classifier_result: ClassificationResult, paths: tuple[str, ...]) -> RoutePlan:
    return RoutePlan(
        router_version=ROUTER_VERSION,
        classifier_version=classifier_result.classifier_version,
        tier="MEDIUM",
        route_id=ROUTE_IDS["MEDIUM"],
        model_roles=("implementer", "reviewer", "tester"),
        human_checkpoints=(
            HumanCheckpoint("final", "tester", None, True),
        ),
        deterministic_gates=(
            DeterministicGate("approved-path-scope", True, "Changed files must stay within scenario-approved MEDIUM paths."),
            DeterministicGate("git-diff-check", True, "Whitespace and conflict-marker checks must pass."),
            DeterministicGate("credential-pattern-scan", True, "Diff must not introduce credential-looking material."),
            DeterministicGate("focused-test-evidence", True, "Relevant focused tests must pass when the environment is available."),
            DeterministicGate("no-high-sensitive-paths", True, "Actual changed paths must not reclassify as HIGH."),
        ),
        capability_profile=(
            CapabilityProfile(
                "implementer",
                ("bounded_file_read", "bounded_file_write_medium_paths"),
                ("planner", "project_manager", "task_tracker", "permission_mutation", "production_access"),
                "May read and write only approved MEDIUM scenario paths.",
            ),
            CapabilityProfile(
                "reviewer",
                ("bounded_file_read",),
                ("file_write", "task_tracker", "general_shell", "permission_mutation"),
                "Read-only independent code and test review.",
            ),
            CapabilityProfile(
                "tester",
                ("bounded_file_read", "focused_test_execution"),
                ("file_write", "project_manager", "task_tracker", "production_access"),
                "May execute only the bounded relevant test target.",
            ),
        ),
        rationale="MEDIUM work touches executable or test code, so it keeps implementation, review, test evidence, and final human readiness approval.",
        escalation_policy=_escalation_policy(),
        relevant_paths=paths,
    )


def _high_route(classifier_result: ClassificationResult, paths: tuple[str, ...]) -> RoutePlan:
    return RoutePlan(
        router_version=ROUTER_VERSION,
        classifier_version=classifier_result.classifier_version,
        tier="HIGH",
        route_id=ROUTE_IDS["HIGH"],
        model_roles=("planner", "implementer", "reviewer", "tester", "project-manager"),
        human_checkpoints=(
            HumanCheckpoint("plan", "planner", "implementer", True),
            HumanCheckpoint("final", "tester", "project-manager", True),
        ),
        deterministic_gates=(
            DeterministicGate("approved-path-scope", True, "Changed files must stay within explicitly approved HIGH scenario paths."),
            DeterministicGate("git-diff-check", True, "Whitespace and conflict-marker checks must pass."),
            DeterministicGate("credential-pattern-scan", True, "Diff must not introduce credential-looking material."),
            DeterministicGate("policy-eval-gates", True, "Policy, evaluation, MCP runtime, and holdout-integrity gates must pass where applicable."),
            DeterministicGate("no-permission-widening", True, "Governed grants must not widen without explicit approval and passing tests."),
        ),
        capability_profile=(
            CapabilityProfile("planner", ("mcp__coursetools__file_read",), ("file_write", "test_runner", "task_tracker", "general_shell"), "Established read-only governed planning grant."),
            CapabilityProfile("implementer", ("mcp__coursetools__file_read", "mcp__coursetools__file_write"), ("task_tracker", "web_search", "unrestricted_shell"), "Established bounded governed implementation grant."),
            CapabilityProfile("reviewer", ("mcp__coursetools__file_read",), ("file_write", "test_runner", "task_tracker", "general_shell"), "Established read-only governed review grant."),
            CapabilityProfile("tester", ("mcp__coursetools__file_read", "mcp__coursetools__test_runner"), ("file_write", "task_tracker", "unrestricted_shell"), "Established bounded governed test grant."),
            CapabilityProfile("project-manager", ("mcp__coursetools__task_tracker",), ("file_read", "file_write", "test_runner", "web_search"), "Established isolated final tracker grant after human approval."),
        ),
        rationale="HIGH touches governance, policy, CI, MCP, schema, credential, or security-sensitive surfaces and keeps full governed controls.",
        escalation_policy=_escalation_policy(),
        relevant_paths=paths,
    )


def _escalation_policy() -> EscalationPolicy:
    return EscalationPolicy(
        behavior="fail_closed",
        triggers=(
            "unknown classifier tier",
            "malformed route metadata",
            "scenario/path evidence inconsistency",
            "observed implementation paths reclassify above planned tier",
        ),
        required_output="ESCALATION REQUIRED",
    )
