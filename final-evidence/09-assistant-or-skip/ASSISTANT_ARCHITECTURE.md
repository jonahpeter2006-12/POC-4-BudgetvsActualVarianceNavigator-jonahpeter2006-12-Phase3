# Assistant Architecture

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5: Grounded Natural-Language Data Assistant
- Assistant Mode: Mode A - Deterministic Guided Assistant
- LLM: Not used
- Architecture Status: Implemented; selected API and browser tests passed; final acceptance pending.

## 1. Purpose

This document describes the implemented deterministic, evidence-grounded assistant for retrieving and understanding approved Budget vs Actual Variance Navigator intelligence findings.

The assistant uses predefined question intents, validated parameters, verified intelligence artifacts, deterministic routing, and controlled response structures.

It does not independently generate financial analysis, predictions, or unsupported conclusions.

## 2. Implemented Request Flow

User Question
-> Input Validation
-> Safety and Scope Checks
-> Deterministic Intent Classification
-> Parameter Validation
-> Verified Intelligence Artifact Loading
-> Deterministic Query Router
-> Evidence and Financial Value Construction
-> Response Construction
-> API Response
-> Frontend Rendering

The assistant uses the existing backend intelligence artifact loader. It does not make HTTP requests to its own intelligence endpoints during assistant processing.

## 3. Architecture Components

### 3.1 Input Validation

Implemented responsibilities:
- Accept a question through POST /api/assistant/query.
- Enforce a maximum question length of 500 characters.
- Reject empty and non-string questions.
- Prevent invalid or excessively large questions from reaching retrieval logic.

### 3.2 Safety and Scope Checks

Implemented responsibilities:
- Check questions against a finite set of unsafe-request patterns.
- Reject selected requests involving secrets, system prompts, instruction overrides, and arbitrary code execution.
- Restrict processing to the approved five question intents.
- Return controlled responses for unsafe and unsupported requests.

Security limitation:
- Pattern-based checks are not comprehensive protection against every possible malicious or adversarial input.
- Retrieved source text is treated as evidence data, not executable instructions.
- Comprehensive security acceptance remains pending.

### 3.3 Deterministic Intent Classification

The assistant uses deterministic intent mapping rather than an LLM.

The five implemented intents are:
- `cost_centre_variance_comparison`
- `department_comparison`
- `expenditure_category_lookup`
- `finding_evidence_lookup`
- `monthly_insufficient_evidence_lookup`

Unknown or unsupported requests do not trigger unrestricted retrieval.

### 3.4 Parameter Validation

Implemented responsibilities:
- Validate required parameters before retrieval.
- Resolve approved department names using exact matching.
- Require exactly two approved departments for a department comparison.
- Resolve one approved expenditure category.
- Resolve finding evidence using an exact finding ID or approved cost-centre identifier.
- Return controlled missing-parameter, ambiguous, or out-of-scope responses.
- Do not invent or silently substitute parameter values.

### 3.5 Verified Intelligence Artifact Loading

The assistant uses the existing backend verified-artifact loader.

The loader checks the approved intelligence artifact bundle and its relevant identity, version, validation, reconciliation, sensitivity, weak-case, and timestamp information.

Unavailable or invalid verified artifacts are handled through controlled error responses.

The assistant does not independently read canonical CSV files or recalculate analytical results.

### 3.6 Deterministic Query Router

The router maps each approved intent to a predefined operation using the verified artifact bundle.

Implemented behaviour includes:
- Cost-centre comparison using approved cost-centre findings and existing priority ranks.
- Department comparison using exactly two approved department names.
- Expenditure-category lookup using an exact approved category.
- Finding evidence lookup using an exact finding ID or cost-centre identifier.
- Monthly insufficient-evidence lookup restricted to the three approved monthly result types and findings marked `insufficient_evidence`.
- Maximum 25 returned findings, with truncation disclosed when more results match.

Monthly findings are filtered from the verified artifact bundle in-process. The assistant does not make three separate HTTP requests to its own API.

### 3.7 Evidence Package

Responses preserve available approved information, including:
- Result identifier.
- Result type.
- Financial values.
- Source record identifiers.
- Canonical record identifiers.
- Reporting period.
- Independent source count.
- Quality status.
- Evidence excerpts.
- Relevant limitations.

Available metadata includes:
- `contract_version`
- `dataset_version`
- `method_version`
- Validation status and other approved metadata fields.

Evidence construction checks required fields and applies configured response limits.

### 3.8 Response Construction

