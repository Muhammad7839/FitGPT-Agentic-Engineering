# Backend Startup and Configuration Onboarding Patch Plan

## Scope and Evidence

Files reviewed this session (all read in full unless noted):

| File | Evidence type |
|---|---|
| `README.md` | Documentation claim |
| `CLAUDE.md` (provided in system context, re-checked against repo) | Documentation claim |
| `backend/.env.example` | Implementation/configuration evidence (template shipped with repo) |
| `backend/Procfile` | Implementation/configuration evidence |
| `render.yaml` | Implementation/configuration evidence — not listed in the prior audit's "Evidence Reviewed" section, so its content is new evidence this session, not a re-check of a prior claim |
| `backend/app/config.py` (lines 1–171, full file) | Implementation evidence |
| `backend/app/main.py` (lines 1–290, full file) | Implementation evidence |
| `backend/app/database/database.py` (full file) | Implementation evidence |
| `backend/app/storage.py` (full file) | Implementation evidence |
| `backend/tests/test_config_startup.py` (full file, 7 tests) | Focused-test evidence (covers only: optional-config warning collection, `GOOGLE_CLIENT_ID` fallback, `CORS_ORIGINS` list parsing, and three production-validation branches) |
| `docs/development/storage-backends.md` | Documentation claim |
| `docs/features/architecture.md` | Documentation claim |
| `docs/features/system_overview.md` | Documentation claim |
| `docs/features/api_endpoints.md` | Documentation claim |
| `docs/agents/backend-config-docs-auditor/final-report.md` | Existing audit artifact |
| `docs/agents/backend-config-docs-auditor/final-context-check.md` | Existing audit artifact |

Supplementary read-only spot-checks (file reads/greps only, no execution), done specifically to verify whether prior audit claims still hold rather than repeating them blindly:

- `backend/requirements.txt` vs `backend/requirements-local.txt` (diff) — confirms the two files still diverge materially.
- `.github/workflows/*.yml` (grep for requirements) — confirms CI still installs only `requirements.txt`.
- `backend/app/groq_service.py`, `backend/app/chat_service.py` existence + grep for references in `backend/app` and `backend/tests` — both files still exist, zero references found outside themselves.
- Grep for `llama-3.1-8b-instant`/model text across `README.md`, `CLAUDE.md`, `docs/features/*.md`.

Memory-derived current intent: Per active Project Memory entry `decisions/decision-001.md` (Status: Active, review by 2026-10-30, not yet due), this plan is scoped to new-contributor onboarding and reproducibility, restricted to documentation and test-support recommendations only, and explicitly excludes production-code change proposals regardless of what an earlier draft may have contained. `.memory/knowledge/agent-safety-and-evidence-standards.md` (same review window) governs the evidence hierarchy and read-only conduct applied throughout.

