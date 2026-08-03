# Agent Governance Policy

Version: v1.0.0
Last updated: 2026-08-03
Reviewed by: Muhammad Imran

## Policy basis

This policy is newly designed for the FitGPT Agentic Engineering target repository. It is not ported from Module 4 template files.

This policy is derived from:

- `docs/routing-and-tool-grant-map.md`
- `docs/calibration-log.md`
- `docs/governance-risk-analysis.md`
- least-privilege defaults applied to all roles

## Least-privilege default

Every role starts with no access. All grants are explicit and justified. Any access not explicitly granted is denied by default.

To widen access, require a reviewed change containing:

- the proposed grant
- a concrete functional justification
- the affected risk statement
- updated enforcement artifacts
- passing policy tests
- new runtime verification evidence

## Governance model

The storage and retrieval servers in this exercise are course governance infrastructure. They are not FitGPT production services and do not connect to production databases, production APIs, external services, or real credentials.

Controlled storage operations:

- `write_entry`
- `read_entry`
- `list_entries`
- `update_entry`
- `delete_entry`
- `audit_read`

Controlled retrieval operation:

- `retrieve`

Governed skills:

- `run-tests`
- `draft-pr-description`
- `summarize-session`

Classification levels:

- `public`
- `internal`
- `confidential`

Runtime state belongs under `.governance-data/` and must remain uncommitted.

## Governed roles

The active FitGPT orchestration roles are:

- `orchestrator`
- `planner`
- `implementer`
- `reviewer`
- `tester`
- `project-manager`

### Existing-role summary

| Role | Defined in | MCP storage access | Retrieval ceiling | Skills | Autonomy | Container |
|---|---|---|---|---|---|---|
| orchestrator | `CLAUDE.md` | read/list/write/update/audit_read only | confidential | summarize-session only | medium with plan and final approval checkpoints | workspace read-write, memory omitted |
| planner | `.claude/agents/planner.md` | read/list only | internal | summarize-session only | low advisory before write approval | workspace read-only, memory omitted |
| implementer | `.claude/agents/implementer.md` | read/list/write/update only | internal | run-tests and summarize-session | medium after plan approval | workspace read-write, memory omitted |
| reviewer | `.claude/agents/reviewer.md` | read/list only | internal | summarize-session only | low advisory | workspace read-only, memory omitted |
| tester | `.claude/agents/tester.md` | read/list only | internal | run-tests and summarize-session | low after Reviewer pass | workspace read-only, memory omitted |
| project-manager | `.claude/agents/project-manager.md` | read/list only | none | draft-pr-description and summarize-session | low after final approval | workspace read-only, memory omitted |

### Existing-role detailed policy

Every `NO` below is justified by either a recorded risk in `docs/governance-risk-analysis.md` or by least privilege.

