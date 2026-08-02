# Backend Startup and Configuration Onboarding Patch Plan

This plan follows the active Project Memory decision (`decisions/decision-001.md`): follow-up is scoped to new-contributor onboarding documentation and
test-support only; production-code changes remain out of scope. Consistent with this audit's compact-plan format, exactly three recommendations are
prioritized below; additional valid findings are listed in the Excluded section rather than dropped.

## Scope and Evidence

Implementation/configuration evidence (read directly this session):

- `backend/app/config.py` — env-var loading/defaults, `validate_runtime_configuration()` (SQLite/production gating), `STORAGE_BACKEND`/S3 vars
- `backend/app/main.py` — CORS middleware wiring, security headers, `/health`, storage mount
- `backend/app/database/database.py` — engine created from `DATABASE_URL`
- `backend/app/storage.py` — local/S3 storage adapters
- `backend/.env.example` — 7 listed vars
- `backend/Procfile`, `render.yaml` — deploy start/build commands, production env var comments
- `backend/requirements.txt` vs `backend/requirements-local.txt` (supplementary, diffed) — confirms `requirements-local.txt` omits `groq`, `boto3`, `sentry-sdk`,
  `psycopg2-binary`, `pytest`

Focused-test evidence:

- `backend/tests/test_config_startup.py` (7 tests) — verifies optional-integration warning behavior, `CORS_ORIGINS` parsing, and production-mode validation
  (`DATABASE_URL` required, SQLite rejected unless `ALLOW_SQLITE_IN_PRODUCTION` set). This test exercises only these specific behaviors, not the full app.

Documentation claims reviewed:

- `README.md` — setup steps, "Environment Variables" table
- `docs/features/architecture.md` — env var table, DB/CORS/reset-token/Groq claims
- `docs/features/system_overview.md`, `docs/features/api_endpoints.md` (lines 270–329) — Groq model claim
- `docs/development/storage-backends.md` — storage backend reference (found internally consistent with `config.py`/`storage.py`; no correction proposed here)
- `CLAUDE.md` (already loaded via session context, not re-read as a separate file operation this turn)

Existing audit artifacts (treated as leads, re-verified against current files rather than cited as direct proof):

- `docs/agents/backend-config-docs-auditor/final-report.md`, `final-context-check.md` — prior facts (F1–F14) and recommendations (R1–R11); re-checked against this
  session's own reads of `config.py`, `main.py`, `.env.example`, `README.md`, `architecture.md`, `system_overview.md`, `api_endpoints.md`, and the requirements-file diff.
  All claims relied on below were independently re-confirmed.

Memory-derived current intent:

- `.memory/project/decisions/decision-001.md` — active decision restricting scope to onboarding documentation/test-support recommendations.

## Current Contributor Journey

1. Clone the repo, `cd backend`, create/activate a virtualenv (`README.md:42–51`). Clearly documented.
2. Run `pip install -r requirements.txt` (`README.md:53–56`). Not documented clearly — `backend/requirements-local.txt` sits alongside it in the same directory with
   a materially smaller dependency set, and README never mentions or disambiguates it.
3. `cp .env.example .env` and fill in 7 listed values (`README.md:58–61, 112–126`). Not documented clearly — the table calls `DATABASE_URL` a required "PostgreSQL
   connection string" without noting the working local SQLite default, and lists `FRONTEND_URL` as CORS-related when it is not.
4. Run `uvicorn app.main:app --reload` (`README.md:63–66`). Clearly documented and consistent with `Procfile`/`render.yaml` (which only differ in host/port for
   deployment).
5. Confirm the server at `http://localhost:8000/docs`. Not documented — a contributor must read `config.py`/`email.py` directly to learn that `DATABASE_URL`, `GMAIL_*`,
   `GROQ_API_KEY`, and `OPENWEATHER_API_KEY` are all optional for local startup, and that CORS is controlled solely by `CORS_ORIGINS`, not `FRONTEND_URL`.

## Prioritized Recommendations

### R7 — Clarify that DATABASE_URL defaults to local SQLite (Rank 1 of 3)

**Priority:** High

**Contributor symptom:** A new contributor reads the README, believes a real PostgreSQL connection string is mandatory, and stalls trying to provision a database
before attempting to run the backend at all.

**Current documentation claim:** `README.md:118` lists `DATABASE_URL` as "PostgreSQL connection string" under a section titled "The required variables are:"
(`README.md:114`), with no mention of a local default.

**Current implementation or focused-test evidence:**

