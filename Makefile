# Banking Classification - Dual-Prediction Hybrid Text Classification System
# Makefile for orchestrating Python (uv) and JavaScript (bun) development workflows
#
# Usage:
#   make help              - Show all available targets
#   make setup             - Complete project setup (dependencies + env)
#   make install-deps      - Install Python and frontend dependencies
#   make train             - Run model training pipeline
#   make train-intent      - Train only intent model (Banking77)
#   make train-sentiment   - Train only sentiment model (GoEmotions)
#   make backend-dev       - Start backend API in development mode
#   make frontend-dev      - Start frontend in development mode
#   make test              - Run all tests (backend + frontend)
#   make test-backend      - Run backend tests only
#   make test-frontend     - Run frontend tests only
#   make coverage          - Generate coverage reports
#   make lint              - Run all linters (Python + TypeScript)
#   make format            - Format all code
#   make docker-build      - Build Docker images
#   make docker-up         - Start services with docker-compose
#   make docker-down       - Stop services
#   make clean             - Clean build artifacts and caches

.PHONY: help setup install-deps setup-python setup-frontend train train-intent train-sentiment train-slice backend-dev frontend-dev test test-backend test-frontend coverage lint format docker-build docker-up docker-down clean

# Default shell
SHELL := /bin/bash

# Python executable (using uv venv)
PYTHON := ./.venv/bin/python
PIP := ./.venv/bin/pip
UV := uv

# Node/Bun executables
BUN := bun
NODE := node

# Project paths
PYTHON_ROOT := .
BACKEND_DIR := ./apps/backend
FRONTEND_DIR := ./apps/frontend
TRAINING_DIR := ./training

# Environment
ifdef GITHUB_ACTIONS
	CI := true
else
	CI := false
endif

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# ============================================================================
# HELP
# ============================================================================

help:
	@echo "$(BLUE)=========================================="
	@echo "Banking Classification Project - Make Targets"
	@echo "==========================================$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@echo "  make setup              - Complete project setup (dependencies + env)"
	@echo "  make install-deps       - Install Python and frontend dependencies"
	@echo "  make setup-python       - Setup Python environment with uv"
	@echo "  make setup-frontend     - Setup Frontend with bun"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make train              - Run model training pipeline"
	@echo "  make train-intent       - Train only intent model (mteb/banking77)"
	@echo "  make train-sentiment    - Train only sentiment model (go_emotions)"
	@echo "  make train-slice N=500  - Run quick slice with limited samples"
	@echo "  make backend-dev        - Start backend API (http://localhost:8000)"
	@echo "  make frontend-dev       - Start frontend (http://localhost:5173)"
	@echo "  make dev                - Run backend and frontend concurrently"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test               - Run all tests (backend + frontend + e2e)"
	@echo "  make test-backend       - Run backend tests with coverage"
	@echo "  make test-frontend      - Run frontend tests with coverage"
	@echo "  make test-e2e           - Run Playwright E2E tests"
	@echo "  make coverage           - Generate coverage reports (HTML)"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make lint               - Run all linters (pylint, eslint)"
	@echo "  make format             - Format all code (black, prettier)"
	@echo "  make type-check         - Run type checking (mypy, tsc)"
	@echo ""
	@echo "$(GREEN)Docker & Deployment:$(NC)"
	@echo "  make docker-build       - Build Docker images"
	@echo "  make docker-up          - Start services with docker-compose"
	@echo "  make docker-down        - Stop services"
	@echo "  make docker-logs        - View docker-compose logs"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make clean              - Clean build artifacts and caches"
	@echo "  make env-template       - Generate .env.example template"
	@echo "  make deps-update        - Update all dependencies"
	@echo ""

# ============================================================================
# SETUP & INSTALLATION
# ============================================================================

install-deps: setup-python setup-frontend

setup: install-deps env-template
	@echo "$(GREEN)✓ Project setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Configure .env with your LiteLLM provider (LM Studio, Ollama, etc.)"
	@echo "  2. Start services: make dev"
	@echo "  3. Run tests: make test"

setup-python:
	@echo "$(BLUE)Setting up Python environment with uv...$(NC)"
	@$(UV) venv
	@$(UV) sync --all-groups
	@echo "$(GREEN)✓ Python environment ready$(NC)"

setup-frontend:
	@echo "$(BLUE)Setting up Frontend with bun...$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) install
	@echo "$(GREEN)✓ Frontend dependencies installed$(NC)"

env-template:
	@if [ ! -f .env ]; then \
		echo "$(BLUE)Creating .env template...$(NC)"; \
		echo "# API Configuration" > .env.example; \
		echo "API_BASE_URL=http://localhost:8000" >> .env.example; \
		echo "API_TIMEOUT=30" >> .env.example; \
		echo "" >> .env.example; \
		echo "# LiteLLM Configuration" >> .env.example; \
		echo "LITELLM_MODEL=openai/text-embedding-3-small" >> .env.example; \
		echo "LITELLM_API_BASE=http://localhost:1234/v1" >> .env.example; \
		echo "LITELLM_API_KEY=sk-test" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Optional: Cloud Providers" >> .env.example; \
		echo "OPENROUTER_API_KEY=" >> .env.example; \
		echo "OPENAI_API_KEY=" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Observability" >> .env.example; \
		echo "SENTRY_DSN=" >> .env.example; \
		echo "OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Database (if using PostgreSQL for results history)" >> .env.example; \
		echo "DATABASE_URL=postgresql://user:password@localhost:5432/banking_classification" >> .env.example; \
		echo "" >> .env.example; \
		echo "# Development" >> .env.example; \
		echo "DEBUG=false" >> .env.example; \
		echo "CI=$(CI)" >> .env.example; \
		cp .env.example .env; \
		echo "$(GREEN)✓ Created .env (copy of .env.example)$(NC)"; \
	else \
		echo "$(YELLOW).env already exists, skipping...$(NC)"; \
	fi

