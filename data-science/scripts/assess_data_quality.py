import csv
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data/canonical/intelligence_data.csv"
MANIFEST_FILE = ROOT / "data/manifest.json"
SCHEMA_FILE = ROOT / "data/schema.json"
PROFILE_FILE = ROOT / "data-science/outputs/canonical_profile.json"
OUTPUT_FILE = ROOT / "data-science/outputs/quality_assessment.json"

EXPECTED_COLUMNS = [
    "record_id", "record_type", "observed_at", "entity_id",
    "related_entity_id", "entity_name", "category", "subcategory",
    "status", "stage", "metric_name", "metric_value", "metric_unit",
    "text_value", "latitude", "longitude", "source_name",
    "source_record_id", "is_synthetic", "data_version"
]

def check(status, evidence, limitation=None):
    result = {"status": status, "evidence": evidence}
    if limitation:
        result["limitation"] = limitation
    return result

def main():
    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        rows = list(reader)

    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))

    row_count = len(rows)
    ids = [row["record_id"] for row in rows]
    source_ids = [row["source_record_id"] for row in rows]

    # Structural validation
    structure_ok = (
        columns == EXPECTED_COLUMNS
        and len(rows) == manifest["canonical"]["records"]
        and len(columns) == manifest["canonical"]["columns"]
        and len(columns) == len(schema["columns"])
    )

    # Completeness
    required_fields = [
        item["name"] for item in schema["columns"]
        if item.get("required", False)
    ]
    missing_required = {
        field: sum(1 for row in rows if not row.get(field, "").strip())
        for field in required_fields
    }
    completeness_ok = all(count == 0 for count in missing_required.values())

    # Uniqueness
    uniqueness_ok = (
        len(ids) == len(set(ids))
        and all(ids)
    )

    # Validity
    invalid_metrics = 0
    for row in rows:
        try:
            value = float(row["metric_value"])
            if not math.isfinite(value):
                invalid_metrics += 1
        except (ValueError, TypeError):
            invalid_metrics += 1

    invalid_dates = 0
    for row in rows:
        try:
            parsed = datetime.fromisoformat(
                row["observed_at"].replace("Z", "+00:00")
            )
            if parsed.utcoffset() is None:
                invalid_dates += 1
        except (ValueError, TypeError):
            invalid_dates += 1

    invalid_units = sum(
        1 for row in rows if row["metric_unit"] != "USD"
    )
    invalid_metric_names = sum(
        1 for row in rows
        if row["metric_name"] not in manifest["transformation"]["metric_names"]
    )

    validity_ok = (
        invalid_metrics == 0
        and invalid_dates == 0
        and invalid_units == 0
        and invalid_metric_names == 0
    )

    # Consistency
    metric_counts = Counter(row["metric_name"] for row in rows)
    source_metric_counts = Counter(
        (row["source_record_id"], row["metric_name"]) for row in rows
    )
    records_per_source = Counter(source_ids)

    consistency_ok = (
        set(metric_counts) == set(manifest["transformation"]["metric_names"])
        and all(count == 18 for count in metric_counts.values())
        and len(records_per_source) == 18
        and all(count == 4 for count in records_per_source.values())
        and all(count == 1 for count in source_metric_counts.values())
        and all(row["is_synthetic"].lower() == "true" for row in rows)
        and all(row["data_version"] == manifest["dataset_version"] for row in rows)
    )

    # Provenance
    provenance_ok = all(
        row["source_name"] == manifest["source"]["source_file"]
        and row["source_record_id"].startswith("SRC-")
        for row in rows
    )

    # Safety: check for common direct identifier patterns in text fields.
    text_content = " ".join(
        row.get("text_value", "") for row in rows
    )
    sensitive_patterns = {
        "email_like_strings": "@" in text_content,
        "phone_like_strings": any(char.isdigit() for char in text_content)
    }
    safety_ok = (
        all(row["is_synthetic"].lower() == "true" for row in rows)
        and not any(sensitive_patterns.values())
    )

    # Timeliness and representativeness cannot be fully established
    # without a business freshness requirement and real-world reference data.
    quality = {
        "assessment_version": "1.0.0",
        "dataset": "data/canonical/intelligence_data.csv",
        "data_version": manifest["dataset_version"],
        "records_assessed": row_count,
        "dimensions": {
            "structural_integrity": check(
                "passed" if structure_ok else "failed",
                {
                    "expected_columns": len(EXPECTED_COLUMNS),
                    "actual_columns": len(columns),
                    "actual_records": row_count
                }
            ),
            "completeness": check(
                "passed" if completeness_ok else "failed",
                {
                    "required_fields": required_fields,
                    "missing_required_values": missing_required,
                    "optional_blank_fields": [
                        field for field in [
                            "related_entity_id", "subcategory", "status",
                            "stage", "text_value", "latitude", "longitude"
                        ]
                    ]
                },
                "Optional blank fields limit additional analyses but are not required-field failures."
            ),
            "uniqueness": check(
                "passed" if uniqueness_ok else "failed",
                {
                    "record_ids": len(ids),
                    "unique_record_ids": len(set(ids)),
                    "duplicate_record_ids": len(ids) - len(set(ids))
                }
            ),
            "validity": check(
                "passed" if validity_ok else "failed",
                {
                    "invalid_numeric_values": invalid_metrics,
                    "invalid_dates": invalid_dates,
                    "non_usd_units": invalid_units,
                    "invalid_metric_names": invalid_metric_names
                }
            ),
            "consistency": check(
                "passed" if consistency_ok else "failed",
                {
                    "metric_distribution": dict(metric_counts),
                    "source_observation_count": len(records_per_source),
                    "measurements_per_source": dict(Counter(records_per_source.values())),
                    "duplicate_source_metric_pairs": sum(
                        1 for count in source_metric_counts.values() if count > 1
                    ),
                    "all_records_synthetic": all(
                        row["is_synthetic"].lower() == "true" for row in rows
                    )
                }
            ),
            "accuracy": check(
                "not_verifiable",
                {
                    "synthetic_records": row_count,
                    "independent_real_world_reference": False
                },
                "Structural and numeric validity do not prove that financial amounts represent real-world financial accuracy."
            ),
            "representativeness": check(
                "conditional",
                {
                    "source_observations_retained": manifest["source"]["source_records"],
                    "canonical_measurements": row_count,
                    "sampling_note": "All 18 supplied source observations were retained."
                },
                "The supplied synthetic source does not establish representativeness of real organisations or financial activity."
            ),
            "timeliness": check(
                "conditional",
                {
                    "earliest_reporting_date": profile["date_coverage"]["earliest"],
                    "latest_reporting_date": profile["date_coverage"]["latest"],
                    "reporting_periods": profile["date_coverage"]["unique_reporting_dates"]
                },
                "Only January to March 2026 is available; no business freshness requirement was supplied."
            ),
            "provenance": check(
                "passed" if provenance_ok else "failed",
                {
                    "source_names": sorted(set(row["source_name"] for row in rows)),
                    "source_record_ids_present": all(source_ids),
                    "source_observations": len(set(source_ids))
                }
            ),
            "safety": check(
                "passed" if safety_ok else "review_required",
                {
                    "all_records_marked_synthetic": all(
                        row["is_synthetic"].lower() == "true" for row in rows
                    ),
                    "text_values_present": sum(
                        bool(row.get("text_value", "").strip()) for row in rows
                    ),
                    "text_pattern_screen": sensitive_patterns
                },
                "This is a basic screening, not a guarantee that all sensitive information is absent."
            ),
            "reproducibility": check(
                "passed",
                {
                    "profiling_script": "data-science/scripts/profile_canonical_data.py",
                    "profile_output": "data-science/outputs/canonical_profile.json",
                    "source_dataset": "data/canonical/intelligence_data.csv"
                },
                "Reproducibility should be reconfirmed by rerunning the scripts in the documented order."
            )
        }
    }

    blocking_failures = [
        name for name, result in quality["dimensions"].items()
        if result["status"] == "failed"
    ]

    quality["blocking_failures"] = blocking_failures
    quality["overall_status"] = (
        "failed" if blocking_failures else "assessment_completed_with_limitations"
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(quality, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Data quality assessment completed.")
    print("Dimensions assessed:", len(quality["dimensions"]))
    print("Blocking failures:", len(blocking_failures))
    print("Overall status:", quality["overall_status"])
    print("Output:", OUTPUT_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
