# DATA ARCHETYPE CONFIRMATION

## Project
Budget vs Actual Variance Navigator

## Dataset
`data/canonical/intelligence_data.csv`

## Data Version
1.0.0

## Confirmed Archetype
**Structured Monthly Financial Measurement Panel**

## Evidence from the Canonical Dataset

- Canonical records: 72
- Original source observations: 18
- Reporting periods: January, February and March 2026
- Cost centres: 6
- Departments: 4
- Expenditure categories: 6
- Financial measurements: budget, actual, committed and forecast
- Synthetic records: 72 (100%)

Each original source observation produces four canonical financial measurement records. Therefore, the 72 canonical records must not be interpreted as 72 independent transactions.

## Why This Archetype Was Selected

The dataset contains repeated monthly financial measurements for multiple cost centres and expenditure categories.

It supports comparisons between financial measurement types and across organisational groups. It also contains a temporal dimension because observations cover three consecutive reporting months.

However, three reporting periods are insufficient to establish a reliable long-term historical trend or forecasting foundation.

The dataset is therefore best classified as a small structured monthly financial measurement panel rather than a long historical time series.

## Analytical Characteristics

| Characteristic | Finding |
|---|---|
| Structured data | Yes |
| Financial measurements | Yes |
| Multiple comparison groups | Yes |
| Monthly reporting | Yes |
| Long historical time series | No |
| Geographic data coverage | No |
| Meaningful text coverage | No |
| Operational status/stage coverage | No |
| Real-world verified observations | No |

## Supported Analytical Direction

The strongest supported direction is descriptive comparative intelligence.

The dataset can support comparisons of budget, actual, committed and illustrative forecast amounts across cost centres, departments and expenditure categories.

Short-window descriptive month-to-month comparisons are conditionally possible.

## Limitations

1. All observations are synthetic.
2. Only three reporting months are available.
3. The 72 canonical records originate from 18 source observations.
4. No independent real-world financial reference is available to verify accuracy.
5. The forecast amounts are inherited illustrative source values, not validated predictive outputs.
6. Geographic and meaningful text data are absent.

## Conclusion

The confirmed archetype is a structured monthly financial measurement panel.

It is suitable for limited descriptive comparative intelligence development. It is not currently suitable for predictive analytics, anomaly detection, risk scoring, simulation or text analysis.
