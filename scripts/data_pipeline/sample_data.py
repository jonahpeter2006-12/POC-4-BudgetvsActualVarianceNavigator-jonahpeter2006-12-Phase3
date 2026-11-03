
from pathlib import Path
import csv
import json
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = PROJECT_ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT_REPORT = PROJECT_ROOT / "data" / "quality" / "sampling_report.md"

EXPECTED_RECORDS = 18


def main():
    print("Starting sampling and reduction process...")

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source sample not found: {SOURCE_FILE}")

    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        rows = list(reader)

    if len(rows) != EXPECTED_RECORDS:
        raise ValueError(
            f"Expected {EXPECTED_RECORDS} records, found {len(rows)}."
        )

    # Retain the complete dataset: no filtering or random sampling.
    sampled_rows = rows.copy()

    if len(sampled_rows) != len(rows):
        raise ValueError("Record preservation check failed.")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    report = f"""# Sampling and Reduction Report

## Dataset Information

- Source: `data/source-sample/source_sample.csv`
- Original records: {len(rows)}
- Retained records: {len(sampled_rows)}
- Source columns: {len(columns)}
- Sampling method: Complete dataset retention
- Random sampling: Not applied
- Record reduction: None

## Sampling Decision

All {len(rows)} source records were retained.

The dataset is small enough to process in full. Retaining every
record preserves all available departments, cost centres,
account categories, reporting months, and financial measures.

## Preservation Check

- Original record count: {len(rows)}
- Retained record count: {len(sampled_rows)}
- Records excluded: 0
- Records lost: 0
- Preservation status: PASSED

## Canonical Expansion Plan

Each source record will later produce four canonical financial
measure records:

- budget_amount
- actual_amount
- committed_amount
- forecast_amount

Expected canonical records: {len(sampled_rows)} × 4 = {len(sampled_rows) * 4}

## Generated Information

- Report generated at: {datetime.now(timezone.utc).isoformat()}
- Sampling script: `scripts/data_pipeline/sample_data.py`
"""

    OUTPUT_REPORT.write_text(report, encoding="utf-8")

    print("Sampling completed successfully.")
    print(f"Original records: {len(rows)}")
    print(f"Retained records: {len(sampled_rows)}")
    print("Records excluded: 0")
    print(f"Expected canonical records: {len(sampled_rows) * 4}")
    print(f"Report: {OUTPUT_REPORT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
