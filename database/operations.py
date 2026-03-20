from __future__ import annotations

import json
from typing import Any

from database.connection import get_db_connection


def log_recommendation(
    request_data: dict[str, Any],
    result_data: dict[str, Any],
    scenario_name: str | None = None,
) -> None:
    winner = result_data.get("winner") or {}

    query = """
    INSERT INTO recommendation_logs (
        scenario_name,
        project_type,
        team_languages,
        low_ops,
        expected_scale,
        prefer_enterprise,
        prototype_only,
        rapid_schema_changes,
        needs_cache,
        prefer_portability,
        winner_language,
        winner_framework,
        winner_database,
        winner_deployment,
        winner_score,
        recommendation_payload,
        explanation
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s
    );
    """

    values = (
        scenario_name,
        request_data.get("project_type"),
        json.dumps(request_data.get("team_languages", [])),
        request_data.get("low_ops", False),
        request_data.get("expected_scale", "medium"),
        request_data.get("prefer_enterprise", False),
        request_data.get("prototype_only", False),
        request_data.get("rapid_schema_changes", False),
        request_data.get("needs_cache", False),
        request_data.get("prefer_portability", False),
        winner.get("language"),
        winner.get("backend_framework"),
        winner.get("database"),
        winner.get("deployment"),
        winner.get("score"),
        json.dumps(result_data),
        result_data.get("explanation"),
    )

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
    finally:
        conn.close()

def get_scenarios():
    query = """
    SELECT id, scenario_name, project_type, created_at
    FROM recommendation_logs
    ORDER BY created_at DESC
    LIMIT 20;
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
                    "project_type": r[2],
                    "created_at": str(r[3]),
                }
                for r in rows
            ]
    finally:
        conn.close()

def get_scenario_by_id(scenario_id: int):
    query = """
    SELECT recommendation_payload
    FROM recommendation_logs
    WHERE id = %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (scenario_id,))
            row = cur.fetchone()

            if not row:
                return None

            return row[0]
    finally:
        conn.close()