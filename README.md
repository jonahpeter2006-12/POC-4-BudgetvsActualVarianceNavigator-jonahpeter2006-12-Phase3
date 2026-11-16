# Budget vs Actual Variance Navigator

A containerized financial analytics application with an operational budget-versus-actual dashboard, Phase 3 comparative intelligence, and an evidence-grounded assistant.

> **Phase 3 release status: CERTIFICATION BLOCKED.**
> The current public Render deployment and local Post #6 implementation have different capabilities. Clean-clone validation is completed with documented limitations. Public browser acceptance and the official evidence pack have since been completed; reviewer approval and certification remain outstanding.

## 1. Project Overview

The project contains two main services:

- **Frontend:** Next.js, React, TypeScript, and Recharts.
- **Backend:** FastAPI, Python, Pandas, and DuckDB.

The operational dashboard reads `backend/budget_data.csv`. Phase 3 comparative intelligence uses `data/canonical/intelligence_data.csv` and exposes validated findings and supporting evidence through the intelligence API.

The deterministic assistant supports five approved question types. An optional Gemini explanation layer exists in the local Post #6 implementation; it does not replace deterministic financial values or evidence.

## 2. Public Render Deployment

| Service | URL |
|---|---|
| Frontend | https://poc4-budget-phase3-frontend.onrender.com |
| Backend API | https://poc4-budget-phase3-backend.onrender.com |
| Backend health | https://poc4-budget-phase3-backend.onrender.com/api/health |
| Intelligence health | https://poc4-budget-phase3-backend.onrender.com/api/intelligence/health |

Both public Render services were verified Live on commit `daa7f61`. The public backend provides the deterministic Mode A assistant.

The public deployment has passed the recorded HTTP and analytical checks, including 1,325 validation checks with zero failures and zero warnings. Supported and out-of-scope deterministic assistant responses were also checked.

**Important deployment boundary:** Local Post #6 Gemini Mode B changes have not yet been published or deployed to Render. Public HTTP checks do not establish complete browser-based acceptance or final release certification.

Render free services may spin down after inactivity. The first request after an idle period may take 50 seconds or more while the service wakes up.

## 3. Project Structure

```text
.
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── assistant.py
│   ├── gemini_explainer.py
│   ├── budget_data.csv
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── data/
│   └── canonical/
│       └── intelligence_data.csv
├── data-science/
│   ├── scripts/
│   └── notebooks/
├── docs/
├── scripts/
├── tests/
├── screenshots/
├── test-results/
├── final-evidence/
├── docker-compose.yml
└── README.md
```

## 4. Services and Ports

| Service | Technology | Local URL |
|---|---|---|
| Frontend | Next.js | http://localhost:3000 |
| Backend | FastAPI | http://localhost:8000 |
| Backend health | FastAPI | http://localhost:8000/api/health |
| API documentation | FastAPI | http://localhost:8000/docs |

## 5. Prerequisites

- Python 3.11 or a compatible project-supported Python version.
- Node.js and npm compatible with the frontend lockfile.
- Docker Desktop and Docker Engine for container validation.
- Docker Compose.
- Git.
- A supported browser for manual application acceptance.

For browser automation, Chrome and a compatible ChromeDriver/Selenium setup are required. On managed Windows devices, follow the organization's approved application-control process. Do not disable or bypass endpoint security controls.

## 6. Local Backend Setup

From the repository root, install backend dependencies:

```powershell
python -m pip install -r .\backend\requirements.txt
```

Start the backend from the `backend` directory:

```powershell
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend should be available at:

`http://127.0.0.1:8000`

Useful endpoints:

- `GET /api/health`
- `GET /api/intelligence/health`
- `GET /api/intelligence/metadata`
- `GET /api/intelligence/summary`
- `GET /api/intelligence/results`
- `GET /api/intelligence/results/{result_id}`
- `POST /api/assistant/query`
- `/docs` for interactive API documentation.

## 7. Local Frontend Setup

In another PowerShell terminal, from the repository root:

```powershell
npm --prefix frontend ci
```

Configure the frontend API base URL for local development in the current PowerShell session:

```powershell
$env:NEXT_PUBLIC_API_URL = "http://127.0.0.1:8000"
```

Start the frontend:

```powershell
npm --prefix frontend run dev
```

Open:

`http://localhost:3000`

## 8. Run with Docker Compose

Open PowerShell in the repository root.

Build and start the services:

```powershell
docker compose up --build
```

Open the application:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/api/health

Useful commands:

```powershell
docker compose ps
docker compose logs
docker compose logs backend
docker compose logs frontend
```

To stop the Compose services, press `Ctrl + C` in the terminal and run:

```powershell
docker compose down
```

Only use `docker compose down` when you intend to stop and remove the Compose-managed containers and network.

## 9. Backend API

