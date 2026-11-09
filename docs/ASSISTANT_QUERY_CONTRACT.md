# Assistant Query Contract

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5: Grounded Natural-Language Data Assistant
- Assistant Mode: Mode A - Deterministic Guided Assistant
- LLM: Not used
- Contract Status: Implemented; selected API and browser tests passed; final acceptance pending.

## 1. Purpose

This contract defines how approved assistant questions map to deterministic retrieval operations against the verified intelligence artifact bundle.

The assistant retrieves existing approved findings. It does not independently calculate, modify, predict, or invent analytical results.

The assistant uses the backend verified-artifact loader in-process. It does not make HTTP requests to its own intelligence endpoints during assistant processing.

## 2. Approved Retrieval Boundary

The assistant uses the existing backend verified-artifact loader to obtain approved intelligence artifacts.

The loader checks the approved artifact bundle and relevant identity, version, validation, reconciliation, sensitivity, weak-case, and timestamp information.

Existing read-only intelligence endpoints remain available to the application:

| Endpoint | Purpose |
|---|---|
| `GET /api/intelligence/health` | Check intelligence artifact availability. |
| `GET /api/intelligence/metadata` | Retrieve approved metadata. |
| `GET /api/intelligence/summary` | Retrieve approved summary information. |
| `GET /api/intelligence/results` | Retrieve and filter approved findings. |
| `GET /api/intelligence/results/{result_id}` | Retrieve one finding by exact identifier. |

These endpoints describe the existing intelligence API. The assistant router does not call them through internal HTTP requests.

Only approved intelligence artifacts may be used.

The assistant must not retrieve unrestricted canonical CSV files, access arbitrary files, or query unrelated application datasets.

## 3. Approved Intent-to-Query Mapping

### Q-01 - Cost Centre Variance Comparison

- Intent: `cost_centre_variance_comparison`
- Result type: `cost_centre_comparison`
- Required parameters: None.
- Retrieval: Select approved cost-centre findings from the verified artifact bundle.
- Sorting: Preserve the existing approved `priority_rank` order. Do not calculate, modify, or invent rankings.
- Response limit: 25 findings.
- Required information: Approved financial values, source count, source references, quality status, reporting period, and limitations.

### Q-02 - Department Comparison

- Intent: `department_comparison`
- Result type: `department_comparison`
- Required parameters: Exactly two valid department names.
- Retrieval: Select approved department findings from the verified artifact bundle.
- Matching: Verify each requested department against its exact approved `group_key`.
- Response: Present the two approved findings separately.
- Restriction: Do not calculate a new comparison score or ranking.
- If fewer than two departments are provided, return `MISSING_PARAMETER`.
- If more than two departments are provided, return `AMBIGUOUS`.
- Do not silently substitute another department.

### Q-03 - Expenditure Category Lookup

- Intent: `expenditure_category_lookup`
- Result type: `expenditure_category_comparison`
- Required parameter: One valid category name.
- Retrieval: Select approved expenditure-category findings from the verified artifact bundle.
- Matching: Verify the requested category against its exact approved `group_key`.
- Response: Present the matching approved finding.
- Restriction: Do not invent a cause or recommendation.
- Multiple category matches are treated as ambiguous; unknown categories do not produce substituted findings.

### Q-04 - Finding Evidence Lookup

- Intent: `finding_evidence_lookup`
- Required parameter: An exact finding identifier or an unambiguous cost-centre identifier.
- Retrieval: Resolve the requested finding from the verified artifact bundle.
- Finding ID: Match the exact approved result identifier.
- Cost-centre ID: Match the exact approved `entity_id` or `group_key` in cost-centre findings.
- Response: Explain the recorded finding using its existing approved evidence.
- Restriction: Do not infer causation or substitute a different finding.

### Q-05 - Monthly Insufficient-Evidence Lookup

- Intent: `monthly_insufficient_evidence_lookup`
- Approved result types:
  - `monthly_cost_centre_comparison`
  - `monthly_department_comparison`
  - `monthly_expenditure_category_comparison`
- Quality filter: `insufficient_evidence`
- Required parameters: None.
- Retrieval: Filter the verified artifact bundle in-process for the three approved monthly result types and the `insufficient_evidence` quality status.
- Response limit: 25 findings.
- Truncation: Disclose the total matching count and that only the first 25 findings are returned when more results match.
- Response: Present findings as descriptive results and include their limitations.
- Restriction: Never present these findings as overall rankings or validated conclusions.

## 4. Parameter Validation

