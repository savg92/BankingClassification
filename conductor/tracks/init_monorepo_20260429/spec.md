# Specification: Initialize Monorepo and Scaffold Core Architecture

## Overview
This track focuses on the foundational setup of the "Dual-Prediction Hybrid Text Classification System" monorepo. It establishes the workspace management, environment configuration, and initial directory structure required for subsequent training, backend, and frontend development.

## Objectives
- Initialize a Python workspace using `uv` for training and backend services.
- Initialize a frontend application using `bun`, `vite`, and `react`.
- Configure global environment variables and secret management.
- Establish the directory structure defined in the project overview.
- Define initial boilerplate for testing (Pytest, Vitest).

## Scope
- **Workspace Management**: `uv` for Python, `bun` for JavaScript/TypeScript.
- **Directories**: `/training`, `/apps/backend`, `/apps/frontend`.
- **Configuration**: `.env`, `README.md`, `pyproject.toml`, `package.json`.
- **Infrastructure**: Initial Git ignore rules and project documentation.

## Acceptance Criteria
- [ ] Root `pyproject.toml` managed by `uv` exists.
- [ ] `/apps/frontend` contains a working Vite/React scaffold managed by `bun`.
- [ ] `/apps/backend` contains a FastAPI scaffold.
- [ ] `/training` directory exists for future model training artifacts.
- [ ] `.env` template exists with required variables (`API_BASE_URL`, `LITELLM_KEY`).
- [ ] `README.md` provides clear instructions for monorepo setup and execution.
- [ ] All scaffolds pass initial linting/type-checking.
