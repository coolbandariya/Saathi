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

The current Exotel adapter supports outbound call initiation and signed webhook handling. A production phone conversation still needs Exotel's bidirectional Voice AI/WebSocket path wired to the same voice gateway.

Do not describe phone streaming as live until an actual call has completed the complete audio round trip.

## Safety boundary

The voice endpoint does not grant the model authority to invent prices, weather, eligibility, application status, or deadlines. Those answers must come from deterministic rules or a verified provider tool.
