from banking_classification.prediction import build_prediction_result, softmax, top_k_predictions
from banking_classification.text import normalize_text, pad_or_truncate, preprocess_text, tokenize_text
from banking_classification.vector import embed_text


def test_text_preprocessing_enforces_length_and_normalization() -> None:
    text = "Hello, Banking! 😊 Need help?"

    normalized = normalize_text(text)
    tokens = tokenize_text(text)
    padded = pad_or_truncate(tokens, max_length=5)
    processed = preprocess_text(text, max_length=5)

    assert normalized == "hello banking need help"
    assert tokens == ["hello", "banking", "need", "help"]
    assert len(padded) == 5
    assert processed[-1] == "<pad>"


def test_embedding_is_deterministic_and_fixed_dimension() -> None:
    vector = embed_text("transfer funds to savings")

    assert len(vector) == 768
    assert vector == embed_text("transfer funds to savings")


def test_top_k_and_warning_logic() -> None:
    result = build_prediction_result(["a", "b", "c"], [1.0, 0.5, -0.5])

    assert len(result.predictions) == 3
    assert result.predictions[0].label == "a"
    assert result.warning is False

    probabilities = softmax([1.0, 0.0])
    ranked = top_k_predictions(["x", "y"], probabilities)

    assert ranked[0].label == "x"