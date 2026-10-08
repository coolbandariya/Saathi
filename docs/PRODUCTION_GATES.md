# Production gates

A Saathi release is not production-ready until all of these are true:

- [ ] Supabase schema and RLS reviewed against the actual live project
- [ ] household isolation integration tests pass
- [ ] durable webhook idempotency exists
- [ ] exact telephony signature contract tested
- [ ] telephony stream admission token configured and rotated
- [ ] production API authentication/household authorization is enforced for non-demo clients
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
- [ ] Mandi "today" claims are backed by an observation dated today; otherwise Saathi says "latest verified observation"
- [ ] day-specific weather requests use day-specific forecast evidence
- [ ] rollback procedure is documented
