from datetime import datetime, timezone
import httpx
from .domain import SourceRef, ToolResult

class DataGovMandiAdapter:
    def __init__(self, resource_url: str | None = None, api_key: str | None = None, timeout: float = 6.0) -> None:
        self.resource_url = resource_url
        self.api_key = api_key
        self.timeout = timeout

    def price(self, commodity: str, market: str, state: str | None = None) -> ToolResult:
        if not commodity.strip() or not market.strip():
            return ToolResult(ok=False, message="Commodity and market are required.")
        if not self.resource_url or not self.api_key:
            return ToolResult(
                ok=False,
                message="Data.gov.in mandi resource is not configured.",
                sources=[SourceRef(name="Open Government Data Platform India", url="https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi")],
            )
        params={"api-key":self.api_key,"format":"json","limit":50,"filters[commodity]":commodity,"filters[market]":market}
        if state: params["filters[state]"]=state
        try:
            response=httpx.get(self.resource_url,params=params,timeout=self.timeout)
            response.raise_for_status()
            return ToolResult(ok=True,data=response.json(),sources=[SourceRef(name="Open Government Data Platform India",url="https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi",retrieved_at=datetime.now(timezone.utc))])
        except httpx.HTTPError as exc:
            return ToolResult(ok=False,message=f"Mandi provider unavailable: {exc.__class__.__name__}",sources=[SourceRef(name="Open Government Data Platform India",url="https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi")])
