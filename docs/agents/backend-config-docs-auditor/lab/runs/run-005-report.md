# Backend Startup and Configuration Onboarding Patch Plan

## Scope and Evidence

Implementation/configuration evidence (read directly this session): `backend/app/config.py` (full, 171 lines), `backend/app/main.py` (full, 290 lines),
`backend/app/database/database.py` (full, 28 lines), `backend/app/storage.py` (full, 87 lines), `backend/.env.example` (full), `backend/Procfile` (full), `render.yaml`
(full).

Focused-test evidence (read directly): `backend/tests/test_config_startup.py` (full, 76 lines, 7 tests).

Documentation claims (read directly): `README.md` (full), `docs/features/architecture.md` (full), `docs/features/system_overview.md` (full),
`docs/features/api_endpoints.md` (full), `docs/development/storage-backends.md` (full). `CLAUDE.md` was supplied via prior session context and confirmed unchanged
on disk when a read was attempted this session (the tool reported no repository change since context was loaded); its content is treated as current but was
not freshly re-read line-by-line via a new Read call.

Existing audit artifacts (read directly, treated as leads, not as direct implementation support): `docs/agents/backend-config-docs-auditor/final-report.md`,
`docs/agents/backend-config-docs-auditor/final-context-check.md`.

Memory-derived current intent (session context, not a repository file): `.memory/project/decisions/decision-001.md`, loaded at session start — restricts this
plan to onboarding-audience, documentation/test-support recommendations only, no production-code changes.

No supplementary files beyond the user-named list were read this session (e.g., `backend/app/routes.py`, `backend/app/email.py`, `backend/app/groq_service.py`,
`backend/requirements.txt`, `backend/requirements-local.txt` were not opened here); findings depending on those are marked accordingly below.

## Current Contributor Journey

1. Clone the repo and run `cd backend` — documented clearly in `README.md`.
2. Activate a virtualenv (`source venv/bin/activate`) — unclear: README never documents creating the venv (e.g., `python -m venv venv`); a fresh clone has no
   `venv/` directory.
3. `pip install -r requirements.txt` — documented in README; whether a second requirements file affects this step was not checked this session.
4. `cp .env.example .env` and "fill in your values" for all 7 template variables — unclear: `.env.example` presents `DATABASE_URL=your_postgresql_url_here` as if a
   real Postgres string is mandatory, but `config.py` (read this session) shows a working SQLite default and non-production defaults for most vars.
5. `uvicorn app.main:app --reload` — documented and consistent with Procfile/render.yaml command patterns.

## Prioritized Recommendations

### R1 — Clarify that DATABASE_URL has a working local SQLite default; PostgreSQL is required only in production

**Rank:** 1 of 3

**Priority:** High

**Contributor symptom:** A new contributor may believe they must obtain a real PostgreSQL connection string before the backend will run at all, stalling their
first local setup attempt.

**Current documentation claim:** README.md's Environment Variables table (lines ~112–126) lists `DATABASE_URL` as "PostgreSQL connection string" with no mention of
a default; `backend/.env.example` line 1 shows `DATABASE_URL=your_postgresql_url_here`, implying a real value is required.

**Current implementation or focused-test evidence:**

- `backend/app/config.py` lines 96–103: `DATABASE_URL` falls back to a local `sqlite:///.../fitgpt.db` path when unset.
- `backend/app/config.py` lines 136–150 (`validate_runtime_configuration`): strict `DATABASE_URL`/SQLite rules apply only when `ENVIRONMENT` is prod/production.
- `backend/tests/test_config_startup.py` lines 47–76: three tests directly exercise this behavior (requires `DATABASE_URL` in production, rejects SQLite in
  production, allows SQLite via `ALLOW_SQLITE_IN_PRODUCTION` override).
- `render.yaml` lines 13–18: confirms `ENVIRONMENT=production` is what triggers the strict enforcement in deployment, separate from local defaults.

**Exact target file and section:** `README.md` → "Environment Variables" table and the `DATABASE_URL=your_postgresql_url_here` line in `backend/.env.example`.

