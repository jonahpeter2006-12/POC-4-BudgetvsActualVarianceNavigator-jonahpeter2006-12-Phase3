# INTELLIGENCE OUTPUT CONTRACT

## 1. Contract Information

- Project: Budget vs Actual Variance Navigator
- PoC: 4
- Phase: Phase 3 — Post #3
- Approved Track: Track A — Comparative Intelligence
- Contract Version: 1.0.0
- Method Version: 1.0.0
- Dataset Version: 1.0.0

## 2. Purpose

This contract defines the machine-readable outputs produced by the approved Track A analytical method.

Outputs must be reproducible, traceable to canonical records, versioned and suitable for future Data Intelligence integration after the required approval.

## 3. Output Files

The analytical workflow must produce:

- data-science/outputs/intelligence_results.json
- data-science/outputs/intelligence_summary.json
- data-science/outputs/validation_metrics.json
- data-science/outputs/weak_case_review.json

## 4. Intelligence Results Structure

The intelligence results file must contain:

- project_id
- project_title
- approved_track
- contract_version
- dataset_version
- method_version
- generated_at
- result_count
- results

The results field must be an array of structured analytical findings.

## 5. Required Finding Fields

Every finding must contain the following fields:

| Field | Type | Purpose |
|---|---|---|
| result_id | string | Stable unique finding identifier |
| result_type | string | Type of descriptive comparison |
| record_id | string or null | Single canonical record reference, when applicable |
| entity_id | string or null | Cost-centre identifier, when applicable |
| group_key | string | Group identifier used for comparison |
| period_start | string | Reporting period start |
| period_end | string | Reporting period end |
| metric_name | string | Primary analytical metric |
| result_value | number or null | Calculated result |
| result_unit | string | Currency, percentage or count unit |
| result_category | string | Overspend, underspend or on-budget classification |
| priority_rank | integer or null | Deterministic comparison rank |
| finding | string | Plain-language descriptive finding |
| evidence | object | Supporting canonical evidence |
| method_version | string | Analytical method version |
| data_version | string | Canonical dataset version |
| generated_at | string | UTC generation timestamp |
| quality_status | string | Validation and evidence status |
| limitation | array | Relevant limitations and qualifications |

Fields that do not apply must remain present with null values or an empty array/object as appropriate. They must not be silently omitted.

## 6. Finding Types

The following descriptive comparison types are permitted:

- cost_centre_comparison
- department_comparison
- expenditure_category_comparison
- monthly_cost_centre_comparison
- monthly_department_comparison
- monthly_expenditure_category_comparison

No predictive, anomaly or financial-risk result types are permitted.

## 7. Evidence Object

Each finding must preserve enough evidence for independent recalculation.

The evidence object must include:

- budget_total
- actual_total
- variance_amount
- variance_percentage
- committed_total
- forecast_total
- independent_source_count
- canonical_record_ids
- source_record_ids
- reporting_period
- currency_unit
- aggregation_method

Committed and forecast totals are contextual measurements only. They must not be included in the Budget-versus-Actual variance calculation.

Canonical record identifiers and source observation identifiers must be traceable to the authoritative CSV.

## 8. Variance Interpretation

The sign convention is:

Variance = Actual - Budget

Variance Percentage = (Variance / Budget) * 100

Classification:

- overspend: positive variance
- underspend: negative variance
- on_budget: zero variance

When aggregate Budget is zero, variance percentage must be null and the limitation must explain why it is unavailable.

## 9. Quality Status

Permitted quality status values:

- validated
- validated_with_limitations
- insufficient_evidence
- excluded

A finding with fewer than three independent source observations must not be represented as a fully supported overall group ranking.

Monthly subgroup results must disclose their actual independent source count and remain descriptive.

## 10. Intelligence Summary Structure

The summary file must contain:

- project_id
- project_title
- data_version
- method_version
- approved_track
- primary_analytical_question
- decision_supported
- result_count
- key_findings
- priority_items
- validation_result
- important_limitations
- generated_at

The summary must be derived from the validated intelligence results. It must not introduce manually invented figures or unsupported conclusions.

## 11. Validation Metrics Structure

The validation metrics file must record:

- validation_version
- dataset_version
- method_version
- generated_at
- overall_status
- checks
- passed_count
- failed_count
- warning_count
- independent_recalculation
- aggregation_reconciliation
- reproducibility
- baseline_comparison

Every check must include a check identifier, description, status and evidence or explanation.

## 12. Weak Case Review Structure

The weak case review must document:

- review_version
- dataset_version
- method_version
- generated_at
- minimum_group_size
- small_group_cases
- extreme_value_cases
- missing_group_effects
- ranking_stability
- sensitivity_review
- excluded_cases
- interpretation

The review must identify weak evidence and limitations rather than conceal them.

## 13. Determinism and Traceability

- Findings must have deterministic identifiers.
- Group ordering and tie handling must follow the analytical method report.
- Evidence identifiers must originate from the canonical dataset.
- Numeric outputs must be finite JSON numbers or null.
- Timestamps must use UTC ISO 8601 format.
- Dataset and method versions must be present.
- The same input and method configuration must produce the same analytical values and ordering.

Execution timestamps may differ between runs.

## 14. Output Integrity

The export process must verify:

- Valid JSON syntax.
- Required top-level fields.
- Required finding fields.
- Correct data and method versions.
- Evidence references.
- Valid result types and quality statuses.
- Numeric values are finite.
- No unsupported analytical result types.
- No fabricated or manually entered financial values.

A failed contract validation must prevent the output from being marked approved.

## 15. Limitations

- The dataset contains only 18 independent synthetic source observations.
- The 72 canonical records represent four measurements per observation, not 72 independent transactions.
- Monthly coverage is limited to January–March 2026.
- Forecast values are illustrative and not validated predictive outputs.
- Findings are descriptive and do not establish real-world financial accuracy.
- Small-group comparisons must be interpreted cautiously.

## 16. Approval Boundary

These outputs are analytical feeder artifacts for Phase 3 Post #3.

Their creation does not authorize a new dashboard, production API, Data Intelligence page integration or subsequent phase implementation.

The final analytical track outcome must be one of:

- ANALYTICAL TRACK OUTPUT APPROVED
- ANALYTICAL TRACK CHANGES REQUIRED
- APPROVED TRACK NOT VIABLE
