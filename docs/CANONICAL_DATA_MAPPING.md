# Canonical Data Mapping

## 1. Purpose

This document explains how the original budget dataset is transformed into the Phase 3 canonical data structure.

The canonical dataset provides a standardized format for budget and actual financial metrics while preserving the relationship between each record and its original source.

## 2. Source Dataset

**Source file:** `backend/budget_data.csv`

- Original records: 18
- Original columns: 8
- Departments: 4
- Cost centres: 6
- Reporting period: January–March 2026
- Currency: USD
- Data classification: Synthetic

The original source file is preserved without modification.

## 3. Transformation Approach

Each source record contains four financial measures:

1. `budget_amount`
2. `actual_amount`
3. `committed_amount`
4. `forecast_amount`

Each measure is converted into a separate canonical record.

Therefore:

- Original source records: 18
- Canonical records per source record: 4
- Total canonical records: 18 × 4 = 72

No source records are removed during this transformation.

## 4. Canonical Field Mapping

| Canonical field | Source / transformation |
|---|---|
| `record_id` | Generated as `FIN-{source index}-{metric name}` |
| `record_type` | Constant value: `financial_metric` |
| `observed_at` | Month converted to ISO 8601 UTC format using the first day of the month |
| `entity_id` | `cost_centre` |
| `related_entity_id` | Blank; not available in source |
| `entity_name` | `department` |
| `category` | `account_category` |
| `subcategory` | Blank; not available in source |
| `status` | Blank; not available in source |
| `stage` | Blank; not available in source |
| `metric_name` | One of the four financial measure names |
| `metric_value` | Corresponding financial amount |
| `metric_unit` | Constant value: `USD` |
| `text_value` | Blank; not available in source |
| `latitude` | Blank; not available in source |
| `longitude` | Blank; not available in source |
| `source_name` | `backend/budget_data.csv` |
| `source_record_id` | Generated as `SRC-{source index}` |
| `is_synthetic` | `true` |
| `data_version` | `1.0.0` |

## 5. Record Identification and Lineage

Every original source row receives a stable source record identifier.

The pipeline generates four canonical records from that source row, one for each financial measure.

The generated identifiers follow these patterns:

- Source record: `SRC-0001`
- Canonical records: `FIN-0001-BUDGET_AMOUNT`, `FIN-0001-ACTUAL_AMOUNT`, `FIN-0001-COMMITTED_AMOUNT`, and `FIN-0001-FORECAST_AMOUNT`

The source record identifier maintains traceability between canonical records and the original dataset.

Identifiers are generated deterministically using the source row order and metric name.

## 6. Date Standardization

The original month values use the format `Mon YYYY`.

They are converted to ISO 8601 UTC timestamps using the first day of each month.

Example:

- Original value: `Jan 2026`
- Canonical value: `2026-01-01T00:00:00Z`

The same approach is applied to February and March 2026.

## 7. Canonical Output

**Output file:** `data/canonical/intelligence_data.csv`

The output contains:

- 72 records
- 20 canonical columns
- Standardized financial metric names
- Numeric metric values
- USD as the metric unit
- Source record lineage
- Synthetic data indicators
- Dataset version `1.0.0`

The canonical CSV is the single source of truth for the published dataset.

## 8. Assumptions and Limitations

1. The source dataset contains synthetic financial information.
2. All four financial measures are preserved for every source record.
3. No additional records or external data are introduced.
4. Missing information is represented using blank fields.
5. No geographic coordinates or related entity identifiers are available in the source.
6. The `forecast_amount` values are taken directly from the source dataset. They are not newly generated or statistically validated forecasts.
7. The dataset covers only January, February, and March 2026.

## 9. Reproducibility

The transformation is implemented in:

`scripts/data_pipeline/standardize_data.py`

The pipeline reads the preserved source sample and produces the canonical CSV using the documented mapping rules.

The generated output can be checked using:

`scripts/data_pipeline/validate_data.py`
