from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .artifacts import ClassifierArtifact, load_artifact
from .prediction import build_prediction_result


def _dot(left: Iterable[float], right: Iterable[float]) -> float:
    return sum(item_left * item_right for item_left, item_right in zip(left, right))


def _relu(values: Iterable[float]) -> list[float]:
    return [value if value > 0 else 0.0 for value in values]


@dataclass(slots=True)
class LinearTextClassifier:
    """A lightweight classifier that mirrors the training/export contract."""

    artifact: ClassifierArtifact

    @classmethod
    def from_path(cls, path: Path) -> "LinearTextClassifier":
        return cls(artifact=load_artifact(path))

    def _hidden_projection(self, embedding: list[float]) -> list[float]:
        hidden_size = max(self.artifact.hidden_size, 1)
        projection = []
        for index in range(hidden_size):
            source = embedding[index % len(embedding)] if embedding else 0.0
            projection.append(source * (1.0 - self.artifact.dropout))
        return _relu(projection)

    def predict_logits(self, embedding: list[float]) -> list[float]:
        hidden = self._hidden_projection(embedding)
        logits: list[float] = []
        for row, bias in zip(self.artifact.weights, self.artifact.bias):
            expanded = row[: len(hidden)]
            logits.append(_dot(hidden[: len(expanded)], expanded) + bias)
        return logits

    def predict(self, embedding: list[float]):
        logits = self.predict_logits(embedding)
        return build_prediction_result(self.artifact.label_names, logits)