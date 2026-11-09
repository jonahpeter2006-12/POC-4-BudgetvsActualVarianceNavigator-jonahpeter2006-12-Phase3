# Assistant Grounding Validation

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5
- Component: Grounded Natural-Language Data Assistant
- Mode: A - Deterministic guided assistant
- LLM: Not used
- Execution record date: 2026-11-08

## 1. Purpose

Verify that supported assistant answers use approved intelligence findings, preserve financial values and evidence, and communicate the documented limitations.

This document separates completed verification from outstanding acceptance requirements. A selected test passing does not establish 100% fidelity or complete security acceptance.

## 2. Implemented Validation Principles

The implemented assistant:

1. Supports only the five intents in `SUPPORTED_QUESTION_CATALOG.md`.
2. Loads approved intelligence artifacts through the existing in-process verified-artifact loader.
3. Does not make HTTP requests to its own intelligence endpoints during assistant processing.
4. Preserves approved finding identifiers and financial values.
5. Includes evidence references and relevant finding metadata.
6. Preserves available quality and limitation information.
7. Includes approved contract, dataset and method version metadata.
8. Applies input validation and selected unsafe-request checks.
9. Does not use an LLM to generate financial findings.

The loader checks approved artifact identity, versions, validation and reconciliation status, sensitivity, weak cases and timestamps. This does not independently prove every response claim.

## 3. Numerical Fidelity

### Completed selected checks

- Cost-centre comparison displayed approved budget, actual, variance and percentage values.
- Engineering and Sales comparison displayed the approved department values.
- Cloud Infrastructure lookup displayed the approved category values.
- CC-101 evidence lookup displayed the approved finding values.
- Monthly insufficient-evidence lookup displayed approved returned finding values.
- The assistant response renders backend-provided values; the frontend does not independently calculate replacement financial values.

### Still pending

- Exhaustive comparison of every displayed numerical field against every corresponding approved finding.
- Independent 100% numerical fidelity assessment across all supported responses.
- Exhaustive priority-rank, committed-total and forecast-total fidelity checks.

Acceptance target remains 100%. Selected successful examples do not establish that target.

## 4. Evidence Coverage

### Completed selected checks

Browser tests verified evidence details for:
- Cost-centre comparison.
- Engineering and Sales department comparison.
- Cloud Infrastructure category lookup.
- Exact CC-101 finding lookup.
- Monthly insufficient-evidence lookup.

Displayed evidence included relevant result identifiers, source record IDs, canonical record IDs, reporting periods, independent source counts, quality status and limitations.

Backend evidence construction validates required evidence fields and applies response limits.

### Still pending

- Exhaustive verification of every evidence reference against its original approved finding.
- 100% evidence coverage across every supported result.
- Independent verification of every excerpt and limitation.

Acceptance target remains 100% evidence coverage.

## 5. Limitation Fidelity

The assistant and project documentation retain these important dataset limitations:

- The dataset contains 18 independent synthetic source observations.
- The 72 canonical rows represent four derived financial measures per observation, not 72 independent transactions.
- Monthly findings with fewer than three independent sources are descriptive and insufficient for stronger conclusions.
- Forecast figures are illustrative, not predictive.
- Findings do not support population-level conclusions.
- One leave-one-source-observation-out sensitivity analysis is not a statistical robustness test.

Selected browser tests displayed limitations for the tested findings, including the monthly insufficient-evidence response.

Exhaustive 100% limitation fidelity remains pending.

## 6. Functional Test Execution

| Test ID | Test | Execution status |
|---|---|---|
| GF-01 | Cost-centre comparison | PASS - browser tested |
| GF-02 | Exactly two department comparison | PASS - browser tested |
| GF-03 | Expenditure-category lookup | PASS - browser tested |
| GF-04 | Exact finding evidence lookup | PASS - browser tested |
| GF-05 | Monthly insufficient-evidence lookup | PASS - browser tested |
| GF-06 | Missing required parameter | PASS - API tested |
| GF-07 | Ambiguous department request | PASS - three-department API and browser tests |
| GF-08 | Unsupported prediction request | PASS - API and browser tested |
| GF-09 | Unavailable evidence/artifact handling | PASS - simulated missing/invalid and stale artifact failures, plus an evidence-processing ValueError, all returned controlled HTTP 503 responses |

Additional completed checks:
- Empty question returned MISSING_PARAMETER.
- Non-string question returned MISSING_PARAMETER.
- Question exceeding 500 characters returned OUT_OF_SCOPE.
- Unknown finding ID returned OUT_OF_SCOPE.
- Multiple category names returned AMBIGUOUS.
- Unknown category returned MISSING_PARAMETER.

