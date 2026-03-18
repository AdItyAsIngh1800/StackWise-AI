from pathlib import Path
import polars as pl

BENCHMARK_PATH = Path("data/processed/language_benchmarks.parquet")


def load_language_benchmarks() -> dict:
    if not BENCHMARK_PATH.exists():
        return {}

    df = pl.read_parquet(str(BENCHMARK_PATH))
    rows = df.to_dicts()

    return {row["language"]: row for row in rows if row.get("language") is not None}


def get_option_evidence_adjustments() -> dict:
    benchmarks = load_language_benchmarks()

    python_strength = benchmarks.get("Python", {}).get("ecosystem_strength_score", 0.5)
    javascript_strength = benchmarks.get("JavaScript", {}).get("ecosystem_strength_score", 0.5)
    go_strength = benchmarks.get("Go", {}).get("ecosystem_strength_score", 0.5)
    java_strength = benchmarks.get("Java", {}).get("ecosystem_strength_score", 0.5)

    return {
        "EKS": round(0.05 * float(go_strength), 3),
        "Lambda": round(0.03 * float((python_strength + javascript_strength) / 2), 3),
        "ECS": round(0.03 * float((python_strength + java_strength) / 2), 3),
    }