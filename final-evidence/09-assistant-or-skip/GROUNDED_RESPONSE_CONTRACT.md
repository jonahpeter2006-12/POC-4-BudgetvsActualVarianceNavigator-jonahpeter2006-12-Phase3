# Grounded Response Contract

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5
- Component: Grounded Natural-Language Data Assistant
- Mode: A - Deterministic guided assistant
- LLM: Not required

## 1. Purpose

Define the implemented response structure for the deterministic assistant.

Supported answers use approved Data Intelligence findings loaded through the existing verified intelligence artifact loader. The assistant does not make HTTP requests to its own Data Intelligence endpoints during processing.

Selected API and browser tests have passed. Full acceptance remains pending.

## 2. Required Response Fields

The implemented response contains:

- `answer_id`: Unique response identifier.
- `status`: Response status.
- `intent`: Resolved supported intent, or null when no intent is resolved.
- `answer`: Plain-language response.
- `evidence_references`: Grouped finding and source evidence references.
- `key_values`: Relevant financial values copied from approved findings.
- `metadata`: Available project, track, contract, dataset, method, generation, result-count, and validation metadata.
- `limitation`: Applicable evidence or interpretation limitations.
- `suggested_follow_ups`: Supported follow-up questions.

The metadata object preserves available version fields, including `contract_version`, `dataset_version`, and `method_version`. These values are passed through from the verified artifact metadata; exhaustive independent version-fidelity testing remains pending.

## 3. Allowed Status Values

- `SUPPORTED`: An approved question was answered using available findings.
- `MISSING_PARAMETER`: A required entity or parameter was not provided or could not be resolved.
- `AMBIGUOUS`: The request contains an ambiguous entity selection, such as more than two departments for the two-department comparison.
- `OUT_OF_SCOPE`: The question is not covered by the approved question catalog.
- `UNSAFE`: The request matches a detected unsafe pattern.
- `UNAVAILABLE`: Reserved for unavailable approved intelligence evidence or artifacts. Full unavailable-artifact behavior still requires verification.

## 4. Supported Intents

The implemented assistant supports five deterministic question types:

1. Cost-centre variance comparison.
2. Comparison of exactly two approved departments.
3. Exact expenditure-category lookup.
4. Evidence lookup by exact finding ID or cost-centre identifier.
5. Monthly insufficient-evidence lookup across the three approved monthly result types.

The assistant does not provide arbitrary questions, forecasts, predictions, risk scores, anomaly scores, or unrestricted data exports.

## 5. Grounding Rules

1. Use the verified approved intelligence artifact bundle.
2. Preserve exact finding IDs and source references.
3. Copy approved numerical values rather than independently calculating financial results.
4. Preserve available quality status and limitation text.
5. Keep overall comparison findings separate from monthly findings.
6. Do not combine rankings from different comparison dimensions.
7. Keep budget, actual, committed, and forecast values distinct.
8. Identify forecast values as illustrative, not predictive.
9. Do not present insufficient-evidence findings as confirmed conclusions.

These are implementation rules. Exhaustive verification of every claim and every returned value remains pending.

## 6. Evidence Requirements

Evidence references preserve available fields including:

- `result_id`.
- `result_type`.
- Source record IDs.
- Canonical record IDs.
- Reporting period.
- Independent source count.
- Quality status.
- Limitation text.
- Evidence excerpt.

The implementation validates required evidence structure and limits excerpt length. It does not establish that every possible factual sentence has passed an independent claim-by-claim audit.

If required approved artifacts are unavailable or fail verified-loader checks, the API uses controlled unavailable-service handling. Exhaustive unavailable-evidence tests remain pending.

## 7. Numerical Fidelity

The assistant copies available approved finding values, including:

- Budget amounts.
- Actual amounts.
- Variance amounts.
- Variance percentages.
- Committed amounts.
- Forecast amounts.
- Priority ranks.
- Independent source counts.

The response builder does not independently recalculate these financial values.

Selected browser tests verified displayed values against their approved findings. An exhaustive 100% numerical fidelity audit across all supported responses has not yet been completed.

## 8. Limitation Fidelity

