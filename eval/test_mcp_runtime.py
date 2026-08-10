"""Runtime checks for governed MCP server registration."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _import_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_governed_mcp_servers_import_and_register_tools():
    storage = _import_module("fitgpt_governance_storage", "mcp-servers/storage/server.py")
    retrieval = _import_module("fitgpt_governance_retrieval", "mcp-servers/retrieval/server.py")

    assert storage.SERVER_NAME == "fitgpt-governance-storage"
    assert retrieval.SERVER_NAME == "fitgpt-governance-retrieval"
