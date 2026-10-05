# Production gates

A Saathi release is not production-ready until all of these are true:

- [ ] Supabase schema and RLS reviewed against the actual live project
- [ ] household isolation integration tests pass
- [ ] durable webhook idempotency exists
- [ ] exact telephony signature contract tested
- [ ] real STT/TTS adapters tested
- [ ] tool results carry source and retrieval timestamps
- [ ] outbound calling requires stored consent and quiet-hours checks
- [ ] documents use private storage and expiring access
- [ ] secrets are absent from source control
- [ ] rate limits are enforced by a shared production store
- [ ] logs redact phone numbers and sensitive content
- [ ] E2E voice flow passes
- [ ] demo data is clearly synthetic
- [ ] deployment health/readiness checks pass
- [ ] rollback procedure is documented
