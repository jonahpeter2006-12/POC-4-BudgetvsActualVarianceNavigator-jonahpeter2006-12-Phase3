"""Reusable Track A comparative financial intelligence calculations."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import math
import pandas as pd


METHOD_VERSION = "1.0.0"
DATASET_VERSION = "1.0.0"
CONTRACT_VERSION = "1.0.0"
MINIMUM_OVERALL_GROUP_SIZE = 3

EXPECTED_METRICS = {
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
}

SOURCE_KEY = ["source_record_id", "entity_id", "observed_at"]

REQUIRED_COLUMNS = {
    "record_id",
    "observed_at",
    "entity_id",
    "entity_name",
    "category",
    "metric_name",
    "metric_value",
    "metric_unit",
    "source_record_id",
    "data_version",
}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _single_value(frame: pd.DataFrame, column: str, context: str) -> Any:
    values = frame[column].dropna().unique().tolist()
    if len(values) != 1:
        raise ValueError(
            f"{context}: expected exactly one distinct {column}, found {values}"
        )
    return values[0]


def load_and_pair(canonical_csv: str | Path) -> pd.DataFrame:
    """Validate canonical records and pair the four measures per observation."""

    path = Path(canonical_csv)
    if not path.is_file():
        raise FileNotFoundError(f"Canonical dataset not found: {path}")

    frame = pd.read_csv(path)

    missing_columns = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if frame.empty:
        raise ValueError("Canonical dataset is empty.")

    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        missing = frame[list(REQUIRED_COLUMNS)].isna().sum()
        missing = missing[missing > 0].to_dict()
        raise ValueError(f"Required fields contain missing values: {missing}")

    if set(frame["data_version"].astype(str).unique()) != {DATASET_VERSION}:
        raise ValueError(
            f"Expected dataset version {DATASET_VERSION}; "
            f"found {sorted(frame['data_version'].astype(str).unique())}"
        )

    unexpected_metrics = sorted(
        set(frame["metric_name"].astype(str).unique()) - EXPECTED_METRICS
    )
    missing_metrics = sorted(
        EXPECTED_METRICS - set(frame["metric_name"].astype(str).unique())
    )
    if unexpected_metrics or missing_metrics:
        raise ValueError(
            f"Unexpected metrics: {unexpected_metrics}; "
            f"missing metrics: {missing_metrics}"
        )

    frame["metric_value"] = pd.to_numeric(
        frame["metric_value"], errors="raise"
    )

    values = frame["metric_value"].astype(float)
    if not values.map(math.isfinite).all():
        raise ValueError("Financial values must all be finite.")
    if (values < 0).any():
        raise ValueError("Negative financial values are not supported.")

    if frame["record_id"].duplicated().any():
        duplicates = frame.loc[
            frame["record_id"].duplicated(keep=False), "record_id"
        ].tolist()
        raise ValueError(f"Duplicate canonical record IDs: {duplicates}")

    if frame.duplicated(SOURCE_KEY + ["metric_name"]).any():
        raise ValueError("Duplicate source-observation and metric combinations.")

    frame["observed_at"] = pd.to_datetime(
        frame["observed_at"], utc=True, errors="raise"
    )

    currencies = sorted(frame["metric_unit"].astype(str).unique().tolist())
    if len(currencies) != 1:
        raise ValueError(
            f"Mixed currency units are not supported in one comparison: {currencies}"
        )

    paired_rows = []

    for key, group in frame.groupby(SOURCE_KEY, sort=True, dropna=False):
        context = "/".join(str(part) for part in key)

        counts = group["metric_name"].value_counts().to_dict()
        if set(counts) != EXPECTED_METRICS or any(
            counts.get(metric, 0) != 1 for metric in EXPECTED_METRICS
        ):
            raise ValueError(
                f"{context}: expected exactly one of each financial measure; "
                f"found {counts}"
            )

        department = _single_value(group, "entity_name", context)
        category = _single_value(group, "category", context)
        currency = _single_value(group, "metric_unit", context)
        version = _single_value(group, "data_version", context)

        measures = group.set_index("metric_name")["metric_value"].to_dict()
        record_ids = group.set_index("metric_name")["record_id"].to_dict()

        paired_rows.append(
            {
                "source_record_id": str(key[0]),
                "entity_id": str(key[1]),
                "observed_at": key[2],
                "period": key[2].strftime("%Y-%m"),
                "department": str(department),
                "category": str(category),
                "currency_unit": str(currency),
                "data_version": str(version),
                "budget_amount": float(measures["budget_amount"]),
                "actual_amount": float(measures["actual_amount"]),
                "committed_amount": float(measures["committed_amount"]),
                "forecast_amount": float(measures["forecast_amount"]),
                "canonical_record_ids": [
                    str(record_ids[metric]) for metric in sorted(EXPECTED_METRICS)
                ],
            }
        )

    paired = pd.DataFrame(paired_rows)
    if paired.empty:
        raise ValueError("No complete source observations were produced.")

    # Each cost centre must retain one department and one category.
    mappings = paired.groupby("entity_id").agg(
        departments=("department", "nunique"),
        categories=("category", "nunique"),
    )
    if (mappings["departments"] != 1).any():
        raise ValueError("A cost centre maps to multiple departments.")
    if (mappings["categories"] != 1).any():
        raise ValueError("A cost centre maps to multiple categories.")

    return paired.sort_values(
        ["observed_at", "entity_id", "source_record_id"]
    ).reset_index(drop=True)


def _aggregate_group(
    group: pd.DataFrame,
    dimension: str,
    group_key: str,
    result_type: str,
    period_start: str,
    period_end: str,
    generated_at: str,
) -> dict[str, Any]:
    """Create one evidence-backed descriptive comparison."""

    budget = float(group["budget_amount"].sum())
    actual = float(group["actual_amount"].sum())
    committed = float(group["committed_amount"].sum())
    forecast = float(group["forecast_amount"].sum())

    variance = actual - budget
    variance_percentage = (variance / budget * 100.0) if budget != 0 else None

    source_count = int(group["source_record_id"].nunique())
    entity_ids = sorted(group["entity_id"].astype(str).unique().tolist())

    if variance > 0:
        category = "overspend"
    elif variance < 0:
        category = "underspend"
    else:
        category = "on_budget"

    is_monthly = result_type.startswith("monthly_")
    if is_monthly:
        quality_status = (
            "insufficient_evidence"
            if source_count < MINIMUM_OVERALL_GROUP_SIZE
            else "validated_with_limitations"
        )
        limitations = [
            "Monthly subgroup results are descriptive and are not overall rankings."
        ]
        if source_count < MINIMUM_OVERALL_GROUP_SIZE:
            limitations.append(
                f"Only {source_count} independent source observation(s); "
                f"the overall evidence threshold is {MINIMUM_OVERALL_GROUP_SIZE}."
            )
    else:
        quality_status = (
            "validated_with_limitations"
            if source_count >= MINIMUM_OVERALL_GROUP_SIZE
            else "insufficient_evidence"
        )
        limitations = [
            "All source observations are synthetic.",
            "The dataset contains only 18 independent source observations.",
            "Results describe the supplied period and do not establish population-level conclusions.",
        ]
        if source_count < MINIMUM_OVERALL_GROUP_SIZE:
            limitations.append(
                f"Group has {source_count} independent observations; "
                f"minimum required is {MINIMUM_OVERALL_GROUP_SIZE}."
            )

    if budget == 0:
        limitations.append(
            "Variance percentage is unavailable because aggregate Budget is zero."
        )

    dimension_label = {
        "cost_centre": "cost centre",
        "department": "department",
        "expenditure_category": "expenditure category",
    }[dimension]

    direction = {
        "overspend": "above budget",
        "underspend": "below budget",
        "on_budget": "equal to budget",
    }[category]

    finding = (
        f"{dimension_label.title()} {group_key} recorded actual spending "
        f"${actual:,.2f} against budget ${budget:,.2f}, "
        f"a variance of ${variance:,.2f} ({direction})."
    )

    if variance_percentage is not None:
        finding += f" The aggregate variance is {variance_percentage:.2f}%."

    evidence = {
        "budget_total": budget,
        "actual_total": actual,
        "variance_amount": variance,
        "variance_percentage": variance_percentage,
        "committed_total": committed,
        "forecast_total": forecast,
        "independent_source_count": source_count,
        "canonical_record_ids": sorted(
            {
                record_id
                for record_list in group["canonical_record_ids"]
                for record_id in record_list
            }
        ),
        "source_record_ids": sorted(
            group["source_record_id"].astype(str).unique().tolist()
        ),
        "reporting_period": {
            "period_start": period_start,
            "period_end": period_end,
        },
        "currency_unit": str(group["currency_unit"].iloc[0]),
        "aggregation_method": (
            "sum of source-observation Budget and Actual; "
            "variance = aggregate Actual - aggregate Budget; "
            "percentage = aggregate variance / aggregate Budget * 100"
        ),
    }

    stable_key = group_key.replace(" ", "_").replace("&", "and")
    period_key = period_start.replace("-", "")
    result_id = f"track-a-{result_type}-{period_key}-{stable_key}".lower()

    entity_id = group_key if dimension == "cost_centre" else None

    return {
        "result_id": result_id,
        "result_type": result_type,
        "record_id": None,
        "entity_id": entity_id,
        "group_key": group_key,
        "period_start": period_start,
        "period_end": period_end,
        "metric_name": "budget_vs_actual_variance",
        "result_value": variance,
        "result_unit": str(group["currency_unit"].iloc[0]),
        "result_category": category,
        "priority_rank": None,
        "finding": finding,
        "evidence": evidence,
        "method_version": METHOD_VERSION,
        "data_version": str(group["data_version"].iloc[0]),
        "generated_at": generated_at,
        "quality_status": quality_status,
        "limitation": limitations,
    }


def _rank_overall(results: list[dict[str, Any]]) -> None:
    """Rank eligible overall groups by absolute variance, with stable ties."""

    by_type: dict[str, list[dict[str, Any]]] = {}

    for result in results:
        if result["result_type"].startswith("monthly_"):
            continue
        if result["quality_status"] == "insufficient_evidence":
            continue
        by_type.setdefault(result["result_type"], []).append(result)

    for group_results in by_type.values():
        ordered = sorted(
            group_results,
            key=lambda item: (
                -abs(float(item["result_value"])),
                str(item["group_key"]).casefold(),
            ),
        )
        for rank, result in enumerate(ordered, start=1):
            result["priority_rank"] = rank


def build_comparisons(
    paired: pd.DataFrame,
    generated_at: str | None = None,
) -> list[dict[str, Any]]:
    """Build overall and monthly Track A comparisons."""

    if paired.empty:
        raise ValueError("Cannot build comparisons from an empty paired dataset.")

    timestamp = generated_at or _utc_timestamp()
    first_period = paired["observed_at"].min()
    last_period = paired["observed_at"].max()

    overall_start = first_period.strftime("%Y-%m-%d")
    overall_end = (
        last_period + pd.offsets.MonthEnd(0)
    ).strftime("%Y-%m-%d")

    dimensions = [
        ("cost_centre", "entity_id", "cost_centre_comparison"),
        ("department", "department", "department_comparison"),
        (
            "expenditure_category",
            "category",
            "expenditure_category_comparison",
        ),
    ]

    results: list[dict[str, Any]] = []

    for dimension, column, result_type in dimensions:
        for group_key, group in paired.groupby(column, sort=True):
            results.append(
                _aggregate_group(
                    group=group,
                    dimension=dimension,
                    group_key=str(group_key),
                    result_type=result_type,
                    period_start=overall_start,
                    period_end=overall_end,
                    generated_at=timestamp,
                )
            )

    monthly_types = {
        "cost_centre": "monthly_cost_centre_comparison",
        "department": "monthly_department_comparison",
        "expenditure_category": "monthly_expenditure_category_comparison",
    }

    for period, period_group in paired.groupby("period", sort=True):
        period_start = f"{period}-01"
        period_end = (
            pd.Period(period, freq="M").end_time.strftime("%Y-%m-%d")
        )

        for dimension, column, _ in dimensions:
            result_type = monthly_types[dimension]
            for group_key, group in period_group.groupby(column, sort=True):
                results.append(
                    _aggregate_group(
                        group=group,
                        dimension=dimension,
                        group_key=str(group_key),
                        result_type=result_type,
                        period_start=period_start,
                        period_end=period_end,
                        generated_at=timestamp,
                    )
                )

    _rank_overall(results)

    results.sort(
        key=lambda item: (
            item["result_type"],
            item["period_start"],
            item["priority_rank"] is None,
            item["priority_rank"] if item["priority_rank"] is not None else 0,
            item["group_key"].casefold(),
        )
    )

    ids = [result["result_id"] for result in results]
    if len(ids) != len(set(ids)):
        raise ValueError("Generated result identifiers are not unique.")

    return results


def run_analysis(
    canonical_csv: str | Path,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Run canonical validation, pairing and comparative analysis."""

    timestamp = generated_at or _utc_timestamp()
    paired = load_and_pair(canonical_csv)
    results = build_comparisons(paired, generated_at=timestamp)

    return {
        "project_id": "poc-4-budget-vs-actual-variance-navigator",
        "project_title": "Budget vs Actual Variance Navigator",
        "approved_track": "Track A — Comparative Intelligence",
        "contract_version": CONTRACT_VERSION,
        "dataset_version": DATASET_VERSION,
        "method_version": METHOD_VERSION,
        "generated_at": timestamp,
        "result_count": len(results),
        "results": results,
    }
