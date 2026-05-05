# Banking Classification

Dual-prediction hybrid text classification system for banking intent and user sentiment analysis.

This repository is a full monorepo with training, inference, and dashboard layers, plus shared utilities and planning docs.

## What’s inside

- `apps/backend` — FastAPI inference gateway with `/health` and `/analyze`
- `apps/frontend` — React + Vite dashboard with tabs, result cards, warnings, and history
- `training` — dataset-driven training pipeline, artifact export, and report generation
- `banking_classification/` — shared utilities for text processing, embeddings, prediction ranking, and artifact loading
- `conductor/` — project plans, execution tracks, and workflow guidance
- `ARCHITECTURE.md` — system architecture and data flow overview
- `TECHNICAL.md` — implementation notes and validation commands

## Project at a glance

- **Backend**: FastAPI service that accepts text input, fetches an embedding, runs dual inference, and returns top-5 predictions with warning flags.
- **Frontend**: Analyst dashboard for entering customer text, reviewing intent/sentiment predictions, and viewing low-confidence alerts.
- **Training**: Training/export pipeline that pulls `mteb/banking77` + `go_emotions`, produces artifacts, and writes reports under `artifacts/` and `reports/`.
- **Shared core**: Reusable logic for normalization, token shaping, softmax ranking, and artifact persistence.

## Architecture summary

1. A user enters banking-related text in the React dashboard.
2. The frontend sends the text to `POST /analyze`.
3. The backend derives a 768-dimension embedding using LiteLLM-compatible providers.
4. Intent and sentiment classifiers run in parallel.
5. The API returns top-5 predictions, probabilities, the embedding, and confidence warning flags.
6. The frontend renders the results, stores recent analyses locally, and exposes a history view for recall.

If you want the long-form version with diagrams, see `ARCHITECTURE.md`.

## Repository layout

| Path                      | Purpose                                                             |
| ------------------------- | ------------------------------------------------------------------- |
| `apps/backend/`           | FastAPI app, runtime settings, providers, and service orchestration |
| `apps/frontend/`          | React UI, state store, API client, and Vitest tests                 |
| `training/`               | Training pipeline, dataset preparation, and artifact generation     |
| `banking_classification/` | Shared domain logic used by backend, training, and tests            |
| `reports/`                | Training summaries in Markdown and JSON                             |
| `artifacts/`              | Serialized model artifacts and label maps                           |
| `conductor/`              | Execution plans, phase docs, and workflow references                |

## Requirements

- Python 3.13+
- `uv` for Python workspace/dependency management
- Bun for frontend dependencies and scripts
- Optional: LiteLLM-compatible provider(s) if you want to swap in real embedding services

## Windows — Setup & requirements

This project runs on Windows but requires a few platform-specific tools and small workflow adjustments. Follow the steps below to prepare a Windows development machine.

- Prerequisites
  - Windows 10/11 with latest updates
  - Python 3.13 installed and added to PATH (download from python.org)
  - Git for Windows (Git Bash) — provides a Unix-like shell for some Makefile workflows
  - Visual Studio Build Tools (C++ Build Tools) — required for some Python packages that build native extensions
  - A package manager: `winget` (Windows Package Manager) or `choco` (Chocolatey) for easy installs

- Install Python dependencies (PowerShell)

  ```powershell
  python -m pip install --upgrade pip
  python -m pip install uv
  # Create venv and install pinned deps
  uv venv
  uv sync --all-groups
  ```

- Install Bun (PowerShell)

  ```powershell
  powershell -c "irm bun.sh/install.ps1 | iex"
  # Ensure %USERPROFILE%\.bun\bin is in your user PATH and restart the terminal
  ```

- Install GNU Make (recommended via winget)

  ```powershell
  winget install --id ezwinports.make -e --accept-package-agreements --accept-source-agreements
  # or with Chocolatey (admin): choco install make -y
  ```

  After install restart your terminal and verify:

  ```powershell
  make --version
  ```

