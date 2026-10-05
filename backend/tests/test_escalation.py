from backend.app.escalation import EscalationPolicy


def test_explicit_human_request_always_escalates() -> None:
    decision = EscalationPolicy().evaluate(confidence=0.99, explicit_human_request=True)
    assert decision.escalate is True
    assert decision.reason == "explicit_human_request"


def test_low_confidence_escalates() -> None:
    decision = EscalationPolicy(minimum_confidence=0.7).evaluate(confidence=0.69)
    assert decision.escalate is True
    assert decision.reason == "low_confidence"


def test_provider_failure_escalates() -> None:
    decision = EscalationPolicy().evaluate(confidence=0.9, provider_failed=True)
    assert decision.escalate is True
    assert decision.reason == "provider_failure"


def test_safe_confident_result_does_not_escalate() -> None:
    decision = EscalationPolicy().evaluate(confidence=0.8)
    assert decision.escalate is False
