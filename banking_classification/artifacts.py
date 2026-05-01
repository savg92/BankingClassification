from __future__ import annotations

import json
import pickle
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ClassifierArtifact:
    name: str
    label_names: list[str]
    hidden_size: int
    dropout: float
    weights: list[list[float]]
    bias: list[float]
    metadata: dict[str, Any]


def save_artifact(artifact: ClassifierArtifact, path: Path) -> None:
    """Persist an artifact in a pickle-backed `.pth` file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        pickle.dump(asdict(artifact), handle)


def load_artifact(path: Path) -> ClassifierArtifact:
    """Load a persisted classifier artifact."""

    with path.open("rb") as handle:
        payload = pickle.load(handle)
    return ClassifierArtifact(**payload)


def save_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")