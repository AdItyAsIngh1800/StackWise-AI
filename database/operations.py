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
                return int(row[0])
    finally:
        conn.close()


def list_scenarios() -> list[dict]:
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

            return [
                {
                    "id": r[0],
                    "scenario_name": r[1],
                    "created_at": str(r[2]),
                }
                for r in rows
            ]
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
def list_recommendation_runs(limit: int = 20) -> list[dict]:
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

            return [
                {
                    "id": r[0],
                    "project_type": r[1],
                    "winner_language": r[2],
                    "score": r[3],
                    "created_at": str(r[4]),
                }
                for r in rows
            ]
    finally:
        conn.close()


def get_recommendation_run(run_id: int) -> dict | None:
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

            return row[0]
    finally:
        conn.close()