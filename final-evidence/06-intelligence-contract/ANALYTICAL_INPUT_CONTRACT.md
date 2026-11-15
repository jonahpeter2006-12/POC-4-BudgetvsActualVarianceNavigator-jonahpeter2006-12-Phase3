# ANALYTICAL INPUT CONTRACT

## 1. Contract Information

- Project: Budget vs Actual Variance Navigator
- PoC: 4
- Phase: Phase 3 — Post #3
- Approved Track: Track A — Comparative Intelligence
- Contract Version: 1.0.0
- Dataset Version: 1.0.0
- Dataset: data/canonical/intelligence_data.csv
- Data Archetype: structured_monthly_financial_measurement_panel

## 2. Input Source

The sole source of analytical input is:

data/canonical/intelligence_data.csv

No secondary dataset, manually entered financial values or external financial source may be introduced.

## 3. Required Input Fields

| Field | Role | Required | Treatment |
|---|---|---|---|
| record_id | Canonical record identifier | Yes | Preserve for evidence |
| observed_at | Reporting timestamp | Yes | Parse into reporting period |
| entity_id | Cost-centre identifier | Yes | Grouping key |
| entity_name | Department name | Yes | Grouping key |
| category | Expenditure category | Yes | Grouping key |
| metric_name | Financial measure type | Yes | Pivot into separate measures |
| metric_value | Financial amount | Yes | Numeric validation |
| metric_unit | Currency unit | Yes | Preserve and validate consistency |
| source_record_id | Original observation identifier | Yes | Pair four measures |
| data_version | Dataset version | Yes | Verify version 1.0.0 |

## 4. Financial Measures

The input contains four distinct measure types:

- budget_amount
- actual_amount
- committed_amount
- forecast_amount

Budget and Actual are required for primary variance calculations.

Committed and Forecast must remain separate measures and must not be added to Budget or Actual.

Forecast is illustrative and must not be presented as a validated prediction.

## 5. Source Observation Construction

The canonical dataset uses long-format financial measurements.

The analytical input preparation step must pivot the four metric types into one source-level observation.

The source observation key is:

source_record_id + entity_id + observed_at

Each valid source observation is expected to contain exactly one value for each of the four financial measures.

The process must reject or flag:
- Missing required measures.
- Duplicate metric records for a source observation.
- Inconsistent grouping fields within a source observation.
- Invalid numeric values.
- Unexpected metric names.
- Inconsistent currency units.
- Dataset version mismatches.

The 72 canonical rows must produce 18 source-level observations. These 18 observations, not the 72 rows, are the independent source observation count.

## 6. Financial Calculation Rules

Variance:

Actual - Budget

Variance percentage:

((Actual - Budget) / Budget) * 100

Sign convention:

- Positive: overspending.
- Negative: underspending.
- Zero: on budget.

Budget must be non-zero before calculating a percentage.

For aggregated groups, calculate:

Total Actual - Total Budget

Aggregated variance percentage:

((Total Actual - Total Budget) / Total Budget) * 100

Do not average individual observation percentages to calculate a group percentage.

## 7. Grouping Fields

Cost-centre comparison:
- entity_id
- entity_name

Department comparison:
- entity_name

Expenditure-category comparison:
- category

Monthly comparison:
- Reporting month derived from observed_at.

Every group result must retain its contributing source_record_id values and canonical record_id values.

## 8. Data Availability and Excluded Fields

The following fields are not analytical features for this track:

- related_entity_id
- subcategory
- status
- stage
- text_value
- latitude
- longitude
- source_name
- is_synthetic

The synthetic-data indicator may be retained as provenance metadata if required, but it must not be treated as a financial predictor.

Missing values in unused fields must not be filled with invented values.

## 9. Evidence and Output Requirements

Every important finding must preserve:

- Group type and group identifier.
- Department and expenditure category where applicable.
- Reporting period.
- Budget amount.
- Actual amount.
- Absolute variance.
- Variance percentage.
- Contributing source observation identifiers.
- Supporting canonical record identifiers.
- Observation count.
- Dataset version.
- Method version.

## 10. Quality and Validation Requirements

- Verify the dataset version before execution.
- Verify all required columns.
- Validate numeric and non-negative financial amounts.
- Verify exactly one Budget, Actual, Committed and Forecast value per source observation.
- Check duplicate source keys.
- Check non-zero Budget before percentage calculation.
- Verify currency consistency.
- Verify deterministic grouping and ranking.
- Independently recalculate selected findings.
- Record missing-group and weak-case effects.

## 11. Minimum Evidence Rules

For overall cost-centre, department and category rankings, require at least three independent source observations.

Report the actual source observation count for every result.

Monthly subgroup results must disclose their actual count and remain descriptive when below the overall threshold.

The minimum count is an evidence threshold for this dataset, not a claim of statistical representativeness.

## 12. Leakage and Interpretation Controls

The analysis is descriptive, not predictive.

Budget and Actual are paired measurements from the same source observation. The resulting variance is not evidence of information available before actual expenditure occurred.

Do not claim future performance, causation, statistical significance or validated financial risk.

Committed and Forecast must not be used to imply future outcomes.

## 13. Versioning

- Dataset version: 1.0.0
- Initial method version: 1.0.0
- Contract version: 1.0.0

Every generated result must identify the dataset and method versions.

Changes to required fields, transformations or financial calculation rules must be documented.

## 14. Contract Acceptance Criteria

The input contract is satisfied when:

1. Only the approved canonical dataset is read.
2. All required fields are present.
3. The 72 canonical records are correctly reshaped into 18 source observations.
4. Four financial measures are kept separate.
5. Required financial calculations follow the approved sign convention.
6. Evidence identifiers and versions are retained.
7. Invalid, duplicate or incomplete source observations are detected.
8. The process is reproducible without manual data edits.
