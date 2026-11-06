import json
import math
from collections import defaultdict
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FILE = (
    PROJECT_ROOT / "data" / "canonical" / "intelligence_data.csv"
)

RESULTS_FILE = (
    PROJECT_ROOT / "data-science" / "outputs" / "intelligence_results.json"
)

EXPECTED_METHOD_VERSION = "1.0.0"
EXPECTED_DATASET_VERSION = "1.0.0"
MINIMUM_OVERALL_GROUP_SIZE = 3

GROUP_COLUMNS = {
    "cost_centre_comparison": "entity_id",
    "department_comparison": "entity_name",
    "expenditure_category_comparison": "category",
    "monthly_cost_centre_comparison": "entity_id",
    "monthly_department_comparison": "entity_name",
    "monthly_expenditure_category_comparison": "category",
}

OVERALL_TYPES = {
    "cost_centre_comparison",
    "department_comparison",
    "expenditure_category_comparison",
}

MONTHLY_TYPES = {
    "monthly_cost_centre_comparison",
    "monthly_department_comparison",
    "monthly_expenditure_category_comparison",
}

REQUIRED_FINDING_FIELDS = {
    "result_id",
    "result_type",
    "record_id",
    "entity_id",
    "group_key",
    "period_start",
    "period_end",
    "metric_name",
    "result_value",
    "result_unit",
    "result_category",
    "priority_rank",
    "finding",
    "evidence",
    "method_version",
    "data_version",
    "generated_at",
    "quality_status",
    "limitation",
}

REQUIRED_EVIDENCE_FIELDS = {
    "budget_total",
    "actual_total",
    "variance_amount",
    "variance_percentage",
    "committed_total",
    "forecast_total",
    "independent_source_count",
    "canonical_record_ids",
    "source_record_ids",
    "reporting_period",
    "currency_unit",
    "aggregation_method",
}


def close(actual, expected):
    return math.isclose(
        float(actual),
        float(expected),
        rel_tol=1e-10,
        abs_tol=1e-8
    )


