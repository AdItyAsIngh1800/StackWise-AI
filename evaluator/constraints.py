def check_constraints(option_data: dict, needs_kubernetes: bool) -> bool:
    """
    Returns True if the option is allowed, False if it breaks hard requirements.
    """
    if needs_kubernetes and not option_data["hard_constraints"]["needs_kubernetes"]:
        return False
    return True