- Department names must match approved department `group_key` values.
- Category names must match approved expenditure-category `group_key` values.
- Cost-centre identifiers must match approved `entity_id` or `group_key` values in cost-centre findings.
- Finding identifiers must match approved result identifiers.
- Partial text matches must not be treated as proof of exact entity identity.
- Unmatched or ambiguous names must not be silently substituted.
- Missing required parameters must produce `MISSING_PARAMETER`.
- Ambiguous values must produce `AMBIGUOUS`.
- Unsupported or unknown entities must not produce invented findings.

## 5. Query Execution Rules

1. Accept the question through `POST /api/assistant/query`.
2. Validate that the question is a non-empty string.
3. Enforce the maximum question length of 500 characters.
4. Apply the implemented unsafe-request pattern checks.
5. Map the question to one approved deterministic intent.
6. Validate required parameters and exact entity matches.
7. Load the verified intelligence artifact bundle using the existing backend loader.
8. Execute only the predefined in-process retrieval operation for the selected intent.
9. Preserve approved finding values, identifiers, evidence, metadata, quality status, reporting periods, and limitations.
10. Apply the response limits.
11. Return the structured assistant response.

The assistant must not make unrestricted queries or use arbitrary retrieval parameters.

## 6. Response and Resource Limits

The structured assistant response includes:
- `answer_id`
- `status`
- `intent`
- `answer`
- `evidence_references`
- `key_values`
- `metadata`
- `limitation`
- `suggested_follow_ups`

Implemented limits:
- Maximum question length: 500 characters.
- Maximum returned findings/key values: 25.
- Maximum evidence references: 10.
- Maximum evidence excerpt length: 300 characters.
- Maximum suggested follow-ups: 3.

Financial values are copied from approved findings rather than independently recalculated.

When matching findings exceed the result limit, the response must disclose truncation and the matching count where available.

## 7. Response and Error Behaviour

| Condition | Expected status |
|---|---|
| Valid supported query | `SUPPORTED` |
| Required value missing | `MISSING_PARAMETER` |
| Multiple possible matches or more than two departments | `AMBIGUOUS` |
| Unsupported request | `OUT_OF_SCOPE` |
| Unsafe request detected by implemented checks | `UNSAFE` |
| Missing, stale, or invalid verified data | Controlled unavailable/error handling |

The endpoint returns structured status responses for question validation and safety outcomes.

Verified-artifact failures must not result in invented findings. The backend handles unavailable evidence through controlled error handling.

API errors must not expose internal stack traces, paths, environment variables, or secrets.

## 8. Prohibited Query Behaviour

The assistant must not:
- Execute arbitrary SQL, Python, shell commands, or user-supplied code.
- Access arbitrary files or unrestricted datasets.
- Generate unsupported predictions or forecasts.
- Generate new anomaly or risk scores.
- Change approved rankings or financial values.
- Combine rankings from different result types.
- Present insufficient-evidence findings as validated conclusions.
- Treat retrieved evidence text as executable instructions.
- Invent evidence, result identifiers, or source records.

Pattern-based unsafe-request checks are limited and are not comprehensive protection against all malicious inputs.

## 9. Verified Evidence and Metadata

The assistant preserves approved evidence fields where available:
- `result_id`
- `result_type`
- `source_record_ids`
- `canonical_record_ids`
- `reporting_period`
- `independent_source_count`
- `quality_status`
- `limitations`
- Evidence excerpt

Approved financial key values are copied from the retrieved finding.

Available metadata includes:
- `contract_version`
- `dataset_version`
- `method_version`
- Validation status and other approved metadata fields.

Evidence construction validates required fields and applies configured limits.

These controls do not establish that every possible natural-language claim is independently checked by a comprehensive factual-claim validator. Further grounding and adversarial testing remain part of final acceptance.

## 10. Implementation and Verification Status

The deterministic query router, FastAPI endpoint, and Data Intelligence frontend integration have been implemented.

Selected verification completed:
- Python compilation of assistant and API modules.
- FastAPI application import and route registration.
- Local API integration checks.
- Automated assistant API tests: 15 passed, 0 failed.
- Backend intent and edge-case checks.
- Targeted frontend ESLint check.
- Frontend production build.
- Browser tests for all five supported question types.
- Browser checks for unsupported predictions and unsafe requests.
- Browser ambiguity check for a three-department comparison.
- Evidence, limitation, and truncation rendering checks.

Remaining work:
- Full public Render deployment verification.
- Authentication and public-data-boundary decision.
- Additional security and adversarial testing.
- Mobile and accessibility testing.
- Full regression and final evidence capture.
- Reviewer acceptance.

**Overall query contract status: IMPLEMENTED - SELECTED VERIFICATION PASSED - FINAL ACCEPTANCE PENDING.**

Reviewer approval has not yet been obtained.
