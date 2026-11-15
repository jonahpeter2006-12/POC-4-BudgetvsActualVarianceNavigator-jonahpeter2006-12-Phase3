# Grounded Data Assistant - User Acceptance Testing

## Project
- PoC: 4 - Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 - Post #5
- Component: Grounded Natural-Language Data Assistant
- Mode: A - Deterministic guided assistant
- LLM: Not required

## 1. Purpose

Record the user acceptance testing performed for the grounded data assistant.

Testing verifies that supported questions receive deterministic answers based on approved Data Intelligence findings, with evidence references and limitations preserved.

## 2. Preconditions and Environment

- Post #4 Data Intelligence integration is available locally.
- Approved intelligence output files are loaded and verified by the backend.
- The assistant implementation and API route are available.
- Test data is synthetic.
- The assistant uses the approved question catalog and deterministic routing.
- Local FastAPI backend: http://127.0.0.1:8000
- Local frontend: http://localhost:3000/data-intelligence
- Execution date: 2026-11-08

Public deployment and public-data security approval have not been confirmed as part of this local UAT execution.

## 3. Functional UAT

| Test ID | User action | Actual result | Status |
|---|---|---|---|
| UAT-01 | Compare cost centres | Six approved cost-centre findings returned with financial values and evidence | PASS |
| UAT-02 | Compare Engineering and Sales departments | Exactly two approved department findings returned with supporting evidence | PASS |
| UAT-03 | Compare Cloud Infrastructure expenditure category | Correct category finding and supporting evidence returned | PASS |
| UAT-04 | Show evidence for CC-101 | Exact finding ID, financial values, source IDs, canonical IDs and limitations returned | PASS |
| UAT-05 | Show monthly findings with insufficient evidence | Descriptive monthly findings returned; 25 of 48 matches shown with truncation disclosed | PASS |
| UAT-06 | Submit a question without a required parameter | Missing-parameter response returned in API tests | PASS |
| UAT-07 | Compare three departments | AMBIGUOUS response requested exactly two approved department names | PASS |
| UAT-08 | Predict next year's revenue | OUT_OF_SCOPE response; no prediction generated | PASS |
| UAT-09 | Request an unavailable finding | Unknown finding ID handled as a controlled OUT_OF_SCOPE response in backend testing | PASS |

The functional results above reflect the executed local API and browser checks. They do not imply that every possible input combination has been tested.

## 4. Grounding UAT

Verified during the supported browser tests:

- Financial values were rendered from the assistant API response.
- Cost-centre and department findings matched the approved intelligence results.
- Finding IDs were preserved.
- Source record IDs and canonical record IDs were displayed.
- Reporting periods were preserved.
- Independent source counts and quality statuses were displayed.
- Evidence excerpts and limitations were displayed.
- Monthly findings with insufficient evidence were clearly identified.
- The monthly response disclosed that 25 of 48 matching findings were returned.
- Response metadata included the approved validation information.

**Acceptance for tested cases:** The inspected supported responses preserved their returned financial values and evidence details.

A separate exhaustive comparison of every response field against every approved artifact has not been claimed.

## 5. Safety UAT

| Test | Actual result | Status |
|---|---|---|
| Request hidden system prompt | UNSAFE; request rejected | PASS |
| Request unsupported future prediction | OUT_OF_SCOPE | PASS |
| Submit a question longer than 500 characters | OUT_OF_SCOPE | PASS |
| Submit an empty question | MISSING_PARAMETER | PASS |
| Request an unknown finding ID | Controlled OUT_OF_SCOPE response | PASS |
| Request API keys or environment variables | API key request returned UNSAFE; environment-variable request returned OUT_OF_SCOPE | PASS |
| Attempt to change approved findings or rankings | OUT_OF_SCOPE; no modification performed | PASS |
| Request all canonical records | OUT_OF_SCOPE; bulk records not returned | PASS |
| Request arbitrary SQL or Python execution | Both SQL and Python execution requests returned UNSAFE | PASS |
| Include malicious instructions in source evidence | Isolated in-memory test confirmed malicious-looking text remains an ordinary evidence excerpt; full API/source-artifact injection testing remains outstanding | PARTIAL |
| Request an unsupported risk score | OUT_OF_SCOPE; no unsupported score generated | PASS |

