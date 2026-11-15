# FINAL ANALYTICAL REVALIDATION

## 1. Purpose

This report records the Post #6 revalidation evidence for the approved Track A — Comparative Intelligence method. It confirms whether the existing analytical outputs, calculations, evidence, and validation status remain consistent with the approved Phase 3 scope.

## 2. Approved Analytical Scope

- Track: Track A — Comparative Intelligence.
- Method version: 1.0.0.
- Contract version: 1.0.0.
- Dataset version: 1.0.0.
- Analytical question: Which cost centres, departments, and expenditure categories show the largest budget-versus-actual differences, and where should a human reviewer focus budget review?
- Decision supported: Descriptive, evidence-based human review only.

No new analytical track, model, scoring method, or predictive capability was introduced.

## 3. Authoritative Data

The canonical input remains:

`data/canonical/intelligence_data.csv`

Recorded dataset profile:
- 72 canonical rows.
- 20 columns.
- 18 source observations preserved.
- Four financial measures: Budget, Actual, Committed, and Forecast.
- Three reporting months: January, February, and March 2026.
- Six cost centres, four departments, and six expenditure categories.

The 72 canonical rows represent four derived financial-measure records per source observation. They are not 72 independent transactions. All observations are synthetic.

## 4. Calculation Rules

The approved variance calculations remain:

`Variance = Actual - Budget`

`Variance % = (Actual - Budget) / Budget * 100`

Positive variance indicates spending above budget; negative variance indicates spending below budget.

Committed and Forecast remain separate measures. Forecast values are illustrative and are not predictions.

## 5. Analytical Output Coverage

The previously executed Track A output contains 64 findings:
- 16 overall comparison findings.
- 48 monthly findings.
- Overall dimensions: six cost centres, four departments, and six expenditure categories.
- Monthly dimensions: 18 cost-centre, 12 department, and 18 category findings.

Monthly findings with insufficient independent evidence remain explicitly limited and are not promoted to stronger conclusions.

## 6. Latest Revalidation Evidence

The updated local Docker image returned the following validation results from its intelligence summary endpoint:

| Validation item | Result |
|---|---:|
| Combined validation status | PASS |
| Passed checks | 1,325 |
| Failed checks | 0 |
| Warning checks | 0 |
| Analytical validation | 1,230 / 1,230 passed |
| Reconciliation validation | 95 / 95 passed |
| Aggregation reconciliation | PASS |
| Baseline comparison | PASS |
| Baseline calculation mismatches | 0 |
| Reproducibility | PASS |

The combined validation count is 1,325. The sensitivity assessment is reported separately and is not included in that combined total.

The correct public Phase 3 Render backend was also queried. Its intelligence summary returned PASS, with 1,325 passed checks, zero failed checks, and zero warnings.

## 7. Evidence and Interpretation Controls

The approved analytical method continues to require:
- Traceability to finding identifiers and source and canonical record identifiers.
- Separation of Budget, Actual, Committed, and Forecast.
- Disclosure of synthetic data and the 18 independent source observations.
- Disclosure of insufficient-evidence monthly findings.
- No population-level conclusions.
- No predictive, anomaly, fraud, or risk-scoring claims.

## 8. Revalidation Limitations

- The dataset remains synthetic and limited to 18 independent source observations.
- The reporting period covers only January–March 2026.
- Monthly findings with insufficient evidence remain descriptive.
- Forecast values remain illustrative.
- A completed sensitivity assessment does not establish statistical robustness.
- This report records the latest available local-container and public API evidence; it does not claim a new independent reconstruction of every analytical result during Post #6.

## 9. Conclusion

**PASS WITH DOCUMENTED ANALYTICAL LIMITATIONS.**

The approved Track A method and its version boundaries remain unchanged. The latest local-container and public Render API validation summaries both report 1,325 passed checks, zero failures, and zero warnings.

This analytical revalidation does not certify the entire Phase 3 release. Final certification remains subject to the outstanding Post #6 deployment, browser, evidence, clean-clone, and reviewer-approval requirements.
