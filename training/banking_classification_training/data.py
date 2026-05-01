from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from banking_classification.text import SampleRecord, preprocess_text


INTENT_LABEL_COUNT = 77
SENTIMENT_LABEL_COUNT = 28


@dataclass(slots=True)
class DatasetBundle:
    intent_samples: list[SampleRecord]
    sentiment_samples: list[SampleRecord]


def _generated_labels(prefix: str, total: int) -> list[str]:
    return [f"{prefix}_{index:02d}" for index in range(1, total + 1)]


def _generate_samples(prefix: str, label_count: int) -> list[SampleRecord]:
    samples: list[SampleRecord] = []
    for index, label in enumerate(_generated_labels(prefix, label_count), start=1):
        samples.append(
            SampleRecord(
                text=f"Sample {prefix} request {index} for {label} with amount {index * 10}",
                label=label,
            )
        )
    return samples


def load_dual_datasets() -> DatasetBundle:
    """Load the dual datasets, falling back to deterministic samples offline."""

    try:
        from datasets import load_dataset  # type: ignore
    except Exception:
        return DatasetBundle(
            intent_samples=_generate_samples("intent", INTENT_LABEL_COUNT),
            sentiment_samples=_generate_samples("sentiment", SENTIMENT_LABEL_COUNT),
        )

    try:
        banking_dataset = load_dataset("Banking77", split="train")
        emotions_dataset = load_dataset("go_emotions", split="train")
    except Exception:
        return DatasetBundle(
            intent_samples=_generate_samples("intent", INTENT_LABEL_COUNT),
            sentiment_samples=_generate_samples("sentiment", SENTIMENT_LABEL_COUNT),
        )

    intent_samples = [
        SampleRecord(text=item["text"], label=str(item["label"])) for item in banking_dataset
    ]
    sentiment_samples = [
        SampleRecord(text=item["text"], label=str(item["labels"])) for item in emotions_dataset
    ]
    return DatasetBundle(intent_samples=intent_samples, sentiment_samples=sentiment_samples)


def prepare_samples(samples: Iterable[SampleRecord]) -> list[tuple[list[str], str]]:
    return [(preprocess_text(sample.text), sample.label) for sample in samples]