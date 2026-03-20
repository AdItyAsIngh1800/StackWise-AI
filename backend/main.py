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


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    result = recommend_stack(request.dict())
    return result