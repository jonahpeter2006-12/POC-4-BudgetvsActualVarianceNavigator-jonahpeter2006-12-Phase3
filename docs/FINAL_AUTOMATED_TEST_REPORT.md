# FINAL AUTOMATED TEST REPORT

## 1. Purpose

This report records the automated validation performed for the Post #6 Phase 3 release work. It distinguishes successful automated tests from environment-blocked browser execution.

## 2. Post #6 Targeted Python Tests

The Post #6 targeted Python test modules were executed in the dedicated `.venv-post6` environment with:

`python -m pytest .\tests\test_assistant_api.py .\tests\test_gemini_explainer.py -v`

Fresh recorded results:
- Tests passed: 24.
- Tests failed: 0.
- Warnings: 0.
- Overall result: PASS for these two targeted modules.

A separate full default pytest discovery attempt using `python -m pytest -v` was blocked during test collection. The legacy modules `tests/test_live_application.py` and `tests/test_post4_intelligence.py` require the `requests` package, which is not installed in the dedicated environment. No tests from those two modules ran in that attempt.

The targeted 24-test result must not be interpreted as a passing complete repository test suite.
## 3. Gemini Explanation Test Coverage

The 8 tests in `tests/test_gemini_explainer.py` passed as part of the 24-test targeted run described above. They were not counted as an additional 8 tests.

Coverage includes missing API key behavior, accepted explanations, rejection of unsupported numeric claims, contradictory budget-direction claims, provider failure fallback, exclusion of unsupported questions from Gemini explanation, excessive explanation length rejection, and empty explanation rejection.
## 4. Static and Build Validation

Recorded successful checks:
- Python compilation of the backend and tests using `python -m compileall -q backend tests`.
- Production frontend build using `npm --prefix frontend run build`.
- TypeScript validation as part of the production frontend build.
- Targeted ESLint check for `frontend/src/app/data-intelligence/page.tsx`.
- Docker backend image build using `docker build -f backend/Dockerfile -t poc4-budget-backend:post6 .`.
- Import verification of `backend.gemini_explainer` inside the built Docker image.

The production frontend build completed successfully with TypeScript validation.

Repository-wide frontend lint is not recorded as passing. An earlier repository-wide run reported 12 issues in the existing operational dashboard file `frontend/src/app/page.tsx`. The Post #6 work did not broadly refactor that file.

## 5. Docker Runtime Checks

The newly built backend image was started in a separate local test container.

Recorded checks:
- `/api/health` returned a healthy response.
- `/api/intelligence/health` reported readiness and 64 findings.
- `/api/intelligence/summary` reported 1,325 passed checks, 0 failures, and 0 warnings.
- A representative supported assistant question returned grounded CC-101 evidence.
- An unsupported prediction and fraud-risk question returned OUT_OF_SCOPE without unsupported financial conclusions.

The container was tested without a Gemini API key, confirming the deterministic fallback state.

## 6. Browser Automation

A Post #6 Selenium execution was attempted using:

`python .\tests\test_live_application.py`

The run was blocked before browser startup. Windows Application Control prevented Selenium Manager from launching `selenium-manager.exe`, and no locally available ChromeDriver was found.

Result: BLOCKED — browser automation did not reach the application.

This is not counted as a passing Selenium test or as an application regression failure. The existing Post #4 Selenium reports remain historical evidence only.

## 7. Test Environment and Limitations

- The two Post #6 targeted Python test modules passed: 24 tests, 0 failures. Full default pytest collection was blocked by missing `requests` in two legacy test modules; those modules did not run.
- All 8 Gemini explanation tests passed within the 24-test targeted run; they are included in that total.
- Python compilation and frontend production build passed.
- The Docker image and runtime checks validate the local Post #6 backend implementation.
- Gemini Mode B was tested locally but is not deployed on the public Render service.
- Browser-based Post #6 regression remains outstanding.
- Repository-wide frontend lint has documented existing issues.
- These results do not establish exhaustive security, accessibility, or end-to-end browser coverage.

## 8. Conclusion

**PASS WITH DOCUMENTED LIMITATIONS** for the 24 targeted Python tests, Python compilation, frontend build, targeted lint, Docker build, and local runtime checks. Full default pytest collection remains blocked during collection because two legacy test modules require the missing `requests` package.

**BLOCKED** for fresh Post #6 Selenium browser automation due to Windows Application Control.

This report does not claim complete automated release validation or final Phase 3 certification.

## Post-Correction Local Results — 2026-11-15

These results are additional to, and separate from, the clean-clone results above:

- Clean clone at commit `daa7f610882862157287e350d8850499cb8ca44f`: 24 targeted tests passed. Compilation, reproducibility, frontend dependency installation, and frontend production build passed. Clean-clone Docker build was BLOCKED because the Docker Desktop Linux engine was unavailable.
- After the subsequent local assistant correction: 27 targeted Python tests passed (19 assistant API tests and 8 Gemini explainer tests). Python compilation and `git diff --check` passed.
- Local browser acceptance after the correction: 17 checks passed (4 assistant regression, 9 filter/responsive, 4 viewport).
- Public Render remains on commit `daa7f61`; the local correction has not been committed, pushed, or deployed.
- Public post-correction browser acceptance: NOT PERFORMED. The earlier Windows Application Control block remains a historical environment-blocked attempt, not a passing browser test.
- The separate full default pytest collection attempt remains BLOCKED because the dedicated environment lacked `requests` for two legacy test modules; those modules did not run.
- These results do not establish complete repository-wide test coverage or Phase 3 certification.

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
- Final Repomix snapshot generation and XML validation were completed for GitHub master commit `029b6bb` on 15 November 2026; reviewer approval and certification remain outstanding.
- No Phase 3 release tag has been created.

**PHASE 3 STATUS: DRAFT — NOT CERTIFIED.**
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
- Reviewer approval and the required certification decision have not been received. The release tag has not been created.

**Current release status: NOT CERTIFIED — reviewer approval and final release packaging remain outstanding.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.
