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

**PARTIAL ACCEPTANCE — PASS WITH DOCUMENTED LIMITATIONS.**

The verified public API behavior, analytical validation summary, representative deterministic assistant responses, and local build and test evidence support the tested portions of Phase 3.

Complete Post #6 UAT is not established because fresh browser-based acceptance, clean-clone validation, final release evidence, and reviewer approval remain outstanding.

This report does not declare Phase 3 complete or certified.
