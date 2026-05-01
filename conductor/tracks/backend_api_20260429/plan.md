# Implementation Plan: Backend API (FastAPI + LiteLLM)

## Phase 1: API Foundation & AI Gateway

- [x] Task: Scaffold FastAPI and Environment Setup
  - [x] Write failing tests to verify FastAPI initialization and CORS configuration
  - [x] Initialize FastAPI app in `/apps/backend`
  - [x] Configure `.env` loading for `API_BASE_URL` and `LITELLM_KEY`
  - [x] Verify tests pass
- [x] Task: Integrate LiteLLM for Embedding Routing
  - [x] Write failing tests to verify LiteLLM embedding retrieval and provider routing
  - [x] Implement `litellm.embedding` utility with support for dynamic provider switching
  - [x] Verify tests pass with mock AI responses
- [x] **Task: Conductor - User Manual Verification 'Phase 1: API Foundation'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Verify FastAPI server starts without errors
  - [x] Test CORS configuration allows frontend requests
  - [x] Verify LiteLLM is properly routed based on .env configuration

## Phase 2: Inference & Business Logic

- [x] Task: Implement Asynchronous Inference Logic
  - [x] Write failing tests for parallel model loading and `asyncio` inference execution
  - [x] Implement parallel loading of `banking_model.pth` and `emotion_model.pth`
  - [x] Build the `/analyze` endpoint using `asyncio.gather` for dual-model inference
  - [x] Verify tests pass
- [x] Task: Implement Top 5 Prediction & Flagging Logic
  - [x] Write failing tests for softmax calculation, top 5 sorting, and < 30% flag injection
  - [x] Implement softmax-based probability calculation
  - [x] Implement sorting logic for top 5 predictions
  - [x] Implement the `warning: true` flag logic for low-confidence results
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 2: Inference Logic'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Run inference on sample embeddings and verify Top 5 results are sorted correctly
  - [x] Verify warning flag is triggered for probabilities < 0.30
  - [x] Verify parallel inference completes within <500ms target latency

## Phase 3: Error Handling & Final Schema

- [x] Task: Implement Global Error Handling
  - [x] Write failing tests for 504 (Timeout), 422 (Input Validation), and 500 (Model Failure) responses
  - [x] Implement FastAPI exception handlers for AI provider and inference failures
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 3: Final Verification'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Test all error response codes (504, 422, 500) are returned correctly
  - [x] Verify response JSON schema matches API documentation
  - [x] Run full test suite and achieve >80% coverage
  - [x] Write failing tests to verify the verbose JSON response (including 1D vector)
  - [x] Finalize the response model to include embeddings, predictions, and flags
  - [x] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 3: Final Verification' (Protocol in workflow.md)
