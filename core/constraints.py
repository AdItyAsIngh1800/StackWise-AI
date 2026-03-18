def filter_invalid_options(options, constraints):
    """
    Remove options that violate hard constraints
    """

    valid = []

    for opt in options:

        # ❌ If Kubernetes is required → Lambda not allowed
        if constraints.get("need_kubernetes") and opt == "Lambda":
            continue

        valid.append(opt)

    return valid


def apply_penalties(option, constraints):
    """
    Apply soft penalties based on constraints
    """

    penalty = 0

    # ⚠️ Low ops capacity → Kubernetes (EKS) is harder to manage
    if constraints.get("low_ops_capacity"):
        if option == "EKS":
            penalty -= 0.2

    # ⚠️ Vendor neutrality → AWS-managed services penalized slightly
    if constraints.get("vendor_neutrality"):
        if option in ["ECS", "Lambda"]:
            penalty -= 0.1

    return penalty