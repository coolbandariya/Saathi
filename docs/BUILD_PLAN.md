# Saathi Build Plan

## Milestone 1 — Foundation
- [x] Repository scaffold
- [x] Backend health endpoint
- [x] Typed conversation request/response
- [x] Deterministic intent-routing placeholder
- [x] Backend smoke tests
- [ ] Supabase migrations reviewed and tested

## Milestone 2 — Core agent
- [x] Provider interfaces
- [x] Agent orchestrator foundation
- [x] Tool provenance contract
- [x] Intent smoke benchmark
- [ ] LLM adapter
- [ ] LangGraph or equivalent durable orchestration
- [ ] Scheme catalogue and deterministic eligibility rules
- [ ] Task/memory persistence

## Milestone 3 — Voice
- [x] Telephony adapter boundary
- [x] Webhook HMAC primitive
- [ ] Browser voice mode
- [ ] STT adapter
- [ ] TTS adapter
- [ ] Exotel inbound/missed-call integration
- [ ] Exotel bidirectional voice integration

## Milestone 4 — Actions
- [x] Live Open-Meteo adapter contract
- [ ] Verified mandi adapter
- [ ] Verified scheme catalogue
- [ ] Document/OCR pipeline
- [ ] Proactive scheduler
- [ ] Callback/resume workflow

## Milestone 5 — Human fallback
- [ ] Volunteer cases
- [ ] Realtime dashboard
- [ ] Assignment and resolution workflow

## Milestone 6 — Hardening
- [ ] RLS/security tests against the live database
- [x] Consent decision unit tests
- [x] Tool provenance tests
- [x] Webhook HMAC unit tests
- [ ] Durable webhook idempotency
- [ ] Integration tests
- [ ] End-to-end demo test
- [ ] Load/latency tests
- [ ] Deployment verification

## Release principle
Build one complete vertical slice first: phone -> speech -> orchestrator -> verified tool -> source-backed response -> memory/task -> speech. Do not expand the number of agents until that slice is reliable.
