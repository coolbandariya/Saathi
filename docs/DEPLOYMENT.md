# Saathi deployment and rollback

## Architecture

- Frontend: Next.js deployment (Vercel recommended).
- Backend: FastAPI container (Render or any Docker-compatible host).
- Providers: secrets live only in the backend environment.
- Browser: only receives NEXT_PUBLIC_API_URL.

## Backend

Build and run:

\`\`\`bash
docker build -t saathi-api ./backend
docker run --rm -p 8000:8000 --env-file backend/.env saathi-api
\`\`\`

The production health contract is:

- GET /health/live — process is alive.
- GET /health/ready — reports capability readiness without pretending optional providers are configured.
- GET /health/metrics — bounded in-memory request/latency metrics for an instance.

Never expose SUPABASE_SECRET_KEY, GEMINI_API_KEY, SARVAM_API_KEY, Exotel credentials or government API keys to the browser.

## Frontend

Set:

NEXT_PUBLIC_API_URL=https://<backend-host>

Build with npm run lint && npx tsc --noEmit && npm run build.

## Release procedure

1. Merge only green CI.
2. Record the exact Git commit deployed to frontend and backend.
3. Set provider secrets in the hosting secret manager.
4. Deploy backend first and wait for /health/ready.
5. Deploy frontend with the backend URL.
6. Run the golden demo and one factual tool smoke test.
7. If voice is claimed, complete a real provider-backed browser turn before calling it live.

## Rollback

- Frontend: redeploy the previous known-good Vercel deployment/commit.
- Backend: redeploy the previous known-good container image/commit.
- Never roll back by changing secrets in source control.
- After rollback, verify /health/ready and the golden demo before reopening traffic.

## Demo safety

DEMO_MODE=true is the default for local development. A production deployment must explicitly set DEMO_MODE=false and then verify every provider capability that is advertised. Missing providers remain visible as unavailable rather than being replaced by synthetic live-looking data.
