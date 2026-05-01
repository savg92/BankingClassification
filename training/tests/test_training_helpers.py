from training.banking_classification_training.data import load_dual_datasets, prepare_samples
from training.banking_classification_training.trainer import grid_search_configurations, split_train_validation


def test_training_fallback_datasets_and_grid_search() -> None:
    bundle = load_dual_datasets()
    assert bundle.intent_samples
    assert bundle.sentiment_samples

    prepared = prepare_samples(bundle.intent_samples[:2])
    train_split, validation_split = split_train_validation(prepared)

    assert train_split
    assert validation_split is not None
    assert len(grid_search_configurations()) == 27