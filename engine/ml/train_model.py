from __future__ import annotations

import pandas as pd
import lightgbm as lgb
import joblib


def train_model():
    df = pd.read_csv("data/processed/training_data.csv")

    X = df.drop(columns=["label"])
    y = df["label"]

    model = lgb.LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        n_estimators=100,
    )

    # group = number of candidates per query
    group = df.groupby("query_id").size().to_list()

    model.fit(X, y, group=group)

    joblib.dump(model, "engine/ml/model.pkl")


if __name__ == "__main__":
    train_model()