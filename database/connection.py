from __future__ import annotations

import os
from typing import Any

import psycopg2
from psycopg2.extensions import connection


def get_db_connection() -> connection:
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "stackwise_ai"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "naina2628"),
    )