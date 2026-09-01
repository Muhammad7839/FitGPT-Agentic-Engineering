"""Course-only retrieval governance MCP server.

The corpus is synthetic and exists only to verify role classification ceilings.
"""

import json
import math
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

try:
    from mcp.server.fastmcp.exceptions import ToolError
except Exception:  # pragma: no cover - keeps static validation independent.
    class ToolError(Exception):
        pass


SERVER_NAME = "fitgpt-governance-retrieval"
ROOT = Path(os.environ.get("GOVERNANCE_ROOT", ".")).resolve()
ALLOW_LIST_PATH = Path(os.environ.get("GOVERNANCE_RETRIEVAL_ALLOW_LIST", ROOT / "mcp-servers" / "retrieval" / "allow-list.json")).resolve()
AUDIT_PATH = Path(os.environ.get("GOVERNANCE_RETRIEVAL_AUDIT", ROOT / ".governance-data" / "retrieval-audit.jsonl")).resolve()

CLASSIFICATION_ORDER = ["public", "internal", "confidential"]
CORPUS = [
    {
        "id": "public-dependency-style",
        "classification": "public",
        "text": "Public dependency guidance: report manifest inconsistencies with file evidence.",
        "citation": {
            "path": "docs/routing-and-tool-grant-map.md",
            "section": "Dependency Auditor",
        },
    },
    {
        "id": "internal-dependency-decision",
        "classification": "internal",
        "text": "Internal synthetic dependency decision: prefer advisory reports before manifest edits.",
        "citation": {
            "path": "docs/governance-policy.md",
            "section": "Governed roles",
        },
    },
    {
        "id": "confidential-release-note",
        "classification": "confidential",
        "text": "Synthetic confidential release planning note for ceiling verification only.",
        "citation": {
            "path": "docs/governance-policy.md",
            "section": "Classification levels",
        },
    },
]

SEMANTIC_EQUIVALENTS = {
    "audit": ("report", "review"),
    "package": ("dependency", "manifest"),
    "packages": ("dependency", "manifest"),
    "policy": ("governance", "guardrail"),
    "release": ("deployment", "planning"),
}

mcp = FastMCP(SERVER_NAME)


def _role() -> str:
    return os.environ.get("AGENT_ROLE", "").strip() or "unknown"


def _load_allow_list() -> dict[str, dict[str, Any]]:
    return json.loads(ALLOW_LIST_PATH.read_text(encoding="utf-8"))


def _audit(operation: str, outcome: str, policy_reference: str) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "event": "retrieval_authorization",
        "role": _role(),
        "operation": operation,
        "outcome": outcome,
        "policy_reference": policy_reference,
    }
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def _authorize() -> str:
    role = _role()
    policy_reference = f"docs/governance-policy.md:{role}:mcp_retrieval:retrieve"
    rule = _load_allow_list().get(role, {})
    if not rule.get("retrieve", False):
        _audit("retrieve", "denied", policy_reference)
        raise ToolError(f"Authorization denied for role={role} operation=retrieve")
    ceiling = str(rule.get("ceiling", "none"))
    if ceiling not in CLASSIFICATION_ORDER:
        _audit("retrieve", "denied", policy_reference)
        raise ToolError(f"Invalid retrieval ceiling for role={role}: {ceiling}")
    _audit("retrieve", "granted", policy_reference)
    return ceiling


def _within_ceiling(classification: str, ceiling: str) -> bool:
    return CLASSIFICATION_ORDER.index(classification) <= CLASSIFICATION_ORDER.index(ceiling)


def _semantic_vector(text: str) -> Counter[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = list(tokens)
    for token in tokens:
        expanded.extend(SEMANTIC_EQUIVALENTS.get(token, ()))
    return Counter(expanded)


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    common = set(left) & set(right)
    dot_product = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot_product / (left_norm * right_norm)


@mcp.tool()
def retrieve(
    query: str,
    requested_classification: str | None = None,
    top_k: int = 5,
) -> dict[str, Any]:
    """Return ranked, cited synthetic documents within the role ceiling."""
    ceiling = _authorize()
    normalized_query = query.strip()
    if not normalized_query:
        raise ToolError("query must not be empty")
    if requested_classification and requested_classification not in CLASSIFICATION_ORDER:
        raise ToolError(f"unknown requested classification: {requested_classification}")
    if not 1 <= top_k <= 10:
        raise ToolError("top_k must be between 1 and 10")

    query_vector = _semantic_vector(normalized_query)
    ranked: list[tuple[float, dict[str, Any]]] = []
    for item in CORPUS:
        if requested_classification and item["classification"] != requested_classification:
            continue
        score = _cosine_similarity(query_vector, _semantic_vector(f"{item['id']} {item['text']}"))
        if score > 0:
            ranked.append((score, item))

    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    matches = []
    withheld = []
    for score, item in ranked:
        if _within_ceiling(item["classification"], ceiling):
            if len(matches) < top_k:
                matches.append(
                    {
                        **item,
                        "score": round(score, 6),
                    }
                )
        else:
            withheld.append(
                {
                    "id": item["id"],
                    "classification": item["classification"],
                    "reason": "above role ceiling",
                    "citation": item["citation"],
                }
            )
    return {
        "schema_version": "governed-retrieval-result-v2",
        "search_mode": "deterministic-semantic-vector",
        "role": _role(),
        "ceiling": ceiling,
        "query": normalized_query,
        "matches": matches,
        "withheld": withheld,
    }


if __name__ == "__main__":
    mcp.run()
