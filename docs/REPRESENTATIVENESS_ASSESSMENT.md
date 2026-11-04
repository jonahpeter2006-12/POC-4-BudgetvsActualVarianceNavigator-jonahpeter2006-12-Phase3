# REPRESENTATIVENESS ASSESSMENT

## 1. Assessment Overview

- Assessment version: 2.0.0
- Assessment result: **source_mapping_verified_with_real_world_limitations**
- Source observations: 18
- Canonical records: 72
- Canonical source identifiers: 18
- Expected source-metric mappings: 72
- Actual canonical source-metric mappings: 72

## 2. Transformation and Record Relationships

Each source observation is expected to produce exactly four canonical financial measurement rows. These are derived measurements, not independent transactions.

Expected metrics:

- `actual_amount`
- `budget_amount`
- `committed_amount`
- `forecast_amount`

The canonical measurement rows are derived from source observations. They are not independent source transactions.

## 3. Source-to-Canonical Coverage

### Cost Centres

- Source field: `cost_centre`
- Canonical field: `entity_id`
- Source unique values: 6
- Canonical unique values: 6
- All source values preserved: **True**
- Missing from canonical: []
- Unexpected in canonical: []

### Departments

- Source field: `department`
- Canonical field: `entity_name`
- Source unique values: 4
- Canonical unique values: 4
- All source values preserved: **True**
- Missing from canonical: []
- Unexpected in canonical: []

### Categories

- Source field: `account_category`
- Canonical field: `category`
- Source unique values: 6
- Canonical unique values: 6
- All source values preserved: **True**
- Missing from canonical: []
- Unexpected in canonical: []

## 4. Temporal Coverage

- Source reporting periods: 3
- Canonical reporting periods: 3
- All reporting periods preserved: **True**

Source reporting dates:
- 2026-01-01T00:00:00Z
- 2026-02-01T00:00:00Z
- 2026-03-01T00:00:00Z

Canonical reporting dates:
- 2026-01-01T00:00:00Z
- 2026-02-01T00:00:00Z
- 2026-03-01T00:00:00Z

## 5. Source-to-Canonical Mapping Verification

- Expected source-metric pairs: 72
- Actual canonical source-metric pairs: 72
- Missing mappings: 0
- Unexpected mappings: 0
- Duplicate mappings: 0
- Field mismatches: 0
- Incorrect metric sets: 0
- Source value or date errors: 0

## 6. Assessment Checks

| Check | Result |
|---|---|
| Source Observation Count Matches Manifest | PASS |
| Canonical Record Count Matches Manifest | PASS |
| All Source Observations Retained | PASS |
| Four Expected Metrics Per Source Observation | PASS |
| No Duplicate Source Metric Mappings | PASS |
| No Missing Source Metric Mappings | PASS |
| No Unexpected Source Metric Mappings | PASS |
| All Source To Canonical Values Match | PASS |
| Reporting Month Coverage Preserved | PASS |
| Cost Centre Coverage Preserved | PASS |
| Department Coverage Preserved | PASS |
| Category Coverage Preserved | PASS |

**Checks passed: 12 / 12**

## 7. Distribution Evidence

### Source observation distributions

```json
{
  "cost_centre": {
    "CC-101": 3,
    "CC-102": 3,
    "CC-201": 3,
    "CC-202": 3,
    "CC-301": 3,
    "CC-401": 3
  },
  "department": {
    "Engineering": 6,
    "Marketing": 6,
    "Sales": 3,
    "HR & Ops": 3
  },
  "category": {
    "Cloud Infrastructure": 3,
    "Software Licenses": 3,
    "Paid Ads & Campaigns": 3,
    "Events & PR": 3,
    "Travel & Client Entertainment": 3,
    "Recruitment & Onboarding": 3
  },
  "month": {
    "Jan 2026": 6,
    "Feb 2026": 6,
    "Mar 2026": 6
  }
}
```

### Canonical record distributions

```json
{
  "entity_id": {
    "CC-101": 12,
    "CC-102": 12,
    "CC-201": 12,
    "CC-202": 12,
    "CC-301": 12,
    "CC-401": 12
  },
  "entity_name": {
    "Engineering": 24,
    "Marketing": 24,
    "Sales": 12,
    "HR & Ops": 12
  },
  "category": {
    "Cloud Infrastructure": 12,
    "Software Licenses": 12,
    "Paid Ads & Campaigns": 12,
    "Events & PR": 12,
    "Travel & Client Entertainment": 12,
    "Recruitment & Onboarding": 12
  },
  "observed_at": {
    "2026-01-01T00:00:00Z": 24,
    "2026-02-01T00:00:00Z": 24,
    "2026-03-01T00:00:00Z": 24
  },
  "metric_name": {
    "budget_amount": 18,
    "actual_amount": 18,
    "committed_amount": 18,
    "forecast_amount": 18
  }
}
```

## 8. Limitations

- All supplied observations are synthetic.
- Preservation of the source sample does not establish real-world population representativeness.
- Only the reporting periods present in the source sample are assessed.
- The preserved source sample is the available comparison reference, not an independent external population.
- The canonical measurement rows must not be interpreted as independent source observations.
- Source identifiers are generated from source row order because the source sample has no independent source-record identifier.

## 9. Conclusion

**The source-to-canonical mapping and supplied sample coverage checks passed. This finding is limited to the preserved synthetic source sample and does not establish real-world representativeness.**

## 10. Full Machine-Readable Evidence

The complete assessment output is available at `data-science/outputs/representativeness_assessment.json`.
