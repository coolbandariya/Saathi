# Saathi — Next-stage technical research

Updated: 2026-10-06

## Executive decision

Do not add more generic agents yet. The next milestone should be one measured, real vertical slice:

caller speech -> language/intent -> specialist tool -> grounded response -> spoken audio -> observable result.

The strongest improvement is to make every step real, measurable and replaceable before adding breadth.

## What current provider research changes

### Voice runtime

Sarvam's current Realtime STT endpoint is the preferred direction for a production phone agent. It provides interim and final transcripts, server-side VAD, mid-call configuration updates and explicit audio-input events; `saaras:v4` is supported on the Realtime endpoint. For browser turn capture, the REST STT endpoint accepts WebM, so the current browser path can stay REST-based while the phone path moves to Realtime.

Exotel AgentStream provides bidirectional WebSocket audio using raw mono 16-bit Linear16 PCM at 8, 16 or 24 kHz. A public wss:// endpoint is required for a real phone connection.

Implication:

- keep the current Exotel protocol boundary
- replace the bounded REST speech adapter with a realtime STT/TTS transport next
- use provider VAD for turn detection rather than adding a second VAD blindly
- implement barge-in by clearing outbound Exotel audio when caller speech starts (`clear` event)
- add reconnect/failover handling and call-level correlation IDs
- use Saaras v4 keyterms for high-value places/commodities where recognition errors are costly
- measure TTFT/TTFA, end-of-turn latency and dropped-session rate

### Document AI

Sarvam's current Document AI uses /doc-ai/v1 job APIs. Digitise is for full-document OCR/layout; Extract is for schema-defined fields. The current adapter therefore stays job-based and should not be mixed with the legacy document-intelligence API.

Next:

- add consented upload endpoint
- add status/result polling
- persist only metadata initially
- expose field confidence and source page
- never trigger a downstream application action directly from OCR output

### Gemini orchestration

Gemini Interactions API is the current API for new agentic/tool workflows. Function calls are returned as structured steps; Saathi must execute them locally and return function results. The model is not the factual authority.

Next:

- use Gemini only for ambiguous routing/planning
- allow-list tools
- validate arguments
- execute tools locally
- send tool results back for final phrasing
- keep deterministic intent/rules as the fallback
- set stateless behavior for sensitive prototype requests unless server-side state is intentionally required

## Product priority order

### P0 — prove the core

1. Real Sarvam browser voice.
2. Real Open-Meteo query with provenance.
3. Real OGD/AGMARKNET query with exact commodity/district/market/date.
4. Real Exotel call using a public deployment.
5. Measure the full chain.

### P1 — make the chain resilient

1. Realtime STT/TTS.
2. Barge-in and playback cancellation.
3. Provider timeout/retry/circuit-breaker policy.
4. Structured error taxonomy.
5. Call/session correlation.
6. Observability dashboard with latency and failure counters.
7. Synthetic audio fixtures for regression testing.

### P2 — persistence

Only after the above is stable:

1. Supabase repositories behind interfaces.
2. Household isolation/RLS tests.
3. Consent enforcement at the repository boundary.
4. Durable webhook idempotency.
5. Volunteer handoff cases.
6. Task/reminder state and quiet hours.

### P3 — breadth

1. Versioned scheme catalogue.
2. Document workflows.
3. More commodities/markets.
4. Noisy Hindi/Hinglish benchmark.
5. Haryanvi benchmark before claiming Haryanvi support.

## Provider contract notes (verified 2026-10-06)

- Sarvam REST STT accepts WebM and supports `saaras:v4`; this matches the browser `MediaRecorder` path.
- Sarvam Realtime STT is the better production voice-agent transport because it exposes partial transcripts and millisecond VAD controls.
- Exotel Voicebot sessions use raw mono Linear16 PCM and support bidirectional `media`, `mark`, and `clear`; `clear` is the required primitive for barge-in playback cancellation.
- Sarvam Bulbul v3 REST returns base64 audio and supports WAV/telephony codecs; Saathi currently uses WAV for browser playback and should use an 8 kHz telephony codec when the phone path is finalized.

## Evaluation plan

A credible demo should report numbers, not only feature names.

Minimum benchmark:

- intent accuracy
- farming entity accuracy
- tool-selection accuracy
- grounded-answer correctness
- escalation precision/recall
- speech WER/CER
- time to first transcript
- time to first audio
- complete turn latency
- provider failure rate
- successful end-to-end call rate

Use synthetic/redacted audio and text. Never place Aadhaar, real phone numbers, private medical documents or household secrets in fixtures.

## Agent design rule

The LLM can decide:

- which declared specialist/tool is appropriate
- what parameters are needed
- how to phrase a result

The LLM cannot decide:

- the current mandi price
- the current weather
- government eligibility
- application status
- medical diagnosis
- whether consent exists

Those must come from deterministic policy, verified tools or persisted authorization state.

## Hackathon strategy

JAI 2026 explicitly emphasizes an already-developed working prototype and a short demonstration that establishes the team's development ownership. The project should therefore show a coherent existing implementation and Git evidence rather than a last-minute collection of disconnected screens.

JAI's official summit page places the final hackathon activity on 30–31 October 2026 and lists NLP and Open Innovation among the core tracks.

Tech Eximius 2.0 asks for a maximum-six-slide submission with repository, prototype and demo links on the first slide, followed by problem, solution, features/workflow, stack, USP and impact. Its evaluation emphasizes innovation, implementation, impact, scalability/feasibility and presentation.

Therefore the demo should optimize for:

1. one memorable user story
2. one technically impressive live chain
3. visible source/provenance
4. explicit safety/consent
5. measurable engineering evidence
6. a clean repository and reproducible setup

## What not to build next

- generic RAG without authoritative sources
- additional agents that only produce text
- blockchain/payment features unrelated to the core user journey
- fake GPS or fake live telephony
- autonomous government application submission without an authorized integration
- medical diagnosis/prescribing
- decorative 3D effects that consume build time without improving the demo

## Research sources

- Sarvam realtime STT: https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming
- Sarvam Pipecat production guide: https://docs.sarvam.ai/api/integration/pipecat-production-guide
- Sarvam Exotel voice-agent guide: https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel
- Sarvam Document AI: https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview
- Google Gemini models: https://ai.google.dev/gemini-api/docs/models
- Google Gemini Interactions API: https://ai.google.dev/gemini-api/docs/interactions-overview
- Google Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling
- Exotel AgentStream protocol: https://developer.exotel.com/docs/agentstream/websocket-protocol
- Exotel Connect Voice AI: https://developer.exotel.com/docs/agentstream/connect-voice-ai
- OGD/AGMARKNET daily mandi resource: https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi
- JAI 2026: https://www.jiityouthclub128.in/
- Tech Eximius 2.0: https://unstop.com/hackathons/tech-eximius-20-tech-circle-1755763/
