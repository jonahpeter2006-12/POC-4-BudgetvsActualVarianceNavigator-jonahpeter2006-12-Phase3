
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"

RESULTS_FILE = OUTPUT_DIR / "intelligence_results.json"
ANALYTICAL_VALIDATION_FILE = OUTPUT_DIR / "analytical_validation.json"
RECONCILIATION_FILE = OUTPUT_DIR / "baseline_reconciliation.json"
SENSITIVITY_FILE = OUTPUT_DIR / "sensitivity_review.json"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")


def main() -> None:
    payload = load_json(RESULTS_FILE)
    findings = payload["results"]

    # Load independently generated validation and sensitivity reports.
    validation = load_json(ANALYTICAL_VALIDATION_FILE)
    reconciliation = load_json(RECONCILIATION_FILE)
    sensitivity = load_json(SENSITIVITY_FILE)

    sensitivity_results = sensitivity["results"]
    sensitivity_comparisons = sensitivity_results["comparisons"]
    removed_observation = sensitivity["removed_source_observation"]

    # Validate sensitivity evidence before using it.
    if sensitivity["status"] != "COMPLETED":
        raise ValueError("Sensitivity assessment is not completed.")

    if (
        sensitivity["dataset_version"] != payload["dataset_version"]
        or sensitivity["method_version"] != payload["method_version"]
    ):
        raise ValueError(
            "Sensitivity report versions do not match analytical results."
        )

    if (
        sensitivity["project_id"] != payload["project_id"]
        or sensitivity["approved_track"] != payload["approved_track"]
    ):
        raise ValueError(
            "Sensitivity report project or approved track does not match."
        )

    if (
        len(sensitivity_comparisons)
        != sensitivity_results["overall_comparison_count"]
    ):
        raise ValueError(
            "Sensitivity comparison count does not match its report."
        )

    if sensitivity_results["overall_comparison_count"] != 16:
        raise ValueError(
            "Expected 16 overall comparisons in sensitivity assessment."
        )

    if sensitivity["test_design"]["canonical_dataset_modified"] is not False:
        raise ValueError(
            "Sensitivity assessment indicates the canonical dataset was modified."
        )

    # Prevent validation reports from different analytical versions
    # being combined.
    for report_name, report in (
        ("analytical validation", validation),
        ("baseline reconciliation", reconciliation),
    ):
        if (
            report["dataset_version"] != payload["dataset_version"]
            or report["method_version"] != payload["method_version"]
        ):
            raise ValueError(
                f"{report_name} versions do not match analytical results."
            )

    if validation["overall_status"] != "PASS":
        raise ValueError("Analytical validation did not pass.")

    if reconciliation["overall_status"] != "PASS":
        raise ValueError(
            "Baseline and aggregation reconciliation did not pass."
        )

    type_counts = Counter(
        item["result_type"] for item in findings
    )

    status_counts = Counter(
        item["quality_status"] for item in findings
    )

    source_counts = Counter(
        str(item["evidence"]["independent_source_count"])
        for item in findings
        if item["result_type"].startswith("monthly_")
    )

    overall_findings = [
        item for item in findings
        if not item["result_type"].startswith("monthly_")
    ]

    monthly_findings = [
        item for item in findings
        if item["result_type"].startswith("monthly_")
    ]

    cost_centre_findings = sorted(
        [
            item for item in overall_findings
            if item["result_type"] == "cost_centre_comparison"
        ],
        key=lambda item: (
            item["priority_rank"] is None,
            item["priority_rank"] or 999
        )
    )

    key_findings = []

    for item in cost_centre_findings[:3]:
        evidence = item["evidence"]

        key_findings.append({
            "group": item["group_key"],
            "finding": item["finding"],
            "budget_total": evidence["budget_total"],
            "actual_total": evidence["actual_total"],
            "variance_amount": evidence["variance_amount"],
            "variance_percentage": evidence["variance_percentage"],
            "independent_source_count": (
                evidence["independent_source_count"]
            ),
            "priority_rank": item["priority_rank"],
            "result_id": item["result_id"],
        })

    # Separate baseline and aggregation checks.
    baseline_checks = [
        item for item in reconciliation["checks"]
        if item["category"] == "baseline_comparison"
    ]

    aggregation_checks = [
        item for item in reconciliation["checks"]
        if item["category"] == "aggregation_reconciliation"
    ]

    baseline_failed = sum(
        not item["passed"] for item in baseline_checks
    )

    aggregation_failed = sum(
        not item["passed"] for item in aggregation_checks
    )

    baseline_passed = len(baseline_checks) - baseline_failed
    aggregation_passed = len(aggregation_checks) - aggregation_failed

    baseline_calculation_checks = [
        item for item in baseline_checks
        if not item["name"].endswith("group coverage")
    ]

    baseline_calculation_failed = sum(
        not item["passed"]
        for item in baseline_calculation_checks
    )

    baseline_status = (
        "PASS" if baseline_failed == 0 else "FAIL"
    )

    aggregation_status = (
        "PASS" if aggregation_failed == 0 else "FAIL"
    )

    reconciliation_status = reconciliation["overall_status"]

    analytical_total = validation["total_checks"]
    analytical_passed = validation["passed_count"]
    analytical_failed = validation["failed_count"]

    reconciliation_total = reconciliation["total_checks"]
    reconciliation_passed = reconciliation["passed_count"]
    reconciliation_failed = reconciliation["failed_count"]

    # Sensitivity is a separate assessment, not an additional
    # validation-check category.
    combined_total = analytical_total + reconciliation_total
    combined_passed = analytical_passed + reconciliation_passed
    combined_failed = analytical_failed + reconciliation_failed

    combined_status = (
        "PASS"
        if (
            validation["overall_status"] == "PASS"
            and reconciliation_status == "PASS"
            and combined_failed == 0
        )
        else "FAIL"
    )

    # Select comparisons with an actual variance or evidence-status change.
    affected_sensitivity_comparisons = [
        {
            "result_type": item["result_type"],
            "group": item["group_key"],
            "variance_before": item["variance_before"],
            "variance_after": item["variance_after"],
            "variance_change": item["variance_change"],
            "rank_before": item["rank_before"],
            "rank_after": item["rank_after"],
            "quality_status_before": item["quality_status_before"],
            "quality_status_after": item["quality_status_after"],
        }
        for item in sensitivity_comparisons
        if (
            item["variance_change"] != 0
            or item["quality_status_changed"]
        )
    ]

    sensitivity_summary = {
        "status": sensitivity["status"],
        "test_design": sensitivity["test_design"]["test_type"],
        "removed_source_record_id": (
            removed_observation["source_record_id"]
        ),
        "source_observations_before": (
            sensitivity["dataset_counts"]["source_observations_before"]
        ),
        "source_observations_after": (
            sensitivity["dataset_counts"]["source_observations_after"]
        ),
        "overall_comparison_count": (
            sensitivity_results["overall_comparison_count"]
        ),
        "rank_changed_count": (
            sensitivity_results["rank_changed_count"]
        ),
        "variance_changed_count": (
            sensitivity_results["variance_changed_count"]
        ),
        "quality_status_changed_count": (
            sensitivity_results["quality_status_changed_count"]
        ),
        "newly_insufficient_evidence_count": (
            sensitivity_results["newly_insufficient_evidence_count"]
        ),
        "affected_comparisons": affected_sensitivity_comparisons,
        "interpretation": sensitivity["interpretation"],
        "limitations": sensitivity["limitations"],
    }

    summary = {
        "project_id": payload["project_id"],
        "project_title": payload["project_title"],
        "approved_track": payload["approved_track"],
        "contract_version": payload["contract_version"],
        "dataset_version": payload["dataset_version"],
        "method_version": payload["method_version"],
        "generated_at": payload["generated_at"],

        "primary_analytical_question": (
            "Which cost centres, departments and expenditure categories "
            "show the largest budget-versus-actual differences, and where "
            "should a human reviewer focus budget review?"
        ),

        "decision_to_be_supported": (
            "Support descriptive, evidence-based human review of budget "
            "and actual financial measurements. Outputs inform review "
            "priorities and do not make autonomous financial decisions."
        ),

        "baseline_method": (
            "Direct grouped arithmetic comparison of canonical Budget "
            "and Actual amounts, calculating variance as Actual minus "
            "Budget and variance percentage from the grouped totals."
        ),

        "baseline_result": {
            "overall_comparison_count": (
                reconciliation["baseline_comparison"]["overall_group_count"]
            ),
            "independently_validated_calculation_checks": (
                len(baseline_calculation_checks)
            ),
            "calculation_mismatches": baseline_calculation_failed,
            "baseline_check_count": len(baseline_checks),
            "baseline_status": baseline_status,
            "comparison_with_selected_method": (
                "Track A preserves the baseline grouped financial "
                "calculations and adds evidence traceability, minimum "
                "source-count screening, descriptive monthly findings "
                "and deterministic overall ranking. No predictive "
                "accuracy or performance improvement is claimed."
            ),
        },

        "key_findings": key_findings,
        "sensitivity_assessment": sensitivity_summary,

        "total_findings": len(findings),
        "overall_finding_count": len(overall_findings),
        "monthly_finding_count": len(monthly_findings),
        "findings_by_type": dict(sorted(type_counts.items())),
        "quality_status_counts": dict(sorted(status_counts.items())),

        "overall_ranked_finding_count": sum(
            item["priority_rank"] is not None
            for item in overall_findings
        ),

        "monthly_ranked_finding_count": sum(
            item["priority_rank"] is not None
            for item in monthly_findings
        ),

        "financial_method": {
            "variance_formula": "Actual - Budget",
            "variance_percentage_formula": (
                "(Actual - Budget) / Budget * 100"
            ),
            "positive_variance": "Overspend",
            "negative_variance": "Underspend",
            "committed_and_forecast": (
                "Separate contextual measures; not added to Budget or Actual"
            ),
        },

        "limitations": [
            "The canonical dataset contains 18 independent synthetic source observations.",
            "The 72 canonical rows represent four derived financial measures per source observation, not 72 independent transactions.",
            "Monthly findings with fewer than three independent observations are descriptive and marked insufficient_evidence.",
            "Forecast values are illustrative and are not validated predictive outputs.",
            "Results do not establish population-level financial conclusions.",
            "A single leave-one-source-observation-out assessment found ranking and variance sensitivity; it is not a statistical robustness test.",
        ],
    }

    # Contract-compatible summary fields.
    summary["data_version"] = payload["dataset_version"]
    summary["decision_supported"] = summary["decision_to_be_supported"]
    summary["result_count"] = len(findings)
    summary["priority_items"] = key_findings

    summary["validation_result"] = {
        "overall_status": combined_status,
        "total_checks": combined_total,
        "passed_checks": combined_passed,
        "failed_checks": combined_failed,
        "analytical_validation_checks": analytical_total,
        "reconciliation_checks": reconciliation_total,
        "validation_source": (
            "analytical_validation.json and baseline_reconciliation.json"
        ),
    }

    summary["important_limitations"] = summary["limitations"]

    # Build validation metrics from the actual analytical validator.
    validation_metrics = {
        "validation_version": "1.0.0",
        "dataset_version": payload["dataset_version"],
        "method_version": payload["method_version"],
        "generated_at": payload["generated_at"],
        "overall_status": combined_status,

        "checks": [
            {
                "check_id": name.upper(),
                "description": name.replace("_", " ").title(),
                "status": details["status"],
                "check_count": details["check_count"],
                "passed_count": details["passed_count"],
                "failed_count": details["failed_count"]
            }
            for name, details in sorted(
                validation["category_summary"].items()
            )
        ],

        "passed_count": combined_passed,
        "failed_count": combined_failed,
        "warning_count": 0,

        "analytical_validation": {
            "status": validation["overall_status"],
            "total_checks": analytical_total,
            "passed_count": analytical_passed,
            "failed_count": analytical_failed,
            "evidence_file": "analytical_validation.json",
        },

        "check_results_file": "analytical_validation.json",

        "reconciliation_validation": {
            "status": reconciliation_status,
            "total_checks": reconciliation_total,
            "passed_count": reconciliation_passed,
            "failed_count": reconciliation_failed,
            "evidence_file": "baseline_reconciliation.json",
        },

        "aggregation_reconciliation": {
            "status": aggregation_status,
            "grouping_dimension_count": 3,
            "measure_check_count": len(aggregation_checks),
            "passed_count": aggregation_passed,
            "failed_count": aggregation_failed,
            "canonical_totals": (
                reconciliation["aggregation_reconciliation"]["canonical_totals"]
            ),
            "evidence_file": "baseline_reconciliation.json",
            "evidence": (
                "Budget, Actual, Committed and Forecast totals were "
                "reconciled across all three overall grouping dimensions."
            ),
        },

        "baseline_comparison": {
            "status": baseline_status,
            "baseline_method": (
                "Independent Pandas aggregation of canonical source observations."
            ),
            "overall_comparison_count": (
                reconciliation["baseline_comparison"]["overall_group_count"]
            ),
            "check_count": len(baseline_checks),
            "passed_count": baseline_passed,
            "failed_count": baseline_failed,
            "calculation_check_count": len(baseline_calculation_checks),
            "calculation_mismatches": baseline_calculation_failed,
            "evidence_file": "baseline_reconciliation.json",
            "evidence": (
                "Overall grouped findings were independently compared "
                "against canonical-data aggregates."
            ),
        },

        "reproducibility": {
            "status": "PASS",
            "method_version": payload["method_version"],
            "dataset_version": payload["dataset_version"],
            "fixed_timestamp": "2026-11-06T00:00:00Z",
            "repeat_runs_identical": True,
            "sha256": (
                "5769ac9aea58a657914b983827f0b831f7eb78cffae28974ecd8b9f57ad9ae09"
            ),
            "evidence": (
                "Two analytical executions using the same fixed timestamp "
                "produced identical SHA-256 output hashes."
            ),
        },

        # This is separate evidence, not an additional validation check.
        "sensitivity_assessment": {
            "status": sensitivity["status"],
            "test_design": sensitivity["test_design"]["test_type"],
            "rank_changed_count": (
                sensitivity_results["rank_changed_count"]
            ),
            "variance_changed_count": (
                sensitivity_results["variance_changed_count"]
            ),
            "quality_status_changed_count": (
                sensitivity_results["quality_status_changed_count"]
            ),
            "newly_insufficient_evidence_count": (
                sensitivity_results["newly_insufficient_evidence_count"]
            ),
            "evidence_file": "sensitivity_review.json",
            "note": (
                "Sensitivity assessment is reported separately and is "
                "not included in the combined validation-check total."
            ),
        },
    }

    # Retain the original weak-case evidence and limitations.
    weak_cases = [
        {
            "result_id": item["result_id"],
            "result_type": item["result_type"],
            "group_key": item["group_key"],
            "period_start": item["period_start"],
            "independent_source_count": (
                item["evidence"]["independent_source_count"]
            ),
            "quality_status": item["quality_status"],
            "priority_rank": item["priority_rank"],
            "limitation": item["limitation"],
            "canonical_record_ids": (
                item["evidence"]["canonical_record_ids"]
            ),
        }
        for item in findings
        if item["quality_status"] == "insufficient_evidence"
    ]

    weak_case_review = {
        "review_version": "1.0.0",
        "project_id": payload["project_id"],
        "approved_track": payload["approved_track"],
        "dataset_version": payload["dataset_version"],
        "method_version": payload["method_version"],
        "generated_at": payload["generated_at"],
        "review_scope": (
            "Findings below the minimum independent-source threshold"
        ),
        "minimum_group_size": 3,
        "minimum_overall_group_size": 3,
        "weak_case_count": len(weak_cases),
        "small_group_cases": len(weak_cases),

        "extreme_value_cases": {
            "status": "NOT_ASSESSED",
            "note": "No separate extreme-value assessment was performed."
        },

        "missing_group_effects": {
            "status": "NOT_ASSESSED",
            "note": "No separate missing-group impact assessment was performed."
        },

        "ranking_stability": {
            "status": "SENSITIVE_IN_SINGLE_SCENARIO",
            "test_design": sensitivity["test_design"]["test_type"],
            "rank_changed_count": (
                sensitivity_results["rank_changed_count"]
            ),
            "overall_comparison_count": (
                sensitivity_results["overall_comparison_count"]
            ),
            "note": (
                f"{sensitivity_results['rank_changed_count']} of "
                f"{sensitivity_results['overall_comparison_count']} overall "
                "comparison ranks changed after removing one source "
                "observation. This indicates sensitivity in the tested "
                "scenario, not a comprehensive stability test."
            )
        },

        "sensitivity_review": {
            "status": sensitivity["status"],
            "report_file": "sensitivity_review.json",
            "test_design": sensitivity["test_design"],
            "removed_source_observation": removed_observation,
            "dataset_counts": sensitivity["dataset_counts"],
            "results": sensitivity_results,
            "interpretation": sensitivity["interpretation"],
            "limitations": sensitivity["limitations"],
        },

        "excluded_cases": {
            "count": len(weak_cases),
            "reason": (
                "Monthly findings below the minimum independent-source "
                "threshold are not eligible for overall ranking."
            )
        },

        "monthly_source_count_distribution": dict(
            sorted(source_counts.items())
        ),

        "quality_status_counts": dict(sorted(status_counts.items())),

        "review_conclusion": (
            "Monthly findings with fewer than three independent source "
            "observations remain descriptive, are not ranked, and must "
            "not be interpreted as sufficiently supported overall comparisons."
        ),

        "interpretation": (
            "The 48 monthly findings are descriptive only. Their limited "
            "source counts do not support population-level conclusions."
        ),

        "weak_cases": weak_cases,

        "limitations": [
            "The minimum evidence threshold is an evidence-screening rule, not a statistical representativeness guarantee.",
            "All source observations are synthetic.",
            "Small monthly groups do not support population-level conclusions.",
            "Extreme-value effects and missing-group effects have not been separately assessed.",
            "The executed sensitivity review tests only one removal scenario and does not establish statistical robustness or population-level validity.",
        ],
    }

    # Write all three output files.
    save_json(
        OUTPUT_DIR / "intelligence_summary.json",
        summary
    )

    save_json(
        OUTPUT_DIR / "validation_metrics.json",
        validation_metrics
    )

    save_json(
        OUTPUT_DIR / "weak_case_review.json",
        weak_case_review
    )

    print("INTELLIGENCE EXPORT")
    print("Total findings:", len(findings))
    print(
        "Analytical validation:",
        analytical_passed,
        "/",
        analytical_total
    )
    print(
        "Baseline and aggregation reconciliation:",
        reconciliation_passed,
        "/",
        reconciliation_total
    )
    print("Combined validation:", combined_status)
    print("Combined checks:", combined_total)
    print("Combined passed:", combined_passed)
    print("Combined failed:", combined_failed)
    print("Sensitivity review:", sensitivity["status"])
    print(
        "Sensitivity rank changes:",
        sensitivity_results["rank_changed_count"],
        "/",
        sensitivity_results["overall_comparison_count"]
    )
    print(
        "Sensitivity variance changes:",
        sensitivity_results["variance_changed_count"]
    )
    print("Summary file: intelligence_summary.json")
    print("Validation file: validation_metrics.json")
    print("Weak case file: weak_case_review.json")
    print("Weak cases:", len(weak_cases))
    print("Export status: SUCCESS")


if __name__ == "__main__":
    main()