**Proposed documentation change:**

```text
| DATABASE_URL | PostgreSQL connection string. Optional for local
  development — defaults to a local SQLite file
  (backend/fitgpt.db) when unset. Required only when
  ENVIRONMENT=production (see backend/app/config.py). |
```

In `.env.example`, add a comment above the line:

```text
# Optional locally — leave blank to use SQLite (backend/fitgpt.db).
# Required when ENVIRONMENT=production.
DATABASE_URL=your_postgresql_url_here
```

**Human validation step:** Compare the updated README wording and `.env.example` comment against `backend/app/config.py` lines 96–103 and 136–150, and against
`test_config_startup.py` lines 47–76. Passing condition: the documented behavior matches the default/production logic exactly. Failing condition: any wording
implying `DATABASE_URL` is mandatory outside production.

**Confidence and limitations:** High confidence — directly triangulated across the explanatory doc, the committed template, the implementation, and a focused test
read in this session. Does not verify actual local startup success (no command was executed).

---

### R2 — Correct the hardcoded Groq model name across documentation

**Rank:** 2 of 3

**Priority:** High

**Contributor symptom:** A contributor cross-referencing docs against code for the AI recommendation/chat feature encounters a repeated, specific model name that
does not match configuration, undermining trust in the rest of the documentation.

**Current documentation claim:** `CLAUDE.md` ("Groq API (llama-3.1-8b-instant)"), `README.md` ("Groq API with Llama 3.1 8B"), `docs/features/architecture.md` line 17
and line 122, `docs/features/system_overview.md` lines 94 and 139, and `docs/features/api_endpoints.md` line 303 all state the model is `llama-3.1-8b-instant`.

**Current implementation or focused-test evidence:** `backend/app/config.py` line 129: `GROQ_MODEL = get_env("GROQ_MODEL", "llama-3.3-70b-versatile")` — configurable
via env var, with a different default than every document states. No test in `test_config_startup.py` asserts this specific default value.

**Exact target file and section:** All five listed documents, wherever `llama-3.1-8b-instant` appears.

**Proposed documentation change:**

```text
AI Recommendations: Groq API, model configurable via GROQ_MODEL
(backend/app/config.py), defaulting to llama-3.3-70b-versatile.
```

**Human validation step:** Grep each listed document for `llama-3.1-8b-instant` after the edit and confirm zero remaining matches; re-open `backend/app/config.py`
line 129 to confirm the default string still matches the new wording. Failing condition: any remaining hardcoded model name in the five files.

**Confidence and limitations:** High confidence for the config default itself (read directly, single source of truth). This recommendation covers only the
documented model name — it does not confirm which code path (e.g., `groq_service.py` vs. an AI service layer) is actually invoked at runtime, since those files
were not opened in this session.

---

### R3 — Correct README.md's claim that FRONTEND_URL is "used for CORS"

**Rank:** 3 of 3

**Priority:** High

**Contributor symptom:** While integrating the local frontend and backend for the first time, a contributor sees a CORS error, edits `FRONTEND_URL` per the README
table, observes no effect, and loses time before finding the actual mechanism.

**Current documentation claim:** `README.md`'s Environment Variables table (row for `FRONTEND_URL`) states it is "used for CORS."

**Current implementation or focused-test evidence:** `backend/app/main.py` lines 68–76 configure `CORSMiddleware` with `allow_origins=CORS_ORIGINS`;
`backend/app/config.py` lines 88–94 and 115 define `DEFAULT_CORS_ORIGINS` and `CORS_ORIGINS` as the only inputs to this middleware. Neither `config.py` nor `main.py`,
as read this session, references `FRONTEND_URL` anywhere.

**Exact target file and section:** `README.md` → "Environment Variables" table, `FRONTEND_URL` row.

**Proposed documentation change:**

```text
| FRONTEND_URL | Base URL used for links generated by the backend
  (e.g., password-reset emails); does not affect CORS. |
| CORS_ORIGINS | Comma-separated list of additional allowed origins.
  CORS is controlled entirely by this variable and its built-in
  defaults (see backend/app/config.py). |
```

