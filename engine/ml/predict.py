from __future__ import annotations

from typing import Any, Dict, List

import joblib
import pandas as pd

from evidence.language_signals import get_language_signal

MODEL_PATH = "engine/ml/model.pkl"

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def build_feature_row(language: str, context: Dict[str, Any]) -> Dict[str, Any]:
    signals = get_language_signal(language)
    team_languages = context.get("team_languages", [])

    return {
        "project_type_api": int(context.get("project_type") == "api"),
        "expected_scale_high": int(context.get("expected_scale") == "high"),

        "low_ops": int(context.get("low_ops", False)),
        "prefer_enterprise": int(context.get("prefer_enterprise", False)),
        "prototype_only": int(context.get("prototype_only", False)),
        "rapid_schema_changes": int(context.get("rapid_schema_changes", False)),
        "needs_cache": int(context.get("needs_cache", False)),
        "prefer_portability": int(context.get("prefer_portability", False)),

        "team_has_language": int(language in team_languages),

        # engineered features
        "matches_team_pref": int(language in team_languages),
        "low_ops_fit": int(language in ["python", "go"]),
        "enterprise_fit": int(language in ["java"]),
        "performance_fit": int(language in ["go", "rust"]),

        # signals
        "ecosystem": float(signals.get("ecosystem", 0.5)),
        "activity": float(signals.get("activity", 0.5)),
        "popularity": float(signals.get("popularity", 0.5)),
    }


def rank_with_model(context: Dict[str, Any], candidates: List[str]) -> List[Dict[str, Any]]:
    model = load_model()

    rows = []
    for language in candidates:
        row = build_feature_row(language, context)
        row["language"] = language
        rows.append(row)

    df = pd.DataFrame(rows)

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

    scores = model.predict(df[feature_columns])

    ranked = []
    for i, language in enumerate(candidates):
        ranked.append(
            {
                "language": language,
                "score": float(scores[i]),  # important: keep "score" key
            }
        )

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked