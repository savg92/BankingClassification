# Initial Concept

System Role: You are an Expert Full-Stack AI Engineer and Lead Data Scientist. Your task is to build a "Dual-Prediction Hybrid Text Classification System" strictly following the architectural blueprint below.

1. Project Overview
   The objective is to build a text evaluation platform that predicts both Banking Intent (Banking77 dataset) and User Sentiment (GoEmotions dataset) simultaneously from a single text input.

The system extracts text embeddings using an external/local provider via LiteLLM, then passes those embeddings through two custom PyTorch neural networks. The UI strictly handles uncertainty (<30% confidence) using targeted warnings.

2. Tech Stack & Environment
   Monorepo Management: uv (for Python workspaces), bun (for Frontend).

Machine Learning: PyTorch (torch), Jupyter Notebooks (.ipynb).

AI Provider Routing: LiteLLM (configured for LM Studio, Ollama, OpenAI, etc.).

Backend: FastAPI, pytest.

Frontend: React, Vite, Bun, Tailwind CSS, Shadcn UI, Vitest/Playwright.

3. Monorepo Structure
   Initialize the project with the following structure:

/monorepo-root
├── /training # Jupyter notebooks, datasets, PyTorch models (.pth), label_list.json
├── /apps/backend # FastAPI app, uv pyproject.toml, pytest suite
├── /apps/frontend # Vite + Bun + React app, Shadcn components, e2e tests
├── .env # Global environment variables (API_BASE_URL, LITELLM_KEY)
└── README.md # Master documentation

4. Phase I: Model Training (PyTorch)
   Inside /training, create a Jupyter Notebook to train two separate models.
   Data Preparation:

- Datasets: Load Banking77 (77 classes) and GoEmotions (28 classes).
- Preprocessing: Lowercase, remove punctuation, truncate/pad to a fixed sequence length of 128 tokens.
- Embeddings: Use LiteLLM to generate 1D vector representations (e.g., 768-dim) for the text. Treat the LLM as a frozen base model.
- Split: Strictly reserve 20% of data for validation.

Neural Architecture (Create two instances of this class):

- Global Average Pooling 1D (if sequence dimension exists).
- Dense Hidden Layer (Test 1024 vs 256 via Grid Search).
- ReLU Activation.
- Dropout Layer (Test 0.2 vs 0.3 via Grid Search).
- Dense Output Layer (Softmax logic applied via CrossEntropyLoss).

Output: Export banking_model.pth, emotion_model.pth, banking_labels.json, and emotion_labels.json.

5. Phase II: Backend API (FastAPI + LiteLLM)
   Inside /apps/backend, build a REST API.

