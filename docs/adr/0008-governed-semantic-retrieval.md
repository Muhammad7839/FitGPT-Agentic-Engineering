# ADR 0008: Governed Semantic Retrieval

## Context

The existing retrieval server enforced role classification ceilings but used exact substring matching and returned no source citation. Canvas feedback specifically identified semantic document search as missing.

## Decision

Keep retrieval local and deterministic for the course corpus. Convert query and document text to expanded token vectors, rank with cosine similarity, enforce the existing role ceiling before returning text, and attach a repository path and section citation to every match.

## Rejected Alternatives

- External embedding API. Rejected because offline grading should require no secret, network, paid call, or production data.
- Exact substring search only. Rejected because it cannot satisfy related-term queries such as `package audit` against dependency/manifest/report language.
- Returning uncited snippets. Rejected because a grader or reviewer must be able to inspect the stated source.

## Evidence

- `eval/test_retrieval_behavior.py` covers related-term ranking, citations, classification withholding, and empty-query denial.
- `docs/governance-policy.md` records the schema, classification field, citation fields, and bounded `top_k` range.

## Consequences

The result is reproducible and governable without external infrastructure. Search breadth is intentionally limited by the small synthetic corpus and checked synonym map.

## Open Risks

This is not a production embedding index and does not establish retrieval quality at real FitGPT document scale.
