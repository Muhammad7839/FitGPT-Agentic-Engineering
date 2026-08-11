#!/usr/bin/env python3
"""Build a sanitized CI audit trail from available machine evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_audit_trail(
    output_dir: Path,
    classification: Path | None = None,
    integrity: Path | None = None,
    advisory: Path | None = None,
    policy_status: str = "not_available",
    evaluation_status: str = "not_available",
) -> dict[str, object]:
    audit: dict[str, object] = {
        "schema_version": "aura-audit-trail-v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "policy_result": policy_status,
        "evaluation_result": evaluation_status,
    }
    if classification:
        audit["change_classification"] = _read_json(classification)
    if integrity:
        audit["integrity_result"] = _read_json(integrity)
    if advisory:
        audit["advisory_result"] = _read_json(advisory)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit-trail.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "audit-trail.md").write_text(_summary(audit), encoding="utf-8")
    return audit


def _read_json(path: Path) -> Any:
    if not path.exists():
        return {"status": "not_available", "reason": f"{path} was not produced"}
    return json.loads(path.read_text(encoding="utf-8"))


def _summary(audit: dict[str, object]) -> str:
    lines = [
        "# AURA Forge Audit Trail",
        "",
        f"Policy result: {audit.get('policy_result', 'not_available')}",
        f"Evaluation result: {audit.get('evaluation_result', 'not_available')}",
        f"Integrity result: {(audit.get('integrity_result') or {}).get('status', 'not_available') if isinstance(audit.get('integrity_result'), dict) else 'not_available'}",
        f"Advisory result: {(audit.get('advisory_result') or {}).get('status', 'not_available') if isinstance(audit.get('advisory_result'), dict) else 'not_available'}",
        "",
        "Unavailable producer data is omitted or marked `not_available`; no secrets are included.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--classification")
    parser.add_argument("--integrity")
    parser.add_argument("--advisory")
    parser.add_argument("--policy-status", default="not_available")
    parser.add_argument("--evaluation-status", default="not_available")
    parser.add_argument("--output-dir", default="artifacts/audit-trail")
    args = parser.parse_args(argv)
    audit = build_audit_trail(
        output_dir=Path(args.output_dir),
        classification=Path(args.classification) if args.classification else None,
        integrity=Path(args.integrity) if args.integrity else None,
        advisory=Path(args.advisory) if args.advisory else None,
        policy_status=args.policy_status,
        evaluation_status=args.evaluation_status,
    )
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
