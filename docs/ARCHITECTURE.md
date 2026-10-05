# Saathi Architecture Baseline

## Core principle

Saathi is a voice-first AI agent that remembers unfinished tasks and proactively helps users complete them. The MVP is one verified end-to-end workflow, not a collection of disconnected AI demos.

## Runtime flow

Phone/Web voice -> telephony or browser gateway -> STT -> orchestrator -> specialist agent -> validated tools -> Supabase memory/tasks -> TTS -> user.

## Provider adapters

External services must be isolated behind interfaces so they can be replaced without changing agent logic. Initial targets are Exotel for Indian telephony, Bhashini/Whisper for speech, Gemini/local model for reasoning, Supabase/Postgres/pgvector for persistence, Open-Meteo for weather, and official government/agriculture data sources for factual answers.

## Safety boundaries

- LLM output is not a source of truth for eligibility, prices, weather, deadlines, or application status.
- Outbound calls require explicit consent and respect quiet hours.
- Secrets stay server-side.
- Household data is isolated with RLS.
- Healthcare is informational/navigation-only in the MVP; no autonomous diagnosis or prescribing.
- Demo data must be synthetic.
