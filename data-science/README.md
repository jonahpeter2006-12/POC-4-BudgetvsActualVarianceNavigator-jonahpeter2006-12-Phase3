
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
