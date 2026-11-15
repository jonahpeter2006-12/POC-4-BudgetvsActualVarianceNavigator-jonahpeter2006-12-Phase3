# Phase 3 Final Evidence Package

## Purpose

This folder contains selected evidence records for the PoC-4 Phase 3 Post #6 release review.

## Analytical evidence

The `analytical/` directory contains copies of the original JSON outputs from `data-science/outputs/`.

These records preserve their original generated timestamps and validation results. The included analytical records have generated timestamps spanning 2026-11-04 through 2026-11-07.

The combined validation record reports:
- 1,325 checks passed
- 0 failed checks
- 0 warnings
- 1,230 analytical checks
- 95 reconciliation checks

The sensitivity assessment is reported separately and is not included in the combined validation total.

## Browser automation evidence

`browser-automation/post6-selenium-attempt-2026-11-14.json` records the Post #6 Selenium attempt against the current Phase 3 Render URLs.

The attempt did not reach browser startup because Selenium could not obtain ChromeDriver. Windows Application Control blocked Selenium Manager. The recorded result is a blocked execution attempt, not a passing browser test.

## Automated test report

`FINAL_AUTOMATED_TEST_REPORT.md` records the verified local Python tests, Gemini tests, Python compilation, frontend build, targeted lint, Docker build, local runtime checks, and their limitations.

## Evidence limitations

- Local post-correction browser screenshots are included. A public Render post-correction browser screenshot is not yet available.
- Historical Post #4 screenshots and test results are not represented as Post #6 evidence.
- Gemini Mode B was validated locally but is not deployed or configured on the public Render service.
- Clean-clone validation was executed: 24 tests passed; compilation, reproducibility, and frontend build passed. The clean-clone Docker image build was blocked because the Docker Desktop Linux engine was unavailable.
- Public Render post-correction browser UAT remains outstanding; local acceptance is recorded separately above.
- This evidence package does not establish final Phase 3 certification or reviewer approval.

## Post-Correction Local Browser Acceptance — 2026-11-15

`browser-automation/post6-local-browser-acceptance-2026-11-15.json` records successful local Selenium checks performed after the targeted assistant correction.

Results:
- Assistant browser regression: 4 passed, 0 failed.
- Dashboard filter and responsive checks: 9 passed, 0 failed.
- Exact mobile and tablet viewport checks: 4 passed, 0 failed.
- Total: 17 passed, 0 failed.

The two screenshots are:
- `browser-automation/post6-local-dashboard-2026-11-15.png`
- `browser-automation/post6-local-assistant-regression-2026-11-15.png`

This is local acceptance evidence only. It does not establish that the correction is deployed to Render or that public post-correction browser acceptance has passed.

The earlier blocked public Selenium attempt dated 2026-11-14 remains preserved as a separate historical record.

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
