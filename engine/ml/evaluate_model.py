from __future__ import annotations

import joblib
import pandas as pd
from sklearn.metrics import ndcg_score
import numpy as np

MODEL_PATH = "engine/ml/model.pkl"
DATA_PATH = "data/processed/training_data.csv"


def evaluate():
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

    scores = []

    for _, group_df in df.groupby("query_id"):
        X = group_df[feature_columns]
        y_true = group_df["label"].values
        y_pred = model.predict(X)

        score = ndcg_score(
            np.array([y_true], dtype=float),
            np.array([y_pred], dtype=float),
        )
        scores.append(score)

    mean_score = sum(scores) / len(scores)
    print(f"✅ Mean NDCG: {mean_score:.4f}")


if __name__ == "__main__":
    evaluate()