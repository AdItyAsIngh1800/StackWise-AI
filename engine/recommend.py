from __future__ import annotations

from typing import Any

from engine.scoring import rank_languages
from evidence.mappings import (
    LANGUAGE_TO_BACKEND_FRAMEWORKS,
    LANGUAGE_TO_DATABASES,
    LANGUAGE_TO_DEPLOYMENT,
)


def _pick_framework(language: str, context: dict[str, Any]) -> str | None:
    frameworks = LANGUAGE_TO_BACKEND_FRAMEWORKS.get(language, [])
    if not frameworks:
        return None

    project_type = context.get("project_type")
    prefer_enterprise = context.get("prefer_enterprise", False)
    low_ops = context.get("low_ops", False)

    if language == "python":
        if project_type == "api":
            return "fastapi"
        if prefer_enterprise:
            return "django"
        return "fastapi"

    if language == "typescript":
        if prefer_enterprise:
            return "nestjs"
        return "nestjs"

    if language == "javascript":
        return "express"

    if language == "java":
        return "spring-boot"

    if language == "go":
        return "gin"

    # fallback
    return frameworks[0]


def _pick_database(language: str, context: dict[str, Any]) -> str | None:
    databases = LANGUAGE_TO_DATABASES.get(language, [])
    if not databases:
        return None

    project_type = context.get("project_type")
    rapid_schema_changes = context.get("rapid_schema_changes", False)
    needs_cache = context.get("needs_cache", False)
    prototype_only = context.get("prototype_only", False)

    if prototype_only and "sqlite" in databases:
        return "sqlite"

    if rapid_schema_changes and "mongodb" in databases:
        return "mongodb"

    if needs_cache and "redis" in databases:
        return "redis"

    if project_type in {"api", "web", "saas", "platform"} and "postgresql" in databases:
        return "postgresql"

    return databases[0]


def _pick_deployment(language: str, context: dict[str, Any]) -> str | None:
    deployment_targets = LANGUAGE_TO_DEPLOYMENT.get(language, [])
    if not deployment_targets:
        return None

    low_ops = context.get("low_ops", False)
    project_type = context.get("project_type")
    prefer_portability = context.get("prefer_portability", False)
    expected_scale = context.get("expected_scale", "medium")

    if low_ops:
        if language in {"javascript", "typescript"} and "vercel" in deployment_targets:
            return "vercel"
        if "render" in deployment_targets:
            return "render"
        if "railway" in deployment_targets:
            return "railway"

    if prefer_portability and "docker-vm" in deployment_targets:
        return "docker-vm"

    if expected_scale == "high":
        if "kubernetes" in deployment_targets:
            return "kubernetes"
        if "ecs" in deployment_targets:
            return "ecs"

    if project_type == "web" and "vercel" in deployment_targets:
        return "vercel"

    return deployment_targets[0]


def recommend_stack(context: dict[str, Any]) -> dict[str, Any]:
    candidate_languages = [
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "php",
        "ruby",
        "rust",
    ]

    ranked_languages = rank_languages(candidate_languages, context)
    top_languages = ranked_languages[:3]

    recommendations: list[dict[str, Any]] = []

    for item in top_languages:
        language = item["language"]

        framework = _pick_framework(language, context)
        database = _pick_database(language, context)
        deployment = _pick_deployment(language, context)

        recommendations.append(
            {
                "language": language,
                "language_score": item["score"],
                "backend_framework": framework,
                "database": database,
                "deployment": deployment,
            }
        )

    winner = recommendations[0] if recommendations else None

    explanation = None
    if winner is not None:
        explanation = (
            f"{winner['language']} is recommended because it best matches the "
            f"project profile, team familiarity, operational preferences, and "
            f"ecosystem evidence. The suggested backend framework is "
            f"{winner['backend_framework']}, the database is {winner['database']}, "
            f"and the preferred deployment target is {winner['deployment']}."
        )

    return {
        "winner": winner,
        "alternatives": recommendations[1:],
        "ranked_languages": ranked_languages,
        "explanation": explanation,
    }


if __name__ == "__main__":
    sample_context = {
        "project_type": "api",
        "team_languages": ["python", "javascript"],
        "low_ops": True,
        "prefer_enterprise": False,
        "rapid_schema_changes": False,
        "needs_cache": False,
        "prototype_only": False,
        "prefer_portability": False,
        "expected_scale": "medium",
    }

    result = recommend_stack(sample_context)
    print(result)