- `backend/app/config.py:99-103` builds a default `sqlite:///.../fitgpt.db` URL whenever `DATABASE_URL` is unset or empty.
- `validate_runtime_configuration()` (`config.py:136-150`) only enforces a real `DATABASE_URL`/rejects SQLite when `ENVIRONMENT` is `prod`/`production`;
  `ALLOW_SQLITE_IN_PRODUCTION` is an explicit override.
- `backend/tests/test_config_startup.py:47-76` (3 tests) confirms this production-only gating for `DATABASE_URL` requirement and SQLite rejection/override — this
  test does not verify local/non-production behavior directly but confirms the gate is production-scoped.

**Exact target file and section:** `README.md`, "Environment Variables" table row for `DATABASE_URL` (`README.md:118`) plus one clarifying sentence near `README.md:114`.

**Proposed documentation change:**

```text
Create a `.env` file in the `backend/` folder. Use `backend/.env.example`
as the template. Only `SECRET_KEY` and `DATABASE_URL` matter for
production; the backend runs locally out of the box with a SQLite file
even if `.env` is empty or missing.

| Variable | Description |
|---|---|
| DATABASE_URL | DB connection string. Optional for local dev — defaults
  to a local SQLite file when unset. A non-SQLite PostgreSQL URL is
  required only when ENVIRONMENT=production (see backend/app/config.py). |
```

**Human validation step:** Ask a maintainer to confirm this wording doesn't conflict with any deploy-time documentation intent, and to verify the exact default
SQLite filename/path contributors should expect to see created.

**Confidence and limitations:** High confidence — verified directly in `config.py` and exercised by named tests. Whether Render's actual production environment
currently sets `ALLOW_SQLITE_IN_PRODUCTION` is not verifiable from committed evidence and is not claimed here.

---

### R9 — Document or disambiguate requirements-local.txt (Rank 2 of 3)

**Priority:** High

