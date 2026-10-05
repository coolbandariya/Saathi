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
