# Saathi deployment

This repository contains two deployable services:

- **Frontend:** Next.js in `frontend/`
- **Backend:** FastAPI in `backend/`

The browser product does not require Streamlit. The supported deployment shape is a Next.js frontend plus a public FastAPI backend.

## 1. Deploy the backend

A Render blueprint is provided in `render.yaml`.

Required production secrets:

- `SARVAM_API_KEY`
- `MANDI_API_KEY`
- `EXOTEL_API_KEY`
- `EXOTEL_API_TOKEN`
- `EXOTEL_ACCOUNT_SID`
- `EXOTEL_VIRTUAL_NUMBER`
- `EXOTEL_STREAM_URL`
- `TELEPHONY_WEBHOOK_SECRET`
- `TELEPHONY_STREAM_TOKEN` (recommended: unpredictable token appended to the Exotel Stream URL)
- `API_AUTH_TOKEN` (optional operator/server-to-server API guard; do not expose it in browser code)

Set `CORS_ORIGINS` to the exact deployed frontend origin.

For the phone path, `EXOTEL_STREAM_URL` must point to the deployed backend WebSocket endpoint:

`wss://<backend-host>/api/v1/telephony/stream?token=<stream-token>`

Do not enable realtime telephony claims until a real Exotel call completes the full round trip.

## 2. Deploy the frontend

Deploy `frontend/` as a Next.js application.

Set:

`NEXT_PUBLIC_API_URL=https://<backend-host>`

The frontend must be rebuilt after changing this value because it is a public Next.js build-time environment variable.

## 3. First smoke test

After deployment:

1. `GET /health/live` returns `{"status":"alive"}`.
2. `GET /health/ready` reports the capabilities actually configured.
3. Text agent request succeeds.
4. Browser microphone request succeeds with a real Sarvam key.
5. Mandi responses contain government provenance.
6. Weather responses contain Open-Meteo provenance.
7. Missing entities trigger clarification rather than guessed values.
8. Human requests trigger deterministic escalation.
9. Only after those pass, configure Exotel.

## 4. Production safety

- Never commit provider secrets.
- Keep `DEMO_MODE=false` only when real providers are configured.
- Do not expose Sarvam/Exotel/API keys to the frontend.
- Restrict CORS to the deployed frontend.
- Keep caller phone numbers and sensitive documents out of logs.
- Keep the in-memory rate limiter and webhook store treated as prototype-only until durable infrastructure is added.
- The telephony stream token is an admission guard, not a replacement for Exotel event validation or durable call authorization.
- If `API_AUTH_TOKEN` is configured, direct agent/conversation/voice API clients must send `X-Saathi-API-Key`. Do not put this token in browser JavaScript; public browser authentication belongs behind the future Supabase session layer.
