# Render deployment — Saathi API

This deploys the **FastAPI backend** as a Docker web service. It does not deploy the Next.js dashboard or the Streamlit judge demo.

## Connect the repository

Use the repository that contains the Dockerfile and backend code you intend to deploy. The maintained repository is:

- Repository: `kaustubhdua/Saathi`
- Branch: `main`

The currently shown Render service in the supplied screenshots clones `harshilgupta926/Saathi`. Changes pushed to `kaustubhdua/Saathi` do not update that other repository. Either connect Render to `kaustubhdua/Saathi`, or copy/merge the deployment files into `harshilgupta926/Saathi` first.

## Render fields

Choose **Docker** as the runtime and set:

| Field | Value |
|---|---|
| Name | `saathi-api` (or another unique name) |
| Branch | `main` |
| Root Directory | **Leave blank** |
| Dockerfile Path | `./Dockerfile` |
| Docker Build Context Directory | `.` if Render displays this field |
| Health Check Path | `/health` if available; otherwise use the actual health route from the API |

Do **not** enter `backend/app/` as the Root Directory or Dockerfile Path. The Dockerfile is at the repository root and copies dependencies from `backend/requirements.txt`.

The previous failure, `open Dockerfile: no such file or directory`, means Render was configured to build from a location where it could not find a Dockerfile. The root Dockerfile fixes that for the maintained repository once it is present in the repository Render actually clones.

## Environment variables

Start in safe demo mode:

```text
DEMO_MODE=true
APP_ENV=production
CORS_ORIGINS=https://YOUR-FRONTEND-DOMAIN
```

Add provider secrets only in Render's Environment page, never in Git. For a verified live vertical slice, add the required `GEMINI_API_KEY`, `SARVAM_API_KEY`, and/or `MANDI_API_KEY` plus `MANDI_RESOURCE_ID`. Set `DEMO_MODE=false` only after testing the corresponding provider path end-to-end.

For Exotel, configure its account credentials, public `wss://` stream URL and webhook/call tokens only after the deployed endpoint and signature handling have been verified. Never trigger unsolicited outbound calls: implement explicit consent, quiet hours, duplicate-job prevention, and retry limits first.

## Scope and readiness

This Dockerfile runs the current FastAPI API only. It does **not** imply that Supabase persistence, household memory, proactive callback scheduling, WhatsApp, MyScheme retrieval, OCR upload/storage, or a full LangGraph multi-agent workflow are complete. The current project has provider boundaries and parts of the voice/telephony path, but those additional blueprint capabilities must be implemented and tested before they are represented as live.

For a standalone judge demo, use Streamlit Community Cloud with `streamlit_app/app.py` as documented in `docs/STREAMLIT_DEPLOY.md`.
