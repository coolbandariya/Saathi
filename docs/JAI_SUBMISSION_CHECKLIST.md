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
5. Household context is preserved only when consent is enabled.
6. A human request triggers deterministic escalation.

## Evidence to capture

- Git history showing the project was developed by the participating team.
- Working prototype URL.
- Demo video showing the exact submitted build.
- Provider configuration status.
- Screenshots of source provenance and consent controls.
- Test results from the submitted commit.

## Claims to avoid

Do not claim:
- live phone AI unless a real call is tested end-to-end;
- Haryanvi support without a benchmark;
- automatic scheme application submission without an authorized integration;
- persistent memory while Supabase is inactive;
- live mandi prices while MANDI_RESOURCE_ID / MANDI_API_KEY are absent;
- healthcare diagnosis or autonomous prescribing.

## Final technical gate

Before recording the final demo:

- [ ] pytest -q passes
- [ ] frontend npm run build passes
- [ ] /health/ready reflects actual provider configuration
- [ ] live weather query has provenance
- [ ] live mandi query has provenance, if enabled
- [ ] microphone loop works with configured STT/TTS
- [ ] no secrets or real PII are committed
