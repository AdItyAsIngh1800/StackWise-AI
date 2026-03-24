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

    # build features for each candidate
    feature_rows = [build_features(context, language) for language in candidates]

    # IMPORTANT: convert to DataFrame (matches training)
    X = pd.DataFrame(feature_rows)

    # predict probabilities
    probs = np.asarray(model.predict_proba(X))

    # get probability of class 1
    if probs.ndim == 2 and probs.shape[1] > 1:
        scores = probs[:, 1]
    else:
        scores = probs.ravel()

    results: list[dict] = []
    for i, language in enumerate(candidates):
        results.append(
            {
                "language": language,
                "score": float(scores[i]),
            }
        )

    # sort descending
    results.sort(key=lambda item: item["score"], reverse=True)

    return results