from __future__ import annotations

from fastapi import FastAPI

from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
)
from engine.recommend import recommend_stack


app = FastAPI(
    title="StackWise-AI API",
    version="1.0.0",
    description="AI-powered tech stack recommendation service",
)


@app.get("/")
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
        "core_modules": [
            "catalog",
            "evidence",
            "engine",
            "backend",
            "frontend",
        ],
        "available_routes": {
            "root": "/",
            "health": "/health",
            "recommend": "/recommend",
            "docs": "/docs",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    result = recommend_stack(request.model_dump())
    return result