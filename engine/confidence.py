from __future__ import annotations

from typing import List, Dict, Any
import math

from evidence.language_signals import get_language_signal


def _softmax(scores: List[float]) -> List[float]:
    if not scores:
        return []

    max_score = max(scores)  # for numerical stability
    exp_scores = [math.exp(s - max_score) for s in scores]
    total = sum(exp_scores)

    return [s / total for s in exp_scores]


def _normalize_gap(prob_gap: float) -> float:
    # already between 0–1, just scale slightly
    return min(prob_gap * 2.0, 1.0)


def compute_confidence(
    ranked_languages: List[Dict[str, Any]],
    context: Dict[str, Any],
) -> float:
    if not ranked_languages:
        return 0.0

    # --- 1. Convert ranking scores → probabilities ---
    raw_scores = [float(item.get("score", 0.0)) for item in ranked_languages]
    probs = _softmax(raw_scores)

    top_prob = probs[0]
    second_prob = probs[1] if len(probs) > 1 else 0.0

    # --- 2. Score gap (relative confidence) ---
    prob_gap = top_prob - second_prob
    gap_score = _normalize_gap(prob_gap)

    # --- 3. Evidence strength ---
    top_lang = str(ranked_languages[0].get("language", "")).lower()
    signals = get_language_signal(top_lang)

    evidence_strength = (
        0.4 * float(signals.get("popularity", 0.0)) +
        0.3 * float(signals.get("maturity", 0.0)) +
        0.3 * float(signals.get("activity", 0.0))
    )

    # --- 4. Team alignment ---
    team_languages = context.get("team_languages", [])

    if isinstance(team_languages, str):
        team_languages = [team_languages]

    team_languages = [str(x).lower() for x in team_languages]

    if top_lang in team_languages:
        team_score = 1.0
    elif len(team_languages) == 0:
        team_score = 0.6
    else:
        team_score = 0.4

    # --- 5. Final weighted confidence ---
    confidence = (
        0.4 * gap_score +
        0.4 * evidence_strength +
        0.2 * team_score
    )

    return round(min(confidence, 1.0), 3)