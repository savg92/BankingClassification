from __future__ import annotations

import argparse
import os

from training.banking_classification_training.pipeline import run_training_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Banking Classification training pipeline")
    parser.add_argument(
        "--target",
        choices=["both", "intent", "sentiment"],
        default=os.getenv("TRAIN_TARGET", "both"),
        help="Which dataset/model(s) to train",
    )
    args = parser.parse_args()
    result = run_training_pipeline(target=args.target)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
