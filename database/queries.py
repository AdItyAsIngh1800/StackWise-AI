from __future__ import annotations

from typing import Any

from database.connection import get_db_connection


def get_top_languages(limit: int = 5) -> list[dict[str, Any]]:
    query = """
    SELECT winner_language, COUNT(*) as count
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
                            "winner_language": row.get("winner_language"),
                            "count": row.get("count"),
                        }
                    )
                else:
                    results.append(
                        {
                            "winner_language": row[0],
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

            if isinstance(row, dict):
                value = next(iter(row.values()), None)
            else:
                value = row[0]

            if value is None:
                return None

            return float(value)
    finally:
        conn.close()