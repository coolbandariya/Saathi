# API Contracts

## Health

GET /health returns service status, API version, and whether demo mode is enabled.

## Readiness

GET /ready returns ready=true when the application process can serve requests. Provider/database dependency checks belong in a future production readiness profile.

## Conversation

POST /api/v1/conversation

Request:
- message: 1–4000 characters
- household_id: optional until persistence is connected
- language: short language code, default hi

Response:
- status
- reply
- intent
- task_created
- request_id
- tool_name
- confidence

## Tasks

POST /api/v1/tasks and GET /api/v1/tasks/{household_id} are demo-only in-memory endpoints. They intentionally return 503 for task creation when DEMO_MODE=false until Supabase persistence is connected.

## Telephony

Exotel AgentStream uses a WebSocket media boundary. The adapter accepts connected, start, media, dtmf, mark, stop, and clear events and can emit bidirectional media messages. Provider-specific call persistence is intentionally deferred until the database integration is live.
