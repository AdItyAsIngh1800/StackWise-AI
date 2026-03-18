from fastapi import APIRouter
from api.schemas.evaluate import EvaluateRequest
from core.constraints import filter_invalid_options, apply_penalties
from core.scoring import normalize_weights, rank_options
from core.sensitivity import sensitivity_analysis
from core.confidence import compute_confidence

router = APIRouter()


@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    options = filter_invalid_options(req.options, req.constraints.dict())

    weights = normalize_weights(req.weights)

    penalties = {
        opt: apply_penalties(opt, req.constraints.dict())
        for opt in options
    }

    ranked = rank_options(options, weights, penalties)

    sensitivity = sensitivity_analysis(options, weights, penalties)

    confidence = compute_confidence(
        ranked,
        weights,
        evidence_score=0.7  # temporary
    )

    return {
        "winner": ranked[0]["name"],
        "ranked_options": ranked,
        "sensitivity": sensitivity,
        "confidence": confidence
    }