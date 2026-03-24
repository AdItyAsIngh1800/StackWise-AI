from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    NaturalLanguageRecommendationRequest,
    NaturalLanguageRecommendationResponse,
    FeedbackRequest,
    FeedbackResponse,
)
from database.operations import (
    create_recommendation_run,
    create_scenario,
    get_recommendation_run,
    get_runs_for_scenario,
    get_scenario_by_id,
    list_recommendation_runs,
    list_scenarios,
    create_feedback,
)
from database.queries import (
    get_avg_confidence,
    get_confidence_trend,
    get_runs_by_project_type,
    get_top_languages,
    get_top_stacks,
)
from engine.embeddings import semantic_search
from engine.ml.evaluate_model import evaluate
from engine.nl_parser import parse_natural_language_query
from engine.recommend import recommend_stack

app = FastAPI(title="StackWise-AI")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "message": "StackWise-AI API",
        "description": "Explainable decision-support system for tech stack selection",
    }


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(
    request: RecommendationRequest,
    scenario_name: str | None = Query(default=None),
):
    try:
        context = request.model_dump()
        result = recommend_stack(context)

        scenario_id = None
        if scenario_name:
            scenario_id = create_scenario(scenario_name)

        create_recommendation_run(
            request_data=context,
            result_data=result,
            scenario_id=scenario_id,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/recommend/natural-language",
    response_model=NaturalLanguageRecommendationResponse,
)
def recommend_from_text(request: NaturalLanguageRecommendationRequest):
    try:
        parsed = parse_natural_language_query(request.query)
        parsed_request = RecommendationRequest(**parsed)
        result = recommend_stack(parsed_request.model_dump())

        return {
            "parsed_input": parsed_request,
            "recommendation": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    try:
        payload = request.model_dump()
        result = create_feedback(payload)

        return {
            "status": "ok",
            "accepted": bool(result["accepted"]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/semantic-search")
def semantic_search_api(query: str, top_k: int = 3):
    try:
        from engine.embeddings import semantic_search
        return semantic_search(query, top_k=top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ml/evaluation")
def ml_evaluation():
    try:
        return evaluate()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scenarios")
def get_all_scenarios():
    try:
        return list_scenarios()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scenarios/{scenario_id}")
def get_scenario_detail(scenario_id: int):
    try:
        scenario = get_scenario_by_id(scenario_id)

        if scenario is None:
            raise HTTPException(status_code=404, detail="Scenario not found")

        runs = get_runs_for_scenario(scenario_id)

        return {
            "scenario": scenario,
            "runs": runs,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/runs/{run_id}")
def get_run_detail(run_id: int):
    try:
        result = get_recommendation_run(run_id)

        if result is None:
            raise HTTPException(status_code=404, detail="Run not found")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/top-languages")
def top_languages():
    try:
        return get_top_languages()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/confidence")
def avg_confidence():
    try:
        value = get_avg_confidence()
        return {"average_confidence": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/confidence-trend")
def confidence_trend():
    try:
        return get_confidence_trend()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/top-stacks")
def top_stacks():
    try:
        return get_top_stacks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/project-types")
def project_type_distribution():
    try:
        return get_runs_by_project_type()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/recent-runs")
def recent_runs():
    try:
        return list_recommendation_runs(limit=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))