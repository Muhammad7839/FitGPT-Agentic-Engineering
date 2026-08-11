#!/usr/bin/env python3
"""Build evidence-backed AURA Forge Change Passports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "change-passport-v1"


class PassportError(ValueError):
    pass


def build_passport(
    repo_root: Path,
    scenario_id: str,
    ci_run_metadata: str | None = None,
    ci_artifact_root: str | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    run_root = _safe_ref(repo_root, f".eval-artifacts/capstone/aura-runs/{scenario_id}")
    metrics_path = _safe_ref(repo_root, f".eval-artifacts/capstone/aura-runs/{scenario_id}/final-successful-route-metrics.json")
    quality_path = _safe_ref(repo_root, f".eval-artifacts/capstone/aura-runs/{scenario_id}/final-quality-score.json")
    precheck_path = _safe_ref(repo_root, f".eval-artifacts/capstone/aura-runs/{scenario_id}/precheck-001/classifier-router-output.json")

    for required in (metrics_path, quality_path, precheck_path):
        if not required.exists():
            raise PassportError(f"missing required producer: {_rel(repo_root, required)}")

    metrics = _read_json(metrics_path)
    quality = _read_json(quality_path)
    precheck = _read_json(precheck_path)
    classifier = precheck["classifier"]
    router = precheck["router"]

    passport: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "change": {
            "scenario_id": scenario_id,
            "final_readiness_result": quality["result"],
            "quality_score": _quality_score(quality),
        },
        "classification": {
            "classifier_version": classifier["classifier_version"],
            "risk_tier": classifier["tier"],
            "triggered_rules": classifier["triggered_rules"],
            "normalized_paths": classifier["normalized_paths"],
        },
        "route": {
            "router_version": router["router_version"],
            "route_id": router["route_id"],
            "ordered_roles": _roles_from_metrics(metrics),
            "human_checkpoint_count": metrics.get("human_checkpoints", metrics.get("human_checkpoints_reached", 0)),
        },
        "deterministic_gates": _deterministic_gates(metrics),
        "tooling": {
            "tool_event_count": _metric(metrics, "tool_event_count", "tool_event_count_through_tester"),
            "authorization_denial_count": _metric(metrics, "authorization_denial_count", "authorization_denial_count_through_tester"),
        },
        "measurements": {
            "total_cost_usd": _metric(metrics, "total_cost_usd", "total_cost_usd_through_tester"),
            "duration_ms": _metric(metrics, "duration_ms", "duration_ms_through_tester"),
            "duration_api_ms": _metric(metrics, "duration_api_ms", "duration_api_ms_through_tester"),
        },
        "evidence": _evidence(repo_root, [metrics_path, quality_path, precheck_path]),
    }

    approvals = _approval_events(repo_root, run_root)
    if approvals:
        passport["human_approval_events"] = approvals

    policy = metrics.get("policy_test_result") or (metrics.get("deterministic_gates") or {}).get("test_policy")
    if policy:
        passport["policy_result"] = policy
    evaluation = metrics.get("focused_jest_result") or metrics.get("mcp_runtime_test_result")
    if evaluation:
        passport["evaluation_result"] = evaluation
    tests = _tests_from_metrics(metrics)
    if tests:
        passport["tests"] = tests
    if ci_run_metadata:
        passport["ci"] = _ci_evidence(repo_root, ci_run_metadata, ci_artifact_root)

    return passport


def validate_passport(passport: dict[str, object], repo_root: Path) -> None:
    for key in ("schema_version", "change", "classification", "route", "evidence"):
        if key not in passport:
            raise PassportError(f"missing passport field: {key}")
    if passport["schema_version"] != SCHEMA_VERSION:
        raise PassportError("unsupported schema version")
    for item in passport["evidence"]:
        path = _safe_ref(repo_root, item["path"])
        if not path.exists():
            raise PassportError(f"evidence reference does not resolve: {item['path']}")
        if item["sha256"] != _sha256(path):
            raise PassportError(f"evidence hash mismatch: {item['path']}")
    ci = passport.get("ci", {})
    github = ci.get("github_actions", {}) if isinstance(ci, dict) else {}
    for item in github.get("artifact_references", []):
        path = _safe_ref(repo_root, item["path"])
        if not path.exists():
            raise PassportError(f"CI artifact reference does not resolve: {item['path']}")
        if item["sha256"] != _sha256(path):
            raise PassportError(f"CI artifact hash mismatch: {item['path']}")


def _roles_from_metrics(metrics: dict[str, Any]) -> list[str]:
    if "per_role" in metrics:
        return [item["role"] for item in metrics["per_role"]]
    if "route" in metrics:
        return [item for item in metrics["route"] if not str(item).lower().startswith("muhammad")]
    raise PassportError("metrics do not contain route or per_role evidence")


def _deterministic_gates(metrics: dict[str, Any]) -> dict[str, object]:
    if "deterministic_gates" in metrics:
        return metrics["deterministic_gates"]
    gates = {}
    for key in ("focused_jest_result", "policy_test_result", "mcp_runtime_test_result", "escalation_required", "observed_tier"):
        if key in metrics:
            gates[key] = metrics[key]
    return gates


def _tests_from_metrics(metrics: dict[str, Any]) -> dict[str, object]:
    tests = {}
    for key in ("focused_jest_result", "policy_test_result", "mcp_runtime_test_result"):
        if key in metrics:
            tests[key] = metrics[key]
    return tests


def _quality_score(quality: dict[str, Any]) -> str:
    total = quality.get("total_score", quality.get("total"))
    maximum = quality.get("max_score", quality.get("maximum"))
    if total is None or maximum is None:
        raise PassportError("quality artifact does not contain total/max score evidence")
    return f"{total}/{maximum}"


def _approval_events(repo_root: Path, run_root: Path) -> list[dict[str, object]]:
    events = []
    for path in sorted(run_root.glob("*approval*/*.json")):
        data = _read_json(path)
        event = {
            "path": _rel(repo_root, path),
            "sha256": _sha256(path),
        }
        for key in ("approval_type", "approved_by", "approved_at_utc", "approved_after", "approved_before"):
            if key in data:
                event[key] = data[key]
        events.append(event)
    return events


def _ci_evidence(repo_root: Path, metadata_ref: str, artifact_root_ref: str | None) -> dict[str, object]:
    metadata_path = _safe_ref(repo_root, metadata_ref)
    if not metadata_path.exists():
        raise PassportError(f"missing CI metadata producer: {metadata_ref}")
    run = _read_json(metadata_path)
    jobs = {job["name"]: job.get("conclusion") or job.get("status", "not_available") for job in run.get("jobs", [])}
    artifact_references: list[dict[str, str]] = []
    artifact_names: list[str] = []
    advisory_artifact = None
    if artifact_root_ref:
        artifact_root = _safe_ref(repo_root, artifact_root_ref)
        if not artifact_root.exists():
            raise PassportError(f"missing CI artifact producer: {artifact_root_ref}")
        for path in sorted(p for p in artifact_root.rglob("*") if p.is_file()):
            artifact_references.append({"path": _rel(repo_root, path), "sha256": _sha256(path)})
            artifact_names.append(_rel(artifact_root, path))
        advisory_path = artifact_root / "advisory-review" / "advisory-review.json"
        if advisory_path.exists():
            advisory_artifact = _read_json(advisory_path)

    github_actions: dict[str, object] = {
        "provider": "github_actions",
        "workflow_run_id": run["databaseId"],
        "run_url": run["url"],
        "commit_sha": run["headSha"],
        "status": run["status"],
        "conclusion": run["conclusion"],
        "policy_status": jobs.get("policy-tests", "not_available"),
        "evaluation_status": jobs.get("evaluation-gate", "not_available"),
        "integrity_status": jobs.get("pipeline-integrity", "not_available"),
        "audit_status": jobs.get("audit-trail", "not_available"),
        "artifact_names": artifact_names,
        "metadata_reference": {"path": _rel(repo_root, metadata_path), "sha256": _sha256(metadata_path)},
    }
    if advisory_artifact:
        github_actions["advisory_status"] = advisory_artifact["status"]
        github_actions["advisory_reason"] = advisory_artifact.get("reason", "not_available")
    else:
        github_actions["advisory_status"] = jobs.get("advisory-review", "not_available")
    if artifact_references:
        github_actions["artifact_references"] = artifact_references
    return {"github_actions": github_actions}


def _evidence(repo_root: Path, paths: list[Path]) -> list[dict[str, str]]:
    return [{"path": _rel(repo_root, path), "sha256": _sha256(path)} for path in paths]


def _metric(metrics: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in metrics:
            return metrics[name]
    raise PassportError(f"missing metric: {names[0]}")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_ref(repo_root: Path, ref: str) -> Path:
    repo_root = repo_root.resolve()
    candidate = (repo_root / ref).resolve()
    if not str(candidate).startswith(str(repo_root) + "/") and candidate != repo_root:
        raise PassportError(f"evidence path escapes repository: {ref}")
    return candidate


def _rel(repo_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(repo_root.resolve()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario_id")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output")
    parser.add_argument("--ci-run-metadata")
    parser.add_argument("--ci-artifact-root")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    passport = build_passport(
        repo_root,
        args.scenario_id,
        ci_run_metadata=args.ci_run_metadata,
        ci_artifact_root=args.ci_artifact_root,
    )
    validate_passport(passport, repo_root)
    payload = json.dumps(passport, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