- Provider Protocol: Use litellm.embedding to fetch embeddings based on .env configuration.
  - **Default Local Provider**: LM Studio (http://localhost:1234/v1) for development.
  - **Cloud Option**: OpenAI API (set LITELLM_KEY and model="openai/text-embedding-3-small" in .env).
  - **Alternative Local**: Ollama (http://localhost:11434/api/embeddings).
- Inference Logic: Create a POST /analyze endpoint.
  - Receive raw text.
  - Get 1 embedding vector via LiteLLM.
  - Pass the vector in parallel to the loaded Banking PyTorch model and Emotion PyTorch model.
  - Calculate torch.nn.functional.softmax.
- Business Logic (Crucial): For both models, return the Top 5 predictions. Evaluate the Top 1 probability for each. If Top 1 Probability < 0.30, inject a strict boolean flag: "warning": true into that model's response object.

6. Phase III: Frontend UI (Vite + Bun + Shadcn)
   Inside /apps/frontend, build an interactive dashboard using React with Vite.

- Layout:
  - Top: Instructional guide (3 steps) and Text Input area.
  - Bottom: Two side-by-side Shadcn Card components containing a Table of the Top 5 Banking Intents and Top 5 Sentiments.
  - **Results History Tab** (NEW): Display cached analyses (IndexedDB locally, PostgreSQL on server).
- Alert Logic (Crucial): Import the Shadcn Alert (variant="destructive"). Conditionally render an alert above the respective table if warning === true.
- Mandatory Warning String: The alert MUST strictly read: "Warning: I am not sure about this [Intent/Sentiment]!"
- **Results Persistence**: Store all analyses with timestamp and text input. Persist locally via IndexedDB (last 100) and server-side via PostgreSQL (90-day retention).

7. Phase IV: Testing Suite
   Implement a robust testing strategy:

- Unit Tests (Backend): Use pytest to mock LiteLLM and verify that the FastAPI backend correctly sorts the Top 5 probabilities and triggers the < 30% boolean flag properly.
- Unit Tests (Frontend): Use Vitest to ensure the Shadcn Alert component renders ONLY when the warning flag is true.
- Integration Tests: Test the connection between FastAPI and LiteLLM (using a mock endpoint) to ensure API timeouts and malformed JSONs are handled gracefully.
- End-to-End (E2E) Tests: Use Playwright to simulate a user typing a highly ambiguous sentence, submitting the form, and asserting that the Red Shadcn Warning Alert becomes visible on the DOM.

8. Phase V: Documentation
   Ensure the final output includes:

- Technical Functional Document (Markdown): Containing Matplotlib charts of Training/Validation Loss & Accuracy curves, and a Markdown table of the Hyperparameter Grid Search results.
- API Swagger: Auto-generated via FastAPI, clearly documenting the JSON request/response schema.
- Setup Guide: Instructions on how to start the monorepo using uv run and bun run dev.

Execution Constraints:

- NO HARDCODED API KEYS. All secrets must be loaded via dotenv.
  - For production: Rotate API keys quarterly and validate via key versioning in .env.
  - For testing: Use `pytest-mock` and `vitest.mock()` to intercept external calls.
  - For CI/CD: Use GitHub Secrets for sensitive environment variables (LITELLM_KEY, API_BASE_URL).
- Write modular, clean, and typed code (Python Type Hints, TypeScript interfaces for React).
- Organize imports: Use absolute paths for monorepo internal imports (e.g., `from apps.backend.utils import ...`).
- Errors: All exceptions must include context (file, line, action attempted). Log at WARN level for recoverable errors, ERROR for unrecoverable.- **Observability**: Instrument backend with OpenTelemetry for distributed tracing. Integrate Sentry for exception tracking in production.
- **Results Storage**: Persist analyses in PostgreSQL with 90-day retention. Support IndexedDB caching on client-side.
- **Retry Logic**: Queue failed embedding requests with exponential backoff (max 3 attempts, 5-min timeout).

## Deployment & Operations

- **Docker**: Use minimal base images (python:3.13-slim, oven/bun:latest) for fast builds and small container sizes.
- **API Rate Limiting**: Implement per-IP rate limiting (100 requests/min) on `/analyze` endpoint.
- **Request Retry**: Queue failed embedding requests with exponential backoff (3 retries, 5-min timeout total).
- **Results Persistence**: Store all analyses in PostgreSQL (90-day retention, then archive).
- **Error Tracking**: Sentry for production exception monitoring and alerts.
- **Distributed Tracing**: OpenTelemetry for end-to-end request tracing and performance monitoring.

---

# Product Definition: Dual-Prediction Hybrid Text Classification System

## Vision & Mission

To provide a high-performance, dual-prediction text evaluation platform that simultaneously identifies banking intents and user sentiments, ensuring transparency through robust uncertainty management and clear user alerts.

## Target Audience

- **Customer Service Teams**: To monitor customer sentiment and intent across banking channels for improved response strategies.
- **App Developers**: To integrate advanced classification and emotion detection into banking applications using a scalable monorepo structure.

## Core Goals

- **Accurate Dual Classification**: Leveraging Banking77 and GoEmotions datasets to provide deep insights from a single text input.
- **Uncertainty Management**: Implementing strict confidence thresholds (<30%) with mandatory user warnings ("Warning: I am not sure about this [Intent/Sentiment]!") to ensure reliable decision-making.
- **High-Performance Inference**: Utilizing LiteLLM for optimized embeddings and custom PyTorch neural networks for parallel inference.

## Key Features

- **Interactive Sandbox**: A dedicated UI area for users to test model behavior with custom sentences in real-time.
- **Results History**: Access and review all previous analyses with full metadata and timestamps.

- **Distributed Tracing**: OpenTelemetry instrumentation for monitoring inference latency and end-to-end request tracing.
- **Analytics Dashboard**: Side-by-side Shadcn Card components visualizing the Top 5 predictions for both Intent and Sentiment.
- **Batch Processing API**: A robust FastAPI backend capable of handling both single and bulk text analysis requests.
- **Targeted Alerts**: Destructive Shadcn alerts that trigger automatically when model confidence drops below the 30% threshold.

## Constraints & Requirements

- **Monorepo Scalability**: Managed via `uv` (Python) and `bun` (Frontend) for a clean, efficient development and deployment workflow.
- **Low Latency**: Optimized for real-time analysis with LiteLLM routing and parallel PyTorch inference.
- **Technical Integrity**: Comprehensive testing suite (Pytest, Vitest, Playwright) and detailed functional documentation.
- **Security**: Strict adherence to environment-based secret management (no hardcoded keys).