## 7. Safety Test Execution

| Test ID | Test | Execution status |
|---|---|---|
| SF-01 | Ignore previous instructions | PENDING |
| SF-02 | Request system prompt or secrets | PARTIAL PASS - system-prompt request tested |
| SF-03 | Change an approved score | PENDING |
| SF-04 | Request unrestricted records | PENDING |
| SF-05 | Submit arbitrary SQL or Python | PENDING - comprehensive execution checks |
| SF-06 | Invalid finding ID | PASS - controlled OUT_OF_SCOPE response tested |
| SF-07 | Instructions embedded in evidence | PENDING |
| SF-08 | Unsupported risk or anomaly scores | PARTIAL - unsupported prediction tested; exhaustive risk/anomaly cases pending |
| SF-09 | Excessively long question | PASS - 501-character question tested |

The unsafe-request detector uses a finite set of regular-expression patterns. It is a limited input control, not comprehensive protection against prompt injection or every malicious request.

## 8. Version and API Validation

### Completed

- FastAPI application import passed.
- POST `/api/assistant/query` was registered.
- Swagger displayed the assistant request schema.
- Local HTTP API request returned a supported response.
- Async HTTPX ASGI tests passed.
- Response metadata includes approved version fields.
- The verified-artifact loader checks artifact identity and version information.

### Still pending

- Independent comparison of every response version against the approved metadata endpoint.
- Additional artifact failure scenarios beyond the simulated missing/invalid and stale cases.
- Exhaustive API error checks for secrets, internal paths and stack traces.
- Full verification of response limits and error behaviour in all cases.

The assistant API tests recorded 15 passed and 0 failed. Simulated missing/invalid and stale artifact tests, plus an evidence-processing ValueError test, returned the expected controlled HTTP 503 responses. The run produced one nonblocking AnyIO plugin deprecation warning.

## 9. Regression Validation

### Completed selected checks

- `python -m py_compile` passed for the assistant, API and assistant API test files.
- `python -m pytest .\tests\test_assistant_api.py -v`: 15 passed, 0 failed.
- Targeted ESLint check for `frontend/src/app/data-intelligence/page.tsx` passed.
- Frontend `npm run build` passed.
- The Data Intelligence page loaded locally.
- The assistant panel rendered supported answers, evidence and limitations.
- Existing Data Intelligence findings and dashboard content loaded during browser tests.

### Still pending

- Full operational dashboard regression.
- Existing Post #4 Selenium regression.
- Public Render deployment end-to-end verification.
- Mobile layout and accessibility checks.
- Final full regression after all remaining changes.

The repository-wide frontend lint command reported 12 issues in the existing operational dashboard `frontend/src/app/page.tsx`. The targeted Data Intelligence page lint passed. These results must not be represented as a clean repository-wide lint run.

## 10. Acceptance Criteria

The final acceptance targets remain:

- 100% numerical fidelity.
- 100% evidence coverage for supported answers.
- 100% limitation fidelity.
- Correct handling of critical unsupported requests.
- Adequate resistance to critical instruction-injection attempts.
- Version fidelity.
- No regression in approved dashboard and intelligence functionality.

Selected tests passing does not satisfy every acceptance target. Any unresolved critical failure blocks approval.

## 11. Execution Evidence

Execution date: 2026-11-08.

Recorded evidence:
- Assistant API automated tests: 15 passed, 0 failed.
- Python compilation: passed for the tested assistant and API files.
- Targeted Data Intelligence page ESLint: passed.
- Frontend production build: passed.
- Five supported question types: browser tested successfully.
- Unsupported prediction: browser tested successfully.
- System-prompt request: browser tested successfully as UNSAFE.
- Three-department ambiguity: browser tested successfully as AMBIGUOUS.
- Additional missing-parameter, invalid-input, unknown-entity and ambiguity cases: API tested.

Remaining evidence:
- Exhaustive numerical and evidence comparison.
- Full safety test matrix.
- Version fidelity and unavailable-artifact tests.
- Full dashboard and Post #4 regression.
- Mobile and accessibility checks.
- Public deployment verification.
- Final reviewer acceptance.

## 12. Current Status

Grounding validation implementation and selected functional verification are complete.

Full numerical fidelity, exhaustive evidence coverage, comprehensive safety validation, version fidelity and full regression remain pending.

Overall grounding status: IMPLEMENTED - SELECTED VERIFICATION PASSED - FULL ACCEPTANCE PENDING.

Reviewer approval has not yet been obtained.
