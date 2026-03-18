from copy import deepcopy
from core.scoring import rank_options


def sensitivity_analysis(options, base_weights, penalties):
    """
    Check how sensitive the winner is to weight changes
    """

    results = {}

    for key in base_weights:
        modified_weights = deepcopy(base_weights)

        # increase one weight
        modified_weights[key] += 0.2

        # normalize
        total = sum(modified_weights.values())
        modified_weights = {k: v / total for k, v in modified_weights.items()}

        ranked = rank_options(options, modified_weights, penalties)

        results[key] = ranked[0]["name"]

    return results