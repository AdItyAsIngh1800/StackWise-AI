from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from backend.schemas import RecommendationRequest, RecommendationResponse
from engine.recommend import recommend_stack

from database.queries import get_top_languages, get_avg_confidence
from database.operations import list_recommendation_runs

from database.operations import (
    create_scenario,
    create_recommendation_run,
    list_scenarios,
    get_scenario_by_id,
    get_runs_for_scenario,
    get_recommendation_run,
)

app = FastAPI(title="StackWise-AI")


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
    

# ---------------------------
# Analytics: Top Languages
# ---------------------------
@app.get("/analytics/top-languages")
def top_languages():
    try:
        data = get_top_languages()
        return [
            {"language": row["winner_language"], "count": row["count"]}
            if isinstance(row, dict)
            else {"language": row[0], "count": row[1]}
            for row in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Analytics: Average Confidence
# ---------------------------
@app.get("/analytics/confidence")
def avg_confidence():
    try:
        value = get_avg_confidence()
        return {"average_confidence": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Analytics: Recent Runs
# ---------------------------
@app.get("/analytics/recent-runs")
def recent_runs():
    try:
        return list_recommendation_runs(limit=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))