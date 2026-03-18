from fastapi import FastAPI
from api.routes.evaluate import router as evaluate_router
from api.routes.pareto import router as pareto_router

app = FastAPI(
    title="StackWise AI",
    description="Explainable Decision Intelligence Platform",
    version="0.2.0"
)

app.include_router(evaluate_router)
app.include_router(pareto_router)


@app.get("/")
def root():
    return {"message": "StackWise AI API is running"}