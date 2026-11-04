
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "data/canonical/intelligence_data.csv"
SCHEMA_FILE = ROOT / "data/schema.json"
MANIFEST_FILE = ROOT / "data/manifest.json"
OUTPUT_FILE = ROOT / "data-science/outputs/canonical_profile.json"


def parse_date(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except (ValueError, AttributeError):
        return None


def distribution(values):
    return dict(sorted(Counter(values).items()))


def read_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def clean_values(records, field):
    return [
        row.get(field, "").strip()
        for row in records
        if row.get(field, "").strip()
    ]


def main():
    for path in (DATA_FILE, SCHEMA_FILE, MANIFEST_FILE):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        records = list(reader)

    if not columns:
        raise ValueError("Canonical CSV has no column headers.")

    if not records:
        raise ValueError("Canonical dataset contains no records.")

    schema = read_json(SCHEMA_FILE)
    manifest = read_json(MANIFEST_FILE)

    schema_columns = {
        item["name"]: item for item in schema.get("columns", [])
    }

    row_count = len(records)
    column_count = len(columns)
    file_size = DATA_FILE.stat().st_size

    # ---------------------------------------------------------
    # 1. Schema and manifest metadata
    # ---------------------------------------------------------

    expected_columns = list(schema_columns.keys())

    schema_check = {
        "schema_version": schema.get("schema_version"),
        "declared_row_count": schema.get("row_count"),
        "observed_row_count": row_count,
        "declared_column_count": schema.get("column_count"),
        "observed_column_count": column_count,
        "missing_columns": [
            name for name in expected_columns if name not in columns
        ],
        "unexpected_columns": [
            name for name in columns if name not in expected_columns
        ],
        "column_order_matches_schema": columns == expected_columns,
        "row_count_matches_schema": row_count == schema.get("row_count"),
        "column_count_matches_schema": (
            column_count == schema.get("column_count")
        )
    }

    manifest_canonical = manifest.get("canonical", {})
    declared_dataset_version = manifest.get("dataset_version")
    declared_metrics = manifest.get("transformation", {}).get(
        "metric_names", []
    )

    # ---------------------------------------------------------
    # 2. Field completeness and uniqueness
    # ---------------------------------------------------------

    field_profiles = {}

    for column in columns:
        values = [row.get(column, "") or "" for row in records]
        non_null = [value for value in values if value.strip() != ""]
        null_count = row_count - len(non_null)

        field_profiles[column] = {
            "non_null_count": len(non_null),
            "null_count": null_count,
            "null_percentage": round(null_count / row_count * 100, 2),
            "unique_count": len(set(non_null)),
            "uniqueness_percentage": round(
                len(set(non_null)) / len(non_null) * 100, 2
            ) if non_null else 0,
            "examples": list(dict.fromkeys(non_null))[:5],
            "required_by_schema": schema_columns.get(
                column, {}
            ).get("required"),
            "nullable_by_schema": schema_columns.get(
                column, {}
            ).get("nullable"),
            "expected_role": schema_columns.get(
                column, {}
            ).get("description", "Not documented in schema")
        }

    # ---------------------------------------------------------
    # 3. Numeric metric profile
    # ---------------------------------------------------------

    numeric_values = []
    invalid_numeric_count = 0
    infinite_numeric_count = 0

    for row in records:
        value = (row.get("metric_value") or "").strip()

        try:
            number = float(value)
            if math.isfinite(number):
                numeric_values.append(number)
            else:
                infinite_numeric_count += 1
        except (ValueError, TypeError):
            invalid_numeric_count += 1

    metric_statistics = {
        "total_records": row_count,
        "valid_finite_count": len(numeric_values),
        "invalid_count": invalid_numeric_count,
        "infinite_count": infinite_numeric_count,
        "minimum": min(numeric_values) if numeric_values else None,
        "maximum": max(numeric_values) if numeric_values else None,
        "mean": round(statistics.mean(numeric_values), 4)
        if numeric_values else None,
        "median": statistics.median(numeric_values)
        if numeric_values else None,
        "standard_deviation_sample": (
            round(statistics.stdev(numeric_values), 4)
            if len(numeric_values) > 1 else None
        ),
        "unit_distribution": distribution(
            row.get("metric_unit", "") or "(blank)"
            for row in records
        ),
        "metric_distribution": distribution(
            row.get("metric_name", "") or "(blank)"
            for row in records
        )
    }

    # ---------------------------------------------------------
    # 4. Temporal coverage
    # ---------------------------------------------------------

    raw_dates = [row.get("observed_at", "") or "" for row in records]
    parsed_dates = [parse_date(value) for value in raw_dates]
    valid_dates = [value for value in parsed_dates if value is not None]
    unique_dates = sorted(set(valid_dates))

    date_profile = {
        "total_values": len(raw_dates),
        "parseable_count": len(valid_dates),
        "unparseable_count": len(raw_dates) - len(valid_dates),
        "parse_rate_percentage": round(
            len(valid_dates) / len(raw_dates) * 100, 2
        ) if raw_dates else 0,
        "earliest": min(valid_dates).isoformat() if valid_dates else None,
        "latest": max(valid_dates).isoformat() if valid_dates else None,
        "unique_reporting_dates": len(unique_dates),
        "reporting_dates": [
            value.isoformat() for value in unique_dates
        ],
        "timezone_offsets": sorted({
            str(value.utcoffset()) for value in valid_dates
        })
    }

    months = sorted({
        (value.year, value.month) for value in valid_dates
    })

    missing_months = []

    if months:
        current_year, current_month = months[0]
        last_year, last_month = months[-1]
        observed_months = set(months)

        while (current_year, current_month) <= (last_year, last_month):
            if (current_year, current_month) not in observed_months:
                missing_months.append(
                    f"{current_year}-{current_month:02d}"
                )

            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

    date_profile["missing_months_between_endpoints"] = missing_months

    # ---------------------------------------------------------
    # 5. Categorical distributions
    # ---------------------------------------------------------

    categorical_fields = [
        "record_type",
        "entity_id",
        "entity_name",
        "related_entity_id",
        "category",
        "subcategory",
        "status",
        "stage",
        "metric_name",
        "metric_unit",
        "source_name",
        "source_record_id",
        "is_synthetic",
        "data_version"
    ]

    categorical_profiles = {}

    for column in categorical_fields:
        if column in columns:
            categorical_profiles[column] = distribution(
                row.get(column, "") or "(blank)"
                for row in records
            )

    # ---------------------------------------------------------
    # 6. Geographic coverage
    # ---------------------------------------------------------

    latitude_values = clean_values(records, "latitude")
    longitude_values = clean_values(records, "longitude")

    valid_coordinate_pairs = 0
    invalid_coordinate_pairs = 0
    partial_coordinate_pairs = 0
    empty_coordinate_pairs = 0

    for row in records:
        lat = (row.get("latitude") or "").strip()
        lon = (row.get("longitude") or "").strip()

        if bool(lat) != bool(lon):
            partial_coordinate_pairs += 1
        elif not lat and not lon:
            empty_coordinate_pairs += 1
        else:
            try:
                lat_num = float(lat)
                lon_num = float(lon)

                if (
                    math.isfinite(lat_num)
                    and math.isfinite(lon_num)
                    and -90 <= lat_num <= 90
                    and -180 <= lon_num <= 180
                ):
                    valid_coordinate_pairs += 1
                else:
                    invalid_coordinate_pairs += 1
            except (ValueError, TypeError):
                invalid_coordinate_pairs += 1

    geographic_profile = {
        "latitude_non_null": len(latitude_values),
        "longitude_non_null": len(longitude_values),
        "valid_coordinate_pairs": valid_coordinate_pairs,
        "invalid_coordinate_pairs": invalid_coordinate_pairs,
        "partial_coordinate_pairs": partial_coordinate_pairs,
        "empty_coordinate_pairs": empty_coordinate_pairs
    }

    # ---------------------------------------------------------
    # 7. Text coverage
    # ---------------------------------------------------------

    text_values = clean_values(records, "text_value")
    text_lengths = [len(value) for value in text_values]

    text_profile = {
        "non_empty_count": len(text_values),
        "empty_count": row_count - len(text_values),
        "average_length": round(
            statistics.mean(text_lengths), 2
        ) if text_lengths else 0,
        "maximum_length": max(text_lengths, default=0),
        "maximum_allowed_length": schema_columns.get(
            "text_value", {}
        ).get("max_length"),
        "examples": text_values[:5]
    }

    # ---------------------------------------------------------
    # 8. Source provenance and source relationships
    # ---------------------------------------------------------

    source_ids = clean_values(records, "source_record_id")
    source_id_counts = Counter(source_ids)

    metrics_by_source = defaultdict(list)

    for row in records:
        source_id = (row.get("source_record_id") or "").strip()
        metric_name = (row.get("metric_name") or "").strip()

        if source_id:
            metrics_by_source[source_id].append(metric_name)

    metrics_per_source = Counter(
        len(metrics) for metrics in metrics_by_source.values()
    )

    metric_sets_per_source = Counter(
        tuple(sorted(metrics))
        for metrics in metrics_by_source.values()
    )

    duplicate_source_metric_pairs = sum(
        1
        for row in records
        if (row.get("source_record_id") or "").strip()
        and (row.get("metric_name") or "").strip()
    ) - len({
        (
            (row.get("source_record_id") or "").strip(),
            (row.get("metric_name") or "").strip()
        )
        for row in records
        if (row.get("source_record_id") or "").strip()
        and (row.get("metric_name") or "").strip()
    })

    provenance_profile = {
        "source_name_distribution": distribution(
            row.get("source_name", "") or "(blank)"
            for row in records
        ),
        "unique_source_record_count": len(source_id_counts),
        "source_record_id_distribution": distribution(source_id_counts),
        "records_per_source_observation": distribution(
            str(key) for key in metrics_per_source
        ),
        "records_per_source_observation_distribution": {
            str(key): value
            for key, value in sorted(metrics_per_source.items())
        },
        "metric_sets_per_source_observation": {
            "|".join(key): value
            for key, value in sorted(metric_sets_per_source.items())
        },
        "duplicate_source_metric_pairs": duplicate_source_metric_pairs,
        "all_records_have_source_ids": (
            len(source_ids) == row_count
        )
    }

    # ---------------------------------------------------------
    # 9. Synthetic and version profile
    # ---------------------------------------------------------

    synthetic_values = distribution(
        row.get("is_synthetic", "") or "(blank)"
        for row in records
    )

    observed_versions = distribution(
        row.get("data_version", "") or "(blank)"
        for row in records
    )

    version_profile = {
        "manifest_dataset_version": declared_dataset_version,
        "schema_version": schema.get("schema_version"),
        "observed_data_versions": observed_versions,
        "all_records_match_manifest_version": all(
            (row.get("data_version") or "").strip()
            == str(declared_dataset_version)
            for row in records
        ),
        "schema_version_matches_manifest": (
            schema.get("schema_version")
            == manifest.get("schema_version")
        )
    }

    # ---------------------------------------------------------
    # 10. Derived record relationships
    # ---------------------------------------------------------

    observed_metrics = sorted({
        (row.get("metric_name") or "").strip()
        for row in records
        if (row.get("metric_name") or "").strip()
    })

    expected_metric_set = set(declared_metrics)
    observed_metric_set = set(observed_metrics)

    expected_source_count = manifest.get(
        "source", {}
    ).get("source_records")

    source_relationship_profile = {
        "manifest_source_observation_count": expected_source_count,
        "observed_unique_source_observation_count": len(metrics_by_source),
        "expected_metrics": sorted(expected_metric_set),
        "observed_metrics": observed_metrics,
        "missing_metrics": sorted(
            expected_metric_set - observed_metric_set
        ),
        "unexpected_metrics": sorted(
            observed_metric_set - expected_metric_set
        ),
        "canonical_records_per_source_distribution": {
            str(key): value
            for key, value in sorted(metrics_per_source.items())
        },
        "source_observation_count_matches_manifest": (
            len(metrics_by_source) == expected_source_count
        ),
        "all_sources_have_expected_metric_set": all(
            set(metrics) == expected_metric_set
            for metrics in metrics_by_source.values()
        ) and bool(metrics_by_source),
        "canonical_rows_are_independent_transactions": False
    }

    # ---------------------------------------------------------
    # 11. Final profile
    # ---------------------------------------------------------

    result = {
        "profile_version": "2.0.0",
        "dataset": "data/canonical/intelligence_data.csv",
        "dataset_name": manifest.get("dataset_name"),
        "data_version": declared_dataset_version,
        "schema_version": schema.get("schema_version"),
        "record_count": row_count,
        "column_count": column_count,
        "file_size_bytes": file_size,
        "columns_in_order": columns,
        "schema_check": schema_check,
        "record_type_distribution": categorical_profiles.get(
            "record_type", {}
        ),
        "unique_entity_count": len(set(
            clean_values(records, "entity_id")
        )),
        "unique_related_entity_count": len(set(
            clean_values(records, "related_entity_id")
        )),
        "source_distribution": categorical_profiles.get(
            "source_name", {}
        ),
        "synthetic_distribution": synthetic_values,
        "field_completeness": field_profiles,
        "numeric_metric_profile": metric_statistics,
        "date_coverage": date_profile,
        "categorical_distributions": categorical_profiles,
        "geographic_profile": geographic_profile,
        "text_profile": text_profile,
        "provenance_profile": provenance_profile,
        "version_profile": version_profile,
        "source_relationship_profile": source_relationship_profile,
        "interpretation": {
            "all_records_synthetic": (
                len(synthetic_values) == 1
                and "true" in synthetic_values
            ),
            "canonical_rows_are_independent_transactions": False,
            "forecast_values_are_validated_predictions": False,
            "source_mapping_requires_separate_representativeness_assessment": True,
            "real_world_representativeness_established": False
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Canonical profiling completed.")
    print("Records:", row_count)
    print("Columns:", column_count)
    print("Dataset version:", declared_dataset_version)
    print("Schema version:", schema.get("schema_version"))
    print("File size:", file_size, "bytes")
    print("Valid finite numeric values:", len(numeric_values))
    print("Parseable dates:", len(valid_dates))
    print(
        "Unique source observations:",
        len(metrics_by_source)
    )
    print(
        "Duplicate source-metric pairs:",
        duplicate_source_metric_pairs
    )
    print("Output:", OUTPUT_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
