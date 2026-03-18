from pathlib import Path
import json
import uuid

SCENARIO_DIR = Path("data/scenarios")
SCENARIO_DIR.mkdir(parents=True, exist_ok=True)


def save_scenario(payload, result):
    scenario_id = str(uuid.uuid4())

    data = {
        "scenario_id": scenario_id,
        "input": payload,
        "result": result,
    }

    path = SCENARIO_DIR / f"{scenario_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return scenario_id


def load_scenario(scenario_id):
    path = SCENARIO_DIR / f"{scenario_id}.json"
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)