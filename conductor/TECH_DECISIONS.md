# Tech Stack Decisions & Justifications

**Document Date:** April 30, 2026  
**Project:** Banking Classification - Dual-Prediction Hybrid Text Classification System

---

## Executive Summary

This document provides the rationale for each technology choice in the project, informed by the team's specific requirements and constraints.

---

## Python & Environment

### **Python 3.13** (Latest Stable)

**Decision:** Use Python 3.13 with `uv venv` for virtual environment management.

**Rationale:**

- **Latest Features**: Python 3.13 includes performance improvements and new syntax features.
- **Future-Proof**: Ensures long-term compatibility with latest ML libraries (PyTorch, transformers).
- **Security**: Latest security patches and bug fixes.
- **Performance**: Better performance in PyTorch inference and data processing.

**Fallback:** If 3.13 compatibility issues arise, target 3.12 LTS.

### **uv for Python Package Management**

**Decision:** Use `uv` with `uv venv` instead of traditional pip/poetry/conda.

**Rationale:**

- **Speed**: 10-100x faster than pip in dependency resolution and installation.
- **Simplicity**: Single tool for everything (venv, sync, install, run).
- **Lock Files**: Deterministic builds with `uv.lock`.
- **Monorepo Support**: Handles workspace management efficiently.
- **Makefile Integration**: Easy to orchestrate with `make` targets.

**Trade-off:** Newer tool (less battle-tested than pip), but rapidly gaining adoption.

---

## Backend & Machine Learning

### **FastAPI** (Web Framework)

**Decision:** Use FastAPI for REST API and LiteLLM integration.

**Rationale:**

- **Performance**: Fastest Python web framework (near-native async).
- **Auto-Documentation**: Swagger/OpenAPI generation with zero effort.
- **Type Safety**: Full TypeScript-like type hints with Pydantic validation.
- **Async Support**: Native async/await for parallel inference.
- **Standard Library**: Works with standard Python tools (pytest, etc.).

---

### **PyTorch** (Deep Learning Framework)

**Decision:** Use PyTorch for Banking Intent and Sentiment models.

**Rationale:**

- **Flexibility**: Dynamic computation graphs easier to debug than TensorFlow.
- **Ecosystem**: Excellent model zoo and transfer learning capabilities.
- **Hardware**: Seamless CPU/CUDA/MPS auto-detection.
- **Industry Standard**: Most popular in research and production ML.

**Hardware Auto-Detection:**

```python
device = torch.device(
    'cuda' if torch.cuda.is_available()
    else 'mps' if torch.backends.mps.is_available()
    else 'cpu'
)
```

---

### **LiteLLM** (AI Gateway)

**Decision:** Use LiteLLM for embedding extraction with provider routing.

**Rationale:**

- **Provider Flexibility**: Switch between LM Studio, Ollama, OpenAI, OpenRouter without code changes.
- **Caching**: Built-in support for embedding caching.
- **Error Handling**: Unified error handling across providers.
- **Cost Tracking**: Track token usage across multiple providers.

**Provider Priority (Fallback Chain):**

1. **LM Studio** (Primary for local/development)
   - URL: `http://localhost:1234/v1`
   - Reason: Fast, no authentication, full control
2. **Ollama** (Secondary local option)
   - URL: `http://localhost:11434/api/embeddings`
   - Reason: Lightweight alternative to LM Studio
3. **OpenRouter** (Cloud fallback)
   - Reason: Works when local providers unavailable
   - Benefit: Aggregates multiple cloud providers

**Retry Strategy:**

- Queue failed requests with exponential backoff
- Max 3 attempts, 5-minute total timeout
- Graceful degradation with error messages

---

### **Qwen3-Embedding-0.6B-Q8_0.gguf** (Embedding Model)

**Decision:** Use Qwen3-0.6B quantized for local embedding generation.

**Rationale:**

- **Size**: Only 600M parameters, runs on CPU or small GPU.
- **Quantization**: Q8_0 (8-bit) maintains quality while reducing size.
- **Output**: 768-dimensional vectors (standard for classification).
- **Speed**: Local inference < 100ms per embedding (LM Studio).
- **Cost**: Free (local), no API calls needed for development.

**Dimensions:** 768 is fixed per model spec. Matches common embedding standards (OpenAI, Anthropic).

---

### **Dataset Caching**

**Decision:** Cache preprocessed datasets locally to avoid repeated embedding extraction.

**Rationale:**

