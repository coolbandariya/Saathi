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
- [ ] LLM adapter
- [ ] LangGraph orchestration
- [ ] Scheme catalogue and deterministic eligibility rules
- [ ] Task/memory persistence

## Milestone 3 — Voice
- [ ] Browser voice mode
- [ ] STT adapter
- [ ] TTS adapter
- [ ] Exotel bidirectional voice integration

## Milestone 4 — Actions
- [ ] Document/OCR pipeline
- [ ] Weather tool
- [ ] Mandi tool
- [ ] Proactive scheduler
- [ ] Callback/resume workflow

## Milestone 5 — Human fallback
- [ ] Volunteer cases
- [ ] Realtime dashboard
- [ ] Assignment and resolution workflow

## Milestone 6 — Hardening
- [ ] RLS/security tests (database-backed)
- [x] Consent decision unit tests
- [ ] Integration tests
- [ ] End-to-end demo test
- [ ] Deployment verification


## Security foundation added
- Intent normalization is covered by regression tests.
- Consent decisions reject missing grants and invalid future timestamps.
- Webhook HMAC verification and duplicate-event rejection primitives are covered by unit tests.
- These are building blocks only; production webhook idempotency must be persisted in the database and use the exact provider signature contract.
