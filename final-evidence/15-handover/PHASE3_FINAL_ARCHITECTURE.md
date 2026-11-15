# PHASE 3 FINAL ARCHITECTURE

## 1. Purpose

This document describes the Phase 3 architecture as implemented and validated during Post #6. It distinguishes the current public deployment from the newer local Gemini implementation.

## 2. Architecture Overview

The application retains its existing containerized frontend and backend architecture.

The main components are:

1. Frontend — Next.js application providing the operational dashboard and Data Intelligence interface.
2. Backend — FastAPI application exposing operational, analytical, and assistant APIs.
3. Operational data — `backend/budget_data.csv`, used by the existing operational dashboard.
4. Canonical intelligence data — `data/canonical/intelligence_data.csv`, used by the approved Track A analytical pipeline.
5. Analytical outputs — versioned comparative findings, validation metrics, and evidence references.
6. Grounded assistant — deterministic question handling over the approved findings and evidence.
7. Optional explanation provider — local Post #6 Gemini Mode B implementation, which explains supported deterministic responses without generating authoritative financial values.

## 3. Frontend

The frontend is implemented using Next.js.

It provides:
- The existing operational dashboard.
- The Data Intelligence page.
- Comparative findings and validation information.
- Evidence details.
- The grounded assistant interface.
- An optional separate Gemini explanation panel in the local Post #6 implementation.

The frontend communicates with the backend through the configured API base URL. The public Render frontend uses:

`NEXT_PUBLIC_API_URL=https://poc4-budget-phase3-backend.onrender.com`

## 4. Backend and API

The backend is implemented using FastAPI and retains the existing operational API.

The Phase 3 API includes:
- `GET /api/intelligence/health`
- `GET /api/intelligence/metadata`
- `GET /api/intelligence/summary`
- `GET /api/intelligence/results`
- `GET /api/intelligence/results/{result_id}`
- `POST /api/assistant/query`

The assistant first processes a question using the deterministic approved scope. Unsupported questions return an out-of-scope response rather than generating unsupported financial conclusions.

## 5. Data and Analytical Layer

The canonical dataset is:

`data/canonical/intelligence_data.csv`

Its recorded profile is 72 rows and 20 columns, derived from 18 independent synthetic source observations. Each source observation expands into four financial measure records.

The approved analytical method is Track A — Comparative Intelligence:
- Dataset version: 1.0.0.
- Method version: 1.0.0.
- Contract version: 1.0.0.
- Findings: 64 total.
- Overall findings: 16.
- Monthly findings: 48.

Variance is calculated as Actual minus Budget. Committed and Forecast remain separate measures. Forecast is illustrative and is not a prediction.

## 6. Assistant and Optional Gemini Layer

The deterministic assistant supports five approved question types and retains finding identifiers, source identifiers, canonical identifiers, and documented limitations.

The local Post #6 Gemini module:
- Uses a backend-side API key.
- Calls the Gemini Interactions API.
- Receives only supported deterministic response context for explanation.
- Does not replace deterministic financial values or evidence.
- Uses bounded output and numeric/direction validation.
- Falls back to the deterministic response when disabled or unavailable.
- Does not receive the API key through the frontend.

The local model default is `gemini-3.5-flash-lite`.

These Gemini capabilities have been tested locally. They are not present in the currently deployed public Render backend at commit `08327d7`.

## 7. Deployment Architecture

The public deployment uses separate Render frontend and backend services:

- Frontend service: `poc4-budget-phase3-frontend`.
- Backend service: `poc4-budget-phase3-backend`.

The backend is containerized using `backend/Dockerfile`. The local Post #6 Docker image was built and tested separately.

The current public deployment remains on the earlier deterministic assistant version. The local Gemini implementation has not yet been published or deployed.

## 8. Security and Reliability Boundaries

- Gemini credentials are backend-only secrets and must not be committed.
- The `.env.example` file contains variable names and a model default, not a real API key.
- Missing credentials and provider failures must preserve deterministic fallback behavior.
- Gemini explanations are non-authoritative.
- Deterministic findings and evidence remain the source of financial values.
- Unsupported questions remain out of scope.
- The assistant's validation checks are not a claim of comprehensive prompt-injection or semantic security protection.
- Public endpoint availability does not establish authentication, exhaustive authorization, or a complete security audit.

## 9. Architecture Limitations

- The data is synthetic and preserves only 18 independent source observations.
- The reporting period covers January–March 2026.
- Monthly findings with insufficient evidence remain limited.
- Forecast values are illustrative.
- Browser-based Post #6 validation remains blocked by the local Windows Application Control restriction.
- The public Render deployment does not yet include the local Gemini implementation.

## 10. Conclusion

The Phase 3 architecture retains the approved operational application, comparative intelligence pipeline, evidence-grounded deterministic assistant, and separate frontend/backend deployment.

The optional Gemini explanation layer is a bounded local extension, not a replacement for deterministic intelligence or a new analytical model.

This architecture report documents the current implementation boundaries. It does not claim that the complete Post #6 release has been deployed, browser-validated, or certified.
