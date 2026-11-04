
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "data/canonical/intelligence_data.csv"
SOURCE_FILE = ROOT / "data/source-sample/source_sample.csv"
MANIFEST_FILE = ROOT / "data/manifest.json"
SCHEMA_FILE = ROOT / "data/schema.json"
PROFILE_FILE = ROOT / "data-science/outputs/canonical_profile.json"
REPRESENTATIVENESS_FILE = (
    ROOT / "data-science/outputs/representativeness_assessment.json"
)
VALIDATION_FILE = ROOT / "data/quality/validation_report.json"
OUTPUT_FILE = ROOT / "data-science/outputs/quality_assessment.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], list(reader)


def is_blank(value):
    return value is None or str(value).strip() == ""


def parse_number(value):
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (ValueError, TypeError):
        return None


def parse_date(value):
    try:
        parsed = datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )
        if parsed.utcoffset() is None:
            return None
        return parsed
    except (ValueError, TypeError):
        return None


def parse_source_month(value):
    try:
        return datetime.strptime(
            value, "%b %Y"
        ).strftime("%Y-%m-01T00:00:00Z")
    except (ValueError, TypeError):
        return None


def make_check(status, evidence, limitation=None):
    result = {
        "status": status,
        "evidence": evidence
    }

    if limitation:
        result["limitation"] = limitation

    return result


def get_allowed_values(column):
    accepted_keys = (
        "accepted_values",
        "allowed_values",
        "valid_values",
        "enum"
    )

    for key in accepted_keys:
        values = column.get(key)

        if isinstance(values, list):
            return values

    return None


def normalize_schema_value(value, schema_column):
    """
    Normalize CSV text according to the declared schema type.

    CSV values are read as strings. Boolean schema values must
    therefore be converted before comparison.
    """

    if schema_column.get("type") == "boolean":
        if isinstance(value, bool):
            return value

        normalized = str(value).strip().lower()

        if normalized == "true":
            return True

        if normalized == "false":
            return False

        return normalized

    return str(value).strip()


