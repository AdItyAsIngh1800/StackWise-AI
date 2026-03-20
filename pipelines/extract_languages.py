import polars as pl

INPUT_PATH = "data/processed/full_merged.parquet"
OUTPUT_PATH = "data/processed/language_distribution.parquet"


def extract_languages():
    print("📊 Extracting language distribution...")

    df = pl.scan_parquet(INPUT_PATH)

    result = (
        df
        .select(["language", "forks_count", "watchers_count"])
        .filter(pl.col("language").is_not_null())
        .group_by("language")
        .agg([
            pl.count().alias("repo_count"),
            pl.mean("forks_count").alias("avg_forks"),
            pl.mean("watchers_count").alias("avg_watchers")
        ])
        .sort("repo_count", descending=True)
    )

    result.sink_csv("data/processed/language_distribution.csv")

    print(f"✅ Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_languages()
