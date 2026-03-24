from __future__ import annotations

import numpy as np
import joblib
import pandas as pd
from sklearn.metrics import ndcg_score

MODEL_PATH = "engine/ml/model.pkl"
DATA_PATH = "data/processed/training_data.csv"


def evaluate() -> dict[str, float | int]:
    df = pd.read_csv(DATA_PATH)

    feature_columns = [
        "project_type_api",
        "expected_scale_high",
        "low_ops",
        "prefer_enterprise",
        "prototype_only",
        "rapid_schema_changes",
        "needs_cache",
        "prefer_portability",
        "team_has_language",
        "matches_team_pref",
        "low_ops_fit",
        "enterprise_fit",
        "performance_fit",
        "ecosystem",
        "activity",
        "popularity",
    ]

    model = joblib.load(MODEL_PATH)

    scores: list[float] = []

    for _, group_df in df.groupby("query_id"):
        X = group_df[feature_columns]
        y_true = group_df["label"].values.astype(float)
        y_pred = model.predict(X).astype(float)

        score = ndcg_score(
            np.array([y_true]),
            np.array([y_pred]),
        )
        scores.append(float(score))

    mean_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "ndcg": round(mean_score, 4),
        "num_samples": int(len(df)),
        "num_features": int(len(feature_columns)),
    }


if __name__ == "__main__":
    result = evaluate()
    print(result)