# Tech Stack: Dual-Prediction Hybrid Text Classification System

## Core Languages
- **Python 3.11+**: The primary language for model training, data preprocessing, and the FastAPI backend.
- **TypeScript**: Used for the React frontend to ensure type safety and a robust developer experience.

## Backend & Machine Learning
- **FastAPI**: A high-performance web framework for the REST API, providing auto-generated Swagger documentation.
- **PyTorch (torch)**: The core deep learning framework for training and serving the custom Banking and Emotion neural networks.
- **LiteLLM**: An AI gateway for routing embedding requests to providers like LM Studio, Ollama, or OpenAI, configured via environment variables.

## Frontend & UI
- **React (Vite)**: A modern, component-based library for building the interactive dashboard.
- **Bun**: Used as the frontend package manager and runtime for Vite.
- **Tailwind CSS + Shadcn UI**: For building a clean, modern, and accessible interface with highly customizable components.

## Monorepo & Infrastructure
- **uv**: Manages Python workspaces, dependencies, and virtual environments efficiently.
- **Monorepo Structure**:
  - `/training`: PyTorch training scripts and Jupyter Notebooks.
  - `/apps/backend`: FastAPI service.
  - `/apps/frontend`: React application.
- **Environment Management**: All secrets and configurations (e.g., `API_BASE_URL`, `LITELLM_KEY`) are managed via `.env` files.

## Testing Strategy
- **Backend Testing**: `pytest` for unit and integration tests, including mocking AI providers.
- **Frontend Testing**: `Vitest` for component unit tests and `Playwright` for full end-to-end (E2E) testing of the analysis flow and alert logic.
