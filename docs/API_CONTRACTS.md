# API Contracts

## Health

`GET /health` returns service status and demo mode.

## Conversation

`POST /api/v1/conversation`

Request: `message` (1–4000 chars), optional `household_id`, and `language` defaulting to `hi`.

Response includes `status`, `reply`, `intent`, and `task_created`.

Future voice endpoints should accept provider webhooks and return provider-specific instructions without exposing provider credentials.


## Persistence boundary

Household-scoped operations will require an authenticated household identity. The client must not be trusted to grant itself access to another household.

Future task endpoints should follow these semantics:

- GET /api/v1/tasks — return only open tasks visible to the authenticated household.
- POST /api/v1/tasks — create a task only after the workflow's required consent is satisfied.
- PATCH /api/v1/tasks/{task_id} — update only a task belonging to the authenticated household.
- Cross-household access should behave as not-found rather than leaking another household's existence.

Webhook endpoints must verify the exact provider signature over the raw request body before parsing and must persist event IDs for durable idempotency.
