# Agent Safety and Evidence Standards

**Last reviewed:** 2026-08-01
**Review by:** 2026-10-30
**Maintained by:** Muhammad Imran
**Agent access:** Read-only

These standards apply to every agent working in the `Muhammad7839/FitGPT-Agentic-Engineering` repository.

An agent must never modify this file or its directory permissions. A human must review and perform every change.

## Repository Scope

Work only in the isolated course repository:

`Muhammad7839/FitGPT-Agentic-Engineering`

Do not access, inspect, modify, test, mount, push to, or otherwise operate on:

`Muhammad7839/FitGPT`

A configured remote URL is not authorization to contact that remote.

## Secret and Sensitive-Data Exclusion

Never write any of the following to Git, persistent memory, documentation, transcripts intended for commit, agent definitions, or skills:

- Real `.env` contents
- API keys or tokens
- OAuth credentials
- Claude authentication data
- Signing files
- Service-account files
- SSH material
- Private emails or Slack content
- Personal data
- Real production secrets or environment values

Use approved runtime injection and scoped credential mounts when a task genuinely requires credentials.

## Evidence Hierarchy

For current runtime behavior:

1. Committed implementation and configuration provide direct evidence.
2. Focused tests provide evidence only for the behavior they actually exercise.
3. Documentation contains claims that must be compared with implementation and tests.
4. Inferences must be labeled as inferences.
5. Unsupported questions must remain open rather than being answered by assumption.

## Conclusion Calibration

A passing focused test does not prove:

- the complete backend works,
- production deployment is healthy,
- external integrations are configured,
- every environment is supported, or
- the entire application is production-ready.

State both the verified scope and important unverified scope.

## Read-Only Audit Standard

An audit or review agent must not modify:

- Application code
- Tests
- Documentation
- Configuration
- Git state

unless the human task explicitly authorizes those changes.

Evidence discovery does not authorize runtime execution. If the phase says to inspect committed files only, do not run tests, builds, application code, or validation commands.

## Git Integrity

- Preserve existing commit history.
- Do not amend, squash, rebase, force-push, or rewrite history without explicit human authorization.
- Do not push any branch unless the current task explicitly authorizes a push.
- Do not delete branches, tags, remotes, repositories, or evidence without explicit authorization.

## Memory Allocation

Do not place procedures in persistent memory.

Repeatable commands and workflows belong in:

- Agent definitions
- Skills
- Task instructions
- Approved operational documentation

Do not duplicate complete code, tests, reports, or configuration files in memory. Store a short decision or state entry and point to the authoritative artifact when detail is needed.

## Human Ownership

Agents may identify a possible correction to these standards, but they must stop and request human review.

Only a human may:

- make this directory writable,
- edit this file,
- add another Knowledge File,
- change the review date, or
- approve a superseding standard.
