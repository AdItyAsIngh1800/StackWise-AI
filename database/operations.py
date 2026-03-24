from __future__ import annotations

import json
from typing import Any

from database.connection import get_db_connection


# ---------------------------
# Scenario Operations
# ---------------------------
def create_scenario(scenario_name: str) -> int:
    query = """
    INSERT INTO scenarios (scenario_name)
    VALUES (%s)
    RETURNING id;
    """

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, (scenario_name,))
                row = cur.fetchone()

                if row is None:
                    raise RuntimeError("Failed to create scenario: no ID returned from database.")

                if isinstance(row, dict):
                    scenario_id = row.get("id")
                    if scenario_id is None:
                        raise RuntimeError("Failed to create scenario: ID missing in returned row.")
                    return int(scenario_id)

                return int(row[0])
    finally:
        conn.close()


def list_scenarios() -> list[dict[str, Any]]:
    query = """
    SELECT id, scenario_name, created_at
    FROM scenarios
    ORDER BY created_at DESC;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            scenarios: list[dict[str, Any]] = []

            for row in rows:
                if isinstance(row, dict):
                    scenarios.append(
                        {
                            "id": row.get("id"),
                            "scenario_name": row.get("scenario_name"),
                            "created_at": str(row.get("created_at")),
                        }
                    )
                else:
                    scenarios.append(
                        {
                            "id": row[0],
                            "scenario_name": row[1],
                            "created_at": str(row[2]),
                        }
                    )

            return scenarios
    finally:
        conn.close()


# ---------------------------
# Recommendation Logging
# ---------------------------
def create_recommendation_run(
    request_data: dict[str, Any],
    result_data: dict[str, Any],
    scenario_id: int | None = None,
) -> None:
    winner = result_data.get("winner") or {}

    query = """
    INSERT INTO recommendation_runs (
        scenario_id,
        project_type,
        team_languages,
        input_payload,
        winner_language,
        winner_framework,
        winner_database,
        winner_deployment,
        winner_score,
        confidence,
        explanation,
        response_payload,
        sensitivity_payload,
        pareto_payload,
        why_not_payload
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = (
        scenario_id,
        request_data.get("project_type"),
        json.dumps(request_data.get("team_languages", [])),
        json.dumps(request_data),
        winner.get("language"),
        winner.get("backend_framework"),
        winner.get("database"),
        winner.get("deployment"),
        winner.get("score"),
        result_data.get("confidence"),
        result_data.get("explanation"),
        json.dumps(result_data),
        json.dumps(result_data.get("sensitivity")),
        json.dumps(result_data.get("pareto")),
        json.dumps(result_data.get("why_not")),
    )

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
    finally:
        conn.close()


# ---------------------------
# Fetch Recommendation Runs
# ---------------------------
def list_recommendation_runs(limit: int = 20) -> list[dict[str, Any]]:
    query = """
    SELECT id, project_type, winner_language, winner_score, created_at
    FROM recommendation_runs
    ORDER BY created_at DESC
    LIMIT %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

            runs: list[dict[str, Any]] = []

            for row in rows:
                if isinstance(row, dict):
                    runs.append(
                        {
                            "id": row.get("id"),
                            "project_type": row.get("project_type"),
                            "winner_language": row.get("winner_language"),
                            "score": row.get("winner_score"),
                            "created_at": str(row.get("created_at")),
                        }
                    )
                else:
                    runs.append(
                        {
                            "id": row[0],
                            "project_type": row[1],
                            "winner_language": row[2],
                            "score": row[3],
                            "created_at": str(row[4]),
                        }
                    )

            return runs
    finally:
        conn.close()


def get_recommendation_run(run_id: int) -> dict[str, Any] | None:
    query = """
    SELECT response_payload
    FROM recommendation_runs
    WHERE id = %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (run_id,))
            row = cur.fetchone()

            if row is None:
                return None

            if isinstance(row, dict):
                value = row.get("response_payload")
            else:
                value = row[0]

            if value is None:
                return None

            return value
    finally:
        conn.close()

def get_scenario_by_id(scenario_id: int) -> dict[str, Any] | None:
    query = """
    SELECT id, scenario_name, created_at
    FROM scenarios
    WHERE id = %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (scenario_id,))
            row = cur.fetchone()

            if row is None:
                return None

            if isinstance(row, dict):
                return {
                    "id": row.get("id"),
                    "scenario_name": row.get("scenario_name"),
                    "created_at": str(row.get("created_at")),
                }

            return {
                "id": row[0],
                "scenario_name": row[1],
                "created_at": str(row[2]),
            }
    finally:
        conn.close()


def get_runs_for_scenario(scenario_id: int) -> list[dict[str, Any]]:
    query = """
    SELECT id, project_type, winner_language, winner_framework,
           winner_database, winner_deployment, winner_score,
           confidence, created_at
    FROM recommendation_runs
    WHERE scenario_id = %s
    ORDER BY created_at DESC;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (scenario_id,))
            rows = cur.fetchall()

            results: list[dict[str, Any]] = []

            for row in rows:
                if isinstance(row, dict):
                    results.append(
                        {
                            "id": row.get("id"),
                            "project_type": row.get("project_type"),
                            "winner_language": row.get("winner_language"),
                            "winner_framework": row.get("winner_framework"),
                            "winner_database": row.get("winner_database"),
                            "winner_deployment": row.get("winner_deployment"),
                            "winner_score": row.get("winner_score"),
                            "confidence": row.get("confidence"),
                            "created_at": str(row.get("created_at")),
                        }
                    )
                else:
                    results.append(
                        {
                            "id": row[0],
                            "project_type": row[1],
                            "winner_language": row[2],
                            "winner_framework": row[3],
                            "winner_database": row[4],
                            "winner_deployment": row[5],
                            "winner_score": row[6],
                            "confidence": row[7],
                            "created_at": str(row[8]),
                        }
                    )

            return results
    finally:
        conn.close()

def create_feedback(payload: dict[str, Any]) -> dict[str, Any]:
    query = """
    INSERT INTO recommendation_feedback (
        run_id,
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
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, accepted, created_at;
    """

    accepted = payload["recommended_language"] == payload["selected_language"]

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    payload.get("run_id"),
                    payload["project_type"],
                    payload["expected_scale"],
                    payload["low_ops"],
                    payload["prefer_enterprise"],
                    payload["prototype_only"],
                    payload["rapid_schema_changes"],
                    payload["needs_cache"],
                    payload["prefer_portability"],
                    json.dumps(payload["team_languages"]),
                    payload["recommended_language"],
                    payload["selected_language"],
                    accepted,
                ),
            )

            row = cur.fetchone()
            conn.commit()

            # 🔥 IMPORTANT FIX
            if row is None:
                return {
                    "id": None,
                    "accepted": accepted,
                    "created_at": None,
                }

            # handle dict cursor
            if isinstance(row, dict):
                return {
                    "id": row.get("id"),
                    "accepted": row.get("accepted"),
                    "created_at": str(row.get("created_at")),
                }

            # handle tuple cursor
            return {
                "id": row[0],
                "accepted": row[1],
                "created_at": str(row[2]),
            }

    finally:
        conn.close()