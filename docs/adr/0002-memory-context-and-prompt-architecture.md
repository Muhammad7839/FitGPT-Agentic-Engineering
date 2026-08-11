# ADR 0002: Memory, Context, And Prompt Architecture

## Context

The project uses role prompts, bounded evidence packets, and local memory rules. Historical calibration evidence in `docs/calibration-log.md` showed output-contract failures and later correction. The backend config auditor also preserved evidence of source precision problems in `docs/agents/backend-config-docs-auditor/lab/iteration-log.md`.

## Decision

Keep role prompts narrow, pass only required evidence, and preserve measured role outputs as artifacts. Treat memory as context support, not as proof; current repository files and run artifacts remain authoritative.

## Rejected Alternatives

- Broad shared context for every role. Rejected because it increases leakage and stale-evidence risk.
- Memory-only evidence. Rejected because memory may be stale and cannot replace committed files or measured artifacts.

## Evidence

- Calibration before-fix run `CAL-20260802-002` preserved a Tester output-contract failure.
- AURA HIGH used separate Planner, Implementer, Reviewer, Tester, and Project Manager evidence with zero authorization denials.

## Consequences

Roles stay easier to audit and route metrics remain comparable.

## Open Risks

Long multi-role runs still require careful artifact naming and final sanity checks to avoid mixing stale attempts with valid attempts.
