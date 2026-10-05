# Repository boundary

Saathi keeps persistence behind small async repository interfaces.

## Why

Agent and workflow code should not know whether data comes from Supabase/Postgres, a test double, or a future local implementation.

## Required isolation

Every household-scoped repository method must receive the household identity explicitly. A repository implementation must never silently fall back to "all households".

The in-memory implementation exists only for unit tests and local workflow development. It is not durable storage and must not be presented as production persistence.

## Supabase implementation contract

The next persistence layer must:

- enforce household isolation with database RLS;
- use the authenticated user's identity for authorization rather than client-supplied roles;
- persist consent before memory or outbound-call workflows;
- make webhook idempotency durable;
- preserve timestamps and language metadata;
- return not-found semantics for cross-household task access;
- have integration tests against the actual schema.
