# Intelligence API Contract

## Purpose
Define the proposed read-only FastAPI interface for the Post #4 Data Intelligence page.

These endpoints are a design contract. They must not be described as implemented until code and tests confirm them.

## Base path
`/api/intelligence`

## 1. GET /health
Purpose: Check whether the required approved artifacts are present, readable, and compatible.

Expected response fields:
- status
- artifacts_available
- version_alignment
- generated_at
- message

Possible status values:
- ready
- stale
- unavailable

A stale state should be based on concrete artifact/version or generation inconsistencies, not an arbitrary age threshold.

## 2. GET /metadata
Purpose: Return integration metadata.

Expected fields:
- project_id
- project_title
- approved_track
- contract_version
- dataset_version
- method_version
- generated_at
- result_count
- validation_status

## 3. GET /summary
Purpose: Return the approved intelligence summary and its relevant validation and limitation context.

Source:
- intelligence_summary.json
- validation_metrics.json
- sensitivity_review.json
- weak_case_review.json

The API must preserve source values and must not calculate replacement summary metrics.

## 4. GET /results
Purpose: Return approved findings with optional server-side filtering.

Proposed query parameters:
- result_type
- quality_status
- result_category
- search
- limit
- offset

The endpoint may filter records but must not change their values or recompute rankings.

Response should include:
- total matching count
- returned count
- limit
- offset
- results
- metadata

## 5. GET /results/{result_id}
Purpose: Return one exact finding and its evidence.

Return HTTP 404 when the result ID does not exist.

## Error behavior
- HTTP 503: required artifacts missing, unreadable, invalid, or incompatible.
- HTTP 404: requested result ID not found.
- HTTP 422: invalid query parameter values.
- HTTP 500: unexpected server error, without exposing filesystem paths or internal secrets.

## Data handling
- Resolve output paths from the repository structure, not the process working directory.
- Read only the approved JSON artifacts.
- Do not expose local filesystem paths.
- Do not expose the canonical CSV through these endpoints.
- Do not accept write operations.
- Validate required keys and version compatibility before returning data.

## Currency and measures
Preserve the source currency unit. Keep Budget, Actual, Committed, and Forecast separate. Do not add Committed or Forecast to Actual or Budget.

## Implementation verification
The contract is accepted only after endpoint tests confirm response structure, filtering, result lookup, error behavior, and version alignment against the actual approved artifacts.
