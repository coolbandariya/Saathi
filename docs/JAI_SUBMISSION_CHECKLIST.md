# JAI 2026 submission checklist

## Product positioning

Primary track: NLP.

Secondary positioning: Open Innovation.

## Prototype story

Use one coherent 60–90 second story:

1. Farmer speaks in Hindi.
2. Saathi identifies farming intent.
3. Weather or mandi tool is called.
4. The response includes source and retrieval time.
5. Household context is shown only as consent-gated prototype state.
6. A human request triggers deterministic escalation.
7. If live voice is configured, the same story can begin from the microphone; phone AI is only shown if a real Exotel call has passed.

## Evidence to capture

- Git history showing the project was developed by the participating team.
- Exact commit SHA used for the submission.
- Working prototype URL.
- Demo video showing the exact submitted build.
- Provider configuration status without exposing secrets.
- Screenshots of source provenance, consent and escalation controls.
- Backend test output and frontend build/check output.
- Live tool response showing source and retrieval timestamp.

## Claims to avoid

Do not claim:

- live phone AI unless a real call is tested end-to-end;
- Haryanvi support without an audio/transcript benchmark;
- automatic scheme application submission without an authorized integration;
- persistent household memory while Supabase persistence is inactive;
- live mandi prices while the government resource/API key are absent;
- healthcare diagnosis or autonomous prescribing.

## Final technical gate

Before recording the final demo:

- [ ] pytest -q passes
- [ ] frontend lint passes
- [ ] frontend tsc --noEmit passes
- [ ] frontend npm run build passes
- [ ] /health/ready reports capability state accurately
- [ ] live weather query has provenance
- [ ] live mandi query has provenance, if enabled
- [ ] microphone loop works with configured STT/TTS
- [ ] if phone AI is claimed, real Exotel call completes audio round trip
- [ ] no secrets or real PII are committed
- [ ] final video and repository point to the same commit
