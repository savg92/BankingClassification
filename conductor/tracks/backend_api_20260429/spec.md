# Specification: Backend API (FastAPI + LiteLLM)

## Overview
This track involves building a REST API using FastAPI that acts as an inference gateway. The API will receive text, fetch embeddings via LiteLLM, and perform parallel classification using two pre-trained PyTorch models (Banking Intent and User Sentiment).

## Functional Requirements
- **API Scaffolding**: Setup FastAPI with CORS to allow requests from the React frontend.
- **AI Gateway Integration**: Use LiteLLM to fetch 1D embedding vectors from local (LM Studio, Ollama) or cloud (OpenAI, Anthropic) providers, configurable via `.env`.
- **Asynchronous Parallel Inference**: Implement the `/analyze` endpoint to execute inference for both Banking and Emotion models in parallel using `asyncio`.
- **Prediction Logic**:
  - Calculate `softmax` for the model outputs.
  - Sort and return the Top 5 predictions for both models.
- **Uncertainty Flagging**: If the Top 1 probability for either model is < 30%, inject a `"warning": true` flag into the respective model's response object.

## Non-Functional Requirements
- **Robust Error Handling**: Handle LiteLLM timeouts, invalid inputs, and model inference errors with appropriate HTTP status codes (504, 422, 500).
- **Response Schema**: Return a verbose JSON object containing the 1D embedding vector, Top 5 predictions, probabilities, and warning flags.

## Acceptance Criteria
- [ ] POST `/analyze` endpoint successfully returns intent and sentiment predictions.
- [ ] LiteLLM successfully routes requests based on `.env` settings.
- [ ] Parallel inference is confirmed to be non-blocking (async).
- [ ] Warning flag is correctly triggered for low-confidence (< 30%) predictions.
- [ ] API passes all unit tests for sorting logic and flag injection.

## Out of Scope
- Model training (Phase 1).
- Frontend UI implementation (Phase 3).
- Persistent storage of analysis results.