- **Training Speed**: Skip embedding for each epoch (one-time cost at start).
- **Consistency**: Same embeddings for all hyperparameter configurations.
- **Development**: Faster iteration when tweaking model architecture.

**Implementation:**

- Store preprocessed tensors in `/training/cache/banking77_embeddings.pt`
- Hash text inputs to detect changes
- Regenerate cache if dataset changes

---

## Frontend & UI

### **React with Vite**

**Decision:** Use pure client-side React with Vite for development and bundling.

**Rationale:**

- **Simplicity**: Clean, minimalist setup with no extra infrastructure.
- **Fast Development**: Vite provides instant hot module replacement (HMR).
- **Fast Bundling**: Native ES modules for rapid dev server startup.
- **Flexibility**: Easy to add routing and other libraries as needed (React Router, etc.).

**Future Enhancement:** Can add SSR (with Remix/Vike) later if performance requirements demand it.

---

### **Bun** (JavaScript Runtime & Package Manager)

**Decision:** Use Bun for frontend development and package management.

**Rationale:**

- **Speed**: Faster than npm/yarn for installation and task execution.
- **Bundle**: Built-in Bun.build() for zero-config bundling.
- **Tests**: Native support for TypeScript without compilation step.
- **Environment**: Can replace Node.js for most frontend tasks.
- **Minimal Dependencies**: Less boilerplate than npm/yarn setup.

**Latest Version:** Use newest stable Bun release (track from GitHub releases).

---

### **Zustand** (State Management)

**Decision:** Use Zustand over Redux, Recoil, or Jotai.

**Rationale:**

- **Minimal Boilerplate**: Define stores in ~20 lines vs Redux in ~100 lines.
- **Better Performance**: Direct object mutation tracking, no selector memoization needed.
- **Small Bundle**: ~2KB gzipped (Redux is ~7KB).
- **Simplicity**: No action types, no dispatch, just functions.
- **Simplicity**: Works perfectly with client-side rendering setup.

**Example:**

```typescript
const useInferenceStore = create((set) => ({
	results: null,
	setResults: (results) => set({ results }),
}));
```

vs Redux:

```typescript
// Redux requires: actions, reducers, dispatch, selectors
// ~5x more boilerplate
```

---

### **Results Persistence** (IndexedDB + PostgreSQL)

**Decision:** Dual persistence layer for results history.

**Rationale:**

- **IndexedDB (Client)**:
  - Instant access to recent analyses (last 100)
  - Works offline
  - No server round-trip
- **PostgreSQL (Server)**:
  - Persistent storage across devices
  - 90-day retention policy
  - Supports analytics and trending

**Trade-off:** Added complexity vs. convenience for users who want to review past analyses.

---

## Testing Strategy

### **Backend: pytest + pytest-mock**

**Decision:** Use pytest for unit and integration tests.

**Rationale:**

- **Industry Standard**: Most popular Python testing framework.
- **Fixtures**: Powerful setup/teardown with reusable fixtures.
- **Plugins**: Rich ecosystem (pytest-cov, pytest-asyncio, pytest-xdist).
- **Mocking**: Seamless mocking of LiteLLM and external services.
- **Parallel Execution**: Built-in support for running tests in parallel.

**Coverage Target:** >80% for all new code. Fail CI if below threshold.

---

### **Frontend: Vitest + Playwright**

**Decision:** Use Vitest for unit tests, Playwright for E2E.

**Rationale:**

- **Vitest**: ESM-native, works directly with Vite (no compilation).
- **Playwright**: Cross-browser E2E testing (Chrome, Firefox, Safari, Edge).
- **Integration**: Both support modern async/await syntax.
- **Debugging**: Easy to debug with browser DevTools.

**E2E Scenarios:**

1. Ambiguous text input → Alert renders
2. API timeout (504) → Error message displays
3. Results persistence → Data survives page reload
4. Results history tab → Previous analyses load

---

## Deployment & Operations

### **Docker Base Images**

**Decision:** Use minimal images for fast builds and small container sizes.

**Backend:** `python:3.13-slim`

- Includes Python 3.13 with minimal OS dependencies
- ~150MB base image (vs ~900MB with `python:3.13-full`)
- Sufficient for FastAPI + PyTorch inference

**Frontend:** `oven/bun:latest`

- Bun runtime with all necessary tools
- Smaller than Node.js images
- Better compatibility with Bun build system

---

### **API Rate Limiting**

