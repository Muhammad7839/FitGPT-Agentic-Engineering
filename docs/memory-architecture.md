# Memory Architecture

## What this workflow needs to remember

The `backend-config-docs-auditor` supports recurring audits of FitGPT backend startup and configuration documentation. Across sessions, it needs to remember the currently approved follow-up scope, unresolved or deferred priorities, and decisions that cannot be inferred reliably from implementation files alone. It does not need to store exact configuration values, test assertions, agent prompts, or complete reports because those already exist as committed project artifacts. It must never store credentials, real environment values, authentication data, personal information, raw transcripts, or temporary state tied only to a completed run.

## Layer 1: Project memory directory

### Purpose

`.memory/project/` stores evolving project context that a fresh session needs in order to resume work without reopening settled decisions.

### Belongs here

- The active decision that backend configuration follow-up is currently onboarding-focused.
- The current rule that documentation and test-support recommendations remain in scope while production-code recommendations remain excluded unless a human explicitly reopens them.
- A future unresolved question or deferred priority that changes how the next audit should proceed.
- A superseding decision that replaces an earlier active project-memory entry.
- A current workflow phase when that phase cannot be inferred reliably from repository files.

### Does not belong here

- Exact pytest, Docker, or Git procedures; these belong in skills, agent definitions, or task instructions.
- Full copies of reports, tests, configuration files, or documentation already committed elsewhere.
- Temporary test paths, timestamps, token counts, or one-run observations.
- Credentials, real environment values, personal data, or authentication material.

### Scope

Project-scoped to `Muhammad7839/FitGPT-Agentic-Engineering`.

It does not apply to the original `Muhammad7839/FitGPT` repository or any other clone.

### Write permissions

The agent may propose additions or updates to `.memory/project/`, but a human must review the proposed content before it is committed.

The agent must check `.memory/project/MEMORY_INDEX.md` before creating a new entry and must update an existing topic rather than create a duplicate.

### Review and pruning

- Every active decision entry has a concrete review date.
- Project-scoped entries are reviewed at least every 90 days.
- A superseded entry is marked superseded immediately and points to its replacement.
- Workflow-specific entries are archived when their workflow is completed or explicitly abandoned.
- Entries that duplicate current repository artifacts are removed and replaced with a short pointer when useful.

## Layer 2: Knowledge files

### Purpose

`.memory/knowledge/` contains stable, human-maintained constraints that should guide agents across many sessions.

### Belongs here

- Repository isolation and original-repository protection rules.
- Secret-handling and sensitive-data exclusions.
- Evidence standards distinguishing implementation, tests, documentation claims, inference, and open questions.
- The rule that focused tests justify only narrowly scoped conclusions.
- Git-history and explicit-push-authorization constraints.
- Read-only audit expectations.

### Does not belong here

- Current priorities or temporary project phases, because those change and belong in project memory.
- Step-by-step commands, because procedures belong in skills or task instructions.
- Machine-generated observations that have not received human review.
- Credentials, tokens, private data, or real environment values.

### Scope

Project-scoped and applicable to every agent working in the isolated course repository.

### Write permissions

Human-maintained and read-only for agents.

An agent may identify a possible correction but must not modify this directory or its permissions. A human must make and review every change.

### Review and pruning

- Review every 90 days and whenever repository ownership, deployment policy, or course safety requirements change.
- Replace a rule when a human approves a superseding standard.
- Remove rules that no longer affect future agent behavior.
- Restore read-only protection after every human-approved update.

## Layer 3: Indexed reference documents

### Purpose

`.memory/reference/` is reserved for large, historical, or infrequently needed material that should be located through an index and read only when relevant.

### Current state

No reference documents are currently stored.

The existing committed documentation, reports, tests, and configuration files remain discoverable through ordinary repository paths and do not justify duplication into the reference layer.

### Future candidates

- A large collection of historical architecture decisions that cannot be navigated efficiently through existing documentation.
- Sanitized external design material that is necessary for occasional audits but should not load at every startup.
- A substantial set of historical release or migration notes needed only for specialized tasks.

### Does not belong here

- Frequently used current standards, which belong in Knowledge Files.
- Current decisions and priorities, which belong in Project Memory.
- Full duplicates of existing repository documentation.
- Secrets, personal data, raw transcripts, credentials, or unreviewed external content.

### Scope

Project-scoped to the course repository.

### Write permissions

Human-maintained and read-only for agents.

Reference documents may be added only after human review and must be listed in `.memory/reference/MEMORY_INDEX.md`.

### Review and pruning

- Review the index every 180 days or when a referenced source is superseded.
- Remove duplicated or obsolete references.
- Replace a reference when a newer authoritative version is approved.
- Keep the layer empty until a genuine retrieval need exists.

## Allocation decision table

| Information | Allocation | Reason |
|---|---|---|
| Current onboarding-focused follow-up decision | Project memory | It changes over time and affects how a fresh session resumes work. |
| Repository isolation and evidence standards | Knowledge file | These are stable human-owned constraints across sessions and agents. |
| Exact focused-test command | Agent definition, skill, or task input | It is a repeatable procedure, not persistent state. |
| Existing test assertions and environment configuration | Existing repository artifacts | Code and tests already preserve these facts authoritatively. |
| Full managed-session audit report | Existing documentation | The report is already committed and should be referenced rather than duplicated. |
| Temporary SQLite path and evidence directory | Context window or Iteration Log | They matter only to one completed run. |
| Credentials and real environment values | Excluded; secure runtime injection only | Sensitive information must never enter persistent memory. |
| Future large historical design collection | Indexed references | It should be retrieved selectively rather than loaded every session. |

## Alternatives considered

The onboarding-focused recommendation decision could have remained only in the final audit report. That would preserve the history but would not clearly tell a fresh session whether the stakeholder decision remains active. A short project-memory Decision Entry was selected because it records the current approved state, links to the detailed report, and includes an explicit review and supersession policy without duplicating the complete report.
