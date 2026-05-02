from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Literal

from banking_classification.text import SampleRecord, preprocess_text

logger = logging.getLogger(__name__)


INTENT_LABEL_COUNT = 77
SENTIMENT_LABEL_COUNT = 28


@dataclass(slots=True)
class DatasetBundle:
    intent_samples: list[SampleRecord]
    sentiment_samples: list[SampleRecord]


DatasetTarget = Literal["both", "intent", "sentiment"]


def _resolve_split(dataset_name: str, split_hint: str):
    from datasets import load_dataset  # type: ignore

    try:
        return load_dataset(dataset_name, split=split_hint)
    except Exception:
        dataset = load_dataset(dataset_name)
        if split_hint in dataset:
            return dataset[split_hint]
        if "train" in dataset:
            return dataset["train"]
        available = ", ".join(dataset.keys())
        raise RuntimeError(f"Dataset '{dataset_name}' does not expose a '{split_hint}' or 'train' split. Available: {available}")


def _load_intent_samples() -> list[SampleRecord]:
    banking_dataset = _resolve_split("mteb/banking77", "train")
    label_feature = banking_dataset.features.get("label")
    label_names = getattr(label_feature, "names", None)
    samples: list[SampleRecord] = []
    for item in banking_dataset:
        text = item.get("text") or item.get("utterance")
        label_raw = item.get("label")
        if text is None or label_raw is None:
            continue
        if isinstance(label_raw, int) and isinstance(label_names, list) and 0 <= label_raw < len(label_names):
            label = label_names[label_raw]
        else:
            label = str(label_raw)
        samples.append(SampleRecord(text=str(text), label=label))
    if not samples:
        raise RuntimeError("No usable intent samples were loaded from mteb/banking77")
    return samples


def _load_sentiment_samples() -> list[SampleRecord]:
    emotions_dataset = _resolve_split("go_emotions", "train")
    label_feature = emotions_dataset.features.get("labels")
    label_names = getattr(label_feature, "feature", None)
    label_names = getattr(label_names, "names", None)
    samples: list[SampleRecord] = []
    for item in emotions_dataset:
        text = item.get("text")
        labels = item.get("labels")
        if text is None:
            continue
        if isinstance(labels, list) and labels:
            label_idx = labels[0]
        elif isinstance(labels, int):
            label_idx = labels
        else:
            label_idx = 27  # neutral
        if isinstance(label_idx, int) and isinstance(label_names, list) and 0 <= label_idx < len(label_names):
            label = label_names[label_idx]
        else:
            label = str(label_idx)
        samples.append(SampleRecord(text=str(text), label=label))
    if not samples:
        raise RuntimeError("No usable sentiment samples were loaded from go_emotions")
    return samples


def load_dual_datasets(target: DatasetTarget = "both") -> DatasetBundle:
    """Load training datasets from Hugging Face."""

    if target not in {"both", "intent", "sentiment"}:
        raise ValueError(f"Unsupported target '{target}'. Expected one of: both, intent, sentiment")

    try:
        import datasets  # noqa: F401
    except ImportError as e:
        raise RuntimeError("The 'datasets' package is required for training data loading") from e

    intent_samples: list[SampleRecord] = []
    sentiment_samples: list[SampleRecord] = []

    if target in {"both", "intent"}:
        logger.info("Loading intent dataset: mteb/banking77")
        intent_samples = _load_intent_samples()
        logger.info(f"Loaded {len(intent_samples)} intent samples")

    if target in {"both", "sentiment"}:
        logger.info("Loading sentiment dataset: go_emotions")
        sentiment_samples = _load_sentiment_samples()
        logger.info(f"Loaded {len(sentiment_samples)} sentiment samples")

    return DatasetBundle(intent_samples=intent_samples, sentiment_samples=sentiment_samples)


def prepare_samples(samples: Iterable[SampleRecord]) -> list[tuple[list[str], str]]:
    return [(preprocess_text(sample.text), sample.label) for sample in samples]
