
import csv
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
SOURCE_FILE = DATA_DIR / "source-sample" / "source_sample.csv"
CANONICAL_FILE = DATA_DIR / "canonical" / "intelligence_data.csv"
SCHEMA_FILE = DATA_DIR / "schema.json"
MANIFEST_FILE = DATA_DIR / "manifest.json"
REPORT_FILE = DATA_DIR / "quality" / "validation_report.json"

EXPECTED_COLUMNS = [
    "record_id", "record_type", "observed_at", "entity_id",
    "related_entity_id", "entity_name", "category", "subcategory",
    "status", "stage", "metric_name", "metric_value", "metric_unit",
    "text_value", "latitude", "longitude", "source_name",
    "source_record_id", "is_synthetic", "data_version"
]

EXPECTED_METRICS = {
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount"
}

REQUIRED_FILES = [
    DATA_DIR / "README.md",
    MANIFEST_FILE,
    SCHEMA_FILE,
    SOURCE_FILE,
    CANONICAL_FILE,
    DATA_DIR / "published" / "intelligence_data.json",
    DATA_DIR / "quality" / "data_profile.json",
    DATA_DIR / "quality" / "sampling_report.md"
]

errors = []
checks = []


def check(condition, message):
    checks.append({
        "check": message,
        "passed": bool(condition)
    })

    if not condition:
        errors.append(message)


def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


print("Starting canonical data package validation...")


# 1. Required file checks
for path in REQUIRED_FILES:
    check(
        path.is_file(),
        f"Required file exists: {path.relative_to(ROOT)}"
    )


# 2. Check core input files
if (
    not CANONICAL_FILE.is_file()
    or not SCHEMA_FILE.is_file()
    or not MANIFEST_FILE.is_file()
):
    print("Validation stopped: core input files are missing.")
    raise SystemExit(1)


# 3. Read schema and manifest
try:
    schema = read_json(SCHEMA_FILE)
    manifest = read_json(MANIFEST_FILE)

    check(True, "Schema and manifest are valid JSON")

except (json.JSONDecodeError, OSError) as error:
    print(f"Cannot read metadata: {error}")
    raise SystemExit(1)


# 4. Read canonical CSV
try:
    with CANONICAL_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        actual_columns = reader.fieldnames or []
        rows = list(reader)

except (OSError, UnicodeError, csv.Error) as error:
    print(f"Cannot read canonical CSV: {error}")
    raise SystemExit(1)


# 5. Column and structure checks
check(
    actual_columns == EXPECTED_COLUMNS,
    "Exact canonical column order"
)

check(
    actual_columns == [
        column["name"] for column in schema.get("columns", [])
    ],
    "CSV columns match schema"
)

check(len(rows) == 72, "Canonical record count is 72")
check(len(actual_columns) == 20, "Canonical column count is 20")
check(len(rows) <= 10000, "Canonical row limit")
check(len(actual_columns) <= 50, "Canonical column limit")


# 6. Record ID checks
record_ids = [row.get("record_id", "") for row in rows]

check(
    all(value.strip() for value in record_ids),
    "All record IDs are non-empty"
)

check(
    len(record_ids) == len(set(record_ids)),
    "Record IDs are unique"
)


# 7. Data type and required value checks
valid_dates = True
valid_numbers = True
valid_flags = True
valid_sources = True
valid_versions = True
valid_metrics = True
valid_record_types = True
valid_units = True
valid_text_lengths = True

for row in rows:

    try:
        datetime.strptime(
            row["observed_at"],
            "%Y-%m-%dT%H:%M:%SZ"
        )
    except (ValueError, TypeError):
        valid_dates = False

    try:
        value = float(row["metric_value"])

        if value != value or value in (float("inf"), float("-inf")):
            valid_numbers = False

    except (ValueError, TypeError):
        valid_numbers = False

    if row["is_synthetic"].lower() != "true":
        valid_flags = False

    if row["source_name"] != "backend/budget_data.csv":
        valid_sources = False

    if row["data_version"] != manifest["dataset_version"]:
        valid_versions = False

    if row["metric_name"] not in EXPECTED_METRICS:
        valid_metrics = False

    if row["record_type"] != "financial_metric":
        valid_record_types = False

    if row["metric_unit"] != "USD":
        valid_units = False

    if len(row.get("text_value", "")) > 500:
        valid_text_lengths = False


check(valid_dates, "All observed_at values use ISO 8601 UTC")
check(valid_numbers, "All metric values are numeric")
check(valid_flags, "All records are marked synthetic")
check(valid_sources, "All source names are traceable")
check(valid_versions, "All data versions match manifest")
check(valid_metrics, "All metric names are allowed")
check(valid_record_types, "All record types are financial_metric")
check(valid_units, "All metric units are USD")
check(valid_text_lengths, "Text values do not exceed 500 characters")


