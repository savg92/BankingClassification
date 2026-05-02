import os
import requests
import pytest


@pytest.mark.skipif(
    not os.getenv("LITELLM_API_BASE") or not os.getenv("LITELLM_API_KEY"),
    reason="LM Studio not configured in environment",
)
def test_litellm_http_embeddings():
    """Integration test: call LM Studio /v1/embeddings HTTP endpoint and verify shape.

    This test is skipped unless LITELLM_API_BASE and LITELLM_API_KEY are set in the test env.
    """
    api_base = os.getenv("LITELLM_API_BASE")
    if api_base.endswith("/embeddings"):
        url = api_base
    elif api_base.endswith("/v1"):
        url = api_base + "/embeddings"
    else:
        url = api_base.rstrip("/") + "/v1/embeddings"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}",
    }
    payload = {"model": "text-embedding-qwen3-embedding-0.6b", "input": ["test embedding"]}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
    except Exception as e:
        pytest.skip(f"HTTP request to LM Studio failed: {e}")

    assert resp.status_code == 200, f"Unexpected status {resp.status_code}: {resp.text[:200]}"
    j = resp.json()
    assert "data" in j and isinstance(j["data"], list)
    assert len(j["data"]) >= 1
    item = j["data"][0]
    assert "embedding" in item and isinstance(item["embedding"], list)
    # basic sanity on embedding length
    assert len(item["embedding"]) >= 10
