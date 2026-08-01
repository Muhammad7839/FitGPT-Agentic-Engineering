# Managed Session Summary

## Current Goal

Audit FitGPT's committed backend startup and configuration documentation
against current implementation and focused tests, and produce a prioritized,
source-backed report. The session has completed Phase 1 (Evidence Discovery)
and Phase 2 (Broad Recommendation Draft, prioritized by production risk). A
Phase 3 (final report) has not yet begun and no new stakeholder requirement
change has been introduced yet in this session.

## Active Requirements and Constraints

- Work read-only; no file may be created, edited, or deleted.
- Use only committed repository evidence — no network access, no invented
commands/behavior/environment values.
- Treat implementation and focused tests as authoritative for current runtime
behavior; treat documentation as a claim to be checked against that behavior.
- Keep verified fact, documentation claim, inference, and open question
clearly distinguishable at all times.
- Cite repository paths and line ranges wherever practical.
- Every recommendation carries a stable ID, a category, and (per Phase 2) a
production-risk priority tier with cited evidence and impact.
- Do not implement any recommendation.
- Do not claim the focused config-startup test verifies the complete backend
or production deployment.

## Superseded Requirements

None yet. Phase 2's permissions (recommendations may target documentation,
tests, or production code; prioritize by production risk) extended Phase 1's
read-only evidence-gathering scope but did not contradict or replace any Phase
1 rule. No stakeholder requirement change has occurred in this session so
far.

## Decisions Made So Far

- Confirmed via direct execution that backend/tests/test_config_startup.py
passes in isolation (7 passed, exit 0), matching the previously logged lab
result — used as authoritative runtime-behavior evidence, not as full-backend
verification.
- Determined that backend/app/ai/provider.py + backend/app/ai/service.py
(wired through routes.py) is the actual live AI code path, while
backend/app/groq_service.py and backend/app/chat_service.py are
unreferenced/dead code.
- Determined that FRONTEND_URL has no role in CORS and is used solely for
building password-reset/verification email links.
- Determined that no google_id/auth_provider column or migration exists
anywhere in the current schema/codebase, contradicting a specific
documentation claim.
- Determined that the enforced password-reset token lifetime (30 minutes, via
RESET_TOKEN_EXPIRE_MINUTES) conflicts with hardcoded "1 hour" user-facing text
and a matching doc claim.
- Adopted production risk as the Phase 2 prioritization rule, per the active
phase instruction.
- Produced 11 draft recommendations (R1–R11), each with category, priority
tier, evidence, and impact.

## Current State of the Recommendation Draft

ID: R1
Category: Production code (dead-code hygiene)
Priority: High
One-line summary: Resolve duplicate AI implementations — remove/deprecate
backend/app/groq_service.py and backend/app/chat_service.py (unused; only
app/ai/service.py/app/ai/provider.py is live).
---
ID: R2
Category: Production code (correctness)
Priority: High
One-line summary: Reconcile reset-token expiry: email.py:73 says "1 hour," but

RESET_TOKEN_EXPIRE_MINUTES (config.py:109) defaults to 30 minutes and is what
 crud.py:113 enforces.
---
ID: R3
Category: Documentation
Priority: High
One-line summary: Fix the Groq model claim (llama-3.1-8b-instant) across
CLAUDE.md, architecture.md, system_overview.md, api_endpoints.md, README.md —
 actual default is llama-3.3-70b-versatile (config.py:129), configurable via
GROQ_MODEL.
---
ID: R4
Category: Documentation
Priority: High
One-line summary: Fix README.md:123 claim that FRONTEND_URL is "used for CORS"

— CORS is governed solely by CORS_ORIGINS/DEFAULT_CORS_ORIGINS
(config.py:88-94,115).
---
ID: R5
Category: Documentation
Priority: Medium-High
One-line summary: Correct/remove architecture.md:119 claim of automatic
google_id/auth_provider column migrations — no such columns exist (models.py,
 main.py:137-231); needs history confirmation before final wording (see Q4).
---
ID: R6
Category: Documentation
Priority: Medium
One-line summary: Expand backend "Environment Variables" tables
(architecture.md:177-190, README.md:112-126) to cover ~18 currently
undocumented vars from config.py (e.g., ENVIRONMENT,
ALLOW_SQLITE_IN_PRODUCTION, STORAGE_BACKEND/S3_*,
AI_TIMEOUT_SECONDS/AI_MAX_TOKENS/AI_TEMPERATURE, ACCESS_TOKEN_EXPIRE_MINUTES,
 REFRESH_TOKEN_EXPIRE_DAYS, RESET_TOKEN_EXPIRE_MINUTES,
EXPOSE_RESET_TOKEN_IN_RESPONSE, SENTRY_DSN, MAX_UPLOAD_IMAGE_BYTES,
JWT_ALGORITHM, GOOGLE_WEB_CLIENT_ID).
---
ID: R7
Category: Documentation
Priority: Medium
One-line summary: Clarify DATABASE_URL docs: defaults to local SQLite when
unset; PostgreSQL is enforced only in production via
validate_runtime_configuration() (config.py:136-150), with
ALLOW_SQLITE_IN_PRODUCTION override.
---
ID: R8
Category: Documentation
Priority: Medium
One-line summary: Document the full DEFAULT_CORS_ORIGINS default set
(config.py:88-94: Vercel URL, fitgpt.tech, www.fitgpt.tech), not just the two
 localhost origins currently cited in CLAUDE.md/architecture.md.
