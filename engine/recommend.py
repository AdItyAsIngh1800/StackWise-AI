from __future__ import annotations

from typing import Any

from engine.scoring import rank_languages
from engine.confidence import compute_confidence
from engine.sensitivity import run_sensitivity_analysis
from engine.pareto import compute_pareto_frontier
from engine.similarity import find_similar_stacks
from engine.ml.predict import rank_with_model


LANGUAGE_TO_BACKEND_FRAMEWORKS = {
    "python": "fastapi",
    "javascript": "express",
    "typescript": "nestjs",
    "java": "spring boot",
    "go": "gin",
    "rust": "actix-web",
}

LANGUAGE_TO_DATABASES = {
    "python": "postgresql",
    "javascript": "postgresql",
    "typescript": "postgresql",
    "java": "postgresql",
    "go": "postgresql",
    "rust": "postgresql",
}

LANGUAGE_TO_DEPLOYMENT = {
    "python": "render",
    "javascript": "render",
    "typescript": "render",
    "java": "aws ecs",
    "go": "aws ecs",
    "rust": "docker",
}


def build_recommendations(
    ranked_languages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []

    for item in ranked_languages:
        language = item["language"]
        recommendations.append(
            {
                "language": language,
                "score": float(item["score"]),
                "backend_framework": LANGUAGE_TO_BACKEND_FRAMEWORKS.get(language),
                "database": LANGUAGE_TO_DATABASES.get(language),
                "deployment": LANGUAGE_TO_DEPLOYMENT.get(language),
            }
        )

    return recommendations


def build_why_not(
    winner: dict[str, Any] | None,
    alternatives: list[dict[str, Any]],
) -> list[dict[str, str]]:
    if winner is None:
        return []

    why_not: list[dict[str, str]] = []
    winner_score = float(winner["score"])

    for alt in alternatives:
        gap = round(winner_score - float(alt["score"]), 3)
        why_not.append(
            {
                "language": str(alt["language"]),
                "reason": f"Scored lower than the selected option by {gap}.",
            }
        )

    return why_not


def build_explanation(winner: dict[str, Any] | None, context: dict[str, Any]) -> str:
    if winner is None:
        return "No suitable stack could be recommended for the provided inputs."

    language = winner["language"]
    project_type = context.get("project_type", "project")

    return (
        f"For this {project_type} profile, {language} was recommended because it "
        f"offers the strongest balance of fit, ecosystem support, and operational practicality."
    )


def recommend_stack(context: dict[str, Any]) -> dict[str, Any]:
    candidates = ["python", "javascript", "typescript", "java", "go", "rust"]

    ranked = rank_with_model(context, candidates)
    recommendations = build_recommendations(ranked)

    winner = recommendations[0] if recommendations else None
    alternatives = recommendations[1:]

    explanation = build_explanation(winner, context)
    confidence = compute_confidence(ranked, context)
    sensitivity = run_sensitivity_analysis(context, candidates)
    pareto = compute_pareto_frontier(ranked)
    why_not = build_why_not(winner, alternatives)

    similar_stacks = []
    if winner is not None:
      similar_stacks = find_similar_stacks(context, winner["language"], limit=3)

    return {
        "winner": winner,
        "alternatives": alternatives,
        "ranked_languages": ranked,
        "explanation": explanation,
        "confidence": confidence,
        "sensitivity": sensitivity,
        "pareto": pareto,
        "why_not": why_not,
        "similar_stacks": similar_stacks,
    }