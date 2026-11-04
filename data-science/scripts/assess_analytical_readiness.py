import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FILE = ROOT / "data/canonical/intelligence_data.csv"
PROFILE_FILE = ROOT / "data-science/outputs/canonical_profile.json"
QUALITY_FILE = ROOT / "data-science/outputs/quality_assessment.json"
REPRESENTATIVENESS_FILE = ROOT / "data-science/outputs/representativeness_assessment.json"
OUTPUT_FILE = ROOT / "data-science/outputs/analytical_readiness.json"

def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def read_canonical():
    with CANONICAL_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

def main():
    rows = read_canonical()
    profile = read_json(PROFILE_FILE)
    quality = read_json(QUALITY_FILE)
    representativeness = read_json(REPRESENTATIVENESS_FILE)

    if not rows:
        raise ValueError("Canonical dataset is empty.")

    entities = sorted({r["entity_id"] for r in rows if r["entity_id"]})
    departments = sorted({r["entity_name"] for r in rows if r["entity_name"]})
    categories = sorted({r["category"] for r in rows if r["category"]})
    dates = sorted({r["observed_at"] for r in rows if r["observed_at"]})
    metric_names = sorted({r["metric_name"] for r in rows if r["metric_name"]})
    text_count = sum(bool(r.get("text_value", "").strip()) for r in rows)
    geographic_pairs = sum(
        bool(r.get("latitude", "").strip()) and
        bool(r.get("longitude", "").strip())
        for r in rows
    )
    status_count = sum(bool(r.get("status", "").strip()) for r in rows)
    stage_count = sum(bool(r.get("stage", "").strip()) for r in rows)
    synthetic_count = sum(
        r.get("is_synthetic", "").strip().lower() == "true"
        for r in rows
    )

    # Confirm comparable financial measurements exist across groups.
    metric_distribution = Counter(r["metric_name"] for r in rows)
    source_ids = {r["source_record_id"] for r in rows if r["source_record_id"]}
    metrics_per_source = Counter(r["source_record_id"] for r in rows)

    comparable_measurements = (
        len(metric_names) >= 2
        and len(source_ids) > 0
        and all(count == len(metric_names) for count in metrics_per_source.values())
    )

    all_synthetic = synthetic_count == len(rows)
    three_months_only = len(dates) == 3

    tracks = {
        "A_comparative_intelligence": {
            "status": "supported" if (
                len(entities) >= 2 and
                len(departments) >= 2 and
                len(categories) >= 2 and
                comparable_measurements
            ) else "not_supported",
            "evidence": {
                "cost_centres": len(entities),
                "departments": len(departments),
                "categories": len(categories),
                "financial_metrics": dict(metric_distribution),
                "comparable_measurements_available": comparable_measurements
            },
            "missing_requirements": [],
            "recommendation": (
                "Proceed with descriptive budget-versus-actual comparisons "
                "across cost centres, departments and expenditure categories. "
                "Clearly label results as synthetic-data demonstrations."
            )
        },
        "B_trend_intelligence": {
            "status": "conditional" if len(dates) >= 2 else "not_supported",
            "evidence": {
                "reporting_periods": len(dates),
                "reporting_dates": dates,
                "repeated_monthly_observations_per_cost_centre": 3
            },
            "missing_requirements": [
                "A longer historical period is needed for robust trend conclusions.",
                "Business reporting and freshness expectations have not been supplied."
            ],
            "recommendation": (
                "Only short-window descriptive month-to-month comparisons are "
                "justified. Do not claim reliable long-term trends or forecasts."
            )
        },
        "C_risk_and_priority": {
            "status": "not_supported",
            "evidence": {
                "status_values_present": status_count,
                "stage_values_present": stage_count,
                "multiple_explainable_urgency_indicators": False
            },
            "missing_requirements": [
                "Multiple validated urgency or priority indicators.",
                "Business rules defining risk and priority.",
                "Operational status or stage information."
            ],
            "recommendation": (
                "Do not build a risk or priority scoring system from this dataset."
            )
        },
        "D_anomaly_detection": {
            "status": "not_supported",
            "evidence": {
                "source_observations": len(source_ids),
                "reporting_periods": len(dates),
                "independent_source_observations": len(source_ids),
                "all_records_synthetic": all_synthetic
            },
            "missing_requirements": [
                "A sufficiently large comparable historical baseline.",
                "More observations to distinguish unusual values from normal variation.",
                "Validated real-world reference behaviour."
            ],
            "recommendation": (
                "Do not develop anomaly detection. The current dataset is too "
                "small and synthetic to establish a dependable baseline."
            )
        },
        "E_segmentation": {
            "status": "conditional" if (
                len(entities) >= 2 and
                len(departments) >= 2 and
                len(categories) >= 2
            ) else "not_supported",
            "evidence": {
                "cost_centres": len(entities),
                "departments": len(departments),
                "categories": len(categories),
                "source_observations": len(source_ids)
            },
            "missing_requirements": [
                "Larger and more diverse observations for reliable generalisation.",
                "Validation that the groups represent real business populations."
            ],
            "recommendation": (
                "Descriptive grouping by cost centre, department and category "
                "is possible, but treat segments as illustrative."
            )
        },
        "F_predictive_analytics": {
            "status": "not_supported",
            "evidence": {
                "all_records_synthetic": all_synthetic,
                "reporting_periods": len(dates),
                "genuine_validated_prediction_target": False,
                "forecast_values_are_inherited_source_values": True,
                "predictive_model_validation_available": False
            },
            "missing_requirements": [
                "A genuine and clearly defined prediction target.",
                "Sufficient historical observations.",
                "Decision-time input and data-leakage assessment.",
                "Target distribution and baseline evaluation.",
                "Training and validation evidence.",
                "A validated business need for prediction."
            ],
            "recommendation": (
                "Reject predictive model development for this dataset. "
                "Existing forecast_amount values are inherited illustrative "
                "figures, not validated model predictions."
            )
        },
        "G_simulation_and_scenario": {
            "status": "not_supported",
            "evidence": {
                "explicit_scenario_dimension": False,
                "scenario_input_sets": 0,
                "parameter_variations_available": False
            },
            "missing_requirements": [
                "Explicit alternative scenario inputs.",
                "Defined variable parameters and permitted ranges.",
                "Comparable scenario outputs."
            ],
            "recommendation": (
                "Do not build simulation or scenario analysis from the current "
                "single set of supplied financial observations."
            )
        },
        "H_text_and_theme_analysis": {
            "status": "not_supported",
            "evidence": {
                "non_empty_text_values": text_count,
                "text_field_available": "text_value",
                "meaningful_text_context_available": text_count > 0
            },
            "missing_requirements": [
                "Sufficient meaningful text observations.",
                "Context linking text to categories, sources or outcomes."
            ],
            "recommendation": (
                "Do not perform text, sentiment or theme analysis because "
                "the canonical text_value field is entirely blank."
            )
        }
    }

    primary_question = (
        "Which cost centres, departments and expenditure categories show "
        "the largest budget-versus-actual differences, and where should "
        "a human reviewer focus budget review?"
    )

    decision = (
        "Support descriptive human review of budget and actual financial "
        "measurements across the available groups. Do not automate financial "
        "decisions or infer real-world performance from synthetic records."
    )

    result = {
        "assessment_version": "1.0.0",
        "canonical_dataset": "data/canonical/intelligence_data.csv",
        "data_version": profile.get("data_version", "unknown"),
        "records_assessed": len(rows),
        "data_archetype": (
            "structured_monthly_financial_measurement_panel"
        ),
        "archetype_explanation": (
            "The dataset contains repeated monthly financial measurements "
            "for multiple cost centres and categories. It has both group-based "
            "comparative structure and a short three-month temporal dimension. "
            "It is better described as a small panel of financial measurements "
            "than as a long historical time series."
        ),
        "primary_analytical_question": primary_question,
        "decision_supported": decision,
        "quality_context": {
            "quality_overall_status": quality.get("overall_status"),
            "representativeness_assessment": representativeness.get("assessment"),
            "all_records_synthetic": all_synthetic
        },
        "tracks": tracks,
        "overall_conclusion": (
            "DATA READY FOR ANALYTICAL TRACK DEVELOPMENT"
            if tracks["A_comparative_intelligence"]["status"] == "supported"
            else "DATA INSUFFICIENT FOR PHASE 3"
        ),
        "scope_warning": (
            "Readiness means only that a limited descriptive comparative "
            "track is supportable. It does not establish real-world accuracy, "
            "predictive readiness or operational decision reliability."
        )
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print("Analytical readiness assessment completed.")
    print("Tracks assessed:", len(tracks))
    for name, track in tracks.items():
        print(f'{name}: {track["status"]}')
    print("Conclusion:", result["overall_conclusion"])
    print("Output:", OUTPUT_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
