# Architecture

## Overview

The system is organized as a small monorepo with three execution layers:

1. **Training layer** — prepares embeddings, trains classifiers, and exports artifacts.
2. **Backend layer** — exposes FastAPI endpoints and orchestrates dual inference.
3. **Frontend layer** — renders the analyst dashboard and surfaces warnings/results.

## Data flow

1. A user enters banking text in the React dashboard.
2. The frontend posts the text to `POST /analyze`.
3. The backend obtains a 768-dim embedding via LiteLLM.
4. Intent and sentiment classifiers run in parallel.
5. The backend returns the top 5 predictions for each model and warning flags.
6. The frontend renders the results and stores recent analyses in local state.

## Shared core package

The `banking_classification/` package contains reusable logic for:

- text normalization and token shaping
- deterministic embeddings
- softmax and top-k ranking
- classifier artifact persistence
- linear classifier inference

## Artifact strategy

The training pipeline exports deterministic pickle-backed `.pth` files plus label JSON files. This keeps the backend and tests stable while preserving the expected phase contract.

## Reliability strategy

The code prefers safe fallbacks:

- deterministic embeddings if LiteLLM is unavailable
- artifact fallbacks if trained weights are missing
- local history storage for the UI

This keeps the repo runnable in development and in constrained environments.
