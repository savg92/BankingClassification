# Master Implementation Plan: Dual-Prediction Hybrid Text Classification System

This document outlines the end-to-end execution strategy for the project, covering environment setup, model training, API development, UI implementation, and verification.

---

## Phase 0: Foundations & Monorepo Scaffolding

- [ ] **Task 0.1: Initialize Python Workspace (uv)**
  - Initialize root project and configure workspace members.
  - Setup `/training` and `/apps/backend` directories.
- [ ] **Task 0.2: Initialize Frontend Workspace (bun)**
  - Scaffold `/apps/frontend` using Vite + React + TypeScript.
  - Integrate Tailwind CSS and Shadcn UI.
- [ ] **Task 0.3: Global Configuration**
  - Create `.env` template with LiteLLM and API base configurations.
  - Setup master `README.md` with monorepo execution guides.

## Phase 1: Model Training (PyTorch)

- [ ] **Task 1.1: Data Engineering**
  - Load Banking77 and GoEmotions datasets.
  - Implement 128-token padding/truncation and text normalization.
  - **NEW**: Cache preprocessed datasets locally to avoid repeated embedding extraction.
- [ ] **Task 1.2: Embedding Integration**
  - Integrate LiteLLM for 768-dim vector extraction.
  - Support multiple embedding providers: LM Studio (primary), Ollama, OpenRouter (fallback).
- [ ] **Task 1.3: Model Development & Training**
  - Implement PyTorch architecture: GAP 1D -> Dense -> ReLU -> Dropout -> Softmax.
  - Auto-detect hardware (CPU/CUDA/MPS) and use best available.
  - **NEW**: Run extended hyperparameter grid search including:
    - Hidden layer size: 1024 vs 512 vs 256
    - Dropout: 0.2 vs 0.3 vs 0.4
    - Learning rate: 1e-3 vs 5e-4 vs 1e-4 (if time permits)
  - Total combinations: minimum 2x2 (4 models), ideally 3x3 (9 models) or more.
- [ ] **Task 1.4: Artifact Export**
  - Save `.pth` model weights and `.json` label maps for both Intent and Sentiment.
  - Track training metrics: Loss, Accuracy, F1-score (weighted) for all grid search configurations.

## Phase 2: Backend API (FastAPI + LiteLLM)

- [ ] **Task 2.1: API Scaffolding & Routing**
  - Setup FastAPI with CORS and environment-based LiteLLM provider routing.
- [ ] **Task 2.2: Inference Service**
  - Implement `/analyze` endpoint to fetch embeddings and run parallel PyTorch inference.
- [ ] **Task 2.3: Business Logic & Thresholds**
  - Implement Top 5 sorting and probability calculation.
  - Inject `warning: true` flag for Top 1 Probability < 0.30.

## Phase 3: Frontend UI (Vite + Bun + Shadcn)

- [ ] **Task 3.1: Dashboard Layout**
  - Build the dashboard with Vite and React.
  - Implement 3-step instructional guide and text input area (pre-rendered on server).
  - Setup results history tab for cached analyses.
- [ ] **Task 3.2: Visualization Components & Results History**
  - Build side-by-side Shadcn Card components with result tables.
  - Implement IndexedDB caching for client-side results persistence (last 100 analyses).
  - Connect to backend PostgreSQL for server-side results history (90-day retention).
- [ ] **Task 3.3: Interactive Alert Logic**
  - Implement conditional rendering of destructive Alerts with mandatory warning strings.
  - Implement client-side state management with Zustand for results history filtering.

## Phase 4: Quality Assurance & Testing

- [ ] **Task 4.1: Backend Unit & Integration Tests**
  - Mock LiteLLM embeddings and verify inference/flagging logic via Pytest.
- [ ] **Task 4.2: Frontend Unit & E2E Tests**
  - Verify conditional alert rendering via Vitest.
  - Implement Playwright E2E flows for ambiguous text scenarios.

## Phase 5: Documentation & Delivery

- [ ] **Task 5.1: Performance Analytics**
  - Generate training/validation loss/accuracy charts using Matplotlib.
- [ ] **Task 5.2: Final Handover**
  - Finalize API Swagger documentation and setup/execution guides.
