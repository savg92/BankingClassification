from __future__ import annotations

import logging
from hashlib import sha256
from typing import Protocol

from banking_classification.vector import EMBEDDING_DIMENSION, embed_text, normalize_embedding

logger = logging.getLogger(__name__)


class EmbeddingProvider(Protocol):
    async def embed(self, text: str) -> list[float]:
        ...


class LiteLLMEmbeddingProvider:
    """Embedding provider with LiteLLM fallback and deterministic offline support."""

    def __init__(self, model: str, api_base: str, api_key: str | None) -> None:
        self.model = model
        self.api_base = api_base
        self.api_key = api_key

    async def embed(self, text: str) -> list[float]:
        try:
            import litellm  # type: ignore

            response = litellm.embedding(  # type: ignore[attr-defined]
                model=self.model,
                input=[text],
                api_base=self.api_base,
                api_key=self.api_key,
            )
            data = response["data"][0]["embedding"]
            # Ensure embedding matches the expected project dimension and is normalized
            raw = [float(value) for value in data]
            logger.info(f"✓ Real embedding from {self.model} at {self.api_base} (original_size={len(raw)})")
            return normalize_embedding(raw, target_dim=EMBEDDING_DIMENSION)
        except ImportError as e:
            logger.error(f"✗ LiteLLM import failed: {e}. Falling back to deterministic embeddings.")
            return normalize_embedding(embed_text(text, dimension=EMBEDDING_DIMENSION), target_dim=EMBEDDING_DIMENSION)
        except Exception as e:
            logger.error(f"✗ LiteLLM embedding failed ({self.api_base}): {type(e).__name__}: {e}. Falling back to deterministic embeddings.")
            return normalize_embedding(embed_text(text, dimension=EMBEDDING_DIMENSION), target_dim=EMBEDDING_DIMENSION)


class DeterministicEmbeddingProvider:
    async def embed(self, text: str) -> list[float]:
        return normalize_embedding(embed_text(text, dimension=EMBEDDING_DIMENSION), target_dim=EMBEDDING_DIMENSION)