
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = ROOT / "data-science/outputs/representativeness_assessment.json"
OUTPUT_FILE = ROOT / "docs/REPRESENTATIVENESS_ASSESSMENT.md"


def main():
    data = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))

    coverage = data.get("coverage_comparison", {})
    temporal = data.get("temporal_coverage", {})
    mapping = data.get("mapping_verification", {})
    checks = data.get("checks", {})
    limitations = data.get("limitations", [])

    lines = [
        "# REPRESENTATIVENESS ASSESSMENT",
        "",
        "## 1. Assessment Overview",
        "",
        f"- Assessment version: {data.get('assessment_version', 'Not specified')}",
        f"- Assessment result: **{data.get('assessment', 'Not specified')}**",
        f"- Source observations: {data.get('source_observation_count', 0)}",
        f"- Canonical records: {data.get('canonical_record_count', 0)}",
        f"- Canonical source identifiers: {data.get('canonical_source_id_count', 0)}",
        f"- Expected source-metric mappings: {mapping.get('expected_source_metric_pairs', 0)}",
        f"- Actual canonical source-metric mappings: {mapping.get('actual_canonical_source_metric_pairs', 0)}",
        "",
        "## 2. Transformation and Record Relationships",
        "",
        data.get("transformation_note", "Transformation relationship not documented."),
        "",
        "Expected metrics:",
        ""
    ]

    for metric in data.get("expected_metric_names", []):
        lines.append(f"- `{metric}`")

    lines.extend([
        "",
        "The canonical measurement rows are derived from source observations. "
        "They are not independent source transactions.",
        "",
        "## 3. Source-to-Canonical Coverage",
        ""
    ])

    for name, details in coverage.items():
        lines.extend([
            f"### {name.replace('_', ' ').title()}",
            "",
            f"- Source field: `{details.get('source_field')}`",
            f"- Canonical field: `{details.get('canonical_field')}`",
            f"- Source unique values: {details.get('source_unique_count', 0)}",
            f"- Canonical unique values: {details.get('canonical_unique_count', 0)}",
            f"- All source values preserved: **{details.get('all_source_values_preserved', False)}**",
            f"- Missing from canonical: {details.get('missing_from_canonical', [])}",
            f"- Unexpected in canonical: {details.get('unexpected_in_canonical', [])}",
            ""
        ])

    lines.extend([
        "## 4. Temporal Coverage",
        "",
        f"- Source reporting periods: {temporal.get('source_reporting_period_count', 0)}",
        f"- Canonical reporting periods: {temporal.get('canonical_reporting_period_count', 0)}",
        f"- All reporting periods preserved: **{temporal.get('all_reporting_periods_preserved', False)}**",
        "",
        "Source reporting dates:"
    ])

    for period in temporal.get("source_reporting_dates", []):
        lines.append(f"- {period}")

    lines.extend(["", "Canonical reporting dates:"])

    for period in temporal.get("canonical_reporting_dates", []):
        lines.append(f"- {period}")

    lines.extend([
        "",
        "## 5. Source-to-Canonical Mapping Verification",
        "",
        f"- Expected source-metric pairs: {mapping.get('expected_source_metric_pairs', 0)}",
        f"- Actual canonical source-metric pairs: {mapping.get('actual_canonical_source_metric_pairs', 0)}",
        f"- Missing mappings: {len(mapping.get('missing_mappings', []))}",
        f"- Unexpected mappings: {len(mapping.get('unexpected_mappings', []))}",
        f"- Duplicate mappings: {len(mapping.get('duplicate_mappings', []))}",
        f"- Field mismatches: {len(mapping.get('field_mismatches', []))}",
        f"- Incorrect metric sets: {len(mapping.get('incorrect_metric_sets', {}))}",
        f"- Source value or date errors: {len(mapping.get('source_value_or_date_errors', []))}",
        "",
        "## 6. Assessment Checks",
        "",
        "| Check | Result |",
        "|---|---|"
    ])

    for check_name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        lines.append(f"| {check_name.replace('_', ' ').title()} | {result} |")

    lines.extend([
        "",
        f"**Checks passed: {data.get('checks_passed', 0)} / {data.get('checks_total', len(checks))}**",
        "",
        "## 7. Distribution Evidence",
        "",
        "### Source observation distributions",
        "",
        "```json",
        json.dumps(data.get("source_observation_distributions", {}), indent=2, ensure_ascii=False),
        "```",
        "",
        "### Canonical record distributions",
        "",
        "```json",
        json.dumps(data.get("canonical_record_distributions", {}), indent=2, ensure_ascii=False),
        "```",
        "",
        "## 8. Limitations",
        ""
    ])

    for limitation in limitations:
        lines.append(f"- {limitation}")

    lines.extend([
        "",
        "## 9. Conclusion",
        ""
    ])

    if data.get("all_mapping_coverage_checks_passed", False):
        lines.append(
            "**The source-to-canonical mapping and supplied sample coverage "
            "checks passed. This finding is limited to the preserved synthetic "
            "source sample and does not establish real-world representativeness.**"
        )
    else:
        lines.append(
            "**Mapping or coverage review is required. One or more assessment "
            "checks did not pass. Review the detailed mapping evidence before "
            "treating the canonical dataset as representative of the supplied sample.**"
        )

    lines.extend([
        "",
        "## 10. Full Machine-Readable Evidence",
        "",
        "The complete assessment output is available at "
        "`data-science/outputs/representativeness_assessment.json`.",
        ""
    ])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("Representativeness report created:", OUTPUT_FILE)
    print("Assessment:", data.get("assessment", "Not specified"))
    print(
        "Checks passed:",
        data.get("checks_passed", 0),
        "/",
        data.get("checks_total", len(checks))
    )


if __name__ == "__main__":
    main()
