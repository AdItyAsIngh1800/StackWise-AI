from pathlib import Path
import polars as pl

MERGED_PARQUET_PATH = Path("data/processed/full_merged.parquet")
PROFILE_DIR = Path("data/processed/profile")
FEATURE_SAMPLE_PATH = Path("data/processed/repo_features_sample.parquet")


USEFUL_COLUMNS = [
    "repo_name",
    "language",
    "created_at",
    "license_key",
    "forks_count",
    "watchers_count",
    "size",
    "last_pr_id",
]


def inspect_dataset() -> None:
    print("Starting dataset inspection...")
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    if not MERGED_PARQUET_PATH.exists():
        raise FileNotFoundError(f"Missing file: {MERGED_PARQUET_PATH}")

    lazy_df = pl.scan_parquet(str(MERGED_PARQUET_PATH))

    print("\nCollecting schema...")
    schema = lazy_df.collect_schema()
    for name, dtype in schema.items():
        print(f"{name}: {dtype}")

    print("\nBuilding selected working dataset...")
    available_cols = [col for col in USEFUL_COLUMNS if col in schema]

    selected = lazy_df.select(available_cols)

    print("\nSaving feature sample...")
    selected.limit(200_000).sink_parquet(str(FEATURE_SAMPLE_PATH))
    print(f"Saved: {FEATURE_SAMPLE_PATH}")

    print("\nNull counts...")
    null_counts = selected.null_count().collect()
    print(null_counts)
    null_counts.write_csv(PROFILE_DIR / "null_counts.csv")

    if "language" in available_cols:
        print("\nTop languages...")
        lang_counts = (
            selected
            .group_by("language")
            .len()
            .sort("len", descending=True)
            .limit(20)
            .collect()
        )
        print(lang_counts)
        lang_counts.write_csv(PROFILE_DIR / "top_languages.csv")

    numeric_cols = [c for c in ["forks_count", "watchers_count", "size"] if c in available_cols]
    if numeric_cols:
        print("\nNumeric summary...")
        summary = selected.select(numeric_cols).collect().describe()
        print(summary)
        summary.write_csv(PROFILE_DIR / "numeric_summary.csv")

    print("\nInspection completed successfully.")


if __name__ == "__main__":
    inspect_dataset()