
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "canonical"
OUTPUT_DIR = REPO_ROOT / "data-science" / "outputs"

CANONICAL_FILE = DATA_DIR / "intelligence_data.csv"
RESULTS_FILE = OUTPUT_DIR / "intelligence_results.json"
REPORT_FILE = OUTPUT_DIR / "sensitivity_review.json"

METHOD_FILE = (
    REPO_ROOT
    / "data-science"
    / "scripts"
    / "track-specific"
    / "comparative_intelligence.py"
)


def load_method():
    """Load the existing approved analytical method without modifying it."""

    spec = importlib.util.spec_from_file_location(
        "comparative_intelligence",
        METHOD_FILE,
    )

    if spec is None or spec.loader is None:
        raise ImportError("Could not load the approved analytical method.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")


def overall_findings(results: list[dict]) -> dict:
    """Index overall comparisons by result type and group."""

    return {
        (item["result_type"], item["group_key"]): item
        for item in results
        if not item["result_type"].startswith("monthly_")
    }


def main() -> None:
    if not CANONICAL_FILE.is_file():
        raise FileNotFoundError(CANONICAL_FILE)

    if not RESULTS_FILE.is_file():
        raise FileNotFoundError(RESULTS_FILE)

    method = load_method()
    published = load_json(RESULTS_FILE)

    if (
        published["method_version"] != method.METHOD_VERSION
        or published["dataset_version"] != method.DATASET_VERSION
    ):
        raise ValueError(
            "Published analytical versions do not match the approved method."
        )

    # Load the canonical dataset and run the approved method.
    canonical = pd.read_csv(CANONICAL_FILE)
    original_paired = method.load_and_pair(CANONICAL_FILE)

    original_results = method.build_comparisons(
        original_paired,
        generated_at=published["generated_at"],
    )

    # Confirm that the regenerated original findings match the published output.
    published_overall = overall_findings(published["results"])
    regenerated_overall = overall_findings(original_results)

    if set(published_overall) != set(regenerated_overall):
        raise ValueError(
            "Regenerated overall findings do not match published findings."
        )

    for key, regenerated in regenerated_overall.items():
        published_item = published_overall[key]

        for field in (
            "result_value",
            "priority_rank",
            "quality_status",
        ):
            if regenerated[field] != published_item[field]:
                raise ValueError(
                    f"Published result mismatch for {key}: {field}"
                )

    # Calculate each independent source observation's variance.
    source_variances = original_paired.copy()
    source_variances["variance_amount"] = (
        source_variances["actual_amount"]
        - source_variances["budget_amount"]
    )
    source_variances["absolute_variance"] = (
        source_variances["variance_amount"].abs()
    )

    source_variances = source_variances.sort_values(
        ["absolute_variance", "source_record_id"],
        ascending=[False, True],
    )

    largest = source_variances.iloc[0]
    removed_source_id = str(largest["source_record_id"])

    # Remove all four financial rows belonging to this one observation.
    reduced_canonical = canonical.loc[
        canonical["source_record_id"].astype(str) != removed_source_id
    ].copy()

    removed_rows = len(canonical) - len(reduced_canonical)

    if removed_rows != len(method.EXPECTED_METRICS):
        raise ValueError(
            "Expected exactly four metric rows for the removed observation; "
            f"found {removed_rows}."
        )

    removed_metrics = set(
        canonical.loc[
            canonical["source_record_id"].astype(str) == removed_source_id,
            "metric_name",
        ].astype(str)
    )

    if removed_metrics != method.EXPECTED_METRICS:
        raise ValueError(
            "The removed source observation does not contain exactly "
            "the four expected financial measures."
        )

    # Use a temporary copy. The canonical CSV is never modified.
    with tempfile.TemporaryDirectory(
        prefix="poc4_sensitivity_"
    ) as temporary_directory:

        temporary_csv = (
            Path(temporary_directory) / "reduced_canonical.csv"
        )

        reduced_canonical.to_csv(
            temporary_csv,
            index=False,
        )

        reduced_paired = method.load_and_pair(temporary_csv)

        reduced_results = method.build_comparisons(
            reduced_paired,
            generated_at=published["generated_at"],
        )

    original_overall = overall_findings(original_results)
    reduced_overall = overall_findings(reduced_results)

    if set(original_overall) != set(reduced_overall):
        raise ValueError(
            "The set of overall comparison groups changed unexpectedly."
        )

    comparisons = []

    for key in sorted(original_overall):
        before = original_overall[key]
        after = reduced_overall[key]

        before_rank = before["priority_rank"]
        after_rank = after["priority_rank"]

        comparisons.append({
            "result_type": before["result_type"],
            "group_key": before["group_key"],
            "variance_before": before["result_value"],
            "variance_after": after["result_value"],
            "variance_change": (
                after["result_value"] - before["result_value"]
            ),
            "variance_percentage_before": (
                before["evidence"]["variance_percentage"]
            ),
            "variance_percentage_after": (
                after["evidence"]["variance_percentage"]
            ),
            "source_count_before": (
                before["evidence"]["independent_source_count"]
            ),
            "source_count_after": (
                after["evidence"]["independent_source_count"]
            ),
            "rank_before": before_rank,
            "rank_after": after_rank,
            "rank_changed": before_rank != after_rank,
            "quality_status_before": before["quality_status"],
            "quality_status_after": after["quality_status"],
            "quality_status_changed": (
                before["quality_status"] != after["quality_status"]
            ),
        })

    rank_changes = [
        item for item in comparisons if item["rank_changed"]
    ]

    evidence_status_changes = [
        item for item in comparisons
        if item["quality_status_changed"]
    ]

    newly_insufficient = [
        item for item in comparisons
        if (
            item["quality_status_before"] != "insufficient_evidence"
            and item["quality_status_after"] == "insufficient_evidence"
        )
    ]

    variance_changes = [
        item for item in comparisons
        if abs(item["variance_change"]) > 1e-9
    ]

    report = {
        "report_version": "1.0.0",
        "project_id": published["project_id"],
        "approved_track": published["approved_track"],
        "dataset_version": published["dataset_version"],
        "method_version": published["method_version"],
        "generated_at": published["generated_at"],

        "status": "COMPLETED",

        "test_design": {
            "test_type": "Leave-one-source-observation-out sensitivity review",
            "selection_rule": (
                "Remove the individual source observation with the "
                "largest absolute Actual minus Budget variance."
            ),
            "removal_unit": "One complete source observation containing four financial measures.",
            "analytical_method": (
                "The existing approved load_and_pair and build_comparisons "
                "functions were used without modification."
            ),
            "minimum_overall_group_size": (
                method.MINIMUM_OVERALL_GROUP_SIZE
            ),
            "canonical_dataset_modified": False,
        },

        "removed_source_observation": {
            "source_record_id": removed_source_id,
            "entity_id": str(largest["entity_id"]),
            "entity_name": str(largest["department"]),
            "category": str(largest["category"]),
            "period": str(largest["period"]),
            "budget_amount": float(largest["budget_amount"]),
            "actual_amount": float(largest["actual_amount"]),
            "variance_amount": float(largest["variance_amount"]),
            "absolute_variance": float(largest["absolute_variance"]),
            "removed_metric_row_count": removed_rows,
            "removed_metrics": sorted(removed_metrics),
        },

        "dataset_counts": {
            "source_observations_before": len(original_paired),
            "source_observations_after": len(reduced_paired),
            "source_observations_removed": (
                len(original_paired) - len(reduced_paired)
            ),
            "canonical_rows_before": len(canonical),
            "canonical_rows_after": len(reduced_canonical),
            "canonical_rows_removed": removed_rows,
            "overall_groups_before": len(original_overall),
            "overall_groups_after": len(reduced_overall),
        },

        "results": {
            "overall_comparison_count": len(comparisons),
            "rank_changed_count": len(rank_changes),
            "variance_changed_count": len(variance_changes),
            "quality_status_changed_count": len(evidence_status_changes),
            "newly_insufficient_evidence_count": len(newly_insufficient),
            "comparisons": comparisons,
        },

        "interpretation": (
            "This is a descriptive sensitivity assessment of the effect "
            "of removing one large source observation. Changes in variance, "
            "ranking or evidence status indicate sensitivity to that "
            "observation. Unchanged findings do not establish statistical "
            "robustness or population-level validity."
        ),

        "limitations": [
            "The dataset contains synthetic source observations.",
            "Only one removal scenario was tested.",
            "This test does not establish statistical significance or population-level robustness.",
            "Groups falling below the minimum source threshold become insufficient_evidence and are excluded from ranking.",
            "Ranking changes can result from changed variances, evidence eligibility or the ordering of remaining groups.",
        ],
    }

    save_json(REPORT_FILE, report)

    print("SENSITIVITY REVIEW")
    print("Removed source:", removed_source_id)
    print("Removed metric rows:", removed_rows)
    print(
        "Source observations:",
        len(original_paired),
        "->",
        len(reduced_paired),
    )
    print("Overall comparisons:", len(comparisons))
    print("Rank changes:", len(rank_changes))
    print("Variance changes:", len(variance_changes))
    print("Evidence status changes:", len(evidence_status_changes))
    print("Newly insufficient:", len(newly_insufficient))
    print("Canonical dataset modified: NO")
    print("Report:", REPORT_FILE)
    print("Sensitivity review: COMPLETED")


if __name__ == "__main__":
    main()
