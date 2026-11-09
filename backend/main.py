
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.assistant import process_question

class AssistantQueryRequest(BaseModel):
    question: Any = None


app = FastAPI(
    title="Budget vs Actual Variance Navigator API",
    version="2.0.0",
    description="Financial performance and budget variance analytics API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://localhost:3002",
    "http://127.0.0.1:3000",
        "http://127.0.0.1:3002",
    "https://poc4-budget-frontend.onrender.com",
    "https://poc4-budget-phase3-frontend.onrender.com",
],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).resolve().parent / "budget_data.csv"

REQUIRED_COLUMNS = {
    "cost_centre",
    "department",
    "account_category",
    "month",
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
}

AMOUNT_COLUMNS = [
    "budget_amount",
    "actual_amount",
    "committed_amount",
    "forecast_amount",
]

GROUPING_COLUMNS = [
    "department",
    "month",
    "cost_centre",
    "account_category",
]


def load_data() -> pd.DataFrame:
    """Load and validate the financial CSV dataset."""
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Financial dataset was not found.",
        ) from exc
    except (OSError, pd.errors.ParserError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to read the financial dataset.",
        ) from exc

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Dataset is missing columns: {sorted(missing)}",
        )

    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="Financial dataset contains no records.",
        )

    for column in AMOUNT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[AMOUNT_COLUMNS].isna().any().any():
        raise HTTPException(
            status_code=500,
            detail="Dataset contains missing or invalid financial amounts.",
        )

    if (df[AMOUNT_COLUMNS] < 0).any().any():
        raise HTTPException(
            status_code=500,
            detail="Dataset contains negative financial amounts.",
        )

    if df[GROUPING_COLUMNS].isna().any().any():
        raise HTTPException(
            status_code=500,
            detail="Dataset contains missing grouping information.",
        )

    return df


def get_month_date(month: str) -> datetime:
    """Convert month labels such as Jan 2026 into sortable dates."""
    try:
        return datetime.strptime(month, "%b %Y")
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid month label in dataset: {month}",
        ) from exc


def money(value: Any) -> float:
    """Return a rounded numeric value for API responses."""
    return round(float(value), 2)


def apply_filters(
    df: pd.DataFrame,
    department: str | None = None,
    month: str | None = None,
) -> pd.DataFrame:
    """Validate and apply the shared dashboard filters."""

    if department:
        available_departments = df["department"].unique().tolist()

        if department not in available_departments:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Unknown department filter.",
                    "available_departments": sorted(available_departments),
                },
            )

        df = df[df["department"] == department]

    if month:
        available_months = df["month"].unique().tolist()

        if month not in available_months:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Unknown month filter.",
                    "available_months": sorted(
                        available_months,
                        key=get_month_date,
                    ),
                },
            )

        df = df[df["month"] == month]

    return df


def sort_monthly_results(result: list[dict]) -> list[dict]:
    """Sort monthly results chronologically."""
    return sorted(
        result,
        key=lambda row: get_month_date(row["month"]),
    )


def round_result_fields(
    rows: list[dict],
    fields: list[str],
) -> list[dict]:
    """Round selected numeric fields in grouped API results."""
    for row in rows:
        for field in fields:
            row[field] = money(row[field])

    return rows


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Budget vs Actual Variance Navigator",
        "version": "2.0.0",
    }


