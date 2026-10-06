# Saathi Build Plan

## Current release state

The non-Supabase runtime is consolidated on the active implementation branch. The browser demo, deterministic routing, provenance contracts, Open-Meteo adapter, configurable OGD/AGMARKNET adapter, Sarvam browser STT/TTS adapters, current Document AI adapter, executable Exotel WebSocket boundary, bounded-turn phone speech adapter, consent UI, escalation policy, webhook HMAC/idempotency contract, tests and CI configuration are implemented.

The remaining work before Supabase is intentionally narrow: run the configured providers for real, measure the vertical slice, and prove the exact submitted build.

## P0 — Non-Supabase completion

**Current state:** engineering gates are green, but provider-backed execution and submission evidence are still required. Do not move to Supabase until the real vertical slice is captured.

- [x] Responsive landing page + operator dashboard
- [x] Browser microphone capture path
- [x] Deterministic Hindi/Hinglish intent baseline
- [x] 120-case synthetic intent benchmark
- [x] Source provenance + demo/live labelling
- [x] Consent and human-escalation UI
- [x] Capability-aware readiness endpoint
- [x] Current OGD/AGMARKNET field/resource contract
- [x] Current Sarvam Document AI job lifecycle
- [x] Exotel AgentStream media primitives
- [x] Executable Exotel WebSocket route
- [x] Bounded-turn phone STT → orchestrator → TTS adapter
- [x] Sarvam Realtime STT WebSocket transport with VAD and keyterms
- [x] Sarvam streaming TTS WebSocket transport with cancellation-aware barge-in
- [x] Gemini structured tool-call boundary with allow-listed tool validation
- [x] Frontend lint/typecheck/build and dependency-audit workflow
- [ ] Run provider-backed browser voice with real Sarvam credentials and record transcript/audio latency
- [ ] Query live Open-Meteo and capture provenance in the submitted environment
- [ ] Query live OGD/AGMARKNET and verify market/date/entity selection; report it as a daily government observation
- [ ] Run a real Exotel call against a public `wss://` deployment
- [ ] Measure speech WER, intent/entity/tool accuracy, grounded-answer correctness and end-to-end latency
- [ ] Record the exact submitted build/commit and preserve Git evidence
- [ ] Produce one reproducible judge-mode runbook that works even if an external provider temporarily fails

## P1 — Persistence and human workflow

**Do not start P1 until the JAI prototype submission is frozen and the provider-backed vertical slice is demonstrated.**

After the non-Supabase release gate passes:

1. Connect Supabase through repository interfaces.
2. Apply and audit RLS with multiple households.
3. Replace in-memory webhook idempotency with durable storage.
4. Add a durable volunteer case record: assignment, status, notes and resolution.
5. Add consented household memory and task/reminder persistence with quiet hours.
6. Add document metadata/storage persistence without storing unnecessary sensitive content.
7. Add integration tests for tenant isolation and consent enforcement.

## P2 — Low-latency phone runtime

The realtime transport is now implemented behind `SARVAM_REALTIME_STT_ENABLED=false` by default. Remaining work is provider/deployment verification:

1. Run Sarvam Realtime STT against a real key and verify VAD/final events.
2. Run streaming TTS and verify Linear16 output at the Exotel rate.
3. Run a real Exotel call against a public `wss://` deployment.
4. Add reconnect/failover behavior and call-level observability.
5. Measure first partial, final transcript, first audio and turn-complete latency.
6. Only claim live phone AI after a real call completes the full round trip.

## P3 — Factual depth and language robustness

- Build a versioned government scheme catalogue with source URL, effective date and deterministic eligibility rules.
- Add verified mandi market/date/entity selection instead of taking the first record blindly.
- Add weather caching and explicit consented location provenance.
- Expand evaluation to 300–500 synthetic utterances plus recorded/synthetic audio fixtures.
- Benchmark noisy Hindi/Hinglish and Haryanvi-accented Hindi before making dialect claims.
- Add document confidence/field-source handling before any automated downstream action.

## Explicitly avoid

- generic agent proliferation without a user-facing workflow
- unverified Haryanvi support
- generic RAG as a substitute for authoritative government data
- fake GPS, fake payments or fake application submission
- autonomous medical diagnosis/prescribing
- heavy visual effects that distract from the voice-to-action story

## Release gate

A submission build is ready only when:

- backend tests pass
- frontend lint, typecheck and build pass
- readiness accurately reports configured capabilities
- at least one live factual tool has provenance
- browser voice works with configured STT/TTS
- if phone AI is claimed, a real Exotel call completes the round trip
- no secrets or real PII are committed
- the demo video shows the same build/commit being submitted
