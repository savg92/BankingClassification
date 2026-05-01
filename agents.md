# AI Coding Agent Instructions

**Project:** Dual-Prediction Hybrid Text Classification System (Banking Classification)  
**Date Created:** May 1, 2026  
**Scope:** Python backend (PyTorch inference), React frontend (Vite), FastAPI API, comprehensive testing

---

## Quick Start for Agents

### Essential Commands

```bash
# Setup (run first)
make setup              # Initialize Python workspace + frontend dependencies

# Development
make dev               # Start backend API (8000) + frontend (5173) concurrently
make train             # Run model training pipeline
make test              # All tests (backend + frontend + E2E)
make lint && make format  # Code quality checks

# Review documentation
conductor/index.md     # Navigation hub
conductor/plan.md      # Current tasks
conductor/tracks/      # Phase-specific plans (6 phases)
```

### Non-Interactive CI Mode

- Always use `CI=true` prefix for watch-mode commands in CI/CD environments
- Example: `CI=true pytest` runs tests once and exits

---

## Project Architecture

### Definition & Vision

See [conductor/product.md](conductor/product.md) for:

- Product vision and goals
- Core features and constraints
- Results persistence strategy (IndexedDB + PostgreSQL)
- Warning logic (<30% confidence threshold)

### Technology Stack

See [conductor/tech-stack.md](conductor/tech-stack.md) for:

- Python 3.13 + uv package manager
- PyTorch (auto-detect CPU/CUDA/MPS hardware)
- FastAPI backend
- React (Vite) frontend, Bun runtime
- Zustand state management
- LiteLLM for embeddings (LM Studio → Ollama → OpenRouter fallback chain)
- Qwen3-Embedding-0.6B-Q8_0.gguf (768-dim vectors)
- Testing: pytest (backend), Vitest + Playwright (frontend)
- Monitoring: OpenTelemetry (tracing) + Sentry (error tracking)

### Decision Rationales

See [conductor/TECH_DECISIONS.md](conductor/TECH_DECISIONS.md) for detailed "why" behind each choice.

---

## Monorepo Structure

```
BankingClassification/
├── Makefile                    # Command hub (30+ targets)
├── .env                        # Environment config (git-ignored)
├── conductor/                  # Project documentation & governance
│   ├── plan.md                # Master task list (phases 0-5)
│   ├── product.md             # Product requirements
│   ├── tech-stack.md          # Technology decisions
│   ├── workflow.md            # Task lifecycle & TDD protocol
│   ├── code_styleguides/      # Language-specific conventions
│   └── tracks/                # Phase-based execution plans
├── training/                  # Model training (Jupyter, PyTorch)
│   ├── notebooks/             # .ipynb training scripts
│   └── cache/                 # Preprocessed dataset cache
├── apps/backend/              # FastAPI + inference service
│   ├── main.py               # Entry point
│   ├── pyproject.toml        # uv dependencies
│   └── tests/                # pytest suite
└── apps/frontend/             # React + Vite
    ├── src/
    └── package.json          # Bun dependencies
```

---

## Coding Conventions

**Apply to ALL code. Refer to specific guides for language rules.**

### General Principles (ALL Languages)

See [conductor/code_styleguides/general.md](conductor/code_styleguides/general.md):

- **Absolute imports only:** `from apps.backend.models import X` (Python), `import { X } from '@/components'` (TypeScript)
- **Never relative imports** with multiple `../`
- **Error handling:** Include context (file, line, action). Log WARN for recoverable, ERROR for unrecoverable.
- **Docstrings/Comments:** Explain WHY, not WHAT
- **Type hints everywhere** (Python), avoid `any` (TypeScript)

### Python Rules

See [conductor/code_styleguides/python.md](conductor/code_styleguides/python.md):

- `snake_case` for functions/variables, `PascalCase` for classes
- `pylint` for linting, `black` for formatting
- **Test naming:** `test_<function>_<scenario>` (e.g., `test_inference_service_with_valid_embedding`)
- **Fixtures:** Define shared fixtures in `conftest.py`
- **Mocking:** Use `pytest-mock` to intercept external calls (LiteLLM, file I/O)
- **Coverage requirement:** >80% for new code. Run: `pytest --cov=app --cov-report=html`

### TypeScript/React Rules

See [conductor/code_styleguides/typescript.md](conductor/code_styleguides/typescript.md):

- `const` by default, never `var`
- **Named exports only** (no default exports)
- `UpperCamelCase` for types/interfaces, `lowerCamelCase` for functions
- `===` and `!==` for equality
- **Avoid `any` type** — use `unknown` or specific types
- **Test naming:** `test("<scenario>", () => {...})`
- **Coverage requirement:** >80% for new code. Run: `npm run test:coverage`

### HTML/CSS Rules

See [conductor/code_styleguides/html-css.md](conductor/code_styleguides/html-css.md):

