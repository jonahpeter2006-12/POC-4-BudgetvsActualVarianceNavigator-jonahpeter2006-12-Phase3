
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FILE = ROOT / "data/canonical/intelligence_data.csv"
SOURCE_SAMPLE_FILE = ROOT / "data/source-sample/source_sample.csv"
MANIFEST_FILE = ROOT / "data/manifest.json"
OUTPUT_FILE = ROOT / "data-science/outputs/representativeness_assessment.json"

EXPECTED_SOURCE_METRICS = {
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount"
}


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], list(reader)


def unique_values(rows, field):
    return sorted({
        row.get(field, "").strip()
        for row in rows
        if row.get(field, "").strip()
    })


def normalize_month(value):
    parsed = datetime.strptime(value.strip(), "%b %Y")
    return parsed.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    canonical_columns, canonical = read_csv(CANONICAL_FILE)
    source_columns, source = read_csv(SOURCE_SAMPLE_FILE)

    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))

    if not canonical or not source:
        raise ValueError("Canonical dataset or preserved source sample is empty.")

    required_source_fields = [
        "cost_centre",
        "department",
        "account_category",
        "month",
        *sorted(EXPECTED_SOURCE_METRICS)
    ]

    missing_source_fields = [
        field for field in required_source_fields
        if field not in source_columns
    ]

    if missing_source_fields:
        raise ValueError(
            f"Source sample is missing expected fields: {missing_source_fields}"
        )

    required_canonical_fields = [
        "record_id",
        "observed_at",
        "entity_id",
        "entity_name",
        "category",
        "metric_name",
        "metric_value",
        "source_record_id",
        "data_version"
    ]

    missing_canonical_fields = [
        field for field in required_canonical_fields
        if field not in canonical_columns
    ]

    if missing_canonical_fields:
        raise ValueError(
            f"Canonical dataset is missing expected fields: {missing_canonical_fields}"
        )

    # Compare source and canonical entity/category coverage.
    comparisons = {
        "cost_centres": ("cost_centre", "entity_id"),
        "departments": ("department", "entity_name"),
        "categories": ("account_category", "category")
    }

    coverage = {}

    for name, (source_field, canonical_field) in comparisons.items():
        source_values = unique_values(source, source_field)
        canonical_values = unique_values(canonical, canonical_field)

        coverage[name] = {
            "source_field": source_field,
            "canonical_field": canonical_field,
            "source_unique_count": len(source_values),
            "canonical_unique_count": len(canonical_values),
            "source_values": source_values,
            "canonical_values": canonical_values,
            "all_source_values_preserved": set(source_values) == set(canonical_values),
            "missing_from_canonical": sorted(
                set(source_values) - set(canonical_values)
            ),
            "unexpected_in_canonical": sorted(
                set(canonical_values) - set(source_values)
            )
        }

    # Build the expected source-to-canonical mapping.
    expected = {}
    mapping_errors = []

    for source_index, source_row in enumerate(source, start=1):
        source_id = f"SRC-{source_index:04d}"

        try:
            expected_month = normalize_month(source_row["month"])
        except ValueError:
            mapping_errors.append({
                "source_record_id": source_id,
                "issue": "invalid_source_month",
                "value": source_row["month"]
            })
            continue

        for metric_name in sorted(EXPECTED_SOURCE_METRICS):
            try:
                expected_value = float(source_row[metric_name])
            except (TypeError, ValueError):
                mapping_errors.append({
                    "source_record_id": source_id,
                    "metric_name": metric_name,
                    "issue": "invalid_source_amount",
                    "value": source_row[metric_name]
                })
                continue

            expected[(source_id, metric_name)] = {
                "observed_at": expected_month,
                "entity_id": source_row["cost_centre"].strip(),
                "entity_name": source_row["department"].strip(),
                "category": source_row["account_category"].strip(),
                "metric_value": expected_value
            }

    # Index canonical rows by source observation and metric.
    canonical_index = {}
    duplicate_keys = []

    for row in canonical:
        key = (
            row.get("source_record_id", "").strip(),
            row.get("metric_name", "").strip()
        )

        if key in canonical_index:
            duplicate_keys.append({
                "source_record_id": key[0],
                "metric_name": key[1]
            })
        else:
            canonical_index[key] = row

    missing_mappings = []
    unexpected_mappings = []
    field_mismatches = []

    for key in sorted(set(expected) - set(canonical_index)):
        missing_mappings.append({
            "source_record_id": key[0],
            "metric_name": key[1]
        })

    for key in sorted(set(canonical_index) - set(expected)):
        unexpected_mappings.append({
            "source_record_id": key[0],
            "metric_name": key[1]
        })

    # Compare every expected mapped value.
    for key in sorted(set(expected) & set(canonical_index)):
        expected_row = expected[key]
        actual_row = canonical_index[key]

        comparisons_to_check = {
            "observed_at": (
                expected_row["observed_at"],
                actual_row.get("observed_at", "").strip()
            ),
            "entity_id": (
                expected_row["entity_id"],
                actual_row.get("entity_id", "").strip()
            ),
            "entity_name": (
                expected_row["entity_name"],
                actual_row.get("entity_name", "").strip()
            ),
            "category": (
                expected_row["category"],
                actual_row.get("category", "").strip()
            )
        }

        for field, (expected_value, actual_value) in comparisons_to_check.items():
            if expected_value != actual_value:
                field_mismatches.append({
                    "source_record_id": key[0],
                    "metric_name": key[1],
                    "field": field,
                    "expected": expected_value,
                    "actual": actual_value
                })

        try:
            actual_metric_value = float(actual_row["metric_value"])
            if actual_metric_value != expected_row["metric_value"]:
                field_mismatches.append({
                    "source_record_id": key[0],
                    "metric_name": key[1],
                    "field": "metric_value",
                    "expected": expected_row["metric_value"],
                    "actual": actual_metric_value
                })
        except (TypeError, ValueError):
            field_mismatches.append({
                "source_record_id": key[0],
                "metric_name": key[1],
                "field": "metric_value",
                "expected": expected_row["metric_value"],
                "actual": actual_row.get("metric_value")
            })

    # Verify each source observation has exactly the expected four metrics.
    source_id_counts = Counter(
        row.get("source_record_id", "").strip()
        for row in canonical
    )

    source_ids_expected = {
        f"SRC-{index:04d}"
        for index in range(1, len(source) + 1)
    }

    source_ids_actual = set(source_id_counts)

    source_id_coverage = {
        "expected_source_ids": len(source_ids_expected),
        "actual_source_ids": len(source_ids_actual),
        "missing_source_ids": sorted(source_ids_expected - source_ids_actual),
        "unexpected_source_ids": sorted(source_ids_actual - source_ids_expected)
    }

    metrics_per_source = {
        source_id: sorted(
            row.get("metric_name", "").strip()
            for row in canonical
            if row.get("source_record_id", "").strip() == source_id
        )
        for source_id in sorted(source_ids_expected | source_ids_actual)
    }

    incorrect_metric_sets = {
        source_id: metrics
        for source_id, metrics in metrics_per_source.items()
        if metrics != sorted(EXPECTED_SOURCE_METRICS)
    }

    # Compare normalized reporting-period coverage.
    source_months = sorted({
        normalize_month(row["month"])
        for row in source
    })

    canonical_months = sorted(unique_values(canonical, "observed_at"))

    # Compare source and canonical distributions.
    source_distribution = {
        "cost_centre": dict(Counter(row["cost_centre"] for row in source)),
        "department": dict(Counter(row["department"] for row in source)),
        "category": dict(Counter(row["account_category"] for row in source)),
        "month": dict(Counter(row["month"] for row in source))
    }

    canonical_distribution = {
        "entity_id": dict(Counter(row["entity_id"] for row in canonical)),
        "entity_name": dict(Counter(row["entity_name"] for row in canonical)),
        "category": dict(Counter(row["category"] for row in canonical)),
        "observed_at": dict(Counter(row["observed_at"] for row in canonical)),
        "metric_name": dict(Counter(row["metric_name"] for row in canonical))
    }

    checks = {
        "source_observation_count_matches_manifest": (
            len(source) == manifest["source"]["source_records"]
        ),
        "canonical_record_count_matches_manifest": (
            len(canonical) == manifest["canonical"]["records"]
        ),
        "all_source_observations_retained": (
            source_ids_actual == source_ids_expected
        ),
        "four_expected_metrics_per_source_observation": (
            not incorrect_metric_sets
        ),
        "no_duplicate_source_metric_mappings": (
            not duplicate_keys
        ),
        "no_missing_source_metric_mappings": (
            not missing_mappings
        ),
        "no_unexpected_source_metric_mappings": (
            not unexpected_mappings
        ),
        "all_source_to_canonical_values_match": (
            not field_mismatches and not mapping_errors
        ),
        "reporting_month_coverage_preserved": (
            source_months == canonical_months
        ),
        "cost_centre_coverage_preserved": (
            coverage["cost_centres"]["all_source_values_preserved"]
        ),
        "department_coverage_preserved": (
            coverage["departments"]["all_source_values_preserved"]
        ),
        "category_coverage_preserved": (
            coverage["categories"]["all_source_values_preserved"]
        )
    }

    result = {
        "assessment_version": "2.0.0",
        "canonical_dataset": "data/canonical/intelligence_data.csv",
        "representativeness_reference": "data/source-sample/source_sample.csv",
        "canonical_record_count": len(canonical),
        "source_observation_count": len(source),
        "canonical_source_id_count": len(source_ids_actual),
        "expected_metric_names": sorted(EXPECTED_SOURCE_METRICS),
        "transformation_note": (
            "Each source observation is expected to produce exactly four "
            "canonical financial measurement rows. These are derived "
            "measurements, not independent transactions."
        ),
        "source_id_coverage": source_id_coverage,
        "coverage_comparison": coverage,
        "temporal_coverage": {
            "source_reporting_dates": source_months,
            "canonical_reporting_dates": canonical_months,
            "source_reporting_period_count": len(source_months),
            "canonical_reporting_period_count": len(canonical_months),
            "all_reporting_periods_preserved": source_months == canonical_months
        },
        "source_observation_distributions": source_distribution,
        "canonical_record_distributions": canonical_distribution,
        "mapping_verification": {
            "expected_source_metric_pairs": len(expected),
            "actual_canonical_source_metric_pairs": len(canonical_index),
            "missing_mappings": missing_mappings,
            "unexpected_mappings": unexpected_mappings,
            "duplicate_mappings": duplicate_keys,
            "field_mismatches": field_mismatches,
            "incorrect_metric_sets": incorrect_metric_sets,
            "source_value_or_date_errors": mapping_errors
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_mapping_coverage_checks_passed": all(checks.values()),
        "limitations": [
            "All supplied observations are synthetic.",
            "Preservation of the source sample does not establish real-world population representativeness.",
            "Only the reporting periods present in the source sample are assessed.",
            "The preserved source sample is the available comparison reference, not an independent external population.",
            "The canonical measurement rows must not be interpreted as independent source observations.",
            "Source identifiers are generated from source row order because the source sample has no independent source-record identifier."
        ],
        "assessment": (
            "source_mapping_verified_with_real_world_limitations"
            if all(checks.values())
            else "mapping_or_coverage_review_required"
        )
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Representativeness assessment completed.")
    print("Source observations:", len(source))
    print("Canonical records:", len(canonical))
    print("Mapping pairs expected:", len(expected))
    print("Mapping pairs found:", len(canonical_index))
    print("Checks passed:", result["checks_passed"], "/", result["checks_total"])
    print("Assessment:", result["assessment"])
    print("Output:", OUTPUT_FILE.relative_to(ROOT))

    if not all(checks.values()):
        print("Review mapping_verification in the output JSON for failed comparisons.")


if __name__ == "__main__":
    main()
