# PHASE 3 HANDOVER GUIDE

## 1. Purpose

This guide provides the setup, operation, API, validation, and known limitations information needed to continue maintaining the Phase 3 Budget vs Actual Variance Navigator.

This handover reflects the current local Post #6 implementation and distinguishes it from the older public Render deployment.

## 2. Project Overview

The project contains:
- A Next.js operational dashboard and Data Intelligence frontend.
- A FastAPI backend.
- An operational budget dataset.
- A canonical financial intelligence dataset.
- Track A comparative analytical outputs.
- A deterministic evidence-grounded assistant.
- An optional local Gemini explanation layer.

The analytical scope is descriptive budget-versus-actual comparison. It does not provide predictive, fraud-detection, or risk-scoring capabilities.

## 3. Prerequisites

Install or provide:
- Python 3.11 or a compatible project-supported Python version.
- Node.js and npm compatible with the frontend lockfile.
- Docker Desktop for container validation.
- Git.
- A supported browser for manual application acceptance.

For browser automation, Chrome and a compatible ChromeDriver/Selenium setup are required. On managed Windows devices, follow the organization's approved application-control process. Do not disable or bypass endpoint security controls.

## 4. Local Backend Setup

From the repository root, install backend dependencies:

`python -m pip install -r .\backend\requirements.txt`

Start the backend from the `backend` directory:

`python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`

The backend should be available at:

`http://127.0.0.1:8000`

Useful endpoints:
- `GET /api/health`
- `GET /api/intelligence/health`
- `GET /api/intelligence/metadata`
- `GET /api/intelligence/summary`
- `GET /api/intelligence/results`
- `POST /api/assistant/query`
- `/docs` for the interactive API documentation.

## 5. Local Frontend Setup

In another terminal, from the repository root:

`npm --prefix frontend ci`

Configure the frontend API base URL for local development using the project's supported frontend environment configuration:

`NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`

Start the frontend:

`npm --prefix frontend run dev`

Open:

`http://localhost:3000`

For Windows PowerShell, environment variables for the current session can be set using `$env:VARIABLE_NAME = "value"` before starting the relevant process.

## 6. Gemini Explanation Configuration

Gemini Mode B is optional and is available in the local Post #6 implementation.

Configure these variables only in the backend environment:

- `GEMINI_API_KEY` — private Google AI Studio API key.
- `GEMINI_MODEL` — `gemini-3.5-flash-lite`.

Never commit a real API key, paste it into source files, or configure it as a frontend variable.

The `.env.example` file documents variable names and the model default. It must not contain a real secret.

When the key is absent or Gemini is unavailable, the assistant should retain its deterministic response. Deterministic findings and evidence remain authoritative; Gemini is only an explanation layer.

The current public Render deployment does not yet include this local Gemini implementation or its environment configuration.

## 7. Data and Analytical Scope

Canonical dataset:

`data/canonical/intelligence_data.csv`

Recorded profile:
- 72 rows.
- 20 columns.
- 18 independent synthetic source observations.
- Four measures: Budget, Actual, Committed, and Forecast.
- January–March 2026 reporting period.

Approved analytical method:
- Track A — Comparative Intelligence.
- Dataset version 1.0.0.
- Method version 1.0.0.
- Contract version 1.0.0.
- 64 findings: 16 overall and 48 monthly.

Variance is Actual minus Budget. Positive variance indicates spending above budget. Committed and Forecast must remain separate measures. Forecast is illustrative, not predictive.

The 72 canonical records are derived measure rows, not 72 independent transactions. Do not generalize the synthetic sample to a wider population.

## 8. Assistant Scope

The deterministic assistant supports five approved question types:
1. Cost-centre variance comparison.
2. Department comparison.
3. Expenditure-category lookup.
4. Finding-evidence lookup.
5. Monthly insufficient-evidence lookup.

Unsupported questions must remain out of scope. Do not expand assistant categories or use Gemini to invent financial values, evidence, predictions, causal claims, fraud findings, or risk scores.

## 9. Validation Commands

From the repository root:

Compile the backend and relevant test modules:

`python -m py_compile .\backend\main.py .\backend\gemini_explainer.py .\tests\test_assistant_api.py .\tests\test_gemini_explainer.py`

Run the full Python suite:

`python -m pytest -v`

Run Gemini tests:

`python -m pytest .\tests\test_gemini_explainer.py -v`

Build the frontend:

`npm --prefix frontend run build`

Build the backend Docker image:

`docker build -f backend/Dockerfile -t poc4-budget-backend:post6 .`

These commands reflect the successful local checks recorded for Post #6. Re-run them on the final release commit rather than assuming earlier results automatically validate later changes.

## 10. Public Render Services

The current public service references are:

- Frontend: https://poc4-budget-phase3-frontend.onrender.com
- Backend: https://poc4-budget-phase3-backend.onrender.com

The public backend was last verified on commit `08327d7` and uses the deterministic Mode A assistant. The local Post #6 Gemini implementation has not yet been published or deployed.

Do not treat the public deployment as the final Post #6 release until the approved changes have been published, deployed, and verified.

## 11. Known Limitations and Outstanding Work

- Data is synthetic and based on 18 independent source observations.
- The reporting period covers only three months.
- Monthly findings with insufficient evidence remain limited.
- Forecast is illustrative.
- Assistant scope is intentionally narrow.
- Gemini safeguards are bounded validation checks, not comprehensive semantic or prompt-injection protection.
- Fresh Post #6 Selenium execution was blocked by Windows Application Control.
- Clean-clone validation remains outstanding.
- Final release evidence, manifest, and final Repomix remain outstanding.
- Final reviewer approval and certification remain outstanding.

## 12. Handover and Release Discipline

Before treating the project as a certified release:

1. Review the complete working-tree changes.
2. Exclude API keys, local environment files, temporary files, and accidental backups.
3. Complete the approved clean-clone and browser validation.
4. Re-run the required tests and build checks against the intended release commit.
5. Collect genuine final evidence without relabeling historical screenshots or test results.
6. Complete the release manifest using the actual commit identifier.
7. Generate the final Repomix after the final approved changes.
8. Obtain reviewer confirmation before describing Phase 3 as certified.

Do not stage, commit, push, tag, or deploy without explicit authorization.

## 13. Handover Status

**HANDOVER DOCUMENTATION: PREPARED WITH OUTSTANDING RELEASE REQUIREMENTS.**

This guide records the current setup and operating boundaries. It does not certify the complete Phase 3 release.
