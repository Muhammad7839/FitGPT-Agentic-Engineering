# AURA Forge — Governed Adaptive Engineering for FitGPT

This is the isolated LaunchCode Agentic Engineering course repository for FitGPT. The original completed FitGPT senior-project repository remains protected and separate at `https://github.com/Muhammad7839/FitGPT.git`.

AURA Forge is an engineering-governance system around FitGPT, not another consumer feature. It decides how much autonomy a software change deserves, routes the change through bounded agents and deterministic gates, and leaves machine-readable evidence for review.

Thesis:

> AURA Forge does not ask how many AI agents can automate a software change. It determines how much autonomy a change actually deserves, then proves that the selected agents stayed within policy, the change passed evaluation, and every important decision is traceable to machine-generated evidence.

## Architecture

```text
Change
  -> deterministic risk classifier
  -> adaptive route
  -> bounded agents/tools
  -> deterministic/evaluation gates
  -> human approval where required
  -> Change Passport/audit evidence
```

Key evidence:

- Grader quickstart: `docs/capstone/GRADER-QUICKSTART.md`
- Evidence index: `docs/capstone/evidence-index.md`
- Final rubric audit: `docs/capstone/final-rubric-audit.md`
- Stakeholder one-pager: `docs/capstone/stakeholder-one-pager.md`
- Reproducibility runbook: `docs/capstone/reproducibility-runbook.md`
- Architecture diagrams: `docs/capstone/final-architecture.md`
- Change Passport example: `docs/capstone/evidence/change-passport-AF-HIGH-001.json`
- Real GitHub CI evidence: `docs/capstone/governance-ci-results.md`
- ADR evidence matrix: `docs/capstone/adr-evidence-matrix.md`
- Final presentation: `docs/capstone/submission/AURA_Forge_Final_Gamma_Presentation.pdf`
- Final walkthrough video: https://youtu.be/WxEXCWC75vs

## Measured Impact

Measured across three representative capstone scenarios only:

| Scenario | PRE-AURA quality | AURA quality | Cost change | Model-role change | Human-checkpoint change |
|---|---:|---:|---:|---:|---:|
| LOW | `14/16 FAIL` | `16/16 PASS` | `-44.32%` | `-60%` | `-100%` |
| MEDIUM | `15/16 PASS` | `16/16 PASS` | `-19.71%` | `-40%` | `-50%` |
| HIGH | `15/16 PASS` | `16/16 PASS` | `-5.89%` | unchanged | unchanged |
| Aggregate | `44/48` | `48/48` | `-19.22%` | `-33.33%` | `-50%` |

These are measured capstone results only. They are not company-wide or production-wide savings claims.

## Real CI Status Evidence

Stable demonstrated GitHub Actions run used in the final presentation:

`31531270032`

Commit:

`25207fc5994ab893fa70dd8e48629577b686d455`

Result:

- `policy-tests`: success, `18 passed`
- `evaluation-gate`: success, `60 passed`
- `pipeline-integrity`: success, `PASS`
- `advisory-review`: success with `SKIPPED - AI SECRET UNAVAILABLE`
- `audit-trail`: success

Additional passed evidence runs:

- `31513596822`: CI-backed Change Passport source run.
- `31520499134`: verified submission-package CI evidence used in an earlier deck.
- `31527786959`: passed after final presentation visual repair.
- `31763864725`: latest final repository CI before the final quality check.

## Quick Verification

Fast deterministic checks:

```bash
pytest -q -p no:cacheprovider eval/test_risk_classifier.py eval/test_adaptive_router.py eval/test_pre_aura_control.py
pytest -q -p no:cacheprovider eval/test_ci_change_classifier.py eval/test_pipeline_integrity.py eval/test_audit_trail.py eval/test_change_passport.py
pytest -q -p no:cacheprovider eval/test_config_docs_consistency.py eval/test_governance_overreach.py
```

Governed Docker verification:

```bash
docker run --rm -i \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/workspace:ro" \
  -w /workspace \
  agentic_engineer_4:latest \
  pytest -q -p no:cacheprovider eval/test_policy.py eval/test_mcp_runtime.py eval/test_coursetools_runtime.py
```

Pipeline integrity:

```bash
python3 scripts/check-pipeline-integrity.py .github/workflows/ci.yml
```

Change Passport:

```bash
python3 scripts/build-change-passport.py AF-HIGH-001 --output /tmp/aura-passport.json
```

## Safety Boundaries

AURA Forge does not deploy to production, mutate live FitGPT, contact production databases, use real user data, or require production secrets for deterministic verification. Advisory AI review is optional and safely skips when its secret is unavailable.

