from __future__ import annotations

from typing import Any

from evidence.language_signals import get_language_signal


def dominates(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """
    Returns True if a dominates b on both score and ecosystem.
    """
    better_or_equal = (
        float(a["score"]) >= float(b["score"])
        and float(a["ecosystem"]) >= float(b["ecosystem"])
    )

    strictly_better = (
        float(a["score"]) > float(b["score"])
        or float(a["ecosystem"]) > float(b["ecosystem"])
    )

    return better_or_equal and strictly_better


def compute_pareto_frontier(ranked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Compute Pareto optimal set from ranked options.

    The ranked list may only contain language + score, so we enrich each item
    with ecosystem evidence from the language signals layer.
    """
    enriched: list[dict[str, Any]] = []

    for item in ranked:
        language = item["language"]
        signals = get_language_signal(language)

        enriched.append(
            {
                "language": language,
                "score": float(item.get("score", 0.0)),
                "ecosystem": float(signals.get("ecosystem", 0.0)),
            }
        )

    pareto_set: list[dict[str, Any]] = []

    for candidate in enriched:
        is_dominated = False

        for other in enriched:
            if other["language"] == candidate["language"]:
                continue

            if dominates(other, candidate):
                is_dominated = True
                break

        if not is_dominated:
            pareto_set.append(candidate)

    return pareto_set