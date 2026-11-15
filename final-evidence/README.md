# Phase 3 Final Evidence Package

## Purpose

This folder contains selected evidence records for the PoC-4 Phase 3 Post #6 release review.

## Analytical evidence

The `analytical/` directory contains copies of the original JSON outputs from `data-science/outputs/`.

These records preserve their original generated timestamps and validation results. The included analytical records have generated timestamps spanning 2026-11-04 through 2026-11-07.

The combined validation record reports:
- 1,325 checks passed
- 0 failed checks
- 0 warnings
- 1,230 analytical checks
- 95 reconciliation checks

The sensitivity assessment is reported separately and is not included in the combined validation total.

## Browser automation evidence

`browser-automation/post6-selenium-attempt-2026-11-14.json` records the Post #6 Selenium attempt against the current Phase 3 Render URLs.

The attempt did not reach browser startup because Selenium could not obtain ChromeDriver. Windows Application Control blocked Selenium Manager. The recorded result is a blocked execution attempt, not a passing browser test.

## Automated test report

`FINAL_AUTOMATED_TEST_REPORT.md` records the verified local Python tests, Gemini tests, Python compilation, frontend build, targeted lint, Docker build, local runtime checks, and their limitations.

## Evidence limitations

- No fresh Post #6 Selenium browser screenshot is included.
- Historical Post #4 screenshots and test results are not represented as Post #6 evidence.
- Gemini Mode B was validated locally but is not deployed or configured on the public Render service.
- A clean-clone validation has not been executed.
- Fresh deployed browser UAT remains outstanding.
- This evidence package does not establish final Phase 3 certification or reviewer approval.
