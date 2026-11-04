# DATA QUALITY ASSESSMENT

## Assessment Overview

- Dataset: `data/canonical/intelligence_data.csv`
- Data version: 1.0.0
- Records assessed: 72
- Overall status: **assessment_completed_with_limitations**

## Quality Dimensions

| Dimension | Status |
|---|---|
| Completeness | passed |
| Uniqueness | passed |
| Validity | passed |
| Consistency | passed |
| Accuracy | passed |
| Representativeness | conditional |
| Timeliness | conditional |
| Provenance | passed |
| Safety | passed |
| Reproducibility | passed |

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
  "field_completeness": {
    "record_id": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "record_type": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "observed_at": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "entity_id": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "related_entity_id": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "entity_name": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "category": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "subcategory": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "status": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "stage": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "metric_name": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "metric_value": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "metric_unit": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "text_value": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "latitude": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "longitude": {
      "non_null_count": 0,
      "null_count": 72,
      "null_percentage": 100.0
    },
    "source_name": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "source_record_id": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "is_synthetic": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    },
    "data_version": {
      "non_null_count": 72,
      "null_count": 0,
      "null_percentage": 0.0
    }
  }
}
```

**Limitation:** Optional blank fields are reported but are not automatically required-field failures.

## Uniqueness

**Status:** passed

**Evidence:**

```json
{
  "record_count": 72,
  "unique_record_ids": 72,
  "duplicate_record_ids": 0,
  "duplicate_source_metric_pairs": 0
}
```

## Validity

**Status:** passed

**Evidence:**

```json
{
  "invalid_numeric_values": 0,
  "invalid_dates": 0,
  "invalid_metric_names": 0,
  "invalid_units": 0,
  "invalid_coordinates": {
    "latitude": 0,
    "longitude": 0
  },
  "partial_coordinate_pairs": 0,
  "invalid_schema_accepted_values": {
    "record_type": 0,
    "entity_id": 0,
    "entity_name": 0,
    "category": 0,
    "metric_name": 0,
    "metric_unit": 0,
    "source_name": 0,
    "is_synthetic": 0,
    "data_version": 0
  }
}
```

**Limitation:** Accepted-value checks are normalized according to the declared schema type.

## Consistency

**Status:** passed

**Evidence:**

```json
{
  "checks": {
    "metric_distribution_matches_expected": true,
    "source_observation_count_matches": true,
    "four_measurements_per_source_observation": true,
    "no_duplicate_source_metric_pairs": true,
    "all_records_have_expected_synthetic_flag": true,
    "data_version_matches_manifest": true,
    "metric_units_consistent": true
  },
  "metric_distribution": {
    "budget_amount": 18,
    "actual_amount": 18,
    "committed_amount": 18,
    "forecast_amount": 18
  },
  "expected_metric_distribution": {
    "budget_amount": 18,
    "actual_amount": 18,
    "committed_amount": 18,
    "forecast_amount": 18
  },
  "source_observation_count": 18,
  "records_per_source_distribution": {
    "4": 18
  },
  "mixed_metric_units": {},
  "data_version_values": [
    "1.0.0"
  ],
  "manifest_status": "validated",
  "post1_validation_status": "passed"
}
```

## Accuracy

**Status:** passed

**Evidence:**

```json
{
  "source_accuracy_checks": {
    "source_columns_match_expected": true,
    "source_observation_count_matches_manifest": true
  },
  "expected_source_metric_pairs": 72,
  "actual_source_metric_pairs": 72,
  "missing_mappings": [],
  "unexpected_mappings": [],
  "duplicate_mappings": [],
  "value_mismatches": [],
  "metadata_mismatches": []
}
```

**Limitation:** This verifies exact mapping against the preserved synthetic source sample; it does not prove real-world financial accuracy.

## Representativeness

**Status:** conditional

**Evidence:**

```json
{
  "assessment": "source_mapping_verified_with_real_world_limitations",
  "checks_passed": 12,
  "checks_total": 12,
  "all_mapping_coverage_checks_passed": true,
  "source_observations": 18,
  "canonical_measurements": 72
}
```

**Limitation:** The synthetic source sample cannot establish representativeness of real organisations or financial activity.

## Timeliness

**Status:** conditional

**Evidence:**

```json
{
  "earliest_reporting_date": "2026-01-01T00:00:00+00:00",
  "latest_reporting_date": "2026-03-01T00:00:00+00:00",
  "reporting_periods": 3,
  "unique_months": null
}
```

**Limitation:** The dataset covers January to March 2026 only. No business freshness requirement was supplied.

## Provenance

**Status:** passed

**Evidence:**

```json
{
  "expected_source_name": "backend/budget_data.csv",
  "actual_source_names": [
    "backend/budget_data.csv"
  ],
  "source_record_ids_present": true,
  "source_observation_count": 18,
  "data_versions": [
    "1.0.0"
  ]
}
```

## Safety

**Status:** passed

**Evidence:**

```json
{
  "all_records_synthetic": true,
  "text_values_present": 0,
  "email_like_matches": 0,
  "phone_like_matches": 0
}
```

**Limitation:** Automated pattern screening is limited and does not guarantee that all sensitive information is absent.

## Reproducibility

**Status:** passed

**Evidence:**

```json
{
  "profiling_script": "data-science/scripts/profile_canonical_data.py",
  "quality_script": "data-science/scripts/assess_data_quality.py",
  "profile_output": "data-science/outputs/canonical_profile.json",
  "source_dataset": "data/canonical/intelligence_data.csv",
  "full_pipeline_reproduction_verified": true,
  "verification_method": "Two complete pipeline executions with JSON output comparison.",
  "pipeline_runs_completed": 2,
  "assessment_outputs_compared": 4,
  "assessment_outputs_match": true,
  "input_files_unchanged": true
}
```

**Limitation:** Verification confirms repeatable execution against the current local inputs. It does not establish real-world data accuracy.

## Blocking Failures

Number of blocking failures: 0

```json
[]
```

## Overall Interpretation

The canonical dataset passes its structural, completeness, uniqueness, validity, consistency and provenance checks.

Accuracy cannot be independently verified because all observations are synthetic. Representativeness and timeliness remain conditional because the available data covers only three months and does not establish real-world population coverage.

The safety assessment is a basic screening and does not guarantee that all sensitive information is absent.

Reproducibility verification passed. Two complete pipeline executions produced matching assessment outputs, and the input files remained unchanged.

## Conclusion

**assessment_completed_with_limitations**

The dataset has no blocking quality failures, but its documented limitations must be considered before analytical development.
