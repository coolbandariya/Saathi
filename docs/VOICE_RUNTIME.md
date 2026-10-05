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

The frontend microphone control uses this endpoint. It is intentionally provider-gated: without a configured speech provider the UI reports the provider error instead of simulating a live call.

## Current provider contract

The first real adapter is Sarvam:

- STT: Saaras v4
- TTS: Bulbul v3
- Hindi code: hi-IN
- Browser audio: WebM upload
- TTS response: base64 audio returned by the API

The provider key is server-side only. Never put SARVAM_API_KEY in NEXT_PUBLIC_* variables.

## Phone path

The Exotel adapter now includes the bidirectional Connect Voice AI call contract (`StreamUrl` + `StreamType=bidirectional`). The actual WebSocket media endpoint remains deployment-gated, but the target protocol is now explicit: Exotel AgentStream opens the configured `wss://` StreamUrl with bidirectional audio; the server must relay the negotiated 8/16/24 kHz Linear16 PCM to a realtime STT transport and return raw phone-compatible audio. Sarvam's current Realtime STT (`saaras:v3-realtime`, with `saaras:v4` also supported) is the preferred live STT path; its WebSocket accepts base64 `audio_input` messages and emits `transcript.partial` / `transcript.final` events. Do not claim this path is live until a real Exotel call completes the audio round trip.

Do not describe phone streaming as live until an actual call has completed the complete audio round trip.

## Safety boundary

The voice endpoint does not grant the model authority to invent prices, weather, eligibility, application status, or deadlines. Those answers must come from deterministic rules or a verified provider tool.


## Current external-provider findings

- Sarvam REST STT supports short clips up to 30 seconds; Realtime STT is the correct transport for a phone voice agent.
- Sarvam TTS Bulbul v3 supports WAV and phone-oriented codecs; browser voice keeps WAV, while a future Exotel bridge should request phone-compatible raw Linear16 and strip any container before streaming.
- Exotel Connect Voice AI uses HTTP Basic Auth and `StreamType=bidirectional`; `StreamUrl` must be a reachable WebSocket endpoint.
- The repository therefore keeps live phone credentials and public deployment outside CI and outside the demo-mode path.
