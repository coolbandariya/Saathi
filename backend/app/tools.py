from datetime import datetime, timezone
from typing import Protocol

from .provenance import SourceRecord, ToolResult


class WeatherTool(Protocol):
    async def forecast(self, *, latitude: float, longitude: float) -> ToolResult: ...


class MandiTool(Protocol):
    async def price(self, *, commodity: str, state: str, district: str | None = None, market: str | None = None) -> ToolResult: ...


class DemoWeatherTool:
    async def forecast(self, *, latitude: float, longitude: float) -> ToolResult:
        return ToolResult(
            ok=True,
            data={
                "condition": "Partly cloudy",
                "temperature_c": 28,
                "rain_probability_pct": 20,
                "latitude": latitude,
                "longitude": longitude,
            },
            source=SourceRecord(
                name="Saathi Demo Weather",
                url="https://open-meteo.com/",
                retrieved_at=datetime.now(timezone.utc),
                freshness_note="DEMO DATA — replace with live provider before production.",
            ),
        )


class DemoMandiTool:
    async def price(self, *, commodity: str, state: str, district: str | None = None, market: str | None = None) -> ToolResult:
        return ToolResult(
            ok=True,
            data={
                "commodity": commodity,
                "market": market or district or state,
                "min_price": 2100,
                "modal_price": 2250,
                "max_price": 2325,
                "unit": "INR/quintal",
            },
            source=SourceRecord(
                name="Saathi Demo Mandi",
                url="https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi",
                retrieved_at=datetime.now(timezone.utc),
                freshness_note="DEMO DATA — not a live market quote.",
            ),
        )
