# ANALYTICAL VALIDATION REPORT

## 1. Report Information

- Project: Budget vs Actual Variance Navigator
- PoC: 4
- Approved analytical track: Track A — Comparative Intelligence
- Dataset version: 1.0.0
- Method version: 1.0.0
- Contract version: 1.0.0
- Validation status: PASS
- Total validation checks: 1,230
- Failed checks: 0

## 2. Validation Objective

This report records the validation of the comparative financial intelligence method developed for Phase 3 Post #3.

The validation checks whether the analytical outputs:
- Use the approved canonical dataset.
- Apply the documented financial variance formulas.
- Preserve the separation of Budget, Actual, Committed and Forecast.
- Retain traceability to canonical source records.
- Apply the agreed evidence threshold and ranking rules.
- Follow the intelligence output contract.
- Disclose limitations and insufficient evidence.

## 3. Input and Scope

The analysis uses only:

`data/canonical/intelligence_data.csv`

The canonical dataset contains 72 rows and 20 columns, representing 18 independent synthetic financial source observations across three monthly reporting periods.

The four financial measures are:
- Budget Amount
- Actual Amount
- Committed Amount
- Forecast Amount

The approved method is descriptive and comparative. No predictive model, anomaly detection, causal inference or financial risk scoring is used.

## 4. Validation Methodology

The validation script independently checks the generated findings against the canonical input and the documented analytical rules.

The checks cover:
- Finding schema and structure.
- Financial calculations and classifications.
- Evidence and canonical record traceability.
- Separation of financial measures.
- Minimum evidence eligibility.
- Ranking order and eligibility.
- Finding descriptions and limitations.
- Dataset, method and contract version metadata.
- Expected finding counts and identity.

## 5. Validation Results

| Validation area | Checks |
|---|---:|
| Calculations | 256 |
| Classification | 128 |
| Count | 1 |
| Evidence | 256 |
| Evidence status | 64 |
| Finding descriptions | 64 |
| Identity | 1 |
| Limitations | 64 |
| Measure separation | 128 |
| Metadata | 3 |
| Ranking eligibility | 64 |
| Ranking order | 3 |
| Schema | 128 |
| Finding type counts | 6 |
| Version checks | 64 |
| **Total** | **1,230** |

- Passed checks: 1,230
- Failed checks: 0
- Validation result: PASS

## 6. Analytical Output Coverage

The execution produced 64 findings.

| Finding type | Findings |
|---|---:|
| Cost-centre comparisons | 6 |
| Department comparisons | 4 |
| Expenditure-category comparisons | 6 |
| Monthly cost-centre comparisons | 18 |
| Monthly department comparisons | 12 |
| Monthly expenditure-category comparisons | 18 |
| **Total** | **64** |

The output contains 16 overall comparison findings and 48 monthly comparison findings.

## 7. Financial Calculation Validation

The method uses the following definitions:

- Variance = Actual − Budget
- Variance Percentage = (Actual − Budget) / Budget × 100

Positive variance represents overspending. Negative variance represents underspending. Zero variance represents spending on budget.

Group variance percentages are calculated from aggregated Budget and Actual totals. Individual percentages are not averaged to produce group percentages.

The validator recalculates the reported Budget, Actual, variance, variance percentage and source observation counts against canonical source records. A separate baseline comparison run has not been recorded (NOT_SEPARATELY_TESTED). A separate aggregation reconciliation test has also not been run (NOT_SEPARATELY_TESTED).

## 8. Evidence and Traceability

The validation checked evidence references for all 64 findings.

Each finding retains its applicable:
- Group identity.
- Reporting period.
- Budget and Actual totals.
- Variance amount and percentage.
- Independent source observation count.
- Canonical record IDs.
- Source record IDs.
- Data and method versions.

Evidence traceability checks: 64 passed, 0 failed.

## 9. Measure Separation

Budget, Actual, Committed and Forecast remain separate measures.

Committed and Forecast totals are included as contextual information. They are not added to Budget or Actual when calculating variance.

The validation confirmed the separation of these measures and the use of Actual minus Budget for variance calculations.

Measure-separation checks: 128 passed, 0 failed.

## 10. Evidence Threshold and Ranking

Overall group comparisons require at least three independent source observations to qualify for ranking.

Overall comparison findings meeting this threshold are ranked by descending absolute variance, while retaining the signed variance direction. Deterministic alphabetical tie-breaking is applied.

Monthly findings are descriptive and are not ranked because their individual group sizes do not meet the overall evidence threshold.

Ranking and evidence-rule checks: 57 passed, 0 failed.

## 11. Reproducibility Evidence

Two analytical executions using the same canonical input and a fixed generation timestamp produced identical results.

- Findings in each execution: 64
- SHA-256: `5769ac9aea58a657914b983827f0b831f7eb78cffae28974ecd8b9f57ad9ae09`
- Output equality: True

These two runs establish deterministic analytical output reproducibility using the same canonical input, method and dataset versions, and fixed timestamp. This does not establish full-workspace reproducibility or replace the separately documented baseline, aggregation and regression checks.

The notebook was executed successfully:
- Code cells: 5
- Executed code cells: 5
- Execution errors: 0

## 12. Limitations and Interpretation

The validation confirms implementation consistency against the documented method and input contract. It does not establish statistical representativeness or population-level financial conclusions.

Important limitations:
- The 18 independent source observations are synthetic.
- The 72 canonical rows represent four derived financial measures per source observation, not 72 independent transactions.
- Only three monthly reporting periods are available.
- Forecast values are illustrative and are not validated predictive outputs.
- Monthly comparisons with fewer than three independent observations are not eligible for overall ranking.

The minimum evidence threshold is a screening rule, not proof of statistical significance or representativeness.

## 13. Validation Conclusion

The Track A comparative intelligence execution passed all 1,230 recorded validation checks with zero failures.

The 64 findings conform to the tested calculation, evidence, ranking, measure-separation and output-structure rules.

The analytical results JSON was reproduced identically in two fixed-timestamp executions and is traceable to the canonical dataset. Baseline comparison and separate aggregation reconciliation remain untested, and full-workspace reproducibility and Phase 2 regression must be assessed separately.

**Result: VALIDATION PASS — READY FOR POST #3 REVIEW, SUBJECT TO THE DOCUMENTED LIMITATIONS AND REMAINING SUBMISSION CHECKS.**
