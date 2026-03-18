from fastapi import FastAPI
from api.routes.evaluate import router as evaluate_router

app = FastAPI(
    title="Referee Tool API",
    description="Decision-analysis engine for infrastructure recommendation",
    version="0.2.0"
)

# Register routes
app.include_router(evaluate_router)


@app.get("/")
def root():
    return {"message": "Referee Tool API is running"}