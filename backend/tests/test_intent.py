from app.intent import classify_intent


def test_intent_normalizes_whitespace_and_case():
    assert classify_intent("  SCHOLARSHIP\n  help  ") == "scheme"


def test_hindi_intent_is_supported():
    assert classify_intent("मुझे मंडी का भाव बताओ") == "farming"
