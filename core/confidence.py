def compute_confidence(ranked_options, weights, evidence_score):
    """
    Confidence based on:
    - gap between top 2 options
    - balance of weights
    - evidence completeness
    """

    if len(ranked_options) < 2:
        return 0.5

    top = ranked_options[0]["score"]
    second = ranked_options[1]["score"]

    # 1. score gap (bigger gap = higher confidence)
    score_gap = top - second

    # normalize gap (0–1)
    gap_score = min(score_gap / 0.5, 1.0)

    # 2. weight balance (avoid dominance)
    max_weight = max(weights.values())
    balance_score = 1 - max_weight  # if one weight dominates → low confidence

    # 3. evidence completeness
    evidence = evidence_score  # already 0–1

    # final weighted confidence
    confidence = (
        0.4 * gap_score +
        0.3 * balance_score +
        0.3 * evidence
    )

    return round(confidence, 3)