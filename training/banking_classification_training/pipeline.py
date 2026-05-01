from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from banking_classification.artifacts import save_artifact, save_json
from banking_classification.vector import EMBEDDING_DIMENSION, batch_embed_texts

from .data import INTENT_LABEL_COUNT, SENTIMENT_LABEL_COUNT, load_dual_datasets, prepare_samples
from .trainer import grid_search_configurations, split_train_validation, train_classifier


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


def run_training_pipeline() -> dict[str, object]:
    """Run the full training pipeline and export deterministic artifacts."""

    dataset_bundle = load_dual_datasets()
    intent_samples = prepare_samples(dataset_bundle.intent_samples)
    sentiment_samples = prepare_samples(dataset_bundle.sentiment_samples)

    intent_train, intent_val = split_train_validation(intent_samples)
    sentiment_train, sentiment_val = split_train_validation(sentiment_samples)

    intent_train_texts = [" ".join(tokens) for tokens, _label in intent_train]
    sentiment_train_texts = [" ".join(tokens) for tokens, _label in sentiment_train]
    intent_embeddings = batch_embed_texts(intent_train_texts)
    sentiment_embeddings = batch_embed_texts(sentiment_train_texts)
    intent_labels = [label for _tokens, label in intent_train]
    sentiment_labels = [label for _tokens, label in sentiment_train]

    configurations = grid_search_configurations()
    selected_configurations = configurations[:9]

    metrics_payload: list[dict[str, object]] = []
    best_intent = None
    best_sentiment = None
    best_score = -1.0

    for hidden_size, dropout, learning_rate in selected_configurations:
        intent_artifact, intent_metrics = train_classifier(
            intent_embeddings,
            intent_labels,
            label_limit=INTENT_LABEL_COUNT,
            hidden_size=hidden_size,
            dropout=dropout,
            learning_rate=learning_rate,
            name="intent",
        )
        sentiment_artifact, sentiment_metrics = train_classifier(
            sentiment_embeddings,
            sentiment_labels,
            label_limit=SENTIMENT_LABEL_COUNT,
            hidden_size=hidden_size,
            dropout=dropout,
            learning_rate=learning_rate,
            name="sentiment",
        )

        metrics_payload.append({"name": "intent", **asdict(intent_metrics)})
        metrics_payload.append({"name": "sentiment", **asdict(sentiment_metrics)})

        score = intent_metrics.accuracy + sentiment_metrics.accuracy
        if score > best_score:
            best_score = score
            best_intent = intent_artifact
            best_sentiment = sentiment_artifact

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    if best_intent is not None:
        save_artifact(best_intent, ARTIFACT_DIR / "intent_model.pth")
        save_json({"labels": best_intent.label_names}, ARTIFACT_DIR / "intent_labels.json")
    if best_sentiment is not None:
        save_artifact(best_sentiment, ARTIFACT_DIR / "sentiment_model.pth")
        save_json({"labels": best_sentiment.label_names}, ARTIFACT_DIR / "sentiment_labels.json")

    _write_report(metrics_payload)
    return {
        "intent_validation_count": len(intent_val),
        "sentiment_validation_count": len(sentiment_val),
        "configurations_evaluated": len(selected_configurations),
        "artifact_dir": str(ARTIFACT_DIR),
        "report_dir": str(REPORT_DIR),
    }
