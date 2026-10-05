from app.intent import classify_intent


def test_human_phrase_wins():
    assert classify_intent("मुझे किसी इंसान से बात करनी है") == "human"


def test_negated_human_is_not_escalated():
    assert classify_intent("मुझे किसी इंसान से बात नहीं करनी") != "human"


def test_word_boundary_avoids_substring_match():
    assert classify_intent("personal finance advice") == "general"


def test_hindi_farming_terms():
    assert classify_intent("कल बारिश होगी क्या") == "farming"


def test_scheme_precedes_generic_farming_context():
    assert classify_intent("किसान की सरकारी योजना बताओ") == "scheme"
