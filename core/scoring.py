def normalize_weights(weights):
    total = sum(weights.values())
    if total == 0:
        raise ValueError("Weights sum cannot be zero")
    return {k: v / total for k, v in weights.items()}


# Base scores for options (can improve later using data)
BASE_SCORES = {
    "ECS": {
        "cost": 0.7,
        "scalability": 0.8,
        "portability": 0.5,
        "ops_simplicity": 0.7,
        "time_to_market": 0.7,
    },
    "EKS": {
        "cost": 0.6,
        "scalability": 0.95,
        "portability": 0.9,
        "ops_simplicity": 0.4,
        "time_to_market": 0.5,
    },
    "Lambda": {
        "cost": 0.8,
        "scalability": 0.85,
        "portability": 0.3,
        "ops_simplicity": 0.9,
        "time_to_market": 0.9,
    },
}


def score_option(option, weights):
    scores = BASE_SCORES.get(option)

    if not scores:
        raise ValueError(f"Unknown option: {option}")

    return sum(weights[k] * scores[k] for k in weights)


def rank_options(options, weights, penalties):
    results = []

    for opt in options:
        base_score = score_option(opt, weights)
        penalty = penalties.get(opt, 0)

        final_score = base_score + penalty

        results.append({
            "name": opt,
            "score": round(final_score, 3)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)