"""Behavior checks for the governed semantic retrieval tool."""

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load_retrieval(monkeypatch, tmp_path, role="dependency-auditor"):
    monkeypatch.setenv("AGENT_ROLE", role)
    monkeypatch.setenv("GOVERNANCE_ROOT", str(ROOT))
    monkeypatch.setenv("GOVERNANCE_RETRIEVAL_AUDIT", str(tmp_path / "retrieval-audit.jsonl"))
    path = ROOT / "mcp-servers" / "retrieval" / "server.py"
    spec = importlib.util.spec_from_file_location("retrieval_server_behavior", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_semantic_retrieval_ranks_a_related_document_and_returns_a_citation(monkeypatch, tmp_path):
    retrieval = _load_retrieval(monkeypatch, tmp_path)

    result = retrieval.retrieve(query="package audit", top_k=1)

    assert result["schema_version"] == "governed-retrieval-result-v2"
    assert result["search_mode"] == "deterministic-semantic-vector"
    assert result["matches"][0]["id"] == "public-dependency-style"
    assert result["matches"][0]["score"] > 0
    assert result["matches"][0]["citation"] == {
        "path": "docs/routing-and-tool-grant-map.md",
        "section": "Dependency Auditor",
    }


def test_semantic_retrieval_withholds_relevant_documents_above_role_ceiling(monkeypatch, tmp_path):
    retrieval = _load_retrieval(monkeypatch, tmp_path)

    result = retrieval.retrieve(
        query="release planning",
        requested_classification="confidential",
        top_k=3,
    )

    assert result["matches"] == []
    assert result["withheld"] == [
        {
            "id": "confidential-release-note",
            "classification": "confidential",
            "reason": "above role ceiling",
            "citation": {
                "path": "docs/governance-policy.md",
                "section": "Classification levels",
            },
        }
    ]


def test_semantic_retrieval_rejects_an_empty_query(monkeypatch, tmp_path):
    retrieval = _load_retrieval(monkeypatch, tmp_path)

    try:
        retrieval.retrieve(query="   ")
    except retrieval.ToolError as error:
        assert "query must not be empty" in str(error)
    else:
        raise AssertionError("empty semantic query must fail closed")


def test_semantic_retrieval_rejects_invalid_classification_and_result_limits(monkeypatch, tmp_path):
    retrieval = _load_retrieval(monkeypatch, tmp_path)

    with pytest.raises(retrieval.ToolError, match="unknown requested classification"):
        retrieval.retrieve(query="dependency", requested_classification="secret")

    with pytest.raises(retrieval.ToolError, match="top_k must be between 1 and 10"):
        retrieval.retrieve(query="dependency", top_k=11)


def test_semantic_retrieval_denies_a_role_without_a_retrieval_grant(monkeypatch, tmp_path):
    retrieval = _load_retrieval(monkeypatch, tmp_path, role="project-manager")

    with pytest.raises(retrieval.ToolError, match="Authorization denied"):
        retrieval.retrieve(query="dependency")
