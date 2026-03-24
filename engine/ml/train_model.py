from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from lightgbm import LGBMRanker
from sklearn.model_selection import GroupShuffleSplit

MODEL_PATH = Path("engine/ml/model.pkl")
TRAINING_DATA_PATH = Path("data/processed/training_data.csv")


def _build_group_sizes(query_ids: pd.Series) -> list[int]:
    # query_ids must already be ordered so equal ids are contiguous
    return query_ids.groupby(query_ids).size().tolist()


def train_model() -> None:
    df = pd.read_csv(TRAINING_DATA_PATH)

    feature_columns = [
        "project_type_api",
        "project_type_web",
        "expected_scale_low",
        "expected_scale_medium",
        "expected_scale_high",
        "low_ops",
        "prefer_enterprise",
        "prototype_only",
        "rapid_schema_changes",
        "needs_cache",
        "prefer_portability",
        "candidate_python",
        "candidate_javascript",
        "candidate_typescript",
        "candidate_java",
        "candidate_go",
        "candidate_rust",
        "team_knows_python",
        "team_knows_javascript",
        "team_knows_typescript",
        "team_knows_java",
        "team_knows_go",
        "team_knows_rust",
        "team_has_candidate_language",
        "ecosystem",
        "activity",
        "popularity",
        "is_recommended_language",
    ]

    print("Dataset shape:", df.shape)
    print("\nRelevance label distribution:")
    print(df["label"].value_counts())
    print("\nUnique queries:", df["query_id"].nunique())
    print("\nMissing values:")
    print(df[feature_columns].isnull().sum())

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(
        splitter.split(df[feature_columns], df["label"], groups=df["query_id"])
    )

    train_df = df.iloc[train_idx].sort_values("query_id").reset_index(drop=True)
    test_df = df.iloc[test_idx].sort_values("query_id").reset_index(drop=True)

    X_train = train_df[feature_columns]
    y_train = train_df["label"]
    group_train = _build_group_sizes(train_df["query_id"])

    X_test = test_df[feature_columns]
    y_test = test_df["label"]
    group_test = _build_group_sizes(test_df["query_id"])

    model = LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        ndcg_eval_at=[1, 3, 6],
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=6,
        min_child_samples=10,
        force_row_wise=True,
        verbosity=-1,
        random_state=42,
    )

    model.fit(
        X_train,
        y_train,
        group=group_train,
        eval_set=[(X_test, y_test)],
        eval_group=[group_test],
        eval_at=[1, 3, 6],
    )

    feature_importance = pd.DataFrame(
        {
            "feature": feature_columns,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    print("\nTop feature importances:")
    print(feature_importance.head(15).to_string(index=False))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nSaved ranker to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()