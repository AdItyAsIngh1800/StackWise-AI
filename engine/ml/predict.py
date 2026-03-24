from __future__ import annotations

import joblib
import numpy as np

from engine.ml.features import build_features

MODEL_PATH = "engine/ml/model.pkl"

model = joblib.load(MODEL_PATH)


def rank_with_model(context: dict, candidates: list[str]):
    features = []
    for lang in candidates:
        features.append(build_features(context, lang))

    scores = model.predict(np.array(features))

    results = []
    for i, lang in enumerate(candidates):
        results.append({
            "language": lang,
            "score": float(scores[i])
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results