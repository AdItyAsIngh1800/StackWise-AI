from __future__ import annotations

from fastapi import FastAPI

from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from database.operations import (
    get_scenario_by_id,
    get_scenarios,
    log_recommendation,
)
from engine.recommend import recommend_stack


app = FastAPI(
    title="StackWise-AI API",
    version="1.0.0",
    description="AI-powered tech stack recommendation service",
    contact={
        "name": "Aditya Singh",
    },
)


@app.get("/", tags=["Meta"])
def root():
    return {
        "project": "StackWise-AI",
        "version": "1.0.0",
        "description": (
            "StackWise-AI is a data-driven recommendation platform that helps "
            "developers choose a suitable tech stack for a new project."
        ),
        "v1_scope": [
            "language recommendation",
            "backend framework recommendation",
            "database recommendation",
            "deployment recommendation",
        ],
        "available_routes": {
            "root": "/",
            "health": "/health",
            "recommend": "/recommend",
            "scenarios": "/scenarios",
            "scenario_detail": "/scenario/{scenario_id}",
            "docs": "/docs",
        },
    }


@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok"}


@app.post("/recommend", tags=["Recommendation"], response_model=RecommendationResponse)
def recommend(
    request: RecommendationRequest,
    scenario_name: str | None = None,
):
    request_data = request.model_dump()
    result = recommend_stack(request_data)

    try:
        log_recommendation(request_data, result, scenario_name)
    except Exception as exc:
        # Logging failure should not break the recommendation response
        print(f"Database logging failed: {exc}")

    return result


@app.get("/scenarios", tags=["Scenarios"])
def list_scenarios():
    return get_scenarios()


@app.get("/scenario/{scenario_id}", tags=["Scenarios"])
def get_scenario(scenario_id: int):
    data = get_scenario_by_id(scenario_id)

    if not data:
        return {"error": "Scenario not found"}

    return data