def main():

    # ---------------------------------------------------------
    # LOAD APPROVED DATA AND EXISTING ASSESSMENTS
    # ---------------------------------------------------------

    columns, rows = read_csv(DATA_FILE)
    source_columns, source_rows = read_csv(SOURCE_FILE)

    manifest = read_json(MANIFEST_FILE)
    schema = read_json(SCHEMA_FILE)
    profile = read_json(PROFILE_FILE)
    representativeness = read_json(REPRESENTATIVENESS_FILE)

    validation_report = (
        read_json(VALIDATION_FILE)
        if VALIDATION_FILE.exists()
        else {}
    )

    schema_columns = schema.get("columns", [])

    schema_names = [
        item["name"] for item in schema_columns
    ]

    expected_metrics = manifest["transformation"]["metric_names"]
    expected_source_count = manifest["source"]["source_records"]
    expected_unit = manifest["transformation"]["metric_unit"]
    expected_version = manifest["dataset_version"]
    expected_source_name = manifest["source"]["source_file"]
    expected_synthetic = manifest["transformation"]["is_synthetic"]

    row_count = len(rows)

    # ---------------------------------------------------------
    # STRUCTURAL INTEGRITY — SEPARATE GATE
    # ---------------------------------------------------------

    structural_checks = {
        "canonical_columns_match_schema": columns == schema_names,

        "canonical_record_count_matches_manifest": (
            row_count == manifest["canonical"]["records"]
        ),

        "canonical_column_count_matches_manifest": (
            len(columns) == manifest["canonical"]["columns"]
        ),

        "schema_column_count_matches_manifest": (
            len(schema_names) == manifest["canonical"]["columns"]
        )
    }

    structural_ok = all(structural_checks.values())

    # ---------------------------------------------------------
    # 1. COMPLETENESS
    # ---------------------------------------------------------

    required_fields = [
        item["name"]
        for item in schema_columns
        if item.get("required", False)
    ]

    field_completeness = {}

    for field in columns:
        blank_count = sum(
            1 for row in rows if is_blank(row.get(field))
        )

        field_completeness[field] = {
            "non_null_count": row_count - blank_count,
            "null_count": blank_count,
            "null_percentage": round(
                blank_count / row_count * 100, 2
            ) if row_count else 0
        }

    missing_required = {
        field: field_completeness.get(field, {}).get(
            "null_count", row_count
        )
        for field in required_fields
    }

    completeness_ok = (
        all(count == 0 for count in missing_required.values())
        and all(field in columns for field in required_fields)
    )

    # ---------------------------------------------------------
    # 2. UNIQUENESS
    # ---------------------------------------------------------

    record_ids = [
        row.get("record_id", "") for row in rows
    ]

    duplicate_record_ids = sum(
        count - 1
        for count in Counter(record_ids).values()
        if count > 1
    )

    source_metric_pairs = [
        (
            row.get("source_record_id", ""),
            row.get("metric_name", "")
        )
        for row in rows
    ]

    duplicate_source_metric_pairs = sum(
        count - 1
        for count in Counter(source_metric_pairs).values()
        if count > 1
    )

    uniqueness_ok = (
        all(not is_blank(value) for value in record_ids)
        and duplicate_record_ids == 0
        and duplicate_source_metric_pairs == 0
    )

    # ---------------------------------------------------------
    # 3. VALIDITY
    # ---------------------------------------------------------

    invalid_numeric_values = sum(
        1 for row in rows
        if parse_number(row.get("metric_value")) is None
    )

    invalid_dates = sum(
        1 for row in rows
        if parse_date(row.get("observed_at")) is None
    )

    invalid_metric_names = sum(
        1 for row in rows
        if row.get("metric_name") not in expected_metrics
    )

    invalid_units = sum(
        1 for row in rows
        if row.get("metric_unit") != expected_unit
    )

    invalid_coordinates = {}

    for field, minimum, maximum in (
        ("latitude", -90, 90),
        ("longitude", -180, 180)
    ):

        invalid_coordinates[field] = sum(
            1 for row in rows
            if not is_blank(row.get(field))
            and (
                parse_number(row.get(field)) is None
                or not minimum <= parse_number(row.get(field)) <= maximum
            )
        )

    partial_coordinate_pairs = sum(
        1 for row in rows
        if (
            is_blank(row.get("latitude"))
            != is_blank(row.get("longitude"))
        )
    )

    invalid_accepted_values = {}

    for schema_column in schema_columns:

        field = schema_column["name"]
        allowed = get_allowed_values(schema_column)

        if allowed is not None and field in columns:

            accepted = {
                normalize_schema_value(value, schema_column)
                for value in allowed
            }

            invalid_accepted_values[field] = sum(
                1 for row in rows
                if (
                    not is_blank(row.get(field))
                    and normalize_schema_value(
                        row.get(field), schema_column
                    ) not in accepted
                )
            )

    validity_ok = (
        invalid_numeric_values == 0
        and invalid_dates == 0
        and invalid_metric_names == 0
        and invalid_units == 0
        and all(
            value == 0
            for value in invalid_coordinates.values()
        )
        and partial_coordinate_pairs == 0
        and all(
            value == 0
            for value in invalid_accepted_values.values()
        )
    )

    # ---------------------------------------------------------
    # 4. CONSISTENCY
    # ---------------------------------------------------------

    metric_counts = Counter(
        row.get("metric_name", "") for row in rows
    )

    source_ids = [
        row.get("source_record_id", "") for row in rows
    ]

    records_per_source = Counter(source_ids)

    expected_metric_distribution = {
        metric: expected_source_count
        for metric in expected_metrics
    }

    metric_unit_sets = defaultdict(set)

    for row in rows:
        metric_unit_sets[row.get("metric_name", "")].add(
            row.get("metric_unit", "")
        )

    mixed_metric_units = {
        metric: sorted(units)
        for metric, units in metric_unit_sets.items()
        if len(units) > 1
    }

    synthetic_values = [
        row.get("is_synthetic", "").strip().lower()
        for row in rows
    ]

    version_values = sorted(set(
        row.get("data_version", "") for row in rows
    ))

    expected_source_ids = {
        f"SRC-{index:04d}"
        for index in range(1, expected_source_count + 1)
    }

    actual_source_ids = set(source_ids)

    source_metric_sets = defaultdict(set)

    for row in rows:
        source_metric_sets[row.get("source_record_id", "")].add(
            row.get("metric_name", "")
        )

    every_source_has_expected_metrics = (
        actual_source_ids == expected_source_ids
        and all(
            source_metric_sets[source_id] == set(expected_metrics)
            for source_id in expected_source_ids
        )
    )

    consistency_checks = {
        "metric_distribution_matches_expected": (
            dict(metric_counts) == expected_metric_distribution
        ),

        "source_observation_count_matches": (
            len(actual_source_ids) == expected_source_count
        ),

        "four_measurements_per_source_observation": (
            every_source_has_expected_metrics
            and all(
                count == len(expected_metrics)
                for count in records_per_source.values()
            )
        ),

        "no_duplicate_source_metric_pairs": (
            duplicate_source_metric_pairs == 0
        ),

        "all_records_have_expected_synthetic_flag": (
            all(
                value == str(expected_synthetic).lower()
                for value in synthetic_values
            )
        ),

        "data_version_matches_manifest": (
            version_values == [expected_version]
        ),

        "metric_units_consistent": not mixed_metric_units
    }

    consistency_ok = all(consistency_checks.values())

    # ---------------------------------------------------------
    # 5. ACCURACY AGAINST PRESERVED SOURCE SAMPLE
    # ---------------------------------------------------------

    source_fields = [
        "cost_centre",
        "department",
        "account_category",
        "month",
        "budget_amount",
        "actual_amount",
        "committed_amount",
        "forecast_amount"
    ]

    source_accuracy_checks = {
        "source_columns_match_expected": (
            source_columns == source_fields
        ),

        "source_observation_count_matches_manifest": (
            len(source_rows) == expected_source_count
        )
    }

    source_metric_mapping = {
        "budget_amount": "budget_amount",
        "actual_amount": "actual_amount",
        "committed_amount": "committed_amount",
        "forecast_amount": "forecast_amount"
    }

    expected_mapping = {}

    for index, source in enumerate(source_rows, start=1):

        source_id = f"SRC-{index:04d}"

        for metric, source_field in source_metric_mapping.items():

            expected_mapping[(source_id, metric)] = {
                "metric_value": parse_number(source.get(source_field)),
                "entity_id": source.get("cost_centre", ""),
                "entity_name": source.get("department", ""),
                "category": source.get("account_category", ""),
                "observed_at": parse_source_month(
                    source.get("month", "")
                )
            }

    actual_mapping = defaultdict(list)

    for row in rows:

        key = (
            row.get("source_record_id", ""),
            row.get("metric_name", "")
        )

        actual_mapping[key].append(row)

    missing_mappings = []
    unexpected_mappings = []
    duplicate_mappings = []
    value_mismatches = []
    metadata_mismatches = []

    for key, expected in expected_mapping.items():

        matches = actual_mapping.get(key, [])

        if not matches:
            missing_mappings.append({
                "source_record_id": key[0],
                "metric_name": key[1]
            })
            continue

        if len(matches) > 1:
            duplicate_mappings.append({
                "source_record_id": key[0],
                "metric_name": key[1]
            })
            continue

        actual = matches[0]

        if (
            parse_number(actual.get("metric_value"))
            != expected["metric_value"]
        ):
            value_mismatches.append({
                "source_record_id": key[0],
                "metric_name": key[1]
            })

        for field in (
            "entity_id",
            "entity_name",
            "category",
            "observed_at"
        ):

            if actual.get(field) != expected[field]:
                metadata_mismatches.append({
                    "source_record_id": key[0],
                    "metric_name": key[1],
                    "field": field
                })

    for key in actual_mapping:

        if key not in expected_mapping:
            unexpected_mappings.append({
                "source_record_id": key[0],
                "metric_name": key[1]
            })

    accuracy_ok = (
        all(source_accuracy_checks.values())
        and not missing_mappings
        and not unexpected_mappings
        and not duplicate_mappings
        and not value_mismatches
        and not metadata_mismatches
    )

    # ---------------------------------------------------------
    # 6. REPRESENTATIVENESS
    # ---------------------------------------------------------

    representativeness_status = representativeness.get(
        "assessment", "unknown"
    )

    representativeness_passed = representativeness.get(
        "checks_passed"
    )

    representativeness_total = representativeness.get(
        "checks_total"
    )

    representativeness_ok = (
        representativeness.get(
            "all_mapping_coverage_checks_passed"
        ) is True
        and representativeness_passed is not None
        and representativeness_total is not None
        and representativeness_passed == representativeness_total
        and representativeness_total > 0
        and not missing_mappings
        and not unexpected_mappings
        and not duplicate_mappings
        and not value_mismatches
        and not metadata_mismatches
    )

    # ---------------------------------------------------------
    # 7. TIMELINESS
    # ---------------------------------------------------------

    date_coverage = profile.get("date_coverage", {})

    # No business freshness requirement was supplied.
    # Timeliness therefore remains conditional.

    # ---------------------------------------------------------
    # 8. PROVENANCE
    # ---------------------------------------------------------

    provenance_ok = (
        all(
            row.get("source_name") == expected_source_name
            for row in rows
        )
        and all(
            not is_blank(row.get("source_record_id"))
            for row in rows
        )
        and all(
            row.get("data_version") == expected_version
            for row in rows
        )
    )

    # ---------------------------------------------------------
    # 9. SAFETY
    # ---------------------------------------------------------

    text_values = [
        row.get("text_value", "")
        for row in rows
        if not is_blank(row.get("text_value"))
    ]

    text_content = " ".join(text_values)

    email_matches = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text_content
    )

    phone_like_matches = re.findall(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
        text_content
    )

    safety_ok = (
        all(
            value == str(expected_synthetic).lower()
            for value in synthetic_values
        )
        and not email_matches
        and not phone_like_matches
    )

    # ---------------------------------------------------------
    # 10. REPRODUCIBILITY
    # ---------------------------------------------------------

    # The quality assessment script itself cannot prove that
    # the complete documented pipeline has been rerun.

    reproducibility_status = "pending_verification"

    # ---------------------------------------------------------
    # BUILD THE TEN QUALITY DIMENSIONS
    # ---------------------------------------------------------

    dimensions = {

        "completeness": make_check(
            "passed" if completeness_ok else "failed",
            {
                "required_fields": required_fields,
                "missing_required_values": missing_required,
                "field_completeness": field_completeness
            },
            "Optional blank fields are reported but are not automatically required-field failures."
        ),

        "uniqueness": make_check(
            "passed" if uniqueness_ok else "failed",
            {
                "record_count": row_count,
                "unique_record_ids": len(set(record_ids)),
                "duplicate_record_ids": duplicate_record_ids,
                "duplicate_source_metric_pairs": duplicate_source_metric_pairs
            }
        ),

        "validity": make_check(
            "passed" if validity_ok else "failed",
            {
                "invalid_numeric_values": invalid_numeric_values,
                "invalid_dates": invalid_dates,
                "invalid_metric_names": invalid_metric_names,
                "invalid_units": invalid_units,
                "invalid_coordinates": invalid_coordinates,
                "partial_coordinate_pairs": partial_coordinate_pairs,
                "invalid_schema_accepted_values": invalid_accepted_values
            },
            "Accepted-value checks are normalized according to the declared schema type."
        ),

        "consistency": make_check(
            "passed" if consistency_ok else "failed",
            {
                "checks": consistency_checks,
                "metric_distribution": dict(metric_counts),
                "expected_metric_distribution": expected_metric_distribution,
                "source_observation_count": len(actual_source_ids),
                "records_per_source_distribution": dict(
                    Counter(records_per_source.values())
                ),
                "mixed_metric_units": mixed_metric_units,
                "data_version_values": version_values,
                "manifest_status": manifest.get("status", "missing"),
                "post1_validation_status": validation_report.get(
                    "status", "unknown"
                )
            }
        ),

        "accuracy": make_check(
            "passed" if accuracy_ok else "failed",
            {
                "source_accuracy_checks": source_accuracy_checks,
                "expected_source_metric_pairs": len(expected_mapping),
                "actual_source_metric_pairs": len(actual_mapping),
                "missing_mappings": missing_mappings,
                "unexpected_mappings": unexpected_mappings,
                "duplicate_mappings": duplicate_mappings,
                "value_mismatches": value_mismatches,
                "metadata_mismatches": metadata_mismatches
            },
            "This verifies exact mapping against the preserved synthetic source sample; it does not prove real-world financial accuracy."
        ),

        "representativeness": make_check(
            "conditional" if representativeness_ok else "review_required",
            {
                "assessment": representativeness_status,
                "checks_passed": representativeness_passed,
                "checks_total": representativeness_total,
                "all_mapping_coverage_checks_passed": (
                    representativeness.get(
                        "all_mapping_coverage_checks_passed"
                    )
                ),
                "source_observations": len(source_rows),
                "canonical_measurements": row_count
            },
            "The synthetic source sample cannot establish representativeness of real organisations or financial activity."
        ),

        "timeliness": make_check(
            "conditional",
            {
                "earliest_reporting_date": date_coverage.get("earliest"),
                "latest_reporting_date": date_coverage.get("latest"),
                "reporting_periods": date_coverage.get(
                    "unique_reporting_dates"
                ),
                "unique_months": date_coverage.get("unique_months")
            },
            "The dataset covers January to March 2026 only. No business freshness requirement was supplied."
        ),

        "provenance": make_check(
            "passed" if provenance_ok else "failed",
            {
                "expected_source_name": expected_source_name,
                "actual_source_names": sorted(set(
                    row.get("source_name", "") for row in rows
                )),
                "source_record_ids_present": all(
                    not is_blank(value) for value in source_ids
                ),
                "source_observation_count": len(actual_source_ids),
                "data_versions": version_values
            }
        ),

        "safety": make_check(
            "passed" if safety_ok else "review_required",
            {
                "all_records_synthetic": all(
                    value == str(expected_synthetic).lower()
                    for value in synthetic_values
                ),
                "text_values_present": len(text_values),
                "email_like_matches": len(email_matches),
                "phone_like_matches": len(phone_like_matches)
            },
            "Automated pattern screening is limited and does not guarantee that all sensitive information is absent."
        ),

        "reproducibility": make_check(
            reproducibility_status,
            {
                "profiling_script": (
                    "data-science/scripts/profile_canonical_data.py"
                ),
                "quality_script": (
                    "data-science/scripts/assess_data_quality.py"
                ),
                "profile_output": (
                    "data-science/outputs/canonical_profile.json"
                ),
                "source_dataset": (
                    "data/canonical/intelligence_data.csv"
                ),
                "full_pipeline_reproduction_verified": False
            },
            "Full reproducibility must be confirmed by executing the complete documented workflow."
        )
    }

    # ---------------------------------------------------------
    # OVERALL ASSESSMENT
    # ---------------------------------------------------------

    blocking_failures = [
        name
        for name, result in dimensions.items()
        if result["status"] == "failed"
    ]

    review_required = [
        name
        for name, result in dimensions.items()
        if result["status"] == "review_required"
    ]

    conditional_dimensions = [
        name
        for name, result in dimensions.items()
        if result["status"] == "conditional"
    ]

    quality = {
        "assessment_version": "2.0.0",
        "dataset": "data/canonical/intelligence_data.csv",
        "data_version": expected_version,
        "records_assessed": row_count,
        "structural_integrity": {
            "status": "passed" if structural_ok else "failed",
            "checks": structural_checks
        },
        "dimensions_assessed": len(dimensions),
        "dimensions": dimensions,
        "blocking_failures": blocking_failures,
        "review_required_dimensions": review_required,
        "conditional_dimensions": conditional_dimensions,
        "overall_status": (
            "failed"
            if not structural_ok or blocking_failures
            else "review_required"
            if review_required
            else "assessment_completed_with_limitations"
        )
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(quality, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Data quality assessment completed.")
    print("Records assessed:", row_count)
    print("Structural integrity:", quality["structural_integrity"]["status"])
    print("Quality dimensions assessed:", len(dimensions))
    print("Blocking failures:", len(blocking_failures))
    print("Review-required dimensions:", len(review_required))
    print("Conditional dimensions:", len(conditional_dimensions))
    print("Overall status:", quality["overall_status"])
    print("Output:", OUTPUT_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
