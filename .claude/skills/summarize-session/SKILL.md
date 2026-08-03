---
name: summarize-session
description: Summarize a governed role's own work without expanding authority.
---

# summarize-session

## Activation Scope

<!-- ACTIVATION_SCOPE_JSON_START
{
  "skill": "summarize-session",
  "allowed_roles": ["orchestrator", "planner", "implementer", "reviewer", "tester", "project-manager"],
  "denied_roles": [],
  "reason": "Every governed role may summarize its own bounded work; this skill does not grant file, storage, retrieval, test, or tracker authority."
}
ACTIVATION_SCOPE_JSON_END -->

Summaries must describe only work already performed by the active role.
