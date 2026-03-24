from __future__ import annotations

from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd

MODEL_PATH = Path("engine/ml/model.pkl")
TRAINING_DATA_PATH = Path("data/processed/training_data.csv")


def train_model() -> None:
    df = pd.read_csv(TRAINING_DATA_PATH)

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
        "ecosystem",
        "activity",
        "popularity",
    ]

    X = df[feature_columns]
    y = df["label"]
    group = df.groupby("query_id").size().tolist()

    model = lgb.LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        eval_at=[1, 3, 5],
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42,
    )

    model.fit(X, y, group=group)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()