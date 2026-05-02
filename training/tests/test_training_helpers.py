from __future__ import annotations

import sys
import types

import pytest

from training.banking_classification_training.data import load_dual_datasets, prepare_samples
from training.banking_classification_training.trainer import grid_search_configurations, split_train_validation


class _FakeLabelFeature:
    def __init__(self, names: list[str]) -> None:
        self.names = names


class _FakeNestedLabelFeature:
    def __init__(self, names: list[str]) -> None:
        self.feature = _FakeLabelFeature(names)


class _FakeDataset(list):
    def __init__(self, rows: list[dict[str, object]], features: dict[str, object]) -> None:
        super().__init__(rows)
        self.features = features


def _mock_datasets(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_load_dataset(name: str, split: str = "train"):
        if name == "mteb/banking77":
            return _FakeDataset(
                rows=[{"text": "check my balance", "label": 0}, {"text": "wire transfer", "label": 1}],
                features={"label": _FakeLabelFeature(["balance", "transfer"])},
            )
        if name == "go_emotions":
            return _FakeDataset(
                rows=[{"text": "great app", "labels": [0]}, {"text": "this is bad", "labels": [1]}],
                features={"labels": _FakeNestedLabelFeature(["joy", "anger"])},
            )
        raise RuntimeError(f"unexpected dataset name: {name}")

    fake_module = types.ModuleType("datasets")
    fake_module.load_dataset = fake_load_dataset  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "datasets", fake_module)


def test_training_dataset_loading_and_grid_search(monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_datasets(monkeypatch)
    bundle = load_dual_datasets()
    assert bundle.intent_samples
    assert bundle.sentiment_samples
    assert bundle.intent_samples[0].label == "balance"
    assert bundle.sentiment_samples[0].label == "joy"

    prepared = prepare_samples(bundle.intent_samples[:2])
    train_split, validation_split = split_train_validation(prepared)

    assert train_split
    assert validation_split is not None
    assert len(grid_search_configurations()) == 27


def test_training_dataset_target_filtering(monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_datasets(monkeypatch)
    intent_bundle = load_dual_datasets(target="intent")
    sentiment_bundle = load_dual_datasets(target="sentiment")
    assert intent_bundle.intent_samples and not intent_bundle.sentiment_samples
    assert sentiment_bundle.sentiment_samples and not sentiment_bundle.intent_samples
