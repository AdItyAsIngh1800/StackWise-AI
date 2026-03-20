from __future__ import annotations

from typing import Dict

from evidence.language_signals import get_language_signal


# -----------------------------
# Weights (tunable later)
# -----------------------------
WEIGHTS = {
    "project_fit": 0.35,
    "team_fit": 0.20,
    "ops_fit": 0.15,
    "evidence": 0.30,
}


# -----------------------------
# Scoring Components
# -----------------------------
def _score_project_fit(language: str, context: Dict) -> float:
    project_type = context.get("project_type")

    if project_type == "api":
        return 1.0 if language in ["python", "go", "javascript"] else 0.6

    if project_type == "web":
        return 1.0 if language in ["javascript", "typescript"] else 0.7

    if project_type == "ai-ml":
        return 1.0 if language == "python" else 0.5

    if project_type == "enterprise":
        return 1.0 if language in ["java", "typescript"] else 0.6

    return 0.7


def _score_team_fit(language: str, context: Dict) -> float:
    team_languages = context.get("team_languages", [])

    if not team_languages:
        return 0.5

    return 1.0 if language in team_languages else 0.4


def _score_ops_fit(language: str, context: Dict) -> float:
    low_ops = context.get("low_ops", False)

    if not low_ops:
        return 0.7

    if language in ["python", "javascript", "typescript"]:
        return 1.0

    return 0.6


def _score_evidence(language: str) -> float:
    signals = get_language_signal(language)

    return (
        0.4 * signals["popularity"]
        + 0.3 * signals["maturity"]
        + 0.3 * signals["activity"]
    )


# -----------------------------
# Final Score
# -----------------------------
def score_language(language: str, context: Dict) -> float:
    project_fit = _score_project_fit(language, context)
    team_fit = _score_team_fit(language, context)
    ops_fit = _score_ops_fit(language, context)
    evidence = _score_evidence(language)

    final_score = (
        WEIGHTS["project_fit"] * project_fit
        + WEIGHTS["team_fit"] * team_fit
        + WEIGHTS["ops_fit"] * ops_fit
        + WEIGHTS["evidence"] * evidence
    )

    return round(final_score, 4)


# -----------------------------
# Ranking
# -----------------------------
def rank_languages(languages: list[str], context: Dict) -> list[dict]:
    results = []

    for lang in languages:
        score = score_language(lang, context)

        results.append({
            "language": lang,
            "score": score
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)