#!/usr/bin/env python3
"""Focused integrity checks for the AURA Forge capstone workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REQUIRED_JOBS = {
    "change-classifier",
    "policy-tests",
    "evaluation-gate",
    "pipeline-integrity",
    "advisory-review",
    "audit-trail",
}

PRODUCTION_MARKERS = (
    "render.com",
    "vercel",
    "fitgpt.tech",
    "deploy",
    "railway",
)

FORBIDDEN_WRITE_PERMISSIONS = {
    "actions": "write",
    "checks": "write",
    "contents": "write",
    "deployments": "write",
    "id-token": "write",
    "packages": "write",
    "pull-requests": "write",
}


def check_workflow(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    failures: list[str] = []

    if not isinstance(data, dict):
        return _result(path, ["workflow YAML did not parse to a mapping"])

    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict):
        return _result(path, ["workflow jobs block is missing or malformed"])

    missing = sorted(REQUIRED_JOBS - set(jobs))
    if missing:
        failures.append(f"missing required jobs: {missing}")

    policy = jobs.get("policy-tests", {})
    if policy.get("continue-on-error") is True:
        failures.append("policy-tests must not use continue-on-error")
    policy_text = json.dumps(policy, sort_keys=True)
    for required in ("eval/test_policy.py", "eval/test_mcp_runtime.py"):
        if required not in policy_text:
            failures.append(f"policy-tests does not reference {required}")

    eval_job = jobs.get("evaluation-gate", {})
    if "change-classifier" not in _needs(eval_job):
        failures.append("evaluation-gate must depend on change-classifier")
    if "policy-tests" not in _needs(eval_job):
        failures.append("evaluation-gate must depend on policy-tests")

    integrity = jobs.get("pipeline-integrity", {})
    if integrity.get("continue-on-error") is True:
        failures.append("pipeline-integrity must not use continue-on-error")
    for needed in ("change-classifier", "policy-tests", "evaluation-gate"):
        if needed not in _needs(integrity):
            failures.append(f"pipeline-integrity must depend on {needed}")

    audit = jobs.get("audit-trail", {})
    if str(audit.get("if", "")).strip() != "always()":
        failures.append("audit-trail must use if: always()")
    for needed in ("change-classifier", "policy-tests", "evaluation-gate", "pipeline-integrity", "advisory-review"):
        if needed not in _needs(audit):
            failures.append(f"audit-trail must depend on {needed}")

    advisory = jobs.get("advisory-review", {})
    if advisory.get("continue-on-error") is not True:
        failures.append("advisory-review must be explicitly non-blocking")

    _check_permissions(data.get("permissions"), "workflow", failures)
    for job_name, job in jobs.items():
        if isinstance(job, dict):
            _check_permissions(job.get("permissions"), f"job {job_name}", failures)
            if job_name != "advisory-review" and _contains_secret_context(job):
                failures.append(f"{job_name} exposes secrets outside advisory-review")

    lowered = text.lower()
    for marker in PRODUCTION_MARKERS:
        if marker in lowered:
            failures.append(f"workflow contains prohibited production/deployment marker: {marker}")

    return _result(path, failures)


def _result(path: Path, failures: list[str]) -> dict[str, object]:
    return {
        "schema_version": "pipeline-integrity-v1",
        "workflow": str(path),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }


def _needs(job: Any) -> set[str]:
    if not isinstance(job, dict):
        return set()
    needs = job.get("needs", [])
    if isinstance(needs, str):
        return {needs}
    if isinstance(needs, list):
        return {str(item) for item in needs}
    return set()


def _check_permissions(permissions: Any, label: str, failures: list[str]) -> None:
    if permissions is None:
        return
    if permissions == "write-all":
        failures.append(f"{label} uses write-all permissions")
        return
    if isinstance(permissions, dict):
        for key, forbidden in FORBIDDEN_WRITE_PERMISSIONS.items():
            if permissions.get(key) == forbidden:
                failures.append(f"{label} grants {key}: {forbidden}")


def _contains_secret_context(value: Any) -> bool:
    return "secrets." in json.dumps(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check AURA Forge workflow integrity.")
    parser.add_argument("workflow", nargs="?", default=".github/workflows/ci.yml")
    parser.add_argument("--output", help="Write JSON report to this path.")
    args = parser.parse_args(argv)

    result = check_workflow(Path(args.workflow))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
