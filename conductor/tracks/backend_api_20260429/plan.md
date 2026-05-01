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
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: API Foundation'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Verify FastAPI server starts without errors
  - [ ] Test CORS configuration allows frontend requests
  - [ ] Verify LiteLLM is properly routed based on .env configuration

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
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Inference Logic'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Run inference on sample embeddings and verify Top 5 results are sorted correctly
  - [ ] Verify warning flag is triggered for probabilities < 0.30
  - [ ] Verify parallel inference completes within <500ms target latency

## Phase 3: Error Handling & Final Schema

- [ ] Task: Implement Global Error Handling
  - [ ] Write failing tests for 504 (Timeout), 422 (Input Validation), and 500 (Model Failure) responses
  - [ ] Implement FastAPI exception handlers for AI provider and inference failures
  - [ ] Verify tests pass
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Final Verification'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Test all error response codes (504, 422, 500) are returned correctly
  - [ ] Verify response JSON schema matches API documentation
  - [ ] Run full test suite and achieve >80% coverage
  - [ ] Write failing tests to verify the verbose JSON response (including 1D vector)
  - [ ] Finalize the response model to include embeddings, predictions, and flags
  - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Verification' (Protocol in workflow.md)
