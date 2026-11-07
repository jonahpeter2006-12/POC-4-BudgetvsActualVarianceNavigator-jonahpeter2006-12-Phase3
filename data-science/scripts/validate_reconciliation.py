
import json
import math
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_FILE = (
    PROJECT_ROOT / "data" / "canonical" / "intelligence_data.csv"
)
RESULTS_FILE = (
    PROJECT_ROOT / "data-science" / "outputs"
    / "intelligence_results.json"
)
OUTPUT_FILE = (
    PROJECT_ROOT / "data-science" / "outputs"
    / "baseline_reconciliation.json"
)

GROUPINGS = {
    "cost_centre_comparison": "entity_id",
    "department_comparison": "entity_name",
    "expenditure_category_comparison": "category",
}

MEASURES = [
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
]


def close(actual, expected):
    return math.isclose(
        float(actual),
        float(expected),
        rel_tol=1e-10,
        abs_tol=1e-8,
    )


def main():
    if not CANONICAL_FILE.exists():
        raise FileNotFoundError(CANONICAL_FILE)

    if not RESULTS_FILE.exists():
        raise FileNotFoundError(RESULTS_FILE)

    canonical = pd.read_csv(CANONICAL_FILE)
    payload = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))

    canonical["observed_at"] = pd.to_datetime(
        canonical["observed_at"], utc=True
    )

    wide = canonical.pivot_table(
        index=[
            "source_record_id",
            "entity_id",
            "entity_name",
            "category",
            "observed_at",
        ],
        columns="metric_name",
        values="metric_value",
        aggfunc="first",
    ).reset_index()

    if wide[MEASURES].isna().any().any():
        raise ValueError("Canonical data contains incomplete measure groups.")

    findings = payload["results"]
    checks = []
    failures = []

    def record(category, name, actual, expected, passed):
        checks.append({
            "category": category,
            "name": name,
            "actual": float(actual),
            "expected": float(expected),
            "passed": bool(passed),
        })
        if not passed:
            failures.append(name)

    # Independent baseline comparison for all 16 overall findings.
    baseline_count = 0

    for result_type, column in GROUPINGS.items():
        actual_findings = [
            item for item in findings
            if item["result_type"] == result_type
        ]

        expected_groups = {
            str(key): group
            for key, group in wide.groupby(column, sort=True)
        }

        actual_groups = {
            str(item["group_key"]): item
            for item in actual_findings
        }

        record(
            "baseline_comparison",
            f"{result_type}: group coverage",
            len(actual_groups),
            len(expected_groups),
            set(actual_groups) == set(expected_groups),
        )

        for group_key, group in expected_groups.items():
            if group_key not in actual_groups:
                continue

            item = actual_groups[group_key]
            evidence = item["evidence"]

            budget = float(group["budget_amount"].sum())
            actual = float(group["actual_amount"].sum())
            variance = actual - budget
            percentage = variance / budget * 100 if budget else None

            comparisons = [
                ("budget_total", evidence["budget_total"], budget),
                ("actual_total", evidence["actual_total"], actual),
                ("variance_amount", evidence["variance_amount"], variance),
                ("result_value", item["result_value"], variance),
            ]

            for name, observed, expected in comparisons:
                record(
                    "baseline_comparison",
                    f"{result_type}/{group_key}: {name}",
                    observed,
                    expected,
                    close(observed, expected),
                )

            observed_percentage = evidence.get("variance_percentage")
            percentage_passed = (
                observed_percentage is None
                if percentage is None
                else observed_percentage is not None
                and close(observed_percentage, percentage)
            )

            record(
                "baseline_comparison",
                f"{result_type}/{group_key}: variance_percentage",
                observed_percentage or 0,
                percentage or 0,
                percentage_passed,
            )

            baseline_count += 1

    # Reconcile each measure across all three grouping dimensions.
    aggregation_count = 0

    canonical_totals = {
        measure: float(wide[measure].sum())
        for measure in MEASURES
    }

    for result_type, column in GROUPINGS.items():
        grouped = wide.groupby(column, sort=True)[MEASURES].sum()

        for measure in MEASURES:
            grouped_total = float(grouped[measure].sum())
            canonical_total = canonical_totals[measure]

            record(
                "aggregation_reconciliation",
                f"{result_type}: {measure}",
                grouped_total,
                canonical_total,
                close(grouped_total, canonical_total),
            )
            aggregation_count += 1

    passed_count = sum(item["passed"] for item in checks)
    failed_count = len(checks) - passed_count

    report = {
        "report_version": "1.0.0",
        "dataset_version": payload["dataset_version"],
        "method_version": payload["method_version"],
        "overall_status": "PASS" if failed_count == 0 else "FAIL",
        "baseline_comparison": {
            "status": (
                "PASS" if not any(
                    item["category"] == "baseline_comparison"
                    and not item["passed"] for item in checks
                ) else "FAIL"
            ),
            "overall_group_count": baseline_count,
        },
        "aggregation_reconciliation": {
            "status": (
                "PASS" if not any(
                    item["category"] == "aggregation_reconciliation"
                    and not item["passed"] for item in checks
                ) else "FAIL"
            ),
            "measure_check_count": aggregation_count,
            "canonical_totals": canonical_totals,
        },
        "total_checks": len(checks),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "checks": checks,
        "failures": failures,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("BASELINE AND AGGREGATION RECONCILIATION")
    print("Baseline groups checked:", baseline_count)
    print("Aggregation checks:", aggregation_count)
    print("Total checks:", len(checks))
    print("Passed:", passed_count)
    print("Failed:", failed_count)
    print("Overall status:", report["overall_status"])
    print("Report:", OUTPUT_FILE)

    if failed_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
