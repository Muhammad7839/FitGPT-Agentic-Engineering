# ADR 0003: MCP Tool Boundaries And Least Privilege

## Context

Module 4 governance depends on role-scoped MCP tool grants. The sandbox foundation verified governed MCP storage/retrieval imports and read-only workspace behavior. The fresh overreach demo `GO-20260811-001` proved the `implementer` role cannot use Project-Manager-only `task_tracker`.

## Decision

Keep role/tool boundaries explicit and testable. Use real authorization denials as governance evidence.

## Rejected Alternatives

- Trusting prompt instructions alone. Rejected because prompt-only boundaries are not enforceable.
- Granting broad shell or task-tracker access to implementation roles. Rejected because implementation should not mark work complete.

## Evidence

- `eval/test_policy.py`, `eval/test_mcp_runtime.py`, and `eval/test_coursetools_runtime.py` are permanent deterministic checks.
- `docs/capstone/governance-overreach-demo.md` records a real denial: `implementer` was not on the allow-list for `task_tracker`.

## Consequences

The system can show least-privilege enforcement with concrete machine evidence.

## Open Risks

The course `task_tracker` is simulated. It proves local role authorization, not behavior of a real external ticketing integration.