@app.get("/api/summary")
def get_summary(
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    df = apply_filters(load_data(), department, month)

    total_budget = df["budget_amount"].sum()
    total_actual = df["actual_amount"].sum()
    total_committed = df["committed_amount"].sum()
    total_forecast = df["forecast_amount"].sum()

    variance = total_actual - total_budget

    variance_pct = (
        (variance / total_budget) * 100
        if total_budget != 0
        else 0
    )

    status = (
        "Over Budget" if variance > 0
        else "Under Budget" if variance < 0
        else "On Budget"
    )

    return {
        "total_budget": money(total_budget),
        "total_actual": money(total_actual),
        "total_committed": money(total_committed),
        "total_forecast": money(total_forecast),
        "variance": money(variance),
        "variance_pct": money(variance_pct),
        "status": status,
        "record_count": int(len(df)),
        "department_count": int(df["department"].nunique()),
    }


@app.get("/api/waterfall")
def get_waterfall(
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    df = apply_filters(load_data(), department, month)

    total_budget = df["budget_amount"].sum()
    total_actual = df["actual_amount"].sum()

    grouped = (
        df.groupby("department")
        .agg(
            budget=("budget_amount", "sum"),
            actual=("actual_amount", "sum"),
        )
        .reset_index()
    )

    grouped["variance"] = grouped["actual"] - grouped["budget"]
    grouped = grouped.sort_values("department")

    waterfall_items = [
        {
            "name": "Base Budget",
            "value": money(total_budget),
            "is_total": True,
        }
    ]

    for _, row in grouped.iterrows():
        waterfall_items.append(
            {
                "name": f"{row['department']} Variance",
                "value": money(row["variance"]),
                "is_total": False,
            }
        )

    waterfall_items.append(
        {
            "name": "Final Actual",
            "value": money(total_actual),
            "is_total": True,
        }
    )

    variance_sum = grouped["variance"].sum()

    reconciles = bool(
        abs((total_budget + variance_sum) - total_actual) < 0.01
    )

    return {
        "waterfall": waterfall_items,
        "reconciliation": {
            "budget": money(total_budget),
            "variance_sum": money(variance_sum),
            "actual": money(total_actual),
            "reconciles": reconciles,
        },
    }


@app.get("/api/department-breakdown")
def get_department_breakdown(
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    df = apply_filters(load_data(), department, month)

    with duckdb.connect() as con:
        result = con.execute(
            """
            SELECT
                department,
                SUM(budget_amount) AS budget,
                SUM(actual_amount) AS actual,
                SUM(committed_amount) AS committed,
                SUM(forecast_amount) AS forecast,
                SUM(actual_amount - budget_amount) AS variance,
                CASE
                    WHEN SUM(budget_amount) = 0 THEN 0
                    ELSE ROUND(
                        SUM(actual_amount - budget_amount)
                        / SUM(budget_amount) * 100,
                        2
                    )
                END AS variance_pct
            FROM df
            GROUP BY department
            ORDER BY variance DESC
            """
        ).df().to_dict(orient="records")

    round_result_fields(
        result,
        [
            "budget",
            "actual",
            "committed",
            "forecast",
            "variance",
            "variance_pct",
        ],
    )

    return {"departments": result}


@app.get("/api/monthly-trends")
def get_monthly_trends(
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    """Return monthly financial trends with shared filters."""
    df = apply_filters(load_data(), department, month)

    with duckdb.connect() as con:
        result = con.execute(
            """
            SELECT
                month,
                SUM(budget_amount) AS budget,
                SUM(actual_amount) AS actual,
                SUM(forecast_amount) AS forecast
            FROM df
            GROUP BY month
            """
        ).df().to_dict(orient="records")

    result = sort_monthly_results(result)

    round_result_fields(
        result,
        ["budget", "actual", "forecast"],
    )

    return {"trends": result}


@app.get("/api/department-heatmap")
def get_department_heatmap(
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    df = apply_filters(load_data(), department, month)

    with duckdb.connect() as con:
        result = con.execute(
            """
            SELECT
                department,
                account_category,
                SUM(budget_amount) AS budget,
                SUM(actual_amount) AS actual,
                SUM(actual_amount - budget_amount) AS variance,
                CASE
                    WHEN SUM(budget_amount) = 0 THEN 0
                    ELSE ROUND(
                        SUM(actual_amount - budget_amount)
                        / SUM(budget_amount) * 100,
                        2
                    )
                END AS variance_pct
            FROM df
            GROUP BY department, account_category
            ORDER BY department, account_category
            """
        ).df().to_dict(orient="records")

    round_result_fields(
        result,
        ["budget", "actual", "variance", "variance_pct"],
    )

    return {"heatmap": result}


@app.get("/api/forecast")
def get_forecast(
    range_pct: float = Query(default=10.0, ge=0, le=50),
    department: str | None = Query(default=None),
    month: str | None = Query(default=None),
):
    """
    Return an illustrative forecast range.

    This is an assumption-based display range, not a statistically
    validated confidence interval. The current dataset does not
    contain historical forecast-error observations.
    """
    df = apply_filters(load_data(), department, month)

    with duckdb.connect() as con:
        result = con.execute(
            """
            SELECT
                month,
                SUM(budget_amount) AS budget,
                SUM(actual_amount) AS actual,
                SUM(forecast_amount) AS forecast
            FROM df
            GROUP BY month
            """
        ).df().to_dict(orient="records")

    result = sort_monthly_results(result)

    forecast_items = []

    for row in result:
        forecast = float(row["forecast"])
        margin = forecast * (range_pct / 100)

        forecast_items.append(
            {
                "month": row["month"],
                "budget": money(row["budget"]),
                "actual": money(row["actual"]),
                "forecast": money(forecast),
                "lower_bound": money(max(0, forecast - margin)),
                "upper_bound": money(forecast + margin),
            }
        )

    return {
        "forecast": forecast_items,
        "method": "Illustrative percentage-based range",
        "range_pct": range_pct,
        "is_statistically_validated": False,
        "disclaimer": (
            "The displayed range is assumption-based and is not "
            "a statistically validated confidence interval."
        ),
    }


@app.get("/api/filters")
def get_filters():
    df = load_data()

    months = sorted(
        df["month"].unique().tolist(),
        key=get_month_date,
    )

    return {
        "departments": sorted(df["department"].unique().tolist()),
        "months": months,
        "account_categories": sorted(
            df["account_category"].unique().tolist()
        ),
        "cost_centres": sorted(df["cost_centre"].unique().tolist()),
    }

# ============================================================
# INTELLIGENCE API - PHASE 3 POST 4
# Read-only integration of approved Track A JSON artifacts.
# Existing operational dashboard routes remain unchanged.
# ============================================================



INTELLIGENCE_OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "data-science"
    / "outputs"
)

INTELLIGENCE_PROJECT_ID = "poc-4-budget-vs-actual-variance-navigator"
INTELLIGENCE_APPROVED_TRACK = "Track A — Comparative Intelligence"


class IntelligenceArtifactError(Exception):
    """An approved intelligence artifact is missing or invalid."""


class IntelligenceStaleError(Exception):
    """Approved intelligence artifacts have incompatible versions."""


def _read_intelligence_json(filename: str) -> dict:
    path = INTELLIGENCE_OUTPUT_DIR / filename

    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, json.JSONDecodeError):
        raise IntelligenceArtifactError(
            "A required intelligence artifact is unavailable or invalid."
        )

    if not isinstance(payload, dict):
        raise IntelligenceArtifactError(
            "A required intelligence artifact has an invalid structure."
        )

    return payload


def _load_intelligence_artifacts() -> dict:
    """Load and verify the approved Post #3 intelligence artifacts."""

    filenames = {
        "results": "intelligence_results.json",
        "summary": "intelligence_summary.json",
        "validation": "validation_metrics.json",
        "weak_cases": "weak_case_review.json",
        "sensitivity": "sensitivity_review.json",
        "reconciliation": "baseline_reconciliation.json",
    }

    artifacts = {
        key: _read_intelligence_json(filename)
        for key, filename in filenames.items()
    }

    results = artifacts["results"]
    summary = artifacts["summary"]
    validation = artifacts["validation"]
    weak_cases = artifacts["weak_cases"]
    sensitivity = artifacts["sensitivity"]
    reconciliation = artifacts["reconciliation"]

    # Verify project and approved-track identity wherever supplied.
    for artifact in (
        results,
        summary,
        weak_cases,
        sensitivity,
    ):
        if (
            artifact.get("project_id") != INTELLIGENCE_PROJECT_ID
            or artifact.get("approved_track") != INTELLIGENCE_APPROVED_TRACK
        ):
            raise IntelligenceStaleError(
                "Project identity or approved track does not match."
            )

    # Verify required version fields and alignment.
    versioned_artifacts = (
        results,
        summary,
        validation,
        weak_cases,
        sensitivity,
        reconciliation,
    )

    for artifact in versioned_artifacts:
        if not artifact.get("dataset_version") or not artifact.get("method_version"):
            raise IntelligenceArtifactError(
                "A required artifact is missing version information."
            )

    expected_dataset_version = results["dataset_version"]
    expected_method_version = results["method_version"]

    for artifact in versioned_artifacts:
        if (
            artifact["dataset_version"] != expected_dataset_version
            or artifact["method_version"] != expected_method_version
        ):
            raise IntelligenceStaleError(
                "Dataset or method versions do not match."
            )

    # Contract version is defined in the results and summary artifacts.
    if (
        results.get("contract_version")
        != summary.get("contract_version")
    ):
        raise IntelligenceStaleError(
            "Output contract versions do not match."
        )

    # Check the published result collection.
    findings = results.get("results")

    if not isinstance(findings, list):
        raise IntelligenceArtifactError(
            "The intelligence results collection is invalid."
        )

    if results.get("result_count") != len(findings):
        raise IntelligenceArtifactError(
            "The published result count does not match the results."
        )

    if summary.get("result_count") != len(findings):
        raise IntelligenceStaleError(
            "Summary and results counts do not match."
        )

    for finding in findings:
        if not isinstance(finding, dict) or not finding.get("result_id"):
            raise IntelligenceArtifactError(
                "A published finding has an invalid structure."
            )

        if (
            finding.get("method_version") != expected_method_version
            or finding.get("data_version") != expected_dataset_version
        ):
            raise IntelligenceStaleError(
                "A finding has incompatible version information."
            )

    # Check the recorded validation and assessment outcomes.
    if validation.get("overall_status") != "PASS":
        raise IntelligenceArtifactError(
            "Analytical validation has not passed."
        )

    if reconciliation.get("overall_status") != "PASS":
        raise IntelligenceArtifactError(
            "Baseline and aggregation reconciliation has not passed."
        )

    if sensitivity.get("status") != "COMPLETED":
        raise IntelligenceArtifactError(
            "The sensitivity assessment is incomplete."
        )

    if weak_cases.get("weak_case_count") is None:
        raise IntelligenceArtifactError(
            "The weak-case review is incomplete."
        )

    # Ensure generated timestamps agree where they are available.
    timestamps = {
        artifact.get("generated_at")
        for artifact in (
            results,
            summary,
            validation,
            weak_cases,
            sensitivity,
        )
        if artifact.get("generated_at")
    }

    if len(timestamps) > 1:
        raise IntelligenceStaleError(
            "Intelligence artifact generation timestamps do not match."
        )

    return artifacts


def _get_verified_intelligence_artifacts() -> dict:
    try:
        return _load_intelligence_artifacts()
    except IntelligenceStaleError:
        raise HTTPException(
            status_code=503,
            detail="Intelligence artifacts are stale or version-incompatible.",
        )
    except IntelligenceArtifactError:
        raise HTTPException(
            status_code=503,
            detail="Approved intelligence artifacts are unavailable or invalid.",
        )


@app.get("/api/intelligence/health")
def intelligence_health():
    try:
        artifacts = _load_intelligence_artifacts()

        return {
            "status": "ready",
            "project_id": INTELLIGENCE_PROJECT_ID,
            "approved_track": INTELLIGENCE_APPROVED_TRACK,
            "dataset_version": artifacts["results"]["dataset_version"],
            "method_version": artifacts["results"]["method_version"],
            "result_count": artifacts["results"]["result_count"],
        }

    except IntelligenceStaleError:
        return {
            "status": "stale",
            "message": "Intelligence artifacts have incompatible versions or timestamps.",
        }

    except IntelligenceArtifactError:
        return {
            "status": "unavailable",
            "message": "Required intelligence artifacts are unavailable or invalid.",
        }


@app.get("/api/intelligence/metadata")
def intelligence_metadata():
    artifacts = _get_verified_intelligence_artifacts()
    results = artifacts["results"]
    validation = artifacts["validation"]

    return {
        "project_id": results["project_id"],
        "project_title": results.get("project_title"),
        "approved_track": results["approved_track"],
        "contract_version": results["contract_version"],
        "dataset_version": results["dataset_version"],
        "method_version": results["method_version"],
        "generated_at": results.get("generated_at"),
        "result_count": results["result_count"],
        "validation_status": validation["overall_status"],
        "validation_passed_count": validation.get("passed_count"),
        "validation_failed_count": validation.get("failed_count"),
    }


@app.get("/api/intelligence/summary")
def intelligence_summary():
    artifacts = _get_verified_intelligence_artifacts()

    return {
        "summary": artifacts["summary"],
        "validation_metrics": artifacts["validation"],
        "weak_case_review": artifacts["weak_cases"],
        "sensitivity_review": artifacts["sensitivity"],
        "baseline_reconciliation": artifacts["reconciliation"],
    }


@app.get("/api/intelligence/results")
def intelligence_results(
    result_type: str | None = None,
    quality_status: str | None = None,
    result_category: str | None = None,
    search: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    artifacts = _get_verified_intelligence_artifacts()
    findings = artifacts["results"]["results"]

    filtered = findings

    if result_type:
        filtered = [
            item for item in filtered
            if item.get("result_type") == result_type
        ]

    if quality_status:
        filtered = [
            item for item in filtered
            if item.get("quality_status") == quality_status
        ]

    if result_category:
        filtered = [
            item for item in filtered
            if item.get("result_category") == result_category
        ]

    if search:
        term = search.strip().casefold()

        if term:
            filtered = [
                item for item in filtered
                if term in " ".join(
                    str(item.get(field, ""))
                    for field in (
                        "result_id",
                        "result_type",
                        "entity_id",
                        "group_key",
                        "finding",
                        "result_category",
                    )
                ).casefold()
            ]

    total = len(filtered)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": filtered[offset:offset + limit],
    }


@app.get("/api/intelligence/results/{result_id}")
def intelligence_result_detail(result_id: str):
    artifacts = _get_verified_intelligence_artifacts()

    for finding in artifacts["results"]["results"]:
        if finding.get("result_id") == result_id:
            return {"result": finding}

    raise HTTPException(
        status_code=404,
        detail="Intelligence result not found.",
    )



@app.post("/api/assistant/query")
def assistant_query(request: AssistantQueryRequest):
    from backend.assistant import (
        build_status_response,
        is_unsafe_question,
        validate_question,
    )

    validation_error = validate_question(request.question)

    if validation_error:
        return build_status_response(
            validation_error,
            None,
            "Please provide a valid question of no more than 500 characters.",
        )

    if is_unsafe_question(request.question):
        return build_status_response(
            "UNSAFE",
            None,
            "This request cannot be processed because it violates the assistant safety rules.",
        )

    artifacts = _get_verified_intelligence_artifacts()

    try:
        return process_question(request.question, artifacts)
    except ValueError as exc:
        raise HTTPException(
            status_code=503,
            detail="Verified assistant evidence is unavailable.",
        ) from exc
