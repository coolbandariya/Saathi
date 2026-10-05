# Security Policy

Saathi handles potentially sensitive household, voice, document, and service-request data.

- Never disclose API keys, Supabase service-role keys, telephony credentials, or access tokens in issues or PRs.
- Keep privileged credentials server-side.
- Enforce household isolation with Supabase RLS.
- Record consent before persistence or outbound contact.
- Avoid real PII in fixtures and demos.
- Verify third-party webhook signatures and deduplicate webhook events.

For a real vulnerability, contact maintainers privately rather than opening a public issue containing exploit details.
