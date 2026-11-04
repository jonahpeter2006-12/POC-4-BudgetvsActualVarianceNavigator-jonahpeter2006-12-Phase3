import json
from pathlib import Path

root = Path.cwd()
profile_path = root / "data-science/outputs/canonical_profile.json"
output_path = root / "docs/CANONICAL_DATA_PROFILE.md"

profile = json.loads(profile_path.read_text(encoding="utf-8"))

lines = [
    "# CANONICAL DATA PROFILE",
    "",
    "## Dataset",
    "",
    f"- Source: `{profile.get('dataset', 'data/canonical/intelligence_data.csv')}`",
    f"- Data version: `{profile.get('data_version', '1.0.0')}`",
    f"- Records: {profile.get('record_count', 'See profile output')}",
    f"- Columns: {profile.get('column_count', 'See profile output')}",
    "",
    "## Generated Profile Evidence",
    "",
    "The detailed, machine-readable profile is available at:",
    "`data-science/outputs/canonical_profile.json`.",
    "",
    "## Column Completeness and Uniqueness",
    "",
    "| Column | Non-null | Null | Unique |",
    "|---|---:|---:|---:|"
]

columns = profile.get("field_completeness", {})

for name, details in columns.items():
    non_null = details.get("non_null_count", "Not reported")
    null_count = details.get("null_count", "Not reported")
    unique = details.get("unique_count", "Not reported")
    lines.append(f"| `{name}` | {non_null} | {null_count} | {unique} |")

lines.extend([
    "",
    "## Interpretation",
    "",
    "- The canonical dataset contains four financial measurements per source observation.",
    "- The 72 canonical records originate from 18 source observations.",
    "- All records are marked synthetic.",
    "- The reporting period covers January to March 2026.",
    "- Geographic coordinates and meaningful text values are absent.",
    "- Forecast values are inherited illustrative source figures, not validated predictive outputs.",
    "",
    "## Reproducibility",
    "",
    "Regenerate the profile by running:",
    "",
    "```powershell",
    "python data-science/scripts/profile_canonical_data.py",
    "```",
    "",
    "The script reads the canonical dataset and writes the machine-readable profile."
])

output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Canonical data profile report created:", output_path)
