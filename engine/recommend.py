from __future__ import annotations

from typing import Any

from engine.confidence import compute_confidence
from engine.explain import explain_top_choice
from engine.ml.predict import rank_with_model
from engine.pareto import compute_pareto_frontier
from engine.scoring import rank_languages
from engine.sensitivity import run_sensitivity_analysis
from engine.similarity import find_similar_stacks

CANDIDATES = ["python", "javascript", "typescript", "java", "go", "rust"]

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


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_recommendations(
    ranked_languages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []

    for item in ranked_languages:
        language = str(item.get("language", "")).strip().lower()
        score = _safe_float(item.get("score"), 0.0)

        recommendations.append(
            {
                "language": language,
                "score": score,
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
    winner_score = _safe_float(winner.get("score"), 0.0)

    for alt in alternatives:
        alt_language = str(alt.get("language", "")).strip().lower()
        alt_score = _safe_float(alt.get("score"), 0.0)
        gap = round(winner_score - alt_score, 3)

        why_not.append(
            {
                "language": alt_language,
                "reason": f"Scored lower than the selected option by {gap}.",
            }
        )

    return why_not


def build_explanation(
    winner: dict[str, Any] | None,
    context: dict[str, Any],
) -> str:
    if winner is None:
        return "No suitable stack could be recommended for the provided inputs."

    language = str(winner.get("language", "unknown")).strip().lower()
    project_type = str(context.get("project_type", "project")).strip().lower()
    expected_scale = str(context.get("expected_scale", "unknown")).strip().lower()

    reasons: list[str] = []

    if project_type == "api":
        reasons.append("backend suitability")
    elif project_type == "web":
        reasons.append("web application fit")
    else:
        reasons.append("overall project fit")

    if expected_scale == "high":
        reasons.append("scalability considerations")

    if bool(context.get("low_ops")):
        reasons.append("lower operational overhead")

    if bool(context.get("prefer_enterprise")):
        reasons.append("enterprise readiness")

    if bool(context.get("prototype_only")):
        reasons.append("rapid prototyping speed")

    if bool(context.get("prefer_portability")):
        reasons.append("portability")

    if not reasons:
        reasons.append("overall balance")

    joined_reasons = ", ".join(reasons[:3])

    return (
        f"For this {project_type} profile, {language} was recommended because it "
        f"showed the strongest balance of {joined_reasons}."
    )


def recommend_stack(context: dict[str, Any]) -> dict[str, Any]:
    try:
        ranked = rank_with_model(context, CANDIDATES)
        ranking_source = "ml_model"
    except FileNotFoundError:
        ranked = rank_languages(CANDIDATES, context)
        ranking_source = "rules_fallback"

    recommendations = build_recommendations(ranked)

    winner = recommendations[0] if recommendations else None
    alternatives = recommendations[1:]

    explanation = build_explanation(winner, context)
    explanation_details = explain_top_choice(ranked, context)
    confidence = compute_confidence(ranked, context)
    sensitivity = run_sensitivity_analysis(context, CANDIDATES)
    pareto = compute_pareto_frontier(ranked)
    why_not = build_why_not(winner, alternatives)

    similar_stacks: list[dict[str, Any]] = []
    if winner is not None:
        similar_stacks = find_similar_stacks(
            context,
            str(winner["language"]),
            limit=3,
        )

    return {
        "winner": winner,
        "alternatives": alternatives,
        "ranked_languages": ranked,
        "explanation": explanation,
        "explanation_details": explanation_details,
        "confidence": confidence,
        "sensitivity": sensitivity,
        "pareto": pareto,
        "why_not": why_not,
        "similar_stacks": similar_stacks,
        "ranking_source": ranking_source,
    }