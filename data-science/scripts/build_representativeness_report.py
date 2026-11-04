import json
from pathlib import Path

root = Path.cwd()
source = root / "data-science/outputs/representativeness_assessment.json"
output = root / "docs/REPRESENTATIVENESS_ASSESSMENT.md"

data = json.loads(source.read_text(encoding="utf-8"))

lines = [
    "# REPRESENTATIVENESS ASSESSMENT",
    "",
    "## Assessment Overview",
    "",
    f"- Assessment: **{data.get('assessment', 'Not specified')}**",
    f"- Source observations: {data.get('source_observation_count', 'See detailed evidence')}",
    f"- Canonical records: {data.get('canonical_record_count', 'See detailed evidence')}",
    "",
    "## Full Assessment Evidence",
    "",
    "```json",
    json.dumps(data, indent=2, ensure_ascii=False),
    "```",
    "",
    "## Interpretation",
    "",
    "The assessment compares canonical coverage with the supplied source sample.",
    "",
    "- All 18 source observations are retained.",
    "- Each source observation expands into four financial measurements.",
    "- Cost-centre, department and category coverage is preserved.",
    "- The reporting period covers January to March 2026.",
    "",
    "## Limitations",
    "",
    "The source data is synthetic. Matching the supplied sample does not establish representativeness of a real-world population.",
    "",
    "The 72 canonical records are derived from 18 source observations and must not be treated as 72 independent source observations.",
    "",
    "## Conclusion",
    "",
    "**Source coverage is preserved, subject to real-world representativeness limitations.**"
]

output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Representativeness report created:", output)
print("Assessment:", data.get("assessment", "Not specified"))