# ============================================================================
# DEVELOPMENT
# ============================================================================

train:
	@echo "$(BLUE)Running model training pipeline...$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(PYTHON) training/train.py

train-intent:
	@echo "$(BLUE)Running intent-only training (mteb/banking77)...$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(PYTHON) training/train.py --target intent

train-sentiment:
	@echo "$(BLUE)Running sentiment-only training (go_emotions)...$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(PYTHON) training/train.py --target sentiment

train-slice:
	@echo "$(BLUE)Running quick training slice (TRAIN_SLICE=${N:-500})...$(NC)"
	@TRAIN_SLICE=${N:-500} PYTHONPATH=$(PYTHON_ROOT) $(PYTHON) training/train.py

backend-dev:
	@echo "$(BLUE)Starting backend API (http://localhost:8000)...$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(UV) run uvicorn apps.backend.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	@echo "$(BLUE)Starting frontend dev server (http://localhost:5173)...$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run dev

dev:
	@echo "$(BLUE)Starting both backend and frontend...$(NC)"
	@echo "$(YELLOW)Backend: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:5173$(NC)"
	@echo "$(YELLOW)Docs: http://localhost:8000/docs$(NC)"
	@echo ""
	@echo "Press Ctrl+C to stop both services."
	@echo ""
	@$(MAKE) -j2 backend-dev frontend-dev

# ============================================================================
# TESTING
# ============================================================================

test: test-backend test-frontend test-e2e
	@echo "$(GREEN)✓ All tests completed!$(NC)"

test-backend:
	@echo "$(BLUE)Running backend tests (pytest)...$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(UV) run pytest -v apps/backend/tests --cov=apps/backend --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Backend tests passed$(NC)"
	@echo "Coverage report: apps/backend/htmlcov/index.html"

test-frontend:
	@echo "$(BLUE)Running frontend tests (vitest)...$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run test --run
	@echo "$(GREEN)✓ Frontend tests passed$(NC)"

test-e2e:
	@echo "$(BLUE)Running E2E tests (playwright)...$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run test:e2e
	@echo "$(GREEN)✓ E2E tests passed$(NC)"

coverage:
	@echo "$(BLUE)Generating coverage reports...$(NC)"
	@echo "$(YELLOW)Backend coverage:$(NC)"
	@PYTHONPATH=$(PYTHON_ROOT) $(UV) run pytest apps/backend --cov=apps/backend --cov-report=html
	@echo "  Report: apps/backend/htmlcov/index.html"
	@echo ""
	@echo "$(YELLOW)Frontend coverage:$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run test:coverage
	@echo "  Report: $(FRONTEND_DIR)/coverage/index.html"

# ============================================================================
# CODE QUALITY
# ============================================================================

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "$(YELLOW)Python (pylint):$(NC)"
	@cd $(BACKEND_DIR) && $(UV) run pylint --recursive=y .
	@echo "$(YELLOW)TypeScript (eslint):$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run lint
	@echo "$(GREEN)✓ Linting complete$(NC)"

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@echo "$(YELLOW)Python (black, isort):$(NC)"
	@cd $(BACKEND_DIR) && $(UV) run black . && $(UV) run isort .
	@echo "$(YELLOW)TypeScript (prettier):$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run format
	@echo "$(GREEN)✓ Code formatted$(NC)"

type-check:
	@echo "$(BLUE)Running type checking...$(NC)"
	@echo "$(YELLOW)Python (mypy):$(NC)"
	@cd $(BACKEND_DIR) && $(UV) run mypy .
	@echo "$(YELLOW)TypeScript (tsc):$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) run type-check
	@echo "$(GREEN)✓ Type checking complete$(NC)"

# ============================================================================
# DOCKER & DEPLOYMENT
# ============================================================================

docker-build:
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker-compose build
	@echo "$(GREEN)✓ Docker images built$(NC)"

docker-up: docker-build
	@echo "$(BLUE)Starting services with docker-compose...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo ""
	@echo "$(YELLOW)Services available at:$(NC)"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

docker-down:
	@echo "$(BLUE)Stopping services...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

docker-logs:
	@docker-compose logs -f

# ============================================================================
# UTILITIES
# ============================================================================

clean:
	@echo "$(BLUE)Cleaning up...$(NC)"
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name .DS_Store -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

deps-update:
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@echo "$(YELLOW)Python (uv):$(NC)"
	@$(UV) sync --upgrade
	@echo "$(YELLOW)JavaScript (bun):$(NC)"
	@cd $(FRONTEND_DIR) && $(BUN) update
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

# ============================================================================
# CI/CD (GitHub Actions Helper Targets)
# ============================================================================

ci-check: lint type-check test
	@echo "$(GREEN)✓ CI checks passed!$(NC)"

ci-build:
	@echo "$(BLUE)Building for production...$(NC)"
	@$(MAKE) setup
	@cd $(BACKEND_DIR) && $(UV) run pip install -r requirements.txt
	@cd $(FRONTEND_DIR) && $(BUN) run build
	@echo "$(GREEN)✓ Production build complete$(NC)"

# ============================================================================
# DEFAULT TARGET
# ============================================================================

.DEFAULT_GOAL := help
