# Backend Configuration Documentation Alignment Report

## Scope

This audit compares FitGPT's committed backend startup and configuration
documentation (CLAUDE.md, README.md, docs/features/architecture.md,
docs/features/system_overview.md, docs/features/api_endpoints.md,
docs/development/storage-backends.md, backend/.env.example) against the
committed implementation (backend/app/config.py, backend/app/main.py,
backend/app/database/database.py, backend/app/storage.py,
backend/app/email.py, backend/app/google_oauth.py, backend/app/ai/*,
backend/app/groq_service.py, backend/app/chat_service.py) and the focused
configuration test suite (backend/tests/test_config_startup.py,
backend/tests/test_security_headers.py).

Following the stakeholder update, this report is written for new contributors
onboarding to the FitGPT backend, not for production-remediation planning.
Recommendations are prioritized by likely onboarding confusion and
reproducibility impact (i.e., how much a gap would slow down or mislead
someone trying to understand, run, or test the backend for the first time),
not by production risk. Every recommendation in this report is a documentation
or test-support change; no recommendation proposes modifying
application/production code.

## Evidence Reviewed

Unchanged from Phase 1/2 evidence gathering (read-only; no files modified in
any phase):

- Configuration implementation: backend/app/config.py:1-171,
backend/app/database/database.py:1-27, backend/app/storage.py:1-87,
backend/app/main.py:1-290
- AI code paths: backend/app/ai/provider.py:1-156,
backend/app/ai/service.py:1-829, backend/app/groq_service.py:1-189,
backend/app/chat_service.py:1-313
- Auth/email: backend/app/email.py:1-183, backend/app/google_oauth.py:1-101,
backend/app/crud.py:107-134, backend/app/routes.py (import list :1-35;
token/reset routes :662,697,816,900-953), backend/app/models.py
- Tests: backend/tests/test_config_startup.py:1-76 (7 tests),
backend/tests/test_security_headers.py:1-67, backend/tests/conftest.py:1-66
- Documentation: CLAUDE.md, README.md:1-165,
docs/features/architecture.md:1-207, docs/features/system_overview.md:1-145,
docs/features/api_endpoints.md:280-320,
docs/development/storage-backends.md:1-197, backend/.env.example:1-7
- CI/deploy config: .github/workflows/test.yml:1-62, backend/requirements.txt
vs backend/requirements-local.txt, backend/Procfile
- Command executed (read-only):
cd /workspace/backend && PYTHONDONTWRITEBYTECODE=1 ENVIRONMENT=test
SECRET_KEY=sandbox-test-only \
DATABASE_URL=sqlite:////tmp/fitgpt_lab_config_audit.db
TEST_DATABASE_URL=sqlite:////tmp/fitgpt_lab_config_audit.db \
STORAGE_BACKEND=local OPENWEATHER_API_KEY= GROQ_API_KEY= GOOGLE_CLIENT_ID=
GOOGLE_WEB_CLIENT_ID= \
GMAIL_ADDRESS= GMAIL_APP_PASSWORD= SENTRY_DSN= pytest -p no:cacheprovider -q
tests/test_config_startup.py
- Result: 7 passed in 0.29s, exit status 0. No repository file was created or
modified during any phase of this audit.

## Confirmed Current Behavior

(Verified facts F1–F14 from Phase 1, unchanged and carried forward —
reproduced here for onboarding relevance.)

- F1. backend/app/config.py:104-134 defines roughly 27 backend env vars, most
with working defaults, including DATABASE_URL, SECRET_KEY, JWT_ALGORITHM,
ACCESS_TOKEN_EXPIRE_MINUTES (60), REFRESH_TOKEN_EXPIRE_DAYS (30),
GOOGLE_CLIENT_ID/GOOGLE_WEB_CLIENT_ID, RESET_TOKEN_EXPIRE_MINUTES (30),
ENVIRONMENT, EXPOSE_RESET_TOKEN_IN_RESPONSE, CORS_ORIGINS, OPENWEATHER_*,
MAX_UPLOAD_IMAGE_BYTES, STORAGE_BACKEND+S3_*,
GROQ_API_KEY/GROQ_MODEL/GROQ_VISION_MODEL,
AI_TIMEOUT_SECONDS/AI_MAX_TOKENS/AI_TEMPERATURE, SENTRY_DSN.
- F2. GROQ_MODEL default is "llama-3.3-70b-versatile" (config.py:129).
- F3. validate_runtime_configuration() (config.py:136-150) only enforces
strict production rules when ENVIRONMENT is prod/production; a local
contributor running the backend with no .env at all gets a working SQLite
database with no errors — confirmed by test_config_startup.py:47-76.
- F4. The only AI code path wired into the running app is
routes.py:18,47,1655,1913,1988,2065 → app/ai/service.py →
app/ai/provider.py:40-56, which reads
GROQ_MODEL/AI_MAX_TOKENS/AI_TEMPERATURE/AI_TIMEOUT_SECONDS from config.py.
- F5. backend/app/groq_service.py and backend/app/chat_service.py are not
referenced anywhere in backend/app or backend/tests (confirmed by grep); they
hardcode max_tokens=1024/1536, ignoring AI_MAX_TOKENS.
- F6. FRONTEND_URL (email.py:11,34,122) builds password-reset/verification
links only. CORS is governed entirely by CORS_ORIGINS/DEFAULT_CORS_ORIGINS
(config.py:88-94,115) applied in main.py:68-76.
- F7. RESET_TOKEN_EXPIRE_MINUTES defaults to 30 (config.py:109) and is the
value actually enforced (crud.py:113,121-127); tokens are single-use
(crud.py:133-134).
- F8. email.py:73 hardcodes the user-facing text "This link will expire in 1
hour."
- F9. No google_id/auth_provider column exists in backend/app/models.py;
main.py:137-231 (_ensure_runtime_schema) never adds one. Google sign-in
matches purely by verified email (google_oauth.py:39-101).
- F10. STORAGE_BACKEND (config.py:122, storage.py:77-86) accepts local/s3/r2;
any other value raises RuntimeError at first use, not at process startup.
- F11. backend/.env.example lists only 7 vars: DATABASE_URL, SECRET_KEY,
GROQ_API_KEY, GMAIL_ADDRESS, GMAIL_APP_PASSWORD, FRONTEND_URL,
OPENWEATHER_API_KEY.
- F12. CI (.github/workflows/test.yml:29-34) installs backend/requirements.txt
(not requirements-local.txt) and sets only SECRET_KEY/DATABASE_URL before
running pytest -q.
- F13. Security headers and an explicit CORS method/header allowlist are
applied in main.py:79-95, confirmed by 6 passing assertions in
test_security_headers.py.
- F14. Re-running test_config_startup.py in isolation reproduced 7 passed, 0
failures/errors/warnings, exit 0 — consistent with the previously logged lab
run.

## Documentation Gaps

Unchanged in substance from Phase 1 (D1–D12 claims, M1–M10
mismatches/omissions); restated here as the direct basis for the
recommendations below:

- Multiple docs (CLAUDE.md, architecture.md, system_overview.md,
api_endpoints.md, README.md) state the Groq model is llama-3.1-8b-instant and
imply groq_service.py/chat_service.py are the live implementation —
contradicted by F2/F4/F5.
- README.md:123 states FRONTEND_URL is "used for CORS" — contradicted by F6.
- architecture.md:119 claims automatic google_id/auth_provider column
migrations — contradicted by F9.
- architecture.md:128 and email.py:73 both say reset tokens last "1 hour" —
the enforced default is 30 minutes (F7/F8).
- architecture.md's and README.md's environment-variable tables omit roughly
18 of the ~27 vars defined in config.py (F1).
- README.md:118 frames DATABASE_URL as a required PostgreSQL string without
noting the working local SQLite default (F1/F3).
- CLAUDE.md/architecture.md describe only two default CORS origins, omitting
the three additional deployed-origin defaults baked into DEFAULT_CORS_ORIGINS
(F1).
- backend/requirements-local.txt exists but is undocumented and unreferenced
by CI/Procfile (F12), creating a plausible wrong-file trap for a new
contributor following the README's install step.
- No document describes the security-headers middleware or CORS allowlist
behavior verified by test_security_headers.py (F13).

## Prioritized Onboarding Recommendations

All recommendations below are documentation or test-support only, consistent
with the stakeholder's updated scope. Priorities reflect likely onboarding
confusion and reproducibility impact, not production risk.
---
R9 — Category: Documentation — Priority: High
Document the purpose and status of backend/requirements-local.txt, or note in
the README that it is not the file used by CI/deploy and should not be used
for standard setup.
Supporting evidence: README.md:53-56 instructs pip install -r
requirements.txt; backend/requirements-local.txt exists alongside it with a
materially different, smaller dependency set (missing groq, boto3, sentry-sdk,
psycopg2-binary, pytest); CI (.github/workflows/test.yml:21,27) and
Procfile:1 both use only requirements.txt (F12).
Onboarding benefit: A new contributor guessing between two similarly-named
requirements files (one literally named "local") could reasonably install the
wrong one and then hit confusing ModuleNotFoundErrors or missing pytest when
trying to run the test suite for the first time — this is a direct,
first-session reproducibility blocker.

---
R1 (rewritten) — Category: Documentation — Priority: High
Add a note in CLAUDE.md/docs/features/architecture.md clarifying that
backend/app/groq_service.py and backend/app/chat_service.py are not used by
the running application — the live AI recommendation and chat path is
backend/app/ai/service.py + backend/app/ai/provider.py, reached via routes.py.
Supporting evidence: F4/F5 — grep confirms zero references to
groq_service.py/chat_service.py anywhere in backend/app or backend/tests;
routes.py:18,47,1655,1913,1988,2065 wires only AiService.
Onboarding benefit: A contributor exploring "how does AI recommendation/chat
work" will find two complete, plausible-looking Groq implementations. Without
a documented pointer to the correct one, they can easily study, modify
expectations around, or attempt to "fix" the wrong file and observe no effect
— a significant source of wasted exploration time with no code change required
to resolve.

---
R3 — Category: Documentation — Priority: High
Correct the Groq model name claim (llama-3.1-8b-instant) in CLAUDE.md,
architecture.md, system_overview.md, api_endpoints.md, and README.md to
reflect that the model is configurable via GROQ_MODEL (config.py:129),
defaulting to llama-3.3-70b-versatile.
Supporting evidence: M1/D1 vs F2 — the incorrect model name appears in at
least 7 separate locations across 5 documents.
Onboarding benefit: A new contributor cross-referencing docs against code (a
very common onboarding activity) will hit an immediate, repeated
inconsistency, undermining confidence in the rest of the documentation set and
prompting unnecessary "which is right?" investigation.

---
R4 — Category: Documentation — Priority: High
Correct README.md:123's claim that FRONTEND_URL is "used for CORS." Clarify
that CORS is controlled solely by CORS_ORIGINS (default set in
config.py:88-94), while FRONTEND_URL only builds password-reset/verification
email links.
Supporting evidence: M2/D3 vs F6.
Onboarding benefit: Local frontend/backend integration (a near-universal first
onboarding task) commonly surfaces CORS errors in the browser console. A
contributor following the README would edit the wrong variable, see no effect,
and could lose significant time before discovering CORS_ORIGINS is the actual
mechanism — a direct reproducibility obstacle for the "get the app running
end-to-end locally" milestone.

---
R7 — Category: Documentation — Priority: High
Clarify that DATABASE_URL defaults to a local SQLite file when unset
(config.py:99-103), and that PostgreSQL is required only when ENVIRONMENT is
prod/production (validate_runtime_configuration(), config.py:136-150), with
ALLOW_SQLITE_IN_PRODUCTION as an explicit override.
Supporting evidence: M7/D2 vs F1/F3 — confirmed by
test_config_startup.py:47-76.
Onboarding benefit: README.md:18,118 currently reads as though a real
PostgreSQL connection string is required to run the backend at all. A new
contributor could stall on setting up a database before realizing the backend
runs out of the box with SQLite — this directly affects whether a first-time
setup is quick and reproducible.

---
R6 — Category: Documentation — Priority: Medium-High
Expand the backend "Environment Variables" tables in architecture.md:177-190
and README.md:112-126 to include the currently undocumented vars in config.py
(at minimum: ENVIRONMENT, ALLOW_SQLITE_IN_PRODUCTION, STORAGE_BACKEND+S3_*,
AI_TIMEOUT_SECONDS/AI_MAX_TOKENS/AI_TEMPERATURE, ACCESS_TOKEN_EXPIRE_MINUTES,
REFRESH_TOKEN_EXPIRE_DAYS, RESET_TOKEN_EXPIRE_MINUTES,
EXPOSE_RESET_TOKEN_IN_RESPONSE, SENTRY_DSN, MAX_UPLOAD_IMAGE_BYTES,
JWT_ALGORITHM, GOOGLE_WEB_CLIENT_ID).
Supporting evidence: M6/D8/D9/D12 vs F1.
Onboarding benefit: New contributors have no documented way to discover these
configuration levers exist at all, which reduces their ability to safely tune
behavior (e.g., shortening AI timeouts for local testing, or knowing
STORAGE_BACKEND defaults to local) without reading config.py line-by-line.

---
R2 (rewritten) — Category: Documentation — Priority: Medium
Correct architecture.md:128's claim that "reset tokens expire after 1 hour" to
state the actual enforced default (RESET_TOKEN_EXPIRE_MINUTES = 30 minutes,
config.py:109, enforced in crud.py:113), and flag in the documentation that
the reset email's own wording (email.py:73, "1 hour") does not match this
default, pending maintainer confirmation of intended behavior.
Supporting evidence: M4/D7 vs F7/F8. (Note: whether production deployment
overrides this to 60 minutes is unresolved — see Open Questions, Q1 — so this
recommendation corrects the doc to match the verified default, and documents
the discrepancy as an open item, rather than asserting a single "correct"
value.)
Onboarding benefit: A contributor testing the password-reset flow locally
(using the default 30-minute window) who has read "expires after 1 hour" may
be confused when a 45-minute-old token doesn't work as expected during manual
testing.

---
R5 — Category: Documentation — Priority: Medium
Correct or remove architecture.md:119's claim that "column migrations for
google_id and auth_provider run automatically on startup," since no such
columns exist in models.py and _ensure_runtime_schema (main.py:137-231) never
adds them. Ideally, describe the actual mechanism (email-based matching in
google_oauth.py:39-101) instead.
Supporting evidence: M3/D6 vs F9.
Onboarding benefit: A contributor investigating Google sign-in or planning to
add a schema-inspection habit (a common onboarding technique — "read the
startup migration list to understand the schema") would be misled about what
columns exist, and could waste time searching for migration logic that isn't
present.

---
R8 — Category: Documentation — Priority: Medium
Document the full default CORS origin list (DEFAULT_CORS_ORIGINS,
config.py:88-94: two localhost origins plus a Vercel preview URL, fitgpt.tech,
and www.fitgpt.tech), rather than describing only the two localhost defaults
in CLAUDE.md/architecture.md.
Supporting evidence: M5/D4/D5 vs F1.
Onboarding benefit: Lower urgency for local-only onboarding (localhost origins
are already documented correctly), but a contributor trying to understand
full request-flow behavior (e.g., testing against a deployed preview) would
otherwise have an incomplete picture of what's actually allowed by default.

---
R10 — Category: Test-support — Priority: Medium
Add a focused test (in test_config_startup.py or a new file) that pins the
content of DEFAULT_CORS_ORIGINS and/or the resulting CORS_ORIGINS, so future
documentation about the CORS allowlist can be trusted to stay accurate.
Supporting evidence: M5 — the existing test_get_list_env_parses_cors_origins
(test_config_startup.py:35-44) only tests the parsing helper, not the actual
default list content.
Onboarding benefit: Gives new contributors (and future doc authors) a
reliable, test-enforced source of truth for the CORS defaults, reducing the
chance that documentation like R8's fix silently goes stale again.

---
R11 — Category: Documentation — Priority: Low
Add a short description of the security-headers middleware and explicit CORS
method/header allowlist (main.py:79-95) to architecture.md/CLAUDE.md, since
this is active, tested startup behavior with no documentation footprint.
Supporting evidence: M9; behavior confirmed correct and tested via
test_security_headers.py.
Onboarding benefit: Minor completeness improvement — helps a new contributor
understand response headers they'll see in local testing/curl output, but
doesn't block any onboarding task.
## Recommendations Changed or Removed After the Stakeholder Update

ID: R1
Phase 2 category / priority: Production code / High
Disposition: Rewritten (now Documentation / High)
Explanation: Original recommendation proposed deleting or modifying
groq_service.py/chat_service.py — a production-code change, now excluded.
Rewritten to instead document (in CLAUDE.md/architecture.md) that these files
 are unused legacy code and that the live path is app/ai/*. This preserves
the onboarding value (avoiding confusion between two AI implementations)
without touching application code.
---
ID: R2
Phase 2 category / priority: Production code / High
Disposition: Rewritten (now Documentation / Medium)
Explanation: Original recommendation proposed changing either email.py's copy
or config.py's default — both production-code changes, now excluded.
Rewritten to instead correct the documentation claim to match the verified
default (30 minutes) and flag the email-text/config discrepancy as an open
item rather than resolving it via code. Priority lowered from High to Medium
because, reframed as a documentation fix, its onboarding impact (confusion
during manual QA of the reset flow) is real but narrower than
R3/R4/R7/R9/R1's broader first-session impact.
---
ID: R3
Phase 2 category / priority: Documentation / High
Disposition: Retained, reprioritized (still High)
Explanation: Purely a documentation fix already; no rewrite needed. Priority
retained at High — under the onboarding lens, a documentation claim
contradicted in 7 locations across the docs a new contributor is most likely
to read first (CLAUDE.md, architecture.md) remains high-impact for onboarding
 confusion.
---
ID: R4
Phase 2 category / priority: Documentation / High
Disposition: Retained, reprioritized (still High)
Explanation: Already documentation-only. Retained at High; reframed rationale
shifted from "production CORS misconfiguration risk" to "reproducibility
blocker during first local frontend/backend integration," which is arguably
an even more universal new-contributor pain point.
---
ID: R5
Phase 2 category / priority: Documentation / Medium-High
Disposition: Retained, reprioritized (now Medium)
Explanation: Already documentation-only. Lowered from Medium-High to Medium:
under production-risk framing this concerned schema/migration planning; under
 onboarding framing its impact is narrower (mainly affects someone
specifically investigating Google auth or schema history), so it ranks below
the broader-impact items (R1, R3, R4, R6, R7, R9).
---
ID: R6
Phase 2 category / priority: Documentation / Medium
Disposition: Retained, reprioritized (now Medium-High)
Explanation: Already documentation-only. Raised from Medium to Medium-High:
for
a new contributor, discoverability of configuration levers (rather than
production-safety implications) is the dominant concern, and this gap covers
the largest number of undocumented variables.
---
ID: R7
Phase 2 category / priority: Documentation / Medium
Disposition: Retained, reprioritized (now High)
Explanation: Already documentation-only. Raised from Medium to High: under
production-risk framing this was about operators misconfiguring deployments;
under onboarding framing it directly affects whether a brand-new contributor
can start the backend at all without additional setup, which is a first-hour
reproducibility concern.
---
ID: R8
Phase 2 category / priority: Documentation / Medium
Disposition: Retained, reprioritized (still Medium)
Explanation: Already documentation-only. Priority essentially unchanged —
moderate onboarding relevance (understanding full request-flow behavior) but
not a blocker for core local setup tasks.
---
ID: R9
Phase 2 category / priority: Documentation / Low-Medium
Disposition: Retained, reprioritized (now High)
Explanation: Already documentation-only. Raised substantially from Low-Medium
to High: under production-risk framing this had no deploy impact (CI/Procfile
 use the correct file); under onboarding framing it is one of the most
concrete, literal first-command pitfalls (pip  install -r
requirements-local.txt looks like the natural choice for "local" development)
 and can directly break test-suite reproducibility.
---
ID: R10
Phase 2 category / priority: Test coverage / Low-Medium
Disposition: Retained, reprioritized (now Medium)
Explanation: Test-support category explicitly permitted under the new scope.
Raised slightly from Low-Medium to Medium: preventing future doc/code drift
has ongoing value for onboarding trust in the docs, independent of production
 risk.
---
ID: R11
Phase 2 category / priority: Documentation / Low
Disposition: Retained (still Low)
Explanation: Already documentation-only. Priority unchanged — a completeness
gap with minimal onboarding-task impact under either framing.

No Phase 2 recommendation was fully removed; the two production-code
recommendations (R1, R2) were rewritten into documentation-only equivalents
rather than discarded, since their underlying evidence (dead-code confusion;
expiry-text mismatch) remains directly relevant to new-contributor
understanding even without a code change.

## Open Questions

Carried forward unchanged from Phase 1/2, still unresolved:

- Q1. Does the real production .env set RESET_TOKEN_EXPIRE_MINUTES=60 (making
the email/doc "1 hour" text correct for production while 30 minutes is only
the local default)? Not verifiable from committed evidence — no real .env or
deployment configuration is accessible. Directly affects the final wording of
R2.
- Q2. Is groq_service.py/chat_service.py intentionally retained as
legacy/reference code, or accidentally undeleted dead code? Affects whether
R1's documentation note should describe the files as "deprecated, pending
removal" or simply "unused."
- Q3. Is backend/requirements-local.txt meant for a specific workflow (e.g.,
avoiding native/S3/Sentry dependencies in constrained environments), or is it
stale? Affects whether R9 should recommend documenting its purpose or flagging
it for removal.
- Q4. Was google_id/auth_provider column-based migration ever real and later
removed, or was the architecture.md:119 claim never accurate? Git history was
not reviewed in this audit; affects the final wording of R5.
- Q5. Is the "185+ backend tests" / "617 web tests" claim (README.md:138,145)
still accurate? Not attached to any recommendation ID; remains a candidate for
a separate, differently-scoped check.

## Out of Scope

This audit did not validate:

- The complete FitGPT backend beyond the configuration/startup surface
examined (config.py, main.py, database.py, storage.py, the AI provider/service
layer, email/auth helpers) and the two focused test files reviewed
(test_config_startup.py, test_security_headers.py).
- Any production or staging deployment platform (Render, Vercel), real
environment variables, or live secrets.
- Any live external integration — Groq API, OpenWeatherMap, Gmail SMTP, Google
OAuth, or S3/R2 object storage — beyond confirming which environment
variables and code paths would invoke them.
- The frontend (web/) or Android (app/) codebases.
- The full backend or frontend test suites (only test_config_startup.py and
test_security_headers.py were executed or read in detail; broader suite counts
cited in README.md were not independently verified — see Q5).
- Git history or authorship, which would be needed to resolve Q2 and Q4 with
certainty.
- Any real .env file or deployment secret, which would be needed to resolve Q1
and Q3 with certainty.

## Final Consistency Statement

This report has been checked for consistency with the stakeholder's Phase 3
requirements. No recommendation in this final report proposes a
production-code change, and no recommendation carries a production-risk
priority label. The two Phase 2 recommendations that originally proposed
production-code changes (R1: remove/deprecate groq_service.py/chat_service.py;
R2: change email.py copy or config.py's reset-token default) have been
rewritten into documentation-only recommendations that preserve their
underlying evidence and onboarding relevance without touching application
code. All ten retained recommendations (R1 rewritten, R2 rewritten, R3–R9,
R11) are categorized as Documentation, and one (R10) is categorized as
Test-support; all priorities (High/Medium-High/Medium/Low) are expressed
strictly in terms of onboarding confusion and reproducibility impact,
consistent with the current audience and prioritization rule. No file was
created, modified, or removed at any point during this audit.
