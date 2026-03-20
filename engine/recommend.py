from __future__ import annotations

from typing import Any

from engine.confidence import compute_confidence
from engine.pareto import compute_pareto_frontier
from engine.scoring import rank_languages
from engine.sensitivity import run_sensitivity_analysis
from evidence.language_signals import get_language_signal
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
        if context.get("prefer_enterprise"):
            return "django" if "django" in options else options[0]
        return "fastapi" if "fastapi" in options else options[0]

    if language == "typescript":
        return "nestjs" if "nestjs" in options else options[0]

    if language == "javascript":
        return "express" if "express" in options else options[0]

    if language == "java":
        return "spring-boot" if "spring-boot" in options else options[0]

    if language == "go":
        return "gin" if "gin" in options else options[0]

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
        if language in {"javascript", "typescript"} and "vercel" in options:
            return "vercel"
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
    sensitivity = run_sensitivity_analysis(context, candidates)

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
            f"and ecosystem strength. The recommended backend framework is "
            f"{winner['backend_framework']}, the suggested database is "
            f"{winner['database']}, and the preferred deployment option is "
            f"{winner['deployment']}."
        )

    pareto_input = []
    for item in ranked:
        signals = get_language_signal(item["language"])
        pareto_input.append(
            {
                "language": item["language"],
                "score": item["score"],
                "ecosystem": signals["ecosystem"],
            }
        )

    pareto = compute_pareto_frontier(pareto_input)

    return {
        "winner": winner,
        "alternatives": recommendations[1:],
        "ranked_languages": ranked,
        "explanation": explanation,
        "confidence": confidence,
        "sensitivity": sensitivity,
        "pareto": pareto,
    }


if __name__ == "__main__":
    sample_context = {
        "project_type": "api",
        "team_languages": ["python"],
        "low_ops": True,
        "expected_scale": "medium",
        "prefer_enterprise": False,
        "prototype_only": False,
        "rapid_schema_changes": False,
        "needs_cache": False,
        "prefer_portability": False,
    }

    print(recommend_stack(sample_context))