No claim is made that the complete safety checklist has passed.

## 6. Usability UAT

Verified:
- Assistant explains its evidence-based purpose.
- The question input and Ask assistant action work in the desktop browser.
- Supported responses are understandable.
- Status and intent are displayed.
- Evidence references and limitations are visible.
- Mobile layout manually verified at 390 × 844 pixels, including assistant input, dashboard cards, findings, filters, evidence details, methodology and footer.
- Unsupported and unsafe requests receive clear responses.
- Suggested follow-up questions are available.

- Keyboard-only navigation verified, including visible focus and Tab navigation.
- Windows Narrator screen-reader announcements checked.
- Assistant question input accessibility label checked.

## 7. Regression and Build UAT

Verified:
- FastAPI application imports successfully.
- POST /api/assistant/query is registered.
- Existing intelligence artifacts are loaded through the verified backend loader.
- Assistant API requests work through the local FastAPI server.
- Data Intelligence page passes its targeted ESLint check.
- Frontend production build completes successfully.
- Data Intelligence page and assistant panel render in the local browser.
- Existing intelligence findings, filters and evidence content remain visible during the tested assistant interactions.
- Operational dashboard manually checked and confirmed working.

Additional regression work pending:
- Dedicated mobile regression.
- Public Render deployment end-to-end verification.
- Full existing Selenium regression scripts.

The repository-wide frontend lint command reports existing issues in frontend/src/app/page.tsx. These were not introduced or changed as part of the assistant page integration.

## 8. Automated Test Execution Record

| Item | Result |
|---|---|
| Execution date | 2026-11-09 |
| Environment | Local Windows development environment |
| API test file | tests/test_assistant_api.py |
| Pytest result | 15 passed, 0 failed |
| Python compilation | Passed |
| Backend edge-case checks | Passed |
| Targeted Data Intelligence page ESLint | Passed |
| Frontend production build | Passed |
| Browser functional checks | Passed for the cases listed above |
| Pytest warning | One non-blocking AnyIO plugin deprecation warning |

The pytest result applies to the assistant API test file; it is not a count of all manual UAT checks.

## 9. Required Evidence

Retain the following evidence:
- Assistant API test file and test output.
- Python compilation result.
- Browser results for supported question types.
- Browser results for unsafe and unsupported requests.
- Three-department ambiguity result.
- Frontend production build result.
- Targeted ESLint result.
- Grounding and evidence details displayed by the assistant.
- Outstanding safety and regression checks.

Dedicated screenshots and any additional reviewer-requested evidence should be retained before handover.

## 10. Acceptance Criteria

Final UAT approval requires:
- Required functional tests to pass.
- Numerical and evidence fidelity to be confirmed.
- Critical safety tests to pass.
- Version and limitation fidelity to be confirmed.
- Existing dashboard and intelligence functionality to have no regression.
- Mobile layout, keyboard navigation, screen-reader and accessibility-label checks completed for tested scenarios.
- Required evidence to be retained.
- No unresolved critical issue.
- Reviewer approval.

## 11. Current Status

**Implementation:** Completed for the local Mode A assistant integration.

**Executed tests:** The recorded API tests, supported browser cases, unsafe/unsupported cases and three-department ambiguity test passed.

**Remaining work:**
- Complete the outstanding safety checks.
- Dedicated mobile regression remains to be completed.
- Complete the remaining regression checks.
- Verify public deployment and resolve the public API security/data-boundary approval requirement before treating the public service as ready.
- Retain the required evidence.
- Obtain reviewer approval.

**Overall UAT status: PARTIALLY EXECUTED - FINAL ACCEPTANCE PENDING.**

Reviewer approval has not yet been obtained.
