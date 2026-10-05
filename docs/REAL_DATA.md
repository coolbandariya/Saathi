# Real data path

## Weather

Saathi uses Open-Meteo when DEMO_MODE=false. The adapter records the queried coordinates and retrieval timestamp in the tool result provenance.

The default coordinates remain Sonipat only as a fallback context for the prototype. Production should use caller-provided or persisted consented location context.

## Mandi

Saathi includes a configurable Open Government Data adapter for the government commodity/market-price resource sourced through the OGD platform and AGMARKNET.

Configuration:

- MANDI_API_KEY
- MANDI_RESOURCE_ID (defaulted to the current OGD mandi resource: 9ef84268-d588-465a-a308-a864a43d0070)
- MANDI_API_BASE

The resource ID remains configurable even though the current catalogue resource is known. The adapter filters using the resource's current field IDs (`state.keyword`, `district`, `market`, `commodity`) and surfaces the returned `arrival_date` separately from retrieval time. This matters because the dataset is daily administrative market data, not a tick-by-tick live quote. The system refuses to present a demo price as live when the government adapter is not configured.

## What remains provider-gated

- government scheme catalogue / eligibility records
- persistent household memory
- durable webhook idempotency
- Exotel bidirectional voice streaming
- document OCR/storage
- human volunteer handoff

These are not faked in the demo.