# 8. Metric distribution
metric_counts = Counter(
    row["metric_name"] for row in rows
)

check(
    metric_counts == {
        "budget_amount": 18,
        "actual_amount": 18,
        "committed_amount": 18,
        "forecast_amount": 18
    },
    "Exactly 18 records exist for each financial metric"
)


# 9. Source sample checks
if SOURCE_FILE.is_file():

    try:
        with SOURCE_FILE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            source_rows = list(csv.DictReader(file))

        check(
            len(source_rows) == 18,
            "Source sample contains 18 records"
        )

        check(
            len(rows) == len(source_rows) * 4,
            "Four canonical records per source record"
        )

    except (OSError, UnicodeError, csv.Error):
        check(False, "Source sample can be read")


# 10. Manifest consistency
check(
    manifest["canonical"]["records"] == len(rows),
    "Manifest record count matches CSV"
)

check(
    manifest["canonical"]["columns"] == len(actual_columns),
    "Manifest column count matches CSV"
)

check(
    manifest["canonical"]["file"]
    == "data/canonical/intelligence_data.csv",
    "Manifest canonical path is correct"
)


# 11. File-size checks
main_files = [
    SOURCE_FILE,
    CANONICAL_FILE,
    DATA_DIR / "published" / "intelligence_data.json"
]

for path in main_files:

    if path.is_file():

        check(
            path.stat().st_size <= 5 * 1024 * 1024,
            f"Main file size limit: {path.relative_to(ROOT)}"
        )


data_size = sum(
    path.stat().st_size
    for path in DATA_DIR.rglob("*")
    if path.is_file()
)

check(
    data_size <= 10 * 1024 * 1024,
    "Total data directory size limit"
)


# 12. Data directory safety
binary_extensions = {
    ".png", ".jpg", ".jpeg", ".gif",
    ".mp4", ".mp3", ".pdf", ".zip",
    ".exe", ".dll", ".bin"
}

binary_files = [
    path.relative_to(ROOT).as_posix()
    for path in DATA_DIR.rglob("*")
    if path.is_file()
    and path.suffix.lower() in binary_extensions
]

check(
    not binary_files,
    "No binary or media files under data/"
)


# 13. Published JSON validation
published_file = (
    DATA_DIR / "published" / "intelligence_data.json"
)

if published_file.is_file():

    try:
        published = read_json(published_file)

        check(
            isinstance(published, list),
            "Published JSON is a record list"
        )

        check(
            len(published) == len(rows),
            "Published JSON record count matches CSV"
        )

        # Recreate the expected JSON representation from CSV.
        # CSV values are strings, while JSON uses numbers,
        # booleans and null values.

        expected_published = []

        for row in rows:

            record = {}

            for key, value in row.items():

                if value == "":
                    record[key] = None

                elif key in {
                    "metric_value",
                    "latitude",
                    "longitude"
                }:
                    record[key] = float(value)

                elif key == "is_synthetic":
                    record[key] = (
                        value.strip().lower() == "true"
                    )

                else:
                    record[key] = value

            expected_published.append(record)

        if isinstance(published, list):

            check(
                published == expected_published,
                "Published JSON records match canonical CSV after type conversion"
            )

    except (
        json.JSONDecodeError,
        OSError,
        ValueError
    ):
        check(
            False,
            "Published JSON is valid and matches canonical data"
        )


# 14. Generate validation report
passed_count = sum(
    item["passed"] for item in checks
)

failed_count = len(checks) - passed_count

report = {
    "validation_version": "1.0.0",
    "dataset": "data/canonical/intelligence_data.csv",
    "status": "passed" if failed_count == 0 else "failed",
    "records_checked": len(rows),
    "columns_checked": len(actual_columns),
    "checks_passed": passed_count,
    "checks_failed": failed_count,
    "errors": errors,
    "checks": checks
}

REPORT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with REPORT_FILE.open("w", encoding="utf-8") as file:
    json.dump(report, file, indent=2)


# 15. Final result
print("\nValidation completed.")
print(f"Records checked: {len(rows)}")
print(f"Columns checked: {len(actual_columns)}")
print(f"Checks passed: {passed_count}")
print(f"Checks failed: {failed_count}")

print(
    f"Report: {REPORT_FILE.relative_to(ROOT)}"
)

if failed_count:

    print("\nValidation errors:")

    for error in errors:
        print(f"- {error}")

    raise SystemExit(1)

print("\nCANONICAL DATA PACKAGE CHECKS PASSED")
