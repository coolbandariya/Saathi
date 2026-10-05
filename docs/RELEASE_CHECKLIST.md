# Release Checklist

Before merging a milestone into main:

- CI is green.
- No secrets or real PII are present.
- Provider credentials are configured only outside Git.
- Database migrations are reviewed and reversible where practical.
- RLS/authorization tests pass.
- Consent behavior is tested for memory and outbound calls.
- External factual tools return source/timestamp metadata.
- Webhooks verify signatures and are idempotent.
- Demo-only paths are labeled.
- README and build plan match the actual implementation.
- Hackathon claims are limited to verified functionality.
