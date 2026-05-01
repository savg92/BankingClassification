from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Iterable


@dataclass(slots=True)
class PredictionItem:
    label: str
    probability: float


@dataclass(slots=True)
class PredictionResult:
    predictions: list[PredictionItem]
    warning: bool


def softmax(logits: Iterable[float]) -> list[float]:
    """Compute a numerically stable softmax over the provided scores."""

    scores = list(logits)
    if not scores:
        return []
    max_score = max(scores)
    exp_scores = [exp(score - max_score) for score in scores]
    total = sum(exp_scores)
    if total == 0:
        return [0.0 for _ in exp_scores]
    return [score / total for score in exp_scores]


def top_k_predictions(labels: list[str], probabilities: list[float], k: int = 5) -> list[PredictionItem]:
    """Return the top-k predictions ordered by descending probability."""

    ranked = sorted(zip(labels, probabilities), key=lambda item: item[1], reverse=True)
    return [PredictionItem(label=label, probability=probability) for label, probability in ranked[:k]]


def build_prediction_result(labels: list[str], logits: list[float], warning_threshold: float = 0.30) -> PredictionResult:
    """Convert logits into a ranked prediction result with warning metadata."""

    probabilities = softmax(logits)
    predictions = top_k_predictions(labels, probabilities)
    warning = bool(predictions and predictions[0].probability < warning_threshold)
    return PredictionResult(predictions=predictions, warning=warning)