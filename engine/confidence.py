from __future__ import annotations

from typing import List, Dict

from evidence.language_signals import get_language_signal


def compute_confidence(
    ranked_languages: List[Dict],
    context: Dict
) -> float:
    if not ranked_languages:
        return 0.0

    # Top scores
    top_score = ranked_languages[0]["score"]
    second_score = ranked_languages[1]["score"] if len(ranked_languages) > 1 else 0

    # 1. Score gap
    score_gap = top_score - second_score

    gap_score = min(score_gap * 2, 1.0)  # normalize

    # 2. Evidence strength
    top_lang = ranked_languages[0]["language"]
    signals = get_language_signal(top_lang)

    evidence_strength = (
        0.4 * signals["popularity"]
        + 0.3 * signals["maturity"]
        + 0.3 * signals["activity"]
    )

    # 3. Team alignment
    team_languages = context.get("team_languages", [])
    team_score = 1.0 if top_lang in team_languages else 0.5

    # Final confidence
    confidence = (
        0.4 * gap_score +
        0.4 * evidence_strength +
        0.2 * team_score
    )

    return round(min(confidence, 1.0), 3)