**Contributor symptom:** A contributor guessing between two similarly named files could install `requirements-local.txt` (its name reads as "the one for local
development") and then hit `ModuleNotFoundError` or a missing `pytest` when trying to run tests.

**Current documentation claim:** `README.md:53-56` instructs `pip install -r requirements.txt` and never mentions `requirements-local.txt`, which exists in the same
`backend/` directory.

**Current implementation or focused-test evidence:**

- A direct diff of `backend/requirements.txt` vs `backend/requirements-local.txt` (read this session) shows `requirements-local.txt` omits `groq`, `boto3`,
  `sentry-sdk[fastapi]`, `psycopg2-binary`, and `pytest`, and pins older `fastapi`/`pyjwt`/`python-multipart`/`python-dotenv` versions.
- `backend/Procfile:1` and `render.yaml:7` both reference only `requirements.txt` for install/start.

**Exact target file and section:** `README.md`, step 3 of "How to Run the Backend Locally" (`README.md:53-56`).

**Proposed documentation change:**

```text
3. Install dependencies:
   pip install -r requirements.txt
Note: use `requirements.txt`, not `requirements-local.txt`. The latter
omits packages the app needs at runtime and in tests (e.g. `groq`,
`boto3`, `sentry-sdk`, `psycopg2-binary`, `pytest`) and is not used by
CI, the Procfile, or render.yaml.
```

**Human validation step:** Ask a maintainer whether `requirements-local.txt` still serves an intended constrained-environment workflow or is stale; that answer
determines whether the final note should say "not used for standard setup" (as proposed) or recommend removal — the latter would be a repository change
outside this plan's scope.

**Confidence and limitations:** High confidence in the file contents and diff (directly inspected). No confidence claim is made about why `requirements-local.txt`
was created — that remains an open question for a maintainer.

---

### R4 — Correct README's FRONTEND_URL "used for CORS" claim (Rank 3 of 3)

**Priority:** High

**Contributor symptom:** While wiring up the local frontend and backend (a near-universal first task), a contributor hits a browser CORS error, edits `FRONTEND_URL`
per the README, sees no effect, and loses time before finding the actual mechanism.

**Current documentation claim:** `README.md:123` — `| FRONTEND_URL | URL of the frontend, used for CORS (e.g. http://localhost:3000) |`.

**Current implementation or focused-test evidence:**

- `backend/app/email.py:11,34,122` (referenced via grep this session) uses `FRONTEND_URL` only to build password-reset/verification links.
- CORS is governed entirely by `CORS_ORIGINS`/`DEFAULT_CORS_ORIGINS` (`config.py:88-94,115`), applied in `main.py:68-76`.
- `docs/features/architecture.md:127-128,189` already describes `FRONTEND_URL` correctly (reset-link builder) and lists `CORS_ORIGINS` separately — the mismatch is
  isolated to `README.md`.

**Exact target file and section:** `README.md`, "Environment Variables" table, `FRONTEND_URL` row (`README.md:123`); add a `CORS_ORIGINS` row, currently absent from this
table.

**Proposed documentation change:**

```text
| FRONTEND_URL | Base URL used to build password-reset/verification email
  links (backend/app/email.py). Does not affect CORS. |
| CORS_ORIGINS | Comma-separated list of additional allowed CORS origins.
  Defaults include http://localhost:3000, http://127.0.0.1:3000, and three
  deployed origins (see backend/app/config.py). |
```

**Human validation step:** Ask a maintainer to confirm the exact deployed origins that should be described in the README (vs. only summarizing "three deployed
origins") before publishing.

**Confidence and limitations:** High confidence — verified in `email.py`, `config.py`, and `main.py` directly, and cross-checked against `architecture.md`'s
already-correct wording. This does not verify that CORS behaves correctly in any live/deployed environment.

## Cross-File Consistency Check

- R7's fix targets `README.md` only; `architecture.md:14,183` already states "SQLite (default), PostgreSQL (via env var)" correctly, so no other file needs a
  matching edit.
- R4's fix targets `README.md` only; `architecture.md:127-189` already describes `FRONTEND_URL`/`CORS_ORIGINS` correctly, so this change brings README into alignment
  with an already-correct sibling doc rather than requiring multi-file coordination.
- R9's fix is README-only; `Procfile` and `render.yaml` already correctly reference `requirements.txt`, so no deploy-config change is implied.
- If `backend/.env.example` is ever updated to add a `CORS_ORIGINS` placeholder, the README table (R4) should be re-checked so the template and table stay in
  sync.
- None of these three recommendations require touching `CLAUDE.md`, `system_overview.md`, or `api_endpoints.md` — those files' inaccuracies (Groq model name) are
  tracked separately below and were not re-opened here.

## Excluded or Lower-Priority Findings

- Groq model name (`llama-3.1-8b-instant` claimed in `CLAUDE.md`, `architecture.md`, `system_overview.md`, `api_endpoints.md:303`, `README.md` vs. `config.py:129`'s
  configurable default `llama-3.3-70b-versatile`) — still verified present in all cited docs this session; excluded from the top 3 because it affects AI-feature
  exploration accuracy, not the ability to start/configure the backend.
- Incomplete env-var tables (`README.md`, `architecture.md:180-190` document far fewer than the ~27 vars read in `config.py`) — a real discoverability gap, but a
  contributor can still complete initial setup without it; ranked below the three chosen blocking/near-blocking issues.
- Legacy AI files note (`groq_service.py`/`chat_service.py` appear unused per grep, per prior audit) — relevant to AI-code navigation, not backend
  startup/configuration, the stated scope of this plan.
- Reset-token expiry wording (`architecture.md:128` says "1 hour"; `RESET_TOKEN_EXPIRE_MINUTES` defaults to 30 in `config.py:109`) and `google_id` migration claim
  (`architecture.md:119`, no such column in `models.py`) — both narrower-audience issues (password-reset QA, Google-auth investigation) with lower first-session
  frequency.
- CORS full-origin-list documentation, a CORS-defaults pinning test, and security-headers documentation — completeness items with no acute onboarding-blocking
  impact; still valid on re-check but lower priority than the three selected.

## Important Unverified Scope

- No backend process, test suite, or build was run in this session; all conclusions come from static reading of `config.py`, `main.py`, `database.py`, `storage.py`,
  and `test_config_startup.py`.
- No real `.env` file, Render dashboard configuration, or any live deployment was accessed.
- No live external integration (Groq, OpenWeatherMap, Gmail SMTP, Google OAuth, S3/R2) was exercised or confirmed working.
- The full backend/frontend/Android test suites and codebases were not reviewed; the "185+ backend tests" / "617 web tests" README claims are unverified here.
- Whether production actually overrides `RESET_TOKEN_EXPIRE_MINUTES` to 60 minutes, and whether `requirements-local.txt` serves an intentional workflow, remain
  open questions requiring maintainer input.
- Git history was not reviewed, so the origin/intent of the `architecture.md:119` `google_id` claim and of `requirements-local.txt` cannot be determined from this
  session's evidence.

No proposed change in this plan was performed. This session remained read-only; no repository file, test, configuration, or Git state was created, modified,
or removed.

> This file is a content-faithful reconstruction from the rendered PTY transcript. The raw PTY transcript is authoritative for disputed formatting details.
