from __future__ import annotations

import random
import requests

API_URL = "http://127.0.0.1:8000/feedback"

PROJECT_TYPES = ["api", "web"]
SCALES = ["low", "medium", "high"]
LANGUAGES = ["python", "javascript", "typescript", "java", "go", "rust"]

def generate_context():
    return {
        "project_type": random.choice(PROJECT_TYPES),
        "expected_scale": random.choice(SCALES),
        "low_ops": random.choice([True, False]),
        "prefer_enterprise": random.choice([True, False]),
        "prototype_only": random.choice([True, False]),
        "rapid_schema_changes": random.choice([True, False]),
        "needs_cache": random.choice([True, False]),
        "prefer_portability": random.choice([True, False]),
        "team_languages": random.sample(LANGUAGES, k=random.randint(1, 2)),
    }

def choose_best_language(context):
    # Simple heuristic (acts like “ground truth”)
    if context["project_type"] == "api":
        if context["low_ops"]:
            return "python"
        if context["expected_scale"] == "high":
            return "go"
        return "java"
    else:
        return "typescript"

def send_feedback(n=100):
    success = 0

    for i in range(n):
        context = generate_context()
        selected = choose_best_language(context)

        payload = {
            "run_id": None,
            **context,
            "recommended_language": selected,
            "selected_language": selected,
        }

        try:
            res = requests.post(API_URL, json=payload, timeout=3)
            if res.status_code == 200:
                success += 1
        except Exception:
            pass

    print(f"Inserted {success}/{n} feedback rows")

if __name__ == "__main__":
    send_feedback(100)