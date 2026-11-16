# PHASE 3 FINAL UAT

## 1. Purpose

This report consolidates the available Post #6 user-acceptance evidence for the Phase 3 Budget vs Actual Variance Navigator. It records verified behavior and identifies acceptance activities that remain incomplete.

## 2. UAT Scope

The UAT scope covers:
- Public application and backend availability.
- Phase 3 Data Intelligence API readiness.
- Analytical summary and finding availability.
- Representative supported and unsupported assistant questions.
- Local build, test, compilation, and Docker runtime checks.
- Browser-based validation status.

## 3. Public Application Availability

The correct public Render frontend was checked and returned HTTP 200.

The correct Phase 3 backend was checked and exposed the expected operational and Phase 3 API routes through its OpenAPI document.

The backend health endpoint returned a healthy response. The intelligence health endpoint reported ready status, dataset version 1.0.0, method version 1.0.0, and 64 findings.

## 4. Analytical Acceptance Evidence

The public intelligence summary reported:
- Overall validation status: PASS.
- Passed checks: 1,325.
- Failed checks: 0.
- Warning checks: 0.

The approved Track A output contains 64 findings: 16 overall comparisons and 48 monthly findings.

The analytical scope remains descriptive and evidence-based. The canonical dataset contains synthetic observations and 18 independent source observations. Monthly findings with insufficient evidence remain explicitly limited.

## 5. Assistant Acceptance Evidence

A representative supported public question, "Why is Cost Centre CC-101 above budget?", returned a SUPPORTED response with:
- Actual: $149,500.
- Budget: $135,000.
- Variance: $14,500.
- Variance percentage: approximately 10.74%.
- Finding identifier and source-record evidence.
- The synthetic-data and limited-source caveats.

A representative unsupported request to predict next year's spending and identify fraud risks returned OUT_OF_SCOPE and did not generate unsupported financial conclusions.

The public deployment remains deterministic Mode A. Gemini Mode B has passed local implementation tests but has not been deployed or configured on Render.

## 6. Local Acceptance Evidence

The following local checks were recorded as successful:
- Full Python suite: 24 passed, 0 failed, with one non-blocking AnyIO pytest-plugin deprecation warning.
- Dedicated Gemini tests: 8 passed, 0 failed, with one non-blocking warning.
- Backend and test Python compilation: passed using `python -m compileall -q backend tests`.
- Frontend production build and TypeScript validation: passed.
- Targeted ESLint check for the Data Intelligence page: passed.
- Backend Docker image build and module import: passed.
- Local Docker health, intelligence summary, and representative assistant checks: passed.
- Local Gemini API diagnostic and supported-question explanation: passed.

These checks validate the local Post #6 implementation, not the currently deployed public Gemini capability.

## 7. Browser and Interaction Acceptance

A fresh Post #6 Selenium run was attempted but was blocked before browser startup because Windows Application Control prevented Selenium Manager from launching.

Consequently:
- Fresh Post #6 browser interaction testing is not complete.
- Fresh visual and responsive browser acceptance is not established.
- Historical Post #4 Selenium results are retained as historical evidence only and are not treated as Post #6 UAT.

## 8. UAT Limitations and Outstanding Acceptance

The following items remain outstanding:
- Successful fresh browser-based UAT.
- Public deployment and validation of Gemini Mode B, if it remains part of the intended Post #6 implementation.
- Clean-clone validation.
- Final release evidence collection and manifest completion.
- Final reviewer approval.

The dataset remains synthetic and limited to 18 independent source observations. The forecast measure is illustrative, not predictive. The assistant is limited to five approved question types.

## 9. UAT Conclusion

**PARTIAL ACCEPTANCE â€” PASS WITH DOCUMENTED LIMITATIONS.**

The verified public API behavior, analytical validation summary, representative deterministic assistant responses, and local build and test evidence support the tested portions of Phase 3.

At this earlier UAT checkpoint, complete Post #6 UAT was not established because fresh browser-based acceptance, clean-clone validation, final release evidence, and reviewer approval remained outstanding. The later public browser acceptance and evidence-pack reconciliation are recorded in the dated addendum below. Clean-clone limitations and reviewer certification remain outstanding.

This report does not declare Phase 3 complete or certified.

## Updated Local and Clean-Clone Acceptance Record â€” 2026-11-15

The following later evidence supplements the earlier UAT record:

- Clean-clone validation at commit `daa7f610882862157287e350d8850499cb8ca44f` completed with documented limitations: 24 targeted tests passed; compilation, reproducibility, frontend dependency installation, and production build passed. The clean-clone Docker build was BLOCKED because the Docker Desktop Linux engine was unavailable.
- Following a subsequent local assistant correction, 27 targeted Python tests passed (19 assistant API tests and 8 Gemini explainer tests).
- Local browser acceptance after that correction passed 17 checks: 4 assistant regression, 9 filter/responsive, and 4 viewport checks.
- Historical checkpoint: the local correction had not yet been committed, pushed, or deployed, and public Render was recorded on commit `daa7f61`. This was superseded by the later correction push and public acceptance recorded below.
- Historical checkpoint: public post-correction browser acceptance had not yet been performed. This was superseded by the public Selenium acceptance on 15 November 2026, which passed 19/19 checks.
- Public Gemini Mode B behavior remains unverified; the public deployment uses the deterministic assistant path.
- At that earlier checkpoint, final evidence-pack completion and Repomix generation remained outstanding. Both were subsequently completed and validated for GitHub master commit `029b6bb`. reviewer acceptance had not yet been recorded at that historical checkpoint.

