from __future__ import annotations

from typing import Any, Dict, List

from evidence.language_signals import get_language_signal


def explain_top_choice(
    ranked_languages: List[Dict[str, Any]],
    context: Dict[str, Any],
) -> Dict[str, Any]:
    if len(ranked_languages) < 2:
        return {"summary": "Not enough candidates for comparison.", "details": []}

    winner = ranked_languages[0]
    runner_up = ranked_languages[1]

    winner_lang = winner["language"]
    runner_lang = runner_up["language"]

    winner_score = float(winner["score"])
    runner_score = float(runner_up["score"])

    score_gap = round(winner_score - runner_score, 3)

    explanations: List[str] = []

    # --- 1. Signals comparison ---
    w_sig = get_language_signal(winner_lang)
    r_sig = get_language_signal(runner_lang)

    def compare_signal(name: str, label: str):
        w = float(w_sig.get(name, 0))
        r = float(r_sig.get(name, 0))
        diff = round(w - r, 3)

        if diff > 0.05:
            explanations.append(f"better {label} (+{diff})")
        elif diff < -0.05:
            explanations.append(f"weaker {label} ({diff})")

    compare_signal("ecosystem", "ecosystem support")
    compare_signal("activity", "community activity")
    compare_signal("popularity", "adoption/popularity")

    # --- 2. Team alignment ---
    team_languages = context.get("team_languages", [])

    if isinstance(team_languages, str):
        team_languages = [team_languages]

    team_languages = [str(x).lower() for x in team_languages]

    winner_in_team = winner_lang in team_languages
    runner_in_team = runner_lang in team_languages

    if winner_in_team and not runner_in_team:
        explanations.append("better team alignment")
    elif not winner_in_team and runner_in_team:
        explanations.append("worse team alignment")

    # --- 3. Context-based reasoning ---
    if context.get("low_ops"):
        explanations.append("lower operational overhead")

    if context.get("prefer_enterprise"):
        explanations.append("better enterprise readiness")

    if context.get("prototype_only"):
        explanations.append("faster prototyping")

    if context.get("prefer_portability"):
        explanations.append("better portability")

    # --- 4. Final summary ---
    if explanations:
        summary = (
            f"{winner_lang} ranked higher than {runner_lang} "
            f"by {score_gap} due to " + ", ".join(explanations[:3]) + "."
        )
    else:
        summary = (
            f"{winner_lang} slightly outperformed {runner_lang} "
            f"based on overall model scoring."
        )

    return {
        "summary": summary,
        "winner": winner_lang,
        "runner_up": runner_lang,
        "score_gap": score_gap,
        "details": explanations,
    }