from __future__ import annotations

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

BENCHMARK_PATH = DATA_DIR / "language_benchmarks.csv"
DISTRIBUTION_PATH = DATA_DIR / "language_distribution.csv"


def load_language_benchmarks() -> pd.DataFrame:
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(f"{BENCHMARK_PATH} not found")
    return pd.read_csv(BENCHMARK_PATH)


def load_language_distribution() -> pd.DataFrame:
    if not DISTRIBUTION_PATH.exists():
        raise FileNotFoundError(f"{DISTRIBUTION_PATH} not found")
    return pd.read_csv(DISTRIBUTION_PATH)