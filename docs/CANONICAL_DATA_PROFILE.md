# CANONICAL DATA PROFILE

## 1. Dataset Overview

- Dataset: `data/canonical/intelligence_data.csv`
- Dataset name: Budget vs Actual Variance Navigator - Canonical Intelligence Data
- Data version: 1.0.0
- Schema version: 1.0.0
- Records: 72
- Columns: 20
- File size: 12,991 bytes

## 2. Schema Verification

| Check | Result |
|---|---|
| Declared rows | 72 |
| Observed rows | 72 |
| Declared columns | 20 |
| Observed columns | 20 |
| Column order matches schema | True |
| Row count matches schema | True |
| Column count matches schema | True |
| Missing columns | 0 |
| Unexpected columns | 0 |

## 3. Column Completeness and Uniqueness

| Column | Non-null | Null | Null % | Unique | Required | Nullable |
|---|---:|---:|---:|---:|---|---|
| `record_id` | 72 | 0 | 0.0% | 72 | True | False |
| `record_type` | 72 | 0 | 0.0% | 1 | True | False |
| `observed_at` | 72 | 0 | 0.0% | 3 | True | False |
| `entity_id` | 72 | 0 | 0.0% | 6 | True | False |
| `related_entity_id` | 0 | 72 | 100.0% | 0 | False | True |
| `entity_name` | 72 | 0 | 0.0% | 4 | True | False |
| `category` | 72 | 0 | 0.0% | 6 | True | False |
| `subcategory` | 0 | 72 | 100.0% | 0 | False | True |
| `status` | 0 | 72 | 100.0% | 0 | False | True |
| `stage` | 0 | 72 | 100.0% | 0 | False | True |
| `metric_name` | 72 | 0 | 0.0% | 4 | True | False |
| `metric_value` | 72 | 0 | 0.0% | 47 | True | False |
| `metric_unit` | 72 | 0 | 0.0% | 1 | True | False |
| `text_value` | 0 | 72 | 100.0% | 0 | False | True |
| `latitude` | 0 | 72 | 100.0% | 0 | False | True |
| `longitude` | 0 | 72 | 100.0% | 0 | False | True |
| `source_name` | 72 | 0 | 0.0% | 1 | True | False |
| `source_record_id` | 72 | 0 | 0.0% | 18 | True | False |
| `is_synthetic` | 72 | 0 | 0.0% | 1 | True | False |
| `data_version` | 72 | 0 | 0.0% | 1 | True | False |

## 4. Numeric Metric Profile

- Total records: 72
- Valid finite values: 72
- Invalid values: 0
- Infinite values: 0
- Minimum: 500.0000
- Maximum: 75,000.0000
- Mean: 26,902.7778
- Median: 24,000.0000
- Sample standard deviation: 20,880.0462

### Metric Distribution

| Value | Count |
|---|---:|
| actual_amount | 18 |
| budget_amount | 18 |
| committed_amount | 18 |
| forecast_amount | 18 |

### Unit Distribution

| Value | Count |
|---|---:|
| USD | 72 |

## 5. Temporal Coverage

- Total date values: 72
- Parseable dates: 72
- Unparseable dates: 0
- Parse rate: 100.0%
- Earliest date: 2026-01-01T00:00:00+00:00
- Latest date: 2026-03-01T00:00:00+00:00
- Unique reporting dates: 3
- Missing months between endpoints: []

Reporting dates:
- 2026-01-01T00:00:00+00:00
- 2026-02-01T00:00:00+00:00
- 2026-03-01T00:00:00+00:00

Timezone offsets: ['0:00:00']

## 6. Categorical Distributions

### record_type

| Value | Count |
|---|---:|
| financial_metric | 72 |

### entity_id

| Value | Count |
|---|---:|
| CC-101 | 12 |
| CC-102 | 12 |
| CC-201 | 12 |
| CC-202 | 12 |
| CC-301 | 12 |
| CC-401 | 12 |

### entity_name

