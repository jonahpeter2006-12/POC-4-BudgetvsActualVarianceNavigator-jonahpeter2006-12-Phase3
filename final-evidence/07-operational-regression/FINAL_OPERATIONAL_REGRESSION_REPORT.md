# FINAL OPERATIONAL REGRESSION REPORT

## 1. Purpose

This report records the Post #6 operational regression evidence for the existing Budget vs Actual Variance Navigator application. The objective is to confirm that the established operational dashboard and its existing backend service remain available without expanding the approved application scope.

## 2. Regression Scope

The regression scope covers:
- Existing operational dashboard availability.
- Existing backend health and API availability.
- Separation between operational budget data and the Phase 3 canonical intelligence dataset.
- Preservation of the existing operational application alongside the Data Intelligence experience.

No operational dashboard redesign or new business functionality is introduced by this report.

## 3. Historical Browser Regression Evidence

The existing Post #4 operational and Data Intelligence regression record documented a Selenium execution with 11 checks passed and 0 failed on 7 November 2026.

That historical result is retained as prior evidence only. It is not represented as a fresh Post #6 browser execution.

The Post #6 Selenium attempt on this Windows machine was blocked before browser interaction because Windows Application Control prevented Selenium Manager from launching its driver executable. This is an environment-level blocker, not a confirmed application regression or a successful browser test.

## 4. Current Backend and Deployment Evidence

The current Phase 3 Render backend was checked using its public health and intelligence endpoints.

The backend health endpoint returned a ready status and the expected Phase 3 project identity. The intelligence health response reported:
- Dataset version: 1.0.0.
- Method version: 1.0.0.
- Result count: 64.
- Readiness status: ready.

The intelligence summary endpoint reported:
- Overall validation status: PASS.
- Passed checks: 1,325.
- Failed checks: 0.
- Warning checks: 0.

The current Phase 3 frontend URL also returned HTTP 200.

These checks confirm the availability of the queried public endpoints. They do not replace full browser-based operational regression.

## 5. Operational and Intelligence Data Boundaries

The application retains two distinct data responsibilities:

- Operational dashboard data: `backend/budget_data.csv`.
- Phase 3 canonical intelligence data: `data/canonical/intelligence_data.csv`.

The analytical dataset and its findings do not replace or silently rewrite the operational dashboard's source data.

## 6. Regression Limitations

- A fresh Post #6 Selenium browser run remains blocked by Windows Application Control.
- The historical Post #4 browser result is not a substitute for current browser verification.
- The current public HTTP checks establish endpoint availability, not complete visual, interaction, accessibility, or mobile acceptance.
- Repository-wide frontend lint has previously reported 12 issues in the operational dashboard file `frontend/src/app/page.tsx`; these were not broadly refactored as part of Post #6.
- No claim is made that every operational workflow or failure scenario has been exhaustively retested.

## 7. Conclusion

**PASS WITH DOCUMENTED LIMITATIONS** for the current public endpoint checks and previously recorded operational regression evidence.

The current Phase 3 backend and frontend endpoints responded successfully, and the backend reported the expected intelligence readiness and validation summary.

Fresh browser-based regression remains outstanding because the local browser-driver execution was blocked before interacting with the application. This report does not certify complete operational UI regression or the overall Phase 3 release.

## Post-Correction Local Browser Regression Addendum — 2026-11-15

A subsequent local browser run was completed using Chrome 157.0.8103.78 and matching ChromeDriver 157.0.8103.78.

Results:
- Assistant browser regression: 4 passed, 0 failed.
- Filter and responsive checks: 9 passed, 0 failed.
- Exact mobile/tablet viewport checks: 4 passed, 0 failed.
- Total local browser checks: 17 passed, 0 failed.

The local assistant correction was tested locally only. It has not been committed, pushed, or deployed. Public Render remains on commit daa7f61.

Public post-correction browser acceptance remains **NOT PERFORMED**. The earlier Selenium Manager attempt blocked by Windows Application Control is retained as a historical environment limitation. These local results do not establish public deployment browser acceptance or complete Phase 3 certification.

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
