# Data provenance contract

Every factual tool response must carry a source name, source URL and retrieval timestamp. The orchestrator may explain a tool result but must not replace missing source data with an invented factual answer.

For demo data, the source note must explicitly say that it is simulated. Demo data must never be presented as a live government, market or weather observation.

Initial live weather adapter: Open-Meteo. Its forecast API supports geographic coordinates and hourly precipitation probability/temperature fields. See the current API documentation before changing parameters.

Mandi and government-scheme adapters remain provider-specific work items until the exact official endpoint/terms are verified.