**Updated UAT status: PARTIAL ACCEPTANCE â€” PASS WITH DOCUMENTED LIMITATIONS. Phase 3 certification is not established.**

## Public Post #6 Acceptance Addendum â€” 2026-11-15

A fresh public Render browser and API acceptance run completed on 2026-11-15.

**Result: PASS â€” 19 checks passed, 0 failed.**

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

## Final status reconciliation â€” 15 November 2026

This reconciliation supersedes earlier status snapshots in this document wherever they describe the assistant correction as unpublished, the public browser acceptance as not performed, or the public backend as remaining on commit `daa7f61`. Those statements accurately describe earlier checkpoints but are no longer the current release status.

### Verified current results

- The assistant scope correction is committed and pushed to GitHub `master` at commit `3610659d87831639ee2fc3b17d8ce66beb3fdcb1`.
- The Render dashboard independently confirmed the backend service `poc4-budget-phase3-backend` Live on commit `3610659`.
- Public assistant API regression: 4/4 checks passed. The supported comparison question returned `SUPPORTED`; the three predictive/future-projection questions returned `OUT_OF_SCOPE` with zero evidence.
- Public Selenium acceptance on 15 November 2026: **19 passed, 0 failed**. This included backend and intelligence health, summary, assistant API behavior, desktop dashboard rendering, Data Intelligence content, and both pages at a 390 Ã— 844 mobile viewport.
- The public acceptance report is `final-evidence/browser-automation/post6-public-final-acceptance-20261115-142307.json`. The corresponding final dashboard and Data Intelligence screenshots are stored in the official evidence folders.
- The official evidence structure contains all 15 required folders and 73 files. The latest structural and evidence-copy consistency audits passed, with zero report-copy failures and zero required-evidence-copy failures.
- The correction's local targeted tests passed 27/27. Python compilation passed. Earlier clean-clone checks recorded 24 targeted tests passing, with the limitations below.

### Remaining limitations and certification status

- Clean-clone Docker build remains **BLOCKED** because the Docker Desktop Linux engine was unavailable during that validation.
- Full default pytest collection in the separate clean-clone environment was **BLOCKED** by missing `requests` for two legacy test modules; those modules were not executed in that environment.
- Public Gemini Mode B positive-path and staging fallback behavior have been operationally validated for the tested scenarios. Formal reviewer certification remains outstanding.
- Production Render frontend and backend services were confirmed Live on application commit `954a6ed` (15 November 2026). The isolated staging fallback service was deployed from repository commit `79feed9`.
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The final Repomix snapshot was generated from GitHub master commit `029b6bb` and XML-validated on 15 November 2026.
- Historical checkpoint: reviewer acceptance and release-tag publication had not yet been recorded when this status was written. Subsequent reviewer acceptance and the published release tag are documented in the 16 November 2026 reconciliation.

**Current status: Project development ACCEPTED AND COMPLETE; professional demonstration ACCEPTED; source release tag v2.0.0-phase3-final points to commit 3f3f751814ba6b6b8947bf4c14c8846855a53d92; formal Phase 3 release certification PENDING separate governance approval.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.

## Public Gemini Mode B Positive-Path UAT â€” 15 November 2026

**Result: PASS â€” tested public positive path.**

The deployed Render assistant successfully processed the supported question "Compare cost centres" and returned:

- `status`: `SUPPORTED`
- `intent`: `cost_centre_variance_comparison`
- `explanation_status`: `generated`
- `explanation_provider`: `gemini`
- `metadata.validation_status`: `PASS`
- Six cost-centre findings with deterministic evidence references.

The response retained the approved Track A comparison, source and canonical record references, and the documented limitations. The Gemini explanation agreed with the deterministic values.

The captured response is stored at `final-evidence/09-assistant-or-skip/post6-public-gemini-mode-b-acceptance-20261115.json`.

**Not established by this test:** Public provider-failure or missing-key fallback behavior. Earlier local fallback tests remain separate evidence and are not represented as a new public test.

This positive-path result does not replace reviewer approval. Phase 3 remains `DRAFT â€” NOT CERTIFIED` pending formal review.

## Public Gemini Mode B Fallback UAT — 15 November 2026

**Result: PASS — tested public staging fallback paths.**

The isolated Render staging service was tested with two configurations:

1. Gemini API key absent: the assistant returned `SUPPORTED` with `explanation_status: disabled`.
2. Deliberately invalid staging-only Gemini API key: the assistant returned `SUPPORTED` with `explanation_status: fallback`.

For the provider-failure test:

- Intent: `cost_centre_variance_comparison`
- Deterministic answer: present
- Gemini explanation: absent, as expected during fallback
- Evidence references: preserved, containing six findings
- Metadata validation: `PASS`
- Assertions: 6 passed, 0 failed
- Staging deployment source: `79feed9`
- Production environment: not modified

The provider-failure response is preserved at `final-evidence/09-assistant-or-skip/post6-public-gemini-provider-failure-fallback-20261115.json`.

The missing-key test was separately observed on the same staging service before the invalid-key configuration was applied.

These results complement the production Gemini positive-path UAT. They do not constitute reviewer approval or Phase 3 certification.

**Phase 3 remains DRAFT — NOT CERTIFIED pending formal review.**

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
