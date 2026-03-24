from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from database.connection import get_db_connection
from evidence.language_signals import get_language_signal

CANDIDATES = ["python", "javascript", "typescript", "java", "go", "rust"]
PROJECT_TYPES = ["api", "web"]
SCALES = ["low", "medium", "high"]


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


def _parse_team_languages(raw: object) -> list[str]:
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(x).strip().lower() for x in parsed]
            return []
        except json.JSONDecodeError:
            return []

    if isinstance(raw, list):
        return [str(x).strip().lower() for x in raw]

    return []


def build_training_dataframe() -> pd.DataFrame:
    feedback_rows = load_feedback_rows()
    output_rows: list[dict] = []

    for feedback in feedback_rows:
        query_id = feedback["id"]
        project_type = str(feedback["project_type"]).strip().lower()
        expected_scale = str(feedback["expected_scale"]).strip().lower()
        recommended_language = str(feedback["recommended_language"]).strip().lower()
        selected_language = str(feedback["selected_language"]).strip().lower()
        team_languages = _parse_team_languages(feedback["team_languages"])

        for language in CANDIDATES:
            signals = get_language_signal(language)

            row = {
                "query_id": query_id,

                # project type one-hot
                "project_type_api": int(project_type == "api"),
                "project_type_web": int(project_type == "web"),

                # expected scale one-hot
                "expected_scale_low": int(expected_scale == "low"),
                "expected_scale_medium": int(expected_scale == "medium"),
                "expected_scale_high": int(expected_scale == "high"),

                # project constraints
                "low_ops": int(bool(feedback["low_ops"])),
                "prefer_enterprise": int(bool(feedback["prefer_enterprise"])),
                "prototype_only": int(bool(feedback["prototype_only"])),
                "rapid_schema_changes": int(bool(feedback["rapid_schema_changes"])),
                "needs_cache": int(bool(feedback["needs_cache"])),
                "prefer_portability": int(bool(feedback["prefer_portability"])),

                # candidate language identity
                "candidate_python": int(language == "python"),
                "candidate_javascript": int(language == "javascript"),
                "candidate_typescript": int(language == "typescript"),
                "candidate_java": int(language == "java"),
                "candidate_go": int(language == "go"),
                "candidate_rust": int(language == "rust"),

                # team language context
                "team_knows_python": int("python" in team_languages),
                "team_knows_javascript": int("javascript" in team_languages),
                "team_knows_typescript": int("typescript" in team_languages),
                "team_knows_java": int("java" in team_languages),
                "team_knows_go": int("go" in team_languages),
                "team_knows_rust": int("rust" in team_languages),

                # direct team-candidate compatibility
                "team_has_candidate_language": int(language in team_languages),

                # static evidence for candidate language
                "ecosystem": float(signals.get("ecosystem", 0.0)),
                "activity": float(signals.get("activity", 0.0)),
                "popularity": float(signals.get("popularity", 0.0)),

                # whether the rules engine recommended this language
                "is_recommended_language": int(language == recommended_language),

                # target
                "label": int(language == selected_language),
            }

            output_rows.append(row)

    return pd.DataFrame(output_rows)


if __name__ == "__main__":
    df = build_training_dataframe()
    output_path = Path("data/processed/training_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved training data to {output_path} with {len(df)} rows.")