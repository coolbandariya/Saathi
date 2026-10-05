# Provider matrix

## Reasoning
Gemini Interactions API is the preferred reasoning adapter for the current implementation because it supports multi-turn state and agent/tool workflows. Keep it behind the ReasoningProvider protocol. The LLM may explain validated tool results but must not become the source of truth for factual government, market or weather data.

## Speech
BHASHINI exposes ASR and TTS capabilities and requires onboarding/API access for programmatic use. The repository therefore uses configured endpoint adapters rather than inventing undocumented request payloads. Endpoint details should be copied from the team's approved BHASHINI dashboard documentation, not hard-coded from guesses.

## Telephony
Exotel currently documents call-connect APIs, missed-call application settings, status callbacks and bidirectional Voicebot WebSocket streaming. The Exotel adapter is configuration-gated and must be tested against the team's actual account before being treated as live.

## Configuration rule
No API key is committed to source control. Provider construction returns no real provider when required credentials are missing.