- Git Bash / Make compatibility
  - The Makefile includes some POSIX-style env assignments (e.g. `PYTHONPATH=... command`) which may not work with Windows cmd.exe. Options:
    - Run `make` inside Git Bash or WSL (recommended for parity with the Makefile).
    - Install GNU Make via `winget` and add its bin directory to your Git Bash PATH (or copy `make.exe` into Git's `usr/bin`).
    - Alternatively run backend and frontend commands directly in PowerShell (examples below).

- Start services on Windows (PowerShell examples)
  - Backend (use venv python)
    ```powershell
    $env:PYTHONPATH = (Resolve-Path .).Path
    .\.venv\Scripts\python.exe -m uvicorn apps.backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
  - Frontend
    ```powershell
    cd apps/frontend
    %USERPROFILE%\.bun\bin\bun.exe install
    %USERPROFILE%\.bun\bin\bun.exe run dev
    ```

- Troubleshooting
  - If `bun` invokes an older npm shim (errors referencing `%APPDATA%\npm\bun.ps1`), remove the shim files:
    ```powershell
    Remove-Item $env:APPDATA\npm\bun.ps1 -Force -ErrorAction SilentlyContinue
    Remove-Item $env:APPDATA\npm\bun.cmd -Force -ErrorAction SilentlyContinue
    ```
    Then ensure `C:\Users\<you>\.bun\bin` is in your user PATH and restart the terminal.
  - If `make` is not found in Git Bash after installing via winget, add the winget packages bin to your `~/.bashrc`:
    ```bash
    echo 'export PATH="$PATH:/c/Users/<you>/AppData/Local/Microsoft/WinGet/Packages/ezwinports.make_Microsoft.Winget.Source_8wekyb3d8bbwe/bin"' >> ~/.bashrc
    source ~/.bashrc
    ```

If you prefer, run the Makefile targets inside WSL where bash and the standard Unix tools are available; this often yields the smoothest cross-platform behavior.

## Configuration

Copy `.env.example` to `.env` or edit the existing `.env` file to suit your environment.

| Variable                      | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| `API_BASE_URL`                | Frontend API base URL                                  |
| `API_TIMEOUT`                 | Request timeout in seconds                             |
| `LITELLM_MODEL`               | Embedding model identifier                             |
| `LITELLM_API_BASE`            | LiteLLM-compatible base URL                            |
| `LITELLM_API_KEY`             | Provider API key                                       |
| `OPENROUTER_API_KEY`          | Optional fallback provider key                         |
| `OPENAI_API_KEY`              | Optional provider key                                  |
| `DATABASE_URL`                | Optional PostgreSQL connection string for history sync |
| `SENTRY_DSN`                  | Optional error tracking endpoint                       |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Optional tracing endpoint                              |
| `DEBUG`                       | Enable/disable debug mode                              |

## Quick start

1. Install dependencies:
   - `make setup`
2. Review or update `.env`.
3. Start the app stack:
   - `make dev`
4. Open:
   - Backend docs: `http://localhost:8000/docs`
   - Frontend: `http://localhost:5173`

## Day-to-day workflows

### Setup

- `make setup` — initialize Python and frontend dependencies, then create the environment template
- `make make install-deps` — install all dependencies
- `make setup-backend` — install backend dependencies
- `make setup-frontend` — install frontend dependencies

### Development

- `make backend-dev` — run the FastAPI server
- `make frontend-dev` — run the React dev server
- `make dev` — run both services together
- `make train` — execute the dual training pipeline
- `make train-intent` — train only intent model from `mteb/banking77`
- `make train-sentiment` — train only sentiment model from `go_emotions`
- `make train-slice N=500` — run a quick local slice

### Validation

- `make test` — run backend, frontend, and E2E checks
- `make test-backend` — run backend tests with coverage
- `make test-frontend` — run frontend tests
- `make test-e2e` — run browser-style E2E validation
- `make coverage` — generate coverage reports

### Quality and packaging

- `make lint` — run Python and TypeScript linting
- `make format` — format code
- `make type-check` — run Python and TypeScript type checks
- `make docker-build` — build container images
- `make docker-up` — start the containerized stack
- `make docker-down` — stop the containerized stack

## API surface

- `GET /health` — service status and readiness probe
- `POST /analyze` — analyze submitted text and return predictions, probabilities, embedding data, and warning flags

The exact response contract is described in the backend docs and exercised by the test suite.

## Training outputs

The training pipeline writes generated artifacts to:

- `artifacts/intent_model.pth`
- `artifacts/sentiment_model.pth`
- `artifacts/intent_labels.json`
- `artifacts/sentiment_labels.json`
- `reports/training_results.md`
- `reports/training_results.json`

## Validation results

Verified in this repository:

- Python test suite: `uv run pytest -q`
- Frontend test suite: `cd apps/frontend && bun run test`
- Frontend production build: `cd apps/frontend && bun run build`
- Training pipeline: `uv run python -m training.train`

## Design notes

- Text normalization strips punctuation, normalizes Unicode, and preserves word boundaries.
- Training embeddings are fetched from your configured LiteLLM-compatible endpoint.
- Prediction ranking always returns top-5 labels where available.
- A warning is raised when the top prediction falls below the configured confidence threshold.
- Recent analyses are stored locally in the browser for fast recall.

## Contributing

Please keep changes aligned with the existing project conventions:

- Prefer absolute imports
- Add or update tests for behavior changes
- Keep backend/frontend/training logic in their respective layers
- Update the conductor docs if a phase or workflow meaningfully changes
- Keep provider-based embedding behavior explicit and observable

## Troubleshooting

- If the embedding provider is unreachable, verify `LITELLM_API_BASE`, `LITELLM_MODEL`, and `LITELLM_API_KEY`.
- If model artifacts are missing, rerun the training pipeline.
- If the frontend fails type checking, make sure test files are excluded from the production build config as intended.
- If commands behave differently on your machine, check `Makefile` for the canonical workflow.

## Further reading

- `ARCHITECTURE.md`
- `TECHNICAL.md`
- `conductor/plan.md`
- `conductor/tracks.md`
