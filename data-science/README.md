
# Phase 3 — Data Validation, Profiling and Analytical Readiness

## 1. Purpose

This workspace performs reproducible data validation, profiling, quality assessment, representativeness assessment and analytical readiness assessment.

## 2. Authoritative Dataset

Source: `data/canonical/intelligence_data.csv`

- Data version: 1.0.0
- Canonical records: 72
- Columns: 20
- Original source observations: 18
- Financial metrics per observation: 4
- Reporting period: January–March 2026
- All records are synthetic.

The 72 canonical records represent four measurements from each of 18 source observations. They are not 72 independent transactions.

## 3. Workspace Structure

- `notebooks/` — validation and readiness notebook
- `scripts/` — reproducible assessment and verification scripts
- `outputs/` — generated JSON assessment results

## 4. Assessment Workflow

Run these commands from the repository root in the following order:

```powershell
python data-science/scripts/profile_canonical_data.py
python data-science/scripts/assess_representativeness.py
python data-science/scripts/assess_data_quality.py
python data-science/scripts/assess_analytical_readiness.py
```

## 5. Reproducibility Verification

Run the complete automated verification:

```powershell
python data-science/scripts/verify_reproducibility.py
```

The verification script:

- Executes the complete assessment pipeline twice.
- Compares all four generated JSON assessment outputs.
- Checks that the input files remain unchanged.
- Confirms that the final analytical readiness output is stable.
- Records reproducibility evidence in `quality_assessment.json`.

Reproducibility is marked as passed only when all verification checks succeed.

## 6. Generated Documentation

- `docs/CANONICAL_DATA_PROFILE.md`
- `docs/DATA_QUALITY_ASSESSMENT.md`
- `docs/REPRESENTATIVENESS_ASSESSMENT.md`
- `docs/ANALYTICAL_READINESS_REPORT.md`

## 7. Important Limitations

The dataset is synthetic and contains only 18 original source observations. It supports comparative and limited descriptive analysis, but does not establish real-world accuracy, predictive reliability or operational decision-making capability.

Reproducibility verification demonstrates repeatable execution against the current local inputs. It does not independently establish real-world data accuracy.

---

# Phase 3 Post #3 — Comparative Intelligence Track Development

## 8. Approved Analytical Track

- Approved track: Track A — Comparative Intelligence
- Method version: 1.0.0
- Input dataset: `data/canonical/intelligence_data.csv`
- Dataset version: 1.0.0
- Output contract version: 1.0.0

This track performs descriptive financial comparisons using the approved canonical dataset. It does not introduce a second analytical track or a predictive model.

## 9. Analytical Method

The method compares Budget and Actual financial amounts.

- Variance = Actual − Budget
- Variance Percentage = (Actual − Budget) / Budget × 100

Positive variance indicates overspending. Negative variance indicates underspending. Zero variance indicates spending on budget.

Budget, Actual, Committed and Forecast remain separate measures. Committed and Forecast are contextual values and are not added to Budget or Actual when calculating variance.

Group percentages are calculated from aggregated Budget and Actual totals rather than averages of individual percentages.

Overall comparisons are ranked by descending absolute variance when they meet the minimum three-independent-source-observation screening threshold. Monthly findings remain descriptive and unranked.

## 10. Track Execution

Run from the repository root:

```powershell
python data-science/scripts/run_analytical_track.py
python data-science/scripts/validate_analytical_track.py
python data-science/scripts/export_intelligence_results.py
```

The track commands above are run from the repository root.

## 11. Analytical Notebook

- `data-science/notebooks/02_analytical_track_development_and_validation.ipynb`

The notebook executes the analytical workflow, validation and export steps and records their outputs.

## 12. Track Scripts

- `data-science/scripts/track-specific/comparative_intelligence.py`
- `data-science/scripts/run_analytical_track.py`
- `data-science/scripts/validate_analytical_track.py`
- `data-science/scripts/export_intelligence_results.py`

## 13. Generated Intelligence Outputs

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`
- `data-science/outputs/weak_case_review.json`

The analytical execution generated 64 findings:

- 16 overall comparison findings.
- 48 monthly comparison findings.

The output preserves group identity, reporting period, financial values, evidence references and dataset and method versions.

## 14. Post #3 Documentation

- `docs/ANALYTICAL_TRACK_EXECUTION_PLAN.md`
- `docs/ANALYTICAL_INPUT_CONTRACT.md`
- `docs/ANALYTICAL_METHOD_REPORT.md`
- `docs/ANALYTICAL_VALIDATION_REPORT.md`
- `docs/WEAK_CASE_AND_LIMITATION_REVIEW.md`
- `docs/INTELLIGENCE_OUTPUT_CONTRACT.md`

## 15. Validation Evidence

The recorded analytical validation completed with:

- Total checks: 1,230
- Failed checks: 0
- Validation result: PASS
- Findings generated: 64
- Unique finding IDs: 64

Two executions with a fixed generation timestamp produced identical output.

The analytical notebook was executed successfully with five code cells and zero execution errors.

## 16. Evidence and Limitations

The dataset contains 18 independent synthetic source observations. Its 72 canonical rows represent four financial measurements per source observation, not 72 independent transactions.

The 48 monthly findings are marked `insufficient_evidence` because they have only one or two independent source observations. They are retained for descriptive transparency and excluded from overall ranking.

The 16 overall findings meet the three-source screening threshold but remain subject to the limitations of the synthetic dataset.

Forecast amounts are illustrative and are not validated predictive outputs. The analysis does not provide predictive modelling, anomaly detection, financial risk scoring, causal inference or autonomous financial decisions.

## 17. Scope Boundary

This work is limited to the approved Track A comparative intelligence development and validation.

It does not introduce a new dashboard, Data Intelligence page, production analytical API, second dataset, predictive model or architectural redesign.

Integration into the existing application is outside this Post #3 implementation step and must wait for the required review and approval.
