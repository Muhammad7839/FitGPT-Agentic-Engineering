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

Role entries are added in later policy commits after the foundation is established.
