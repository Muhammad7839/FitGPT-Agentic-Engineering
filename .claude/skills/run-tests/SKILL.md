---
name: run-tests
description: Run approved focused checks for governed roles that own test execution.
---

# run-tests

## Activation Scope

<!-- ACTIVATION_SCOPE_JSON_START
{
  "skill": "run-tests",
  "allowed_roles": ["implementer", "tester"],
  "denied_roles": ["orchestrator", "planner", "reviewer", "project-manager"],
  "reason": "Only Implementer and Tester have policy permission to run focused checks; Reviewer and Project Manager are explicitly denied."
}
ACTIVATION_SCOPE_JSON_END -->

Use only when the active role is listed in `allowed_roles` and the task scope supplies an approved test target.
