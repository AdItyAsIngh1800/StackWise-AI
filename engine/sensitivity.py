from __future__ import annotations

from typing import Dict, List

from engine.scoring import rank_languages


def run_sensitivity_analysis(
    context: Dict,
    base_candidates: List[str],
) -> Dict:
    """
    Test how stable the recommendation is under small context variations
    """

    base_ranking = rank_languages(base_candidates, context)
    base_winner = base_ranking[0]["language"]

    variations = []

    # Variation 1: Remove team familiarity
    modified_context = context.copy()
    modified_context["team_languages"] = []

    ranking_no_team = rank_languages(base_candidates, modified_context)
    winner_no_team = ranking_no_team[0]["language"]

    variations.append({
        "scenario": "No team familiarity",
        "winner": winner_no_team
    })

    # Variation 2: Disable low_ops
    modified_context = context.copy()
    modified_context["low_ops"] = False

    ranking_no_ops = rank_languages(base_candidates, modified_context)
    winner_no_ops = ranking_no_ops[0]["language"]

    variations.append({
        "scenario": "No low-ops preference",
        "winner": winner_no_ops
    })

    # Variation 3: Change scale to high
    modified_context = context.copy()
    modified_context["expected_scale"] = "high"

    ranking_high_scale = rank_languages(base_candidates, modified_context)
    winner_high_scale = ranking_high_scale[0]["language"]

    variations.append({
        "scenario": "High scale requirement",
        "winner": winner_high_scale
    })

    # Stability check
    winner_changes = sum(1 for v in variations if v["winner"] != base_winner)

    stability = 1 - (winner_changes / len(variations))

    return {
        "base_winner": base_winner,
        "variations": variations,
        "stability": round(stability, 3)
    }