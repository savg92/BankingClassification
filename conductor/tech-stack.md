# Tech Stack: Dual-Prediction Hybrid Text Classification System

## Core Languages

- **Python 3.13**: The primary language for model training, data preprocessing, and the FastAPI backend. Use `uv venv` for virtual environment management.
- **TypeScript**: Used for the React frontend to ensure type safety and a robust developer experience.
- **Makefile**: Central orchestration for `uv` and `bun` commands (see root `Makefile` for all available targets).

## Backend & Machine Learning

- **FastAPI**: A high-performance web framework for the REST API, providing auto-generated Swagger documentation.
  - **App Location**: `apps/backend/app/main.py`
  - **Endpoints**:
    - `/health` - Service status check
    - `/analyze` - POST endpoint: Accept text payload, return embedding + prediction results
  - **CORS**: Enabled for local frontend development (Vite localhost:5173)
- **PyTorch (torch)**: The core deep learning framework for training and serving the custom Banking and Emotion neural networks. Auto-detect hardware (CPU/CUDA/MPS) and use best available.
- **LiteLLM**: An AI gateway for routing embedding requests to providers, configured via environment variables.
  - **Primary Provider (Local)**: LM Studio (http://localhost:1234/v1)
  - **Secondary Local Option**: Ollama (http://localhost:11434/api/embeddings)
  - **Cloud Fallback**: OpenRouter (for cloud-based embedding if local unavailable)
  - **Configuration**: Requires reachable `LITELLM_API_BASE`, `LITELLM_MODEL`, and `LITELLM_API_KEY` in `.env`
- **Embedding Model**: Qwen3-Embedding-0.6B-Q8_0.gguf (768-dim vectors, optimized for local inference)
- **Training Datasets**:
  - **Banking Intent**: mteb/banking77 (77 intent classes)
  - **Sentiment**: go_emotions (emotion classification)
- **Preprocessing Pipeline**:
  - Text normalization (lowercase, special character handling)
  - Tokenization and padding to 128 tokens
  - Embedding extraction via LiteLLM provider
- **Model Caching**: Cache preprocessed datasets locally to avoid repeated embedding extraction (stored in `/training/cache/`).
- **Artifact Export**: Save model weights (`.pth`) and class labels (`.json`) to `/artifacts/`
- **Request Retry Strategy**: Queue failed requests with exponential backoff. Fail after max retries (default: 3 attempts, 3-minute timeout) with graceful error messaging.

## Frontend & UI

- **React (Vite)**: Client-side rendering with Vite for fast development and bundling.
  - **Dashboard Layout**: 3-step guide + text input area
  - **Results Display**: Side-by-side Shadcn Card tables (Intent Top 5, Sentiment Top 5)
  - **Tabs**: Analyze tab (main input) + History tab (past analyses)
- **Bun**: Used as the frontend package manager and runtime for Vite (latest stable version, minimal dependencies).
- **Tailwind CSS + Shadcn UI**: For building a clean, modern, and accessible interface with highly customizable components.
  - **Banking Theme**: Blue (#0066cc) and white palette per product guidelines.
  - **High Contrast**: WCAG AA compliance (4.5:1 ratio) on all text.
  - **Warning Alert**: Destructive variant (red) displays when confidence < 30%: "Warning: I am not sure about this [Intent/Sentiment]!"
- **State Management**: Zustand (minimal boilerplate, better performance than Redux).
  - Stores UI state and recent analyses
- **Form Management**: React Hook Form (lightweight, zero dependencies).
- **Results History**: Persist analysis results in browser IndexedDB and server-side cache (Redis optional for multi-device sync).
  - **Client Cache**: Last 100 analyses in IndexedDB
  - **Server Cache**: PostgreSQL with 90-day retention policy

## Monorepo & Infrastructure

- **uv**: Manages Python workspaces, dependencies, and virtual environments efficiently (via `make` targets).
  - **Virtual Env**: Use `uv venv` for isolated Python environments per workspace.
  - **Lock Files**: Commit `uv.lock` for reproducible builds.
- **Bun**: JavaScript package manager and runtime (latest stable, configured via `make` targets).
- **Monorepo Structure**:
  - `/training`: PyTorch training scripts, Jupyter Notebooks, preprocessed dataset cache.
  - `/apps/backend`: FastAPI service with OpenTelemetry instrumentation.
  - `/apps/frontend`: React application with Vite, Zustand store, and IndexedDB results cache.
- **Environment Management**: All secrets and configurations (e.g., `API_BASE_URL`, `LITELLM_KEY`, `SENTRY_DSN`) managed via `.env` files (never committed).
- **Orchestration**: Use `Makefile` for all `uv` and `bun` commands (e.g., `make train`, `make backend-dev`, `make frontend-dev`).

## Testing Strategy

- **Backend Testing**: `pytest` for unit and integration tests, mocking LiteLLM providers. Target >80% coverage.
  - **Command**: `uv run pytest -q` (quick) or `uv run pytest --cov=app` (with coverage)
  - **Mocking**: Use `pytest-mock` and fixtures to intercept LiteLLM calls.
  - **Performance**: Track inference latency (<500ms SLA) in tests.
  - **Error Handling**: Test all error codes (504, 422, 500) and retry logic.
- **Frontend Testing**: `Vitest` for component unit tests (>80% coverage). `Playwright` for E2E testing.
  - **Commands**:
    - Unit tests: `cd apps/frontend && bun run test`
    - E2E tests: `cd apps/frontend && bun run test:e2e`
    - Coverage: `cd apps/frontend && bun run test:coverage`
  - **E2E Scenarios**: Ambiguous text input, alert visibility, API failure handling (504), results persistence.
  - **Accessibility**: Axe-core for automated A11y scanning in CI.
- **CI/CD**: GitHub Actions on all commits. Fail build if coverage < 80% or accessibility violations found.
- **Coverage Enforcement**: `pytest --cov=app --cov-report=html` and `npm run test:coverage` with HTML reports.

## Monitoring & Observability

- **Error Tracking**: Sentry for exception tracking and alerting in production.
  - **Integration**: FastAPI middleware and React error boundary hooks.
  - **Configuration**: `SENTRY_DSN` from `.env`.
- **Distributed Tracing**: OpenTelemetry for request tracing across services.
  - **Backend**: FastAPI instrumentation with auto-tracing of LiteLLM calls and PyTorch inference.
  - **Frontend**: React tracing for component mount/render times and API calls.
  - **Exporter**: OTLP protocol to local collector (or cloud Jaeger/DataDog).
- **Logging**: Structured JSON logging with correlation IDs for request tracing.
  - **Backend**: Python `logging` module with JSON formatter.
  - **Frontend**: Console structured logs for development; Sentry breadcrumbs for production.

## Deployment

- **Docker Base Images**:
  - **Backend**: `python:3.13-slim` (minimal, latest Python)
  - **Frontend**: `node:20-alpine` (for Bun compatibility) or `oven/bun:latest`
- **Container Orchestration**: `docker-compose` for local multi-service setup.
- **Secrets Management**:
  - **Local Development**: `.env` file (never committed, use `.env.example` template)
  - **CI/CD**: GitHub Secrets for `LITELLM_KEY`, `SENTRY_DSN`, `OPENROUTER_KEY`
  - **Production**: Azure Key Vault or similar secret management service
  - **Key Rotation**: Rotate API keys quarterly; maintain versioned backups
- **API Rate Limiting**: Implement token bucket or sliding window limiter for `/analyze` endpoint (e.g., 100 requests/min per IP)
- **Results History Storage**:
  - **Client-side**: Browser IndexedDB for local cache (persist last 100 analyses)
  - **Server-side**: PostgreSQL with optional Redis cache layer
  - **Retention**: Keep analyses for 90 days, then archive to cold storage

## Implementation Notes

### **Critical Setup Requirement**

Training and inference require **live embedding provider connectivity**. Before running:

```bash
# Configure .env with provider details
echo "LITELLM_API_BASE=http://localhost:1234/v1" >> .env
echo "LITELLM_MODEL=qwen:0.6b" >> .env
echo "LITELLM_API_KEY=<optional_if_required>" >> .env
```

**Ensure the embedding provider is running locally (LM Studio, Ollama, or OpenRouter) before executing:**

- `make train` - Model training pipeline
- `make backend-dev` or `make dev` - FastAPI inference service

### **Validation Commands Quick Reference**

**Backend:**

```bash
uv run pytest -q              # Quick test validation
uv run pytest --cov=app       # With coverage report (target >80%)
```

**Frontend:**

```bash
cd apps/frontend && bun run test           # Unit tests
cd apps/frontend && bun run test:coverage  # Coverage report
cd apps/frontend && bun run build          # Production build validation
```

**Full Stack:**

```bash
make dev                      # Start backend (8000) + frontend (5173) concurrently
make test                     # All tests (backend + frontend + E2E)
make lint && make format      # Code quality checks
```
