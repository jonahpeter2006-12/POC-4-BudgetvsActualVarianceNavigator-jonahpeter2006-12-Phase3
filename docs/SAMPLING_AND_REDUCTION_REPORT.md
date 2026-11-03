# Sampling and Reduction Report

## 1. Purpose

This report documents the sampling and data reduction decisions for the Phase 3 Canonical Data Foundation of the Budget vs Actual Variance Navigator.

## 2. Source Dataset

- **Source:** `backend/budget_data.csv`
- **Preserved snapshot:** `data/source-sample/source_sample.csv`
- **Format:** CSV
- **Original record count:** 18
- **Original column count:** 8
- **Reporting period:** January–March 2026
- **Data classification:** Synthetic financial data

## 3. Sampling Decision

All 18 source records are retained.

No random sampling, filtering, or record exclusion has been applied.

This decision was made because the source dataset is small and contains only 18 records. Retaining the complete dataset preserves all available cost centres, departments, account categories, reporting months, and financial measures.

## 4. Reduction Decision

No source records have been removed.

The canonical transformation will reorganize the source information into the required 20-column structure. This is a standardization process, not a loss of source records.

Each source row will be represented by multiple canonical records to preserve its separate financial measures:

- Budget amount
- Actual amount
- Committed amount
- Forecast amount

The expected canonical record count is therefore:

18 source rows × 4 financial measures = **72 canonical records**.

## 5. Data Preservation

The original source file remains unchanged at:

`backend/budget_data.csv`

The preserved snapshot is stored at:

`data/source-sample/source_sample.csv`

The canonical output will be stored separately at:

`data/canonical/intelligence_data.csv`

## 6. Sampling Quality Considerations

The complete source dataset preserves:

- All six cost centres.
- All four departments.
- All six account categories.
- All three reporting months.
- All available financial measures.

No rare categories or reporting periods are intentionally excluded.

## 7. Limitations

- The source contains only three months of synthetic financial observations.
- The dataset is not suitable for claiming statistically validated long-term forecasting performance.
- No additional historical records are available in the supplied source.
- The canonical expansion creates separate measure records but does not create additional independent source observations.

## 8. Conclusion

The complete source dataset is retained without sampling or reduction.

The transformation will expand 18 source rows into 72 canonical measure records while preserving the original financial values and their source relationships.