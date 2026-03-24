from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from database.connection import get_db_connection
from evidence.language_signals import get_language_signal

CANDIDATES = ["python", "javascript", "typescript", "java", "go", "rust"]


def _project_type_feature(project_type: str) -> int:
    return 1 if project_type == "api" else 0


def _scale_feature(expected_scale: str) -> int:
    return 1 if expected_scale == "high" else 0


def load_feedback_rows() -> list[dict]:
    query = """
    SELECT
        id,
        project_type,
        expected_scale,
        low_ops,
        prefer_enterprise,
        prototype_only,
        rapid_schema_changes,
        needs_cache,
        prefer_portability,
        team_languages,
        recommended_language,
        selected_language,
        accepted
    FROM recommendation_feedback
    ORDER BY id;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            normalized: list[dict] = []
            for row in rows:
                if isinstance(row, dict):
                    normalized.append(row)
                else:
                    normalized.append(
                        {
                            "id": row[0],
                            "project_type": row[1],
                            "expected_scale": row[2],
                            "low_ops": row[3],
                            "prefer_enterprise": row[4],
                            "prototype_only": row[5],
                            "rapid_schema_changes": row[6],
                            "needs_cache": row[7],
                            "prefer_portability": row[8],
                            "team_languages": row[9],
                            "recommended_language": row[10],
                            "selected_language": row[11],
                            "accepted": row[12],
                        }
                    )
            return normalized
    finally:
        conn.close()


def build_training_dataframe() -> pd.DataFrame:
    feedback_rows = load_feedback_rows()
    output_rows: list[dict] = []

    for feedback in feedback_rows:
        query_id = feedback["id"]
        selected_language = feedback["selected_language"]
        recommended_language = feedback["recommended_language"]

        team_languages_raw = feedback["team_languages"]
        if isinstance(team_languages_raw, str):
            try:
                team_languages = json.loads(team_languages_raw)
            except json.JSONDecodeError:
                team_languages = []
        else:
            team_languages = team_languages_raw or []

        for language in CANDIDATES:
            signals = get_language_signal(language)

            # ✅ Better label (graded relevance)
            if language == selected_language:
                label = 3
            elif language == recommended_language:
                label = 2
            elif language in team_languages:
                label = 1
            else:
                label = 0

            output_rows.append(
                {
                    "query_id": query_id,
                    "language": language,

                    "project_type_api": _project_type_feature(feedback["project_type"]),
                    "expected_scale_high": _scale_feature(feedback["expected_scale"]),

                    "low_ops": int(bool(feedback["low_ops"])),
                    "prefer_enterprise": int(bool(feedback["prefer_enterprise"])),
                    "prototype_only": int(bool(feedback["prototype_only"])),
                    "rapid_schema_changes": int(bool(feedback["rapid_schema_changes"])),
                    "needs_cache": int(bool(feedback["needs_cache"])),
                    "prefer_portability": int(bool(feedback["prefer_portability"])),

                    "team_has_language": int(language in team_languages),

                    # 🔥 New engineered features
                    "matches_team_pref": int(language in team_languages),
                    "low_ops_fit": int(language in ["python", "go"]),
                    "enterprise_fit": int(language in ["java"]),
                    "performance_fit": int(language in ["go", "rust"]),

                    "ecosystem": float(signals["ecosystem"]),
                    "activity": float(signals["activity"]),
                    "popularity": float(signals["popularity"]),

                    "label": label,
                }
            )

    return pd.DataFrame(output_rows)


if __name__ == "__main__":
    df = build_training_dataframe()
    output_path = Path("data/processed/training_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved training data to {output_path} with {len(df)} rows.")