Responses must preserve applicable project limitations:

- The dataset contains 18 independent synthetic source observations.
- The 72 canonical rows represent four derived financial measures per observation, not 72 independent transactions.
- Monthly findings with fewer than three independent sources are descriptive and have insufficient evidence for supported conclusions.
- Forecast values are illustrative and are not generated by a predictive model.
- Findings do not support population-level conclusions.
- The available leave-one-source-observation-out sensitivity analysis is not a statistical robustness test.

Selected browser tests displayed relevant evidence limitations. Exhaustive limitation-fidelity verification remains pending.

## 9. Response Limits

The implemented assistant enforces these limits:

- Maximum question length: 500 characters.
- Maximum returned findings/key values: 25.
- Maximum evidence references: 10.
- Maximum evidence excerpt length: 300 characters.
- Maximum suggested follow-ups: 3.

When a result set exceeds the finding limit, the response metadata indicates truncation and preserves the matched count where available.

## 10. Suggested Follow-ups

Suggested follow-ups are restricted to the approved question catalog.

- Maximum suggested follow-ups: 3.
- Do not suggest unsupported predictions, risk scores, or anomaly detection.
- Do not suggest access to unrestricted canonical data.

## 11. Response Safety and Security Limitations

- The assistant does not execute SQL, Python, shell commands, or arbitrary user-provided code.
- A finite unsafe-pattern detector rejects selected unsafe requests.
- The detector is not comprehensive protection against every prompt-injection or instruction-manipulation attempt.
- Source evidence is treated as data, not as instructions to execute.
- No comprehensive audit of all source-evidence injection cases has been completed.
- Authentication and authorization have not been verified as implemented.
- CORS is not authentication. Public deployment requires an approved data-access boundary or appropriate authentication.
- Logging, retention, and persistent conversation-data behavior have not been independently audited.

## 12. Validation Requirements

Final acceptance requires verification of:

- Numerical fidelity against approved findings.
- Evidence coverage and exact identifiers.
- Quality-status preservation.
- Limitation fidelity.
- Version metadata fidelity.
- Correct handling of unsupported, ambiguous, missing-parameter, unsafe, and unavailable requests.
- No regression in approved dashboard and intelligence functionality.

Required acceptance targets remain:

- 100% numerical fidelity.
- 100% evidence coverage for supported answers.
- 100% limitation fidelity.
- 100% correct handling of critical unsupported requests.
- Adequate resistance to critical instruction-injection attempts.
- 100% version fidelity.
- No regression in approved functionality.

Selected tests passing does not establish that every acceptance target has passed.

## 13. Selected Execution Evidence

Execution date: 2026-11-08.

Recorded results:

- Assistant API automated tests: 15 passed, 0 failed.
- Python compilation for tested assistant and API files: passed.
- Targeted ESLint check for the Data Intelligence page: passed.
- Frontend production build: passed.
- All five supported question types: browser tested successfully.
- Unsupported prediction request: browser tested successfully as `OUT_OF_SCOPE`.
- System-prompt request: browser tested successfully as `UNSAFE`.
- Three-department comparison: browser tested successfully as `AMBIGUOUS`.
- Additional missing-parameter, invalid-input, unknown-entity, and ambiguity cases: API tested.

The above are selected execution results, not exhaustive acceptance evidence.

## 14. Remaining Verification

- Exhaustive numerical fidelity and evidence coverage.
- Full limitation-fidelity assessment.
- Full safety and instruction-injection test matrix.
- Version metadata fidelity.
- Unavailable-artifact and unavailable-evidence behavior.
- Full operational dashboard and Post #4 regression.
- Public Render deployment verification.
- Mobile and accessibility checks.
- Authentication or documented approval of the public data-access boundary.
- Logging and retention review.
- Final reviewer acceptance.

## 15. Implementation Status

The response contract and deterministic assistant response structure are implemented.

Selected API, browser, build, compilation, and targeted lint checks have passed.

Overall response contract status: IMPLEMENTED - SELECTED VERIFICATION PASSED - FULL ACCEPTANCE PENDING.

Reviewer approval has not yet been obtained.