def main():
    checks = defaultdict(int)
    failures = []
    check_results = []

    def record_check(name, passed, detail):
        checks[name] += 1
        check_results.append({
            "category": name,
            "passed": bool(passed),
            "detail": detail if not passed else "Passed"
        })
        if not passed:
            failures.append(f"{name}: {detail}")

    if not CANONICAL_FILE.exists():
        raise FileNotFoundError(CANONICAL_FILE)

    if not RESULTS_FILE.exists():
        raise FileNotFoundError(RESULTS_FILE)

    canonical = pd.read_csv(CANONICAL_FILE)
    canonical["observed_at"] = pd.to_datetime(
        canonical["observed_at"],
        utc=True
    )

    with RESULTS_FILE.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    record_check(
        "metadata",
        payload.get("approved_track") == "Track A — Comparative Intelligence",
        "Unexpected approved track"
    )

    record_check(
        "metadata",
        payload.get("method_version") == EXPECTED_METHOD_VERSION,
        "Unexpected method version"
    )

    record_check(
        "metadata",
        payload.get("dataset_version") == EXPECTED_DATASET_VERSION,
        "Unexpected dataset version"
    )

    findings = payload.get("results", [])

    record_check(
        "count",
        payload.get("result_count") == len(findings) == 64,
        f"Expected 64 findings; found {len(findings)}"
    )

    result_ids = [item.get("result_id") for item in findings]

    record_check(
        "identity",
        len(result_ids) == len(set(result_ids)),
        "Duplicate result IDs"
    )

    type_counts = defaultdict(int)

    for item in findings:
        result_type = item.get("result_type")
        type_counts[result_type] += 1

        missing_fields = REQUIRED_FINDING_FIELDS - set(item.keys())

        record_check(
            "schema",
            not missing_fields,
            f"{item.get('result_id')}: missing fields {sorted(missing_fields)}"
        )

        evidence = item.get("evidence", {})
        missing_evidence = REQUIRED_EVIDENCE_FIELDS - set(evidence.keys())

        record_check(
            "schema",
            not missing_evidence,
            f"{item.get('result_id')}: missing evidence fields {sorted(missing_evidence)}"
        )

        record_check(
            "versions",
            item.get("method_version") == EXPECTED_METHOD_VERSION
            and item.get("data_version") == EXPECTED_DATASET_VERSION,
            f"{item.get('result_id')}: incorrect finding version"
        )

        record_check(
            "classification",
            item.get("metric_name") == "budget_vs_actual_variance"
            and item.get("result_unit") == "USD",
            f"{item.get('result_id')}: incorrect metric or unit"
        )

        record_check(
            "finding",
            isinstance(item.get("finding"), str)
            and bool(item.get("finding", "").strip()),
            f"{item.get('result_id')}: missing finding text"
        )

        record_check(
            "limitations",
            isinstance(item.get("limitation"), list)
            and len(item.get("limitation", [])) > 0,
            f"{item.get('result_id')}: missing limitations"
        )

        if result_type not in GROUP_COLUMNS:
            failures.append(
                f"Unexpected result type: {result_type}"
            )
            continue

        group_column = GROUP_COLUMNS[result_type]

        expected = canonical[
            canonical[group_column] == item["group_key"]
        ].copy()

        if result_type in MONTHLY_TYPES:
            expected = expected[
                expected["observed_at"].dt.strftime("%Y-%m-%d")
                == item["period_start"]
            ]

        expected_wide = expected.pivot_table(
            index=[
                "source_record_id",
                "entity_id",
                "entity_name",
                "category",
                "observed_at"
            ],
            columns="metric_name",
            values="metric_value",
            aggfunc="first"
        ).reset_index()

        source_ids = set(expected["source_record_id"])
        record_ids = set(expected["record_id"])

        actual_source_ids = set(evidence.get("source_record_ids", []))
        actual_record_ids = set(evidence.get("canonical_record_ids", []))

        record_check(
            "evidence",
            source_ids == actual_source_ids,
            f"{item['result_id']}: source IDs do not match"
        )

        record_check(
            "evidence",
            record_ids == actual_record_ids,
            f"{item['result_id']}: canonical record IDs do not match"
        )

        record_check(
            "evidence",
            len(source_ids) == evidence.get("independent_source_count"),
            f"{item['result_id']}: independent source count mismatch"
        )

        record_check(
            "evidence",
            len(record_ids) == len(source_ids) * 4,
            f"{item['result_id']}: expected four measure records per source"
        )

        if expected_wide.empty:
            failures.append(
                f"{item['result_id']}: no matching canonical observations"
            )
            continue

        totals = {
            metric: float(expected_wide[metric].sum())
            for metric in [
                "budget_amount",
                "actual_amount",
                "committed_amount",
                "forecast_amount"
            ]
        }

        budget = totals["budget_amount"]
        actual = totals["actual_amount"]
        variance = actual - budget
        percentage = variance / budget * 100 if budget else None

        record_check(
            "calculations",
            close(evidence["budget_total"], budget),
            f"{item['result_id']}: Budget total mismatch"
        )

        record_check(
            "calculations",
            close(evidence["actual_total"], actual),
            f"{item['result_id']}: Actual total mismatch"
        )

        record_check(
            "calculations",
            close(item["result_value"], variance)
            and close(evidence["variance_amount"], variance),
            f"{item['result_id']}: variance mismatch"
        )

        percentage_valid = (
            evidence.get("variance_percentage") is None
            if percentage is None
            else evidence.get("variance_percentage") is not None
            and close(evidence["variance_percentage"], percentage)
        )
        record_check(
            "calculations",
            percentage_valid,
            f"{item['result_id']}: variance percentage mismatch"
        )

        record_check(
            "measure_separation",
            close(evidence["committed_total"], totals["committed_amount"]),
            f"{item['result_id']}: committed total mismatch"
        )

        record_check(
            "measure_separation",
            close(evidence["forecast_total"], totals["forecast_amount"]),
            f"{item['result_id']}: forecast total mismatch"
        )

        expected_category = (
            "overspend" if variance > 0
            else "underspend" if variance < 0
            else "on_budget"
        )

        record_check(
            "classification",
            item["result_category"] == expected_category,
            f"{item['result_id']}: variance classification mismatch"
        )

        expected_status = (
            "validated_with_limitations"
            if result_type in OVERALL_TYPES
            and len(source_ids) >= MINIMUM_OVERALL_GROUP_SIZE
            else "insufficient_evidence"
        )

        record_check(
            "evidence_status",
            item["quality_status"] == expected_status,
            f"{item['result_id']}: incorrect evidence status"
        )

        if result_type in OVERALL_TYPES:
            record_check(
                "ranking_eligibility",
                len(source_ids) >= MINIMUM_OVERALL_GROUP_SIZE
                and item["priority_rank"] is not None,
                f"{item['result_id']}: overall group ranking eligibility issue"
            )
        else:
            record_check(
                "ranking_eligibility",
                len(source_ids) < MINIMUM_OVERALL_GROUP_SIZE
                and item["priority_rank"] is None,
                f"{item['result_id']}: monthly group should remain unranked"
            )

    for result_type in GROUP_COLUMNS:
        expected_count = {
            "cost_centre_comparison": 6,
            "department_comparison": 4,
            "expenditure_category_comparison": 6,
            "monthly_cost_centre_comparison": 18,
            "monthly_department_comparison": 12,
            "monthly_expenditure_category_comparison": 18,
        }[result_type]

        record_check(
            "type_counts",
            type_counts[result_type] == expected_count,
            f"{result_type}: expected {expected_count}, found {type_counts[result_type]}"
        )

    overall_groups = defaultdict(list)

    for item in findings:
        if item.get("result_type") in OVERALL_TYPES:
            overall_groups[item["result_type"]].append(item)

    for result_type, items in overall_groups.items():
        expected_order = [
            item["group_key"]
            for item in sorted(
                items,
                key=lambda item: (
                    -abs(item["result_value"]),
                    str(item["group_key"]).casefold()
                )
            )
        ]

        actual_order = [
            item["group_key"]
            for item in sorted(
                items,
                key=lambda item: item["priority_rank"]
            )
        ]

        record_check(
            "ranking_order",
            actual_order == expected_order,
            f"{result_type}: ranking order mismatch"
        )

    print("ANALYTICAL TRACK VALIDATION")
    print("Track:", payload.get("approved_track"))
    print("Method version:", payload.get("method_version"))
    print("Dataset version:", payload.get("dataset_version"))
    print("Total findings:", len(findings))

    print("\nFINDINGS BY TYPE")
    for result_type in sorted(GROUP_COLUMNS):
        print(result_type + ":", type_counts[result_type])

    print("\nCHECK COUNTS")
    total_checks = 0
    for name, count in sorted(checks.items()):
        print(name + ":", count)
        total_checks += count

    print("\nTotal checks:", total_checks)
    print("Failed checks:", len(failures))

    if failures:
        print("\nFAILURES")
        for failure in failures:
            print("-", failure)

    category_summary = {}
    for name in sorted(checks):
        entries = [
            item for item in check_results
            if item["category"] == name
        ]
        passed_count = sum(item["passed"] for item in entries)
        category_summary[name] = {
            "check_count": len(entries),
            "passed_count": passed_count,
            "failed_count": len(entries) - passed_count,
            "status": "PASS" if passed_count == len(entries) else "FAIL"
        }

    validation_payload = {
        "validation_version": "1.0.0",
        "dataset_version": payload.get("dataset_version"),
        "method_version": payload.get("method_version"),
        "generated_at": payload.get("generated_at"),
        "overall_status": "PASS" if not failures else "FAIL",
        "total_checks": len(check_results),
        "passed_count": sum(item["passed"] for item in check_results),
        "failed_count": len(failures),
        "category_summary": category_summary,
        "check_results": check_results,
        "failures": failures
    }

    validation_file = (
        PROJECT_ROOT / "data-science" / "outputs"
        / "analytical_validation.json"
    )
    validation_file.parent.mkdir(parents=True, exist_ok=True)
    validation_file.write_text(
        json.dumps(validation_payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print("Structured validation saved:", validation_file)

    print(
        "\nVALIDATION RESULT:",
        "PASS" if not failures else "FAIL"
    )

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
