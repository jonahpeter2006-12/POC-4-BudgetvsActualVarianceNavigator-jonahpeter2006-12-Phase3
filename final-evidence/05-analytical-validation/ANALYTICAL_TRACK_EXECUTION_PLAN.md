# ANALYTICAL TRACK EXECUTION PLAN

## 1. Project Information

- Project: Budget vs Actual Variance Navigator
- PoC: 4
- Phase: Phase 3 — Post #3
- Analytical Track: Track A — Comparative Intelligence
- Approval Status: Approved primary analytical track
- Plan Version: 1.0.0
- Planned Method Version: 1.0.0
- Dataset Path: data/canonical/intelligence_data.csv
- Dataset Version: 1.0.0
- Data Archetype: structured_monthly_financial_measurement_panel

## 2. Target User

A business or finance reviewer who needs to identify where budgeted expenditure differs from actual expenditure and decide which cost centres, departments and expenditure categories deserve further human review.

## 3. Primary Analytical Question

Which cost centres, departments and expenditure categories show the largest budget-versus-actual differences, and where should a human reviewer focus budget review?

## 4. Decision to Be Supported

Support descriptive, evidence-based human review of budget and actual financial measurements across available cost centres, departments, expenditure categories and reporting periods.

The analytical output will inform review priorities. It will not make autonomous financial decisions.

## 5. Approved Scope

Implement Track A — Comparative Intelligence only.

The analysis will cover:

- Cost-centre comparisons.
- Department comparisons.
- Expenditure-category comparisons.
- Monthly budget-versus-actual comparisons.
- Overall group comparisons across the available reporting period.
- Absolute and percentage financial variance.
- Descriptive rankings and supporting evidence.

## 6. Dataset and Evidence Profile

- Canonical records: 72.
- Canonical columns: 20.
- Independent synthetic source observations: 18.
- Reporting periods: January, February and March 2026.
- Departments: 4.
- Cost centres: 6.
- Expenditure categories: 6.
- Budget measurements: 18.
- Actual measurements: 18.
- Committed measurements: 18.
- Forecast measurements: 18.
- Dataset version: 1.0.0.

The 72 canonical records represent four derived financial measurements for each of 18 source observations. They must not be treated as 72 independent financial observations.

## 7. Analytical Input Fields

Required fields:

- record_id
- observed_at
- entity_id
- entity_name
- category
- metric_name
- metric_value
- metric_unit
- source_record_id
- data_version

The analysis will reshape the four financial metric types into one source-level observation before calculating variance.

## 8. Financial Measure Definitions

Budget and Actual are the only measures used to calculate the primary variance.

Variance:

Actual - Budget

Variance percentage:

((Actual - Budget) / Budget) * 100

Sign convention:

- Positive variance: actual expenditure exceeds budget (overspending).
- Negative variance: actual expenditure is below budget (underspending).
- Zero variance: actual expenditure equals budget.

Aggregated group percentages must be calculated using total Actual and total Budget. Individual percentages must not be averaged to represent an aggregated group percentage.

Committed and Forecast remain separate measures. They must not be added to Actual or Budget without an independently approved business rule. Forecast values are illustrative and are not validated predictions.

## 9. Grouping and Comparison Strategy

Cost-centre comparison:
- Group by entity_id and entity_name.
- Compare total Budget and Actual.
- Retain monthly supporting observations.

Department comparison:
- Group by entity_name.
- Aggregate the underlying cost-centre source observations.
- Report the number of contributing source observations.
- Do not interpret a larger department total as worse performance merely because it contains more cost centres.

Expenditure-category comparison:
- Group by category.
- Compare total Budget and Actual.
- Retain monthly supporting observations.

Monthly comparison:
- Group by reporting month and the relevant business dimension.
- Report the actual number of contributing source observations.
- Treat small monthly groups as descriptive evidence, not statistically reliable estimates.

## 10. Baseline Method

The baseline is direct descriptive comparison of grouped Budget and Actual amounts.

For each group:
- Sum Budget.
- Sum Actual.
- Calculate absolute variance.
- Calculate variance percentage.
- Record contributing source observation count.

