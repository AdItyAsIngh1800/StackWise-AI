from __future__ import annotations

from typing import Dict, List


def dominates(a: Dict, b: Dict) -> bool:
    """
    Returns True if a dominates b
    """
    better_or_equal = (
        a["score"] >= b["score"] and
        a["ecosystem"] >= b["ecosystem"]
    )

    strictly_better = (
        a["score"] > b["score"] or
        a["ecosystem"] > b["ecosystem"]
    )

    return better_or_equal and strictly_better


def compute_pareto_frontier(ranked: List[Dict]) -> List[Dict]:
    """
    Compute Pareto optimal set from ranked options
    """

    pareto_set = []

    for candidate in ranked:
        is_dominated = False

        for other in ranked:
            if other == candidate:
                continue

            if dominates(other, candidate):
                is_dominated = True
                break

        if not is_dominated:
            pareto_set.append(candidate)

    return pareto_set