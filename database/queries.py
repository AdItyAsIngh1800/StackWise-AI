from __future__ import annotations

from database.connection import get_db_connection


def get_top_languages(limit: int = 5) -> list[tuple]:
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
            return cur.fetchall()
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

            value = row[0]
            if value is None:
                return None

            return float(value)
    finally:
        conn.close()