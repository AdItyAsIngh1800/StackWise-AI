from evaluator.scoring import calculate_score

def test_portability_high_eks_wins():
    ecs = {"portability": 5}
    eks = {"portability": 9}
    weights = {"portability": 100}

    ecs_total, _ = calculate_score(ecs, weights)
    eks_total, _ = calculate_score(eks, weights)

    assert eks_total > ecs_total

def test_ops_simplicity_high_ecs_wins():
    ecs = {"ops_simplicity": 8}
    eks = {"ops_simplicity": 5}
    weights = {"ops_simplicity": 100}

    ecs_total, _ = calculate_score(ecs, weights)
    eks_total, _ = calculate_score(eks, weights)

    assert ecs_total > eks_total
