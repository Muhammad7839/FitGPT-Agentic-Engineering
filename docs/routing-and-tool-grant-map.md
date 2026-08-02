# Backend Onboarding Routing and Tool-Grant Map

Controlled issue: `COURSE-FITGPT-001`

Exact tool identifiers come from the installed `coursetools` server source. `codebase_search` exists, but this workflow does not need it because every evidence and writable path is explicitly handed off.

| Role | Single responsibility | Receives from Orchestrator | Produces | Exact tools granted | Exact tools denied and reason | Context-isolation reason | Autonomy | Evaluation gate | Human checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| Planner | Produce a documentation-only correction plan and exact file list. | Issue, repository path, approved evidence-file list. | Numbered plan, files, acceptance criteria, open questions. | `mcp__coursetools__file_read` | `file_write`: no implementation; `codebase_search`: explicit paths suffice; `shell`, `test_runner`: no execution; `task_tracker`: no issue changes; `web_search`: committed evidence only. | Prevents planning from becoming implementation or external research. | High; read-only. | Every required plan section is present and scope is documentation-only. One incomplete-output retry maximum. | Human approves the complete plan before any `file_write`. |
| Implementer | Apply only approved documentation/template edits. | Approved plan, writable allowlist, and first-review corrective instructions if needed. | Changed-file list and concise implementation summary. | `mcp__coursetools__file_read`, `mcp__coursetools__file_write` | `codebase_search`: exact paths supplied; `shell`, `test_runner`: independent testing; `task_tracker`: cannot mark own work complete; `web_search`: no external evidence. | Limits write authority to the approved plan and prevents self-approval. | Medium; bounded writes. | Only `README.md` and `backend/.env.example` may change; one reviewer-driven retry maximum. | Current-run plan approval is required before invocation. |
| Reviewer | Compare edits with committed configuration and focused tests. | Changed-file list, diff or proposed contents, acceptance criteria. | `Pass` or `Revise`, severity-ranked findings, corrective instructions, open questions. | `mcp__coursetools__file_read` | `file_write`: independent review; `codebase_search`: explicit paths suffice; `shell`, `test_runner`: separate Tester role; `task_tracker`: no issue changes; `web_search`: committed evidence only. | Keeps the reviewer independent from the writer and tester. | High; read-only. | `Pass` requires no unresolved high-severity issue and no scope violation. A second `Revise` halts. | No new checkpoint; approved plan remains controlling. |
| Tester | Run and interpret only the focused backend configuration test representation. | Approved changed-file list and `backend/tests/test_config_startup.py`. | Command represented by dummy tool, `Pass`/`Fail`/`Blocked`, failures, limitations. | `mcp__coursetools__file_read`, `mcp__coursetools__test_runner` | `file_write`: no repairs; `codebase_search`: target supplied; `shell`: bounded runner is narrower; `task_tracker`: no issue changes; `web_search`: irrelevant. | Prevents test execution from expanding into repair or general shell access. | Medium; bounded execution. | Only the supplied focused target is accepted. `Fail` or `Blocked` halts and escalates. | Final human approval occurs only after Tester and Reviewer pass. |
| Project Manager | Update controlled issue after all gates and final approval. | Final run summary and explicit current-run human-approval token. | Issue status and update confirmation or failure escalation. | `mcp__coursetools__task_tracker` | `file_read`, `file_write`, `codebase_search`: no repository access; `shell`, `test_runner`: gates already complete; `web_search`: irrelevant. | Separates shared-record mutation from implementation, review, and testing. | Medium; shared dummy record change. | Approval evidence, Reviewer `Pass`, and Tester `Pass` must all be present. | Explicit final current-run human approval is mandatory. |
| Orchestrator | Delegate, evaluate, loop, halt, and request approval. | User bug report and role outputs. | Scoped handoffs, gate decisions, approval requests, final summary, escalation. | Built-in `Agent`; `mcp__coursetools__file_read` and `mcp__coursetools__file_write` only for handoff documents and final summaries. | `codebase_search`: delegate evidence work; `shell`, `test_runner`: Tester owns execution; `task_tracker`: Project Manager owns updates; `web_search`: prohibited; source-code editing: prohibited. | Prevents the coordinator from collapsing independent roles or self-validating. | Medium; routing and bounded workflow-document writes. | Validate each output contract and retry counter before routing forward. | Requests both plan approval and final issue-update approval. |

## Later-run writable and test scopes

- Implementer writable allowlist:
  - `README.md`
  - `backend/.env.example`
- Tester allowed target:
  - `backend/tests/test_config_startup.py`
- Project Manager allowed issue:
  - `COURSE-FITGPT-001`

## Tool concentration review

| Tool | Roles granted | Count | Justification |
|---|---|---:|---|
| `mcp__coursetools__file_read` | Planner, Implementer, Reviewer, Tester, Orchestrator | 5 | The read capability is shared because each role needs a different, explicitly scoped evidence subset. Handoffs must restrict paths; the grant is not permission to inspect the whole repository. |
| `mcp__coursetools__file_write` | Implementer, Orchestrator | 2 | Implementer writes only approved target files in later runs. Orchestrator writes only handoff records and final summaries, never source files. |
| `mcp__coursetools__test_runner` | Tester | 1 | Test execution remains independent and bounded. |
| `mcp__coursetools__task_tracker` | Project Manager | 1 | Shared workflow-record mutation occurs only after final approval. |
| `mcp__coursetools__codebase_search` | None | 0 | Exact evidence paths make repository-wide search unnecessary. |
| `mcp__coursetools__shell` | None | 0 | The workflow needs no general or simulated shell capability. |
| `mcp__coursetools__web_search` | None | 0 | Only committed repository evidence is allowed. |

`file_read` is the only tool granted to more than two roles. That concentration is justified by role-specific path isolation and read-only behavior.

## Alternatives considered

1. Giving Implementer `mcp__coursetools__task_tracker` — rejected because it could mark its own work complete before independent review, testing, and human approval.
2. Giving Reviewer `mcp__coursetools__file_write` — rejected because review must remain independent and read-only.
3. Giving Tester `mcp__coursetools__shell` — rejected because `mcp__coursetools__test_runner` is the narrower capability.
4. Giving Orchestrator every tool — rejected because it would collapse role boundaries and allow self-implementation, self-testing, or issue updates.
5. Giving Planner or Reviewer `mcp__coursetools__codebase_search` — rejected for this workflow because the evidence paths are already known and passed explicitly.

## Verification status

The installed source advertises every identifier in this map, including `mcp__coursetools__codebase_search`. Project registration is pending Claude Code approval, so availability and denial behavior remain unproven until the separately authorized boundary test. This document does not claim that enforcement has already been demonstrated.
