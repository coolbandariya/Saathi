# Saathi Build Plan

## Phase A — completed on the non-Supabase branch

- Foundation FastAPI + Next.js
- Typed contracts and CI
- Provider ports + demo adapters
- Gemini adapter
- Orchestrator and intent routing
- Consent and quiet hours
- In-memory task repository
- Weather/mandi/scheme boundaries
- Document validation/review gate
- Volunteer state machine
- Exotel stream contract
- Interactive browser demo
- Unit/API tests

## Phase B — next, before Supabase

- Add a real STT/TTS adapter only after current provider contract is validated.
- Finish Exotel WebSocket session handling and media turn orchestration.
- Add document OCR adapter and fixture-based extraction tests.
- Expand scheme catalogue ingestion/versioning and required-document representation.
- Add farming response normalization and stale-data policy.
- Add 100–200 synthetic Hindi/Haryanvi utterance evaluation.
- Add end-to-end golden-path tests using only deterministic fixtures.
- Add dependency/security CI and production configuration checks.

## Phase C — Supabase

Only after Phase B is green:
- inspect live schema/RLS;
- implement repository adapters;
- wire consent, tasks, conversations, audit events;
- add tenant-isolation integration tests;
- replace in-memory demo persistence.

## Phase D — deployment

Only after the preceding phases are green:
- backend deployment;
- frontend deployment;
- secrets;
- provider webhooks;
- smoke tests;
- rollback procedure.
