"""Merge cleaned raw data sources into a final processed dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .clean_data import load_and_clean_csv

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "final_crop_dataset.csv"


def _load_source(filename: str) -> pd.DataFrame:
    """Load and clean a source CSV from the raw data directory."""
    file_path = RAW_DATA_DIR / filename
    print(f"Loading {file_path}")
    return load_and_clean_csv(str(file_path))


def _validate_columns(df: pd.DataFrame, required_columns: list[str], source_name: str) -> None:
    """Raise an error when required columns are missing from a DataFrame."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"{source_name} is missing required columns: {', '.join(missing_columns)}"
        )


def _merge_on_region(primary: pd.DataFrame, secondary: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Merge two DataFrames on the region column with a left join."""
    _validate_columns(primary, ["region"], "Primary dataset")
    _validate_columns(secondary, ["region"], source_name)
    print(f"Merging {source_name} on region")
    return primary.merge(secondary, on="region", how="left")


def _merge_on_crop(primary: pd.DataFrame, secondary: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Merge two DataFrames on the crop column with a left join."""
    _validate_columns(primary, ["crop"], "Primary dataset")
    _validate_columns(secondary, ["crop"], source_name)
    print(f"Merging {source_name} on crop")
    return primary.merge(secondary, on="crop", how="left")


def _report_merge_stats(before_count: int, after_count: int, source_name: str) -> None:
    """Print row counts before and after a merge and warn on significant expansion."""
    print(f"Rows before merging {source_name}: {before_count}")
    print(f"Rows after merging {source_name}: {after_count}")

    if after_count > before_count * 1.2:
        increase_pct = (after_count / before_count - 1) * 100
        print(
            f"WARNING: row count increased by {increase_pct:.1f}% after merging {source_name}."
            " This may indicate intentional expansion into region-crop combinations."
        )


def merge_raw_datasets() -> pd.DataFrame:
    """Load raw sources, merge them, and save the final dataset.

    The yield data merge is intentionally performed on region only. That merge may expand
    rows into region-crop combinations when yield data contains multiple crops per region.
    """
    soil_data = _load_source("soil_data.csv")
    weather_data = _load_source("weather_data.csv")
    yield_data = _load_source("yield_data.csv")
    market_data = _load_source("market_data.csv")

    merged = _merge_on_region(soil_data, weather_data, "weather_data.csv")
    _report_merge_stats(len(soil_data), len(merged), "weather_data.csv")

    before_yield_count = len(merged)
    merged = _merge_on_region(merged, yield_data, "yield_data.csv")
    _report_merge_stats(before_yield_count, len(merged), "yield_data.csv")

    before_market_count = len(merged)
    merged = _merge_on_crop(merged, market_data, "market_data.csv")
    _report_merge_stats(before_market_count, len(merged), "market_data.csv")

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Saving merged dataset to {OUTPUT_FILE}")
    merged.to_csv(OUTPUT_FILE, index=False)

    return merged


if __name__ == "__main__":
    merge_raw_datasets()
