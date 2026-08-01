# Backend Startup and Configuration Onboarding Patch Plan

## Scope and Evidence

Implementation or configuration evidence (read directly, this session):

- `backend/app/config.py` (full file, lines 1–171) — env-var loading, defaults, `DATABASE_URL`/`_normalize_database_url()` logic, `validate_runtime_configuration()`, `CORS_ORIGINS`/`DEFAULT_CORS_ORIGINS`, `collect_optional_config_warnings()`
- `backend/app/main.py` (full file, lines 1–290) — CORS middleware wiring, `/health` and `/` endpoints, schema-migration helper, static uploads mount
- `backend/app/database/database.py` (full file, lines 1–27) — engine creation from `DATABASE_URL`
- `backend/app/storage.py` (full file, lines 1–87) — `LocalStorage`/`S3Storage` adapters
- `backend/tests/test_config_startup.py` (full file, lines 1–76) — 7 focused tests covering optional-config warnings, `CORS_ORIGINS` parsing helper, and production `DATABASE_URL`/SQLite enforcement
- `backend/.env.example` (7 lines)
- `backend/Procfile` (1 line)
- `render.yaml` (full file)
- `backend/requirements.txt` and `backend/requirements-local.txt` (read this session to verify a prior-audit claim directly rather than trust it secondhand)
- `.github/workflows/test.yml` (read this session for the same reason)
- Targeted Grep of `FRONTEND_URL` across `backend/` → confirmed it is read only in `backend/app/email.py:11,34,122`, not in `config.py`
- Targeted Grep of `postgres` (case-insensitive) across `backend/` → confirmed no `postgres://`→`postgresql://` rewrite exists anywhere in the backend

Focused-test evidence: `backend/tests/test_config_startup.py` verifies only: optional-integration warning strings, `get_list_env` parsing behavior, and that `validate_runtime_configuration()` raises when `ENVIRONMENT` is production with no `DATABASE_URL` or with an un-overridden SQLite URL. It does not exercise CORS behavior, storage backends, or email/reset-token logic.

Documentation claims (compared, not trusted): `README.md` (full file), `CLAUDE.md` (Backend Notes and repo-structure sections, already in context and re-checked with Grep for exact line numbers), `docs/features/architecture.md` (full file), `docs/features/system_overview.md` (full file), `docs/features/api_endpoints.md` (full file), `docs/development/storage-backends.md` (full file).

Existing audit artifacts (treated as leads only, not sufficient evidence): `docs/agents/backend-config-docs-auditor/final-report.md` and `final-context-check.md`. Several of their factual claims (e.g., `groq_service.py`/`chat_service.py` being dead code, `RESET_TOKEN_EXPIRE_MINUTES` enforcement in `crud.py`) depend on files (`app/routes.py`, `app/crud.py`, `app/groq_service.py`, `app/chat_service.py`, `app/email.py` in full) that were not in this session's reviewed-file list and were not independently re-read in full this session. Those claims are therefore excluded from the final recommendations below rather than repeated as verified fact.

Memory-derived current intent: Project Memory `decision-001.md` (Active, review 2026-10-30) restricts this follow-up to onboarding-documentation and test-support recommendations, prioritized by onboarding confusion/reproducibility impact, with production-code changes out of scope. This plan complies with that decision.

## Current Contributor Journey

Inferred from `README.md`'s "How to Run the Backend Locally" section and cross-checked against `config.py`/`main.py`:

1. `cd backend`, activate a virtualenv, run `pip install -r requirements.txt` (`README.md:53–56`). Not clearly documented: a second file, `backend/requirements-local.txt`, sits alongside `requirements.txt` and is never mentioned in the README, so a contributor has no documented reason to prefer one over the other.
2. `cp .env.example .env` and "fill in your values" (`README.md:58–61`), guided by a table (`README.md:112–126`) that labels all 7 listed variables as "required." Not clearly documented: `config.py` gives working local defaults for `DATABASE_URL` (SQLite file), `SECRET_KEY`, `OPENWEATHER_API_KEY`, and `GROQ_API_KEY` (with logged warnings, not failures — `config.py:153–161`), and only enforces `SECRET_KEY`/`DATABASE_URL` strictly when `ENVIRONMENT` is `prod`/`production` (`config.py:136–150`, confirmed by `test_config_startup.py:47–76`).
3. `uvicorn app.main:app --reload` (`README.md:65`). No `.env` is strictly required for this step to succeed locally.
4. Contributor connects the frontend and may hit a CORS error. `README.md:123` tells them `FRONTEND_URL` is "used for CORS." Not clearly documented: `FRONTEND_URL` is read only in `email.py:11,34,122` for reset/verification links; CORS is governed entirely by `CORS_ORIGINS`/`DEFAULT_CORS_ORIGINS` (`config.py:88–94,115`) applied in `main.py:68–76`.
5. If the contributor later configures a real PostgreSQL `DATABASE_URL` from a hosting provider's classic `postgres://`-style connection string, `CLAUDE.md:181` claims the backend "auto-converts `postgres://` → `postgresql://`." Not supported by the code reviewed this session: `_normalize_database_url()` (`config.py:74–85`) only rewrites relative `sqlite:///` paths; there is no `postgres://` rewrite anywhere in `backend/`.

