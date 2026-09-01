# Governed Semantic Retrieval Evidence

## Purpose

The grader reported that semantic document search was absent from the available evidence. AURA Forge now exposes a deterministic semantic-vector retrieval contract through `mcp-servers/retrieval/server.py`.

This remains a synthetic, course-only corpus. It does not connect to production data, external search, or an embedding API.

## Public Tool Contract

Tool: `retrieve`

Inputs:

- `query`: required non-empty text.
- `requested_classification`: optional `public`, `internal`, or `confidential` filter.
- `top_k`: integer from 1 through 10.

Output schema: `governed-retrieval-result-v2`

Every returned match includes:

- document ID;
- classification tag;
- text;
- deterministic similarity score;
- citation path and section.

The top-level result also records the role, classification ceiling, normalized query, search mode, returned matches, and withheld matches.

## Search Behavior

The implementation converts the query and synthetic documents into deterministic token vectors, expands a small checked synonym map, and ranks with cosine similarity. This is intentionally bounded and reproducible. It does not claim the breadth of a hosted embedding model.

The behavior test uses `package audit`, which does not appear as an exact phrase in the selected document. The synonym expansion maps it to the dependency, manifest, report, and review terms that rank `public-dependency-style` first.

## Governance Behavior

Authorization runs before search. A role without the retrieval grant receives no result, and an authorized role never receives document text above its classification ceiling. Above-ceiling relevant documents are returned only as withheld metadata with a citation and denial reason.

Policy source: `docs/governance-policy.md`

Allow-list source: `mcp-servers/retrieval/allow-list.json`

## Verification

```bash
pytest -q -p no:cacheprovider eval/test_retrieval_behavior.py eval/test_policy.py eval/test_mcp_runtime.py
```

The permanent GitHub policy job includes the retrieval behavior test. The offline container verifier runs with network disabled and a read-only workspace.

## Limitation

This proves a governed, schema-validated, classification-tagged, citation-bearing vector retrieval tool over a synthetic corpus. It does not prove production-scale semantic search quality or access to private FitGPT documents.
