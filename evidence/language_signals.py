from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd



BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

LANGUAGE_BENCHMARKS_PATH = PROCESSED_DIR / "language_benchmarks.csv"
LANGUAGE_DISTRIBUTION_PATH = PROCESSED_DIR / "language_distribution.csv"


LANGUAGE_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",
    "node": "javascript",
    "nodejs": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "py": "python",
    "python": "python",
    "golang": "go",
    "go": "go",
    "csharp": "c#",
    "c#": "c#",
    "cpp": "c++",
    "c++": "c++",
    "rb": "ruby",
    "ruby": "ruby",
    "postgres": "postgresql",
    "postgresql": "postgresql",
}


TOP_LANGUAGE_ALLOWLIST = {
    "javascript",
    "typescript",
    "python",
    "java",
    "go",
    "c#",
    "c++",
    "php",
    "ruby",
    "rust",
    "kotlin",
    "swift",
    "scala",
    "r",
    "dart",
    "elixir",
    "clojure",
    "haskell",
    "lua",
    "shell",
    "sql",
    "html",
    "css",
}


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)


def normalize_language_name(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None

    key = text.lower()
    if key in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[key]

    return key


def _min_max_scale(series: pd.Series) -> pd.Series:
    series = series.fillna(0.0).astype(float)
    min_val = series.min()
    max_val = series.max()

    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series([0.0] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val)


def _log1p_scale(series: pd.Series) -> pd.Series:
    series = series.fillna(0.0).astype(float)
    transformed = series.map(lambda x: math.log1p(x))
    return _min_max_scale(transformed)


def _clean_distribution(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["language_norm"] = df["language"].apply(normalize_language_name)
    df = df[df["language_norm"].notna()]

    df = (
        df.groupby("language_norm", as_index=False)
        .agg(
            repo_count=("repo_count", "sum"),
            avg_forks=("avg_forks", "mean"),
            avg_watchers=("avg_watchers", "mean"),
        )
    )

    return df


def _clean_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["language_norm"] = df["language"].apply(normalize_language_name)
    df = df[df["language_norm"].notna()]

    df = (
        df.groupby("language_norm", as_index=False)
        .agg(
            benchmark_repo_count=("repo_count", "sum"),
            benchmark_avg_forks=("avg_forks", "mean"),
            benchmark_avg_watchers=("avg_watchers", "mean"),
            benchmark_avg_size=("avg_size", "mean"),
            ecosystem_strength_score=("ecosystem_strength_score", "mean"),
        )
    )

    return df


@lru_cache(maxsize=1)
def build_language_signals() -> dict[str, dict[str, float]]:
    distribution_df = _safe_read_csv(LANGUAGE_DISTRIBUTION_PATH)
    benchmarks_df = _safe_read_csv(LANGUAGE_BENCHMARKS_PATH)

    distribution_df = _clean_distribution(distribution_df)
    benchmarks_df = _clean_benchmarks(benchmarks_df)

    merged = distribution_df.merge(
        benchmarks_df,
        on="language_norm",
        how="outer",
    )

    merged["repo_count"] = merged["repo_count"].fillna(0.0)
    merged["avg_forks"] = merged["avg_forks"].fillna(0.0)
    merged["avg_watchers"] = merged["avg_watchers"].fillna(0.0)
    merged["benchmark_repo_count"] = merged["benchmark_repo_count"].fillna(0.0)
    merged["benchmark_avg_forks"] = merged["benchmark_avg_forks"].fillna(0.0)
    merged["benchmark_avg_watchers"] = merged["benchmark_avg_watchers"].fillna(0.0)
    merged["benchmark_avg_size"] = merged["benchmark_avg_size"].fillna(0.0)
    merged["ecosystem_strength_score"] = merged["ecosystem_strength_score"].fillna(0.0)

    # keep useful mainstream languages for recommendation priors
    merged = merged[merged["language_norm"].isin(TOP_LANGUAGE_ALLOWLIST)].copy()

    merged["repo_count_norm"] = _log1p_scale(merged["repo_count"])
    merged["forks_norm"] = _log1p_scale(merged["avg_forks"])
    merged["watchers_norm"] = _log1p_scale(merged["avg_watchers"])
    merged["size_norm"] = _log1p_scale(merged["benchmark_avg_size"])
    merged["ecosystem_norm"] = _min_max_scale(merged["ecosystem_strength_score"])

    merged["popularity_score"] = (
        0.55 * merged["repo_count_norm"] +
        0.20 * merged["watchers_norm"] +
        0.25 * merged["forks_norm"]
    )

    merged["maturity_score"] = (
        0.50 * merged["ecosystem_norm"] +
        0.25 * merged["watchers_norm"] +
        0.25 * merged["forks_norm"]
    )

    merged["activity_score"] = (
        0.45 * merged["forks_norm"] +
        0.35 * merged["watchers_norm"] +
        0.20 * merged["repo_count_norm"]
    )

    merged["ecosystem_score"] = (
        0.50 * merged["ecosystem_norm"] +
        0.30 * merged["repo_count_norm"] +
        0.20 * merged["size_norm"]
    )

    merged["evidence_coverage"] = (
        merged[
            [
                "repo_count",
                "avg_forks",
                "avg_watchers",
                "benchmark_avg_size",
                "ecosystem_strength_score",
            ]
        ]
        .notna()
        .sum(axis=1)
        / 5.0
    )

    signals: dict[str, dict[str, float]] = {}

    for _, row in merged.iterrows():
        language = row["language_norm"]
        signals[language] = {
            "popularity": round(float(row["popularity_score"]), 4),
            "maturity": round(float(row["maturity_score"]), 4),
            "activity": round(float(row["activity_score"]), 4),
            "ecosystem": round(float(row["ecosystem_score"]), 4),
            "evidence_coverage": round(float(row["evidence_coverage"]), 4),
        }

    return signals


def get_language_signal(language: str) -> dict[str, float]:
    normalized = normalize_language_name(language)
    signals = build_language_signals()

    default_signal = {
        "popularity": 0.5,
        "maturity": 0.5,
        "activity": 0.5,
        "ecosystem": 0.5,
        "evidence_coverage": 0.0,
    }

    if normalized is None:
        return default_signal

    return signals.get(normalized, default_signal)


if __name__ == "__main__":
    signals = build_language_signals()

    preview_languages = [
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "rust",
    ]

    for language in preview_languages:
        print(language, "->", get_language_signal(language))