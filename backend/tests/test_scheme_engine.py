from app.scheme_engine import SchemeRule, evaluate


def test_scheme_rule_reports_missing_items():
    rule = SchemeRule("demo scholarship", ("age", "income"), ("income_certificate",))
    result = evaluate(rule, {"age": 19}, set())
    assert not result.eligible
    assert result.missing_fields == ("income",)
    assert result.missing_documents == ("income_certificate",)


def test_scheme_rule_can_be_eligible():
    rule = SchemeRule("demo scholarship", ("age",), ("identity_proof",))
    result = evaluate(rule, {"age": 19}, {"identity_proof"})
    assert result.eligible
