from __future__ import annotations

from fastapi import FastAPI

from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from database.operations import log_recommendation
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
            "docs": "/docs",
        },
    }


@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok"}


@app.post("/recommend", tags=["Recommendation"], response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    request_data = request.model_dump()
    result = recommend_stack(request_data)

    try:
        log_recommendation(request_data, result)
    except Exception as exc:
        # logging failure should not break recommendation response
        print(f"Database logging failed: {exc}")

    return result