The assistant returns structured responses containing:
- Unique answer identifier.
- Response status.
- Detected intent.
- Answer text.
- Evidence references.
- Approved financial key values.
- Metadata.
- Limitations.
- Up to three suggested follow-ups.

Financial values are copied from approved findings rather than independently recalculated.

The response limits are:
- Maximum question length: 500 characters.
- Maximum returned findings: 25.
- Maximum evidence references: 10.
- Maximum evidence excerpt length: 300 characters.
- Maximum suggested follow-ups: 3.

### 3.9 Grounding Controls

Implemented controls include:
- Use of verified intelligence artifacts.
- Validation of required evidence fields.
- Preservation of finding identifiers and source references.
- Preservation of approved financial values.
- Preservation of quality status, reporting periods, and limitations.
- Disclosure when result limits truncate matching findings.

These controls do not establish that every possible natural-language statement is independently verified by a comprehensive factual-claim validator. Further grounding and adversarial testing remain part of final acceptance.

## 4. API Integration

Implemented endpoint:
- `POST /api/assistant/query`

Request body:
- `question`: user question.

The endpoint returns a structured assistant response.

Existing intelligence endpoints remain available:
- `/api/intelligence/health`
- `/api/intelligence/metadata`
- `/api/intelligence/summary`
- `/api/intelligence/results`
- `/api/intelligence/results/{result_id}`

The assistant uses the backend verified-artifact loader rather than making internal HTTP calls to these endpoints.

## 5. Response Status Handling

| Status | Behaviour |
|---|---|
| `SUPPORTED` | Return an answer using approved findings. |
| `MISSING_PARAMETER` | Identify the missing required value. |
| `AMBIGUOUS` | Request a bounded clarification. |
| `OUT_OF_SCOPE` | Refuse unsupported requests. |
| `UNSAFE` | Refuse unsafe requests. |
| `UNAVAILABLE` | Handle unavailable verified evidence without inventing results. |

## 6. Frontend Integration

The Data Intelligence page includes an assistant interface.

Implemented frontend behaviour:
- Accept a question.
- Send a POST request to `/api/assistant/query`.
- Display loading and request-error states.
- Display response status and detected intent.
- Render answer text and approved financial values.
- Display evidence references and source identifiers.
- Display reporting periods, source counts, quality status, and limitations.
- Display suggested follow-ups.

The frontend renders backend-provided values; it does not independently calculate assistant findings.

The API base URL uses `NEXT_PUBLIC_API_URL` when configured and defaults to the local backend address for local development.

## 7. Security Boundaries and Deployment Limitations

- The assistant supports only the five approved question intents.
- Arbitrary SQL, user-supplied code, and unrestricted filesystem access are not supported.
- Response and evidence limits are enforced.
- Pattern-based unsafe-request detection is limited and is not comprehensive security protection.
- Authentication and authorization have not been verified as implemented.
- CORS is not authentication.
- Public deployment must use only data explicitly approved for public access.
- Public data exposure and the need for authentication must be resolved before final security acceptance.
- Persistent question logging and retention behaviour have not been fully audited.

## 8. Failure Handling

The assistant must:
- Handle unavailable or invalid verified artifacts safely.
- Return controlled responses for missing or unsupported findings.
- Stop processing unsafe or out-of-scope requests.
- Avoid exposing stack traces, internal paths, or secrets.
- Preserve approved source values and evidence references.
- Disclose result truncation and relevant evidence limitations.

## 9. Resource Limits

Implemented limits:
- Maximum question length: 500 characters.
- Maximum findings: 25.
- Maximum evidence references: 10.
- Maximum evidence excerpt length: 300 characters.
- Maximum follow-up suggestions: 3.
- LLM turns: Not applicable; no LLM is used.

Persistent assistant memory is not part of the implemented assistant response workflow. Logging and retention behaviour still require separate verification.

## 10. Verification Status

Completed checks include:
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
- Evidence and limitation rendering checks.

Remaining checks include:
- Full public Render deployment verification.
- Authentication and public-data-boundary decision.
- Additional security and adversarial testing.
- Mobile and accessibility testing.
- Full regression and final evidence capture.
- Reviewer acceptance.

## 11. Implementation and Review Status

The deterministic assistant, FastAPI endpoint, and Data Intelligence frontend integration have been implemented.

The selected automated, API, and browser checks have passed.

This does not constitute full security acceptance, complete deployment verification, or reviewer approval.

**Overall architecture status: IMPLEMENTED - SELECTED VERIFICATION PASSED - FINAL ACCEPTANCE PENDING.**

Reviewer approval has not yet been obtained.
