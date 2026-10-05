# Saathi voice runtime

## Browser voice loop

The /api/v1/voice/turn endpoint accepts a short browser-recorded audio file and returns:

1. transcript
2. deterministic specialist intent
3. verified tool result when available
4. source provenance
5. optional synthesized Hindi audio
6. escalation metadata
7. correlation ID

The frontend microphone control uses this endpoint. It is provider-gated: without a configured speech provider the UI reports the provider error instead of simulating a live call.

## Phone voice loop

The repository exposes /api/v1/telephony/stream as a FastAPI WebSocket endpoint for Exotel AgentStream. It accepts Exotel connected, start, media and stop events and sends bidirectional media frames containing raw mono Linear16 PCM.

The endpoint now supports two explicit modes. The default bounded-turn adapter remains available as a safe fallback. When `SARVAM_REALTIME_STT_ENABLED=true`, Exotel PCM is streamed to Sarvam Realtime STT with server VAD and final transcript events; replies are synthesized through Sarvam streaming TTS and streamed back to Exotel. Barge-in cancels the active response and sends Exotel `clear`.

The realtime path is implemented but provider/deployment verification is still required before calling it a live production phone agent. Exotel AgentStream sends raw 16-bit mono Linear16 PCM at 8/16/24 kHz; the realtime Sarvam STT path currently accepts 8/16 kHz and the TTS path emits Linear16 at the negotiated rate.

Do not claim live phone AI until a real Exotel call has completed the complete audio round trip on a deployed public wss:// endpoint.

## Provider configuration

- STT: Sarvam Saaras v4 by default
- TTS: Sarvam Bulbul v3 by default
- Hindi code: hi-IN
- Browser audio: WebM upload
- Phone audio: raw Linear16 PCM
- Provider key: server-side only

Sarvam documents linear16 output and 8 kHz telephony sample rates for voice pipelines.

## Safety boundary

The voice endpoint does not grant the model authority to invent prices, weather, eligibility, application status or deadlines. Those answers must come from deterministic rules or a verified provider tool.
