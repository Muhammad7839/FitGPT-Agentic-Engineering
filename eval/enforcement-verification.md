# Enforcement Verification

## New Role

- Role: `dependency-auditor`
- Policy commit: `29d07b1f56b38c8d7bbcac27acf30a901ff10d5d`
- Enforcement commit: `7e8831c3bae423cf74515d793be1504b17ff83e5`
- Date: 2026-08-03
- Branch and HEAD: `module-4-governance-foundation`

## Runtime Status

`agentic_engineer_4:latest` is not available locally. Container enforcement, MCP Inspector verification, audit-log evidence, and live red-team agent execution are pending. This document records static design and policy-test evidence only until the image is restored.

## Layer 1: Container Permissions

### Workspace check

Runtime result: PENDING

Required command after image restoration:

```text
scripts/run-agent.sh reviewer bash -lc 'touch /workspace/should-fail.txt'
```

Dependency-auditor protected-manifest check:

```text
scripts/run-agent.sh dependency-auditor bash -lc 'echo forbidden > /workspace/web/package.json'
```

### Memory-volume check

Runtime result: PENDING

Required command after image restoration:

```text
scripts/run-agent.sh reviewer bash -lc 'if grep -q " /memory " /proc/mounts; then echo "unexpected: /memory is mounted"; exit 1; else echo "OK: /memory is not mounted"; fi'
```

### Read-access check

Runtime result: PENDING

Required command after image restoration:

```text
scripts/run-agent.sh reviewer bash -lc 'test -r /workspace/backend/requirements.txt && echo OK'
```

## Layer 2: MCP Server Allow-Lists

### Denied operation check

Runtime result: PENDING

Expected denied operation: `implementer` attempts `delete_entry`.

### Granted operation check

Runtime result: PENDING

Expected granted operation: `planner` or `reviewer` uses `read_entry` on controlled course state.

### Classification ceiling check

Runtime result: PENDING

Expected withheld result: `implementer` requests confidential retrieval material and receives only internal-or-lower matches with confidential content withheld.

## Skill Activation Scope

Static scopes are defined in:

- `.claude/skills/run-tests/SKILL.md`
- `.claude/skills/draft-pr-description/SKILL.md`
- `.claude/skills/summarize-session/SKILL.md`

Runtime result: PENDING

## Policy Test Suite

Static result recorded after dependency-auditor enforcement:

```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.1, pluggy-1.6.0 -- /Applications/Xcode.app/Contents/Developer/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/muhammad/course-projects/FitGPT-Agentic-Engineering
configfile: pytest.ini
plugins: anyio-4.12.1, hydra-core-1.3.2
collecting ... collected 16 items

eval/test_policy.py::test_policy_json_is_valid_and_complete PASSED       [  6%]
eval/test_policy.py::test_every_governed_role_has_definition PASSED      [ 12%]
eval/test_policy.py::test_active_agent_definitions_have_policy_when_in_governed_workflow PASSED [ 18%]
eval/test_policy.py::test_storage_allow_list_matches_policy PASSED       [ 25%]
eval/test_policy.py::test_retrieval_allow_list_matches_policy PASSED     [ 31%]
eval/test_policy.py::test_skill_scopes_match_policy PASSED               [ 37%]
eval/test_policy.py::test_container_workspace_modes_match_policy PASSED  [ 43%]
eval/test_policy.py::test_container_memory_decisions_match_policy PASSED [ 50%]
eval/test_policy.py::test_unknown_roles_are_denied_by_startup_script PASSED [ 56%]
eval/test_policy.py::test_no_role_receives_undocumented_storage_operation PASSED [ 62%]
eval/test_policy.py::test_no_role_exceeds_classification_ceiling PASSED  [ 68%]
eval/test_policy.py::test_read_only_roles_have_no_state_changing_storage_grants PASSED [ 75%]
eval/test_policy.py::test_project_manager_cannot_run_tests PASSED        [ 81%]
eval/test_policy.py::test_reviewer_cannot_run_tests PASSED               [ 87%]
eval/test_policy.py::test_tester_cannot_update_external_state PASSED     [ 93%]
eval/test_policy.py::test_implementer_cannot_delete_stored_state PASSED  [100%]

============================== 16 passed in 0.03s ==============================
```

## Human Auditability Check

From the committed policy and allow-lists:

- `dependency-auditor` cannot modify dependency manifests through the container policy because `scripts/run-agent.sh` assigns it a read-only `/workspace` mount.
- `dependency-auditor` cannot modify governance storage through the storage allow-list because `write_entry`, `update_entry`, `delete_entry`, and `audit_read` are denied.
- `dependency-auditor` cannot retrieve confidential documents through the retrieval allow-list because its ceiling is `internal`.
- Runtime filesystem, MCP Inspector, audit-log, and agent red-team proof remains PENDING until `agentic_engineer_4:latest` is restored.
