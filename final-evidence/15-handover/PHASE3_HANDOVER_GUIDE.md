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
- Clean-clone validation is complete with documented limitations: 24 targeted tests passed, compilation and reproducibility passed, and the frontend build passed; the clean-clone Docker build was blocked by the unavailable Docker Desktop Linux engine.
- The release manifest exists. The required 15-folder final evidence pack and final Repomix remain outstanding.
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

## Public Post #6 Acceptance Addendum — 2026-11-15

A fresh public Render browser and API acceptance run completed on 2026-11-15.

**Result: PASS — 19 checks passed, 0 failed.**

Verified:
- Chrome 157.0.8103.78 started using the matching ChromeDriver.
- Backend health, intelligence health, and intelligence summary returned HTTP 200.
- The supported "Compare cost centres" assistant question returned SUPPORTED.
- Three predictive/future-projection questions returned OUT_OF_SCOPE with zero evidence references.
- Public dashboard and Data Intelligence pages rendered without a visible backend connection error.
- Data Intelligence displayed 64 findings, 1,230/1,230 analytical checks, 95/95 reconciliation checks, and 1,325 passed with 0 failed.
- Both pages passed exact 390 x 844 mobile viewport checks with no horizontal overflow.

Fresh machine-readable evidence and screenshots are included in the official evidence folders:
- 11-selenium
- 14-screenshots
- 09-assistant-or-skip

The earlier preliminary browser run and diagnostic evidence remain preserved.

**Deployment identity qualification:** local and remote master both identify commit `3610659d87831639ee2fc3b17d8ce66beb3fdcb1`. Public API and browser behavior have been verified after the correction was pushed. The Render dashboard deployment record must still be checked to independently confirm the exact commit associated with the active backend deployment.

**Outstanding limitations:**
- Clean-clone Docker build remains BLOCKED because the Docker Desktop Linux engine was unavailable.
- Full default pytest collection previously remained blocked because two legacy test modules required the missing `requests` package in that clean-clone environment.
- Public Gemini Mode B behavior has not been certified.
- Historical checkpoint: reviewer acceptance and formal certification had not yet been recorded when this 15 November 2026 status was written. Subsequent reviewer acceptance is documented in the 16 November 2026 reconciliation.
- Historical checkpoint: the Phase 3 release tag had not yet been created when this section was recorded. The subsequently published tag is documented in the 16 November 2026 reconciliation.

**Historical checkpoint status when this section was recorded: DRAFT - NOT CERTIFIED.**
This addendum records executed checks; it is not reviewer certification.

## Final status reconciliation — 15 November 2026

This reconciliation supersedes earlier status snapshots in this document wherever they describe the assistant correction as unpublished, the public browser acceptance as not performed, or the public backend as remaining on commit `daa7f61`. Those statements accurately describe earlier checkpoints but are no longer the current release status.

### Verified current results

- The assistant scope correction is committed and pushed to GitHub `master` at commit `3610659d87831639ee2fc3b17d8ce66beb3fdcb1`.
- The Render dashboard independently confirmed the backend service `poc4-budget-phase3-backend` Live on commit `3610659`.
- Public assistant API regression: 4/4 checks passed. The supported comparison question returned `SUPPORTED`; the three predictive/future-projection questions returned `OUT_OF_SCOPE` with zero evidence.
- Public Selenium acceptance on 15 November 2026: **19 passed, 0 failed**. This included backend and intelligence health, summary, assistant API behavior, desktop dashboard rendering, Data Intelligence content, and both pages at a 390 × 844 mobile viewport.
- The public acceptance report is `final-evidence/browser-automation/post6-public-final-acceptance-20261115-142307.json`. The corresponding final dashboard and Data Intelligence screenshots are stored in the official evidence folders.
- The official evidence structure contains all 15 required folders and 73 files. The latest structural and evidence-copy consistency audits passed, with zero report-copy failures and zero required-evidence-copy failures.
- The correction's local targeted tests passed 27/27. Python compilation passed. Earlier clean-clone checks recorded 24 targeted tests passing, with the limitations below.

### Remaining limitations and certification status

