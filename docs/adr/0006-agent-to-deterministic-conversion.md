# ADR 0006: Agent-To-Deterministic Conversion

## Context

The `backend-config-docs-auditor` performed useful source comparison work but historical Run 5 still had factual precision weaknesses. Commit `9f9e461` converted one stable factual subtask to deterministic code.

## Decision

Convert only the `DATABASE_URL` representation check across README, env template, implementation, and focused tests. Leave prioritization and prose recommendation work agentic.

## Rejected Alternatives

- Converting the whole auditor. Rejected because broader audits require judgment.
- Calling the AURA risk classifier the conversion. Rejected because it was designed deterministic from the start.

## Evidence

- `docs/agents/backend-config-docs-auditor/lab/iteration-log.md` records Run 5 inspecting README, `.env.example`, implementation, and tests for `DATABASE_URL`.
- `scripts/check-config-docs-consistency.py` now emits deterministic JSON with model cost `$0`.
- `eval/test_config_docs_consistency.py` covers pass and fail behavior.

## Consequences

Repeated factual guardrails no longer require a model call.

## Open Risks

The utility covers one stable fact only. It must not be presented as a complete backend configuration audit.