<!-- GOVERNANCE_POLICY_JSON_START
{
  "version": "v1.0.0",
  "classification_order": ["public", "internal", "confidential"],
  "storage_operations": ["write_entry", "read_entry", "list_entries", "update_entry", "delete_entry", "audit_read"],
  "retrieval_operations": ["retrieve"],
  "skills": ["run-tests", "draft-pr-description", "summarize-session"],
  "roles": {
    "orchestrator": {
      "defined_in": "CLAUDE.md",
      "mcp_storage": {
        "write_entry": {"grant": true, "reason": "Course workflow state and handoff summaries may be recorded by the coordinator."},
        "read_entry": {"grant": true, "reason": "Needs workflow state to route and checkpoint correctly."},
        "list_entries": {"grant": true, "reason": "Needs to enumerate current workflow state."},
        "update_entry": {"grant": true, "reason": "May update course workflow state, not external tickets."},
        "delete_entry": {"grant": false, "reason": "Least privilege; deleting state would damage auditability."},
        "audit_read": {"grant": true, "reason": "Coordinates governance verification and needs audit visibility."}
      },
      "mcp_retrieval": {"retrieve": true, "ceiling": "confidential", "reason": "Coordinator may need full governed context but must still respect no-secret rules."},
      "skills": {
        "run-tests": {"grant": false, "reason": "Routing map assigns test execution to Tester."},
        "draft-pr-description": {"grant": false, "reason": "Least privilege; not part of course orchestration state."},
        "summarize-session": {"grant": true, "reason": "May summarize its own session and handoffs."}
      },
      "autonomy": {"level": "medium", "checkpoints": ["human plan approval before implementation", "human final approval before project-manager handoff"]},
      "container": {"workspace": "read-write", "memory": "omitted", "reason": "May write course handoff records only; memory omitted because no active workflow requires it."}
    },
    "planner": {
      "defined_in": ".claude/agents/planner.md",
      "mcp_storage": {
        "write_entry": {"grant": false, "reason": "Least privilege; planning is read-only."},
        "read_entry": {"grant": true, "reason": "May read relevant workflow state when handed off."},
        "list_entries": {"grant": true, "reason": "May discover relevant planning records."},
        "update_entry": {"grant": false, "reason": "Least privilege; planning must not mutate state."},
        "delete_entry": {"grant": false, "reason": "Least privilege and audit preservation."},
        "audit_read": {"grant": false, "reason": "Least privilege; audit inspection is not the Planner responsibility."}
      },
      "mcp_retrieval": {"retrieve": true, "ceiling": "internal", "reason": "May retrieve internal planning guidance but not confidential material."},
      "skills": {
        "run-tests": {"grant": false, "reason": "Routing map denies Planner test execution."},
        "draft-pr-description": {"grant": false, "reason": "Least privilege; not a planning duty."},
        "summarize-session": {"grant": true, "reason": "May summarize its own planning result."}
      },
      "autonomy": {"level": "low", "checkpoints": ["human plan approval required before writes"]},
      "container": {"workspace": "read-only", "memory": "omitted", "reason": "Planner is advisory and read-only."}
    },
    "implementer": {
      "defined_in": ".claude/agents/implementer.md",
      "mcp_storage": {
        "write_entry": {"grant": true, "reason": "May record implementation decisions within approved scope."},
        "read_entry": {"grant": true, "reason": "May read approved workflow state."},
        "list_entries": {"grant": true, "reason": "May discover approved implementation records."},
        "update_entry": {"grant": true, "reason": "May update implementation decision records within approved scope."},
        "delete_entry": {"grant": false, "reason": "Unauthorized tracker/state near-miss and audit preservation require no delete access."},
        "audit_read": {"grant": false, "reason": "Least privilege; independent audit inspection is not implementation."}
      },
      "mcp_retrieval": {"retrieve": true, "ceiling": "internal", "reason": "May retrieve internal implementation guidance."},
      "skills": {
        "run-tests": {"grant": true, "reason": "Implementation may run focused checks when explicitly allowed by workflow."},
        "draft-pr-description": {"grant": false, "reason": "Least privilege; not needed before review/testing."},
        "summarize-session": {"grant": true, "reason": "May summarize own implementation work."}
      },
      "autonomy": {"level": "medium", "checkpoints": ["current-run plan approval", "approved writable paths"]},
      "container": {"workspace": "read-write", "memory": "omitted", "reason": "Needs bounded writes only after approval; memory omitted because no active workflow requires it."}
    },
    "reviewer": {
      "defined_in": ".claude/agents/reviewer.md",
      "mcp_storage": {
        "write_entry": {"grant": false, "reason": "Least privilege; independent review is read-only."},
        "read_entry": {"grant": true, "reason": "May read approved workflow state."},
        "list_entries": {"grant": true, "reason": "May find review-relevant records."},
        "update_entry": {"grant": false, "reason": "Least privilege; reviewer must not mutate state."},
        "delete_entry": {"grant": false, "reason": "Least privilege and audit preservation."},
        "audit_read": {"grant": false, "reason": "Least privilege; reviewer checks implementation evidence, not audit logs."}
      },
      "mcp_retrieval": {"retrieve": true, "ceiling": "internal", "reason": "May retrieve internal review guidance."},
      "skills": {
        "run-tests": {"grant": false, "reason": "Routing map assigns test execution to Tester."},
        "draft-pr-description": {"grant": false, "reason": "Least privilege; not part of independent review."},
        "summarize-session": {"grant": true, "reason": "May summarize own review."}
      },
      "autonomy": {"level": "low", "checkpoints": ["returns Pass or Revise only"]},
      "container": {"workspace": "read-only", "memory": "omitted", "reason": "Reviewer is independent and read-only."}
    },
    "tester": {
      "defined_in": ".claude/agents/tester.md",
      "mcp_storage": {
        "write_entry": {"grant": false, "reason": "Unsupported Tester success near-miss requires no state mutation."},
        "read_entry": {"grant": true, "reason": "May read approved test context."},
        "list_entries": {"grant": true, "reason": "May discover relevant test records."},
        "update_entry": {"grant": false, "reason": "Unsupported Tester success near-miss requires Tester to report only."},
        "delete_entry": {"grant": false, "reason": "Least privilege and audit preservation."},
        "audit_read": {"grant": false, "reason": "Least privilege; not a Tester duty."}
      },
      "mcp_retrieval": {"retrieve": true, "ceiling": "internal", "reason": "May retrieve internal testing guidance."},
      "skills": {
        "run-tests": {"grant": true, "reason": "Tester owns focused bounded test execution."},
        "draft-pr-description": {"grant": false, "reason": "Least privilege; Tester does not prepare release text."},
        "summarize-session": {"grant": true, "reason": "May summarize own test result."}
      },
      "autonomy": {"level": "low", "checkpoints": ["requires Reviewer Pass and complete handoff prerequisites"]},
      "container": {"workspace": "read-only", "memory": "omitted", "reason": "Tester must not repair or edit files."}
    },
    "project-manager": {
      "defined_in": ".claude/agents/project-manager.md",
      "mcp_storage": {
        "write_entry": {"grant": false, "reason": "External state update is handled through dedicated tracker-equivalent workflow, not storage writes."},
        "read_entry": {"grant": true, "reason": "May read final handoff state."},
        "list_entries": {"grant": true, "reason": "May locate final approval records."},
        "update_entry": {"grant": false, "reason": "Least privilege; do not mix storage mutation with issue-update duty."},
        "delete_entry": {"grant": false, "reason": "Least privilege and audit preservation."},
        "audit_read": {"grant": false, "reason": "Least privilege; not an audit role."}
      },
      "mcp_retrieval": {"retrieve": false, "ceiling": "none", "reason": "Final update role should not inspect repository or retrieval documents."},
      "skills": {
        "run-tests": {"grant": false, "reason": "Project Manager acts after testing and must not execute tests."},
        "draft-pr-description": {"grant": true, "reason": "May draft final handoff or release summary from approved evidence."},
        "summarize-session": {"grant": true, "reason": "May summarize the approved final workflow."}
      },
      "autonomy": {"level": "low", "checkpoints": ["explicit current-run final approval"]},
      "container": {"workspace": "read-only", "memory": "omitted", "reason": "Project Manager must not read or write repository files beyond approved handoff context."}
    }
  }
}
GOVERNANCE_POLICY_JSON_END -->
