import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("data/raw/Crop_recommendation.csv")
OUTPUT_PATH = Path("data/processed/adapted_crop_dataset.csv")


def infer_season(rainfall):
    if rainfall > 200:
        return "Monsoon"
    elif rainfall > 100:
        return "Kharif"
    return "Rabi"


def infer_soil_texture(ph):
    if ph < 5.5:
        return "Clay"
    elif ph < 7.5:
        return "Loamy"
    return "Sandy"


def main():
    df = pd.read_csv(RAW_PATH)

    df = df.rename(columns={"label": "crop"})

    df["region"] = "Tamil Nadu"
    df["season"] = df["rainfall"].apply(infer_season)
    df["soil_texture"] = df["ph"].apply(infer_soil_texture)

    df["historical_yield"] = np.random.uniform(2.0, 6.0, len(df))
    df["market_price"] = np.random.uniform(1500, 7000, len(df))

    df["estimated_profit"] = (
        df["historical_yield"] * df["market_price"] * 10
    )

    df["moisture"] = df["humidity"]

    df["moisture_category"] = pd.cut(
        df["moisture"],
        bins=[0, 30, 60, 100],
        labels=["Low", "Medium", "High"]
    )

    season_map = {
        "Rabi": 0,
        "Kharif": 1,
        "Monsoon": 2
    }

    df["season_encoded"] = df["season"].map(season_map)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Adapted dataset saved to:", OUTPUT_PATH)
    print("Rows:", len(df))


if __name__ == "__main__":
    main()