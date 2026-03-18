from core.confidence import compute_confidence


def test_confidence_range():
    ranked = [
        {"name": "EKS", "score": 0.9},
        {"name": "ECS", "score": 0.7},
    ]
    weights = {
        "cost": 0.2,
        "scalability": 0.3,
        "portability": 0.2,
        "ops_simplicity": 0.15,
        "time_to_market": 0.15,
    }
    score = compute_confidence(ranked, weights, evidence_score=0.8)
    assert 0 <= score <= 1