# Video Evidence Staging

Prepare these windows before recording. Do not record secrets, browser sessions with personal accounts, `.env` files, OAuth screens, cookies, or production dashboards.

## Windows to prepare

1. PowerPoint: `docs/capstone/submission/AURA_Forge_Final_Presentation.pptx`
2. Terminal at repository root.
3. Browser tab for verified submission-package CI run: `https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31520499134`
4. Optional editor tab: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`
5. Optional editor tab: `docs/capstone/governance-overreach-demo.md`

## Governance denial command

Run from repository root:

```bash
./scripts/capstone-demo.sh denial
```

Expected visible evidence:

- denial ID `GO-20260811-001`
- role `implementer`
- attempted tool `task_tracker`
- decision `DENIED`
- external state changed `No`
- model cost `$0`

Backup if terminal display fails: open `docs/capstone/governance-overreach-demo.md`.

## Route evidence command

Run:

```bash
./scripts/capstone-demo.sh routes
```

Expected visible evidence:

- `LOW` -> `aura-low-v1`
- `MEDIUM` -> `aura-medium-v1`
- `HIGH` -> `aura-high-v1`

Backup: open `docs/capstone/adaptive-routing.md`.

## Change Passport command

Run:

```bash
./scripts/capstone-demo.sh passport
```

Expected visible evidence:

- scenario `AF-HIGH-001`
- readiness `PASS`
- route `aura-high-v1`
- quality `16/16`
- policy tests `17 passed`
- human checkpoints `2`

Backup: open `docs/capstone/evidence/change-passport-AF-HIGH-001.json`.

## GitHub CI evidence

Open:

```text
https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31520499134
```

Show that the run is green and that the permanent gates are visible. Do not claim this run is the latest after later doc-only commits; call it the verified submission-package CI run.

Backup: open `docs/capstone/governance-ci-results.md`.

## Sensitive material to keep closed

- `backend/.env`
- any `.env` file
- browser account settings
- OAuth provider pages
- deployment dashboards
- API key consoles
- local credential folders
- ignored `.eval-artifacts` files unless already sanitized and intentionally opened

## If a live demo fails

Use the backup evidence file for that segment, state that the file is preserved evidence, and continue the recording. Do not improvise new claims.
