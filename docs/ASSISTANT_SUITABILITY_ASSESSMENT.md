# Assistant Suitability Assessment

## Project
- PoC: 4 — Budget vs Actual Variance Navigator
- Batch: 8
- Phase: 3 — Post #5: Grounded Natural-Language Data Assistant

## 1. Assessment Outcome

**DETERMINISTIC ASSISTANT SUITABLE — LLM NOT REQUIRED**

A guided, deterministic assistant is suitable for this project. Existing approved intelligence outputs and read-only API endpoints provide structured information for answering a defined set of business questions without introducing an LLM.

## 2. User Value

The assistant will help users retrieve and understand approved variance findings through guided natural-language questions, reducing the need to manually search and filter the Data Intelligence page.

## 3. Supported Question Candidates

1. Which cost centres have the largest approved variances?
2. How do two departments compare?
3. What is the approved variance for a specified expenditure category?
4. What evidence supports a particular finding?
5. Why does a monthly finding have insufficient evidence?

Only approved result types and available parameters may be used.

## 4. Data and Evidence Readiness

- Approved intelligence output contains 64 findings.
- Six approved result types are available.
- Findings contain evidence references, quality status, data version, method version, and limitations.
- The dataset manifest identifies version 1.0.0 and validated status.
- The source dataset contains 18 synthetic observations.
- The 72 canonical records represent four financial measures derived from those 18 observations, not 72 independent transactions.
- Monthly findings with fewer than three independent observations are marked `insufficient_evidence`.

## 5. Deterministic Retrieval Feasibility

The existing API supports:
- Filtering by result type.
- Filtering by evidence quality.
- Filtering by variance category.
- Searching approved findings.
- Retrieving a finding by its result ID.
- Pagination.

The assistant should retrieve approved findings rather than recalculate financial values or generate new analytical results.

## 6. LLM Decision

An LLM is not justified at this stage.

The existing structured findings and API filters can support the proposed questions through deterministic intent mapping, parameter validation, retrieval, and response templates.

No LLM should generate financial values, rankings, predictions, anomaly flags, or supporting evidence.

## 7. Security and Scope Limitations

- No authentication or authorization implementation was found in the inspected backend Python files.
- CORS restricts browser origins but is not an authentication mechanism.
- The dataset manifest declares synthetic data.
- The inspected source sample contains business grouping labels and financial measurements, with no obvious personal identifiers.
- Public API access must be documented as a limitation. Synthetic data does not prove that every deployed artifact is free of confidential information.
- The assistant must use approved read-only intelligence endpoints only.
- It must not expose unrestricted canonical data, filesystem access, environment variables, or arbitrary SQL/code execution.

## 8. Required Assistant Behaviour

The assistant must:
- Answer only approved question types.
- Preserve original values and evidence.
- Display relevant quality status and limitations.
- Ask for missing parameters when necessary.
- Clarify ambiguous requests.
- Refuse unsupported or unsafe requests.
- Report unavailable or stale data without inventing results.

## 9. Recommendation

Proceed with **Mode A — Deterministic Guided Assistant**, subject to the required architecture, safety, grounding, API, and user-acceptance testing.

Do not introduce an LLM unless a later documented requirement demonstrates a clear need and the governing guide's safeguards can be satisfied.

## 10. Approval Status

**Assessment recommendation prepared; reviewer approval not yet obtained.**

No assistant implementation or Post #6 work is included in this assessment.