# Saathi Build Plan

## Current release state

The repository is consolidated on `main`. There are no open pull requests. The browser demo, deterministic routing, provenance contracts, Open-Meteo adapter, configurable government mandi adapter, Sarvam browser STT/TTS adapters, consent UI, escalation policy, webhook HMAC/idempotency contract, tests and CI are implemented.

The remaining work is deliberately ordered around one reliable vertical slice rather than adding more agents or dashboard features.

## P0 — JAI prototype reliability (before submission)

- [x] Consolidate stacked PR history into `main`
- [x] Responsive landing page + operator dashboard
- [x] Browser microphone capture path
- [x] Deterministic Hindi/Hinglish intent baseline
- [x] Source provenance + demo/live labelling
- [x] Consent and human-escalation UI
- [ ] Green backend + frontend CI on the final commit
- [ ] Run the browser voice loop with real Sarvam credentials
- [ ] Query live Open-Meteo and capture provenance
- [ ] Configure a real OGD/AGMARKNET resource and verify Sonipat/Wheat records
- [ ] Expand the evaluation set and measure speech/intent/tool accuracy and latency
- [ ] Record the exact submitted build and preserve Git evidence

## P1 — Make the vertical slice production-shaped

1. Supabase: reactivate the project or provision capacity; apply migrations; test RLS with multiple households.
2. Replace in-memory webhook idempotency with a durable store.
3. Replace the thin Gemini adapter with structured tool calls/state, keeping factual tools authoritative.
4. Implement a real volunteer handoff case record with assignment, status and resolution.
5. Add document upload/OCR with explicit consent and safe extraction.
6. Add task/reminder persistence only after consent and quiet-hour rules are enforced.
7. Add automated browser/API integration tests for the complete voice-to-tool path.

## P2 — Phone-first runtime

1. Implement the public Exotel `wss://` media endpoint.
2. Decode/validate inbound audio frames and connect them to realtime STT/TTS.
3. Test missed-call -> callback -> speech -> tool -> spoken response end to end.
4. Verify provider signatures/webhooks and durable deduplication.
5. Only then claim live phone AI in the submission.

## P3 — Language and factual depth

- Benchmark Hindi vs noisy/Hinglish speech.
- Benchmark Haryanvi-accented Hindi before making any Haryanvi support claim.
- Build a versioned government scheme catalogue with deterministic eligibility rules.
- Add verified mandi date/market/entity handling rather than returning the first matching record.
- Add weather caching and location provenance where consented location is available.

## Explicitly do not add yet

- More generic agents
- Blockchain/NFT features
- Fake GPS
- Fake payments
- Unverified Haryanvi support
- Generic RAG without an authoritative source
- Heavy 3D/visual effects
- A public control centre or admin surface

## Release gate

A submission build is ready only when:
- frontend build passes
- backend tests pass
- readiness reflects actual provider configuration
- at least one live factual tool has provenance
- browser voice works with configured STT/TTS
- no secrets or real PII are committed
- the demo video shows the same build/commit being submitted
