"""Deterministic, evidence-grounded assistant for Phase 3 Post #5."""

import re
from uuid import uuid4
from typing import Any


MAX_QUESTION_LENGTH = 500
MAX_RESULTS = 25
MAX_EVIDENCE_REFERENCES = 10
MAX_EVIDENCE_EXCERPT_LENGTH = 300
MAX_FOLLOW_UPS = 3

SUPPORTED_INTENTS = {
    "cost_centre_variance_comparison",
    "department_comparison",
    "expenditure_category_lookup",
    "finding_evidence_lookup",
    "monthly_insufficient_evidence_lookup",
}

MONTHLY_RESULT_TYPES = {
    "monthly_cost_centre_comparison",
    "monthly_department_comparison",
    "monthly_expenditure_category_comparison",
}

UNSAFE_PATTERNS = [
    r"\b(ignore|disregard|bypass|override)\b.{0,60}\b(instructions|rules|restrictions|safety|system)\b",
    r"\b(reveal|show|print|expose)\b.{0,60}\b(secret|password|api key|token|system prompt)\b",
    r"\b(execute|run)\b.{0,40}\b(sql|python|shell|command)\b",
    r"\b(drop table|delete from|union select|insert into)\b",
]


def normalize_text(value: str) -> str:
    """Normalize user-supplied text for exact entity matching."""
    return " ".join(value.strip().casefold().split())


def is_unsafe_question(question: str) -> bool:
    """Identify obvious attempts to bypass restrictions or access secrets."""
    text = question.casefold()

    return any(
        re.search(pattern, text)
        for pattern in UNSAFE_PATTERNS
    )


def build_response(
    *,
    status: str,
    intent: str | None,
    answer: str,
    metadata: dict[str, Any] | None = None,
    evidence_references: list[dict[str, Any]] | None = None,
    key_values: list[dict[str, Any]] | None = None,
    limitation: list[str] | str | None = None,
    suggested_follow_ups: list[str] | None = None,
) -> dict[str, Any]:
    """Build the standard response envelope for every assistant outcome."""
    return {
        "answer_id": str(uuid4()),
        "status": status,
        "intent": intent,
        "answer": answer,
        "evidence_references": (
            (evidence_references or [])[:MAX_EVIDENCE_REFERENCES]
        ),
        "key_values": (key_values or [])[:MAX_RESULTS],
        "metadata": metadata or {},
        "limitation": limitation or [],
        "suggested_follow_ups": (
            (suggested_follow_ups or [])[:MAX_FOLLOW_UPS]
        ),
    }



def contains_exact_phrase(text: str, phrase: str) -> bool:
    """Match exact phrases even when surrounded by punctuation."""
    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)
    pattern = rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"

    return re.search(pattern, normalized_text) is not None


def get_results_by_type(
    findings: list[dict[str, Any]],
    result_type: str,
) -> list[dict[str, Any]]:
    """Return findings matching one exact approved result type."""
    return [
        item
        for item in findings
        if item.get("result_type") == result_type
    ]


def get_finding_by_id(
    findings: list[dict[str, Any]],
    result_id: str,
) -> dict[str, Any] | None:
    """Retrieve one finding by its exact result ID."""
    for item in findings:
        if item.get("result_id") == result_id:
            return item

    return None


def get_known_entity_names(
    findings: list[dict[str, Any]],
    result_type: str,
) -> list[str]:
    """Collect unique entity names from one approved result type."""
    names = {
        str(item.get("group_key")).strip()
        for item in findings
        if item.get("result_type") == result_type
        and item.get("group_key")
    }

    return sorted(names, key=str.casefold)


def find_matching_entities(
    question: str,
    known_names: list[str],
) -> list[str]:
    """Find approved entity names mentioned as exact phrases."""
    return [
        name
        for name in known_names
        if contains_exact_phrase(question, name)
    ]


