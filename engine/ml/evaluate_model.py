from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from engine.ml.predict import rank_with_model

TRAINING_DATA_PATH = Path("data/processed/training_data.csv")


def dcg(labels: list[int], k: int) -> float:
    total = 0.0
    for i, rel in enumerate(labels[:k], start=1):
        total += rel / math.log2(i + 1)
    return total


def ndcg(labels: list[int], k: int) -> float:
    actual = dcg(labels, k)
    ideal = dcg(sorted(labels, reverse=True), k)
    if ideal == 0:
        return 0.0
    return actual / ideal


def evaluate() -> dict[str, float]:
    df = pd.read_csv(TRAINING_DATA_PATH)

    grouped = df.groupby("query_id")

    accuracy_at_1 = 0
    precision_at_1 = 0
    ndcg_at_3_scores: list[float] = []
    ndcg_at_5_scores: list[float] = []

    total_queries = 0

    for _, group in grouped:
        total_queries += 1

        first = group.iloc[0]
        context = {
            "project_type": "api" if int(first["project_type_api"]) == 1 else "web",
            "expected_scale": "high" if int(first["expected_scale_high"]) == 1 else "medium",
            "low_ops": bool(first["low_ops"]),
            "prefer_enterprise": bool(first["prefer_enterprise"]),
            "prototype_only": bool(first["prototype_only"]),
            "rapid_schema_changes": bool(first["rapid_schema_changes"]),
            "needs_cache": bool(first["needs_cache"]),
            "prefer_portability": bool(first["prefer_portability"]),
            "team_languages": [],
        }

        candidates = group["language"].tolist()
        ranked = rank_with_model(context, candidates)
        ranked_languages = [item["language"] for item in ranked]

        label_map = {
            row["language"]: int(row["label"])
            for _, row in group.iterrows()
        }

        top_language = ranked_languages[0]
        top_label = label_map[top_language]

        accuracy_at_1 += 1 if top_label == 1 else 0
        precision_at_1 += 1 if top_label == 1 else 0

        ranked_labels = [label_map[lang] for lang in ranked_languages]
        ndcg_at_3_scores.append(ndcg(ranked_labels, 3))
        ndcg_at_5_scores.append(ndcg(ranked_labels, 5))

    return {
        "accuracy_at_1": round(accuracy_at_1 / total_queries, 4) if total_queries else 0.0,
        "precision_at_1": round(precision_at_1 / total_queries, 4) if total_queries else 0.0,
        "ndcg_at_3": round(sum(ndcg_at_3_scores) / len(ndcg_at_3_scores), 4) if ndcg_at_3_scores else 0.0,
        "ndcg_at_5": round(sum(ndcg_at_5_scores) / len(ndcg_at_5_scores), 4) if ndcg_at_5_scores else 0.0,
    }


if __name__ == "__main__":
    metrics = evaluate()
    print(metrics)