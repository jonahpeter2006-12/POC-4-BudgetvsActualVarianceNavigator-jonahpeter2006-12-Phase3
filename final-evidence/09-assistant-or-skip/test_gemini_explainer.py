import pytest
import backend.gemini_explainer as gemini


@pytest.fixture
def deterministic_response():
    return {
        "status": "SUPPORTED",
        "intent": "finding_evidence_lookup",
        "answer": "Cost Centre CC-101 is over budget by 14500.",
        "key_values": [
            {
                "cost_centre": "CC-101",
                "budget_amount": 135000,
                "actual_amount": 149500,
                "variance_amount": 14500,
            }
        ],
        "evidence_references": [
            {"result_id": "CC-101", "source_record_ids": ["SRC-01"]}
        ],
        "limitation": ["The dataset is synthetic."],
        "metadata": {
            "dataset_version": "1.0.0",
            "method_version": "1.0.0",
        },
    }


def test_missing_api_key_disables_gemini(
    monkeypatch, deterministic_response
):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result == {
        "explanation": None,
        "explanation_status": "disabled",
        "explanation_provider": None,
    }


def test_valid_explanation_is_accepted(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    explanation = (
        "CC-101 is over budget by 14500. "
        "The supplied evidence is synthetic and supports human review."
    )

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        lambda question, payload: explanation,
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] == explanation
    assert result["explanation_status"] == "generated"
    assert result["explanation_provider"] == "gemini"


def test_unsupported_numeric_claim_is_rejected(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        lambda question, payload: (
            "CC-101 is over budget by 999999."
        ),
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] is None
    assert result["explanation_status"] == "rejected"


def test_contradictory_budget_direction_is_rejected(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        lambda question, payload: (
            "CC-101 is under budget."
        ),
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] is None
    assert result["explanation_status"] == "rejected"


def test_provider_failure_uses_fallback(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def simulate_provider_failure(question, payload):
        raise RuntimeError("Simulated provider failure.")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        simulate_provider_failure,
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] is None
    assert result["explanation_status"] == "fallback"
    assert result["explanation_provider"] is None


def test_unsupported_response_does_not_call_gemini(
    monkeypatch,
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def unexpected_provider_call(question, payload):
        raise AssertionError("Gemini must not be called.")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        unexpected_provider_call,
    )

    result = gemini.explain_supported_response(
        "Predict next year's revenue",
        {"status": "OUT_OF_SCOPE"},
    )

    assert result == {
        "explanation": None,
        "explanation_status": "not_applicable",
        "explanation_provider": None,
    }
def test_explanation_exceeding_length_limit_is_rejected(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        lambda question, payload: "A" * (
            gemini.MAX_EXPLANATION_LENGTH + 1
        ),
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] is None
    assert result["explanation_status"] == "rejected"


def test_empty_explanation_is_rejected(
    monkeypatch, deterministic_response
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.setattr(
        gemini,
        "_request_gemini",
        lambda question, payload: "   ",
    )

    result = gemini.explain_supported_response(
        "Why is CC-101 above budget?",
        deterministic_response,
    )

    assert result["explanation"] is None
    assert result["explanation_status"] == "rejected"