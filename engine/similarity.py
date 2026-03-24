from __future__ import annotations

from typing import Any

from engine.scoring import rank_languages
from evidence.language_signals import get_language_signal


def _vectorize(language: str, score: float) -> list[float]:
    signals = get_language_signal(language)
    return [
        float(score),
        float(signals.get("ecosystem", 0.0)),
        float(signals.get("activity", 0.0)),
        float(signals.get("popularity", 0.0)),
    ]


def _euclidean_distance(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def find_similar_stacks(
    context: dict[str, Any],
    target_language: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    candidates = ["python", "javascript", "typescript", "java", "go", "rust"]
    ranked = rank_languages(candidates, context)

    score_map = {item["language"]: float(item["score"]) for item in ranked}

    if target_language not in score_map:
        return []

    target_vector = _vectorize(target_language, score_map[target_language])

    comparisons: list[dict[str, Any]] = []
    for language in candidates:
        if language == target_language:
            continue

        vector = _vectorize(language, score_map[language])
        distance = _euclidean_distance(target_vector, vector)

        comparisons.append(
            {
                "language": language,
                "score": score_map[language],
                "distance": round(distance, 4),
            }
        )

    comparisons.sort(key=lambda item: item["distance"])
    return comparisons[:limit]