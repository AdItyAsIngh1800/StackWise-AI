from __future__ import annotations

import random
import requests

API_URL = "http://127.0.0.1:8000/feedback"

PROJECT_TYPES = ["api", "web", "ai-ml", "enterprise"]
SCALES = ["medium", "high"]
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
        "team_languages": random.sample(LANGUAGES, k=random.randint(1, 3)),
    }


def choose_best_language(context):
    if context["project_type"] == "ai-ml":
        if context["expected_scale"] == "high":
            return "python" if context["low_ops"] else "go"
        return random.choice(["python", "go"])

    if context["project_type"] == "enterprise":
        if context["prefer_enterprise"]:
            return random.choice(["java", "go"])
        return random.choice(["go", "python"])

    if context["project_type"] == "web":
        if context["prototype_only"]:
            return random.choice(["typescript", "javascript"])
        return random.choice(["typescript", "python"])

    if context["needs_cache"] and context["expected_scale"] == "high":
        return random.choice(["go", "rust"])

    if context["low_ops"]:
        return random.choice(["python", "go"])

    if context["prefer_portability"]:
        return random.choice(["go", "rust", "python"])

    return random.choice(["python", "go", "java", "typescript"])


def choose_recommended_language(context, selected):
    if random.random() < 0.7:
        return selected
    choices = [lang for lang in LANGUAGES if lang != selected]
    return random.choice(choices)


def send_feedback(n=50):
    success = 0
    failure = 0

    for i in range(n):
        context = generate_context()
        selected = choose_best_language(context)
        recommended = choose_recommended_language(context, selected)

        payload = {
            "run_id": None,
            **context,
            "recommended_language": recommended,
            "selected_language": selected,
        }

        try:
            res = requests.post(API_URL, json=payload, timeout=5)

            if res.status_code == 200:
                success += 1
            else:
                failure += 1
                print(f"[{i}] HTTP {res.status_code}: {res.text}")

        except Exception as e:
            failure += 1
            print(f"[{i}] Request failed: {e}")

    print(f"Inserted {success}/{n} feedback rows")
    print(f"Failed {failure}/{n} feedback rows")


if __name__ == "__main__":
    send_feedback(50)