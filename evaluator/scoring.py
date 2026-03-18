def calculate_score(option_scores: dict, weights: dict) -> tuple[float, dict]:
    """
    Returns:
      - total score (float)
      - breakdown per criterion (dict)
    weights should be numbers (like 30, 20...) or decimals (0.3, 0.2...).
    """
    total_weight = sum(weights.values()) or 1

    breakdown = {}
    total = 0.0

    for key, score in option_scores.items():
        w = weights.get(key, 0)
        contribution = (score * w) / total_weight
        breakdown[key] = round(contribution, 2)
        total += contribution

    return round(total, 2), breakdown
