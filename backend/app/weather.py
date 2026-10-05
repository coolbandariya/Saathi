from datetime import datetime, timezone
import httpx
from .domain import SourceRef, ToolResult

class OpenMeteoWeather:
    base_url = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout = timeout

    def forecast(self, latitude: float, longitude: float, days: int = 3) -> ToolResult:
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            return ToolResult(ok=False, message="Invalid coordinates.")
        if days < 1 or days > 16:
            return ToolResult(ok=False, message="Forecast days must be between 1 and 16.")
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": days,
            "timezone": "auto",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        }
        try:
            response = httpx.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return ToolResult(
                ok=True,
                data=response.json(),
                sources=[SourceRef(name="Open-Meteo", url="https://open-meteo.com/en/docs", retrieved_at=datetime.now(timezone.utc))],
            )
        except httpx.HTTPError as exc:
            return ToolResult(ok=False, message=f"Weather provider unavailable: {exc.__class__.__name__}", sources=[SourceRef(name="Open-Meteo", url="https://open-meteo.com/en/docs")])
