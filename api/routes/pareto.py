from fastapi import APIRouter
from core.scoring import get_option_tradeoff_view
from core.pareto import pareto_frontier

router = APIRouter()


@router.get("/pareto")
def get_pareto():
    options = ["ECS", "EKS", "Lambda"]
    rows = get_option_tradeoff_view(options)
    frontier = pareto_frontier(rows)
    return {"pareto_frontier": frontier}