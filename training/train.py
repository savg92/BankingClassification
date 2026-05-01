from __future__ import annotations

from training.banking_classification_training.pipeline import run_training_pipeline


def main() -> None:
    result = run_training_pipeline()
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()