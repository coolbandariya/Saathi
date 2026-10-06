from app.intent import extract_farming_entities


def test_extract_hindi_farming_entities():
    entities = extract_farming_entities("सोनीपत मंडी में गेहूं का भाव क्या है")
    assert entities.commodity == "Wheat"
    assert entities.state == "Haryana"
    assert entities.district == "Sonipat"
    assert entities.market == "Sonipat"


def test_extracts_hinglish_entities_without_market():
    entities = extract_farming_entities("Karnal me wheat ka rate batao")
    assert entities.commodity == "Wheat"
    assert entities.state == "Haryana"
    assert entities.district == "Karnal"
    assert entities.market is None