## Prioritized Recommendations

### R1 — Clarify that `DATABASE_URL` has a working local SQLite default

**Priority:** High — Rank 1 of 5

**Contributor symptom:** Following `README.md`'s setup steps, a new contributor believes a real PostgreSQL connection string must be obtained and set before the backend will run at all, and may stall the very first setup milestone acquiring/configuring a database that isn't required for local development.

**Current documentation claim:** `README.md:114–124` states "The required variables are:" and lists `DATABASE_URL | PostgreSQL connection string` with no mention of a default or of when it is actually enforced.

**Current implementation or focused-test evidence:** `config.py:96–103` — `DATABASE_URL` defaults to `_default_sqlite_url("fitgpt.db")` when `DATABASE_URL` is unset or `FITGPT_LOCAL_BACKEND` forces local mode. `config.py:136–150` (`validate_runtime_configuration`) only raises when `ENVIRONMENT` is `prod`/`production`. This is directly exercised by `test_config_startup.py:47–65` (raises without `DATABASE_URL` or with SQLite, only when `ENVIRONMENT=production`) and `test_config_startup.py:68–75` (passes when `ALLOW_SQLITE_IN_PRODUCTION` is set).

**Exact target file and section:** `README.md`, "Environment Variables" section, the `DATABASE_URL` table row (line 118) and the introductory sentence (line 114).

**Proposed documentation change:**

- Replace line 114 with: Create a `.env` file in the `backend/` folder using `backend/.env.example` as a template. For local development, the backend runs with working defaults for every variable below except `SECRET_KEY`, which should still be set to any non-empty value. The variables below become strictly required only when `ENVIRONMENT` is set to production.
- Replace the `DATABASE_URL` row (line 118) with: `| DATABASE_URL | PostgreSQL connection string. Optional for local development — if unset, the backend uses a local SQLite file (backend/fitgpt.db) automatically. Required only when ENVIRONMENT=production (see backend/app/config.py). |`

**Human validation step:** A maintainer should confirm the proposed row/sentence against the current `backend/app/config.py:96–150` and `backend/tests/test_config_startup.py:47–76` to ensure no newer commit has changed the default-SQLite or production-enforcement behavior. This is a static check (read the two files side by side with the proposed text); it does not require running the backend. Not executed in this audit: actually starting `uvicorn` with no `.env` present to observe the real startup log output.

**Confidence and limitations:** High confidence — both the default-SQLite path and the production-only enforcement are shown directly in `config.py` and independently exercised by three passing-by-inspection assertions in `test_config_startup.py`. Limitation: this audit did not execute `pytest` or `uvicorn`, so it confirms the code path exists and is tested, not that it behaves identically in every contributor's local Python/OS environment.

---

### R2 — Correct `CLAUDE.md`'s unsupported "auto-converts `postgres://` → `postgresql://`" claim

**Priority:** High — Rank 2 of 5

**Contributor symptom:** A contributor who pastes a `postgres://`-style connection string (the scheme commonly issued by several hosting providers) into `DATABASE_URL`, trusting `CLAUDE.md`'s claim that it is auto-converted, would have no documented reason to suspect the scheme itself if the backend fails to start against that database.

**Current documentation claim:** `CLAUDE.md:181` — "Database: SQLite default (fitgpt.db), PostgreSQL via DATABASE_URL env var (auto-converts postgres:// → postgresql://)."

**Current implementation or focused-test evidence:** `config.py:74–85` (`_normalize_database_url`) only rewrites relative `sqlite:///` paths to absolute ones; it returns any non-`sqlite:///` string unchanged. A repository-wide case-insensitive search for "postgres" in `backend/` (this session) found no scheme-rewriting logic anywhere — only comparison strings (`config.py:146`), a docstring (`main.py:138`), and a dialect-name check (`main.py:142`).

**Proposed documentation change:** Replace line 181 with: `- Database: SQLite default (fitgpt.db, resolved to an absolute path under backend/), PostgreSQL via DATABASE_URL env var. backend/app/config.py's _normalize_database_url() only adjusts relative sqlite:/// paths — it does not rewrite a postgres:// scheme to postgresql://. Use the exact connection string scheme your database provider gives you, or convert it to postgresql:// yourself if your installed SQLAlchemy/driver version requires that scheme (not verified in this audit — confirm with your local environment).`

**Human validation step:** Static check: re-read `backend/app/config.py:74–85` and grep the backend tree for `postgres` to confirm no conversion was added since this audit. A maintainer who wants to know whether a bare `postgres://` URL actually fails would need to run `uvicorn` (or the test suite) locally with such a URL set — this is runtime verification and was explicitly not performed here.

**Confidence and limitations:** High confidence that the claimed conversion code does not exist (directly read + grepped). Lower confidence on the exact failure mode/message a contributor would see, since that depends on the installed SQLAlchemy/psycopg2 version in their environment — the proposed wording is phrased conditionally for that reason rather than asserting a specific error.

---

> This file is a content-faithful reconstruction from the rendered PTY transcript. The raw PTY transcript is authoritative for disputed formatting details.
