# FINAL AUTOMATED TEST REPORT

## 1. Purpose

This report records the Post #6 automated validation evidence available for the PoC-4 Phase 3 release review. It distinguishes successful local checks from browser automation that was blocked by the Windows execution environment.

## 2. Complete Python Test Suite

Command:

`python -m pytest -v`

Verified result on 2026-11-14:
- Tests collected: 24.
- Tests passed: 24.
- Tests failed: 0.
- Non-blocking warnings: 1.
- Overall result: PASS.

The warning concerns an AnyIO pytest plugin deprecation involving an internal pytest API. It did not cause a test failure.

The suite includes 16 assistant API tests and 8 Gemini explanation tests.

## 3. Dedicated Gemini Explanation Tests

Command:

`python -m pytest tests/test_gemini_explainer.py -v`

Verified result:
- Tests passed: 8.
- Tests failed: 0.
- Non-blocking warnings: 1.

Coverage includes missing API key behavior, accepted explanations, unsupported numeric claims, contradictory budget-direction claims, provider failure fallback, and exclusion of unsupported questions from Gemini explanation.

Gemini Mode B is an optional explanation layer. Deterministic assistant results and evidence remain authoritative.

## 4. Python Compilation

Command:

`python -m compileall -q backend tests`

The command completed without reported compilation errors.

## 5. Frontend Build and Lint

Production build command:

`npm --prefix frontend run build`

The Next.js 16.4.3 production build completed successfully. TypeScript validation and static page generation completed.

The targeted ESLint check for `frontend/src/app/data-intelligence/page.tsx` passed.

Repository-wide frontend lint is not recorded as passing. An earlier repository-wide run reported 12 issues in the existing operational dashboard file `frontend/src/app/page.tsx`. These issues were not broadly refactored as part of Post #6.

## 6. Docker Build and Local Runtime

The Post #6 backend Docker image was built and its module import was verified.

The local test container was used to check:
- `/api/health` returned a healthy response.
- `/api/intelligence/health` reported readiness and 64 findings.
- `/api/intelligence/summary` reported 1,325 passed checks, 0 failures, and 0 warnings.
- A representative supported assistant question returned grounded CC-101 evidence.
- An unsupported prediction and fraud-risk question returned `OUT_OF_SCOPE` without unsupported financial conclusions.

The local container was tested without a Gemini API key, confirming the deterministic fallback state.

These checks establish local implementation evidence, not proof of a fresh deployed browser journey.

## 7. Analytical and Reconciliation Validation

The combined analytical and reconciliation validation reported:
- Total checks: 1,325.
- Passed: 1,325.
- Failed: 0.
- Warnings: 0.
- Analytical checks: 1,230.
- Reconciliation checks: 95.

The sensitivity assessment is reported separately and is not included in the combined validation total.

## 8. Browser Automation

A Post #6 Selenium execution was attempted using:

`python tests/test_live_application.py`

The attempt did not reach browser startup. Windows Application Control prevented Selenium Manager from launching `selenium-manager.exe`, and no locally available ChromeDriver was found.

Result: BLOCKED — browser automation did not reach the application.

The recorded Selenium attempt has 0 passed and 1 failed execution-level test. It is evidence of an environment-blocked attempt, not a passing browser test. Historical Post #4 Selenium results remain historical evidence only.

## 9. Environment and Coverage Limitations

- Local Python tests, compilation, frontend production build, targeted lint, Docker build, and recorded local runtime checks passed.
- Gemini Mode B was tested locally but is not deployed or configured on the public Render service.
- Fresh Post #6 deployed browser regression and UAT remain outstanding.
- A clean-clone validation has not been executed.
- Repository-wide frontend lint has documented existing issues.
- These checks do not establish exhaustive security, accessibility, or end-to-end browser coverage.

## 10. Conclusion

**PASS WITH DOCUMENTED LIMITATIONS** for the executed local Python tests, Gemini tests, compilation, frontend build, targeted lint, Docker build, and recorded local runtime checks.

**BLOCKED** for fresh Post #6 Selenium browser automation because Windows Application Control prevented Selenium Manager from starting.

This report does not claim complete release validation or final Phase 3 certification. Certification remains blocked pending outstanding release gates and reviewer approval.