**Decision:** Implement per-IP rate limiting (100 requests/min).

**Rationale:**

- **Cost Control**: Prevent accidental embedding API abuse.
- **Fair Usage**: Distribute resources fairly across users.
- **Security**: Mitigate DDoS-style attacks.

**Implementation:** Use `slowapi` or `starlette-limiter` middleware in FastAPI.

---

### **Error Tracking: Sentry**

**Decision:** Integrate Sentry for production exception tracking.

**Rationale:**

- **Alerting**: Get notified of production errors immediately.
- **Grouping**: Automatically group similar errors.
- **Breadcrumbs**: Track user actions leading up to error.
- **Performance**: Monitor transaction throughput and latency.
- **Free Tier**: Generous free tier for small projects.

**Integration Points:**

- FastAPI middleware for backend exceptions
- React error boundary for frontend
- Automatic breadcrumbs for API calls

---

### **Observability: OpenTelemetry**

**Decision:** Instrument with OpenTelemetry for distributed tracing.

**Rationale:**

- **End-to-End Tracing**: See request path from frontend → backend → LiteLLM → PyTorch inference.
- **Latency Tracking**: Identify bottlenecks in the inference pipeline.
- **Vendor Agnostic**: Export to Jaeger (local), DataDog, or Grafana.
- **Standards-Based**: CNCF standard for observability.

**Instrumentation Points:**

- FastAPI: `FastAPIInstrumentor()`
- LiteLLM: Custom tracing wrapper
- PyTorch: Model inference timing
- React: Component render times

---

## Build & Deploy Orchestration

### **Makefile for Command Centralization**

**Decision:** Use Makefile as single source of truth for all `uv` and `bun` commands.

**Rationale:**

- **Single Entry Point**: `make dev` instead of remembering separate commands.
- **Documentation**: Built-in help (`make help`) shows all targets.
- **Consistency**: Same workflows locally and in CI/CD.
- **Parallelization**: Run backend and frontend simultaneously.
- **Extensibility**: Easy to add new targets.

**Key Targets:**

- `make setup` - Complete project initialization
- `make dev` - Local development (backend + frontend)
- `make test` - All tests with coverage
- `make lint` - Code quality checks
- `make docker-up` - Production-like environment

---

## Key Trade-offs & Decisions

| Decision                   | Pro                          | Con                            | Mitigation                         |
| -------------------------- | ---------------------------- | ------------------------------ | ---------------------------------- |
| **Python 3.13**            | Latest features, performance | Fewer battle-tested packages   | Use LTS (3.12) as fallback         |
| **uv**                     | Fast, simple                 | Newer tool                     | Active development, good community |
| **Zustand**                | Minimal boilerplate, fast    | Less structured for large apps | Add patterns/conventions doc       |
| **Pure React + Vite**      | Simplicity, fast dev loop    | May need SSR later for SEO     | Can upgrade to Remix/Vike later    |
| **Bun**                    | Fast, unified runtime        | Less mature than Node.js       | Monitor for production issues      |
| **OpenTelemetry**          | Vendor agnostic              | Setup overhead                 | Docker Compose includes collector  |
| **PostgreSQL for history** | Persistent, scalable         | Added infrastructure           | SQLite fallback for MVP            |

---

## Future Considerations

### **Potential Upgrades**

1. **Vector Database**: Use Pinecone or Milvus if similarity search needed.
2. **Model Serving**: Add vLLM or TensorRT for faster inference.
3. **Async Workers**: Use Celery/RQ for async embedding jobs.
4. **Cache Layer**: Add Redis for embedding cache (multi-device sync).
5. **Monitoring Dashboard**: Grafana + Prometheus for metrics.

### **Scalability Path**

- **Phase 1** (Current): Single API, React with Vite
- **Phase 2**: Add message queue for async jobs (Celery)
- **Phase 3**: Horizontal scaling with load balancer (nginx)
- **Phase 4**: Kubernetes orchestration (k8s)

---

## Conclusion

All technology choices prioritize:

1. **Developer Experience**: Simple, well-documented tools
2. **Performance**: Fast inference, quick load times
3. **Maintainability**: Standard tools with large communities
4. **Flexibility**: Easy to swap components (LiteLLM providers, databases, etc.)

The Makefile serves as the single source of truth for development workflows, ensuring consistency across local development, CI/CD, and production deployments.

---

_Last Updated: April 30, 2026_  
_Next Review: When adding new major dependencies or significant architectural changes_