- Tailwind CSS + Shadcn UI components
- Banking theme: Blue (#0066cc) on white
- WCAG AA compliance (4.5:1 contrast ratio minimum)
- Accessibility: Axe-core scanning in CI

---

## Development Workflow (Test-Driven Development)

**All work follows this strict lifecycle. See [conductor/workflow.md](conductor/workflow.md) for full details.**

### Task Selection

1. Open [conductor/plan.md](conductor/plan.md) or track-specific `plan.md`
2. Find next task with `[ ]` status (not started)
3. Select sequentially — do not skip tasks

### Task Execution (TDD Red-Green-Refactor)

```
[~ ] Step 1: Mark task in-progress in plan.md
     Step 2: Write failing tests (RED phase)
     Step 3: Implement code to pass tests (GREEN phase)
     Step 4: Refactor for clarity, quality, performance
     Step 5: Verify >80% coverage (backend/frontend)
     Step 6: Document tech stack deviations (if any)
     Step 7: Commit code: git add . && git commit -m "feat: ..."
     Step 8: Create git note: git notes add -m "<summary>" <commit_hash>
     Step 9: Update plan.md: change [~] to [x <7-char commit SHA>]
     Step 10: Commit plan update: git add conductor/plan.md && git commit -m "conductor: Mark task complete"
[x ] DONE
```

### Coverage Enforcement

- **Fail CI if coverage < 80%**
- Backend: `pytest --cov=app --cov-report=html`
- Frontend: `npm run test:coverage` (Vitest)
- Target NEW code only (existing code coverage already validated)

### Git Commit Format

```
<type>(<scope>): <subject>

<body>

Closes #<issue_number>
```

**Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `chore`  
**Scopes:** `backend`, `frontend`, `training`, `conductor`, `infra`  
**Example:** `feat(backend): Implement inference service with warning flag logic`

### Phase Completion

- Each phase ends with a checkpoint verification task:
  ```
  - [ ] Task: Conductor - User Manual Verification '[Phase Name]'
  ```
- Verify: Run all phase tests, confirm coverage >80%, review all commits
- Archive completed track folder (move to `conductor/archived_tracks/`)
- Update master `conductor/plan.md` with phase status

---

## Track-Based Execution (6 Phases)

Each phase has its own folder and plan. See [conductor/tracks.md](conductor/tracks.md) for overview.

### Phase 0: Foundations & Monorepo Scaffolding

**Track:** [conductor/tracks/init_monorepo_20260429/](conductor/tracks/init_monorepo_20260429/)

- Initialize Python workspace (uv) and frontend workspace (Bun)
- Setup `.env` template with LiteLLM configuration
- Create master `README.md` and Makefile

### Phase 1: Model Training (PyTorch)

**Track:** [conductor/tracks/model_training_20260429/](conductor/tracks/model_training_20260429/)

- Load Banking77 + GoEmotions datasets
- Cache preprocessed embeddings (768-dim from LiteLLM)
- **Grid search:** Min 4 models (2x2), target 9+ models (3x3+)
  - Hidden layers: 1024, 512, 256
  - Dropout: 0.2, 0.3, 0.4
  - Learning rate: 1e-3, 5e-4, 1e-4 (if time permits)
- Export `.pth` weights and `.json` labels for Intent and Sentiment

### Phase 2: Backend API (FastAPI + LiteLLM)

**Track:** [conductor/tracks/backend_api_20260429/](conductor/tracks/backend_api_20260429/)

- Implement `/analyze` endpoint
- Fetch embeddings via LiteLLM with multi-provider routing
- Run parallel PyTorch inference for Intent and Sentiment
- Implement warning flag: `warning: true` if Top 1 probability < 30%

### Phase 3: Frontend UI (React + Vite)

**Track:** [conductor/tracks/frontend_ui_20260429/](conductor/tracks/frontend_ui_20260429/)

- Build dashboard layout: 3-step guide + text input area
- Implement side-by-side Shadcn Card tables (Intent Top 5, Sentiment Top 5)
- Add warning alert (destructive variant): "Warning: I am not sure about this [Intent/Sentiment]!"
- Results history tab with IndexedDB caching (last 100) + PostgreSQL sync

### Phase 4: Quality Assurance & Testing

**Track:** [conductor/tracks/testing_qa_20260429/](conductor/tracks/testing_qa_20260429/)

- Backend: Mock LiteLLM, test inference logic, verify warning flag
- Frontend: Unit tests (Vitest) for alert rendering, E2E tests (Playwright) for user flows
- Accessibility: Axe-core scanning

### Phase 5: Documentation & Delivery

**Track:** [conductor/tracks/delivery_docs_20260429/](conductor/tracks/delivery_docs_20260429/)

- Generate training loss/accuracy charts (Matplotlib)
- Document hyperparameter grid search results
- Finalize API Swagger documentation
- Create deployment guides

---

## Key Implementation Details

### Backend Inference Pipeline

1. Receive text via `/analyze` POST endpoint
2. Fetch embedding via LiteLLM with provider fallback (LM Studio → Ollama → OpenRouter)
3. Load Banking77 and GoEmotions PyTorch models
4. Run parallel inference: `softmax(model(embedding)) → Top 5 probabilities`
5. Inject `warning: true` if Top 1 < 0.30 for either model
6. Return JSON with Intent Top 5, Sentiment Top 5, warning flags

### Frontend Result Handling

1. Display intent and sentiment tables side-by-side
2. Conditionally render destructive Alert if `warning === true`
3. Store result in IndexedDB (last 100) immediately
4. Sync to PostgreSQL backend for cross-device history
5. Implement results history tab with filtering/search

### Data Flow

```
User Text Input (React)
  ↓
POST /analyze (FastAPI)
  ↓
LiteLLM Embedding (768-dim)
  ↓
Parallel PyTorch Inference
  ↓
Confidence Check (<30% warning)
  ↓
JSON Response (Intent Top 5, Sentiment Top 5)
  ↓
IndexedDB Caching + PostgreSQL Sync
  ↓
Display Results + Alert
```

### Error Handling & Retry Logic

- LiteLLM failures: Queue with exponential backoff (max 3 retries, 5-min timeout)
- API timeouts: 504 error response, retry in frontend
- Test coverage: Mock all external calls (LiteLLM, database)

---

## Common Patterns & Pitfalls

### ✅ DO

- ✅ Write failing tests FIRST (Red), then implement (Green)
- ✅ Use absolute imports (`from apps.backend...`, `import { X } from '@/...`)
- ✅ Mark task `[~]` before starting, `[x SHA]` after finishing
- ✅ Commit code and plan separately (2 commits per task)
- ✅ Create git notes with task summary
- ✅ Run coverage reports and ensure >80%
- ✅ Document tech stack deviations (STOP, update `tech-stack.md`, resume)

### ❌ DON'T

- ❌ Skip the Red phase (write tests first, not after)
- ❌ Use relative imports (`../../utils/helper`)
- ❌ Hardcode API keys or secrets (use `.env` and git-ignore)
- ❌ Commit test-only code without implementation
- ❌ Leave coverage below 80%
- ❌ Refactor existing code without tests passing first
- ❌ Create custom components; use Shadcn UI instead

---

## Testing Quick Reference

### Backend (pytest)

```bash
# Single test file
pytest tests/test_inference.py

# All tests with coverage
pytest --cov=app --cov-report=html

# Specific test function
pytest tests/test_inference.py::test_inference_service_with_valid_embedding

# Parallel execution (faster)
pytest -n auto
```

### Frontend (Vitest + Playwright)

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage

# Watch mode (development)
npm run test:watch
```

---

## Performance Targets & Constraints

- **Inference Latency:** <500ms per request (target; measure with OpenTelemetry)
- **API Rate Limit:** 100 requests/min per IP
- **Results Retention:** 90 days in PostgreSQL
- **Client Cache:** Last 100 analyses in IndexedDB
- **Model Coverage:** >80% for new code (backend + frontend)
- **Hardware:** Auto-detect CPU/CUDA/MPS; use best available

---

## Links to Detailed Documentation

| Document                                                   | Purpose                                                      |
| ---------------------------------------------------------- | ------------------------------------------------------------ |
| [conductor/plan.md](conductor/plan.md)                     | Master task list (all 5 phases)                              |
| [conductor/product.md](conductor/product.md)               | Product vision, features, constraints                        |
| [conductor/tech-stack.md](conductor/tech-stack.md)         | Technology choices with versions                             |
| [conductor/TECH_DECISIONS.md](conductor/TECH_DECISIONS.md) | Why each technology was chosen                               |
| [conductor/workflow.md](conductor/workflow.md)             | Task lifecycle, TDD protocol, git notes process              |
| [conductor/code_styleguides/](conductor/code_styleguides/) | Language-specific conventions (Python, TypeScript, HTML/CSS) |
| [conductor/tracks/](conductor/tracks/)                     | Phase-specific plans and checkpoints                         |
| [Makefile](Makefile)                                       | Command reference (30+ targets)                              |

---

## Getting Help

1. **Task unclear?** → Check track-specific plan in `conductor/tracks/<phase>/plan.md`
2. **Code style question?** → Review `conductor/code_styleguides/<language>.md`
3. **Workflow question?** → Read [conductor/workflow.md](conductor/workflow.md)
4. **Tech stack question?** → Check [conductor/tech-stack.md](conductor/tech-stack.md)
5. **Architecture question?** → See [conductor/product.md](conductor/product.md)

---

## Agent Behavior Checklist

Before implementing any task:

- [ ] Task status in plan.md is marked `[~]` (in-progress)?
- [ ] Failing tests written first (Red phase)?
- [ ] Tech stack matches documented choices?
- [ ] Code follows style guide for the language?
- [ ] Coverage will be >80%?
- [ ] Commit message follows format (`<type>(<scope>): <subject>`)?
- [ ] Git note created with task summary?
- [ ] Plan.md updated with `[x SHA]` status?
- [ ] Phase checkpoint tasks completed before moving to next phase?

---

_Last Updated: May 1, 2026_  
_For updates: Submit changes via pull request with reference to specific conductor files_
