# Canonical Data Package Validation

## 1. Purpose

This document records the validation of the Phase 3 Canonical Data Foundation package.

The validation process checks the canonical dataset, supporting metadata, published JSON output, required files, data consistency, and project constraints.

## 2. Validation Scope

The following files and components are included:

- `data/README.md`
- `data/manifest.json`
- `data/schema.json`
- `data/source-sample/source_sample.csv`
- `data/canonical/intelligence_data.csv`
- `data/published/intelligence_data.json`
- `data/quality/data_profile.json`
- `data/quality/validation_report.json`
- `data/quality/sampling_report.md`
- `scripts/data_pipeline/`

## 3. Expected Dataset Structure

| Item | Expected value |
|---|---:|
| Original source records | 18 |
| Canonical records | 72 |
| Canonical columns | 20 |
| Metrics per source record | 4 |
| Dataset version | 1.0.0 |
| Currency | USD |
| Synthetic records | 72 |
| Reporting period | January–March 2026 |

The canonical CSV must follow the exact 20-column order defined in `data/schema.json`.

## 4. Validation Checks

The validation script checks the following areas:

### 4.1 Required Files

- Required dataset files exist.
- Schema and manifest files contain valid JSON.
- Required canonical and published outputs are available.

### 4.2 Canonical Structure

- Canonical column names match the schema.
- Canonical column order is correct.
- Expected record count is 72.
- Expected column count is 20.
- Dataset row and column limits are respected.

### 4.3 Record Integrity

- Record identifiers are not empty.
- Record identifiers are unique.
- Source record identifiers are preserved.
- Source names are present.
- Record types are valid.
- Dataset versions match the manifest.

### 4.4 Data Quality

- Observation dates follow the expected ISO 8601 UTC format.
- Metric values are numeric.
- Metric names belong to the allowed metric list.
- Metric units are USD.
- Synthetic indicators are true.
- Free-text values respect the configured length limit.

### 4.5 Source and Transformation Consistency

- The preserved source sample contains 18 records.
- Four canonical metric records are generated per source record.
- Each of the four metric types contains 18 records.
- No source records are excluded.

### 4.6 Published JSON Consistency

- Published JSON is valid.
- Published JSON contains 72 records.
- Published records match the canonical CSV after the expected data-type conversions.

### 4.7 Package Safety and Size

- Main CSV and JSON files respect the configured file-size limits.
- The complete data directory respects the 10 MB limit.
- Binary and media files are not included in the data package.

## 5. Validation Execution

The validation was executed using:

```powershell
python scripts/data_pipeline/validate_data.py
```

The script generated the validation report at:

`data/quality/validation_report.json`

## 6. Validation Results

<text> </text>

| Result | Count |
|---|---:|
| Records checked | 72 |
| Columns checked | 20 |
| Checks passed | 40 |
| Checks failed | 0 |

**Validation status: PASSED**

The validation script completed successfully with no failed checks.

## 7. Pipeline Components

The Phase 3 data pipeline contains five scripts:

1. `extract_data.py` — preserves the original source dataset.
2. `sample_data.py` — documents the sampling and retention decision.
3. `standardize_data.py` — transforms source records into canonical records.
4. `publish_data.py` — generates the published JSON dataset.
5. `validate_data.py` — checks the canonical data package.

## 8. Known Limitations

1. The source dataset contains synthetic financial data.
2. The reporting period is limited to three months.
3. Forecast values are inherited from the source dataset and are not statistically validated.
4. Geographic coordinates and related entity identifiers are unavailable.
5. The 40 passed checks represent the validations implemented in the current script; they do not constitute independent organizational approval.

## 9. Conclusion

The implemented validation process reports 40 checks passed and zero failed.

The canonical dataset and published JSON are consistent with the checks performed.

**Package status: Ready for review and approval.**

Formal approval remains subject to the Phase 3 review process.