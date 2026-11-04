# CANONICAL DATA PROFILE

## Dataset

- Source: `data/canonical/intelligence_data.csv`
- Data version: `1.0.0`
- Records: 72
- Columns: 20

## Generated Profile Evidence

The detailed, machine-readable profile is available at:
`data-science/outputs/canonical_profile.json`.

## Column Completeness and Uniqueness

| Column | Non-null | Null | Unique |
|---|---:|---:|---:|
| `record_id` | 72 | 0 | 72 |
| `record_type` | 72 | 0 | 1 |
| `observed_at` | 72 | 0 | 3 |
| `entity_id` | 72 | 0 | 6 |
| `related_entity_id` | 0 | 72 | 0 |
| `entity_name` | 72 | 0 | 4 |
| `category` | 72 | 0 | 6 |
| `subcategory` | 0 | 72 | 0 |
| `status` | 0 | 72 | 0 |
| `stage` | 0 | 72 | 0 |
| `metric_name` | 72 | 0 | 4 |
| `metric_value` | 72 | 0 | 47 |
| `metric_unit` | 72 | 0 | 1 |
| `text_value` | 0 | 72 | 0 |
| `latitude` | 0 | 72 | 0 |
| `longitude` | 0 | 72 | 0 |
| `source_name` | 72 | 0 | 1 |
| `source_record_id` | 72 | 0 | 18 |
| `is_synthetic` | 72 | 0 | 1 |
| `data_version` | 72 | 0 | 1 |

## Interpretation

- The canonical dataset contains four financial measurements per source observation.
- The 72 canonical records originate from 18 source observations.
- All records are marked synthetic.
- The reporting period covers January to March 2026.
- Geographic coordinates and meaningful text values are absent.
- Forecast values are inherited illustrative source figures, not validated predictive outputs.

## Reproducibility

Regenerate the profile by running:

```powershell
python data-science/scripts/profile_canonical_data.py
```

The script reads the canonical dataset and writes the machine-readable profile.
