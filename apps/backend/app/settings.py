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
    return AppSettings(
        api_base_url=getenv("API_BASE_URL", "http://localhost:8000"),
        litellm_model=getenv("LITELLM_MODEL", "openai/text-embedding-3-small"),
        litellm_api_base=getenv("LITELLM_API_BASE", "http://localhost:1234/v1"),
        litellm_api_key=getenv("LITELLM_API_KEY"),
    )