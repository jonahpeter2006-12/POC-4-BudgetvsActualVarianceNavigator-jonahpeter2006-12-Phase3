# Intelligence Integration Mapping

## Purpose
Map the approved Post #3 outputs to the Post #4 backend API and frontend page.

## Source-to-API mapping

| Source artifact | Purpose | Proposed API use |
|---|---|---|
| intelligence_results.json | Individual findings and evidence | Results list and result detail |
| intelligence_summary.json | Analytical question, key findings, summary, limitations | Summary endpoint |
| validation_metrics.json | Validation status, counts, versions | Metadata and health |
| weak_case_review.json | Insufficient-evidence cases and weak-case interpretation | Results context and limitations |
| sensitivity_review.json | Leave-one-source-out sensitivity evidence | Summary and methodology |
| baseline_reconciliation.json | Baseline and aggregation reconciliation evidence | Validation context |

## Finding fields to preserve
- result_id
- result_type
- record_id
- entity_id
- group_key
- period_start
- period_end
- metric_name
- result_value
- result_unit
- result_category
- priority_rank
- finding
- evidence
- method_version
- data_version
- generated_at
- quality_status
- limitation

## Evidence fields to preserve
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

## Result types
Overall comparisons:
- cost_centre_comparison
- department_comparison
- expenditure_category_comparison

Monthly descriptive findings:
- monthly_cost_centre_comparison
- monthly_department_comparison
- monthly_expenditure_category_comparison

## Quality status handling
Use the actual source values:
- validated_with_limitations
- insufficient_evidence

Do not silently convert these values to other labels or imply that insufficient-evidence findings are validated overall comparisons.

## Classification
Variance = Actual minus Budget.
- Positive variance: overspending.
- Negative variance: underspending.
- Zero variance: on budget.

Absolute variance and percentage variance must be displayed separately.

## Sensitivity integration
The single leave-one-source-observation-out assessment found:
- 12 of 16 overall ranks changed.
- 3 overall variances changed.
- 2 quality statuses changed.
- 2 comparisons became insufficient evidence.

This is a single-scenario sensitivity assessment, not proof of statistical robustness.

## Reconciliation integration
The separate baseline and aggregation reconciliation contains 95 checks, all passed in the recorded execution. The report must be read from its artifact; the UI must not manufacture validation results.

## Prohibited transformations
- No frontend financial recalculation.
- No frontend ranking or re-ranking.
- No hardcoded findings.
- No browser-side CSV loading.
- No LLM-generated financial values.
- No mixing monthly findings into overall rankings.
- No treating committed or forecast values as actual variance.

## Version alignment
The API must preserve and expose project, track, contract, dataset, and method metadata. Incompatible or missing artifacts must produce a clear unavailable or stale response rather than a misleading successful response.