**Human validation step:** Re-check `backend/app/main.py` lines 68–76 and `backend/app/config.py` lines 88–94/115 against the revised wording; confirm no other doc
(e.g., `docs/features/architecture.md`, which already describes CORS via `CORS_ORIGINS` only) is contradicted. Failing condition: any remaining text implying
`FRONTEND_URL` affects CORS behavior.

**Confidence and limitations:** High confidence that CORS is governed solely by `CORS_ORIGINS`/`DEFAULT_CORS_ORIGINS` (directly read this session in both `config.py`
and `main.py`). What `FRONTEND_URL` is actually used for was not independently verified this session (`backend/app/email.py` was not opened); the proposed wording
is conditional on that file matching the prior audit's description and should be confirmed before merging.

## Cross-File Consistency Check

- The GROQ model correction (R2) must be applied identically in all five documents; leaving even one stale copy re-creates the same cross-referencing
  confusion.
- The `DATABASE_URL` wording (R1) must stay consistent between `README.md`'s table and `backend/.env.example`'s inline comment, and must not contradict
  `render.yaml`'s existing "Production mode: enforces SECRET_KEY, DATABASE_URL..." comment or `CLAUDE.md`'s existing "SQLite default... PostgreSQL via DATABASE_URL"
  phrasing, which is already closer to accurate.
- The `FRONTEND_URL`/CORS correction (R3) must not contradict `docs/features/architecture.md`'s existing environment-variable table, which already lists
  `CORS_ORIGINS` and `FRONTEND_URL` as separate rows without claiming `FRONTEND_URL` affects CORS — `README.md` should be brought into line with that existing framing,
  not the reverse.

## Excluded or Lower-Priority Findings

- `CLAUDE.md` states `DATABASE_URL` "auto-converts postgres:// → postgresql://"; no such conversion logic was found in the full
  `_normalize_database_url`/`DATABASE_URL` definitions read this session (only `sqlite:///` paths are rewritten). This is a plausible new mismatch but affects a
  narrower group (contributors supplying a `postgres://`-prefixed URL) and was not cross-checked against any test; ranked below R1–R3 pending confirmation.
- The prior audit's R9 (`backend/requirements-local.txt` vs. `requirements.txt` divergence) is described as high-impact in `final-report.md`, but neither
  requirements file was opened in this session; it is carried forward as an unverified lead, not restated as a confirmed recommendation here.
- Prior audit items on the `groq_service.py`/`chat_service.py` "dead code" note, the `google_id`/`auth_provider` migration claim, the expanded environment-variable
  table, the full CORS-origin list, a CORS-pinning test, and security-headers documentation all depend on files not named or read in this session (`routes.py`,
  `models.py`, `email.py`, `test_security_headers.py`) and are excluded from this compact plan pending re-verification.
- The reset-token "1 hour" vs. 30-minute default discrepancy (prior R2) depends on `email.py` wording, not reviewed this session; excluded pending re-check.

## Important Unverified Scope

- Whether the backend actually starts successfully end-to-end for a new contributor was not tested; no command, build, or test was executed in this session.
- Whether `groq_service.py`/`chat_service.py` are live or unused code paths was not independently re-confirmed this session.
- Whether `backend/requirements-local.txt` still diverges from `requirements.txt`, and which file CI/Procfile actually use, was not verified this session.
- Live external integrations (Groq API, OpenWeatherMap, Gmail SMTP, Google OAuth, S3/R2) were not contacted or tested.
- Actual deployed Render/Vercel environment variable values are inaccessible and were not verified.
- The frontend (`web/`) and Android (`app/`) codebases were not reviewed in this session.

No proposed change in this plan was performed. All findings are read-only recommendations; no repository file, test, configuration, or Git state was modified
during this session.

> This file is a content-faithful reconstruction from the rendered PTY transcript. The raw PTY transcript is authoritative for disputed formatting details.
