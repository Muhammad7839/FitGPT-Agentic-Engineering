"""Deterministic AURA Forge risk classifier.

This module classifies a proposed bounded repository change into exactly one
of LOW, MEDIUM, or HIGH. It does not select routes or call models.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable


CLASSIFIER_VERSION = "aura-risk-v1"
TIERS = ("LOW", "MEDIUM", "HIGH")


HIGH_EXACT_PATHS = {
    "Dockerfile",
    "docker-compose.yml",
    "docs/governance-policy.md",
    "docs/governance-risk-analysis.md",
    "docs/routing-and-tool-grant-map.md",
    "eval/test_policy.py",
    "eval/test_mcp_runtime.py",
    "eval/test_coursetools_runtime.py",
}

HIGH_PREFIXES = (
    ".github/workflows/",
    ".claude/agents/",
    ".agentic/container/",
    "mcp/",
    "mcp-servers/",
    "eval/",
    "migrations/",
    "alembic/",
)

HIGH_SEGMENTS = {
    "auth",
    "authorization",
    "security",
    "secrets",
    "secret",
}

HIGH_FILENAME_MARKERS = (
    ".env",
    "dockerfile",
    "compose",
    "migration",
    "schema",
)

MEDIUM_PREFIXES = (
    "backend/",
    "web/src/",
    "web/tests/",
    "scripts/",
    "tests/",
)

MEDIUM_SUFFIXES = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".sh",
    ".sql",
)

LOW_SUFFIXES = (
    ".md",
    ".txt",
    ".rst",
)


@dataclass(frozen=True)
class ClassificationResult:
    tier: str
    classifier_version: str
    triggered_rules: tuple[str, ...]
    rationale: str
    normalized_paths: tuple[str, ...]


def classify_change(
    changed_paths: Iterable[str],
    metadata: dict[str, object] | None = None,
) -> ClassificationResult:
    """Classify changed paths with strict HIGH > MEDIUM > LOW precedence."""
    metadata = metadata or {}
    normalized, path_rules = _normalize_paths(changed_paths)
    triggered: list[str] = list(path_rules)

    metadata_rules = _metadata_rules(metadata)
    triggered.extend(metadata_rules)

    if not normalized:
        return _result(
            "HIGH",
            ("HIGH_EMPTY_PATH_SET", *tuple(triggered)),
            "No changed paths were supplied, so the classifier uses the conservative HIGH tier instead of defaulting to LOW.",
            normalized,
        )

    high_rules = [rule for path in normalized for rule in _high_rules(path)]
    if high_rules or metadata_rules:
        all_rules = tuple(dict.fromkeys([*triggered, *high_rules, *metadata_rules]))
        return _result(
            "HIGH",
            all_rules,
            "At least one path or metadata field touches a sensitive control surface.",
            normalized,
        )

    medium_rules = [rule for path in normalized for rule in _medium_rules(path)]
    if medium_rules:
        all_rules = tuple(dict.fromkeys([*triggered, *medium_rules]))
        return _result(
            "MEDIUM",
            all_rules,
            "The change touches executable application, test, or tooling code without a HIGH-sensitive trigger.",
            normalized,
        )

    low_rules = [rule for path in normalized for rule in _low_rules(path)]
    if low_rules and len(low_rules) == len(normalized):
        all_rules = tuple(dict.fromkeys([*triggered, "LOW_NON_EXECUTABLE_CONTENT"]))
        return _result(
            "LOW",
            all_rules,
            "All changed paths are non-executable content outside HIGH-sensitive and executable surfaces.",
            normalized,
        )

    return _result(
        "MEDIUM",
        tuple(dict.fromkeys([*triggered, "MEDIUM_UNKNOWN_PATH_CONSERVATIVE"])),
        "At least one path is not clearly non-executable documentation, so the classifier uses MEDIUM conservatively.",
        normalized,
    )


def _result(
    tier: str,
    triggered_rules: tuple[str, ...],
    rationale: str,
    normalized_paths: tuple[str, ...],
) -> ClassificationResult:
    if tier not in TIERS:
        raise ValueError(f"invalid tier: {tier}")
    return ClassificationResult(
        tier=tier,
        classifier_version=CLASSIFIER_VERSION,
        triggered_rules=triggered_rules,
        rationale=rationale,
        normalized_paths=normalized_paths,
    )


def _normalize_paths(paths: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    normalized: list[str] = []
    rules: list[str] = []
    for raw in paths:
        if not isinstance(raw, str) or not raw.strip():
            rules.append("HIGH_MALFORMED_PATH")
            continue
        candidate = raw.strip().replace("\\", "/")
        while candidate.startswith("./"):
            candidate = candidate[2:]
        if candidate.startswith("/") or candidate.startswith("~"):
            rules.append("HIGH_MALFORMED_PATH")
            continue
        parts = PurePosixPath(candidate).parts
        if ".." in parts:
            rules.append("HIGH_PATH_TRAVERSAL")
            continue
        cleaned = "/".join(part for part in parts if part not in ("", "."))
        if not cleaned:
            rules.append("HIGH_MALFORMED_PATH")
            continue
        normalized.append(cleaned)
    return tuple(normalized), tuple(dict.fromkeys(rules))


def _metadata_rules(metadata: dict[str, object]) -> tuple[str, ...]:
    rules: list[str] = []
    text = " ".join(str(value).lower() for value in metadata.values())
    for marker in ("production", "secret", "credential", "auth", "database", "migration"):
        if marker in text:
            rules.append("HIGH_METADATA_SENSITIVE_INTENT")
            break
    return tuple(rules)


def _high_rules(path: str) -> tuple[str, ...]:
    lower = path.lower()
    rules: list[str] = []
    if path in HIGH_EXACT_PATHS:
        rules.append("HIGH_SENSITIVE_EXACT_PATH")
    if any(path.startswith(prefix) for prefix in HIGH_PREFIXES):
        rules.append("HIGH_SENSITIVE_PREFIX")
    segments = set(PurePosixPath(lower).parts)
    if segments & HIGH_SEGMENTS:
        rules.append("HIGH_SECURITY_OR_AUTH_PATH")
    name = PurePosixPath(lower).name
    if name.startswith(".env") or any(marker in name for marker in HIGH_FILENAME_MARKERS):
        rules.append("HIGH_SECRET_ENV_SCHEMA_OR_SANDBOX_PATH")
    return tuple(dict.fromkeys(rules))


def _medium_rules(path: str) -> tuple[str, ...]:
    lower = path.lower()
    rules: list[str] = []
    if any(path.startswith(prefix) for prefix in MEDIUM_PREFIXES):
        rules.append("MEDIUM_EXECUTABLE_OR_TEST_PATH")
    if lower.endswith(MEDIUM_SUFFIXES):
        rules.append("MEDIUM_EXECUTABLE_LOOKING_SUFFIX")
    return tuple(dict.fromkeys(rules))


def _low_rules(path: str) -> tuple[str, ...]:
    if path.lower().endswith(LOW_SUFFIXES):
        return ("LOW_NON_EXECUTABLE_SUFFIX",)
    return ()
