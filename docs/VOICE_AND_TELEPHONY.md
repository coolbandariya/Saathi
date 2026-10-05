# Voice and telephony contract

## MVP path
1. Provider receives a missed call or inbound call.
2. Provider webhook is authenticated and deduplicated.
3. Saathi resolves the household using a normalized phone number.
4. Consent is checked before memory, recording, or outbound actions.
5. Audio is transcribed by a replaceable STT provider.
6. The orchestrator selects a specialist agent.
7. Tools return structured data plus provenance.
8. TTS produces the response.
9. Call state and important events are persisted.

## Provider boundary
The application must not depend on provider-specific payloads outside the adapter layer.

## Production requirements
- exact provider signature validation
- durable webhook event IDs
- replay protection
- call-state persistence
- timeout/retry policy
- quiet hours for outbound calls
- explicit outbound consent
- opt-out
- recording consent
- redacted logs

## Demo mode
DEMO_MODE=true may use deterministic provider doubles. Demo responses must visibly identify simulated/fake data.
