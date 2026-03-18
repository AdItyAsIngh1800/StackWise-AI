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


def normalize_weights(weights):
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weights sum must be greater than zero.")
    return {k: v / total for k, v in weights.items()}


def score_option(option, weights):
    scores = BASE_SCORES.get(option)
    if scores is None:
        raise ValueError(f"Unknown option: {option}")

    total = 0.0
    for criterion, weight in weights.items():
        total += weight * scores[criterion]
    return total


def rank_options(options, weights, penalties):
    results = []

    for opt in options:
        base_score = score_option(opt, weights)
        penalty = penalties.get(opt, 0.0)
        final_score = base_score + penalty

        results.append(
            {
                "name": opt,
                "base_score": round(base_score, 3),
                "penalty": round(penalty, 3),
                "score": round(final_score, 3),
            }
        )

    return sorted(results, key=lambda x: x["score"], reverse=True)


def get_option_tradeoff_view(options):
    rows = []
    for opt in options:
        row = {"name": opt}
        row.update(BASE_SCORES[opt])
        rows.append(row)
    return rows