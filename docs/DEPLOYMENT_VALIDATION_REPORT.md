# DEPLOYMENT VALIDATION REPORT

## 1. Purpose

This report records the deployment state and public-service checks for the Phase 3 Budget vs Actual Variance Navigator as part of Post #6.

## 2. Public Deployment References

The verified Phase 3 public services are:

- Frontend: https://poc4-budget-phase3-frontend.onrender.com
- Backend: https://poc4-budget-phase3-backend.onrender.com

The backend service name in Render is `poc4-budget-phase3-backend`. The frontend is configured to use the Phase 3 backend through `NEXT_PUBLIC_API_URL`.

The separate URL `https://poc4-budget-backend.onrender.com` is not the backend configured for this Phase 3 frontend and is not used as evidence in this report.

## 3. Public Availability Checks

Recorded checks against the correct public services:

| Check | Recorded result |
|---|---|
| Phase 3 frontend HTTP response | HTTP 200 |
| Phase 3 backend health | Healthy response |
| Backend OpenAPI document | Phase 3 routes present |
| Intelligence health | ready |
| Intelligence result count | 64 |
| Intelligence dataset version | 1.0.0 |
| Intelligence method version | 1.0.0 |
| Intelligence summary validation | PASS |
| Passed validation checks | 1,325 |
| Failed validation checks | 0 |
| Warning checks | 0 |

The public API checks establish availability and the reported analytical readiness at the time they were performed. They do not establish complete browser-based acceptance.

## 4. Currently Deployed Backend Version

The Render backend dashboard showed the live backend deployed from Git commit:

`08327d7` — `Implement grounded data assistant for Phase 3 Post 5`

The deployed public assistant is deterministic Mode A. Representative supported and unsupported assistant requests were checked against the public service.

The local Post #6 Gemini implementation is newer than this deployed backend version. It has not yet been published to the repository or deployed to Render.

## 5. Gemini Deployment Status

Gemini Mode B has passed local implementation, API, test, and Docker checks.

It is not currently enabled on the public Render deployment:
- The deployed backend commit predates the Gemini implementation.
- The Render backend environment page showed no Gemini environment variables configured.
- No API key is recorded in this repository report.
- The public assistant response did not contain Gemini explanation fields.

If Mode B is approved for public release, the required sequence is to publish the reviewed code, deploy the correct backend, and configure `GEMINI_API_KEY` and `GEMINI_MODEL` privately in the backend service environment. The API key must never be committed or placed in frontend variables.

The intended model setting is `gemini-3.5-flash-lite`. Deterministic answers and evidence must remain authoritative, with fallback behavior when the provider is unavailable.

## 6. Deployment Limitations

- The public Render deployment is not yet the complete local Post #6 implementation.
- Gemini Mode B is not publicly deployed or validated.
- A fresh Post #6 Selenium browser run was blocked by Windows Application Control before browser interaction.
- HTTP endpoint checks do not prove complete visual, interaction, accessibility, or responsive behavior.
- Final deployment evidence, clean-clone validation, release manifest, and reviewer approval remain outstanding.

## 7. Conclusion

**PASS WITH DOCUMENTED LIMITATIONS** for the verified current public Render frontend and backend availability and the public analytical API checks.

**NOT YET DEPLOYED** for the local Post #6 Gemini Mode B implementation.

The current public deployment must not be described as the final Post #6 release. This report does not declare Phase 3 complete or certified.
