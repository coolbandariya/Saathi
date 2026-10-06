# Saathi — National Hackathon Pitch & Demo Plan

Updated: 2026-10-06

## Core rule

Only demonstrate what the repository and live providers can prove.

Saathi's strongest story is:

> Speak naturally. Get verified help.

Technical proof:

> The model can choose a declared action; it cannot invent the evidence.

## 3-minute live pitch

### 0:00–0:20 — Hook

Do not open with architecture slides.

Say:

> A user should not need a smartphone, a complicated portal, or perfect Hindi to get useful public information. Saathi lets them speak naturally and answers only when it can verify the result.

### 0:20–1:25 — Voice wow moment

Preferred production demo:

1. Place the phone on speaker.
2. Trigger a real Exotel call or use the configured live voice entry point.
3. Say: "Kal Sonipat mein गेहूं ka mandi bhav kya hai? Baarish ka chance bhi batao."
4. Show the live transcript.
5. Show farming intent, Wheat / Haryana / Sonipat, mandi tool, weather tool, and source/observation time.
6. Let Saathi answer in Hindi.

Never use a fake ringing animation if a real call is being claimed. If the provider is unavailable, switch to explicit DEMO mode and say so.

## The proactive-action demo

The product vision includes persistent household tasks and proactive callbacks, but Supabase persistence is intentionally deferred until the provider-backed vertical slice is frozen.

### Live persistence state

Only use this after a real database-backed task exists.

Flow:
missing document → user consent → task persisted → scheduler → outbound call → completion

### Proof-mode simulation

Use a clearly labelled operator-only simulation:

Create follow-up → SIMULATION / NO EXTERNAL CALL → Simulate 3 days later → task becomes due → callback workflow is displayed

The button must never be presented as production persistence.

The winning line is:

> This is the same workflow we will persist server-side; today's proof mode removes the database dependency so the core agent can be judged independently.

Do not claim persistent memory until the database-backed state is actually persisted and read back.

## Safety moment

Use one short deliberate failure:

> Mandi ka bhav batao.

Saathi asks for the missing commodity and location instead of guessing.

If a future healthcare route is added, it must refuse diagnosis/prescription and escalate uncertain cases. Do not call the current product a healthcare agent unless that route is actually implemented and tested.

## Agentic defense

Avoid saying multi-agent unless there are independently defined specialist policies/agents.

For the current prototype, describe the architecture as:

speech → intent/entity layer → specialist tool boundary → authoritative API → provenance → response policy → voice

If a planner is enabled, show:

planner decision → allow-listed tool → tool result → grounded response

The LLM is a planner/router, not the factual source.

## Government language stack

Saathi currently uses Sarvam for speech in the implemented prototype.

BHASHINI is a credible government language-infrastructure integration path, but do not put Bhashini-powered on a slide until a real BHASHINI API path is configured and exercised.

A safe slide label is:

> Indic language stack: Sarvam today · BHASHINI-compatible expansion path

## 2-minute video

0:00–0:30 — real voice interaction, if live provider credentials are available.

0:30–1:00 — transcript → intent → entities → tool selection → source.

1:00–1:30 — missing-input/failure-safe interaction and explicit demo/live boundary.

1:30–1:50 — proactive workflow. Label simulation if persistence is not yet live.

1:50–2:00 — human escalation, repository, and one measured metric.

## Slide plan

### Slide 1 — Saathi

Speak naturally. Get verified help.

Include team, GitHub, working prototype, and demo link/video.

### Slide 2 — Problem

Use sourced, defensible language:
- voice is easier than complex portals for many users
- Indic-language/code-mixed interaction is under-served by rigid workflows
- public-data answers require freshness and provenance

Avoid unsupported 500M+ locked out claims.

### Slide 3 — Solution

Voice → Understand → Verify → Act → Escalate

Three pillars:
- Hindi/Hinglish voice
- verified specialist tools
- human fallback

### Slide 4 — Architecture

Exotel → PCM → Sarvam Realtime STT → Saathi routing → OGD/Open-Meteo → provenance → Sarvam TTS → Exotel

Side branch:
low confidence / unsafe / provider failure → human

### Slide 5 — Why it is not a wrapper

Show evidence:
- deterministic entity extraction
- allow-listed tool boundary
- authoritative source contracts
- source timestamps/freshness notes
- regression tests
- latency and accuracy measurements

### Slide 6 — Impact and scale

- phone-first access
- reusable provider adapters
- additional Indian languages
- government/public-data connectors
- consent-led persistence
- human escalation

## Judge questions

### Is this just an LLM wrapper?

Answer:

> No. The model does not supply the facts. Saathi extracts structured entities, selects only declared tools, executes them server-side, attaches provenance, and refuses to answer when the authoritative tool cannot verify the result.

### Where is your multi-agent system?

Answer:

> We intentionally avoid cosmetic multi-agent claims. The current prototype has specialist tool boundaries. If a planner is enabled, it selects among those declared capabilities; the execution layer remains deterministic.

### Why not Bhashini?

Answer:

> Our current working speech path is Sarvam because it gives us the realtime transport and Indic code-mix support we can actually demonstrate. BHASHINI is an integration target, not a logo we claim without a working API path.

### Where is memory?

Answer:

> Persistent memory is a consented database capability, not browser state. We are freezing the provider-backed voice/data vertical slice before adding persistence, so the demo never confuses simulation with production state.

## Non-negotiable demo labels

Use:
- LIVE
- DEMO
- SIMULATION
- API READY
- PROVIDER NOT CONFIGURED

Never use:
- LIVE for mock data
- CONNECTED for a simulated phone call
- MEMORY SAVED without database persistence
- CALLBACK SENT unless the provider confirms it
