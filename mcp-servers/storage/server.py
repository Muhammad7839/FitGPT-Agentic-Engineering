"""Course-only storage governance MCP server.

This server is for the Module 4 governance exercise. It stores synthetic course
state under .governance-data and does not connect to FitGPT production systems.
"""

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


SERVER_NAME = "fitgpt-governance-storage"
ROOT = Path(os.environ.get("GOVERNANCE_ROOT", ".")).resolve()
DATA_DIR = Path(os.environ.get("GOVERNANCE_DATA_DIR", ROOT / ".governance-data" / "storage")).resolve()
ALLOW_LIST_PATH = Path(os.environ.get("GOVERNANCE_STORAGE_ALLOW_LIST", ROOT / "mcp-servers" / "storage" / "allow-list.json")).resolve()
AUDIT_PATH = Path(os.environ.get("GOVERNANCE_STORAGE_AUDIT", ROOT / ".governance-data" / "storage-audit.jsonl")).resolve()

mcp = FastMCP(SERVER_NAME)


def _role() -> str:
    return os.environ.get("AGENT_ROLE", "").strip() or "unknown"


def _load_allow_list() -> dict[str, dict[str, bool]]:
    return json.loads(ALLOW_LIST_PATH.read_text(encoding="utf-8"))


def _audit(operation: str, outcome: str, policy_reference: str) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "event": "storage_authorization",
        "role": _role(),
        "operation": operation,
        "outcome": outcome,
        "policy_reference": policy_reference,
    }
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def _authorize(operation: str) -> None:
    role = _role()
    policy_reference = f"docs/governance-policy.md:{role}:mcp_storage:{operation}"
    allowed = bool(_load_allow_list().get(role, {}).get(operation, False))
    if not allowed:
        _audit(operation, "denied", policy_reference)
        raise ToolError(f"Authorization denied for role={role} operation={operation}")
    _audit(operation, "granted", policy_reference)


def _entry_path(entry_id: str) -> Path:
    safe_id = entry_id.replace("/", "_").replace("..", "_")
    return DATA_DIR / f"{safe_id}.json"


@mcp.tool()
def write_entry(entry_id: str, value: dict[str, Any]) -> dict[str, Any]:
    """Write a course governance state entry."""
    _authorize("write_entry")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = _entry_path(entry_id)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"entry_id": entry_id, "status": "written"}


@mcp.tool()
def read_entry(entry_id: str) -> dict[str, Any]:
    """Read a course governance state entry."""
    _authorize("read_entry")
    path = _entry_path(entry_id)
    if not path.exists():
        raise ToolError(f"Entry not found: {entry_id}")
    return json.loads(path.read_text(encoding="utf-8"))


@mcp.tool()
def list_entries() -> list[str]:
    """List course governance state entry identifiers."""
    _authorize("list_entries")
    if not DATA_DIR.exists():
        return []
    return sorted(path.stem for path in DATA_DIR.glob("*.json"))


@mcp.tool()
def update_entry(entry_id: str, value: dict[str, Any]) -> dict[str, Any]:
    """Update an existing course governance state entry."""
    _authorize("update_entry")
    path = _entry_path(entry_id)
    if not path.exists():
        raise ToolError(f"Entry not found: {entry_id}")
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"entry_id": entry_id, "status": "updated"}


@mcp.tool()
def delete_entry(entry_id: str) -> dict[str, Any]:
    """Delete a course governance state entry."""
    _authorize("delete_entry")
    path = _entry_path(entry_id)
    if path.exists():
        path.unlink()
    return {"entry_id": entry_id, "status": "deleted"}


@mcp.tool()
def audit_read(limit: int = 20) -> list[dict[str, Any]]:
    """Read recent storage authorization audit events."""
    _authorize("audit_read")
    if not AUDIT_PATH.exists():
        return []
    lines = AUDIT_PATH.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(line) for line in lines if line.strip()]


if __name__ == "__main__":
    mcp.run()
