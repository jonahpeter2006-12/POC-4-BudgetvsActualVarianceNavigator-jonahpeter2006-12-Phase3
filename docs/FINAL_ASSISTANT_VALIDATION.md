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
