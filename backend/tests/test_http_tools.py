import asyncio
from app.http_tools import OpenMeteoWeatherTool

class FakeResponse:
    def raise_for_status(self): pass
    def json(self):
        return {"current":{"temperature_2m":27,"precipitation":0},"hourly":{"precipitation_probability":[10,20,30]}}

class FakeClient:
    async def __aenter__(self): return self
    async def __aexit__(self,*args): pass
    async def get(self,*args,**kwargs): return FakeResponse()

def test_open_meteo_mapping(monkeypatch):
    import app.http_tools as module
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kwargs: FakeClient())
    result=asyncio.run(OpenMeteoWeatherTool().forecast(latitude=28.99,longitude=77.02))
    assert result.ok
    assert result.data["next_24h_rain_probability_max"] == 30


class MandiResponse:
    def raise_for_status(self): pass
    def json(self):
        return {
            "records": [{
                "commodity": "Rice",
                "state": "Haryana",
                "district": "Sonipat",
                "market": "Sonipat",
                "Modal_Price": "2400",
            }]
        }


class MandiClient:
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def get(self, *args, **kwargs): return MandiResponse()


def test_mandi_rejects_entity_mismatch(monkeypatch):
    import app.http_tools as module
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kwargs: MandiClient())
    from app.http_tools import DataGovMandiTool
    result = asyncio.run(
        DataGovMandiTool(api_key="test", resource_id="resource").price(
            commodity="Wheat",
            state="Haryana",
            district="Sonipat",
        )
    )
    assert not result.ok
    assert result.error_code == "MANDI_ENTITY_MISMATCH"


def test_mandi_prefers_newest_arrival_date(monkeypatch):
    import app.http_tools as module
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kwargs: MandiDateClient())
    from app.http_tools import DataGovMandiTool
    result = asyncio.run(
        DataGovMandiTool(api_key="test", resource_id="resource").price(
            commodity="Wheat",
            state="Haryana",
            district="Sonipat",
            market="Sonipat",
        )
    )
    assert result.ok
    assert result.data["modal_price"] == 2600
    assert result.data["arrival_date"] == "2026-10-08"


class MandiDateResponse:
    def raise_for_status(self): pass
    def json(self):
        return {
            "records": [
                {
                    "commodity": "Wheat",
                    "state": "Haryana",
                    "district": "Sonipat",
                    "market": "Sonipat",
                    "arrival_date": "2026-10-07",
                    "Modal_Price": "2400",
                },
                {
                    "commodity": "Wheat",
                    "state": "Haryana",
                    "district": "Sonipat",
                    "market": "Sonipat",
                    "arrival_date": "2026-10-08",
                    "Modal_Price": "2600",
                },
            ]
        }


class MandiDateClient:
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def get(self, *args, **kwargs): return MandiDateResponse()


def test_mandi_rejects_latest_date_tie(monkeypatch):
    import app.http_tools as module
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda **kwargs: MandiTieClient())
    from app.http_tools import DataGovMandiTool
    result = asyncio.run(
        DataGovMandiTool(api_key="test", resource_id="resource").price(
            commodity="Wheat",
            state="Haryana",
            district="Sonipat",
            market="Sonipat",
        )
    )
    assert not result.ok
    assert result.error_code == "MANDI_AMBIGUOUS_MARKET"


class MandiTieResponse:
    def raise_for_status(self): pass
    def json(self):
        return {
            "records": [
                {
                    "commodity": "Wheat",
                    "state": "Haryana",
                    "district": "Sonipat",
                    "market": "Sonipat",
                    "arrival_date": "2026-10-08",
                    "Modal_Price": "2500",
                },
                {
                    "commodity": "Wheat",
                    "state": "Haryana",
                    "district": "Sonipat",
                    "market": "Sonipat",
                    "arrival_date": "2026-10-08",
                    "Modal_Price": "2600",
                },
            ]
        }


class MandiTieClient:
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def get(self, *args, **kwargs): return MandiTieResponse()
