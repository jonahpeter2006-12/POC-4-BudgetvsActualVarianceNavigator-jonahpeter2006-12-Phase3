import json
from pathlib import Path

root = Path.cwd()
source = root / "data-science/outputs/analytical_readiness.json"
output = root / "docs/ANALYTICAL_READINESS_REPORT.md"

data = json.loads(source.read_text(encoding="utf-8"))

track_names = {
    "A_comparative_intelligence": "A — Comparative Intelligence",
    "B_trend_intelligence": "B — Trend Intelligence",
    "C_risk_and_priority": "C — Risk and Priority",
    "D_anomaly_detection": "D — Anomaly Detection",
    "E_segmentation": "E — Segmentation",
    "F_predictive_analytics": "F — Predictive Analytics",
    "G_simulation_and_scenario": "G — Simulation and Scenario Analysis",
    "H_text_and_theme_analysis": "H — Text and Theme Analysis"
}

lines = [
    "# ANALYTICAL READINESS REPORT",
    "",
    "## 1. Assessment Overview",
    "",
    f"- Canonical dataset: `{data['canonical_dataset']}`",
    f"- Data version: `{data['data_version']}`",
    f"- Records assessed: {data['records_assessed']}",
    f"- Assessment version: {data['assessment_version']}",
    f"- Data archetype: **{data['data_archetype']}**",
    "",
    "### Data Archetype Explanation",
    "",
    data["archetype_explanation"],
    "",
    "## 2. Primary Analytical Question",
    "",
    data["primary_analytical_question"],
    "",
    "### Decision Supported",
    "",
    data["decision_supported"],
    "",
    "## 3. Data Quality Context",
    "",
    f"- Quality assessment: `{data['quality_context']['quality_overall_status']}`",
    f"- Representativeness: `{data['quality_context']['representativeness_assessment']}`",
    f"- All records synthetic: **{data['quality_context']['all_records_synthetic']}**",
    "",
    "## 4. Analytical Readiness Matrix",
    "",
    "| Track | Status | Evidence | Missing requirements | Recommendation |",
    "|---|---|---|---|---|"
]

for key, track in data["tracks"].items():
    name = track_names.get(key, key)
    status = track["status"].replace("_", " ").title()
    evidence = json.dumps(track["evidence"], ensure_ascii=False)
    missing = "; ".join(track["missing_requirements"]) or "None identified"
    recommendation = track["recommendation"]

    def clean(value):
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines.append(
        f"| {clean(name)} | **{clean(status)}** | "
        f"{clean(evidence)} | {clean(missing)} | {clean(recommendation)} |"
    )

lines.extend([
    "",
    "## 5. Detailed Track Assessments",
    ""
])

for key, track in data["tracks"].items():
    name = track_names.get(key, key)

    lines.extend([
        f"### {name}",
        "",
        f"- **Status:** {track['status'].replace('_', ' ').title()}",
        "- **Evidence:**",
        "```json",
        json.dumps(track["evidence"], indent=2, ensure_ascii=False),
        "```",
        "- **Missing requirements:**"
    ])

    if track["missing_requirements"]:
        lines.extend(f"  - {item}" for item in track["missing_requirements"])
    else:
        lines.append("  - None identified.")

    lines.extend([
        f"- **Recommendation:** {track['recommendation']}",
        ""
    ])

lines.extend([
    "## 6. Scope and Limitations",
    "",
    data["scope_warning"],
    "",
    "The dataset contains 72 canonical measurement records derived from 18 source observations, with four financial metrics per source observation. These are not 72 independent transactions.",
    "",
    "The dataset is synthetic and covers only January to March 2026. The existing forecast values are inherited illustrative source values, not validated predictive-model outputs.",
    "",
    "## 7. Overall Conclusion",
    "",
    f"**{data['overall_conclusion']}**",
    "",
    "This conclusion supports proceeding only with the limited descriptive comparative analytical direction. It does not approve predictive modelling, risk scoring, anomaly detection or other unsupported tracks."
])

output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Analytical readiness report created:", output)
print("Tracks documented:", len(data["tracks"]))
print("Conclusion:", data["overall_conclusion"])
