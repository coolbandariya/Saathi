# Repository Governance

## Definition of done

A feature is complete only when implementation, tests, documentation, error handling, observability/audit behavior, and CI verification are present.

## Integration rule

A provider is not considered integrated because an API key exists. The repository must contain an adapter, typed contract, timeout/retry policy, failure mode, test strategy, and demo-safe fallback.

## Data rule

Production-like records must be synthetic until privacy, consent, retention, and RLS controls have been validated.

## Release gates

1. Backend tests pass.
2. Frontend production build passes.
3. Security/dependency checks pass.
4. Database migrations and RLS tests pass.
5. End-to-end demo path passes.
6. README and demo claims match the shipped functionality.
