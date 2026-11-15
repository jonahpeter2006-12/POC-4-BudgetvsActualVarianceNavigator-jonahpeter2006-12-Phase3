# CLEAN CLONE VALIDATION REPORT

## 1. Purpose

This report records independent validation of the published Phase 3 Post #6 Git commit in a separate fresh clone.

## 2. Release Commit and Environment

- Repository: POC-4-BudgetvsActualVarianceNavigator-jonahpeter2006-12-Phase3
- Branch: master
- Validated commit: `daa7f610882862157287e350d8850499cb8ca44f`
- Clean clone path: `C:\poc4-post6-cleanclone`
- Python: 3.11
- Operating system: Windows

The clean clone checked out the exact Post #6 commit published to GitHub.

## 3. Validation Results

| Validation | Result |
|---|---|
| Fresh clone of published commit | PASS |
| Backend dependency installation | PASS |
| Python test suite | PASS — 24 passed, 0 failed |
| Python compilation (`backend`, `tests`, `data-science/scripts`) | PASS |
| Reproducibility verification | PASS |
| Frontend dependency installation (`npm ci`) | PASS |
| Frontend production build | PASS |
| Clean-clone Docker engine connection | BLOCKED |
| Clean-clone Docker image build | NOT EXECUTED |

### Test evidence

Command: `.\.venv\Scripts\python.exe -m pytest -v`

Result: 24 passed in 3.10 seconds.

The 24 tests include the assistant API and Gemini explainer tests. The eight Gemini explainer tests are included in the 24-test total.

### Compilation evidence

Command: `.\.venv\Scripts\python.exe -m compileall -q backend tests data-science\scripts`

Result: exit code 0.

### Reproducibility evidence

Command: `.\.venv\Scripts\python.exe .\data-science\scripts\verify_reproducibility.py`

Result:
- Two pipeline runs completed.
- Four assessment outputs compared.
- Assessment outputs matched.
- Input files remained unchanged.
- Final analytical readiness remained stable.
- Reproducibility status: passed.

The canonical dataset contained 72 records and 20 columns, representing 18 independent source observations.

### Frontend evidence

Commands:
- `npm --prefix frontend ci`
- `npm --prefix frontend run build`

Results:
- 396 packages installed.
- Production compilation passed.
- TypeScript validation passed.
- Static routes `/` and `/data-intelligence` generated.
- Frontend build exit code: 0.

The dependency installation reported seven moderate audit vulnerabilities and an ESLint deprecation warning. These warnings did not prevent the production build. No automatic dependency upgrades were performed.

## 4. Docker Limitation

The clean-clone Docker check could not connect to the Docker Desktop Linux engine.

The Docker CLI was installed, but the engine named by the active Docker context was unavailable. Consequently, the clean-clone Docker image build did not execute.

A Docker image build and local Docker runtime/API checks had passed previously in the original project environment. Those results are separate from the clean-clone Docker check and must not be represented as a clean-clone Docker pass.

No Windows security controls were bypassed.

## 5. Other Validation Limitations

- Fresh Selenium browser validation remains blocked by Windows Application Control before browser startup.
- No passing Post #6 Selenium browser run is claimed.
- Public HTTP and API checks do not replace browser-based visual, interaction, accessibility, or responsive testing.
- Gemini Mode B public-provider validation is not claimed by this report.

## 6. Final Assessment

**CLEAN-CLONE VALIDATION: PASS WITH DOCUMENTED LIMITATIONS.**

Fresh-clone dependency installation, Python tests, compilation, analytical reproducibility, and frontend production build passed against the exact published Post #6 commit.

The clean-clone Docker image build was not executed because the Docker engine was unavailable.

**RELEASE CERTIFICATION: NOT GRANTED BY THIS REPORT.**

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
- The Render backend deployment commit is confirmed as `3610659`. The exact active frontend deployment commit has not been independently confirmed in the Render dashboard evidence reviewed for this reconciliation.
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The final Repomix has not yet been regenerated from the finalized release state.
- Reviewer approval and the required certification decision have not been received. The release tag has not been created.

**Current release status: NOT CERTIFIED — reviewer approval and final release packaging remain outstanding.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.
