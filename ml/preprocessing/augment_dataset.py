import pandas as pd
import numpy as np
from pathlib import Path

INPUT_PATH = Path("data/processed/adapted_crop_dataset.csv")
OUTPUT_PATH = Path("data/processed/augmented_crop_dataset.csv")


NUM_AUGMENTS_PER_ROW = 5


NUMERIC_NOISE = {
    "N": 5,
    "P": 5,
    "K": 5,
    "temperature": 2,
    "humidity": 3,
    "ph": 0.3,
    "rainfall": 20,
    "historical_yield": 0.5,
    "market_price": 200,
    "estimated_profit": 5000,
    "moisture": 5
}


def augment_row(row):
    augmented_rows = []

    for _ in range(NUM_AUGMENTS_PER_ROW):
        new_row = row.copy()

        for col, noise in NUMERIC_NOISE.items():
            if col in new_row:
                new_row[col] = max(
                    0,
                    new_row[col] + np.random.normal(0, noise)
                )

        augmented_rows.append(new_row)

    return augmented_rows


def main():
    df = pd.read_csv(INPUT_PATH)

    augmented_data = []

    for _, row in df.iterrows():
        augmented_data.append(row)
        augmented_data.extend(augment_row(row))

    augmented_df = pd.DataFrame(augmented_data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    augmented_df.to_csv(OUTPUT_PATH, index=False)

    print("Original rows:", len(df))
    print("Augmented rows:", len(augmented_df))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()