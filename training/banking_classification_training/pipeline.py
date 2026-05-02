from __future__ import annotations

import logging
import os
import time
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from banking_classification.artifacts import ClassifierArtifact, save_artifact, save_json
from banking_classification.vector import EMBEDDING_DIMENSION

logger = logging.getLogger(__name__)

from .data import DatasetTarget, INTENT_LABEL_COUNT, SENTIMENT_LABEL_COUNT, load_dual_datasets, prepare_samples
from .trainer import grid_search_configurations, split_train_validation, train_classifier


def _normalize_litellm_model(model: str) -> str:
    normalized = model.strip()
    if "/" in normalized:
        return normalized
    return f"openai/{normalized}"


def _embed_texts_with_litellm(texts: list[str]) -> list[list[float]]:
    """Embed texts through LiteLLM/OpenAI-compatible endpoint without deterministic fallback."""

    if not texts:
        return []

    model = os.getenv("LITELLM_MODEL", "openai/text-embedding-3-small")
    api_base = os.getenv("LITELLM_API_BASE", "http://localhost:1234/v1")
    api_key = os.getenv("LITELLM_API_KEY")
    chunk_size = max(1, int(os.getenv("EMBEDDING_CHUNK_SIZE", "16")))
    min_chunk_size = max(1, int(os.getenv("EMBEDDING_MIN_CHUNK_SIZE", "1")))
    embedding_retries = max(1, int(os.getenv("EMBEDDING_RETRIES", "3")))
    embedding_timeout = max(5, int(os.getenv("EMBEDDING_TIMEOUT", "60")))

    def _try_litellm_sdk_call(texts: list[str]) -> list[list[float]] | None:
        try:
            import litellm  # type: ignore

            litellm_model = _normalize_litellm_model(model)
            logger.info(f"Requesting embeddings from LiteLLM SDK (model={litellm_model}, base={api_base})")
            response = litellm.embedding(  # type: ignore[attr-defined]
                model=litellm_model,
                input=texts,
                api_base=api_base,
                api_key=api_key,
                timeout=embedding_timeout,
            )
            if not isinstance(response, dict):
                return None
            data = response.get("data", [])
            if len(data) != len(texts):
                return None
            embeddings: list[list[float]] = []
            for item in data:
                emb = item.get("embedding")
                if emb is None:
                    return None
                embeddings.append([float(v) for v in emb])
            return embeddings
        except Exception as e:
            logger.warning(f"LiteLLM SDK embedding failed: {type(e).__name__}: {e}")
            return None

    sdk_result = _try_litellm_sdk_call(texts)
    if sdk_result is not None:
        return sdk_result

    try:
        import requests
    except ImportError as e:
        raise RuntimeError("Embedding failed via LiteLLM SDK and requests is not installed for HTTP fallback") from e

    if api_base.endswith("/embeddings"):
        embeddings_url = api_base
    elif api_base.endswith("/v1"):
        embeddings_url = f"{api_base}/embeddings"
    else:
        embeddings_url = f"{api_base.rstrip('/')}/v1/embeddings"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    def _http_embed_chunk(chunk_texts: list[str]) -> list[list[float]] | None:
        payload = {"model": model, "input": chunk_texts}
        for attempt in range(1, embedding_retries + 1):
            try:
                response = requests.post(embeddings_url, json=payload, headers=headers, timeout=embedding_timeout)
                response.raise_for_status()
                body = response.json()
                data = body.get("data", [])
                if len(data) != len(chunk_texts):
                    raise RuntimeError(f"Expected {len(chunk_texts)} embeddings, got {len(data)}")
                embeddings = []
                for item in data:
                    emb = item.get("embedding")
                    if emb is None:
                        raise RuntimeError("Embedding response item missing 'embedding'")
                    embeddings.append([float(v) for v in emb])
                return embeddings
            except Exception as e:
                if attempt == embedding_retries:
                    return None
                time.sleep(min(8, 2 ** attempt))
                logger.warning(
                    f"HTTP embedding request failed for chunk size {len(chunk_texts)} (attempt {attempt}/{embedding_retries}): {type(e).__name__}: {e}"
                )
        return None

    embeddings_by_index: list[list[float] | None] = [None] * len(texts)
    pending = list(enumerate(texts))
    active_chunk = min(chunk_size, len(pending))

    while pending:
        chunk = pending[:active_chunk]
        chunk_indices = [index for index, _ in chunk]
        chunk_texts = [text for _, text in chunk]
        chunk_embeddings = _http_embed_chunk(chunk_texts)
        if chunk_embeddings is not None:
            for index, embedding in zip(chunk_indices, chunk_embeddings):
                embeddings_by_index[index] = embedding
            pending = pending[active_chunk:]
            active_chunk = min(chunk_size, len(pending)) if pending else 0
            continue
        if active_chunk == min_chunk_size:
            raise RuntimeError(
                f"Embedding failed at minimum chunk size {min_chunk_size}. Check LITELLM_API_BASE/LITELLM_API_KEY and local provider health."
            )
        next_chunk = max(min_chunk_size, active_chunk // 2)
        logger.warning(f"Reducing embedding chunk size from {active_chunk} to {next_chunk} after repeated failures")
        active_chunk = next_chunk

    resolved_embeddings = [embedding for embedding in embeddings_by_index if embedding is not None]
    if len(resolved_embeddings) != len(texts):
        raise RuntimeError(f"Embedding response incomplete: expected {len(texts)}, got {len(resolved_embeddings)}")
    return resolved_embeddings


ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
REPORT_DIR = Path(__file__).resolve().parents[2] / "reports"


def _write_report(metrics: list[dict[str, object]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "training_results.md"
    lines = ["# Training Summary", "", f"Embedding dimension: {EMBEDDING_DIMENSION}", ""]
    lines.append("| Model | Hidden | Dropout | LR | Accuracy | Loss | F1 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for metric in metrics:
        lines.append(
            f"| {metric['name']} | {metric['hidden_size']} | {metric['dropout']} | {metric['learning_rate']} | {metric['accuracy']} | {metric['loss']} | {metric['f1_weighted']} |"
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    save_json({"metrics": metrics}, REPORT_DIR / "training_results.json")


def _train_best_artifact(
    name: Literal["intent", "sentiment"],
    embeddings: list[list[float]],
    labels: list[str],
    label_limit: int,
    selected_configurations: list[tuple[int, float, float]],
) -> tuple[ClassifierArtifact, list[dict[str, object]], int]:
    metrics_payload: list[dict[str, object]] = []
    best_artifact = None
    best_score = -1.0
    for hidden_size, dropout, learning_rate in selected_configurations:
        artifact, metrics = train_classifier(
            embeddings,
            labels,
            label_limit=label_limit,
            hidden_size=hidden_size,
            dropout=dropout,
            learning_rate=learning_rate,
            name=name,
        )
        metrics_payload.append({"name": name, **asdict(metrics)})
        if metrics.accuracy > best_score:
            best_score = metrics.accuracy
            best_artifact = artifact
    if best_artifact is None:
        raise RuntimeError(f"No trained artifact produced for {name}")
    return best_artifact, metrics_payload, len(selected_configurations)


def run_training_pipeline(target: DatasetTarget = "both") -> dict[str, object]:
    """Run the training pipeline and export artifacts."""

    dataset_bundle = load_dual_datasets(target=target)
    intent_samples = prepare_samples(dataset_bundle.intent_samples) if dataset_bundle.intent_samples else []
    sentiment_samples = prepare_samples(dataset_bundle.sentiment_samples) if dataset_bundle.sentiment_samples else []

    try:
        slice_n = int(os.getenv("TRAIN_SLICE", "0"))
    except Exception:
        slice_n = 0
    if slice_n and slice_n > 0:
        if intent_samples:
            intent_samples = intent_samples[:slice_n]
        if sentiment_samples:
            sentiment_samples = sentiment_samples[:slice_n]

    configurations = grid_search_configurations()
    selected_configurations = configurations[: int(os.getenv("TRAIN_CONFIG_LIMIT", "9"))]
    if not selected_configurations:
        raise RuntimeError("No training configurations selected")

    metrics_payload: list[dict[str, object]] = []
    best_intent = None
    best_sentiment = None
    intent_val_count = 0
    sentiment_val_count = 0

    if target in {"both", "intent"}:
        intent_train, intent_val = split_train_validation(intent_samples)
        intent_val_count = len(intent_val)
        intent_texts = [" ".join(tokens) for tokens, _label in intent_train]
        intent_labels = [label for _tokens, label in intent_train]
        intent_embeddings = _embed_texts_with_litellm(intent_texts)
        best_intent, intent_metrics_payload, _ = _train_best_artifact(
            name="intent",
            embeddings=intent_embeddings,
            labels=intent_labels,
            label_limit=INTENT_LABEL_COUNT,
            selected_configurations=selected_configurations,
        )
        metrics_payload.extend(intent_metrics_payload)

    if target in {"both", "sentiment"}:
        sentiment_train, sentiment_val = split_train_validation(sentiment_samples)
        sentiment_val_count = len(sentiment_val)
        sentiment_texts = [" ".join(tokens) for tokens, _label in sentiment_train]
        sentiment_labels = [label for _tokens, label in sentiment_train]
        sentiment_embeddings = _embed_texts_with_litellm(sentiment_texts)
        best_sentiment, sentiment_metrics_payload, _ = _train_best_artifact(
            name="sentiment",
            embeddings=sentiment_embeddings,
            labels=sentiment_labels,
            label_limit=SENTIMENT_LABEL_COUNT,
            selected_configurations=selected_configurations,
        )
        metrics_payload.extend(sentiment_metrics_payload)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    if best_intent is not None:
        save_artifact(best_intent, ARTIFACT_DIR / "intent_model.pth")
        save_json({"labels": best_intent.label_names}, ARTIFACT_DIR / "intent_labels.json")
    if best_sentiment is not None:
        save_artifact(best_sentiment, ARTIFACT_DIR / "sentiment_model.pth")
        save_json({"labels": best_sentiment.label_names}, ARTIFACT_DIR / "sentiment_labels.json")

    _write_report(metrics_payload)
    return {
        "target": target,
        "intent_validation_count": intent_val_count,
        "sentiment_validation_count": sentiment_val_count,
        "configurations_evaluated": len(selected_configurations),
        "artifact_dir": str(ARTIFACT_DIR),
        "report_dir": str(REPORT_DIR),
    }
