# Contributing to Saathi

## Branches

Use short-lived branches from main:
- `feat/<scope>` for product work
- `fix/<scope>` for defects
- `test/<scope>` for test-only changes
- `chore/<scope>` for tooling/docs

## Pull requests

Every PR should explain the outcome, list important files changed, and include verification performed. Do not merge with failing required checks.

## Secrets

Never commit API keys, tokens, phone credentials, service-role keys, or private user data. Use `.env` locally and repository/environment secrets in deployment systems.

## Data

Use synthetic demo households. Real phone numbers, medical information, identity documents, and recordings must not be added to the repository.

## Commit style

Prefer concise prefixes such as feat:, fix:, test:, docs:, chore: and security:.
