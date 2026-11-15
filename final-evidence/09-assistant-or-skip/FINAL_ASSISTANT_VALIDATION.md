# FINAL ASSISTANT VALIDATION REPORT

## 1. Purpose

This report records the Post #6 validation evidence for the deterministic assistant and the optional Gemini explanation layer.

It distinguishes local implementation tests from checks performed against the currently deployed public service.

## 2. Approved Assistant Scope

The assistant retains the five approved question types:
1. Cost-centre variance comparison.
2. Department comparison.
3. Expenditure-category lookup.
4. Finding-evidence lookup.
5. Monthly insufficient-evidence lookup.

Unsupported questions must return an out-of-scope response without generating unsupported financial values or conclusions.

## 3. Deterministic Assistant Validation

The public Render deployment was tested using:

Supported question:
`Why is Cost Centre CC-101 above budget?`

Recorded response:
- Status: SUPPORTED.
- Intent: finding_evidence_lookup.
- Actual: 149,500.
- Budget: 135,000.
- Variance: 14,500.
- Aggregate variance percentage: approximately 10.74%.
- Evidence result: `track-a-cost_centre_comparison-20260101-cc-101`.
- Independent source observations: 3.
- Canonical evidence records: 12.
- Evidence quality: validated_with_limitations.

The response retained the synthetic-data and limited-source caveats.

Unsupported question:
`Predict next year's spending and identify fraud risks.`

Recorded response:
- Status: OUT_OF_SCOPE.
- No unsupported financial values or conclusions generated.

These checks establish the recorded behavior of the deployed deterministic Mode A assistant.

## 4. Local Gemini Mode B Validation

The local Post #6 implementation adds an optional Gemini explanation layer.

The deterministic assistant remains authoritative for:
- Supported intent classification.
- Financial values.
- Finding selection.
- Evidence and source identifiers.
- Validation metadata.
- Limitations.

Gemini is used only to explain an already-supported deterministic response.

Recorded local checks:
- Live Gemini API diagnostic: HTTP 200.
- Supported CC-101 question: Gemini explanation returned.
- Missing API key: deterministic fallback.
- Provider failure: deterministic fallback.
- Unsupported numeric claim: explanation rejected.
- Contradictory budget direction: explanation rejected.
- Unsupported question: Gemini not called.

Dedicated Gemini tests: 8 passed, 0 failed, with one non-blocking warning.

Full Python test suite: 24 passed, 0 failed, with one non-blocking AnyIO pytest-plugin deprecation warning.
The response validation uses bounded numeric and direction checks. These checks are not comprehensive semantic verification or complete prompt-injection protection.

## 5. Deployment Boundary

The public Render backend was last verified at commit `08327d7`.

That deployment contains the deterministic Mode A assistant. It does not contain the local Post #6 Gemini implementation and has not been configured with Gemini environment variables.

Therefore:
- Public deterministic assistant checks: recorded as passed.
- Local Gemini implementation tests: recorded as passed.
- Public Gemini deployment and browser validation: not completed.

No API key is included in this report or in source-controlled configuration.

## 6. Security and Data Boundaries

- Gemini API credentials must remain backend-side and private.
- Gemini must not create or modify financial values.
- Unsupported questions must remain out of scope.
- Committed and Forecast values must not be presented as Actual.
- Synthetic-data and insufficient-evidence limitations must be preserved.
- Provider failure or missing configuration must not prevent deterministic fallback.

The recorded checks do not constitute a full security audit.

## 7. Final Assessment

**DETERMINISTIC ASSISTANT: RECORDED VALIDATION PASS WITH DOCUMENTED LIMITATIONS.**

**LOCAL GEMINI MODE B: RECORDED TEST PASS WITH DOCUMENTED LIMITATIONS.**

**PUBLIC GEMINI DEPLOYMENT: NOT VALIDATED.**

**POST #6 ASSISTANT CERTIFICATION: NOT YET ESTABLISHED.**

Fresh browser-based acceptance, final release deployment, and reviewer approval remain outstanding.

## Post-Correction Regression Addendum — 2026-11-15

### Correction

The deterministic assistant classifier now explicitly rejects predictive and future-projection questions that are outside the approved Track A comparative-intelligence scope.

The correction returns no approved intent for these question patterns, allowing the existing assistant response handling to return `OUT_OF_SCOPE`.

### Automated tests

The targeted test command:

`pytest -v tests/test_assistant_api.py tests/test_gemini_explainer.py`

Result: **27 passed, 0 failed**.

The assistant API test module contributed 19 passing tests, including three parameterized predictive-question cases:
- Predict next quarter's spending for each cost centre.
- Forecast next quarter spending for cost centers.
- Project future spending for CC-101.

All three returned HTTP 200 with status `OUT_OF_SCOPE`.

Python compilation and `git diff --check` also passed.

### Local browser regression

Local Selenium checks after the correction recorded:
- Dashboard and Data Intelligence page loading: passed.
- Approved comparative question: returned `SUPPORTED`.
- Predictive question: returned `OUT_OF_SCOPE`.
- Assistant browser regression: 4 passed.
- Dashboard filter and responsive checks: 9 passed.
- Exact viewport checks: 4 passed.
- Total: **17 passed, 0 failed**.

The exact viewport checks covered both pages at 390 × 844 and 768 × 1024, with no horizontal overflow.

### Scope and deployment limitation

These results were obtained against the local application and local corrected source. The correction has not been committed, pushed, or deployed to the public Render services. Public post-correction assistant behavior therefore remains unverified.

The local regression result does not certify Gemini provider behavior in the public deployment, clean-clone Docker acceptance, or the complete Phase 3 release.

**ASSISTANT CORRECTION: LOCALLY VALIDATED. PUBLIC DEPLOYMENT: PENDING.**

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
