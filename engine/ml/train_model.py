from __future__ import annotations

from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd

MODEL_PATH = Path("engine/ml/model.pkl")
DATA_PATH = Path("data/processed/training_data.csv")


def train_model() -> None:
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

    missing = [c for c in feature_columns + ["label", "query_id"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Rebuild training data.")

    X = df[feature_columns]
    y = df["label"]
    group = df.groupby("query_id").size().tolist()

    model = lgb.LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=15,
        min_child_samples=5,
        min_split_gain=0.0,
        random_state=42,
    )

    model.fit(X, y, group=group, eval_at=[1, 3, 5])

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"✅ Model saved at {MODEL_PATH}")


if __name__ == "__main__":
    train_model()