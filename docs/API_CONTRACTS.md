# API Contracts

## Health

`GET /health` returns service status and demo mode.

## Conversation

`POST /api/v1/conversation`

Request: `message` (1–4000 chars), optional `household_id`, and `language` defaulting to `hi`.

Response includes `status`, `reply`, `intent`, and `task_created`.

Future voice endpoints should accept provider webhooks and return provider-specific instructions without exposing provider credentials.
