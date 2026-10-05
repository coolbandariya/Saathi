import httpx
from datetime import datetime, timezone
from .provenance import ToolResult, SourceRecord

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

class OpenMeteoWeatherTool:
    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self.timeout_seconds = timeout_seconds

    async def forecast(self, *, latitude: float, longitude: float) -> ToolResult:
        params = {"latitude": latitude, "longitude": longitude, "current":"temperature_2m,precipitation", "hourly":"precipitation_probability,temperature_2m", "forecast_hours": 24, "timezone":"auto"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(OPEN_METEO_URL, params=params)
                response.raise_for_status()
                payload = response.json()
            current = payload.get("current", {})
            hourly = payload.get("hourly", {})
            probabilities = hourly.get("precipitation_probability", [])
            return ToolResult(ok=True, data={"temperature_c":current.get("temperature_2m"), "precipitation_mm":current.get("precipitation"), "next_24h_rain_probability_max":max(probabilities or [0])}, source=SourceRecord(name="Open-Meteo", url=OPEN_METEO_URL, retrieved_at=datetime.now(timezone.utc)))
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            return ToolResult(ok=False, error_code="WEATHER_PROVIDER_ERROR", retryable=True, data={"detail":type(exc).__name__})
