from fastapi import APIRouter
from api.schemas.evaluate import EvaluateRequest
from core.constraints import filter_invalid_options, apply_penalties
from core.scoring import normalize_weights, rank_options, get_option_tradeoff_view
from core.sensitivity import sensitivity_analysis
from core.confidence import compute_confidence
from core.explain import generate_explanation

router = APIRouter()


@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    constraints = req.constraints.model_dump()

    options = filter_invalid_options(req.options, constraints)
    if not options:
        return {
            "winner": None,
            "ranked_options": [],
            "sensitivity": {},
            "confidence": 0.0,
            "explanation": "No valid options remain after applying hard constraints.",
            "pareto_input": []
        }

    weights = normalize_weights(req.weights)

    penalties = {
        opt: apply_penalties(opt, constraints)
        for opt in options
    }

    ranked = rank_options(options, weights, penalties)
    sensitivity = sensitivity_analysis(options, weights, penalties)
    confidence = compute_confidence(ranked, weights, evidence_score=0.7)

    explanation = generate_explanation(
        winner=ranked[0]["name"],
        ranked_options=ranked,
        weights=weights,
        constraints=constraints,
        sensitivity=sensitivity,
        confidence=confidence,
    )

    pareto_input = get_option_tradeoff_view(options)

    return {
        "winner": ranked[0]["name"],
        "ranked_options": ranked,
        "sensitivity": sensitivity,
        "confidence": confidence,
        "explanation": explanation,
        "pareto_input": pareto_input,
    }