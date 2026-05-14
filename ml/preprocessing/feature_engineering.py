"""Feature engineering utilities for smart crop recommendation preprocessing."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROCESSED_DATA_DIR = Path("data/processed")
INPUT_FILE = PROCESSED_DATA_DIR / "final_crop_dataset.csv"


def _load_dataset(file_path: Path) -> pd.DataFrame:
    """Load the processed dataset from disk."""
    print(f"Loading dataset from {file_path}")
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Processed dataset not found at '{file_path}'. Run the preprocessing pipeline first."
        ) from exc


def _add_estimated_profit(df: pd.DataFrame) -> pd.DataFrame:
    """Add an estimated_profit column from historical_yield and market_price."""
    if "historical_yield" not in df.columns or "market_price" not in df.columns:
        raise ValueError(
            "Required columns for estimated profit are missing: historical_yield and/or market_price"
        )

    print("Adding estimated_profit column")
    df = df.copy()
    df["estimated_profit"] = df["historical_yield"] * df["market_price"]
    return df


def _bucket_moisture(df: pd.DataFrame) -> pd.DataFrame:
    """Bucket moisture values into Low, Medium, and High categories."""
    if "moisture" not in df.columns:
        print("Skipping moisture bucketing: no moisture column found")
        return df

    print("Bucketing moisture into Low/Medium/High")
    bins = [float("-inf"), 30.0, 60.0, float("inf")]
    labels = ["Low", "Medium", "High"]
    df = df.copy()
    df["moisture_category"] = pd.cut(df["moisture"], bins=bins, labels=labels)
    return df


def _encode_season(df: pd.DataFrame) -> pd.DataFrame:
    """Encode season labels numerically when a season column exists.

    This encoding is agriculture-domain specific and maps common crop seasons
    to numeric values.
    """
    if "season" not in df.columns:
        print("Skipping season encoding: no season column found")
        return df

    print("Encoding season column numerically")
    df = df.copy()
    season_mapping = {
        "Kharif": 1,
        "Rabi": 2,
        "Zaid": 3,
    }
    season_series = df["season"].astype(str)
    df["season_encoded"] = season_series.map(season_mapping)
    df["season_encoded"] = df["season_encoded"].fillna(0).astype(int)
    return df


def engineer_features() -> pd.DataFrame:
    """Load the processed dataset, engineer features, and save the updated dataset."""
    df = _load_dataset(INPUT_FILE)
    df = _add_estimated_profit(df)
    df = _bucket_moisture(df)
    df = _encode_season(df)

    print(f"Saving updated dataset back to {INPUT_FILE}")
    df.to_csv(INPUT_FILE, index=False)
    return df


if __name__ == "__main__":
    engineer_features()
