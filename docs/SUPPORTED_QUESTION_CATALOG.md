# Supported Question Catalog

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5: Grounded Natural-Language Data Assistant
- Assistant Mode: Mode A - Deterministic Guided Assistant
- LLM: Not used
- Catalog Status: Implemented; selected API and browser tests passed; final acceptance pending.

## 1. Purpose

This catalogue defines the business questions the assistant is permitted to answer using approved Track A intelligence findings.

Each supported question maps to a predefined deterministic intent, validated parameters, and approved findings from the verified intelligence artifact bundle.

The assistant must not invent findings or independently calculate new analytical results.

## 2. Supported Questions

### SQ-01 - Cost Centre Variance Comparison

**Example question:** Which cost centres have the largest approved variances?

- Intent: `cost_centre_variance_comparison`
- Required parameters: None.
- Data source: `cost_centre_comparison`
- Retrieval: Select approved cost-centre comparison findings from the verified artifact bundle.
- Response: Show cost-centre identifiers, approved financial values, variance categories, and existing priority ranks.
- Evidence: Budget, actual, variance, independent source count, source references, quality status, reporting period, and limitations.
- Restriction: Preserve approved priority ranks. Do not calculate or modify rankings.

### SQ-02 - Department Comparison

**Example question:** How do Engineering and Sales compare?

- Intent: `department_comparison`
- Required parameters: Exactly two valid department names.
- Data source: `department_comparison`
- Retrieval: Select approved department findings and match each requested name against its exact `group_key`.
- Response: Show the approved budget, actual, and variance values for both departments.
- Evidence: Supporting source references, independent source counts, quality status, reporting period, and limitations.
- Restriction: Do not create a new ranking or infer reasons for differences.
- Missing department names produce `MISSING_PARAMETER`.
- More than two department names produce `AMBIGUOUS`.

### SQ-03 - Expenditure Category Lookup

**Example question:** What is the approved variance for Cloud Infrastructure?

- Intent: `expenditure_category_lookup`
- Required parameter: One approved expenditure category name.
- Data source: `expenditure_category_comparison`
- Retrieval: Select approved findings and match the requested category against its exact `group_key`.
- Response: Show the matching category's approved financial values and variance.
- Evidence: Source references, independent source count, quality status, reporting period, and limitations.
- Restriction: Do not infer causes or make unsupported recommendations. Do not silently substitute an unknown category.

### SQ-04 - Finding Evidence Explanation

**Example question:** Show evidence for CC-101.

- Intent: `finding_evidence_lookup`
- Required parameter: An exact finding identifier or an unambiguous cost-centre identifier.
- Data source: Approved findings in the verified artifact bundle.
- Retrieval: Resolve the matching finding by its exact result ID or exact approved cost-centre `entity_id` or `group_key`.
- Response: Explain the recorded finding using its existing approved evidence and financial values.
- Evidence: Available budget, actual, variance amount, variance percentage, committed amount, forecast, independent source count, source and canonical record identifiers, and reporting period.
- Restriction: Explain what the data records. Do not claim an unsupported cause or treat correlation as causation.

### SQ-05 - Monthly Insufficient-Evidence Findings

**Example question:** Which monthly findings have insufficient evidence?

- Intent: `monthly_insufficient_evidence_lookup`
- Required parameters: None.
- Data source: The three approved monthly comparison result types:
  - `monthly_cost_centre_comparison`
  - `monthly_department_comparison`
  - `monthly_expenditure_category_comparison`
- Retrieval: Filter the verified artifact bundle for those result types and `quality_status = insufficient_evidence`.
- Response: Show matching monthly findings and their recorded evidence limitations.
- Response limit: Maximum 25 findings. Disclose the matching count and truncation when more findings are available.
- Evidence: Independent source count, source references, reporting period, quality status, and limitation text.
- Restriction: Monthly findings remain descriptive. They must not be presented as confirmed conclusions, overall rankings, or evidence of a sustained trend.
- Optional cost-centre and reporting-period filters are not part of the currently implemented question contract.

## 3. Missing and Ambiguous Questions

- If a required parameter is missing, return `MISSING_PARAMETER`.
- If more than two departments are requested, return `AMBIGUOUS`.
- If multiple category matches are identified, return `AMBIGUOUS`.
- Do not guess an entity or silently select an arbitrary result.
- Ask the user to clarify using the approved entities.
- Unknown entities must not be silently substituted.

## 4. Unsupported Questions

Return `OUT_OF_SCOPE` for requests involving:
- Predictions or unsupported forecasts.
- New risk scores or anomaly detection.
- New scenario calculations.
- Unsupported causal explanations.
- Population-level conclusions.
- Arbitrary SQL, Python, shell commands, or unrestricted data access.
- Unsupported question types outside the five approved intents.

Return `UNSAFE` when an implemented unsafe-request pattern identifies an attempt to bypass assistant restrictions or obtain secrets.

Pattern-based checks are limited and are not comprehensive protection against every possible malicious input.

## 5. Evidence and Quality Requirements

Supported responses preserve available approved information, including:
- Exact finding identifiers.
- Source and canonical record identifiers.
- Financial values from the approved finding.
- Independent source counts.
- Reporting period and comparison type.
- Original quality status and limitation text.
- Evidence excerpts.
- Available `contract_version`, `dataset_version`, and `method_version` metadata.

Evidence construction validates required fields and applies configured response limits.

The assistant does not independently recalculate financial values.

These controls do not establish that every natural-language statement is independently checked by a comprehensive factual-claim validator. Further grounding and adversarial testing remain part of final acceptance.

## 6. Response Limits

- Maximum question length: 500 characters.
- Maximum returned findings/key values: 25.
- Maximum evidence references: 10.
- Maximum evidence excerpt length: 300 characters.
- Maximum suggested follow-ups: 3.

## 7. Implementation and Verification Status

The five deterministic intents, parameter validation, verified-artifact retrieval, FastAPI endpoint, and Data Intelligence frontend integration have been implemented.

Selected verification completed:
- Automated assistant API tests: 15 passed, 0 failed.
- Backend intent and edge-case checks.
- Browser tests for all five supported question types.
- Browser checks for unsupported predictions and unsafe requests.
- Browser ambiguity check for a three-department comparison.
- Evidence, limitation, and truncation rendering checks.

Remaining work:
- Full public Render deployment verification.
- Authentication and public-data-boundary decision.
- Additional security and adversarial testing.
- Mobile and accessibility testing.
- Full regression and final evidence capture.
- Reviewer acceptance.

**Overall catalog status: IMPLEMENTED - SELECTED VERIFICATION PASSED - FINAL ACCEPTANCE PENDING.**

Reviewer approval has not yet been obtained.