---
ID: R9
Category: Documentation
Priority: Low-Medium
One-line summary: Document or remove backend/requirements-local.txt (lighter
dependency set; unreferenced by CI/Procfile, which use requirements.txt).
---
ID: R10
Category: Test coverage
Priority: Low-Medium
One-line summary: Add a focused test pinning DEFAULT_CORS_ORIGINS/CORS_ORIGINS

content so future doc/code drift is caught automatically.
---
ID: R11
Category: Documentation
Priority: Low
One-line summary: Document the security-headers middleware and explicit CORS
method/header allowlist (main.py:79-95), currently covered by tests but not
by any doc.

No recommendation has been implemented, rewritten, reprioritized, or removed
since this draft was produced.

## Evidence That Must Carry Forward

Verified facts (F1–F14):

- F1: config.py:104-134 defines ~27 env vars with defaults (full list includes
DATABASE_URL, SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES=60,
REFRESH_TOKEN_EXPIRE_DAYS=30, GOOGLE_CLIENT_ID/GOOGLE_WEB_CLIENT_ID,
RESET_TOKEN_EXPIRE_MINUTES=30, ENVIRONMENT, EXPOSE_RESET_TOKEN_IN_RESPONSE,
CORS_ORIGINS, OPENWEATHER_*, MAX_UPLOAD_IMAGE_BYTES, STORAGE_BACKEND+S3_*,
GROQ_API_KEY/GROQ_MODEL/GROQ_VISION_MODEL,
AI_TIMEOUT_SECONDS/AI_MAX_TOKENS/AI_TEMPERATURE, SENTRY_DSN).
- F2: GROQ_MODEL default = "llama-3.3-70b-versatile" (config.py:129).
- F3: validate_runtime_configuration() (config.py:136-150) enforces
SECRET_KEY/DATABASE_URL/no-SQLite only when ENVIRONMENT is prod/production;
confirmed by test_config_startup.py:47-76.
- F4: Live AI path is routes.py:18,47,1655,1913,1988,2065 → app/ai/service.py
→ app/ai/provider.py:40-56.
- F5: groq_service.py/chat_service.py have zero references outside themselves;
hardcode max_tokens=1024/1536, ignoring AI_MAX_TOKENS.
- F6: FRONTEND_URL (email.py:11,34,122) builds reset/verification links only;
- F7: RESET_TOKEN_EXPIRE_MINUTES (default 30, config.py:109) is enforced in
crud.py:113,121-127; single-use confirmed (crud.py:133-134).
- F8: email.py:73 hardcodes "1 hour" expiry text.
- F9: No google_id/auth_provider in models.py; main.py:137-231
_ensure_runtime_schema never adds them; Google auth matches by email
(google_oauth.py:39-101).
- F10: STORAGE_BACKEND accepts local/s3/r2; else RuntimeError at first use
(storage.py:77-86), not at startup.
- F11: backend/.env.example lists only 7 vars (DATABASE_URL, SECRET_KEY,
GROQ_API_KEY, GMAIL_ADDRESS, GMAIL_APP_PASSWORD, FRONTEND_URL,
OPENWEATHER_API_KEY).
- F12: CI (.github/workflows/test.yml:29-34) sets only
SECRET_KEY/DATABASE_URL, uses requirements.txt (differs from
requirements-local.txt).
- F13: Security headers + explicit CORS allowlist (main.py:79-95) confirmed by
test_security_headers.py.
- F14: Re-run of test_config_startup.py reproduced 7 passed, 0
failures/errors/warnings, exit 0.

Documentation claims (D1–D12) and Mismatches/Omissions (M1–M10) as enumerated
in the Phase 1 report remain the direct basis for R1–R11 and must not be
re-derived differently in Phase 3.

## Unresolved Questions

- Q1: Does the real production .env set RESET_TOKEN_EXPIRE_MINUTES=60 (making
email text/doc correct for prod while the 30-min value is only a local
default)? Not verifiable — no real .env/deployment config accessible. Bears
directly on final wording of R2.
- Q2: Is groq_service.py/chat_service.py intentionally retained
(reference/legacy) or accidentally undeleted dead code? Affects whether R1
should recommend deletion vs. deprecation labeling.
- Q3: Is backend/requirements-local.txt meant for a specific workflow, or
stale? Affects R9.
- Q4: Was google_id/auth_provider ever real and later removed, or was the
architecture.md:119 claim never accurate? Git history was not reviewed in
Phase 1; affects final wording of R5.
- Q5: Is the "185+ backend tests" / "617 web tests" claim (README.md:138,145)
still accurate? Flagged but explicitly out of scope for the config/startup
evidence gathered so far; not attached to any recommendation ID.

## Next Planned Action

Await the next explicit instruction. Per the pre-session plan, the anticipated
next step is a stakeholder requirement change (reprioritizing by onboarding
confusion/reproducibility instead of production risk, excluding
production-code recommendations, retaining only documentation/test-support
recommendations, and requiring an explicit "out of scope" statement) followed
by a Phase 3 final report that revisits R1–R11 under the new constraints. No
further audit action will be taken until that instruction is received.
