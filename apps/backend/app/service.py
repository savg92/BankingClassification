from __future__ import annotations

import asyncio
from pathlib import Path

from banking_classification.artifacts import ClassifierArtifact, load_artifact
from banking_classification.model import LinearTextClassifier
from banking_classification.prediction import PredictionResult

from .providers import DeterministicEmbeddingProvider, EmbeddingProvider, LiteLLMEmbeddingProvider
from .schemas import AnalyzeResponse, ModelResponse, PredictionItem
from .settings import AppSettings


def _artifact_or_default(path: Path, name: str, labels: list[str]) -> ClassifierArtifact:
    if path.exists():
        return load_artifact(path)
    hidden_size = 256
    weights = [[0.0] * hidden_size for _ in labels]
    bias = [0.0 for _ in labels]
    return ClassifierArtifact(
        name=name,
        label_names=labels,
        hidden_size=hidden_size,
        dropout=0.2,
        weights=weights,
        bias=bias,
        metadata={"source": "fallback"},
    )


def _default_intent_labels() -> list[str]:
    return [
        "account_balance",
        "card_payment",
        "cash_withdrawal",
        "beneficiary_change",
        "charge_dispute",
        "loan_application",
        "travel_notice",
        "transaction_history",
        "cash_deposit",
        "fee_inquiry",
    ]


def _default_sentiment_labels() -> list[str]:
    return ["joy", "sadness", "anger", "fear", "neutral"]


class DualInferenceService:
    def __init__(self, settings: AppSettings, provider: EmbeddingProvider | None = None) -> None:
        self.settings = settings
        self.provider = provider or LiteLLMEmbeddingProvider(
            model=settings.litellm_model,
            api_base=settings.litellm_api_base,
            api_key=settings.litellm_api_key,
        )
        intent_artifact = _artifact_or_default(
            settings.artifact_dir / "intent_model.pth",
            "intent",
            _default_intent_labels(),
        )
        sentiment_artifact = _artifact_or_default(
            settings.artifact_dir / "sentiment_model.pth",
            "sentiment",
            _default_sentiment_labels(),
        )
        self.intent_classifier = LinearTextClassifier(intent_artifact)
        self.sentiment_classifier = LinearTextClassifier(sentiment_artifact)

    async def _predict_with_classifier(self, classifier: LinearTextClassifier, embedding: list[float]) -> PredictionResult:
        return await asyncio.to_thread(classifier.predict, embedding)

    @staticmethod
    def _to_response(result: PredictionResult) -> ModelResponse:
        return ModelResponse(
            top_5=[PredictionItem(label=item.label, probability=item.probability) for item in result.predictions],
            warning=result.warning,
        )

    async def analyze(self, text: str) -> AnalyzeResponse:
        embedding = await self.provider.embed(text)
        intent_result, sentiment_result = await asyncio.gather(
            self._predict_with_classifier(self.intent_classifier, embedding),
            self._predict_with_classifier(self.sentiment_classifier, embedding),
        )
        return AnalyzeResponse(
            embedding=embedding,
            intent=self._to_response(intent_result),
            sentiment=self._to_response(sentiment_result),
        )
