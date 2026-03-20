from __future__ import annotations

import pandas as pd

from evidence.loader import (
    load_language_benchmarks,
    load_language_distribution,
)
from evidence.mappings import normalize_language


def _normalize_series(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - series.min()) / (series.max() - series.min())


def build_language_signals() -> pd.DataFrame:
    dist = load_language_distribution()
    bench = load_language_benchmarks()

    # Normalize language names
    dist["language"] = dist["language"].apply(normalize_language)
    bench["language"] = bench["language"].apply(normalize_language)

    dist = dist.dropna(subset=["language"])
    bench = bench.dropna(subset=["language"])

    # Aggregate distribution (popularity)
    dist_agg = (
        dist.groupby("language")
        .agg({"count": "sum"})
        .rename(columns={"count": "popularity_raw"})
        .reset_index()
    )

    # Aggregate benchmarks
    bench_agg = (
        bench.groupby("language")
        .agg({
            "stars": "mean",
            "forks": "mean",
            "issues": "mean",
        })
        .rename(columns={
            "stars": "maturity_raw",
            "forks": "activity_raw",
            "issues": "issues_raw",
        })
        .reset_index()
    )

    # Merge
    df = pd.merge(dist_agg, bench_agg, on="language", how="outer").fillna(0)

    # Normalize signals
    df["popularity"] = _normalize_series(df["popularity_raw"])
    df["maturity"] = _normalize_series(df["maturity_raw"])
    df["activity"] = _normalize_series(df["activity_raw"])

    # Composite ecosystem score
    df["ecosystem"] = (
        0.4 * df["popularity"]
        + 0.3 * df["maturity"]
        + 0.3 * df["activity"]
    )

    return df


# Cache signals in memory (simple optimization)
_LANGUAGE_SIGNALS_CACHE: pd.DataFrame | None = None


def get_language_signals() -> pd.DataFrame:
    global _LANGUAGE_SIGNALS_CACHE

    if _LANGUAGE_SIGNALS_CACHE is None:
        _LANGUAGE_SIGNALS_CACHE = build_language_signals()

    return _LANGUAGE_SIGNALS_CACHE


def get_language_signal(language: str) -> dict:
    df = get_language_signals()

    row = df[df["language"] == language]

    if row.empty:
        return {
            "popularity": 0.5,
            "maturity": 0.5,
            "activity": 0.5,
            "ecosystem": 0.5,
        }

    row = row.iloc[0]

    return {
        "popularity": float(row["popularity"]),
        "maturity": float(row["maturity"]),
        "activity": float(row["activity"]),
        "ecosystem": float(row["ecosystem"]),
    }