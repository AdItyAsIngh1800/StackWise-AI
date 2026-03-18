from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.scenarios import save_scenario, load_scenario

router = APIRouter()


class ScenarioSaveRequest(BaseModel):
    payload: dict
    result: dict


@router.post("/scenario/save")
def save_scenario_route(req: ScenarioSaveRequest):
    scenario_id = save_scenario(req.payload, req.result)
    return {"scenario_id": scenario_id}


@router.get("/scenario/{scenario_id}")
def get_scenario(scenario_id: str):
    data = load_scenario(scenario_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return data