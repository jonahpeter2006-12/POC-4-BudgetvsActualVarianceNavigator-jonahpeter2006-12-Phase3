import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FILE = ROOT / "data/canonical/intelligence_data.csv"
SOURCE_SAMPLE_FILE = ROOT / "data/source-sample/source_sample.csv"
OUTPUT_FILE = ROOT / "data-science/outputs/representativeness_assessment.json"

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

def main():
    canonical_columns, canonical = read_csv(CANONICAL_FILE)
    source_columns, source = read_csv(SOURCE_SAMPLE_FILE)

    if not canonical or not source:
        raise ValueError("Canonical dataset or preserved source sample is empty.")

    required_source_fields = [
        "month", "cost_centre", "department", "account_category"
    ]

    missing_source_fields = [
        field for field in required_source_fields
        if field not in source_columns
    ]

    if missing_source_fields:
        raise ValueError(
            f"Source sample is missing expected fields: {missing_source_fields}"
        )

    # Source-to-canonical coverage comparisons
    comparisons = {
        "cost_centres": {
            "source_field": "cost_centre",
            "canonical_field": "entity_id"
        },
        "departments": {
            "source_field": "department",
            "canonical_field": "entity_name"
        },
        "categories": {
            "source_field": "account_category",
            "canonical_field": "category"
        }
    }

    coverage = {}

    for name, fields in comparisons.items():
        source_values = unique_values(source, fields["source_field"])
        canonical_values = unique_values(canonical, fields["canonical_field"])

        coverage[name] = {
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

    # Compare monthly coverage
    source_months = sorted(unique_values(source, "month"))
    canonical_dates = sorted(unique_values(canonical, "observed_at"))

    # Verify four canonical measurements per source observation
    source_record_counts = Counter(
        row.get("source_record_id", "") for row in canonical
    )

    source_observation_count = len(source)
    canonical_source_id_count = len(source_record_counts)

    all_four_metrics = (
        canonical_source_id_count == source_observation_count
        and all(
            count == 4
            for count in source_record_counts.values()
        )
        and all(source_record_counts)
    )

    all_source_observations_retained = (
        canonical_source_id_count == source_observation_count
    )

    # Distribution of source observations across categories and entities
    source_distribution = {
        "cost_centre": dict(Counter(
            row["cost_centre"] for row in source
        )),
        "department": dict(Counter(
            row["department"] for row in source
        )),
        "category": dict(Counter(
            row["account_category"] for row in source
        )),
        "month": dict(Counter(
            row["month"] for row in source
        ))
    }

    checks = {
        "all_source_observations_retained": all_source_observations_retained,
        "four_metrics_per_source_observation": all_four_metrics,
        "cost_centre_coverage_preserved": coverage["cost_centres"]["all_source_values_preserved"],
        "department_coverage_preserved": coverage["departments"]["all_source_values_preserved"],
        "category_coverage_preserved": coverage["categories"]["all_source_values_preserved"]
    }

    result = {
        "assessment_version": "1.0.0",
        "canonical_dataset": "data/canonical/intelligence_data.csv",
        "representativeness_reference": "data/source-sample/source_sample.csv",
        "canonical_record_count": len(canonical),
        "source_observation_count": source_observation_count,
        "canonical_source_id_count": canonical_source_id_count,
        "transformation_note": (
            "Canonical records are four financial measurements derived from "
            "each source observation, not independent transactions."
        ),
        "coverage_comparison": coverage,
        "temporal_coverage": {
            "source_month_values": source_months,
            "canonical_reporting_dates": canonical_dates,
            "source_month_count": len(source_months),
            "canonical_reporting_period_count": len(canonical_dates)
        },
        "source_observation_distributions": source_distribution,
        "checks": checks,
        "all_mapping_coverage_checks_passed": all(checks.values()),
        "limitations": [
            "All supplied observations are synthetic.",
            "All 18 available source observations were retained; this does not prove that the source represents real-world financial activity.",
            "Only January to March 2026 is covered.",
            "The preserved source sample is the available comparison reference, not an independent external population.",
            "The 72 canonical rows must not be interpreted as 72 independent source observations."
        ],
        "assessment": (
            "source_coverage_preserved_with_real_world_limitations"
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
    print("Source observations:", source_observation_count)
    print("Canonical records:", len(canonical))
    print("Coverage checks passed:", sum(checks.values()), "/", len(checks))
    print("Assessment:", result["assessment"])
    print("Output:", OUTPUT_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
