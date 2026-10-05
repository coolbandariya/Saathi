# Saathi

**Your voice. Your language. Your companion.**

Saathi is a voice-first, multilingual assistance platform designed to make useful information and service workflows accessible through simple conversations. The project is built around one principle: field-ready workflows over disconnected AI demos.

## Current status

The active implementation branch contains the responsive prototype UI, typed FastAPI backend, deterministic routing, source-provenance contracts, a configurable live Open-Meteo adapter, a configurable government OGD/AGMARKNET mandi adapter, provider-gated browser voice (STT → agent → TTS), telephony/webhook contracts, rate-limited endpoints, operator control room, automated tests, CI configuration, and production/demo gates.

The current operator demo uses clearly labelled simulated mandi data and exposes a judge-mode golden flow, browser microphone capture, consent controls, source health, escalation state and correlation IDs. The backend has real Open-Meteo and configurable OGD/AGMARKNET adapters plus provider-gated Sarvam STT/TTS. Live Exotel bidirectional phone streaming, persistent Supabase memory, government scheme APIs, OCR and durable webhook storage remain provider-gated and are not claimed as complete.

**Operator demo:** run the frontend and open /dashboard.

## Product direction

1. Voice-first access through phone or browser.
2. Hindi-first, with an adapter architecture for Indian languages and dialects.
3. Specialist workflows for schemes, farming, documents, and tasks.
4. Consent-based household memory and unfinished-task continuity.
5. Proactive reminders/callbacks only after explicit outbound consent.
6. Human volunteer fallback when automation is uncertain or requested.
7. Source-backed factual answers; the LLM is not the source of truth.

## Repository

- frontend/ — Next.js + React interface and operator control room
- backend/ — FastAPI API, agent orchestration and provider boundaries
- docs/ — architecture, API contracts, build plan, voice contract, evaluation and release gates
- .github/workflows/ — backend test and frontend build gates

## Development

Requirements: Node.js 24+, Python 3.11+.

Frontend: cd frontend && npm install && npm run dev

Backend: cd backend && python -m venv .venv && pip install -r requirements.txt && pytest -q && uvicorn app.main:app --reload

Never commit .env files or secrets. Start from the provided .env.example files.

## Engineering rules

- Do not hard-code provider secrets.
- Do not fabricate eligibility, prices, weather, deadlines, or application status.
- Keep external providers behind replaceable adapters.
- Keep household data isolated with RLS.
- Use synthetic data for development and demos.
- Require explicit consent before storing memory or making outbound calls.
- Treat healthcare as informational/navigation support in the MVP.
- Do not merge failing required checks.
- Every factual tool result must carry provenance and retrieval time.
- Demo/simulated data must be explicitly labelled.

## Build roadmap

See docs/BUILD_PLAN.md for the milestone sequence and docs/ARCHITECTURE.md for the target runtime. GitHub Issues #11–#25 track the remaining implementation work.

## Hackathon

The project is being prepared for JAI 2026 and Tech Eximius 2.0. Submission claims will match functionality actually demonstrated by the submitted build.

### Backend readiness hardening

The current product branch also includes deterministic intent boundaries, policy-backed escalation decisions, optional caller-provided field location, degraded readiness reporting when provider contracts are absent, and webhook idempotency using a deterministic provider-event/body fingerprint. The webhook store is intentionally in-memory for the demo; production persistence still requires a durable repository such as Supabase.


## Real voice and data configuration

See docs/VOICE_RUNTIME.md, docs/REAL_DATA.md, docs/EVALUATION.md, and docs/JAI_SUBMISSION_CHECKLIST.md before recording a submission demo.
