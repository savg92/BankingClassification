from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable


TOKEN_LIMIT = 128


def normalize_text(text: str) -> str:
    """Lowercase and strip punctuation while preserving word boundaries."""

    normalized = unicodedata.normalize("NFKC", text).lower()
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[\W_]+", " ", normalized, flags=re.UNICODE)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def tokenize_text(text: str) -> list[str]:
    """Tokenize text into a whitespace-separated list."""

    normalized = normalize_text(text)
    if not normalized:
        return []
    return normalized.split(" ")


def pad_or_truncate(tokens: Iterable[str], max_length: int = TOKEN_LIMIT) -> list[str]:
    """Pad or truncate token sequences to a fixed length."""

    trimmed = list(tokens)[:max_length]
    if len(trimmed) < max_length:
        trimmed.extend(["<pad>"] * (max_length - len(trimmed)))
    return trimmed


def preprocess_text(text: str, max_length: int = TOKEN_LIMIT) -> list[str]:
    """Run the project text normalization and fixed-length token shaping."""

    return pad_or_truncate(tokenize_text(text), max_length=max_length)


@dataclass(slots=True)
class SampleRecord:
    text: str
    label: str
