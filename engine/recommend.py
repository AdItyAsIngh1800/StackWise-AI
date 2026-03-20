from __future__ import annotations

from typing import Any

from engine.confidence import compute_confidence
from engine.scoring import rank_languages
from evidence.mappings import (
    LANGUAGE_TO_BACKEND_FRAMEWORKS,
    LANGUAGE_TO_DATABASES,
    LANGUAGE_TO_DEPLOYMENT,
)


def _pick_framework(language: str, context: dict[str, Any]) -> str | None:
    options = LANGUAGE_TO_BACKEND_FRAMEWORKS.get(language, [])
    if not options:
        return None

    if language == "python":
        return "fastapi"

    if language == "typescript":
        return "nestjs"

    if language == "javascript":
        return "express"

    if language == "java":
        return "spring-boot"

    if language == "go":
        return "gin"

    return options[0]


def _pick_database(language: str, context: dict[str, Any]) -> str | None:
    options = LANGUAGE_TO_DATABASES.get(language, [])
    if not options:
        return None

    if context.get("prototype_only"):
        return "sqlite" if "sqlite" in options else options[0]

    if context.get("rapid_schema_changes"):
        return "mongodb" if "mongodb" in options else options[0]

    if context.get("needs_cache"):
        return "redis" if "redis" in options else options[0]

    return "postgresql" if "postgresql" in options else options[0]


def _pick_deployment(language: str, context: dict[str, Any]) -> str | None:
    options = LANGUAGE_TO_DEPLOYMENT.get(language, [])
    if not options:
        return None

    if context.get("low_ops"):
        if "render" in options:
            return "render"
        if "railway" in options:
            return "railway"

    if context.get("expected_scale") == "high":
        if "kubernetes" in options:
            return "kubernetes"
        if "ecs" in options:
            return "ecs"

    if context.get("prefer_portability") and "docker-vm" in options:
        return "docker-vm"

    return options[0]


def recommend_stack(context: dict[str, Any]) -> dict[str, Any]:
    candidates = [
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "rust",
    ]

    ranked = rank_languages(candidates, context)
    confidence = compute_confidence(ranked, context)
    top = ranked[:3]

    recommendations: list[dict[str, Any]] = []

    for item in top:
        language = item["language"]

        recommendations.append(
            {
                "language": language,
                "score": item["score"],
                "backend_framework": _pick_framework(language, context),
                "database": _pick_database(language, context),
                "deployment": _pick_deployment(language, context),
            }
        )

    winner = recommendations[0] if recommendations else None

    explanation = None
    if winner:
        explanation = (
            f"{winner['language']} is recommended due to strong alignment with "
            f"project requirements, team familiarity, operational preference, "
            f"and ecosystem strength."
        )

    return {
        "winner": winner,
        "alternatives": recommendations[1:],
        "ranked_languages": ranked,
        "explanation": explanation,
        "confidence": confidence,
    }


if __name__ == "__main__":
    sample_context = {
        "project_type": "api",
        "team_languages": ["python"],
        "low_ops": True,
        "expected_scale": "medium",
        "prototype_only": False,
        "rapid_schema_changes": False,
        "needs_cache": False,
        "prefer_portability": False,
    }

    print(recommend_stack(sample_context))