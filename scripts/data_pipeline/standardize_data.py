
from pathlib import Path
from datetime import datetime, timezone
import csv
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = PROJECT_ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "canonical" / "intelligence_data.csv"

SOURCE_COLUMNS = [
    "cost_centre",
    "department",
    "account_category",
    "month",
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
]

CANONICAL_COLUMNS = [
    "record_id",
    "record_type",
    "observed_at",
    "entity_id",
    "related_entity_id",
    "entity_name",
    "category",
    "subcategory",
    "status",
    "stage",
    "metric_name",
    "metric_value",
    "metric_unit",
    "text_value",
    "latitude",
    "longitude",
    "source_name",
    "source_record_id",
    "is_synthetic",
    "data_version",
]

FINANCIAL_MEASURES = [
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
]

DATA_VERSION = "1.0.0"
SOURCE_NAME = "backend/budget_data.csv"


def convert_month(month_text):
    """Convert Mon YYYY into the first day of that month in UTC."""
    parsed = datetime.strptime(month_text, "%b %Y")
    return parsed.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0,
        tzinfo=timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    print("Starting canonical data standardization...")

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != SOURCE_COLUMNS:
            raise ValueError(
                f"Unexpected source columns: {reader.fieldnames}"
            )

        source_rows = list(reader)

    if not source_rows:
        raise ValueError("Source dataset is empty.")

    canonical_rows = []

    for source_index, source_row in enumerate(source_rows, start=1):
        source_record_id = f"SRC-{source_index:04d}"
        observed_at = convert_month(source_row["month"])

        for measure in FINANCIAL_MEASURES:
            try:
                metric_value = float(source_row[measure])
            except (TypeError, ValueError):
                raise ValueError(
                    f"Invalid numeric value in source row "
                    f"{source_index}, column {measure}"
                )

            canonical_record = {
                "record_id": f"FIN-{source_index:04d}-{measure.upper()}",
                "record_type": "financial_metric",
                "observed_at": observed_at,
                "entity_id": source_row["cost_centre"],
                "related_entity_id": "",
                "entity_name": source_row["department"],
                "category": source_row["account_category"],
                "subcategory": "",
                "status": "",
                "stage": "",
                "metric_name": measure,
                "metric_value": format(metric_value, ".15g"),
                "metric_unit": "USD",
                "text_value": "",
                "latitude": "",
                "longitude": "",
                "source_name": SOURCE_NAME,
                "source_record_id": source_record_id,
                "is_synthetic": "true",
                "data_version": DATA_VERSION,
            }

            canonical_rows.append(canonical_record)

    expected_count = len(source_rows) * len(FINANCIAL_MEASURES)

    if len(canonical_rows) != expected_count:
        raise ValueError(
            f"Expected {expected_count} canonical records, "
            f"generated {len(canonical_rows)}."
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CANONICAL_COLUMNS,
            extrasaction="raise"
        )
        writer.writeheader()
        writer.writerows(canonical_rows)

    # Verify the written file
    with OUTPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        written_rows = list(reader)

        if reader.fieldnames != CANONICAL_COLUMNS:
            raise ValueError("Canonical column order verification failed.")

    if len(written_rows) != expected_count:
        raise ValueError("Canonical output record count verification failed.")

    record_ids = [row["record_id"] for row in written_rows]

    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Duplicate canonical record IDs detected.")

    print("Canonical standardization completed successfully.")
    print(f"Source records: {len(source_rows)}")
    print(f"Canonical records: {len(written_rows)}")
    print(f"Canonical columns: {len(CANONICAL_COLUMNS)}")
    print("Unique record IDs: verified")
    print(f"Output: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"STANDARDIZATION FAILED: {error}")
        sys.exit(1)
