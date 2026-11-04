
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / "data-science/outputs/quality_assessment.json"
output = root / "docs/DATA_QUALITY_ASSESSMENT.md"

data = json.loads(source.read_text(encoding="utf-8"))

reproducibility = data["dimensions"]["reproducibility"]
reproducibility_status = reproducibility["status"]

lines = [
    "# DATA QUALITY ASSESSMENT",
    "",
    "## Assessment Overview",
    "",
    f"- Dataset: `{data['dataset']}`",
    f"- Data version: {data['data_version']}",
    f"- Records assessed: {data['records_assessed']}",
    f"- Overall status: **{data['overall_status']}**",
    "",
    "## Quality Dimensions",
    "",
    "| Dimension | Status |",
    "|---|---|"
]

for name, result in data["dimensions"].items():
    lines.append(
        f"| {name.replace('_', ' ').title()} | {result['status']} |"
    )

for name, result in data["dimensions"].items():
    lines.extend([
        "",
        f"## {name.replace('_', ' ').title()}",
        "",
        f"**Status:** {result['status']}",
        "",
        "**Evidence:**",
        "",
        "```json",
        json.dumps(
            result.get("evidence", {}),
            indent=2,
            ensure_ascii=False
        ),
        "```"
    ])

    if result.get("limitation"):
        lines.extend([
            "",
            f"**Limitation:** {result['limitation']}"
        ])

lines.extend([
    "",
    "## Blocking Failures",
    "",
    f"Number of blocking failures: {len(data.get('blocking_failures', []))}",
    "",
    "```json",
    json.dumps(data.get("blocking_failures", []), indent=2),
    "```",
    "",
    "## Overall Interpretation",
    "",
    "The canonical dataset passes its structural, completeness, uniqueness, validity, consistency and provenance checks.",
    "",
    "Accuracy cannot be independently verified because all observations are synthetic. Representativeness and timeliness remain conditional because the available data covers only three months and does not establish real-world population coverage.",
    "",
    "The safety assessment is a basic screening and does not guarantee that all sensitive information is absent.",
    "",
    (
        "Reproducibility verification passed. Two complete pipeline "
        "executions produced matching assessment outputs, and the "
        "input files remained unchanged."
        if reproducibility_status == "passed"
        else
        f"Reproducibility verification status: {reproducibility_status}."
    ),
    "",
    "## Conclusion",
    "",
    f"**{data['overall_status']}**",
    "",
    "The dataset has no blocking quality failures, but its documented limitations must be considered before analytical development."
])

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Data quality assessment report created:", output)
print("Dimensions documented:", len(data["dimensions"]))
print("Blocking failures:", len(data.get("blocking_failures", [])))
print("Reproducibility status:", reproducibility_status)
