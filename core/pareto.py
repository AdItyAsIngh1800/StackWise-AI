def is_dominated(a, b):
    return all(b[k] >= a[k] for k in a) and any(b[k] > a[k] for k in a)


def pareto_frontier(options_scores):
    """
    options_scores:
    [
        {"name": "EKS", "cost": 0.6, "scalability": 0.9},
        ...
    ]
    """

    pareto = []

    for i, opt in enumerate(options_scores):
        dominated = False

        for j, other in enumerate(options_scores):
            if i != j and is_dominated(opt, other):
                dominated = True
                break

        if not dominated:
            pareto.append(opt)

    return pareto