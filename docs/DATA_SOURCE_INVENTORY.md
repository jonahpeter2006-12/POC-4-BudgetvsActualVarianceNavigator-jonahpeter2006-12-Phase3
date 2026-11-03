# Data Source Inventory

## 1. Project Information

- **Project:** Budget vs Actual Variance Navigator
- **Phase:** Phase 3 – Canonical Data Foundation
- **Source file:** `backend/budget_data.csv`
- **Preserved source copy:** `data/source-sample/source_sample.csv`
- **Data format:** CSV
- **Encoding:** UTF-8 (to be verified)

## 2. Source Description

The source dataset contains synthetic financial budget information for six cost centres across four departments.

It covers three monthly periods: January, February, and March 2026.

The dataset is used by the existing Budget vs Actual Variance Navigator application.

## 3. Source Statistics

| Property | Value |
|---|---|
| Total records | 18 |
| Total columns | 8 |
| Cost centres | 6 |
| Departments | 4 |
| Reporting period | January–March 2026 |
| Currency | USD |
| Data classification | Synthetic |
| Binary or media content | None |

## 4. Original Source Columns

| Column | Description |
|---|---|
| `cost_centre` | Cost centre identifier |
| `department` | Department responsible for the expenditure |
| `account_category` | Financial expenditure category |
| `month` | Reporting month |
| `budget_amount` | Planned budget amount |
| `actual_amount` | Actual expenditure amount |
| `committed_amount` | Committed expenditure amount |
| `forecast_amount` | Forecast expenditure amount |

## 5. Data Categories

The dataset includes the following departments:

- Engineering
- Marketing
- Sales
- HR & Ops

It includes six cost centres:

- CC-101
- CC-102
- CC-201
- CC-202
- CC-301
- CC-401

## 6. Data Sensitivity and Safety

The source dataset is identified as synthetic financial data.

No personal information, customer records, employee identifiers, or real financial account details have been identified in the supplied records.

The dataset contains numeric financial values expressed in USD.

## 7. Extraction and Preservation

The original source is maintained at:

`backend/budget_data.csv`

A separate source snapshot was copied to:

`data/source-sample/source_sample.csv`

The original Phase 2 source file has not been modified.

All 18 source records are preserved. No sampling or reduction has been applied.

## 8. Known Limitations

- The dataset contains only three months of observations.
- The records are synthetic and do not represent verified real-world expenditure.
- The dataset does not contain transaction-level details.
- No geographical coordinates are supplied.
- Forecast values are supplied by the source and are not independently validated.

## 9. Phase 3 Usage

The preserved source snapshot will be used as the input for the Phase 3 canonical data standardization pipeline.

The canonical dataset will follow the required 20-column schema defined in the Phase 3 Canonical Data Foundation Guide.

The original source dataset will remain unchanged.