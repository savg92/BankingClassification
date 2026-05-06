from __future__ import annotations

from hashlib import sha256

from .text import tokenize_text


EMBEDDING_DIMENSION = 768


def normalize_embedding(embedding: list[float], target_dim: int = EMBEDDING_DIMENSION) -> list[float]:
    """Resize an embedding to target_dim without changing magnitude.

    - If embedding is longer than target_dim, downsample by block-averaging.
    - If shorter, pad with zeros.
    - Preserve original scale (no normalization) so inference matches training statistics.
    """
    if not embedding:
        return [0.0] * target_dim

    current = len(embedding)
    if current == target_dim:
        return [float(v) for v in embedding]

    # Downsample by averaging blocks when longer
    if current > target_dim:
        result: list[float] = []
        base = current // target_dim
        rem = current % target_dim
        idx = 0
        for i in range(target_dim):
            block = base + (1 if i < rem else 0)
            if block <= 0:
                result.append(0.0)
                continue
            block_vals = embedding[idx : idx + block]
            idx += block
            result.append(sum(block_vals) / len(block_vals))
        return [float(v) for v in result]

    # current < target_dim: pad with zeros
    padded = [float(v) for v in embedding] + [0.0] * (target_dim - current)
    return padded


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