## Target Codebase: FitGPT

FitGPT is a cross-platform AI wardrobe assistant. It helps users organize their clothing, get daily outfit recommendations based on weather and personal style, and track what they wear over time. The app is available as a web app and an Android app, both backed by the same FastAPI server.

---

## Tech Stack

**Web Frontend**
- React 19 with React Router 7
- Three.js and React Three Fiber for 3D outfit preview
- TensorFlow.js with MobileNet v2 for clothing classification
- Recharts for analytics

**Backend**
- FastAPI with Python
- SQLAlchemy 2.0 as the ORM
- PostgreSQL in production, SQLite for local development
- JWT and bcrypt for authentication, Google OAuth for social login
- Groq API with Llama 3.1 8B for the AURA AI chatbot
- OpenWeather API for live weather data

**Android**
- Kotlin with Jetpack Compose
- Retrofit for HTTP calls to the shared backend

**Deployment**
- Frontend: Vercel
- Backend: Render (with PostgreSQL)
- CI: GitHub Actions

---

## Live App

The production app is live at: https://fitgpt.tech

---

## How to Run the Backend Locally

1. Go into the backend folder:
   ```
   cd backend
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
   On Windows use: `venv\Scripts\activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy the environment variable template:
   ```
   cp .env.example .env
   ```
   You can leave `DATABASE_URL` blank/unset for local development — the backend automatically falls back to a local SQLite database file, so no Postgres instance is needed just to start the server. Fill in `DATABASE_URL` only if you intentionally want to connect to a local or remote PostgreSQL instance. Fill in the other values as needed for the features you plan to use.

5. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000. The interactive docs are at http://localhost:8000/docs.

---

## How to Run the Web Frontend Locally

1. Go into the web folder:
   ```
   cd web
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

The app will be available at http://localhost:5173 by default.

Make sure the backend is running locally first, and that `FRONTEND_URL` in your `.env` is set to the correct address.

---

## How to Run the Android App

Open the project root in Android Studio. Android Studio will import the Gradle project automatically.

1. Wait for Gradle sync to finish.
2. Connect a device or start an emulator.
3. Click Run or press Shift+F10.

You can also build from the command line:
```
./gradlew assembleDebug
```

The Android app talks to the same backend as the web app. Update the base URL in the network config to point to your local backend if testing locally.

---

## Environment Variables

Create a `.env` file in the `backend/` folder. Use `backend/.env.example` as the template. The variables are:

| Variable | Description |
|---|---|
| DATABASE_URL | PostgreSQL connection string. Optional for local development (see note below); required in a production-flagged environment |
| SECRET_KEY | Secret key for signing JWT tokens |
| GROQ_API_KEY | API key from console.groq.com |
| GMAIL_ADDRESS | Gmail address used for sending reset emails |
| GMAIL_APP_PASSWORD | Gmail app password (not your account password) |
| FRONTEND_URL | URL of the frontend, used for CORS (e.g. http://localhost:3000) |
| OPENWEATHER_API_KEY | API key from openweathermap.org |

**Note on `DATABASE_URL`:** Locally, if `DATABASE_URL` is omitted or left blank, the backend automatically falls back to a local SQLite database file (`backend/fitgpt.db`) — no Postgres instance is needed to start the server for local development. In a production-flagged environment (`ENVIRONMENT=production` or `ENVIRONMENT=prod`), `DATABASE_URL` is enforced as required and must point to a PostgreSQL instance; SQLite is rejected in that mode unless the existing `ALLOW_SQLITE_IN_PRODUCTION` override is explicitly set.

Never commit your `.env` file. It is listed in `.gitignore`.

---

## Testing and GitHub Actions

**Backend tests** use pytest. To run them:
```
cd backend
source venv/bin/activate
pytest tests/
```
There are 185+ backend tests covering authentication, recommendations, wardrobe management, and API routes.

**Web tests** use Jest. To run them:
```
cd web
npm test
```
There are 617 web tests covering components, hooks, and integration flows.

The original product workflow files are in `.github/workflows/`. The capstone governance workflow is `.github/workflows/ci.yml` and runs on `capstone/aura-forge`.

---

## Repository Structure

```
FitGPT/
??? app/              # Android app (Kotlin + Jetpack Compose)
??? backend/          # FastAPI backend (Python)
?   ??? app/          # Routes, models, schemas, auth logic
?   ??? database/     # SQL scripts for tables, indexes, and views
?   ??? tests/        # pytest test suite
?   ??? .env.example  # Environment variable template
?   ??? requirements.txt
??? web/              # React web frontend
??? README.md
```
