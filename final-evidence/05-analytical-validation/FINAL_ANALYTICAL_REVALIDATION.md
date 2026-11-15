# FINAL ANALYTICAL REVALIDATION

## 1. Purpose

This report records the Post #6 revalidation evidence for the approved Track A — Comparative Intelligence method. It confirms whether the existing analytical outputs, calculations, evidence, and validation status remain consistent with the approved Phase 3 scope.

## 2. Approved Analytical Scope

- Track: Track A — Comparative Intelligence.
- Method version: 1.0.0.
- Contract version: 1.0.0.
- Dataset version: 1.0.0.
- Analytical question: Which cost centres, departments, and expenditure categories show the largest budget-versus-actual differences, and where should a human reviewer focus budget review?
- Decision supported: Descriptive, evidence-based human review only.

No new analytical track, model, scoring method, or predictive capability was introduced.

## 3. Authoritative Data

The canonical input remains:

`data/canonical/intelligence_data.csv`

Recorded dataset profile:
- 72 canonical rows.
- 20 columns.
- 18 source observations preserved.
- Four financial measures: Budget, Actual, Committed, and Forecast.
- Three reporting months: January, February, and March 2026.
- Six cost centres, four departments, and six expenditure categories.

The 72 canonical rows represent four derived financial-measure records per source observation. They are not 72 independent transactions. All observations are synthetic.

## 4. Calculation Rules

The approved variance calculations remain:

`Variance = Actual - Budget`

`Variance % = (Actual - Budget) / Budget * 100`

Positive variance indicates spending above budget; negative variance indicates spending below budget.

Committed and Forecast remain separate measures. Forecast values are illustrative and are not predictions.

## 5. Analytical Output Coverage

The previously executed Track A output contains 64 findings:
- 16 overall comparison findings.
- 48 monthly findings.
- Overall dimensions: six cost centres, four departments, and six expenditure categories.
- Monthly dimensions: 18 cost-centre, 12 department, and 18 category findings.

Monthly findings with insufficient independent evidence remain explicitly limited and are not promoted to stronger conclusions.

## 6. Latest Revalidation Evidence

The updated local Docker image returned the following validation results from its intelligence summary endpoint:

| Validation item | Result |
|---|---:|
| Combined validation status | PASS |
| Passed checks | 1,325 |
| Failed checks | 0 |
| Warning checks | 0 |
| Analytical validation | 1,230 / 1,230 passed |
| Reconciliation validation | 95 / 95 passed |
| Aggregation reconciliation | PASS |
| Baseline comparison | PASS |
| Baseline calculation mismatches | 0 |
| Reproducibility | PASS |

The combined validation count is 1,325. The sensitivity assessment is reported separately and is not included in that combined total.

The correct public Phase 3 Render backend was also queried. Its intelligence summary returned PASS, with 1,325 passed checks, zero failed checks, and zero warnings.

## 7. Evidence and Interpretation Controls

The approved analytical method continues to require:
- Traceability to finding identifiers and source and canonical record identifiers.
- Separation of Budget, Actual, Committed, and Forecast.
- Disclosure of synthetic data and the 18 independent source observations.
- Disclosure of insufficient-evidence monthly findings.
- No population-level conclusions.
- No predictive, anomaly, fraud, or risk-scoring claims.

## 8. Revalidation Limitations

- The dataset remains synthetic and limited to 18 independent source observations.
- The reporting period covers only January–March 2026.
- Monthly findings with insufficient evidence remain descriptive.
- Forecast values remain illustrative.
- A completed sensitivity assessment does not establish statistical robustness.
- This report records the latest available local-container and public API evidence; it does not claim a new independent reconstruction of every analytical result during Post #6.

## 9. Conclusion

**PASS WITH DOCUMENTED ANALYTICAL LIMITATIONS.**

The approved Track A method and its version boundaries remain unchanged. The latest local-container and public Render API validation summaries both report 1,325 passed checks, zero failures, and zero warnings.

