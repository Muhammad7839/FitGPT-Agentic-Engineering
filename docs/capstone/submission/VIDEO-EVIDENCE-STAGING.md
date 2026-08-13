# Video Evidence Staging

Prepare these windows before recording. Do not record secrets, browser sessions with personal accounts, `.env` files, OAuth screens, cookies, production dashboards, API key consoles, or local credential folders.

## Windows to Prepare

1. Final Gamma PDF: `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`
2. Terminal at the repository root.
3. Browser tab for verified CI run: `https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31531270032`
4. Optional editor tab: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`
5. Optional editor tab: `docs/capstone/governance-overreach-demo.md`

## Slide 7 Governance Denial

Run from the repository root:

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

## Slide 8 GitHub CI Evidence

Open:

```text
https://github.com/Muhammad7839/FitGPT-Agentic-Engineering/actions/runs/31531270032
```

Show that the run is green and that the permanent gates are visible. Use this as the stable demonstrated pre-submission CI evidence for the recording. Do not edit the Gamma deck just to include any later doc-only freeze run ID.

Backup: open `docs/capstone/governance-ci-results.md`.

## Slide 9 Change Passport

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

## Sensitive Material to Keep Closed

- `backend/.env`
- any `.env` file
- browser account settings
- OAuth provider pages
- deployment dashboards
- API key consoles
- local credential folders
- ignored `.eval-artifacts` files unless already sanitized and intentionally opened

## If a Live Demo Fails

Use the backup evidence file for that segment, state that the file is preserved evidence, and continue the recording. Do not improvise new claims.