| Endpoint | Purpose |
|---|---|
| `/api/health` | Backend health status |
| `/api/summary` | Operational summary metrics |
| `/api/waterfall` | Waterfall analysis |
| `/api/department-breakdown` | Department breakdown |
| `/api/monthly-trends` | Monthly trends |
| `/api/department-heatmap` | Department heatmap |
| `/api/forecast` | Operational forecast data |
| `/api/filters` | Available filters |
| `/api/intelligence/health` | Analytical service readiness |
| `/api/intelligence/metadata` | Analytical project and version metadata |
| `/api/intelligence/summary` | Analytical summary and validation metrics |
| `/api/intelligence/results` | Comparative intelligence findings |
| `/api/intelligence/results/{result_id}` | Finding details and supporting evidence |
| `/api/assistant/query` | Grounded assistant query endpoint (POST) |

The assistant uses deterministic findings and evidence. Unsupported questions must remain out of scope. The assistant does not provide unsupported predictions, fraud conclusions, or risk scores.

## 10. Data and Analytical Scope

Canonical dataset:

`data/canonical/intelligence_data.csv`

Recorded profile:

- 72 canonical rows and 20 columns.
- 18 independent synthetic source observations.
- Four measures: Budget, Actual, Committed, and Forecast.
- January–March 2026 reporting period.
- Six cost centres, four departments, and six expenditure categories.

Approved analytical method:

- Track A — Comparative Intelligence.
- Dataset version: `1.0.0`.
- Method version: `1.0.0`.
- Contract version: `1.0.0`.
- 64 findings: 16 overall and 48 monthly.

Variance is calculated as Actual minus Budget. Positive variance indicates spending above budget. Committed and Forecast remain separate measures. Forecast is illustrative, not predictive.

The 72 canonical records are derived measure rows, not 72 independent transactions. Do not generalize this synthetic sample to a wider population. Monthly findings with insufficient evidence must retain their documented limitations.

## 11. Assistant and Optional Gemini Explanation

The deterministic assistant supports five approved question types:

1. Cost-centre variance comparison.
2. Department comparison.
3. Expenditure-category lookup.
4. Finding-evidence lookup.
5. Monthly insufficient-evidence lookup.

### Optional Gemini Mode B

Gemini Mode B is an optional explanation layer in the local Post #6 implementation.

Configure these variables only in the backend environment:

- `GEMINI_API_KEY` — private Google AI Studio API key.
- `GEMINI_MODEL` — `gemini-3.5-flash-lite`.

For local PowerShell testing, set them in the backend process environment:

```powershell
$env:GEMINI_API_KEY = "YOUR_PRIVATE_API_KEY"
$env:GEMINI_MODEL = "gemini-3.5-flash-lite"
```

Do not paste a real key into source files, commit it, expose it to frontend code, or include it in screenshots or evidence.

The `.env.example` file documents variable names and the model default; it must not contain a real secret.

When the key is absent or Gemini is unavailable, the assistant should retain its deterministic response. Deterministic findings and evidence remain authoritative. Gemini explanations are non-authoritative and its bounded validation checks are not comprehensive semantic or prompt-injection protection.

**Deployment status:** Gemini Mode B has passed the recorded local API and application tests. It is not yet deployed or configured on the public Render backend.

## 12. Render Deployment Configuration

Both services use Docker deployment on Render.

| Setting | Backend | Frontend |
|---|---|---|
| Service name | `poc4-budget-phase3-backend` | `poc4-budget-phase3-frontend` |
| Runtime | Docker | Docker |
| Dockerfile path | `backend/Dockerfile` | `frontend/Dockerfile` |
| Build context | `backend` | `frontend` |
| Branch | `master` | `master` |

Frontend environment variable:

```text
NEXT_PUBLIC_API_URL=https://poc4-budget-phase3-backend.onrender.com
```

The backend uses Render's assigned `PORT` environment variable.

Do not treat the current public deployment as the final Post #6 release until approved changes have been published, deployed, and verified.

## 13. Validation Commands

Run from the repository root.

Compile the backend and relevant test modules:

```powershell
python -m py_compile .\backend\main.py .\backend\gemini_explainer.py .\tests\test_assistant_api.py .\tests\test_gemini_explainer.py
```

Run the Post #6 targeted Python tests:

```powershell
python -m pytest .\tests\test_assistant_api.py .\tests\test_gemini_explainer.py -v
```

Run the Gemini tests:

```powershell
python -m pytest .\tests\test_gemini_explainer.py -v
```

Compile backend and test modules:

```powershell
python -m compileall -q backend tests
```

Build the frontend:

```powershell
npm --prefix frontend run build
```

Build the backend Docker image:

```powershell
docker build -f backend/Dockerfile -t poc4-budget-backend:post6 .
```

These commands reflect recorded local checks, not a guarantee that every future working-tree state or release commit has passed. Re-run required checks against the intended release commit.

