CRITERIA = ["cost", "scalability", "portability", "ops_simplicity", "time_to_market"]


def is_dominated(a, b):
    return (
        all(b[k] >= a[k] for k in CRITERIA) and
        any(b[k] > a[k] for k in CRITERIA)
    )


def pareto_frontier(options_scores):
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