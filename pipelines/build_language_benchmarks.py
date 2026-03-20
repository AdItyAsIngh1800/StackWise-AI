import polars as pl

INPUT_PATH = "data/processed/full_merged.parquet"
OUTPUT_PATH = "data/processed/language_benchmarks.parquet"


def build_benchmarks():
    df = pl.scan_parquet(INPUT_PATH)

    result = (
        df
        .select(["language", "forks_count", "watchers_count", "size"])
        .filter(pl.col("language").is_not_null())
        .group_by("language")
        .agg([
            pl.count().alias("repo_count"),
            pl.mean("forks_count").alias("avg_forks"),
            pl.mean("watchers_count").alias("avg_watchers"),
            pl.mean("size").alias("avg_size")
        ])
        .with_columns([
            (
                pl.col("repo_count") * 0.4 +
                pl.col("avg_forks") * 0.3 +
                pl.col("avg_watchers") * 0.3
            ).alias("ecosystem_strength_score")
        ])
        .sort("ecosystem_strength_score", descending=True)
    )

    result.sink_parquet(OUTPUT_PATH)
    result.sink_csv("data/processed/language_benchmarks.csv")

    print("✅ Benchmarks built!")


if __name__ == "__main__":
    build_benchmarks()