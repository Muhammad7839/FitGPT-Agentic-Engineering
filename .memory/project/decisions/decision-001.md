# Decision 001 — Onboarding-Focused Configuration Follow-Up

**Date:** 2026-08-01
**Review by:** 2026-10-30
**Status:** Active
**Scope:** FitGPT-Agentic-Engineering course repository

## Decision

Future follow-up from the backend configuration documentation audit will prioritize new-contributor onboarding documentation and test-support recommendations.

Production-code recommendations remain excluded unless a human explicitly reopens that scope.

## Why This Matters

The managed context session initially produced recommendations prioritized by production risk. The stakeholder requirement then changed: the intended audience became new contributors, and the final report was revised to focus on onboarding confusion and reproducibility.

A fresh session can inspect the final report but cannot reliably infer whether that stakeholder direction remains the active project decision. This entry records the current approved state without duplicating the full report.

## Current Implications

- Preserve documentation and test-support recommendations that improve onboarding clarity or reproducibility.
- Do not reintroduce production-code recommendations merely because an earlier draft contained them.
- Do not restore production-risk ordering as the current priority.
- Use committed implementation and focused tests as evidence when evaluating documentation claims.
- Keep conclusions limited to the evidence reviewed.

## Supporting Artifacts

- `docs/agents/backend-config-docs-auditor/final-report.md`
- `docs/agents/backend-config-docs-auditor/final-context-check.md`
- `docs/agents/backend-config-docs-auditor/iteration-log.md`

These files contain the detailed evidence and recommendation history. Read them when the task requires detail; do not copy their full contents into memory.

## Supersession Rule

This entry remains active until a human explicitly:

- reopens production-code recommendations,
- changes the intended audience,
- replaces the onboarding priority, or
- marks this entry superseded.

A superseding entry must update `.memory/project/MEMORY_INDEX.md`.

## Review Questions

At the review date, confirm:

1. Is onboarding still the intended audience?
2. Are documentation and test-support still the only allowed recommendation categories?
3. Has a human reopened production-code scope?
4. Do the supporting artifact paths remain current?
5. Should this entry remain active, be revised, or be archived?
