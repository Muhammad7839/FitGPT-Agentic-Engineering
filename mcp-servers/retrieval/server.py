"""Course-only retrieval governance MCP server.

The corpus is synthetic and exists only to verify role classification ceilings.
"""

from __future__ import annotations

import json
import os
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
    },
    {
        "id": "internal-dependency-decision",
        "classification": "internal",
        "text": "Internal synthetic dependency decision: prefer advisory reports before manifest edits.",
    },
    {
        "id": "confidential-release-note",
        "classification": "confidential",
        "text": "Synthetic confidential release planning note for ceiling verification only.",
    },
]

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


@mcp.tool()
def retrieve(query: str = "", requested_classification: str | None = None) -> dict[str, Any]:
    """Retrieve synthetic documents permitted by the role classification ceiling."""
    ceiling = _authorize()
    matches = []
    withheld = []
    needle = query.lower().strip()
    for item in CORPUS:
        if requested_classification and item["classification"] != requested_classification:
            continue
        if needle and needle not in item["text"].lower() and needle not in item["id"].lower():
            continue
        if _within_ceiling(item["classification"], ceiling):
            matches.append(item)
        else:
            withheld.append({"id": item["id"], "classification": item["classification"], "reason": "above role ceiling"})
    return {"role": _role(), "ceiling": ceiling, "matches": matches, "withheld": withheld}


if __name__ == "__main__":
    mcp.run()
