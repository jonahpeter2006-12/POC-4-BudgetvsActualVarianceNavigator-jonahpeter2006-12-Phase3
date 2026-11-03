
from pathlib import Path
import csv
import shutil
import sys

# Locate the project root automatically
PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = PROJECT_ROOT / "backend" / "budget_data.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "source-sample" / "source_sample.csv"

REQUIRED_COLUMNS = [
    "cost_centre",
    "department",
    "account_category",
    "month",
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
]


def main():
    print("Starting source data extraction...")

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

    # Validate the source CSV before copying
    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(
                f"Unexpected source columns: {reader.fieldnames}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("The source dataset is empty.")

    # Create the destination folder if necessary
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Copy the original file without changing its contents
    shutil.copyfile(SOURCE_FILE, OUTPUT_FILE)

    # Verify the copied file
    with OUTPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        copied_rows = list(csv.DictReader(file))

    if len(rows) != len(copied_rows):
        raise ValueError("Source and copied record counts do not match.")

    if SOURCE_FILE.read_bytes() != OUTPUT_FILE.read_bytes():
        raise ValueError("The copied file does not match the original.")

    print("Extraction completed successfully.")
    print(f"Source records: {len(rows)}")
    print(f"Source columns: {len(REQUIRED_COLUMNS)}")
    print(f"Output file: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print("Original source file remains unchanged.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"EXTRACTION FAILED: {error}")
        sys.exit(1)
