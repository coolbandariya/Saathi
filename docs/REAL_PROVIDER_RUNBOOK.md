# Saathi real-provider runbook

Updated: 2026-10-06

This is the final non-Supabase verification sequence. Run it against the exact commit intended for submission.

## 1. Backend

Set:
- DEMO_MODE=false
- SARVAM_API_KEY
- SARVAM_REALTIME_STT_ENABLED=true for realtime phone verification
- GEMINI_API_KEY only if reasoning is being demonstrated
- MANDI_API_KEY
- MANDI_RESOURCE_ID
- CORS_ORIGINS to the deployed frontend origin

Then verify:
- GET /health/live
- GET /health/ready
- POST /api/v1/agent with a fully specified farming request
- POST /api/v1/agent with the combined golden request: mandi price + next-24h rain
- POST /api/v1/agent with an underspecified farming request
- POST /api/v1/agent with a farmer-scheme request

The response must expose correlation_id, tool_name, latency_ms, and source provenance where a factual tool was used.

## 2. Browser voice

Use the dashboard microphone with a Hindi/Hinglish utterance.

Record:
- transcript
- intent
- extracted entities
- source
- turn latency
- spoken response

Saaras REST accepts WebM and is capped at 30 seconds per request; the browser path therefore remains a bounded-turn verification path. For true live voice-agent behavior, use Sarvam Realtime STT.

## 3. Realtime phone

Configure a public wss:// Exotel AgentStream endpoint and run a real call.

Do not call the feature realtime in submission material until the call completes:
caller audio -> Exotel -> Saathi -> STT -> agent -> TTS -> Exotel -> caller.

Capture:
- call/session ID
- first partial transcript timestamp
- final transcript timestamp
- transcript
- p50/p95 turn latency
- first audio latency
- provider failures
- barge-in behavior

## 4. Golden failure tests

Demonstrate all three:
1. मंडी का भाव बताओ -> asks for missing crop/location instead of guessing.
2. provider mismatch/no record -> refuses to present unverified data.
3. मुझे इंसान से बात करनी है -> deterministic human escalation.

## 5. Submission freeze

Freeze one commit and use that same commit for:
- deployed prototype
- GitHub repository
- demo recording
- benchmark report
- PPT
- JAI submission

Never record a demo from one build and submit another.