## 14. Recorded Post #6 Validation Results

The following results were recorded locally on 14 November 2026:

| Check | Recorded result |
|---|---|
| Post #6 targeted Python tests | 24 passed, 0 failed |
| Full default pytest collection | Blocked: two legacy modules require requests |
| Dedicated Gemini tests | 8 passed, 0 failed |
| Python compileall | Passed |
| Frontend production build | Passed |
| Frontend TypeScript build check | Passed |
| Targeted Data Intelligence ESLint check | Passed |
| Backend Docker build and module import | Passed |
| Analytical and reconciliation validation | 1,325 checks, 0 failures, 0 warnings |
| Public Render HTTP and analytical checks | Passed as recorded |
| Fresh Post #6 Selenium browser execution | Blocked before browser startup by Windows Application Control |
| Clean-clone validation | 24 tests passed; compilation, reproducibility, and frontend build passed; Docker and Selenium blocked by environment limitations |

The latest fresh Post #6 targeted test runs passed 24 tests with no warnings. A separate full default pytest collection attempt was blocked because tests/test_live_application.py and tests/test_post4_intelligence.py require the missing requests package in the dedicated environment. No tests from those two modules ran. This limitation is separate from the analytical validation count.

A repository-wide frontend lint run also reported 12 existing issues in `frontend/src/app/page.tsx`; the targeted Data Intelligence page lint result must not be represented as a clean repository-wide lint result.

Historical browser automation results from an earlier Post #4 run are not fresh Post #6 browser acceptance evidence.

## 15. Known Limitations and Outstanding Release Gates

- The dataset is synthetic and based on 18 independent source observations.
- The reporting period covers only three months.
- Monthly findings with insufficient evidence remain limited.
- Forecast values are illustrative.
- Assistant scope is intentionally narrow.
- Gemini safeguards do not constitute a comprehensive security audit.
- The public Render deployment uses deterministic Mode A, not the local Gemini Mode B implementation.
- Fresh Post #6 Selenium execution was blocked by Windows Application Control.
- Clean-clone validation completed with documented limitations: Docker Engine was unavailable and Selenium browser startup was blocked.
- Final release evidence and the final Repomix remain outstanding.
- The final release commit and tag have not been established.
- Final reviewer approval and certification remain outstanding.

## 16. Release and Handover Discipline

Before treating this project as a certified release:

1. Review the complete working-tree changes.
2. Exclude API keys, local environment files, temporary files, accidental artifacts, and unnecessary backups from release evidence.
3. Review the completed clean-clone validation and resolve or obtain reviewer acceptance for its documented Docker and Selenium limitations.
4. Complete fresh browser acceptance using an approved browser automation environment or the formally accepted alternative.
5. Re-run required tests and build checks against the intended release commit.
6. Collect genuine final evidence without relabeling historical screenshots or test results.
7. Complete the release manifest using the actual release commit identifier.
8. Generate the final Repomix after all approved changes are complete.
9. Obtain reviewer confirmation before describing Phase 3 as certified.

Do not stage, commit, push, tag, or deploy without explicit authorization.

## 17. Current Release Status

**PHASE 3 CERTIFICATION BLOCKED.**

The project has substantial recorded analytical, application, API, and local test evidence. However, local success and public HTTP availability do not replace the outstanding acceptance of documented clean-clone limitations, fresh browser acceptance, final evidence, release packaging, and reviewer approval requirements.

This README documents the current implementation and known boundaries. It does not claim that the complete Post #6 release has been deployed, browser-validated, or certified.

## Evidence and Browser Acceptance Reconciliation — 2026-11-15

The official final-evidence structure has now been assembled: all 15 required folders are present, with 67 files across those folders at the time of the structural audit. The audit found no zero-byte files and no duplicate filenames within individual folders. This is a structural/file-presence result, not reviewer certification.

Post-correction local validation is recorded separately:
- Targeted local Python tests: 27 passed (19 assistant API tests and 8 Gemini explainer tests).
- Local Selenium/browser acceptance: 17 checks passed (4 assistant regression, 9 filter/responsive, and 4 viewport checks).
- Local Chrome and ChromeDriver were version-matched at 157.0.8103.78.
- The local assistant correction remains uncommitted, unpublished, and undeployed. Public Render remains on commit daa7f61.
- Public post-correction browser acceptance: NOT PERFORMED.
- Clean-clone Docker build: BLOCKED because the Docker Desktop Linux engine was unavailable. The earlier original-environment Docker result is not a clean-clone Docker result.
- At this earlier checkpoint, final Repomix generation and reviewer approval remained outstanding. The Repomix was subsequently generated and XML-validated for GitHub master commit 029b6bb; reviewer acceptance had not yet been recorded at that historical checkpoint.

The release status remains **PHASE 3 CERTIFICATION BLOCKED — NOT CERTIFIED**.

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
