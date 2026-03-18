from pathlib import Path
from datetime import datetime, timezone
import polars as pl

INPUT_PATH = Path("data/processed/full_merged.parquet")
OUTPUT_PATH = Path("data/processed/repo_features.parquet")

TODAY = datetime.now(timezone.utc)


def safe_parse_created_at(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.with_columns(
        pl.col("created_at")
        .str.strptime(
            pl.Datetime(time_zone="UTC"),
            format="%Y-%m-%dT%H:%M:%SZ",
            strict=False,
        )
        .alias("created_at_dt")
    )


def build_features() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing file: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lf = pl.scan_parquet(str(INPUT_PATH))
    lf = safe_parse_created_at(lf)

    lf = lf.with_columns(
        [
            pl.col("repo_name").cast(pl.Utf8),
            pl.col("language").cast(pl.Utf8),
            pl.col("license_key").cast(pl.Utf8),
            pl.col("forks_count").cast(pl.Float64).fill_null(0.0),
            pl.col("watchers_count").cast(pl.Float64).fill_null(0.0),
            pl.col("size").cast(pl.Float64).fill_null(0.0),
            pl.when(pl.col("license_key").is_not_null())
            .then(1.0)
            .otherwise(0.0)
            .alias("has_license"),
            pl.when(pl.col("last_pr_id").is_not_null())
            .then(1.0)
            .otherwise(0.0)
            .alias("has_pr_activity"),
            pl.when(pl.col("language").is_not_null())
            .then(1.0)
            .otherwise(0.0)
            .alias("has_language"),
            pl.when(pl.col("created_at_dt").is_not_null())
            .then(1.0)
            .otherwise(0.0)
            .alias("has_created_at"),
        ]
    )

    lf = lf.with_columns(
        [
            (
                pl.lit(TODAY).cast(pl.Datetime(time_zone="UTC"))
                - pl.col("created_at_dt")
            )
            .dt.total_days()
            .fill_null(0)
            .clip(lower_bound=0)
            .alias("repo_age_days")
        ]
    )

    lf = lf.with_columns(
        [
            pl.col("watchers_count").log1p().alias("watchers_log"),
            pl.col("forks_count").log1p().alias("forks_log"),
            pl.col("size").log1p().alias("size_log"),
        ]
    )

    lf = lf.with_columns(
        [
            (
                0.6 * pl.col("watchers_log") + 0.4 * pl.col("forks_log")
            ).alias("popularity_score_raw"),
            (
                0.7 * pl.col("forks_log") + 0.3 * pl.col("watchers_log")
            ).alias("community_score_raw"),
            (
                0.5 * pl.col("has_license") + 0.5 * pl.col("has_pr_activity")
            ).alias("activity_score_raw"),
            (
                0.4 * pl.when(pl.col("repo_age_days") > 365).then(1.0).otherwise(0.3)
                + 0.3 * pl.col("has_license")
                + 0.3 * pl.col("has_pr_activity")
            ).alias("maturity_score_raw"),
            (
                (
                    pl.col("has_language")
                    + pl.col("has_created_at")
                    + pl.when(pl.col("forks_count").is_not_null()).then(1.0).otherwise(0.0)
                    + pl.when(pl.col("watchers_count").is_not_null()).then(1.0).otherwise(0.0)
                    + pl.when(pl.col("last_pr_id").is_not_null()).then(1.0).otherwise(0.0)
                    + pl.when(pl.col("license_key").is_not_null()).then(1.0).otherwise(0.0)
                )
                / 6.0
            ).alias("evidence_completeness"),
        ]
    )

    lf.select(
        [
            "repo_name",
            "language",
            "created_at",
            "license_key",
            "forks_count",
            "watchers_count",
            "size",
            "last_pr_id",
            "repo_age_days",
            "has_license",
            "has_pr_activity",
            "popularity_score_raw",
            "community_score_raw",
            "activity_score_raw",
            "maturity_score_raw",
            "evidence_completeness",
        ]
    ).sink_parquet(str(OUTPUT_PATH))

    print(f"Saved features to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_features()