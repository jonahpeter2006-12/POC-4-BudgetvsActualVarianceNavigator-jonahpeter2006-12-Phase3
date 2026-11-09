# Assistant Safety and Scope

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5
- Component: Grounded Natural-Language Data Assistant
- Mode: A - Deterministic guided assistant
- LLM: Not required

## 1. Purpose

Define the permitted scope, implemented safety controls, and remaining security requirements for the grounded data assistant.

The assistant provides answers only from approved Data Intelligence findings. It does not generate new analytical results or access unrestricted project data.

## 2. Approved Scope

The assistant supports five approved question categories:

1. Cost-centre variance comparisons.
2. Department variance comparisons.
3. Expenditure-category comparisons.
4. Explanations of individual approved findings and their evidence.
5. Monthly findings with insufficient evidence, clearly labelled as descriptive.

Question handling follows `SUPPORTED_QUESTION_CATALOG.md`.

The implementation uses deterministic intent classification and approved entity matching. An external LLM is not required.

## 3. Out-of-Scope Requests

The assistant must not provide:

- Predictions or future financial outcomes.
- New forecasts or predictive model outputs.
- New anomaly detection.
- New risk scores or risk rankings.
- New scenario or sensitivity calculations.
- Unsupported recommendations or causal explanations.
- Population-level conclusions.
- Arbitrary SQL, Python, shell commands, or database queries.
- Unrestricted canonical dataset exports.
- Information not present in approved findings.

Unsupported questions receive an `OUT_OF_SCOPE` response.

## 4. Input Safety

Implemented controls in `backend/assistant.py`:

- Maximum question length: 500 characters.
- Empty and non-string questions are rejected.
- Input is normalized for matching.
- Approved intents and entity parameters are resolved deterministically.
- Exact phrase matching is used for approved entities.
- User text is not executed as code.

Executed tests include empty input, non-string input, and an excessively long question.

## 5. Instruction-Injection Protection

The implementation includes regular-expression checks for known unsafe request patterns, including:

- Attempts to ignore or override instructions.
- Requests to reveal secrets, API keys, tokens, or system prompts.
- Requests to execute SQL, Python, or shell commands.
- Common SQL manipulation patterns.

The tested request to reveal the system prompt returned `UNSAFE`.

**Security limitation:** These patterns are a limited detection mechanism. They are not comprehensive protection against every possible prompt-injection or malicious input. The assistant does not use an LLM, which reduces exposure to LLM-specific prompt injection, but does not eliminate general application security risks.

The following safety cases still require dedicated testing:

- Requests for environment variables or credentials.
- Attempts to alter approved findings or rankings.
- Requests to retrieve unrestricted canonical records.
- Arbitrary SQL or code execution requests.
- Malicious instructions embedded in evidence or source data.
- Unsupported risk-score requests.

## 6. Data Access Boundary

The assistant obtains its approved findings from the verified intelligence artifact bundle loaded by the existing backend artifact loader.

The inspected implementation:

- Uses approved result records for deterministic routing.
- Copies approved financial values without recalculating them.
- Requires supporting evidence fields before constructing evidence references.
- Preserves source record IDs and canonical record IDs.
- Preserves reporting periods, independent-source counts, quality statuses, and limitations.
- Does not directly read canonical CSV files in `backend/assistant.py`.
- Does not execute arbitrary database queries or user-supplied code.

The assistant does not provide unrestricted filesystem, database, or URL access.

The artifact loader and API integration must continue to enforce the approved data boundary.

## 7. Authentication and Public Deployment Limitation

The inspected backend does not currently show authentication or authorization middleware protecting the assistant endpoint.

CORS configuration is not authentication. A public API may be accessed by clients other than the intended frontend.

Therefore:

- Do not claim authenticated-user protection.
- Do not claim CORS provides access control.
- Do not expose confidential or sensitive information through the assistant.
- Confirm the permitted public-data boundary before public deployment.
- Obtain reviewer acceptance of this limitation or implement and verify an appropriate access-control solution if required.

Only the inspected source sample was checked for obvious personal identifiers. This does not establish that every repository file or deployed response is free of sensitive information.

**Status: Unresolved deployment concern.**

## 8. Response and Evidence Limits

Implemented constants and response controls:

| Control | Implemented limit |
|---|---:|
| Maximum question length | 500 characters |
| Maximum returned findings | 25 |
| Maximum evidence references | 10 |
| Maximum evidence excerpt | 300 characters |
| Maximum suggested follow-ups | 3 |

Additional implemented behaviour:

- Monthly findings are restricted to the three approved monthly result types.
- Monthly results are filtered to `insufficient_evidence`.
- Truncation is disclosed when more than 25 findings match.
- Response metadata preserves intelligence version and validation information.
- Evidence and financial values are taken from approved findings.

Persistent conversation memory and logging-retention behaviour have not been independently verified as part of this inspection.

## 9. Error Handling

| Condition | Required status | Verification |
|---|---|---|
| Approved question with valid evidence | `SUPPORTED` | Tested |
| Required parameter missing | `MISSING_PARAMETER` | Tested |
| Multiple possible matches | `AMBIGUOUS` | Tested |
| Unsupported question | `OUT_OF_SCOPE` | Tested |
| Unsafe request | `UNSAFE` | Tested for selected patterns |
| Data or evidence unavailable | `UNAVAILABLE` | Requires dedicated verification |

Errors must not expose internal paths, secrets, stack traces, or sensitive configuration.

## 10. Logging and Privacy

Requirements:

- Do not log secrets or credentials.
- Avoid storing full user questions unless necessary and approved.
- Do not retain sensitive conversation information as persistent memory.
- Do not send unrestricted canonical records to an external language model.
- Keep operational logs limited to non-sensitive diagnostic information.

Logging, retention, and deployment privacy behaviour have not been fully audited.

## 11. Implementation and Review Status

**Implementation:** The local Mode A assistant has been implemented.

**Verified implementation controls:**
- Five approved deterministic intents.
- Exact approved entity matching.
- Exactly two departments required for department comparisons.
- Exact category and finding resolution.
- Monthly insufficient-evidence filtering.
- Financial-value copying from approved findings.
- Evidence-field validation and evidence excerpt truncation.
- Response and result limits.
- Metadata and limitation preservation.

**Executed tests:**
- Selected supported question types.
- Missing and invalid question inputs.
- Three-department ambiguity.
- Selected unsafe and unsupported requests.
- Monthly result truncation.
- API and browser integration.

**Remaining work:**
- Complete the outstanding safety test cases.
- Verify unavailable-evidence handling.
- Review logging and privacy behaviour.
- Complete mobile and accessibility checks.
- Complete remaining regression checks.
- Resolve public deployment data-boundary and authentication requirements.
- Retain required evidence.
- Obtain reviewer approval.

**Overall safety status: IMPLEMENTED CONTROLS VERIFIED FOR SELECTED CASES - FULL SECURITY ACCEPTANCE PENDING.**

Reviewer approval has not yet been obtained.
