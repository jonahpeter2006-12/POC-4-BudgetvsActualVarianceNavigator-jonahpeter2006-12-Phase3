import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRACK_SCRIPT_DIR = (
    PROJECT_ROOT / "data-science" / "scripts" / "track-specific"
)

sys.path.insert(0, str(TRACK_SCRIPT_DIR))

from comparative_intelligence import run_analysis


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generated-at",
        help="Optional fixed UTC timestamp for reproducibility checks."
    )
    args = parser.parse_args()
    canonical_csv = (
        PROJECT_ROOT / "data" / "canonical" / "intelligence_data.csv"
    )

    output_dir = (
        PROJECT_ROOT / "data-science" / "outputs"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    generated_at = args.generated_at or (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    result = run_analysis(
        canonical_csv,
        generated_at=generated_at
    )

    output_file = output_dir / "intelligence_results.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=2,
            ensure_ascii=False
        )
        file.write("\n")

    print("ANALYTICAL TRACK EXECUTION")
    print("Approved track:", result["approved_track"])
    print("Method version:", result["method_version"])
    print("Dataset version:", result["dataset_version"])
    print("Total findings:", result["result_count"])
    print("Output file:", output_file.relative_to(PROJECT_ROOT))
    print("Execution status: SUCCESS")


if __name__ == "__main__":
    main()
