def generate_explanation(winner, ranked_options, weights, constraints, sensitivity, confidence):
    top_weight = max(weights, key=weights.get)
    runner_up = ranked_options[1]["name"] if len(ranked_options) > 1 else None
    score_gap = (
        round(ranked_options[0]["score"] - ranked_options[1]["score"], 3)
        if len(ranked_options) > 1
        else 0
    )

    reasons = []

    reasons.append(
        f"{winner} ranks highest overall, with {top_weight.replace('_', ' ')} being the most influential criterion."
    )

    if constraints.get("need_kubernetes"):
        reasons.append("Kubernetes was required, so Lambda was excluded by a hard constraint.")

    if constraints.get("low_ops_capacity") and winner != "EKS":
        reasons.append("Low operations capacity reduced the attractiveness of EKS.")

    if constraints.get("vendor_neutrality"):
        reasons.append("Vendor neutrality introduced penalties for AWS-managed lock-in options.")

    if runner_up:
        reasons.append(
            f"The margin over {runner_up} is {score_gap}, which helps indicate decision strength."
        )

    unstable_factors = [
        k for k, v in sensitivity.items() if v != winner
    ]
    if unstable_factors:
        reasons.append(
            "The winner could change if these priorities shift: "
            + ", ".join(f.replace("_", " ") for f in unstable_factors)
            + "."
        )
    else:
        reasons.append("The recommendation remains stable under the tested weight perturbations.")

    if confidence >= 0.7:
        reasons.append("Overall confidence is high.")
    elif confidence >= 0.4:
        reasons.append("Overall confidence is moderate.")
    else:
        reasons.append("Overall confidence is low, so this decision should be reviewed carefully.")

    return " ".join(reasons)