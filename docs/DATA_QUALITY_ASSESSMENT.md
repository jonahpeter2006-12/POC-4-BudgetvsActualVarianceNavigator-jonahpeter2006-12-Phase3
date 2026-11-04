# DATA QUALITY ASSESSMENT

## Assessment Overview

- Dataset: `data/canonical/intelligence_data.csv`
- Data version: 1.0.0
- Records assessed: 72
- Overall status: **assessment_completed_with_limitations**

## Quality Dimensions

| Dimension | Status |
|---|---|
| Structural Integrity | passed |
| Completeness | passed |
| Uniqueness | passed |
| Validity | passed |
| Consistency | passed |
| Accuracy | not_verifiable |
| Representativeness | conditional |
| Timeliness | conditional |
| Provenance | passed |
| Safety | passed |
| Reproducibility | passed |

## Structural Integrity

**Status:** passed

**Evidence:**

```json
{
  "expected_columns": 20,
  "actual_columns": 20,
  "actual_records": 72
}
```

## Completeness

**Status:** passed

**Evidence:**

```json
{
  "required_fields": [
    "record_id",
    "record_type",
    "observed_at",
    "entity_id",
    "entity_name",
    "category",
    "metric_name",
    "metric_value",
    "metric_unit",
    "source_name",
    "source_record_id",
    "is_synthetic",
    "data_version"
  ],
  "missing_required_values": {
    "record_id": 0,
    "record_type": 0,
    "observed_at": 0,
    "entity_id": 0,
    "entity_name": 0,
    "category": 0,
    "metric_name": 0,
    "metric_value": 0,
    "metric_unit": 0,
    "source_name": 0,
    "source_record_id": 0,
    "is_synthetic": 0,
    "data_version": 0
  },
  "optional_blank_fields": [
    "related_entity_id",
    "subcategory",
    "status",
    "stage",
    "text_value",
    "latitude",
    "longitude"
  ]
}
```

**Limitation:** Optional blank fields limit additional analyses but are not required-field failures.

## Uniqueness

**Status:** passed

**Evidence:**

```json
{
  "record_ids": 72,
  "unique_record_ids": 72,
  "duplicate_record_ids": 0
}
```

## Validity

**Status:** passed

**Evidence:**

```json
{
  "invalid_numeric_values": 0,
  "invalid_dates": 0,
  "non_usd_units": 0,
  "invalid_metric_names": 0
}
```

## Consistency

**Status:** passed

**Evidence:**

```json
{
  "metric_distribution": {
    "budget_amount": 18,
    "actual_amount": 18,
    "committed_amount": 18,
    "forecast_amount": 18
  },
  "source_observation_count": 18,
  "measurements_per_source": {
    "4": 18
  },
  "duplicate_source_metric_pairs": 0,
  "all_records_synthetic": true
}
```

## Accuracy

**Status:** not_verifiable

**Evidence:**

```json
{
  "synthetic_records": 72,
  "independent_real_world_reference": false
}
```

**Limitation:** Structural and numeric validity do not prove that financial amounts represent real-world financial accuracy.

## Representativeness

**Status:** conditional

**Evidence:**

```json
{
  "source_observations_retained": 18,
  "canonical_measurements": 72,
  "sampling_note": "All 18 supplied source observations were retained."
}
```

**Limitation:** The supplied synthetic source does not establish representativeness of real organisations or financial activity.

## Timeliness

**Status:** conditional

**Evidence:**

```json
{
  "earliest_reporting_date": "2026-01-01T00:00:00+00:00",
  "latest_reporting_date": "2026-03-01T00:00:00+00:00",
  "reporting_periods": 3
}
```

**Limitation:** Only January to March 2026 is available; no business freshness requirement was supplied.

## Provenance

**Status:** passed

**Evidence:**

```json
{
  "source_names": [
    "backend/budget_data.csv"
  ],
  "source_record_ids_present": true,
  "source_observations": 18
}
```

## Safety

**Status:** passed

**Evidence:**

```json
{
  "all_records_marked_synthetic": true,
  "text_values_present": 0,
  "text_pattern_screen": {
    "email_like_strings": false,
    "phone_like_strings": false
  }
}
```

**Limitation:** This is a basic screening, not a guarantee that all sensitive information is absent.

## Reproducibility

**Status:** passed

**Evidence:**

```json
{
  "profiling_script": "data-science/scripts/profile_canonical_data.py",
  "profile_output": "data-science/outputs/canonical_profile.json",
  "source_dataset": "data/canonical/intelligence_data.csv"
}
```

**Limitation:** Reproducibility should be reconfirmed by rerunning the scripts in the documented order.

## Blocking Failures

Number of blocking failures: 0

```json
[]
```

## Overall Interpretation

The canonical dataset passes its structural, completeness, uniqueness, validity, consistency and provenance checks.

Accuracy cannot be independently verified because all observations are synthetic. Representativeness and timeliness remain conditional because the available data covers only three months and does not establish real-world population coverage.

The safety assessment is a basic screening and does not guarantee that all sensitive information is absent.

Reproducibility must be reconfirmed by rerunning the documented scripts in sequence.

## Conclusion

**assessment_completed_with_limitations**

The dataset has no blocking quality failures, but its documented limitations must be considered before analytical development.
