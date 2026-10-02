# Saathi

**Your voice. Your language. Your companion.**

Saathi is a voice-first, multilingual assistance platform designed to help people access useful services through simple conversations. The initial prototype focuses on Hindi voice interaction, scheme assistance, consent-based household continuity, and a responsive volunteer dashboard.

## Project status

Early development. Integrations and workflows are added incrementally; features are not considered live until implemented and tested.

## Repository structure

- `frontend/` — Next.js web experience
- `backend/` — FastAPI services and agent orchestration
- `supabase/` — database migrations and seed data
- `docs/` — architecture, setup, and demo notes

## Local development

Requirements:
- Node.js 20+
- Python 3.11+
- A Supabase project
- An LLM API key (optional for the first UI milestone)
- Bhashini credentials (optional until voice integration)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to the relevant local environment file and fill in credentials. Never commit secrets.

## Safety and privacy

- Obtain clear consent before storing household information or sending reminders.
- Collect only information needed for the requested workflow.
- Keep privileged keys server-side.
- Treat scheme eligibility as a rules-based, source-backed check.
- Do not use the prototype as a substitute for professional medical advice.
- Use synthetic data during development and demos.

## Team

Four-person team. Add each member's name and contribution before submission.

## Hackathon deliverables

The project is being developed for JAI 2026 and Tech Eximius 2.0. Submission claims will reflect the functionality actually demonstrated in the submitted build.
