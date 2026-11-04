
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE_FILE = ROOT / "data-science/outputs/canonical_profile.json"
OUTPUT_FILE = ROOT / "docs/CANONICAL_DATA_PROFILE.md"


def fmt(value):
    if value is None:
        return "Not reported"
    if isinstance(value, float):
        return f"{value:,.4f}"
    return f"{value:,}" if isinstance(value, int) else str(value)


def add_distribution(lines, title, values):
    lines.extend(["", f"### {title}", ""])
    if not values:
        lines.append("No values reported.")
        return

    lines.extend(["| Value | Count |", "|---|---:|"])
    for key, count in values.items():
        lines.append(f"| {key} | {count} |")


def main():
    if not PROFILE_FILE.exists():
        raise FileNotFoundError(
            f"Profile JSON not found: {PROFILE_FILE}"
        )

    profile = json.loads(
        PROFILE_FILE.read_text(encoding="utf-8")
    )

    numeric = profile.get("numeric_metric_profile", {})
    dates = profile.get("date_coverage", {})
    geographic = profile.get("geographic_profile", {})
    text_profile = profile.get("text_profile", {})
    provenance = profile.get("provenance_profile", {})
    version = profile.get("version_profile", {})
    relationships = profile.get("source_relationship_profile", {})
    schema = profile.get("schema_check", {})
    interpretation = profile.get("interpretation", {})

    lines = [
        "# CANONICAL DATA PROFILE",
        "",
        "## 1. Dataset Overview",
        "",
        f"- Dataset: `{profile.get('dataset')}`",
        f"- Dataset name: {profile.get('dataset_name')}",
        f"- Data version: {profile.get('data_version')}",
        f"- Schema version: {profile.get('schema_version')}",
        f"- Records: {profile.get('record_count')}",
        f"- Columns: {profile.get('column_count')}",
        f"- File size: {fmt(profile.get('file_size_bytes'))} bytes",
        "",
        "## 2. Schema Verification",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| Declared rows | {schema.get('declared_row_count')} |",
        f"| Observed rows | {schema.get('observed_row_count')} |",
        f"| Declared columns | {schema.get('declared_column_count')} |",
        f"| Observed columns | {schema.get('observed_column_count')} |",
        f"| Column order matches schema | {schema.get('column_order_matches_schema')} |",
        f"| Row count matches schema | {schema.get('row_count_matches_schema')} |",
        f"| Column count matches schema | {schema.get('column_count_matches_schema')} |",
        f"| Missing columns | {len(schema.get('missing_columns', []))} |",
        f"| Unexpected columns | {len(schema.get('unexpected_columns', []))} |",
        "",
        "## 3. Column Completeness and Uniqueness",
        "",
        "| Column | Non-null | Null | Null % | Unique | Required | Nullable |",
        "|---|---:|---:|---:|---:|---|---|"
    ]

    for name, details in profile.get("field_completeness", {}).items():
        lines.append(
            f"| `{name}` | "
            f"{details.get('non_null_count')} | "
            f"{details.get('null_count')} | "
            f"{details.get('null_percentage')}% | "
            f"{details.get('unique_count')} | "
            f"{details.get('required_by_schema')} | "
            f"{details.get('nullable_by_schema')} |"
        )

    lines.extend([
        "",
        "## 4. Numeric Metric Profile",
        "",
        f"- Total records: {numeric.get('total_records')}",
        f"- Valid finite values: {numeric.get('valid_finite_count')}",
        f"- Invalid values: {numeric.get('invalid_count')}",
        f"- Infinite values: {numeric.get('infinite_count')}",
        f"- Minimum: {fmt(numeric.get('minimum'))}",
        f"- Maximum: {fmt(numeric.get('maximum'))}",
        f"- Mean: {fmt(numeric.get('mean'))}",
        f"- Median: {fmt(numeric.get('median'))}",
        f"- Sample standard deviation: {fmt(numeric.get('standard_deviation_sample'))}",
    ])

    add_distribution(
        lines, "Metric Distribution",
        numeric.get("metric_distribution", {})
    )
    add_distribution(
        lines, "Unit Distribution",
        numeric.get("unit_distribution", {})
    )

    lines.extend([
        "",
        "## 5. Temporal Coverage",
        "",
        f"- Total date values: {dates.get('total_values')}",
        f"- Parseable dates: {dates.get('parseable_count')}",
        f"- Unparseable dates: {dates.get('unparseable_count')}",
        f"- Parse rate: {dates.get('parse_rate_percentage')}%",
        f"- Earliest date: {dates.get('earliest')}",
        f"- Latest date: {dates.get('latest')}",
        f"- Unique reporting dates: {dates.get('unique_reporting_dates')}",
        f"- Missing months between endpoints: {dates.get('missing_months_between_endpoints')}",
        "",
        "Reporting dates:"
    ])

    for date in dates.get("reporting_dates", []):
        lines.append(f"- {date}")

    lines.extend([
        "",
        f"Timezone offsets: {dates.get('timezone_offsets')}",
        "",
        "## 6. Categorical Distributions"
    ])

    for field, values in profile.get(
        "categorical_distributions", {}
    ).items():
        add_distribution(lines, field, values)

    lines.extend([
        "",
        "## 7. Geographic Coverage",
        "",
        f"- Latitude values present: {geographic.get('latitude_non_null')}",
        f"- Longitude values present: {geographic.get('longitude_non_null')}",
        f"- Valid coordinate pairs: {geographic.get('valid_coordinate_pairs')}",
        f"- Invalid coordinate pairs: {geographic.get('invalid_coordinate_pairs')}",
        f"- Partial coordinate pairs: {geographic.get('partial_coordinate_pairs')}",
        f"- Empty coordinate pairs: {geographic.get('empty_coordinate_pairs')}",
        "",
        "## 8. Text Coverage",
        "",
        f"- Non-empty text values: {text_profile.get('non_empty_count')}",
        f"- Empty text values: {text_profile.get('empty_count')}",
        f"- Average text length: {text_profile.get('average_length')}",
        f"- Maximum text length: {text_profile.get('maximum_length')}",
        f"- Schema maximum allowed length: {text_profile.get('maximum_allowed_length')}",
        "",
        "## 9. Provenance and Source Relationships",
        "",
        f"- Unique source observations: {provenance.get('unique_source_record_count')}",
        f"- All records have source IDs: {provenance.get('all_records_have_source_ids')}",
        f"- Duplicate source-metric pairs: {provenance.get('duplicate_source_metric_pairs')}",
        f"- Records per source observation: {provenance.get('records_per_source_observation_distribution')}",
        f"- Metric sets per source observation: {provenance.get('metric_sets_per_source_observation')}",
        f"- Manifest source observation count: {relationships.get('manifest_source_observation_count')}",
        f"- Observed source observation count: {relationships.get('observed_unique_source_observation_count')}",
        f"- Source count matches manifest: {relationships.get('source_observation_count_matches_manifest')}",
        f"- All sources have expected metric set: {relationships.get('all_sources_have_expected_metric_set')}",
        f"- Canonical rows are independent transactions: {relationships.get('canonical_rows_are_independent_transactions')}",
        "",
        "## 10. Version and Synthetic Classification",
        "",
        f"- Manifest dataset version: {version.get('manifest_dataset_version')}",
        f"- Schema version: {version.get('schema_version')}",
        f"- Observed data versions: {version.get('observed_data_versions')}",
        f"- All records match manifest version: {version.get('all_records_match_manifest_version')}",
        f"- Schema version matches manifest: {version.get('schema_version_matches_manifest')}",
        f"- Synthetic distribution: {profile.get('synthetic_distribution')}",
        "",
        "## 11. Interpretation and Limitations",
        "",
        f"- All records synthetic: {interpretation.get('all_records_synthetic')}",
        f"- Canonical rows are independent transactions: {interpretation.get('canonical_rows_are_independent_transactions')}",
        f"- Forecast values are validated predictions: {interpretation.get('forecast_values_are_validated_predictions')}",
        f"- Separate representativeness assessment required: {interpretation.get('source_mapping_requires_separate_representativeness_assessment')}",
        f"- Real-world representativeness established: {interpretation.get('real_world_representativeness_established')}",
        "",
        "The 72 canonical records represent four financial measurements "
        "from each of 18 source observations. They must not be interpreted "
        "as 72 independent transactions.",
        "",
        "All records are synthetic. The reporting window contains only "
        "January, February and March 2026. Forecast values are inherited "
        "illustrative source figures, not validated predictive outputs.",
        "",
        "The profile describes the supplied canonical dataset. It does "
        "not establish real-world population representativeness or "
        "independent financial accuracy.",
        "",
        "## 12. Reproducibility",
        "",
        "Run the following commands from the project root:",
        "",
        "```powershell",
        "python data-science/scripts/profile_canonical_data.py",
        "python data-science/scripts/build_profile_report.py",
        "```",
        "",
        "The first script profiles the canonical CSV and writes the "
        "machine-readable JSON. The second script generates this report "
        "from that JSON.",
        "",
        "Machine-readable evidence: "
        "`data-science/outputs/canonical_profile.json`."
    ])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8"
    )

    print("Canonical data profile report created:", OUTPUT_FILE)
    print("Sections generated: 12")
    print("Columns documented:", len(profile.get("field_completeness", {})))


if __name__ == "__main__":
    main()
