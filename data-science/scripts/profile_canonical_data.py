import csv
import json
import math
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data/canonical/intelligence_data.csv"
SCHEMA_FILE = ROOT / "data/schema.json"
OUTPUT_FILE = ROOT / "data-science/outputs/canonical_profile.json"

def parse_date(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None

def distribution(values):
    counts = Counter(values)
    return dict(sorted(counts.items()))

def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Canonical dataset not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        records = list(reader)

    if not records:
        raise ValueError("Canonical dataset contains no records.")

    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    schema_columns = {
        item["name"]: item for item in schema.get("columns", [])
    }

    row_count = len(records)
    file_size = DATA_FILE.stat().st_size

    # Field-level completeness and uniqueness
    field_profiles = {}

    for column in columns:
        values = [row.get(column, "") for row in records]
        non_null = [value for value in values if value.strip() != ""]
        null_count = row_count - len(non_null)

        field_profiles[column] = {
            "non_null_count": len(non_null),
            "null_count": null_count,
            "null_percentage": round(null_count / row_count * 100, 2),
            "unique_count": len(set(non_null)),
            "examples": list(dict.fromkeys(non_null))[:5],
            "expected_role": schema_columns.get(column, {}).get(
                "description", "Not documented in schema"
            )
        }

    # Numeric metric profiling
    numeric_values = []
    invalid_numeric_count = 0
    infinite_numeric_count = 0

    for row in records:
        value = row.get("metric_value", "").strip()
        try:
            number = float(value)
            if not math.isfinite(number):
                infinite_numeric_count += 1
            else:
                numeric_values.append(number)
        except (ValueError, TypeError):
            invalid_numeric_count += 1

    metric_statistics = {}

    if numeric_values:
        metric_statistics = {
            "non_null_valid_count": len(numeric_values),
            "invalid_count": invalid_numeric_count,
            "infinite_count": infinite_numeric_count,
            "minimum": min(numeric_values),
            "maximum": max(numeric_values),
            "mean": round(statistics.mean(numeric_values), 4),
            "median": statistics.median(numeric_values),
            "standard_deviation_sample": (
                round(statistics.stdev(numeric_values), 4)
                if len(numeric_values) > 1 else 0
            ),
            "unit_distribution": distribution(
                row.get("metric_unit", "") for row in records
            ),
            "metric_distribution": distribution(
                row.get("metric_name", "") for row in records
            )
        }

    # Date coverage
    raw_dates = [row.get("observed_at", "") for row in records]
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
        "reporting_dates": [value.isoformat() for value in unique_dates],
        "timezone_offsets": sorted({
            str(value.utcoffset()) for value in valid_dates
        })
    }

    # Monthly gaps
    months = sorted({
        (value.year, value.month) for value in valid_dates
    })
    missing_months = []

    if months:
        current_year, current_month = months[0]
        last_year, last_month = months[-1]

        while (current_year, current_month) <= (last_year, last_month):
            if (current_year, current_month) not in months:
                missing_months.append(
                    f"{current_year}-{current_month:02d}"
                )
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1

    date_profile["missing_months_between_endpoints"] = missing_months

    # Categorical distributions
    categorical_profiles = {}

    for column in [
        "record_type", "entity_id", "entity_name", "category",
        "status", "stage", "metric_name", "metric_unit",
        "source_name", "is_synthetic", "data_version"
    ]:
        if column in columns:
            categorical_profiles[column] = distribution(
                row.get(column, "") or "(blank)" for row in records
            )

    # Geographic and text coverage
    latitude_values = [
        row.get("latitude", "").strip() for row in records
        if row.get("latitude", "").strip()
    ]
    longitude_values = [
        row.get("longitude", "").strip() for row in records
        if row.get("longitude", "").strip()
    ]

    geographic_profile = {
        "latitude_non_null": len(latitude_values),
        "longitude_non_null": len(longitude_values),
        "valid_coordinate_pairs": 0,
        "invalid_coordinate_pairs": 0
    }

    for row in records:
        lat = row.get("latitude", "").strip()
        lon = row.get("longitude", "").strip()

        if lat and lon:
            try:
                lat_num, lon_num = float(lat), float(lon)
                if (
                    math.isfinite(lat_num) and math.isfinite(lon_num)
                    and -90 <= lat_num <= 90
                    and -180 <= lon_num <= 180
                ):
                    geographic_profile["valid_coordinate_pairs"] += 1
                else:
                    geographic_profile["invalid_coordinate_pairs"] += 1
            except ValueError:
                geographic_profile["invalid_coordinate_pairs"] += 1

    text_values = [
        row.get("text_value", "") for row in records
        if row.get("text_value", "").strip()
    ]

    text_profile = {
        "non_empty_count": len(text_values),
        "empty_count": row_count - len(text_values),
        "average_length": round(
            statistics.mean([len(value) for value in text_values]), 2
        ) if text_values else 0,
        "maximum_length": max(
            [len(value) for value in text_values], default=0
        )
    }

    result = {
        "profile_version": "1.0.0",
        "dataset": "data/canonical/intelligence_data.csv",
        "data_version": schema.get("schema_version"),
        "record_count": row_count,
        "column_count": len(columns),
        "file_size_bytes": file_size,
        "columns_in_order": columns,
        "record_type_distribution": categorical_profiles.get(
            "record_type", {}
        ),
        "unique_entity_count": len({
            row.get("entity_id", "") for row in records
            if row.get("entity_id", "")
        }),
        "unique_related_entity_count": len({
            row.get("related_entity_id", "") for row in records
            if row.get("related_entity_id", "")
        }),
        "source_distribution": categorical_profiles.get(
            "source_name", {}
        ),
        "synthetic_distribution": categorical_profiles.get(
            "is_synthetic", {}
        ),
        "field_completeness": field_profiles,
        "numeric_metric_profile": metric_statistics,
        "date_coverage": date_profile,
        "categorical_distributions": categorical_profiles,
        "geographic_profile": geographic_profile,
        "text_profile": text_profile,
        "interpretation": {
            "source_observations": 18,
            "canonical_measurements_per_source_observation": 4,
            "canonical_rows_are_independent_transactions": False,
            "forecast_values_are_validated_predictions": False
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Canonical profiling completed.")
    print("Records:", row_count)
    print("Columns:", len(columns))
    print("File size:", file_size, "bytes")
    print("Valid numeric values:", len(numeric_values))
    print("Parseable dates:", len(valid_dates))
    print("Output:", OUTPUT_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
