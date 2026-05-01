from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class PredictionItem(BaseModel):
    label: str
    probability: float


class ModelResponse(BaseModel):
    top_5: list[PredictionItem]
    warning: bool


class AnalyzeResponse(BaseModel):
    embedding: list[float]
    intent: ModelResponse
    sentiment: ModelResponse