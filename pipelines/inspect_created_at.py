from pathlib import Path
import polars as pl

INPUT_PATH = Path("data/processed/full_merged.parquet")


def inspect_created_at() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing file: {INPUT_PATH}")

    lf = pl.scan_parquet(str(INPUT_PATH))

    print("\nSample non-null created_at values:")
    print(
        lf.select("created_at")
        .filter(pl.col("created_at").is_not_null())
        .limit(30)
        .collect()
    )

    print("\nTop string lengths:")
    print(
        lf.select(pl.col("created_at").str.len_chars().alias("created_at_len"))
        .filter(pl.col("created_at_len").is_not_null())
        .group_by("created_at_len")
        .len()
        .sort("created_at_len")
        .collect()
    )

    print("\nEnds with Z / timezone / fractional seconds:")
    print(
        lf.select(
            [
                pl.col("created_at").str.ends_with("Z").sum().alias("ends_with_Z"),
                pl.col("created_at")
                .str.contains(r"[+-]\d{2}:?\d{2}$")
                .sum()
                .alias("has_tz_offset"),
                pl.col("created_at")
                .str.contains(r"\.\d+")
                .sum()
                .alias("has_fractional_seconds"),
            ]
        ).collect()
    )


if __name__ == "__main__":
    inspect_created_at()