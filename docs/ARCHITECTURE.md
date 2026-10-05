# Saathi Architecture

## Runtime boundary

Phone/Web voice -> telephony/browser gateway -> STT -> orchestrator -> specialist tool -> safe response -> TTS.

Persistence is a separate port: the current branch uses an in-memory repository only for deterministic tests/demo. Supabase is deliberately not connected yet.

## Completed non-Supabase foundation

- Typed FastAPI contracts with request IDs.
- Deterministic intent routing and orchestrator.
- Replaceable LLM/STT/TTS provider protocols.
- Gemini adapter with lazy SDK import.
- Demo provider mode with no external network requirement.
- Consent/quiet-hour policy functions.
- In-memory task repository with household isolation at the repository boundary.
- Weather adapter for Open-Meteo.
- Configurable Data.gov.in/AGMARKNET mandi adapter.
- Source-backed PM-USP scheme eligibility evaluator.
- Document upload validation and confidence review gate.
- Volunteer support case state machine.
- Exotel Voicebot event parser, replay guard, signature helper, and outbound Voice AI client.
- Backend unit/API test coverage for these boundaries.
- Interactive browser demo that calls the FastAPI conversation endpoint.

## Source-of-truth rule

LLMs explain results; they do not invent eligibility, weather, mandi prices, deadlines, application status, or medical advice. Factual tools return source metadata and an explicit stale/error state.

## Next integration seam

The Supabase repository will implement the existing MemoryStore contract. It must preserve household isolation, consent enforcement, auditability, and RLS; no agent code should import Supabase directly.
