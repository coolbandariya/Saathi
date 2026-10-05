# Observability and escalation contract

## Correlation IDs

Every HTTP request receives an `X-Correlation-ID`.

- If the caller supplies one, Saathi preserves it.
- Otherwise the backend generates a UUID-based identifier.
- The identifier is returned in the response header and API response body.
- The frontend may read the header because it is explicitly exposed through CORS.

The same identifier should be propagated into future telephony events, provider calls, audit records, and volunteer escalation records.

## Escalation

Escalation is a deterministic safety boundary, not an LLM decision.

The policy escalates when:

1. the caller explicitly requests a human;
2. a safety boundary is reached;
3. a required provider fails; or
4. confidence falls below the configured threshold (0.65 by default).

The current policy is provider-neutral and has no side effects. A future durable escalation repository should persist the decision together with household/call/correlation identifiers.

## Production requirement

The current implementation intentionally does not pretend that an escalation has reached a real volunteer. Production work must add durable persistence, assignment/claiming, operator notifications, and audit history before that claim is made.