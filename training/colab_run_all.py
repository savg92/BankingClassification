from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=str(cwd) if cwd else None, check=True)


def _ensure_repo(repo_url: str, repo_dir: Path, branch: str) -> None:
    if (repo_dir / ".git").exists():
        _run(["git", "fetch", "--all"], cwd=repo_dir)
        _run(["git", "checkout", branch], cwd=repo_dir)
        _run(["git", "pull", "--ff-only"], cwd=repo_dir)
        return
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    _run(["git", "clone", "--branch", branch, repo_url, str(repo_dir)])


def _install_dependencies() -> None:
    _run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "torch>=2.1.0",
            "datasets>=3.0.0",
            "numpy>=1.24.0",
            "requests>=2.31.0",
            "litellm>=1.40.0",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Colab runner for BankingClassification training")
    parser.add_argument("--repo-url", default="https://github.com/savg92/BankingClassification.git")
    parser.add_argument("--repo-dir", default="/content/BankingClassification")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--target", choices=["both", "intent", "sentiment"], default="both")
    parser.add_argument("--train-slice", type=int, default=0)
    parser.add_argument("--train-config-limit", type=int, default=9)
    parser.add_argument("--embedding-chunk-size", type=int, default=8)
    parser.add_argument("--embedding-min-chunk-size", type=int, default=1)
    parser.add_argument("--embedding-retries", type=int, default=3)
    parser.add_argument("--embedding-timeout", type=int, default=90)
    parser.add_argument("--litellm-model", default="openai/text-embedding-3-small")
    parser.add_argument("--litellm-api-base", required=True)
    parser.add_argument("--litellm-api-key", default=None)
    parser.add_argument("--hf-token", default=None)
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    _ensure_repo(args.repo_url, repo_dir, args.branch)
    _install_dependencies()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_dir)
    env["LITELLM_MODEL"] = args.litellm_model
    env["LITELLM_API_BASE"] = args.litellm_api_base
    env["EMBEDDING_CHUNK_SIZE"] = str(args.embedding_chunk_size)
    env["EMBEDDING_MIN_CHUNK_SIZE"] = str(args.embedding_min_chunk_size)
    env["EMBEDDING_RETRIES"] = str(args.embedding_retries)
    env["EMBEDDING_TIMEOUT"] = str(args.embedding_timeout)
    env["TRAIN_CONFIG_LIMIT"] = str(args.train_config_limit)
    if args.train_slice > 0:
        env["TRAIN_SLICE"] = str(args.train_slice)
    if args.litellm_api_key:
        env["LITELLM_API_KEY"] = args.litellm_api_key
    if args.hf_token:
        env["HF_TOKEN"] = args.hf_token

    subprocess.run(
        [sys.executable, "training/train.py", "--target", args.target],
        cwd=str(repo_dir),
        env=env,
        check=True,
    )


if __name__ == "__main__":
    main()
