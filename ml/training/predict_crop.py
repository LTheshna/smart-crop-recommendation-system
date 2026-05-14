from __future__ import annotations

from pathlib import Path
import joblib
import pandas as pd

from ml.rules.agronomic_filters import (
    filter_recommendations,
    CROP_RULES
)


MIN_CONFIDENCE_THRESHOLD = 15.0
ARTIFACTS_DIR = Path("ml/artifacts")

MODEL_PATH = ARTIFACTS_DIR / "crop_model.pkl"
LABEL_ENCODER_PATH = ARTIFACTS_DIR / "label_encoder.pkl"
FEATURE_COLUMNS_PATH = ARTIFACTS_DIR / "feature_columns.pkl"


def load_artifacts():
    """Load trained model pipeline and encoders."""
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    feature_columns = joblib.load(FEATURE_COLUMNS_PATH)

    return model, label_encoder, feature_columns


def generate_reason(crop: str, input_data: dict) -> str:
    crop_key = crop.lower()
    rule = CROP_RULES.get(crop_key)

    if not rule:
        return f"{crop.title()} matches the learned agronomic pattern."

    rainfall = input_data.get("rainfall")
    ph = input_data.get("ph")
    temperature = input_data.get("temperature")

    reasons = []

    if rainfall >= rule["min_rainfall"]:
        reasons.append(
            f"rainfall ({rainfall} mm) meets requirement"
        )

    if rule["ph_range"][0] <= ph <= rule["ph_range"][1]:
        reasons.append(
            f"soil pH ({ph}) is suitable"
        )

    if rule["temperature_range"][0] <= temperature <= rule["temperature_range"][1]:
        reasons.append(
            f"temperature ({temperature}°C) is optimal"
        )

    if not reasons:
        return f"{crop.title()} matches learned model patterns."

    return f"{crop.title()} recommended because " + ", ".join(reasons) + "."


def validate_input(input_data: dict, feature_columns: list[str]):
    """Validate required model input fields."""
    missing = [
        col for col in feature_columns
        if col not in input_data
    ]

    if missing:
        raise ValueError(
            f"Missing required input fields: {missing}"
        )


def apply_expert_overrides(input_data: dict, recommendations: list):
    """
    Rule-based expert overrides for known agronomic scenarios
    where ML predictions are unreliable.
    """

    # Dry Pulse Override
    if (
        input_data["rainfall"] <= 300 and
        input_data["temperature"] <= 28 and
        input_data["season"] == "Rabi" and
        input_data["ph"] >= 6.5
    ):
        return [
            {
                "crop": "chickpea",
                "confidence": 85.0,
                "reason": "Expert override: Dry Rabi pulse conditions strongly favor chickpea."
            },
            {
                "crop": "lentil",
                "confidence": 78.0,
                "reason": "Expert override: Dry Rabi pulse conditions support lentil."
            },
            {
                "crop": "mothbeans",
                "confidence": 72.0,
                "reason": "Expert override: Dry Rabi pulse conditions support mothbeans."
            }
        ]

    # Wet Tropical Override
    if (
        input_data["rainfall"] >= 1100 and
        input_data["humidity"] >= 80 and
        input_data["temperature"] >= 26
    ):
        return [
    {
        "crop": "rice",
        "confidence": 95.0,
        "reason": "Expert override: Wet tropical conditions strongly favor rice."
    },
    {
        "crop": "banana",
        "confidence": 82.0,
        "reason": "Expert override: Wet humid tropical climate supports banana."
    },
    {
        "crop": "papaya",
        "confidence": 74.0,
        "reason": "Expert override: Warm wet climate supports papaya."
    }
]

    # Moderate Cereal Override
    if (
        400 <= input_data["rainfall"] <= 900 and
        20 <= input_data["temperature"] <= 30 and
        5.8 <= input_data["ph"] <= 7.2
    ):
        return [
            {
                "crop": "maize",
                "confidence": 84.0,
                "reason": "Expert override: Moderate seasonal agronomic conditions favor maize."
            },
            {
                "crop": "cotton",
                "confidence": 76.0,
                "reason": "Expert override: Moderate warm climate supports cotton."
            },
            {
                "crop": "pigeonpeas",
                "confidence": 70.0,
                "reason": "Expert override: Moderate seasonal conditions support pigeonpeas."
            }
        ]

    return recommendations


def predict_top_crops(input_data: dict, top_n: int = 3):
    model, label_encoder, feature_columns = load_artifacts()

    validate_input(input_data, feature_columns)

    input_df = pd.DataFrame([input_data])

    probabilities = model.predict_proba(input_df)[0]

    top_indices = probabilities.argsort()[::-1][:top_n]

    recommendations = []

    for idx in top_indices:
        crop_name = label_encoder.inverse_transform([idx])[0]
        confidence = round(
            float(probabilities[idx]) * 100,
            2
        )

        recommendations.append({
            "crop": crop_name,
            "confidence": confidence,
            "reason": generate_reason(
                crop_name,
                input_data
            )
        })

    print("BEFORE FILTER:", recommendations)

    recommendations = filter_recommendations(
        recommendations,
        input_data
    )

    recommendations = apply_expert_overrides(
        input_data,
        recommendations
    )

    print("AFTER FILTER:", recommendations)

    if not recommendations:
        return [{
            "crop": "No Suitable Crop Found",
            "confidence": 0,
            "reason": "Input conditions violate agronomic constraints."
        }]

    if recommendations[0]["confidence"] < MIN_CONFIDENCE_THRESHOLD:
        return [{
            "crop": "Low Confidence Recommendation",
            "confidence": recommendations[0]["confidence"],
            "reason": "Model confidence too low for reliable recommendation."
        }]

    return recommendations


if __name__ == "__main__":
    sample_input = {
        "region": "Tamil Nadu",
        "N": 90,
        "P": 42,
        "K": 43,
        "ph": 6.5,
        "moisture": 32,
        "soil_texture": "Loamy",
        "season": "Kharif",
        "temperature": 29,
        "humidity": 82,
        "rainfall": 220,
        "historical_yield": 4200,
        "market_price": 22,
        "estimated_profit": 92400,
        "moisture_category": "Medium",
        "season_encoded": 1
    }

    results = predict_top_crops(sample_input)

    print("\nTop Crop Recommendations:")
    for rec in results:
        print(
            f"{rec['crop']} - {rec['confidence']}%\n"
            f"Reason: {rec['reason']}\n"
        )