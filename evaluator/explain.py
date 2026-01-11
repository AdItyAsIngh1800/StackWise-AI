def explain_winner(winner: str, totals: dict, weights: dict) -> str:
    """
    Creates a simple sentence explaining why winner won.
    """
    # Find top 2 most important weights
    top_criteria = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:2]
    top_criteria_names = [c[0].replace("_", " ") for c in top_criteria if c[1] > 0]

    if not top_criteria_names:
        return f"{winner} wins because it has the best overall score."

    important_text = " and ".join(top_criteria_names)
    return f"{winner} wins mainly because your most important criteria are {important_text}, and it scores strongly there."
