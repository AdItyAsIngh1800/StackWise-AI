from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from engine.ml.features import build_features

MODEL_PATH = Path("engine/ml/model.pkl")


def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def rank_with_model(context: dict[str, Any], candidates: list[str]) -> list[dict]:
    model = load_model()
    if model is None:
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    feature_rows = [build_features(context, language) for language in candidates]
    X = pd.DataFrame(feature_rows)

    # Keep inference column order aligned with training.
    if hasattr(model, "feature_name_"):
        X = X.reindex(columns=list(model.feature_name_), fill_value=0)

    scores = np.asarray(model.predict(X)).ravel()

    results: list[dict] = []
    for i, language in enumerate(candidates):
        results.append(
            {
                "language": language,
                "score": float(scores[i]),
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results