| Value | Count |
|---|---:|
| Engineering | 24 |
| HR & Ops | 12 |
| Marketing | 24 |
| Sales | 12 |

### related_entity_id

| Value | Count |
|---|---:|
| (blank) | 72 |

### category

| Value | Count |
|---|---:|
| Cloud Infrastructure | 12 |
| Events & PR | 12 |
| Paid Ads & Campaigns | 12 |
| Recruitment & Onboarding | 12 |
| Software Licenses | 12 |
| Travel & Client Entertainment | 12 |

### subcategory

| Value | Count |
|---|---:|
| (blank) | 72 |

### status

| Value | Count |
|---|---:|
| (blank) | 72 |

### stage

| Value | Count |
|---|---:|
| (blank) | 72 |

### metric_name

| Value | Count |
|---|---:|
| actual_amount | 18 |
| budget_amount | 18 |
| committed_amount | 18 |
| forecast_amount | 18 |

### metric_unit

| Value | Count |
|---|---:|
| USD | 72 |

### source_name

| Value | Count |
|---|---:|
| backend/budget_data.csv | 72 |

### source_record_id

| Value | Count |
|---|---:|
| SRC-0001 | 4 |
| SRC-0002 | 4 |
| SRC-0003 | 4 |
| SRC-0004 | 4 |
| SRC-0005 | 4 |
| SRC-0006 | 4 |
| SRC-0007 | 4 |
| SRC-0008 | 4 |
| SRC-0009 | 4 |
| SRC-0010 | 4 |
| SRC-0011 | 4 |
| SRC-0012 | 4 |
| SRC-0013 | 4 |
| SRC-0014 | 4 |
| SRC-0015 | 4 |
| SRC-0016 | 4 |
| SRC-0017 | 4 |
| SRC-0018 | 4 |

### is_synthetic

| Value | Count |
|---|---:|
| true | 72 |

### data_version

| Value | Count |
|---|---:|
| 1.0.0 | 72 |

## 7. Geographic Coverage

- Latitude values present: 0
- Longitude values present: 0
- Valid coordinate pairs: 0
- Invalid coordinate pairs: 0
- Partial coordinate pairs: 0
- Empty coordinate pairs: 72

## 8. Text Coverage

- Non-empty text values: 0
- Empty text values: 72
- Average text length: 0
- Maximum text length: 0
- Schema maximum allowed length: None

## 9. Provenance and Source Relationships

- Unique source observations: 18
- All records have source IDs: True
- Duplicate source-metric pairs: 0
- Records per source observation: {'4': 18}
- Metric sets per source observation: {'actual_amount|budget_amount|committed_amount|forecast_amount': 18}
- Manifest source observation count: 18
- Observed source observation count: 18
- Source count matches manifest: True
- All sources have expected metric set: True
- Canonical rows are independent transactions: False

## 10. Version and Synthetic Classification

- Manifest dataset version: 1.0.0
- Schema version: 1.0.0
- Observed data versions: {'1.0.0': 72}
- All records match manifest version: True
- Schema version matches manifest: True
- Synthetic distribution: {'true': 72}

## 11. Interpretation and Limitations

- All records synthetic: True
- Canonical rows are independent transactions: False
- Forecast values are validated predictions: False
- Separate representativeness assessment required: True
- Real-world representativeness established: False

The 72 canonical records represent four financial measurements from each of 18 source observations. They must not be interpreted as 72 independent transactions.

All records are synthetic. The reporting window contains only January, February and March 2026. Forecast values are inherited illustrative source figures, not validated predictive outputs.

The profile describes the supplied canonical dataset. It does not establish real-world population representativeness or independent financial accuracy.

## 12. Reproducibility

Run the following commands from the project root:

```powershell
python data-science/scripts/profile_canonical_data.py
python data-science/scripts/build_profile_report.py
```

The first script profiles the canonical CSV and writes the machine-readable JSON. The second script generates this report from that JSON.

Machine-readable evidence: `data-science/outputs/canonical_profile.json`.
