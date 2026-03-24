from __future__ import annotations

from typing import Any

from database.connection import get_db_connection


def get_top_languages(limit: int = 5) -> list[dict[str, Any]]:
    query = """
    SELECT winner_language, COUNT(*) AS count
    FROM recommendation_runs
    GROUP BY winner_language
    ORDER BY count DESC
    LIMIT %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

            results: list[dict[str, Any]] = []
            for row in rows:
                if isinstance(row, dict):
                    results.append(
                        {
                            "language": row.get("winner_language"),
                            "count": row.get("count"),
                        }
                    )
                else:
                    results.append(
                        {
                            "language": row[0],
                            "count": row[1],
                        }
                    )
            return results
    finally:
        conn.close()


def get_avg_confidence() -> float | None:
    query = """
    SELECT AVG(confidence)
    FROM recommendation_runs;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()

            if row is None:
                return None

            value = next(iter(row.values()), None) if isinstance(row, dict) else row[0]
            return float(value) if value is not None else None
    finally:
        conn.close()


def get_confidence_trend() -> list[dict[str, Any]]:
    query = """
    SELECT DATE(created_at) AS date, AVG(confidence) AS avg_confidence
    FROM recommendation_runs
    GROUP BY DATE(created_at)
    ORDER BY date;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            results: list[dict[str, Any]] = []
            for row in rows:
                if isinstance(row, dict):
                    avg = row.get("avg_confidence")
                    results.append(
                        {
                            "date": str(row.get("date")),
                            "avg_confidence": float(avg) if avg is not None else None,
                        }
                    )
                else:
                    results.append(
                        {
                            "date": str(row[0]),
                            "avg_confidence": float(row[1]) if row[1] is not None else None,
                        }
                    )
            return results
    finally:
        conn.close()


def get_top_stacks(limit: int = 5) -> list[dict[str, Any]]:
    query = """
    SELECT
        winner_language,
        winner_framework,
        winner_database,
        COUNT(*) AS count
    FROM recommendation_runs
    GROUP BY winner_language, winner_framework, winner_database
    ORDER BY count DESC
    LIMIT %s;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

            results: list[dict[str, Any]] = []
            for row in rows:
                if isinstance(row, dict):
                    results.append(
                        {
                            "language": row.get("winner_language"),
                            "framework": row.get("winner_framework"),
                            "database": row.get("winner_database"),
                            "count": row.get("count"),
                        }
                    )
                else:
                    results.append(
                        {
                            "language": row[0],
                            "framework": row[1],
                            "database": row[2],
                            "count": row[3],
                        }
                    )
            return results
    finally:
        conn.close()


def get_runs_by_project_type() -> list[dict[str, Any]]:
    query = """
    SELECT project_type, COUNT(*) AS count
    FROM recommendation_runs
    GROUP BY project_type
    ORDER BY count DESC;
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            results: list[dict[str, Any]] = []
            for row in rows:
                if isinstance(row, dict):
                    results.append(
                        {
                            "project_type": row.get("project_type"),
                            "count": row.get("count"),
                        }
                    )
                else:
                    results.append(
                        {
                            "project_type": row[0],
                            "count": row[1],
                        }
                    )
            return results
    finally:
        conn.close()