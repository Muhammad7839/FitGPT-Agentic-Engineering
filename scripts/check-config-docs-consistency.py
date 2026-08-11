#!/usr/bin/env python3
"""Deterministically check a stable backend configuration documentation fact."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


SURFACES = {
    "readme": "README.md",
    "env_template": "backend/.env.example",
    "implementation": "backend/app/config.py",
    "focused_tests": "backend/tests/test_config_startup.py",
}


def check_database_url_consistency(repo_root: Path) -> dict[str, object]:
    start = time.perf_counter()
    texts = {name: _read(repo_root / rel) for name, rel in SURFACES.items()}
    checks = {
        "readme_mentions_database_url": "DATABASE_URL" in texts["readme"],
        "env_template_defines_database_url": "\nDATABASE_URL=" in "\n" + texts["env_template"],
        "implementation_reads_database_url": 'os.getenv("DATABASE_URL"' in texts["implementation"],
        "implementation_requires_database_url_in_production": "DATABASE_URL must be set in production" in texts["implementation"],
        "focused_tests_cover_database_url_production_requirement": "DATABASE_URL must be set in production" in texts["focused_tests"],
        "readme_documents_local_sqlite_fallback": "falls back to a local SQLite database" in texts["readme"],
        "env_template_documents_local_sqlite_fallback": "falls back to a local SQLite database" in texts["env_template"],
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema_version": "config-docs-consistency-v1",
        "converted_from_agentic_step": "backend-config-docs-auditor factual source comparison",
        "checked_fact": "DATABASE_URL is represented consistently across README, env template, implementation, and focused production tests.",
        "status": status,
        "checks": checks,
        "surfaces": SURFACES,
        "model_cost_usd": 0,
        "duration_ms": round((time.perf_counter() - start) * 1000, 3),
    }


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = check_database_url_consistency(Path(args.repo_root))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
