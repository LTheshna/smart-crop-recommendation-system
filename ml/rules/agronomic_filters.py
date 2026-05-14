

CROP_RULES = {
    "rice": {
        "min_rainfall": 200,
        "ph_range": (5.0, 7.5),
        "temperature_range": (20, 38),
    },
    "maize": {
        "min_rainfall": 120,
        "ph_range": (5.5, 7.5),
        "temperature_range": (18, 35),
    },
    "chickpea": {
        "min_rainfall": 60,
        "ph_range": (6.0, 8.0),
        "temperature_range": (15, 30),
    },
    "kidneybeans": {
        "min_rainfall": 100,
        "ph_range": (6.0, 7.5),
        "temperature_range": (15, 30),
    },
    "pigeonpeas": {
        "min_rainfall": 140,
        "ph_range": (5.5, 7.5),
        "temperature_range": (20, 35),
    },
    "mungbean": {
        "min_rainfall": 100,
        "ph_range": (6.0, 7.5),
        "temperature_range": (20, 35),
    },
    "mothbeans": {
        "min_rainfall": 40,
        "ph_range": (6.0, 8.0),
        "temperature_range": (24, 38),
    },
    "lentil": {
        "min_rainfall": 70,
        "ph_range": (6.0, 8.0),
        "temperature_range": (15, 30),
    },
    "pomegranate": {
        "min_rainfall": 80,
        "ph_range": (5.5, 7.5),
        "temperature_range": (20, 35),
    },
    "banana": {
        "min_rainfall": 220,
        "ph_range": (5.5, 7.5),
        "temperature_range": (20, 35),
    },
    "mango": {
        "min_rainfall": 150,
        "ph_range": (5.5, 7.5),
        "temperature_range": (24, 35),
    },
    "grapes": {
        "min_rainfall": 100,
        "ph_range": (5.5, 7.0),
        "temperature_range": (15, 35),
    },
    "watermelon": {
        "min_rainfall": 80,
        "ph_range": (6.0, 7.5),
        "temperature_range": (22, 35),
    },
    "muskmelon": {
        "min_rainfall": 80,
        "ph_range": (6.0, 7.5),
        "temperature_range": (22, 35),
    },
    "apple": {
        "min_rainfall": 150,
        "ph_range": (5.5, 7.0),
        "temperature_range": (10, 25),
    },
    "orange": {
        "min_rainfall": 120,
        "ph_range": (5.5, 7.5),
        "temperature_range": (15, 35),
    },
    "papaya": {
        "min_rainfall": 180,
        "ph_range": (5.5, 7.0),
        "temperature_range": (22, 35),
    },
    "coconut": {
        "min_rainfall": 250,
        "ph_range": (5.0, 7.0),
        "temperature_range": (24, 35),
    },
    "cotton": {
        "min_rainfall": 100,
        "ph_range": (5.5, 8.0),
        "temperature_range": (20, 40),
    },
    "coffee": {
        "min_rainfall": 220,
        "ph_range": (5.0, 6.5),
        "temperature_range": (18, 28),
    },
    "jute": {
        "min_rainfall": 220,
        "ph_range": (6.0, 7.0),
        "temperature_range": (24, 34),
    },
}


# STEP 3 — Single Crop Validation
def passes_rule(crop: str, features: dict) -> bool:
    rule = CROP_RULES.get(crop.lower())

    if not rule:
        return True

    rainfall = features.get("rainfall", 0)
    ph = features.get("ph", 7)
    temperature = features.get("temperature", 25)

    if rainfall < rule["min_rainfall"]:
        return False

    if not (rule["ph_range"][0] <= ph <= rule["ph_range"][1]):
        return False

    if not (
        rule["temperature_range"][0]
        <= temperature
        <= rule["temperature_range"][1]
    ):
        return False

    return True


# STEP 4 — Filter Recommendation List
def filter_recommendations(predictions: list, features: dict) -> list:
    filtered = []

    for pred in predictions:
        if passes_rule(pred["crop"], features):
            filtered.append(pred)

    return filtered
if __name__ == "__main__":
    preds = [
        {"crop": "rice", "confidence": 0.85},
        {"crop": "wheat", "confidence": 0.78},
    ]

    features = {
        "rainfall": 500,
        "ph": 6.5,
        "temperature": 24
    }

    print(filter_recommendations(preds, features))