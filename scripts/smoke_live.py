"""Run provider smoke checks against a running Saathi backend.

Usage:
  SAATHI_BASE_URL=http://localhost:8000 python scripts/smoke_live.py

This script never prints secret values. It is intentionally outside CI because live
provider credentials are environment-specific.
"""
import os
import sys
import httpx

BASE = os.getenv("SAATHI_BASE_URL", "http://localhost:8000").rstrip("/")

def main() -> int:
    with httpx.Client(timeout=20) as client:
        ready = client.get(BASE + "/health/ready")
        ready.raise_for_status()
        print("readiness:", ready.json())

        weather = client.post(
            BASE + "/api/v1/agent",
            json={"message": "अगले 24 घंटे में बारिश की संभावना कितनी है?", "language": "hi", "household_id": "smoke-household", "location": {"latitude": 28.9931, "longitude": 77.0151, "label": "Sonipat district · smoke test"}},
        )
        weather.raise_for_status()
        body = weather.json()
        print("weather intent:", body.get("intent"))
        print("weather source:", (body.get("source") or {}).get("name"))

        mandi = client.post(
            BASE + "/api/v1/agent",
            json={"message": "सोनीपत मंडी में गेहूं का आज का भाव", "language": "hi", "household_id": "smoke-household"},
        )
        mandi.raise_for_status()
        body = mandi.json()
        print("mandi intent:", body.get("intent"))
        print("mandi source:", (body.get("source") or {}).get("name"))

        return 0

if __name__ == "__main__":
    raise SystemExit(main())
