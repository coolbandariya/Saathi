import asyncio
import base64

from app import http_tools, provider_adapters


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeClient:
    response = FakeResponse({})

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def get(self, *args, **kwargs):
        return self.response

    async def post(self, *args, **kwargs):
        return self.response


def test_open_meteo_adapter_preserves_coordinates(monkeypatch):
    FakeClient.response = FakeResponse({
        "current": {"temperature_2m": 31, "precipitation": 0.2},
        "hourly": {"precipitation_probability": [10, 35, 20]},
    })
    monkeypatch.setattr(http_tools.httpx, "AsyncClient", FakeClient)
    result = asyncio.run(http_tools.OpenMeteoWeatherTool().forecast(latitude=28.61, longitude=77.21))
    assert result.ok is True
    assert result.data["latitude"] == 28.61
    assert result.data["longitude"] == 77.21
    assert result.data["rain_probability_pct"] == 35
    assert result.source.name == "Open-Meteo"


def test_mandi_adapter_maps_government_record(monkeypatch):
    FakeClient.response = FakeResponse({
        "records": [{
            "Commodity": "Wheat",
            "Market": "Sonipat",
            "Min_Price": "2100",
            "Modal_Price": "2250",
            "Max_Price": "2325",
        }]
    })
    monkeypatch.setattr(http_tools.httpx, "AsyncClient", FakeClient)
    result = asyncio.run(http_tools.DataGovMandiTool(api_key="key", resource_id="resource").price(
        commodity="Wheat", state="Haryana", district="Sonipat"
    ))
    assert result.ok is True
    assert result.data["modal_price"] == 2250
    assert result.source.name == "Government OGD / AGMARKNET"


def test_sarvam_stt_maps_transcript(monkeypatch):
    FakeClient.response = FakeResponse({"transcript": "सोनीपत मंडी का भाव बताओ"})
    monkeypatch.setattr(provider_adapters.httpx, "AsyncClient", FakeClient)
    result = asyncio.run(provider_adapters.SarvamSpeechToTextProvider("key", "https://example.test").transcribe(
        b"audio", language="hi"
    ))
    assert result.startswith("सोनीपत")


def test_sarvam_tts_decodes_audio(monkeypatch):
    expected = b"RIFF-demo"
    FakeClient.response = FakeResponse({"audios": [base64.b64encode(expected).decode()]})
    monkeypatch.setattr(provider_adapters.httpx, "AsyncClient", FakeClient)
    result = asyncio.run(provider_adapters.SarvamTextToSpeechProvider("key", "https://example.test").synthesize(
        "नमस्ते", language="hi"
    ))
    assert result == expected
