# Canonical Data Package

## Dataset
**Name:** Budget vs Actual Variance Navigator – Canonical Intelligence Data
**Version:** 1.0.0
**Status:** Pending validation
**Format:** CSV
**Encoding:** UTF-8
**Synthetic data:** Yes

## Source
The canonical dataset is derived from `backend/budget_data.csv`, a synthetic financial dataset containing 18 source records and 8 columns.

An unchanged copy of the source is preserved at:

`data/source-sample/source_sample.csv`

## Canonical Dataset
The canonical source of truth is:

`data/canonical/intelligence_data.csv`

It contains:
- 72 canonical records
- 20 columns in the required order
- Four financial metric records per source record
- USD as the metric unit
- ISO 8601 UTC reporting dates

## Financial Metrics
Each source record produces four metric records:
1. `budget_amount`
2. `actual_amount`
3. `committed_amount`
4. `forecast_amount`

## Pipeline
The reproducible pipeline is located in `scripts/data_pipeline/`:

1. `extract_data.py` – extracts and preserves the source sample.
2. `sample_data.py` – documents the sampling decision.
3. `standardize_data.py` – transforms source records into canonical records.
4. `validate_data.py` – validates the canonical package.
5. `publish_data.py` – publishes the canonical dataset as JSON.

## Package Structure
- `source-sample/` – preserved source CSV.
- `canonical/` – canonical CSV source of truth.
- `published/` – published JSON representation.
- `quality/` – sampling, profiling, and validation evidence.
- `schema.json` – canonical column definitions.
- `manifest.json` – dataset metadata and package limits.

## Data Quality and Safety
The dataset is synthetic and contains financial planning figures. No personal financial account information is included in the supplied source.

The package is subject to validation for:
- Required columns and column order
- Record count and unique identifiers
- Data types and date formats
- Source traceability
- Synthetic-data flags and version consistency
- File-size and directory-size limits
- Published JSON consistency

## Important Limitation
The source contains only three monthly periods (January–March 2026). Forecast values are supplied illustrative figures and should not be treated as evidence of statistically validated forecasting performance.

## Approval
The package remains pending until the validation pipeline completes and the required evidence is reviewed.