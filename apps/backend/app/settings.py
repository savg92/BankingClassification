from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from os import getenv
from pathlib import Path


@dataclass(slots=True)
class AppSettings:
    api_base_url: str = "http://localhost:8000"
    litellm_model: str = "openai/text-embedding-3-small"
    litellm_api_base: str = "http://localhost:1234/v1"
    litellm_api_key: str | None = None
    artifact_dir: Path = Path(__file__).resolve().parents[3] / "artifacts"


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    def _strip_quotes(value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        return value

    api_base = _strip_quotes(getenv("API_BASE_URL", "http://localhost:8000"))
    model = _strip_quotes(getenv("LITELLM_MODEL", "openai/text-embedding-3-small"))
    api_base_lm = _strip_quotes(getenv("LITELLM_API_BASE", "http://localhost:1234/v1"))
    api_key = _strip_quotes(getenv("LITELLM_API_KEY"))

    return AppSettings(
        api_base_url=api_base,
        litellm_model=model,
        litellm_api_base=api_base_lm,
        litellm_api_key=api_key,
    )