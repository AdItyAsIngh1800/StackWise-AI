from __future__ import annotations

import pandas as pd

from evidence.loader import (
    load_language_benchmarks,
    load_language_distribution,
)
from evidence.mappings import normalize_language


def _normalize_series(series: pd.Series) -> pd.Series:
    series = series.fillna(0.0).astype(float)

    if series.max() == series.min():
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - series.min()) / (series.max() - series.min())


def build_language_signals() -> pd.DataFrame:
    dist = load_language_distribution().copy()
    bench = load_language_benchmarks().copy()

    # Normalize language names
    dist["language"] = dist["language"].apply(normalize_language)
    bench["language"] = bench["language"].apply(normalize_language)

    dist = dist.dropna(subset=["language"])
    bench = bench.dropna(subset=["language"])

    # Aggregate distribution file
    dist_agg = (
        dist.groupby("language", as_index=False)
        .agg(
            {
                "repo_count": "sum",
                "avg_forks": "mean",
                "avg_watchers": "mean",
            }
        )
        .rename(
            columns={
                "repo_count": "dist_repo_count",
                "avg_forks": "dist_avg_forks",
                "avg_watchers": "dist_avg_watchers",
            }
        )
    )

    # Aggregate benchmark file
    bench_agg = (
        bench.groupby("language", as_index=False)
        .agg(
            {
                "repo_count": "sum",
                "avg_forks": "mean",
                "avg_watchers": "mean",
                "avg_size": "mean",
                "ecosystem_strength_score": "mean",
            }
        )
        .rename(
            columns={
                "repo_count": "bench_repo_count",
                "avg_forks": "bench_avg_forks",
                "avg_watchers": "bench_avg_watchers",
                "avg_size": "bench_avg_size",
                "ecosystem_strength_score": "ecosystem_strength_raw",
            }
        )
    )

    # Merge both evidence sources
    df = pd.merge(dist_agg, bench_agg, on="language", how="outer").fillna(0)

    # Normalized evidence signals
    df["repo_count_norm"] = _normalize_series(
        df["dist_repo_count"] + df["bench_repo_count"]
    )
    df["forks_norm"] = _normalize_series(
        (df["dist_avg_forks"] + df["bench_avg_forks"]) / 2
    )
    df["watchers_norm"] = _normalize_series(
        (df["dist_avg_watchers"] + df["bench_avg_watchers"]) / 2
    )
    df["size_norm"] = _normalize_series(df["bench_avg_size"])
    df["ecosystem_strength_norm"] = _normalize_series(df["ecosystem_strength_raw"])

    # Final derived signals
    df["popularity"] = (
        0.5 * df["repo_count_norm"]
        + 0.25 * df["watchers_norm"]
        + 0.25 * df["forks_norm"]
    )

    df["maturity"] = (
        0.5 * df["ecosystem_strength_norm"]
        + 0.25 * df["watchers_norm"]
        + 0.25 * df["repo_count_norm"]
    )

    df["activity"] = (
        0.5 * df["forks_norm"]
        + 0.3 * df["watchers_norm"]
        + 0.2 * df["repo_count_norm"]
    )

    df["ecosystem"] = (
        0.4 * df["ecosystem_strength_norm"]
        + 0.3 * df["repo_count_norm"]
        + 0.2 * df["watchers_norm"]
        + 0.1 * df["size_norm"]
    )

    return df[
        [
            "language",
            "popularity",
            "maturity",
            "activity",
            "ecosystem",
        ]
    ]


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

    item = row.iloc[0]
    return {
        "popularity": float(item["popularity"]),
        "maturity": float(item["maturity"]),
        "activity": float(item["activity"]),
        "ecosystem": float(item["ecosystem"]),
    }


if __name__ == "__main__":
    print(get_language_signals().head())