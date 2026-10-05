# Saathi Architecture Baseline

## Core principle

Saathi is a voice-first AI agent that remembers unfinished tasks and proactively helps users complete them. The MVP is one verified end-to-end workflow, not a collection of disconnected AI demos.

## Runtime flow

Phone/Web voice -> telephony or browser gateway -> STT -> orchestrator -> specialist tool boundary -> validated tools -> provenance -> TTS -> user.

Persistence is an optional P1 layer: when enabled, consented household memory/tasks are stored through repository interfaces and Supabase/RLS. The current non-Supabase runtime does not require Supabase.

## Provider adapters

External services must be isolated behind interfaces so they can be replaced without changing agent logic. Current implemented targets are Exotel for telephony, Sarvam Saaras/Bulbul for speech, optional Gemini tool routing, Open-Meteo for weather, and official government/agriculture data sources for factual answers. BHASHINI is an expansion path, not an implemented dependency.

## Safety boundaries

- LLM output is not a source of truth for eligibility, prices, weather, deadlines, or application status.
- Outbound calls require explicit consent and respect quiet hours.
- Secrets stay server-side.
- Household data is isolated with RLS.
- Healthcare is informational/navigation-only in the MVP; no autonomous diagnosis or prescribing.
- Demo data must be synthetic.