Inference vs verified fact discipline: Where a claim originates only from `final-report.md`/`final-context-check.md` and was not independently re-confirmed by a file I read this session (e.g., the exact wiring of `app/ai/service.py`/`app/ai/provider.py`, or `email.py`'s use of `FRONTEND_URL`), it is labeled below as carried-forward audit evidence, not re-verified this session, not as a fact I personally confirmed.

---

## Current Contributor Journey

Reconstructed strictly from `README.md` + implementation:

1. `cd backend`, activate venv, `pip install -r requirements.txt`, `cp .env.example .env`, `uvicorn app.main:app --reload`. **Not documented:** `backend/requirements-local.txt` exists alongside `requirements.txt` with a similar name and a materially smaller/older dependency set (confirmed missing `pytest`, `groq`, `boto3`, `sentry-sdk[fastapi]`, `psycopg2-binary`); nothing in `README.md` tells the contributor which file to use or why two exist.
2. Fill in `.env` values using `backend/.env.example`, which lists only 7 variables. **Not documented:** `backend/app/config.py` defines roughly 27 environment variables (e.g. `ENVIRONMENT`, `STORAGE_BACKEND` + `S3_*`, `AI_TIMEOUT_SECONDS`/`AI_MAX_TOKENS`/`AI_TEMPERATURE`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `SENTRY_DSN`, etc.); a contributor has no documented way to discover most of them exist.
3. `DATABASE_URL=your_postgresql_url_here` in `.env.example` reads as though a real Postgres URL is mandatory. **Not documented clearly:** `config.py` defaults `DATABASE_URL` to a local SQLite file when unset, and only enforces Postgres when `ENVIRONMENT` is `prod`/`production` (`validate_runtime_configuration`, directly read). `README.md`'s Tech Stack line ("SQLite for local development") and its Environment Variables table ("PostgreSQL connection string") state two different things about the same variable within the same document.
4. Start the server; if `GROQ_API_KEY`/`OPENWEATHER_API_KEY`/`GOOGLE_CLIENT_ID` are absent, the app starts anyway and logs fallback warnings (`config.py:153-170`, directly read) — this graceful-degradation behavior is not documented in `README.md` or `CLAUDE.md`.
5. To understand "how AI recommendations work," a contributor can find two complete Groq call sites: `groq_service.py`/`chat_service.py` (documented, still referencing `llama-3.1-8b-instant`) and an `app/ai/*` path (per carried-forward audit evidence, the one actually wired into `routes.py`). **Not documented:** which one is live, and that `GROQ_MODEL` (`config.py:129`) actually defaults to `llama-3.3-70b-versatile`, not `llama-3.1-8b-instant` as stated in 5 documents.
6. To verify the backend is "healthy," `docs/features/api_endpoints.md` documents only `GET /` and labels it "Health check." **Not documented:** `GET /health` (`main.py:266-284`) is a separate endpoint that actually probes the database and is the endpoint `render.yaml:9` configures as the deployment platform's real health check (`healthCheckPath: /health`).
7. Running `pytest tests/` per `README.md:130-138` assumes `requirements.txt` (which includes `pytest==9.0.3`) was installed — if the contributor installed `requirements-local.txt` instead in step 1, this step fails outright.

---

## Prioritized Recommendations

### R9 — Undocumented, divergent `backend/requirements-local.txt`

**Priority:** High

**Contributor symptom:** A contributor installs `backend/requirements-local.txt` instead of `requirements.txt` — a plausible guess, since it is literally named "local" and sits next to the file the README does reference — then runs `pytest tests/` per the README's own Testing section and gets `ModuleNotFoundError: No module named 'pytest'` (and later, `groq`/`boto3`/`sentry_sdk` errors if those code paths execute).

**Current documentation claim:** `README.md:53-56` instructs `pip install -r requirements.txt`. No document mentions `backend/requirements-local.txt` exists, what it's for, or that it differs from `requirements.txt`.

**Current implementation or focused-test evidence:** Directly re-verified this session via diff: `requirements-local.txt` omits `groq`, `boto3`, `sentry-sdk[fastapi]`, `psycopg2-binary`, and `pytest`, and pins older `fastapi==0.115.6`/`pyjwt==2.10.1`/`python-dotenv==1.0.1` versus `requirements.txt`'s `fastapi==0.124.4`/`pyjwt==2.12.0`/`python-dotenv==1.2.2`. `.github/workflows/*.yml` (`cache-dependency-path: backend/requirements.txt`, `pip install -r requirements.txt`) and `backend/Procfile:1` both use only `requirements.txt` — directly re-confirmed by grep this session. No focused test exercises which requirements file is "correct"; this is implementation/CI-config evidence only.

**Exact target file and section:** `README.md`, immediately after the code block in step 3 of "How to Run the Backend Locally" (`README.md:53-56`).

**Proposed documentation change:**

```markdown
3. Install dependencies:
   pip install -r requirements.txt

> **Note:** Use `requirements.txt`, not `backend/requirements-local.txt`.
> The `-local` file defines an older, smaller dependency set (it omits
> `pytest`, `groq`, `boto3`, and `sentry-sdk`, among others) and is not
> installed by CI (`.github/workflows/`) or used by the deployment start
> command (`Procfile`). Installing it instead will cause
> `pytest tests/` (see Testing section below) to fail with
> `ModuleNotFoundError: No module named 'pytest'`.
```

**Human validation step:** A maintainer should confirm the intended purpose of `requirements-local.txt` (still an open question from the prior audit — deliberately reduced dependency set for a constrained environment, or stale/abandoned file) before deciding whether the note above should also recommend removing the file. The proposed wording above is deliberately neutral and states only observed facts.

**Confidence and limitations:** High confidence in the file diff and CI behavior (both directly reproduced this session). Not verified: why `requirements-local.txt` exists in the first place, or whether any human workflow intentionally uses it outside CI/Procfile.

---

### R3 — Groq model name incorrect across five documents

**Priority:** High

**Contributor symptom:** A contributor reading any onboarding doc expects the backend to call `llama-3.1-8b-instant`. Cross-referencing docs against code (a common first-session activity) immediately surfaces a contradiction on a feature central to the product (AI recommendations/chat), which can undermine trust in the rest of the documentation.

**Current documentation claim:** "Groq API with Llama 3.1 8B" (`README.md:20`); `llama-3.1-8b-instant` appears 5 times in `CLAUDE.md` (lines 69–70, 127, 189, 252); twice in `docs/features/architecture.md` (lines 17, 122); twice in `docs/features/system_overview.md` (lines 94, 139); once in `docs/features/api_endpoints.md` (line 303) — 10 total occurrences across 5 documents, all directly re-confirmed by grep this session.

**Current implementation or focused-test evidence:** `backend/app/config.py:129`: `GROQ_MODEL = get_env("GROQ_MODEL", "llama-3.3-70b-versatile")` — directly read this session. No test in `test_config_startup.py` pins this specific default value, so this is implementation evidence only, not test-confirmed. Whether `groq_service.py`/`chat_service.py` (which still hardcode `llama-3.1-8b-instant`-era assumptions per the prior audit) are actually reachable from `routes.py` was not re-verified this session.

**Exact target file and section:** `README.md:20`; `CLAUDE.md:69-70,127,189,252`; `docs/features/architecture.md:17,122`; `docs/features/system_overview.md:94,139`; `docs/features/api_endpoints.md:303`.

**Proposed documentation change:** Replace "Llama 3.1 8B" / "llama-3.1-8b-instant" wording with, e.g.:

```markdown
Groq API (model configurable via `GROQ_MODEL`; defaults to
`llama-3.3-70b-versatile` — see backend/app/config.py:129)
```

For the `README.md:20` bullet specifically:

```markdown
- Groq API (model configurable via `GROQ_MODEL`, defaults to
  `llama-3.3-70b-versatile`) for the AURA AI chatbot
```

**Human validation step:** Confirm whether the deployed Render environment overrides `GROQ_MODEL` to a different value than the code default, so the documentation doesn't imply the default is necessarily what's live in production (Render's dashboard values are outside this repo's committed evidence).

**Confidence and limitations:** High confidence the code default is `llama-3.3-70b-versatile` (direct read of `config.py`). Not verified: which model the live production deployment actually invokes at runtime, or whether `groq_service.py`/`chat_service.py` are truly dead code (carried forward from the prior audit, not re-checked against `routes.py` this session).

---

### R4 — `FRONTEND_URL` documented as controlling CORS

**Priority:** High

**Contributor symptom:** Following `README.md`, a contributor sets `FRONTEND_URL` to their local frontend's origin expecting it to fix CORS, still sees browser CORS errors when wiring frontend to backend for the first time — a near-universal first integration task — and may spend real time debugging the wrong variable.

**Current documentation claim:** `README.md:91`: "...that `FRONTEND_URL` in your `.env` is set to the correct address" (in context of running frontend+backend together); `README.md:123` table row: "`FRONTEND_URL` | URL of the frontend, used for CORS (e.g. `http://localhost:3000`)".

**Current implementation or focused-test evidence:** `backend/app/config.py` (full 171-line file, directly read this session) defines `CORS_ORIGINS` (line 115, default list at lines 88–94) as the value passed into `CORSMiddleware` in `backend/app/main.py:68-76` (directly read this session). `FRONTEND_URL` does not appear anywhere in `config.py` — confirmed by reading the entire file; it is not part of the centralized config module at all. Its actual consumer (per carried-forward audit evidence, `email.py`'s password-reset link builder) was not re-read by me this session, so that specific attribution is not independently re-verified here — only the negative fact ("not in `config.py`, not part of the CORS mechanism") is directly confirmed.

**Exact target file and section:** `README.md:91` and the `FRONTEND_URL` row in the Environment Variables table (`README.md:123`).

**Proposed documentation change:**

```markdown
| FRONTEND_URL | Base URL used to build links in outgoing emails (e.g.
password reset). Does NOT control CORS. |
```

And for line 91:

```markdown
Make sure the backend is running locally first. CORS is controlled by the
backend's `CORS_ORIGINS` variable (defaults include `http://localhost:3000`
and `http://127.0.0.1:3000`); `FRONTEND_URL` only affects links sent in
outgoing emails.
```

**Human validation step:** Confirm the exact file(s) that read `FRONTEND_URL` (this session did not re-open `email.py`) before finalizing the "outgoing emails" wording, to avoid asserting a mechanism not directly re-checked this round.

**Confidence and limitations:** High confidence that `config.py` does not reference `FRONTEND_URL` and that `CORS_ORIGINS` is the actual CORS mechanism (both directly read). Medium confidence on "outgoing emails" being `FRONTEND_URL`'s sole consumer — that detail is carried forward from the prior audit's citation of `email.py`, not independently re-opened by me this session.

---

### R7 — `DATABASE_URL` presented as a required PostgreSQL string

**Priority:** High

**Contributor symptom:** A contributor believes a real PostgreSQL connection string is required before the backend can start locally, despite the committed SQLite default, and may waste time provisioning PostgreSQL or leave the placeholder in `.env` and get a connection error.

**Current documentation claim:** `backend/.env.example:1`: `DATABASE_URL=your_postgresql_url_here` (no comment indicating it's optional locally). `README.md:118` table row: "`DATABASE_URL` | PostgreSQL connection string |" — flatly, with no default mentioned. Notably, this directly conflicts with a different sentence in the same document, `README.md:18`: "PostgreSQL in production, SQLite for local development."

**Current implementation or focused-test evidence:** `backend/app/config.py:96-150` (directly read, full function): `DATABASE_URL` defaults to a local SQLite file (`_default_sqlite_url("fitgpt.db")`) whenever unset; `validate_runtime_configuration()` only requires a real, non-SQLite `DATABASE_URL` when `ENVIRONMENT` is `prod`/`production`, with an explicit `ALLOW_SQLITE_IN_PRODUCTION` override. `backend/tests/test_config_startup.py:47-76` (directly read, 3 focused tests) exercises exactly these three branches: production requires `DATABASE_URL`; production rejects SQLite; the override is respected. `render.yaml:13-15` (new evidence this session, not in the prior audit's file list) independently corroborates this as an operational comment: "Production mode: enforces `SECRET_KEY`, `DATABASE_URL`, and disallows SQLite unless overridden."

**Exact target file and section:** `README.md:118` (Environment Variables table row) and, as a lower-risk secondary target, an added comment line in `backend/.env.example` above line 1.

**Proposed documentation change:**

```markdown
| DATABASE_URL | PostgreSQL connection string. Optional for local development
— defaults to a local SQLite file (`backend/fitgpt.db`) when unset. Required
(non-SQLite) only when `ENVIRONMENT=production`, unless
`ALLOW_SQLITE_IN_PRODUCTION=true` is explicitly set. |
```

Optional `.env.example` comment (secondary target, template/comment only — no default value logic changes):

```dotenv
# Optional for local development: defaults to a local SQLite file
# (backend/fitgpt.db) when unset. Only required when ENVIRONMENT=production.
DATABASE_URL=your_postgresql_url_here
```

**Human validation step:** None beyond normal doc review — this recommendation is supported entirely by three files read in full this session (`config.py`, `test_config_startup.py`, `render.yaml`) plus an internal contradiction within `README.md` itself.

**Confidence and limitations:** High. Note: this only documents committed behavior; it does not verify what the actual Render dashboard's `DATABASE_URL` value or override state is at runtime.

---

### R12 — `GET /` mislabeled as "Health check"; real `GET /health` undocumented

**Priority:** Medium

**Contributor symptom:** A contributor curls `GET /` (per `docs/features/api_endpoints.md`, "Health check") and sees `{"message": "FitGPT backend is running"}`, incorrectly concluding the backend and its database connection are healthy — even if the database is actually unreachable, since `GET /` never touches the database. Separately, `render.yaml:9` configures `healthCheckPath: /health`, which no document explains or even mentions.

**Current documentation claim:** `docs/features/api_endpoints.md:403-416`, "## Root" section, labels `GET /` as "Health check" and shows only the static message response. `GET /health` does not appear anywhere in `api_endpoints.md`, `architecture.md`, or `system_overview.md` — confirmed absent by reading all three in full this session.

**Current implementation or focused-test evidence:** `backend/app/main.py:266-284` (directly read): `GET /health` executes `SELECT 1` against the DB via `engine.connect()`, returning `{"status": "degraded", "database": "unavailable"}` with HTTP 503 on failure, or `{"status": "ok", "database": "ok"}` on success. `backend/app/main.py:287-289` (directly read): `GET /` is a separate, unrelated endpoint returning only `{"message": "FitGPT backend is running"}` with no DB probe. `render.yaml:9` (directly read, new evidence this session): `healthCheckPath: /health` confirms `/health` — not `/` — is the endpoint the deployment platform actually relies on.

**Exact target file and section:** `docs/features/api_endpoints.md:403-416`, replace the "Root" section.

**Proposed documentation change:**

````markdown
## Root

### GET `/`

Basic liveness message (does not check the database).

**Auth required:** No

**Response:**

```json
{
  "message": "FitGPT backend is running"
}
```

### GET `/health`

Health check used by the deployment platform (`render.yaml`'s
`healthCheckPath`). Probes the database with `SELECT 1`.

**Auth required:** No

**Response (database reachable):**

```json
{
  "status": "ok",
  "database": "ok"
}
```

**Response (database unreachable, HTTP 503):**

```json
{
  "status": "degraded",
  "database": "unavailable"
}
```
````

**Human validation step:** None required beyond normal doc review — fully supported by three files read in full this session (`main.py`, `api_endpoints.md`, `render.yaml`).

**Confidence and limitations:** High confidence in the documented code behavior and the doc gap (all three source files read directly and in full). Not verified: whether Render's actual dashboard configuration still matches the committed `render.yaml` at deploy time.

---

## Cross-File Consistency Check

- **R3** touches five files (`README.md`, `CLAUDE.md`, `architecture.md`, `system_overview.md`, `api_endpoints.md`) that must all be updated together — leaving even one with `llama-3.1-8b-instant` would reintroduce the exact "which is right?" confusion this recommendation targets. Any future mention of the Groq model anywhere else in the docs set should also be checked against `config.py:129` before merge.
- **R4** must not contradict `CLAUDE.md`'s existing (separately flagged, lower-priority) CORS bullet, which already correctly does *not* mention `FRONTEND_URL` as a CORS mechanism — the README fix should align with, not duplicate or conflict with, that existing correct statement.
- **R7**'s README fix must remain consistent with `README.md:18`'s own Tech Stack line ("SQLite for local development"), which is already accurate — the goal is to make the Environment Variables table match the Tech Stack section of the *same document*, and also to remain consistent with `docs/features/architecture.md:14` ("SQLite (default), PostgreSQL (via env var)"), which is already correct and should not be re-edited.
- **R9** is self-contained to `README.md`; no other reviewed document references `requirements-local.txt`, so no cross-file follow-up is required.
- **R12** is scoped to `api_endpoints.md`; if `architecture.md` or `system_overview.md` are later updated to mention deployment/health-check behavior, they should cite the same `/health` response shape defined here to avoid a second inconsistency.

---

## Excluded or Lower-Priority Findings

From the prior audit's still-valid, re-confirmed set (not re-litigated in full here, per the active decision to avoid duplicating completed audit work without checking currency — each was spot-checked this session where noted):

- **R1** (document that `groq_service.py`/`chat_service.py` are not the live AI path) — still plausible per this session's grep (zero references to either file found in `backend/app`/`backend/tests`), but the specific claim that `app/ai/service.py`/`app/ai/provider.py` is the *actual* live path was not re-opened by me this session (out of this task's file list); ranked below the five above because its evidence chain is partially carried-forward rather than fully re-verified this round.
- **R2** (reset-token "1 hour" vs 30-minute default mismatch) — not re-checked this session (`email.py`, `crud.py` not in this task's file list); still an open question per the prior audit (Q1).
- **R5** (`google_id`/`auth_provider` "automatic migration" claim in `architecture.md:119`) — **partially re-verified this session**: `main.py:137-231` (`_ensure_runtime_schema`, read in full) adds many columns but none named `google_id` or `auth_provider`, consistent with the prior finding. Ranked below the top five because it affects a narrower audience (contributors specifically investigating Google sign-in/schema history).
- **R6** (expand env-var tables to cover ~18 undocumented variables) — still valid per this session's full read of `config.py`; not selected among the five only because R7 and R3 already correct the two highest-impact rows, and a full table rewrite is a larger, lower-urgency documentation task.
- **R8** (document full `DEFAULT_CORS_ORIGINS` list, not just two localhost origins) — re-confirmed this session via `config.py:88-94` and `CLAUDE.md`'s single-line CORS bullet; lower priority since it affects preview/deployed-origin testing, not core local onboarding.
- **R10** (add a focused test pinning `DEFAULT_CORS_ORIGINS`) — legitimate test-support work, but lower priority than the immediate documentation corrections; the current focused test already covers parsing an explicit CORS list, not the default list content.
- **R11** (document security-headers middleware) — re-confirmed present in `main.py:79-96` (directly read this session); low urgency, doesn't block any onboarding task.
- **New, minor observation (not promoted to a numbered recommendation):** `render.yaml:8` hardcodes `startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000`, while `backend/Procfile:1` uses a dynamic `--port ${PORT:-8000}`. No document explains that Render uses `render.yaml`'s command (ignoring `Procfile`) or why the two differ. Not selected due to the cap; lower onboarding impact since it only affects deployment-command reasoning, not local setup.
- **New, minor observation:** `render.yaml:11` pins `PYTHON_VERSION: 3.10.13`; no reviewed document states a required/tested Python version for local setup. Lower priority — a missing "nice to have," not a reproducibility blocker on its own.

---

## Important Unverified Scope

This read-only documentation audit does **not** verify:

- That the complete FastAPI backend, beyond the configuration/startup/storage/health surface examined (`config.py`, `main.py`, `database.py`, `storage.py`, and the `/health`/`/` routes), behaves as documented elsewhere (`routes`, auth, recommendations logic, `app/ai/*`, `groq_service.py`, `chat_service.py` were not re-opened this session).
- Any live deployment: whether the actual Render service currently matches committed `render.yaml`, what environment variables are truly set in the Render dashboard, or whether the live app responds as `main.py` implies.
- Any external integration (Groq API, OpenWeatherMap, Gmail SMTP, Google OAuth, S3/R2) beyond which environment variables and code paths would invoke them.
- The frontend (`web/`) or Android (`app/`) codebases, or whether `README.md`'s "185+ backend tests"/"617 web tests" figures are currently accurate (still open per the prior audit's Q5; not independently re-counted here since running the suites was out of scope for this read-only task).
- Git history/authorship — relevant to unresolved prior questions (e.g., whether `google_id`/`auth_provider` migrations ever existed) that remain open.
- Whether `backend/requirements-local.txt` is intentional legacy tooling or an abandoned file (open item underlying R9).

No repository file, memory file, or Git state was created, modified, or removed at any point during this session. No proposed change above has been applied.

> This file is a content-faithful reconstruction from the rendered PTY transcript. The raw PTY transcript is authoritative for disputed formatting details.
