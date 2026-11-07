# Data Intelligence UI Specification

## Route
`/data-intelligence`

## Design objective
Create a clear, evidence-led intelligence page that complements the existing operational dashboard. Preserve the existing visual language and do not replace the current dashboard.

## Page sections

### 1. Header
- Page title: Data Intelligence
- Short explanation of the approved comparative analysis
- Link back to the operational dashboard
- Visible dataset and method version information

### 2. Summary cards
Show a small set of approved summary values, such as:
- Overall comparison count
- Monthly descriptive finding count
- Validation status
- Sensitivity status

Values must come from the API, not hardcoded frontend constants.

### 3. Filters
Provide filters for:
- Comparison type
- Quality status
- Variance category
- Text search

Filters may narrow displayed results. They must not recalculate or reorder analytical rankings.

### 4. Overall comparative intelligence
Display the three overall comparison types separately:
- Cost centre
- Department
- Expenditure category

Preserve the approved priority ranks and show the basis of comparison.

### 5. Monthly descriptive findings
Display monthly findings in a separate section with a clear insufficient-evidence warning. Do not present these records as reliable trends, forecasts, or risk scores.

### 6. Results table
Show useful fields including:
- Group
- Comparison type
- Budget
- Actual
- Absolute variance
- Percentage variance
- Classification
- Evidence count
- Quality status

### 7. Evidence detail
Allow a user to inspect an individual finding, including source references, reporting period, aggregation method, and limitation.

### 8. Methodology and validation
Explain Actual minus Budget, the quality threshold, validation evidence, reconciliation, and sensitivity assessment.

### 9. Limitations
Display synthetic-data and representativeness limitations, insufficient monthly evidence, and sensitivity caveats.

### 10. Data freshness
Show generated timestamp and version metadata. If artifact alignment fails, show a stale or unavailable state.

## Required UI states
- Loading
- API error
- Empty filtered results
- Stale or incompatible artifacts
- Ready state

## Accessibility and responsiveness
- Semantic headings and table markup
- Keyboard-accessible filters and detail controls
- Visible focus indicators
- Clear text labels; do not rely on color alone
- Responsive layout for narrow screens
- Sufficient contrast and readable data labels

## Prohibited UI behavior
- No frontend financial calculations.
- No new ranking logic.
- No invented insights or values.
- No presentation of monthly insufficient-evidence findings as validated overall comparisons.
- No implication that the illustrative operational forecast is a validated prediction.
