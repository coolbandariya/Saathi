# Real data path

## Weather

Saathi uses Open-Meteo when DEMO_MODE=false. The adapter records the queried coordinates and retrieval timestamp in the tool result provenance.

The default coordinates remain Sonipat only as a fallback context for the prototype. Production should use caller-provided or persisted consented location context.

## Mandi

Saathi includes a configurable Open Government Data adapter for the government commodity/market-price resource sourced through the OGD platform and AGMARKNET.

Configuration:

- MANDI_API_KEY
- MANDI_RESOURCE_ID
- MANDI_API_BASE

The resource ID is intentionally configuration because data.gov.in resource identifiers can differ by dataset/resource version. The system refuses to present a demo price as live when the government adapter is not configured.

## What remains provider-gated

- government scheme catalogue / eligibility records
- persistent household memory
- durable webhook idempotency
- Exotel bidirectional voice streaming
- document OCR/storage
- human volunteer handoff

These are not faked in the demo.
