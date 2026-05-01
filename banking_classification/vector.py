from __future__ import annotations

from hashlib import sha256

from .text import tokenize_text


EMBEDDING_DIMENSION = 768


def _stable_float(token: str, index: int) -> float:
    digest = sha256(f"{token}:{index}".encode("utf-8")).hexdigest()
    raw = int(digest[:12], 16)
    return (raw / 0xFFFFFFFFFFFF) * 2.0 - 1.0


def embed_text(text: str, dimension: int = EMBEDDING_DIMENSION) -> list[float]:
    """Create a deterministic embedding vector without external AI services."""

    vector = [0.0] * dimension
    tokens = tokenize_text(text)
    if not tokens:
        return vector

    for token in tokens:
        for index in range(dimension):
            vector[index] += _stable_float(token, index) / len(tokens)

    return vector


def batch_embed_texts(texts: list[str], dimension: int = EMBEDDING_DIMENSION) -> list[list[float]]:
    """Embed a batch of texts deterministically."""

    return [embed_text(text, dimension=dimension) for text in texts]