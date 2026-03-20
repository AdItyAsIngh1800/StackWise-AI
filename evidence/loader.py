from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

LANGUAGE_BENCHMARKS_PATH = PROCESSED_DIR / "language_benchmarks.csv"
LANGUAGE_DISTRIBUTION_PATH = PROCESSED_DIR / "language_distribution.csv"


def load_language_benchmarks() -> pd.DataFrame:
    if not LANGUAGE_BENCHMARKS_PATH.exists():
        raise FileNotFoundError(f"Missing file: {LANGUAGE_BENCHMARKS_PATH}")

    return pd.read_csv(LANGUAGE_BENCHMARKS_PATH)


def load_language_distribution() -> pd.DataFrame:
    if not LANGUAGE_DISTRIBUTION_PATH.exists():
        raise FileNotFoundError(f"Missing file: {LANGUAGE_DISTRIBUTION_PATH}")

    return pd.read_csv(LANGUAGE_DISTRIBUTION_PATH)