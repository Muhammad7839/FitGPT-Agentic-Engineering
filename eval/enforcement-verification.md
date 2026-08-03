# Enforcement Verification

## New Role

- Role: pending until dependency-auditor is added
- Policy commit: pending
- Enforcement commit: pending
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

Final static output is added after `pytest eval/test_policy.py -v` runs.

## Human Auditability Check

Pending until dependency-auditor is added.
