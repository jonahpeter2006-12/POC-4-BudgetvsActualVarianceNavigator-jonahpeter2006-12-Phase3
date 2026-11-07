# Data Intelligence Page Plan

## Project
- PoC: 4 — Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 — Post #4
- Approved analytical track: Track A — Comparative Intelligence

## Objective
Integrate the approved Post #3 analytical outputs into a separate Data Intelligence page without changing or disrupting the existing operational dashboard.

## Approval boundary
Post #3 was approved, including its documented limitations. Post #4 is an integration task. It does not authorize a new analytical method, model, ranking algorithm, or recalculation in the frontend.

## Architecture decision
Use Pattern A: the existing FastAPI backend reads the approved JSON artifacts and exposes read-only API endpoints. The Next.js frontend consumes those endpoints.

## Approved source artifacts
- data-science/outputs/intelligence_results.json
- data-science/outputs/intelligence_summary.json
- data-science/outputs/validation_metrics.json
- data-science/outputs/weak_case_review.json
- data-science/outputs/sensitivity_review.json
- data-science/outputs/baseline_reconciliation.json

Canonical source:
- data/canonical/intelligence_data.csv

The browser must not receive or process the raw canonical CSV.

## Proposed route
`/data-intelligence`

The existing `/` operational dashboard remains available and must retain its current behavior.

## Proposed API endpoints
- GET /api/intelligence/health
- GET /api/intelligence/metadata
- GET /api/intelligence/summary
- GET /api/intelligence/results
- GET /api/intelligence/results/{result_id}

All endpoints are read-only.

## Integration principles
1. Consume approved JSON outputs; do not hardcode findings.
2. Do not recalculate financial metrics or rankings in the frontend.
3. Preserve result IDs, evidence, method versions, dataset versions, and quality statuses.
4. Keep overall comparisons separate from monthly insufficient-evidence findings.
5. Display absolute variance and percentage variance as distinct measures.
6. Keep Budget, Actual, Committed, and Forecast distinct.
7. Display limitations and sensitivity findings clearly.
8. Provide loading, error, empty, and stale-data states.
9. Do not claim predictive accuracy or population-level validity.

## Implementation sequence
1. Complete and review the integration documentation.
2. Implement backend artifact loading and API contracts.
3. Test backend endpoints against approved JSON artifacts.
4. Implement the separate Next.js route.
5. Test filters, evidence details, and responsive states.
6. Run fresh operational dashboard regression tests.
7. Complete UAT and prepare the Post #4 submission.

## Completion gate
Do not begin Post #5 until the Post #4 reviewer explicitly approves the Data Intelligence Page.
