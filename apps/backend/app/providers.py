from __future__ import annotations

import logging
from hashlib import sha256
from typing import Protocol

from banking_classification.vector import EMBEDDING_DIMENSION, embed_text

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
            logger.info(f"✓ Real embedding from {self.model} at {self.api_base}")
            return [float(value) for value in data]
        except ImportError as e:
            logger.error(f"✗ LiteLLM import failed: {e}. Falling back to deterministic embeddings.")
            return embed_text(text, dimension=EMBEDDING_DIMENSION)
        except Exception as e:
            logger.error(f"✗ LiteLLM embedding failed ({self.api_base}): {type(e).__name__}: {e}. Falling back to deterministic embeddings.")
            return embed_text(text, dimension=EMBEDDING_DIMENSION)


class DeterministicEmbeddingProvider:
    async def embed(self, text: str) -> list[float]:
        return embed_text(text, dimension=EMBEDDING_DIMENSION)