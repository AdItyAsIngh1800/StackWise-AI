from __future__ import annotations

from typing import Dict

from evidence.language_signals import get_language_signal


# -----------------------------
# CONFIG (tunable later)
# -----------------------------
WEIGHTS = {
    "project_fit": 0.4,
    "team_fit": 0.25,
    "ops_fit": 0.15,
    "evidence": 0.20,
}


# -----------------------------
# MAIN SCORING FUNCTION
# -----------------------------
def score_language(language: str, context: Dict) -> float:
    score = 0.0

    # 1. Project Fit
    if context.get("project_type") == "api" and language == "python":
        score += 0.4
    if context.get("project_type") == "web" and language in ["javascript", "typescript"]:
        score += 0.4

    # 2. Team Fit
    team_languages = context.get("team_languages", [])
    if language in team_languages:
        score += 0.25

    # 3. Ops Fit
    if context.get("low_ops") and language in ["python", "javascript", "typescript"]:
        score += 0.15

    # 4. Evidence (from dataset)
    signals = get_language_signal(language)
    evidence_score = (
        0.4 * signals["popularity"]
        + 0.3 * signals["maturity"]
        + 0.3 * signals["activity"]
    )

    score += WEIGHTS["evidence"] * evidence_score

    return round(score, 4)


# -----------------------------
# RANK LANGUAGES
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