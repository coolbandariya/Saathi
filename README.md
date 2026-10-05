# Saathi

**Your voice. Your language. Your companion.**

Saathi is a voice-first, multilingual assistance platform designed to make useful information and service workflows accessible through simple conversations. The project is built around one principle: field-ready workflows over disconnected AI demos.

## Current status

Foundation branch under review. The current build contains the responsive prototype UI, a typed FastAPI backend, deterministic intent-routing scaffolding, automated backend tests, CI, architecture/API documentation, and a staged implementation plan.

Live voice, telephony, scheme, OCR, farming-data, memory, and volunteer integrations are not yet claimed as complete. Anything simulated in a demo must be labeled DEMO or SIMULATED.

## Product direction

1. Voice-first access through phone or browser.
2. Hindi-first, with an adapter architecture for Indian languages and dialects.
3. Specialist workflows for schemes, farming, documents, and tasks.
4. Consent-based household memory and unfinished-task continuity.
5. Proactive reminders/callbacks only after explicit outbound consent.
6. Human volunteer fallback when automation is uncertain or requested.
7. Source-backed factual answers; the LLM is not the source of truth.

## Repository

- frontend/ — Next.js + React interface
- backend/ — FastAPI API and agent foundation
- docs/ — architecture, API contracts, build plan, and demo contract
- .github/workflows/ — backend test and frontend build gates

## Development

Requirements: Node.js 20+, Python 3.11+.

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

## Engineering playbook

- `docs/BUILD_PLAN.md` — implementation sequence
- `docs/ARCHITECTURE.md` — target runtime architecture
- `docs/API_CONTRACTS.md` — current HTTP contracts
- `docs/PROVIDER_MATRIX.md` — replaceable external-service strategy
- `docs/TEST_MATRIX.md` — quality gates
- `docs/REPO_GOVERNANCE.md` — definition of done and release gates
- `docs/DEMO_CONTRACT.md` — what the hackathon demo must actually prove
- GitHub Issues — major implementation workstreams

See the open foundation PR before starting parallel feature work.

## Hackathon

The project is being prepared for JAI 2026 and Tech Eximius 2.0. Submission claims will match functionality actually demonstrated by the submitted build.
