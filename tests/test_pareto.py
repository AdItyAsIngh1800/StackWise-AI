from core.pareto import pareto_frontier


def test_pareto_returns_list():
    rows = [
        {"name": "A", "cost": 0.8, "scalability": 0.8, "portability": 0.8, "ops_simplicity": 0.8, "time_to_market": 0.8},
        {"name": "B", "cost": 0.7, "scalability": 0.7, "portability": 0.7, "ops_simplicity": 0.7, "time_to_market": 0.7},
    ]
    frontier = pareto_frontier(rows)
    assert isinstance(frontier, list)
    assert len(frontier) >= 1