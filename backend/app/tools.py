from .domain import SourceRef, ToolResult

class WeatherTool:
    name = "weather.get_forecast"
    def get_forecast(self, location: str) -> ToolResult:
        if not location.strip():
            return ToolResult(ok=False, message="Location is required.")
        return ToolResult(ok=False, message="Live weather provider is not configured.", sources=[SourceRef(name="Open-Meteo", url="https://open-meteo.com/en/docs")])

class MandiTool:
    name = "mandi.get_price"
    def get_price(self, commodity: str, market: str) -> ToolResult:
        if not commodity.strip() or not market.strip():
            return ToolResult(ok=False, message="Commodity and market are required.")
        return ToolResult(ok=False, message="Live mandi provider is not configured.", sources=[SourceRef(name="Validated agriculture data source")])

class SchemeTool:
    name = "scheme.check"
    def check(self, scheme_id: str, profile: dict) -> ToolResult:
        if not scheme_id:
            return ToolResult(ok=False, message="scheme_id is required.")
        return ToolResult(ok=False, message="Verified scheme catalogue is not connected yet.", sources=[SourceRef(name="Official scheme catalogue")])