def classify_intent(
    question: str,
    findings: list[dict[str, Any]],
) -> str | None:
    """Map a question to one of the five approved assistant intents."""
    text = normalize_text(question)

    # Q-05: Monthly findings with insufficient evidence.
    if (
        "monthly" in text
        and any(word in text for word in ("evidence", "findings", "results"))
    ):
        return "monthly_insufficient_evidence_lookup"

    # Q-04: Evidence lookup for a finding or cost centre.
    if (
        re.search(r"\btrack-a-[a-z0-9_-]+\b", text)
        or (
            re.search(r"\bcc-\d+\b", text)
            and any(
                word in text
                for word in ("evidence", "explain", "explanation", "why", "finding")
            )
        )
    ):
        return "finding_evidence_lookup"

    # Q-02: Department comparison.
    departments = get_known_entity_names(
        findings, "department_comparison"
    )
    if (
        "department" in text
        or (
            len(find_matching_entities(question, departments)) >= 2
            and any(word in text for word in ("compare", "comparison", "versus", "vs"))
        )
    ):
        return "department_comparison"

    # Q-03: Expenditure category lookup.
    categories = get_known_entity_names(
        findings, "expenditure_category_comparison"
    )
    if "category" in text or "expenditure" in text:
        return "expenditure_category_lookup"

    if find_matching_entities(question, categories):
        return "expenditure_category_lookup"

    # Q-01: Cost-centre variance comparison.
    if (
        "cost centre" in text
        or "cost center" in text
        or "cost-centre" in text
        or "cost-center" in text
    ):
        return "cost_centre_variance_comparison"

    return None



def validate_question(question: Any) -> str | None:
    """Validate question type, emptiness, and maximum length."""
    if not isinstance(question, str) or not question.strip():
        return "MISSING_PARAMETER"

    if len(question) > MAX_QUESTION_LENGTH:
        return "OUT_OF_SCOPE"

    return None


