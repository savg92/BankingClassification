# Implementation Plan: Backend API (FastAPI + LiteLLM)

## Phase 1: API Foundation & AI Gateway

- [ ] Task: Scaffold FastAPI and Environment Setup
    - [ ] Write failing tests to verify FastAPI initialization and CORS configuration
    - [ ] Initialize FastAPI app in `/apps/backend`
    - [ ] Configure `.env` loading for `API_BASE_URL` and `LITELLM_KEY`
    - [ ] Verify tests pass
- [ ] Task: Integrate LiteLLM for Embedding Routing
    - [ ] Write failing tests to verify LiteLLM embedding retrieval and provider routing
    - [ ] Implement `litellm.embedding` utility with support for dynamic provider switching
    - [ ] Verify tests pass with mock AI responses
- [ ] Task: Conductor - User Manual Verification 'Phase 1: API Foundation' (Protocol in workflow.md)

## Phase 2: Inference & Business Logic

- [ ] Task: Implement Asynchronous Inference Logic
    - [ ] Write failing tests for parallel model loading and `asyncio` inference execution
    - [ ] Implement parallel loading of `banking_model.pth` and `emotion_model.pth`
    - [ ] Build the `/analyze` endpoint using `asyncio.gather` for dual-model inference
    - [ ] Verify tests pass
- [ ] Task: Implement Top 5 Prediction & Flagging Logic
    - [ ] Write failing tests for softmax calculation, top 5 sorting, and < 30% flag injection
    - [ ] Implement softmax-based probability calculation
    - [ ] Implement sorting logic for top 5 predictions
    - [ ] Implement the `warning: true` flag logic for low-confidence results
    - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Inference Logic' (Protocol in workflow.md)

## Phase 3: Error Handling & Final Schema

- [ ] Task: Implement Global Error Handling
    - [ ] Write failing tests for 504 (Timeout), 422 (Input Validation), and 500 (Model Failure) responses
    - [ ] Implement FastAPI exception handlers for AI provider and inference failures
    - [ ] Verify tests pass
- [ ] Task: Finalize Response Schema
    - [ ] Write failing tests to verify the verbose JSON response (including 1D vector)
    - [ ] Finalize the response model to include embeddings, predictions, and flags
    - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Verification' (Protocol in workflow.md)
