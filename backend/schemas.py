from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    project_type: str
    team_languages: list[str] = []
    low_ops: bool = False
    expected_scale: str = "medium"
    prefer_enterprise: bool = False
    prototype_only: bool = False
    rapid_schema_changes: bool = False
    needs_cache: bool = False
    prefer_portability: bool = False


class NaturalLanguageRecommendationRequest(BaseModel):
    query: str


class StackRecommendation(BaseModel):
    language: str
    score: float
    backend_framework: str | None = None
    database: str | None = None
    deployment: str | None = None


class RecommendationResponse(BaseModel):
    winner: StackRecommendation | None = None
    alternatives: list[StackRecommendation] = []
    ranked_languages: list[dict[str, Any]] = []
    explanation: str | None = None
    confidence: float | None = None
    sensitivity: dict[str, Any] | None = None
    pareto: list[dict[str, Any]] | None = None
    why_not: list[dict[str, str]] | None = None
    similar_stacks: list[dict[str, Any]] | None = None


class NaturalLanguageRecommendationResponse(BaseModel):
    parsed_input: RecommendationRequest
    recommendation: RecommendationResponse