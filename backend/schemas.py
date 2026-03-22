from __future__ import annotations

from typing import Any, List, Optional
from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    project_type: str
    team_languages: List[str] = []
    low_ops: bool = False
    expected_scale: str = "medium"

    prefer_enterprise: bool = False
    prototype_only: bool = False
    rapid_schema_changes: bool = False
    needs_cache: bool = False
    prefer_portability: bool = False


class StackRecommendation(BaseModel):
    language: str
    score: float
    backend_framework: Optional[str]
    database: Optional[str]
    deployment: Optional[str]


class RecommendationResponse(BaseModel):
    winner: Optional[StackRecommendation]
    alternatives: List[StackRecommendation]
    ranked_languages: List[dict[str, Any]]
    explanation: Optional[str]
    confidence: float | None = None
    sensitivity: dict[str, Any] | None = None
    pareto: List[dict[str, Any]] | None = None
    why_not: List[dict[str, str]] | None = None