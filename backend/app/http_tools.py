from datetime import datetime, timezone

import httpx

from .provenance import SourceRecord, ToolResult


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class OpenMeteoWeatherTool:
    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self.timeout_seconds = timeout_seconds

    async def forecast(self, *, latitude: float, longitude: float) -> ToolResult:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation",
            "hourly": "precipitation_probability,temperature_2m",
            "forecast_hours": 24,
            "timezone": "auto",
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(OPEN_METEO_URL, params=params)
                response.raise_for_status()
                payload = response.json()

            current = payload.get("current", {})
            hourly = payload.get("hourly", {})
            probabilities = hourly.get("precipitation_probability", [])
            temperature = current.get("temperature_2m")
            precipitation = current.get("precipitation")
            rain_probability = max(probabilities or [0])

            if temperature is None or not probabilities:
                raise ValueError("weather_payload_missing_required_fields")

            return ToolResult(
                ok=True,
                data={
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature_c": temperature,
                    "precipitation_mm": precipitation,
                    "rain_probability_pct": rain_probability,
                    "next_24h_rain_probability_max": rain_probability,
                },
                source=SourceRecord(
                    name="Open-Meteo",
                    url=OPEN_METEO_URL,
                    retrieved_at=datetime.now(timezone.utc),
                    freshness_note="LIVE provider response; forecast values can change.",
                ),
            )
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as exc:
            return ToolResult(
                ok=False,
                error_code="WEATHER_PROVIDER_ERROR",
                retryable=True,
                data={"detail": type(exc).__name__, "latitude": latitude, "longitude": longitude},
            )


class DataGovMandiTool:
    """AGMARKNET-backed OGD adapter.

    The OGD resource id and API key are configuration, not source-code constants.
    This keeps demo builds deterministic while allowing a real government resource
    to be enabled without changing orchestration code.
    """

    def __init__(
        self,
        *,
        api_key: str,
        resource_id: str,
        api_base: str = "https://api.data.gov.in/resource",
        timeout_seconds: float = 8.0,
    ) -> None:
        self.api_key = api_key
        self.resource_id = resource_id
        self.api_base = api_base.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def price(self, *, commodity: str, state: str, district: str | None = None) -> ToolResult:
        url = f"{self.api_base}/{self.resource_id}"
        filters = {
            "State": state,
            "Commodity": commodity,
        }
        if district:
            filters["District"] = district

        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": 25,
            **{f"filters[{key}]": value for key, value in filters.items()},
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()

            records = payload.get("records") or []
            if not records:
                return ToolResult(
                    ok=False,
                    error_code="MANDI_NO_RECORDS",
                    retryable=False,
                    data={"commodity": commodity, "state": state, "district": district},
                    source=SourceRecord(
                        name="Government OGD / AGMARKNET",
                        url=url,
                        retrieved_at=datetime.now(timezone.utc),
                        freshness_note="Government dataset queried; no matching record returned.",
                    ),
                )

            record = records[0]

            def number(*keys: str) -> float | None:
                for key in keys:
                    value = record.get(key)
                    if value in (None, ""):
                        continue
                    try:
                        return float(str(value).replace(",", "").strip())
                    except ValueError:
                        continue
                return None

            modal = number("Modal_Price", "Modal Price", "modal_price")
            minimum = number("Min_Price", "Min Price", "min_price")
            maximum = number("Max_Price", "Max Price", "max_price")
            if modal is None:
                return ToolResult(
                    ok=False,
                    error_code="MANDI_INVALID_RECORD",
                    retryable=False,
                    data={"record": record},
                    source=SourceRecord(
                        name="Government OGD / AGMARKNET",
                        url=url,
                        retrieved_at=datetime.now(timezone.utc),
                        freshness_note="Government dataset returned a record without a usable modal price.",
                    ),
                )

            return ToolResult(
                ok=True,
                data={
                    "commodity": record.get("Commodity", commodity),
                    "market": record.get("Market", district or state),
                    "min_price": minimum,
                    "modal_price": modal,
                    "max_price": maximum,
                    "unit": "INR/quintal",
                    "raw_record": record,
                },
                source=SourceRecord(
                    name="Government OGD / AGMARKNET",
                    url=url,
                    retrieved_at=datetime.now(timezone.utc),
                    freshness_note="LIVE government market-price response; exact market/date are taken from the returned record.",
                ),
            )
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as exc:
            return ToolResult(
                ok=False,
                error_code="MANDI_PROVIDER_ERROR",
                retryable=True,
                data={"detail": type(exc).__name__},
            )