The analytical method will compare results against this transparent baseline. No trained model is required.

## 11. Ranking and Evidence Rules

- Rank overall groups by descending absolute variance.
- Report overspending and underspending direction separately.
- Identify overspending groups clearly for human review.
- Use a minimum of 3 independent source observations for an overall group-level ranking.
- Report observation counts with every group result.
- Do not apply the overall minimum threshold blindly to monthly subgroups; disclose their actual counts and keep smaller groups descriptive.
- Resolve equal ranking values deterministically using alphabetical group identifiers.
- Do not describe rankings as statistical significance or predictive risk.

## 12. Validation Strategy

The analytical implementation must include:

1. Independent recalculation of selected group results.
2. Verification of Budget and Actual pairing.
3. Verification of variance and percentage formulas.
4. Verification of source observation counts.
5. Duplicate source-key checks.
6. Deterministic ranking and tie-handling checks.
7. Minimum group-size checks.
8. Sensitivity review of small groups and extreme financial values.
9. Ranking stability review.
10. Missing-group and missing-measure impact review.
11. Reproducibility checks through independent script execution.

## 13. Leakage and Data Availability

The analysis is descriptive and uses the approved synthetic financial measurements.

Budget and Actual are paired measurements from the same source observation. The analysis must not claim that the result was available before the actual expenditure was recorded.

Committed and Forecast must not be used to imply independently validated future outcomes.

No predictive model, target leakage experiment or future outcome claim is in scope.

## 14. Planned Intelligence Outputs

- outputs/intelligence_results.json
- outputs/intelligence_summary.json
- outputs/validation_metrics.json
- outputs/weak_case_review.json

The outputs must preserve supporting canonical record identifiers, source observation identifiers, reporting periods, financial values, calculated variances, data version and method version.

## 15. Planned Documentation

- docs/ANALYTICAL_TRACK_EXECUTION_PLAN.md
- docs/ANALYTICAL_INPUT_CONTRACT.md
- docs/ANALYTICAL_METHOD_REPORT.md
- docs/ANALYTICAL_VALIDATION_REPORT.md
- docs/WEAK_CASE_AND_LIMITATION_REVIEW.md
- docs/INTELLIGENCE_OUTPUT_CONTRACT.md

## 16. Method Versioning

Initial method version: 1.0.0.

The method report and generated outputs must identify the dataset version, method version, execution parameters, validation result and generation timestamp.

Changes to analytical logic, thresholds or ranking rules must be documented and reflected in method versioning.

## 17. Known Limitations

- All source observations are synthetic.
- Only 18 independent source observations are available.
- The reporting period covers only three months.
- The 72 canonical records are derived measurements, not 72 independent observations.
- Some departments contain more cost centres than others.
- Monthly department subgroups may contain fewer than three source observations.
- Forecast values are illustrative, not validated predictive outputs.
- No meaningful status, stage, text or geographic observations are populated.
- Results support descriptive human review only.

## 18. Excluded Scope

The following are explicitly excluded:

- Predictive modelling.
- Anomaly detection.
- Financial-risk scoring.
- Simulation and scenario modelling.
- Text and theme analysis.
- Dataset expansion or replacement.
- New dashboards or charts.
- Data Intelligence page integration.
- Chatbot or AI assistant integration.
- Production analytical APIs.
- Architectural redesign.
- Phase 3 Post #4 implementation.

## 19. Stop Conditions

Stop and review before proceeding if:

- The canonical dataset version changes.
- Required Budget or Actual measurements are missing or invalid.
- Source observations cannot be paired reliably.
- Duplicate or inconsistent source keys are discovered.
- Grouping relationships cannot be verified.
- Independent recalculation does not match the analytical output.
- The approved analytical question or track needs to change.

## 20. Expected Review Outcome

Produce a reproducible, independently validated Track A analytical output package that supports explainable financial comparison and human review.

Final review outcome must be one of:

- ANALYTICAL TRACK OUTPUT APPROVED
- ANALYTICAL TRACK CHANGES REQUIRED
- APPROVED TRACK NOT VIABLE
