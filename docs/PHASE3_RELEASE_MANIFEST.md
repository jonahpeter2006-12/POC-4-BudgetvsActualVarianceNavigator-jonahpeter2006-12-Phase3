# PHASE 3 RELEASE MANIFEST

## 1. Manifest Status

**STATUS: DRAFT — NOT CERTIFIED.**

This manifest records the intended Phase 3 release contents and outstanding certification requirements. It does not identify a certified release commit.

## 2. Project Identity

- Project: Budget vs Actual Variance Navigator
- Program: Real Rails Interns Batch 8
- Phase: Phase 3 — Final Deployment, Validation, Evidence & Handover
- Current development branch: `master`
- Intended release version: `1.0.0`
- Proposed Git tag: `phase3-v1.0.0` (NOT CREATED)

## 3. Release Commit

- Intended final commit: PENDING
- Certified commit SHA: NOT ASSIGNED
- Remote publication: NOT COMPLETED FOR POST #6
- Release tag: NOT CREATED
- Tag-to-commit verification: NOT PERFORMED

The previously deployed backend commit `08327d7` is a deployment reference only. It is not the certified Post #6 release commit.

## 4. Application Components

- Frontend: Next.js operational dashboard and Data Intelligence experience.
- Backend: FastAPI application and intelligence APIs.
- Operational dataset: `backend/budget_data.csv`.
- Canonical intelligence dataset: `data/canonical/intelligence_data.csv`.
- Approved analytical track: Track A — Comparative Intelligence.
- Deterministic assistant: five approved question types.
- Optional Gemini explanation layer: implemented and tested locally; public deployment pending.

## 5. Versioned Analytical Assets

- Dataset version: `1.0.0`
- Analytical method version: `1.0.0`
- Intelligence contract version: `1.0.0`
- Canonical dataset profile: 72 rows × 20 columns.
- Independent synthetic source observations: 18.
- Analytical findings: 64 (16 overall and 48 monthly).
- Latest recorded combined validation: 1,325 passed, 0 failed, 0 warnings.

These figures describe the recorded validation outputs and do not imply population-level evidence or predictive capability.

## 6. Required Release Documentation

- `docs/PHASE3_RELEASE_MANIFEST.md`
- `docs/CLEAN_CLONE_VALIDATION_REPORT.md`
- `docs/FINAL_ANALYTICAL_REVALIDATION.md`
- `docs/BUILD_AND_ENVIRONMENT_VALIDATION.md`
- `docs/FINAL_OPERATIONAL_REGRESSION_REPORT.md`
- `docs/FINAL_DATA_INTELLIGENCE_VALIDATION.md`
- `docs/FINAL_ASSISTANT_VALIDATION.md`
- `docs/FINAL_AUTOMATED_TEST_REPORT.md`
- `docs/PHASE3_FINAL_UAT.md`
- `docs/DEPLOYMENT_VALIDATION_REPORT.md`
- `docs/PHASE3_FINAL_ARCHITECTURE.md`
- `docs/PHASE3_COMPLETION_REPORT.md`
- `docs/PHASE3_HANDOVER_GUIDE.md`
- Root `README.md`
- `final-evidence/`
- `repomix-phase3-final.md`

## 7. Validation and Evidence Status

- Full pytest-discoverable test suite: PASS, 24 collected, 24 passed, 0 failed, 0 skipped, 0 warnings (`python -m pytest -v`).
- Dedicated Gemini explainer tests: PASS, 8 passed, 0 failed. These tests are included in the 24-test total and are not additional tests.
- Backend and test Python compilation using `python -m compileall -q backend tests`: PASS.
- Frontend production build and TypeScript validation: PASS.
- Targeted Data Intelligence page lint: PASS.
- Docker image build and module import: PASS.
- Local Docker runtime and API checks: PASS.
- Public deterministic assistant checks: PASS.
- Public Gemini deployment: NOT VALIDATED.
- Fresh Post #6 Selenium browser validation: BLOCKED by Windows Application Control before browser startup.
- Clean-clone validation: NOT EXECUTED.
- Final evidence package: PARTIALLY ASSEMBLED — 13 FILES; RELEASE COMPLETENESS AND FINAL VERIFICATION PENDING.
- Final Repomix: NOT GENERATED.
- Reviewer approval: PENDING.

## 8. Deployment References

- Frontend: https://poc4-budget-phase3-frontend.onrender.com
- Backend: https://poc4-budget-phase3-backend.onrender.com
- Last recorded public backend commit: `08327d7`
- Public assistant mode: deterministic Mode A.
- Local Gemini Mode B: not yet published or deployed.

## 9. Security and Configuration

- Gemini API key must be configured privately on the backend only.
- No real API key may be committed.
- `.env.example` may document variable names and non-secret defaults only.
- No API credentials or private environment files belong in the evidence package.
- Gemini explanations must not replace deterministic financial values or evidence.

## 10. Certification Gates

Certification requires, at minimum:
1. Final approved source changes and a clean working tree.
2. Successful clean-clone validation against the intended release commit.
3. Required analytical, build, API, and automated test validation.
4. Fresh browser-based acceptance or an explicitly approved alternative.
5. Final evidence package and Repomix.
6. Deployment verification for the intended release.
7. Manifest commit and tag verification.
8. Reviewer approval.

## 11. Final Release Decision

**PHASE 3 CERTIFICATION: BLOCKED — OUTSTANDING POST #6 REQUIREMENTS.**

- Certified commit: PENDING.
- Certified tag: PENDING.
- Reviewer decision: PENDING.

This draft must be updated from actual final validation and Git evidence before it can serve as a release manifest. It must not be represented as a certified release.