This analytical revalidation does not certify the entire Phase 3 release. Final certification remains subject to the outstanding Post #6 deployment, browser, evidence, clean-clone, and reviewer-approval requirements.

## Final Release-State Reconciliation — 2026-11-15

The analytical validation results remain unchanged: 1,325 combined analytical and reconciliation checks passed, with 0 failures and 0 warnings. The Track A comparative findings and documented analytical limitations remain the basis of this report.

Subsequent release validation:
- Fresh clean-clone validation completed with documented limitations: 24 targeted tests passed; compilation, reproducibility, frontend dependency installation, and frontend build passed.
- The clean-clone Docker build was BLOCKED because the Docker Desktop Linux engine was unavailable. An earlier Docker PASS refers to the original project environment only.
- Public Render deployment remains live on commit daa7f61, with the previously recorded public API validation.
- Local post-correction assistant tests: 27 passed (19 assistant API and 8 Gemini explainer tests).
- Local post-correction browser checks: 17 passed (4 assistant regression, 9 filter/responsive, and 4 viewport checks).

These later local assistant and browser results do not change the analytical validation totals and do not establish public post-correction browser acceptance. The local assistant correction has not been committed, pushed, or deployed.

The final evidence pack has been structurally assembled. Final Repomix generation, public post-correction browser acceptance or an approved alternative, and reviewer approval remain outstanding.

**Overall Phase 3 status: DRAFT — NOT CERTIFIED.**

## Final status reconciliation — 15 November 2026

This reconciliation supersedes earlier status snapshots in this document wherever they describe the assistant correction as unpublished, the public browser acceptance as not performed, or the public backend as remaining on commit `daa7f61`. Those statements accurately describe earlier checkpoints but are no longer the current release status.

### Verified current results

- The assistant scope correction is committed and pushed to GitHub `master` at commit `3610659d87831639ee2fc3b17d8ce66beb3fdcb1`.
- The Render dashboard independently confirmed the backend service `poc4-budget-phase3-backend` Live on commit `3610659`.
- Public assistant API regression: 4/4 checks passed. The supported comparison question returned `SUPPORTED`; the three predictive/future-projection questions returned `OUT_OF_SCOPE` with zero evidence.
- Public Selenium acceptance on 15 November 2026: **19 passed, 0 failed**. This included backend and intelligence health, summary, assistant API behavior, desktop dashboard rendering, Data Intelligence content, and both pages at a 390 × 844 mobile viewport.
- The public acceptance report is `final-evidence/browser-automation/post6-public-final-acceptance-20261115-142307.json`. The corresponding final dashboard and Data Intelligence screenshots are stored in the official evidence folders.
- The official evidence structure contains all 15 required folders and 73 files. The latest structural and evidence-copy consistency audits passed, with zero report-copy failures and zero required-evidence-copy failures.
- The correction's local targeted tests passed 27/27. Python compilation passed. Earlier clean-clone checks recorded 24 targeted tests passing, with the limitations below.

### Remaining limitations and certification status

- Clean-clone Docker build remains **BLOCKED** because the Docker Desktop Linux engine was unavailable during that validation.
- Full default pytest collection in the separate clean-clone environment was **BLOCKED** by missing `requests` for two legacy test modules; those modules were not executed in that environment.
- Public Gemini Mode B behavior has not been certified. The public results establish the tested deterministic assistant behavior only.
- Both Render frontend and backend services are confirmed Live on commit `029b6bb` (15 November 2026).
- Formal keyboard-only and screen-reader accessibility audits were not performed.
- The final Repomix snapshot was generated from GitHub master commit `029b6bb` and XML-validated on 15 November 2026.
- Reviewer approval and the required certification decision have not been received. The release tag has not been created.

**Current release status: NOT CERTIFIED — reviewer approval and final release packaging remain outstanding.**

The 19/19 public browser result is a successful acceptance test; it does not remove the documented clean-clone limitations or substitute for the required reviewer certification.
