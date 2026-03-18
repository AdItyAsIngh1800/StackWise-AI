from pathlib import Path
import polars as pl


# Update if snapshot hash changes
RAW_DATA_GLOB = "data/raw/snapshots/a6c75e3df7c7af2004d6a7789a757a8a005ced7f/data/full-*.parquet"

PROCESSED_DIR = Path("data/processed")
MERGED_PARQUET_PATH = PROCESSED_DIR / "full_merged.parquet"
FULL_CSV_PATH = PROCESSED_DIR / "full_merged.csv"
SAMPLE_CSV_PATH = PROCESSED_DIR / "sample_100k.csv"


def convert_dataset() -> None:
    print("🚀 Starting dataset conversion...")

    # Create processed folder
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("📥 Reading parquet shards...")
    lazy_df = pl.scan_parquet(RAW_DATA_GLOB)

    # 🔹 Save full merged parquet (streaming, memory-safe)
    print("💾 Saving full merged parquet...")
    lazy_df.sink_parquet(str(MERGED_PARQUET_PATH))
    print(f"✅ Saved: {MERGED_PARQUET_PATH}")

    # 🔹 Save full CSV (streaming, but can be large!)
    print("💾 Saving full CSV (this may take time)...")
    lazy_df.sink_csv(str(FULL_CSV_PATH))
    print(f"✅ Saved: {FULL_CSV_PATH}")

    # 🔹 Save small sample for Excel
    print("📊 Creating sample CSV (100K rows)...")
    sample_df = lazy_df.limit(100_000).collect()
    sample_df.write_csv(str(SAMPLE_CSV_PATH))
    print(f"✅ Saved: {SAMPLE_CSV_PATH}")

    print("\n🎉 Conversion completed successfully!")


if __name__ == "__main__":
    convert_dataset()