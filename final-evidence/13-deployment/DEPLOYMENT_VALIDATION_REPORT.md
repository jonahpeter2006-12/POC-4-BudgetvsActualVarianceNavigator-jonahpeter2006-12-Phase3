# DEPLOYMENT VALIDATION REPORT

## 1. Purpose

This report records public deployment verification for Phase 3 Post #6.

## 2. Public Deployment References

- Frontend: https://poc4-budget-phase3-frontend.onrender.com
- Backend: https://poc4-budget-phase3-backend.onrender.com

The frontend and backend are separate Render web services.

## 3. Render Deployment Verification

Both Render dashboards were inspected and showed the following:

| Service | Commit | Status |
|---|---|---|
| `poc4-budget-phase3-frontend` | `daa7f61` | Live |
| `poc4-budget-phase3-backend` | `daa7f61` | Live |

Deployment commit message:

`Complete Phase 3 Post 6 assistant integration and release evidence`

The frontend deployment completed in 57.9 seconds. The backend deployment completed in 40.9 seconds.

Both services are deployed from the Post #6 commit on branch `master`.

Full commit SHA:

`daa7f610882862157287e350d8850499cb8ca44f`

## 4. Public Availability and API Checks

The following checks were performed against the Phase 3 public services:

| Check | Result |
|---|---|
| Frontend HTTP response | HTTP 200 |
| Backend `/api/health` | Healthy |
| Backend `/api/intelligence/health` | ready |
| Intelligence result count | 64 |
| Dataset version | 1.0.0 |
| Method version | 1.0.0 |
| Intelligence summary validation | PASS |
| Total validation checks | 1,325 |
| Passed checks | 1,325 |
| Failed checks | 0 |
| Warning checks | 0 |
| Analytical validation | 1,230/1,230 passed |
| Reconciliation validation | 95/95 passed |
| Aggregation reconciliation | 12/12 passed |
| Baseline comparison | 83/83 passed |
| Reproducibility assessment | PASS |

The public analytical summary reported canonical totals:
- Budget: 601,000
- Actual: 633,000
- Committed: 42,500
- Forecast: 660,500

The public reproducibility result reported identical repeat runs using the fixed timestamp and SHA-256 evidence recorded by the API.

These checks establish public service availability and analytical validation at the time of testing. They do not establish complete browser-based acceptance.

## 5. Assistant and Gemini Configuration

The Post #6 backend code is deployed.

Public Gemini Mode B provider behavior and private Render environment configuration have not been independently validated as part of this deployment check. No API key is included in this report.

If Gemini Mode B is enabled, `GEMINI_API_KEY` and `GEMINI_MODEL` must be configured privately in the backend service environment. The API key must never be committed or placed in frontend variables.

Deterministic financial values, evidence, and fallback behavior must remain authoritative.

## 6. Deployment Limitations

- Selenium browser validation remains blocked by Windows Application Control before browser startup.
- Public HTTP and API checks do not prove complete visual, interaction, accessibility, or responsive behavior.
- Gemini provider behavior in the public deployment is not certified by these checks.
- Reviewer approval remains pending.

## 7. Conclusion

**POST #6 PUBLIC DEPLOYMENT: VERIFIED.**

Both the Phase 3 frontend and backend Render services were confirmed Live on commit `daa7f61`.

**PUBLIC API AND ANALYTICAL VALIDATION: PASS.**

The documented browser and Gemini-provider limitations remain open. This report does not independently certify the complete Phase 3 release.

## 8. Post-Correction Local Browser Acceptance — 2026-11-15

A targeted local correction was applied to the deterministic assistant intent classifier. Predictive and future-projection questions that are outside the approved comparative-intelligence scope are now rejected as `OUT_OF_SCOPE`.

The correction was validated locally in the original project working directory.

### Automated regression results

| Validation | Result |
|---|---|
| Assistant API and Gemini explainer tests | PASS — 27 passed, 0 failed |
| Python compilation (`backend`, `tests`) | PASS |
| `git diff --check` | PASS |

The 27-test result comprises 19 assistant API tests and 8 Gemini explainer tests. The three new parameterized predictive-question cases passed.

### Local Selenium browser acceptance

| Browser validation | Result |
|---|---|
| Dashboard and Data Intelligence page loading | PASS |
| Supported comparative question | PASS — `SUPPORTED` |
| Predictive question | PASS — `OUT_OF_SCOPE` |
| Assistant browser regression checks | 4 passed |
| Dashboard filters and responsive checks | 9 passed |
| Exact viewport responsive checks | 4 passed |
| Total recorded browser checks | 17 passed, 0 failed |

Exact responsive viewport checks:
- Dashboard: mobile 390 × 844 and tablet 768 × 1024.
- Data Intelligence: mobile 390 × 844 and tablet 768 × 1024.
- No horizontal overflow was detected at these four tested dimensions.

### Public deployment distinction

The local correction has not been committed, pushed, or deployed to Render. The public frontend and backend remain deployed on commit `daa7f61`.

The earlier public browser test identified the predictive-question classification issue before this local correction. No post-correction public Render browser acceptance is claimed.

The earlier Windows Application Control limitation concerned a separate clean-clone browser attempt. It does not invalidate the subsequent successful local Selenium checks.

These results establish targeted local regression and browser acceptance only. They do not establish public deployment of the correction or complete Phase 3 certification.

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
- Final Repomix generation and reviewer approval remain outstanding.
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
- The Render backend deployment commit is confirmed as `3610659`. The exact active frontend deployment commit has not been independently confirmed in the Render dashboard evidence reviewed for this reconciliation.
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The final Repomix has not yet been regenerated from the finalized release state.
- Reviewer approval and the required certification decision have not been received. The release tag has not been created.

**Current release status: NOT CERTIFIED — reviewer approval and final release packaging remain outstanding.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.
