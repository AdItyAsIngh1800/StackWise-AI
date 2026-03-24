from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit

MODEL_PATH = Path("engine/ml/model.pkl")
TRAINING_DATA_PATH = Path("data/processed/training_data.csv")


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

    X = df[feature_columns]
    y = df["label"]
    groups = df["query_id"]

    print("Dataset shape:", df.shape)
    print("\nLabel distribution:")
    print(y.value_counts())
    print("\nUnique queries:", groups.nunique())
    print("\nMissing values:")
    print(X.isnull().sum())

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=6,
        min_child_samples=10,
        force_row_wise=True,
        verbosity=-1,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    y_pred = np.asarray(model.predict(X_test)).ravel()
    y_proba = np.asarray(model.predict_proba(X_test))

    if y_proba.ndim == 2 and y_proba.shape[1] > 1:
        y_prob = y_proba[:, 1]
    else:
        y_prob = y_proba.ravel()

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    try:
        auc = roc_auc_score(y_test, y_prob)
        print("\nROC-AUC:", auc)
    except ValueError:
        print("\nROC-AUC could not be computed on this split.")

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
    print(f"\nSaved model to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()