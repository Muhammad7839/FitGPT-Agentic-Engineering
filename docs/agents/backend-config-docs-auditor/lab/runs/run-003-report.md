# Backend Startup and Configuration Onboarding Patch Plan

*(Read-only audit. No file was created, modified, or deleted. No command, test, build, or application code was executed. Applies the active onboarding-focused
Project Memory decision: `decisions/decision-001.md` — documentation/test-support recommendations only, no production-code changes.)*

## Scope and Evidence

Files directly read this session (all evidence below comes from files re-read in the current session, not carried over unverified from prior audit artifacts):

┌────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
│                                            File                                            │                        Evidence type                        │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ README.md                                                                                  │ Documentation claim (full file)                             │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/.env.example                                                                       │ Implementation/configuration evidence                       │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/Procfile                                                                           │ Implementation/configuration evidence                       │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ render.yaml                                                                                │ Implementation/configuration evidence                       │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/config.py                                                                      │ Implementation evidence (full file, all ~27 vars,           │
│                                                                                            │ validate_runtime_configuration)                             │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/main.py                                                                        │ Implementation evidence (CORS middleware, startup sequence) │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/database/database.py                                                           │ Implementation evidence                                     │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/storage.py                                                                     │ Implementation evidence                                     │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/tests/test_config_startup.py                                                       │ Focused-test evidence (7 tests; production-validation       │
│                                                                                            │ branches only)                                              │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/development/storage-backends.md                                                       │ Documentation claim (cross-checked against                  │
│                                                                                            │ storage.py/config.py; found internally accurate)            │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/features/architecture.md                                                              │ Documentation claim                                         │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/features/system_overview.md                                                           │ Documentation claim                                         │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/features/api_endpoints.md (relevant sections)                                         │ Documentation claim                                         │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/agents/backend-config-docs-auditor/final-report.md                                    │ Existing audit artifact (lead only, re-verified below, not  │
│                                                                                            │ trusted as-is)                                              │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ docs/agents/backend-config-docs-auditor/final-context-check.md                             │ Existing audit artifact (lead only)                         │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ .memory/project/decisions/decision-001.md                                                  │ Memory-derived current intent                               │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/requirements.txt, backend/requirements-local.txt                                   │ Implementation evidence (diffed)                            │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ .github/workflows/test.yml                                                                 │ Implementation/CI evidence                                  │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/email.py                                                                       │ Implementation evidence (FRONTEND_URL usage)                │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ backend/app/ai/provider.py, backend/app/chat_service.py, backend/app/groq_service.py,      │ Implementation evidence (verified directly this session,    │
│ backend/app/routes.py (import lines)                                                       │ not assumed from prior report)                              │
├────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ .gitignore, backend/.gitignore, ls backend/                                                │ Implementation evidence (confirmed no committed venv/)      │
└────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

Memory-derived current intent: Decision-001 (Active, review 2026-10-30) — audience is new contributors; only documentation and test-support recommendations
are permitted; production-code recommendations remain out of scope.

Note on prior audit artifacts: The prior `final-report.md` contains 11 recommendations (R1–R11) touching a broader surface (AI model naming, dead code,
reset-token wording, CORS origin count, security headers). I re-verified the subset that overlaps with "backend startup and configuration" directly against
current files rather than reusing its conclusions as-is (e.g., I independently confirmed `groq_service.py`/`chat_service.py` are unreferenced, and independently
found that `docs/features/architecture.md`'s env-var table is already correct on `DATABASE_URL` and `FRONTEND_URL`, which the prior report did not distinguish from
`README.md`'s incorrect claims). Findings outside strict startup/configuration scope, or already fully covered by the prior report without new evidence, are
listed under Excluded Findings rather than repeated here.

## Current Contributor Journey

Inferred from `README.md` "How to Run the Backend Locally" (lines 40–68) plus `backend/app/config.py`:

1. `cd backend`
2. `source venv/bin/activate` — not documented clearly: no prior step creates the virtual environment, and no `venv/` directory is committed (confirmed via
`.gitignore`/`backend/.gitignore` and directory listing). A first-time contributor on a fresh clone has no `venv/` to activate.

> This file is a content-faithful reconstruction from the rendered PTY transcript. The raw PTY transcript is authoritative for disputed formatting details.