- Clean-clone Docker build remains **BLOCKED** because the Docker Desktop Linux engine was unavailable during that validation.
- Full default pytest collection in the separate clean-clone environment was **BLOCKED** by missing `requests` for two legacy test modules; those modules were not executed in that environment.
- Public Gemini Mode B behavior has not been certified. The public results establish the tested deterministic assistant behavior only.
- Both Render frontend and backend services are confirmed Live on commit `029b6bb` (15 November 2026).
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The final Repomix snapshot was generated from GitHub master commit `029b6bb` and XML-validated on 15 November 2026.
- Historical checkpoint: reviewer acceptance and release-tag publication had not yet been recorded when this status was written. Subsequent reviewer acceptance and the published release tag are documented in the 16 November 2026 reconciliation.

**Current status: Project development ACCEPTED AND COMPLETE; professional demonstration ACCEPTED; source release tag v2.0.0-phase3-final points to commit 3f3f751814ba6b6b8947bf4c14c8846855a53d92; formal Phase 3 release certification PENDING separate governance approval.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.

## Final Governance and Release Reconciliation - 2026-11-16

This reconciliation supersedes earlier release-status statements in this document wherever they conflict with the verified project acceptance, published release tag, final Repomix snapshot, or completed public browser acceptance recorded below. Earlier checkpoints are retained as historical records and are not rewritten.

### Project and reviewer outcome

- Project Development: **COMPLETE**.
- Professional Demonstration: **ACCEPTED**.
- Final project assessment: **ACCEPTED** by the reviewer.
- The reviewer confirmed that no further functionality, analytical redesign, or UI enhancements are required.
- Formal Phase 3 release certification remains a separate governance decision and is **PENDING**. Project acceptance must not be represented as formal release certification.

### Published source release

- Git branch: `master`.
- Verified local HEAD and GitHub `master`: `3f3f751814ba6b6b8947bf4c14c8846855a53d92`.
- Published annotated release tag: `v2.0.0-phase3-final`.
- The tag's peeled commit target was verified against the same commit.
- Final Repomix snapshot: `repomix-output.final-20261115.xml`.
- The final Repomix snapshot was generated and XML-validated for the release commit.
- The release tag and Repomix identify the source snapshot. They do not independently establish the commit currently running on Render.

### Public acceptance and validation evidence

- Fresh public browser acceptance: **19 passed, 0 failed**, including dashboard and Data Intelligence rendering, supported assistant behavior, and 390 x 844 mobile viewport checks.
- Public acceptance evidence: `final-evidence/browser-automation/post6-public-final-acceptance-20261115-142307.json`, with associated screenshots in the evidence folders.
- Latest targeted local Python tests: **27 passed, 0 failed** (19 assistant API tests and 8 Gemini explainer tests).
- Earlier clean-clone targeted Python tests: **24 passed** in that validation environment.
- Analytical and reconciliation validation: **1,325 checks passed, 0 failed**, as recorded in the acceptance evidence.
- These are scoped test and acceptance results. They must not be described as a successful full repository-wide pytest run.

### Preserved limitations and qualifications

- A separate full default pytest collection attempt in the clean-clone environment was **BLOCKED** because the `requests` dependency was missing for two legacy test modules. Those modules did not execute in that environment.
- The clean-clone Docker image build was **NOT EXECUTED** because the Docker Desktop Linux engine was unavailable. This remains a clean-clone environment limitation, not a Docker build pass.
- Earlier Docker build/runtime success in the original project environment remains a separate result.
- Public Gemini Mode B is not certified as a complete public release capability. Tested Gemini behavior and fallback evidence must be distinguished from full Mode B certification. Deterministic financial findings and evidence remain authoritative.
- Historical deployment records in the reports identify different Render commits at different checkpoints. The release tag commit must not be substituted for a Render deployment identity. Confirm the active service deployment commit directly in Render before making a current deployment-identity claim.
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The canonical dataset contains 72 derived measurement rows from 18 independent synthetic source observations. These are not 72 independent transactions.
- The reporting period is January to March 2026. Findings have documented sample and evidence limitations.
- Forecast is illustrative, not predictive. No predictive forecasting, anomaly detection, risk scoring, causal conclusions, or automated financial decisions are claimed.
- The assistant remains limited to its five approved deterministic question types. Unsupported predictive questions remain out of scope.

### Final status

**PROJECT DEVELOPMENT: COMPLETE**

**PROFESSIONAL DEMONSTRATION: ACCEPTED**

**SOURCE RELEASE TAG: PUBLISHED AND VERIFIED**

**FORMAL PHASE 3 RELEASE CERTIFICATION: PENDING SEPARATE GOVERNANCE REVIEW**

This reconciliation records the accepted project outcome and verified release packaging. It does not claim that formal Phase 3 release certification has been granted.
