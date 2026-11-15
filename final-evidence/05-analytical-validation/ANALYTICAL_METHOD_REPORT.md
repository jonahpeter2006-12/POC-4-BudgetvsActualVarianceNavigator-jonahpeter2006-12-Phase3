# ANALYTICAL METHOD REPORT

## 1. Report Information

- Project: Budget vs Actual Variance Navigator
- PoC: 4
- Phase: Phase 3 — Post #3
- Approved Track: Track A — Comparative Intelligence
- Method Version: 1.0.0
- Dataset Version: 1.0.0
- Canonical Dataset: data/canonical/intelligence_data.csv
- Assessment Type: Descriptive financial comparison

## 2. Analytical Objective

The objective is to compare budgeted and actual financial measurements across the available departments, cost centres and expenditure categories.

The analysis identifies where the largest absolute budget-versus-actual differences occur and provides evidence to help a human reviewer focus budget review.

## 3. Primary Analytical Question

Which cost centres, departments and expenditure categories show the largest budget-versus-actual differences, and where should a human reviewer focus budget review?

## 4. Decision Supported

The analytical output supports descriptive, evidence-based human review of budget and actual financial measurements across the available financial groups and reporting periods.

It does not make autonomous financial decisions or establish financial risk.

## 5. Approved Analytical Scope

Only Track A — Comparative Intelligence is implemented.

The analysis includes:

- Budget-versus-actual variance.
- Variance percentage.
- Department-level comparison.
- Cost-centre comparison.
- Expenditure-category comparison.
- Reporting-period comparisons.
- Evidence-backed descriptive findings.
- Deterministic ranking of comparison results.

No second analytical track is introduced.

## 6. Authoritative Input

The sole analytical input is:

data/canonical/intelligence_data.csv

Dataset characteristics:

- 72 canonical measurement records.
- 20 columns.
- 18 independent synthetic source observations.
- Four financial measurements per source observation.
- Six cost centres.
- Four departments.
- Six expenditure categories.
- Three monthly reporting periods.
- Dataset version 1.0.0.

The 72 measurement records must not be interpreted as 72 independent financial observations.

## 7. Financial Measures

The four financial measures remain separate:

1. Budget — planned financial amount.
2. Actual — recorded financial amount.
3. Committed — separately reported committed amount.
4. Forecast — illustrative forecast amount.

Only Budget and Actual are used in the primary variance calculation.

Committed and Forecast are retained as separate contextual measurements. They are not added to Budget or Actual, and are not double-counted.

Forecast values are illustrative and are not validated predictive outputs.

## 8. Variance Definitions

The sign convention is:

Variance = Actual - Budget

Variance Percentage = ((Actual - Budget) / Budget) * 100

Interpretation:

- Positive variance: Actual exceeds Budget (overspend).
- Negative variance: Actual is below Budget (underspend).
- Zero variance: Actual equals Budget.

All monetary calculations retain the original currency unit.

A zero budget must not produce an infinite or fabricated percentage. The percentage must be marked unavailable and the case explicitly disclosed.

## 9. Aggregation Method

For a comparison group:

- Group Budget = sum of Budget amounts.
- Group Actual = sum of Actual amounts.
- Group Variance = Group Actual - Group Budget.
- Group Variance Percentage = (Group Variance / Group Budget) * 100, when Group Budget is non-zero.

The group percentage is calculated from aggregate amounts. It is not the unweighted average of individual percentages.

## 10. Comparison Dimensions

The method evaluates:

### 10.1 Cost Centre

Cost centres are compared using their financial measurements and associated evidence.

### 10.2 Department

Department comparisons aggregate the available cost-centre measurements belonging to each department.

Department totals must be interpreted in the context of the number of cost centres and observations represented. Larger totals alone do not indicate worse performance.

### 10.3 Expenditure Category

Expenditure categories are compared using the same variance definitions and aggregation rules.

### 10.4 Reporting Period

Monthly comparisons retain the reporting month and group identity. Smaller monthly evidence counts are disclosed and interpreted descriptively.

## 11. Evidence and Minimum Group Size

Each financial comparison must preserve:

- Group identifier and dimension.
- Reporting period.
- Budget total.
- Actual total.
- Variance amount.
- Variance percentage, when defined.
- Number of independent source observations.
- Supporting canonical record identifiers.
- Supporting source observation identifiers.
- Dataset version.
- Method version.

For overall group ranking, a minimum of three independent source observations is required.

This is an evidence-screening threshold only. It does not establish statistical representativeness or population-level reliability.

Monthly subgroup counts must be reported explicitly. Results with limited observations remain descriptive and must not be presented as statistically conclusive.

## 12. Ranking and Tie Handling

The primary comparison ranking uses descending absolute variance.

Overspending and underspending direction must remain visible separately through the signed variance.

Ties are resolved deterministically using the alphabetical group identifier as the secondary sort key.

Priority ranking indicates the magnitude of the observed difference. It is not a financial risk score or an automated decision.

## 13. Baseline

The baseline is direct arithmetic comparison of canonical Budget and Actual measurements using the documented formulas.

No predictive model, machine-learning baseline or external financial benchmark is introduced.

The analytical method must be independently recalculable from the canonical input.

## 14. Validation Strategy

Validation includes:

- Required-field and financial-measure checks.
- Numeric and currency consistency checks.
- Source-observation pairing checks.
- Duplicate and missing-measure checks.
- Independent variance recalculation.
- Aggregation reconciliation.
- Minimum evidence checks.
- Deterministic ranking and tie checks.
- Small-group and extreme-value sensitivity review.
- Missing-group impact review.
- Reporting-period and group-identity preservation.
- Dataset and method version checks.
- Reproducible execution through a reusable script and notebook.

A validation failure must be reported explicitly rather than silently corrected.

## 15. Leakage and Availability

The analysis is descriptive and uses the reporting timestamps and financial measurements present in the canonical dataset.

It does not claim that forecast values were available at a verified historical decision time.

No future outcome, target leakage or predictive performance claim is introduced.

## 16. Interpretation Rules

Findings must:

- Identify the financial group and reporting period.
- Show Budget, Actual and calculated variance.
- Include the variance percentage when valid.
- Preserve the supporting canonical evidence.
- State the number of independent source observations.
- Identify the dataset and method versions.
- Explain relevant limitations.

Findings must not imply causation, fraud, financial distress or future performance.

## 17. Known Limitations

- All observations are synthetic.
- Only 18 independent source observations are available.
- The 72 canonical records are four measurements from each source observation, not 72 independent transactions.
- The reporting period covers only January through March 2026.
- Group sizes are small.
- Monthly subgroup results may have limited evidence.
- Forecast measurements are illustrative and are not validated predictions.
- No real-world financial accuracy or operational effectiveness is established.

## 18. Excluded Methods and Scope

The following are excluded:

- Predictive modelling.
- Anomaly detection.
- Unsupported financial risk scoring.
- Causal inference.
- Automated financial decisions.
- A second analytical track.
- Additional datasets or external financial values.
- New dashboards or Data Intelligence page implementation.
- Production analytical API development.

## 19. Reproducibility and Versioning

The analytical method version is 1.0.0.

The implementation must record:

- Dataset version.
- Method version.
- Execution timestamp.
- Validation result.
- Analytical parameters.
- Known limitations.

The reusable analytical script and notebook must produce consistent analytical results from the same canonical input and method configuration.

## 20. Expected Analytical Outcome

The expected outcome is a validated, reproducible set of descriptive financial comparisons and evidence-backed findings suitable for future review and possible Data Intelligence integration after the required approval.

No integration or additional phase work is authorized by this report alone.
