import pandas as pd
import random

regions = [
    "Tamil Nadu", "Karnataka", "Andhra Pradesh",
    "Kerala", "Maharashtra"
]

crops = {
    "Rice": {"price": 22, "yield": 4200},
    "Maize": {"price": 19, "yield": 2800},
    "Groundnut": {"price": 45, "yield": 1800},
    "Wheat": {"price": 24, "yield": 3500},
    "Cotton": {"price": 55, "yield": 1600},
}

rows = []

for _ in range(1000):
    crop = random.choice(list(crops.keys()))

    rows.append({
        "region": random.choice(regions),
        "N": random.randint(40, 120),
        "P": random.randint(20, 80),
        "K": random.randint(20, 80),
        "ph": round(random.uniform(5.5, 8.0), 2),
        "moisture": random.randint(15, 70),
        "soil_texture": random.choice(["Loamy", "Clay", "Sandy"]),
        "season": random.choice(["Kharif", "Rabi", "Zaid"]),
        "temperature": random.randint(18, 38),
        "humidity": random.randint(40, 90),
        "rainfall": random.randint(50, 400),
        "crop": crop,
        "historical_yield": crops[crop]["yield"],
        "market_price": crops[crop]["price"]
    })

df = pd.DataFrame(rows)

df.to_csv("data/raw/enhanced_crop_dataset.csv", index=False)

print("Generated enhanced dataset successfully.")