def build_evidence_references(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build grouped evidence references without dropping source identifiers."""
    grouped: dict[str, list[dict[str, Any]]] = {}

    for item in findings:
        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError("Required finding evidence is unavailable.")

        required_fields = (
            "source_record_ids",
            "canonical_record_ids",
            "independent_source_count",
            "reporting_period",
        )
        if any(field not in evidence for field in required_fields):
            raise ValueError("Required finding evidence is incomplete.")

        source_ids = evidence["source_record_ids"]
        canonical_ids = evidence["canonical_record_ids"]
        period = evidence["reporting_period"]
        limitations = item.get("limitation")

        if (
            not item.get("result_id")
            or not item.get("result_type")
            or not item.get("quality_status")
            or not isinstance(source_ids, list)
            or not isinstance(canonical_ids, list)
            or not isinstance(period, dict)
            or not isinstance(limitations, (list, str))
        ):
            raise ValueError("Finding evidence failed validation.")

        result_type = str(item["result_type"])
        grouped.setdefault(result_type, []).append(
            {
                "result_id": item["result_id"],
                "source_record_ids": source_ids,
                "canonical_record_ids": canonical_ids,
                "reporting_period": period,
                "independent_source_count": evidence[
                    "independent_source_count"
                ],
                "quality_status": item["quality_status"],
                "limitations": limitations,
                "excerpt": str(item.get("finding", ""))[
                    :MAX_EVIDENCE_EXCERPT_LENGTH
                ],
            }
        )

    if len(grouped) > MAX_EVIDENCE_REFERENCES:
        raise ValueError("Evidence reference limit exceeded.")

    return [
        {
            "result_type": result_type,
            "findings": grouped[result_type],
        }
        for result_type in sorted(grouped)
    ]


def build_key_values(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Copy approved financial and ranking values without recalculation."""
    allowed_fields = (
        "budget_total",
        "actual_total",
        "variance_amount",
        "variance_percentage",
        "committed_total",
        "forecast_total",
    )
    values = []

    for item in findings:
        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError("Finding financial evidence is unavailable.")

        entry = {
            "result_id": item.get("result_id"),
            "result_type": item.get("result_type"),
            "entity_id": item.get("entity_id"),
            "group_key": item.get("group_key"),
            "priority_rank": item.get("priority_rank"),
            "result_value": item.get("result_value"),
            "result_category": item.get("result_category"),
            "result_unit": item.get("result_unit"),
        }

        for field in allowed_fields:
            if field in evidence:
                entry[field] = evidence[field]

        values.append(entry)

    return values[:MAX_RESULTS]


def get_findings_by_entity(
    findings: list[dict[str, Any]],
    result_type: str,
    entity_name: str,
) -> list[dict[str, Any]]:
    """Match an entity against approved group and entity identifiers."""
    target = normalize_text(entity_name)

    return [
        item
        for item in findings
        if item.get("result_type") == result_type
        and (
            normalize_text(str(item.get("group_key", ""))) == target
            or normalize_text(str(item.get("entity_id", ""))) == target
        )
    ]


def build_intelligence_metadata(artifacts: dict[str, Any]) -> dict[str, Any]:
    """Return version and validation metadata from verified artifacts."""
    results = artifacts["results"]
    validation = artifacts["validation"]

    return {
        "project_id": results["project_id"],
        "approved_track": results["approved_track"],
        "contract_version": results["contract_version"],
        "dataset_version": results["dataset_version"],
        "method_version": results["method_version"],
        "generated_at": results.get("generated_at"),
        "result_count": results["result_count"],
        "validation_status": validation["overall_status"],
    }


def build_status_response(
    status: str,
    intent: str | None,
    answer: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a controlled response for unsupported or incomplete requests."""
    return build_response(
        status=status,
        intent=intent,
        answer=answer,
        metadata=metadata,
        limitation=[
            "No unsupported financial values or conclusions were generated."
        ],
    )


def resolve_two_departments(
    question: str,
    findings: list[dict[str, Any]],
) -> tuple[str | None, list[str]]:
    """Resolve exactly two approved department names from the question."""
    known_departments = get_known_entity_names(
        findings,
        "department_comparison",
    )
    matched = find_matching_entities(question, known_departments)

    if len(matched) == 0:
        return "MISSING_PARAMETER", []

    if len(matched) == 1:
        return "MISSING_PARAMETER", matched

    if len(matched) > 2:
        return "AMBIGUOUS", matched

    return None, matched


def resolve_expenditure_category(
    question: str,
    findings: list[dict[str, Any]],
) -> tuple[str | None, str | None]:
    """Resolve one exact approved expenditure category."""
    known_categories = get_known_entity_names(
        findings,
        "expenditure_category_comparison",
    )
    matched = find_matching_entities(question, known_categories)

    if len(matched) == 0:
        return "MISSING_PARAMETER", None

    if len(matched) > 1:
        return "AMBIGUOUS", None

    return None, matched[0]


def resolve_finding(
    question: str,
    findings: list[dict[str, Any]],
) -> tuple[str | None, dict[str, Any] | None]:
    """Resolve one finding by exact result ID or cost-centre identifier."""
    result_ids = re.findall(
        r"\btrack-a-[a-z0-9_-]+\b",
        question,
        flags=re.IGNORECASE,
    )

    if result_ids:
        finding = get_finding_by_id(findings, result_ids[0])

        if finding is None:
            return "OUT_OF_SCOPE", None

        return None, finding

    cost_centres = re.findall(
        r"\bcc-\d+\b",
        question,
        flags=re.IGNORECASE,
    )

    if not cost_centres:
        return "MISSING_PARAMETER", None

    matches = get_findings_by_entity(
        findings,
        "cost_centre_comparison",
        cost_centres[0],
    )

    if not matches:
        return "OUT_OF_SCOPE", None

    if len(matches) > 1:
        return "AMBIGUOUS", None

    return None, matches[0]


def get_monthly_insufficient_findings(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return only approved monthly findings marked insufficient_evidence."""
    monthly_findings = []

    for result_type in sorted(MONTHLY_RESULT_TYPES):
        matching = get_results_by_type(findings, result_type)

        for finding in matching:
            if finding.get("quality_status") == "insufficient_evidence":
                monthly_findings.append(finding)

    monthly_findings.sort(
        key=lambda item: (
            item.get("period_start") or "",
            item.get("result_type") or "",
            item.get("group_key") or "",
        )
    )

    return monthly_findings


def build_suggested_follow_ups(intent: str) -> list[str]:
    """Return a maximum of three approved follow-up questions."""
    follow_ups = {
        "cost_centre_variance_comparison": [
            "Show the evidence for a specific cost centre.",
            "Compare two departments.",
            "Show monthly findings with insufficient evidence.",
        ],
        "department_comparison": [
            "Compare another pair of departments.",
            "Look up an expenditure category.",
            "Show monthly findings with insufficient evidence.",
        ],
        "expenditure_category_lookup": [
            "Compare two departments.",
            "Compare cost-centre variances.",
            "Show monthly findings with insufficient evidence.",
        ],
        "finding_evidence_lookup": [
            "Compare cost-centre variances.",
            "Compare two departments.",
            "Look up an expenditure category.",
        ],
        "monthly_insufficient_evidence_lookup": [
            "Compare cost-centre variances.",
            "Compare two departments.",
            "Look up an expenditure category.",
        ],
    }

    return follow_ups.get(intent, [])[:MAX_FOLLOW_UPS]


def build_findings_answer(
    findings: list[dict[str, Any]],
    heading: str,
) -> str:
    """Build an answer using only existing approved finding descriptions."""
    if not findings:
        return f"{heading}\nNo matching approved findings were found."

    lines = [heading]

    for finding in findings:
        finding_text = finding.get("finding")

        if isinstance(finding_text, str) and finding_text.strip():
            lines.append(f"- {finding_text.strip()}")
        else:
            lines.append(
                f"- Finding {finding.get('result_id', 'unknown')} "
                "has no approved description available."
            )

    return "\n".join(lines)



def process_question(
    question: Any,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    """Route a question through the five approved deterministic intents."""
    validation_error = validate_question(question)

    if validation_error:
        return build_status_response(
            validation_error,
            None,
            "Please provide a valid question of no more than 500 characters.",
        )

    if is_unsafe_question(question):
        return build_status_response(
            "UNSAFE",
            None,
            "This request cannot be processed because it violates the assistant safety rules.",
        )

    findings = artifacts["results"]["results"]
    metadata = build_intelligence_metadata(artifacts)

    intent = classify_intent(question, findings)

    if intent is None:
        return build_status_response(
            "OUT_OF_SCOPE",
            None,
            "This question is outside the five supported assistant question types.",
            metadata,
        )

    selected_findings = []

    if intent == "cost_centre_variance_comparison":
        selected_findings = get_results_by_type(
            findings,
            "cost_centre_comparison",
        )
        selected_findings.sort(
            key=lambda item: (
                item.get("priority_rank") is None,
                item.get("priority_rank") or 0,
            )
        )

    elif intent == "department_comparison":
        error, departments = resolve_two_departments(question, findings)

        if error:
            return build_status_response(
                error,
                intent,
                "Please specify exactly two approved department names.",
                metadata,
            )

        for department in departments:
            selected_findings.extend(
                get_findings_by_entity(
                    findings,
                    "department_comparison",
                    department,
                )
            )

        if len(selected_findings) != 2:
            return build_status_response(
                "OUT_OF_SCOPE",
                intent,
                "The requested departments do not match exactly two approved findings.",
                metadata,
            )

    elif intent == "expenditure_category_lookup":
        error, category = resolve_expenditure_category(question, findings)

        if error:
            return build_status_response(
                error,
                intent,
                "Please specify one exact approved expenditure category.",
                metadata,
            )

        selected_findings = get_findings_by_entity(
            findings,
            "expenditure_category_comparison",
            category,
        )

        if len(selected_findings) != 1:
            return build_status_response(
                "OUT_OF_SCOPE",
                intent,
                "The requested category does not match exactly one approved finding.",
                metadata,
            )

    elif intent == "finding_evidence_lookup":
        error, finding = resolve_finding(question, findings)

        if error:
            return build_status_response(
                error,
                intent,
                "Please provide one valid finding ID or cost-centre ID.",
                metadata,
            )

        selected_findings = [finding]

    elif intent == "monthly_insufficient_evidence_lookup":
        selected_findings = get_monthly_insufficient_findings(findings)

    total_matched = len(selected_findings)
    selected_findings = selected_findings[:MAX_RESULTS]
    truncated = total_matched > len(selected_findings)

    limitations = []

    for finding in selected_findings:
        item_limitations = finding.get("limitation", [])

        if isinstance(item_limitations, str):
            item_limitations = [item_limitations]

        if isinstance(item_limitations, list):
            for limitation in item_limitations:
                if isinstance(limitation, str) and limitation not in limitations:
                    limitations.append(limitation)

    if truncated:
        limitations.append(
            f"Only the first {MAX_RESULTS} of {total_matched} matching findings are included."
        )

    metadata["returned_count"] = len(selected_findings)
    metadata["total_matched"] = total_matched
    metadata["truncated"] = truncated

    if intent == "monthly_insufficient_evidence_lookup":
        heading = "Monthly findings marked insufficient evidence:"
    elif intent == "department_comparison":
        heading = "Approved department comparison:"
    elif intent == "expenditure_category_lookup":
        heading = "Approved expenditure category finding:"
    elif intent == "finding_evidence_lookup":
        heading = "Approved finding evidence:"
    else:
        heading = "Approved cost-centre variance comparison:"

    answer = build_findings_answer(selected_findings, heading)

    return build_response(
        status="SUPPORTED",
        intent=intent,
        answer=answer,
        metadata=metadata,
        evidence_references=build_evidence_references(selected_findings),
        key_values=build_key_values(selected_findings),
        limitation=limitations,
        suggested_follow_ups=build_suggested_follow_ups(intent),
    )
