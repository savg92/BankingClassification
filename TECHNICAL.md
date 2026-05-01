# Technical Notes

## Backend

- FastAPI app lives in `apps/backend/app/main.py`
- `/health` returns service status
- `/analyze` accepts a text payload and returns embedding + prediction results
- CORS is enabled for local frontend development

## Training

- The pipeline is deterministic and self-contained
- Shared preprocessing normalizes text, tokenizes, and pads to 128 tokens
- Embeddings are cached in memory within the training run
- Artifact export writes model payloads and label JSON files

## Frontend

- React + Vite dashboard
- Tabbed navigation for Analyze/History views
- Two prediction cards with top-5 rows
- Destructive warning alerts when confidence is below threshold
- Zustand stores the UI and recent analyses

## Validation commands

- `uv run pytest -q`
- `cd apps/frontend && bun run test`
- `cd apps/frontend && bun run build`

## Current implementation note

The codebase uses deterministic fallbacks so it works without external ML services. If you later plug in real models or providers, the contract should remain the same.
