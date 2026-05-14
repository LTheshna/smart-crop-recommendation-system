def derive_dynamic_soil_values(
    soil_type,
    rainfall,
    humidity,
    season,
    temperature,
    climate_zone=None
):
    if climate_zone:
     climate_map = {
        "Wet Tropical": "wet",
        "Humid Subtropical": "moderate",
        "Moderate Seasonal": "moderate",
        "Semi-Arid": "dry",
        "Dry Arid": "dry",
    }

     climate_band = climate_map.get(
        climate_zone,
        "moderate"
    )
    else:
     if rainfall >= 900 and humidity >= 75:
        climate_band = "wet"
     elif rainfall <= 350 and humidity <= 50:
        climate_band = "dry"
     else:
        climate_band = "moderate"

    profiles = {
        "wet": {
            "Loamy": {"N": 95, "P": 45, "K": 50, "ph": 5.8},
            "Clay": {"N": 90, "P": 40, "K": 45, "ph": 5.5},
            "Sandy": {"N": 75, "P": 35, "K": 35, "ph": 6.2},
        },
        "moderate": {
            "Loamy": {"N": 65, "P": 35, "K": 35, "ph": 6.8},
            "Clay": {"N": 60, "P": 30, "K": 30, "ph": 6.6},
            "Sandy": {"N": 50, "P": 25, "K": 25, "ph": 7.0},
        },
        "dry": {
            "Loamy": {"N": 55, "P": 35, "K": 30, "ph": 7.2},
            "Clay": {"N": 50, "P": 30, "K": 25, "ph": 7.0},
            "Sandy": {"N": 45, "P": 30, "K": 25, "ph": 7.3},
        },
    }

    if climate_band == "dry" and temperature <= 26:
        dry_cool_profiles = {
            "Loamy": {"N": 55, "P": 35, "K": 30, "ph": 7.0},
            "Clay": {"N": 50, "P": 30, "K": 25, "ph": 6.8},
            "Sandy": {"N": 45, "P": 30, "K": 25, "ph": 7.0},
        }

        profile = dry_cool_profiles.get(
            soil_type,
            dry_cool_profiles["Loamy"]
        ).copy()
    else:
        profile = profiles[climate_band].get(
            soil_type,
            profiles[climate_band]["Loamy"]
        ).copy()

    if season == "Rabi":
        profile["N"] -= 5
    elif season == "Monsoon":
        profile["K"] += 5

    return profile
REGION_TO_CLIMATE = {
    # Wet Tropical
    "Tamil Nadu": "Wet Tropical",
    "Kerala": "Wet Tropical",
    "Assam": "Wet Tropical",
    "Meghalaya": "Wet Tropical",
    "Tripura": "Wet Tropical",
    "Andaman and Nicobar Islands": "Wet Tropical",
    "Lakshadweep": "Wet Tropical",

    # Humid Subtropical
    "West Bengal": "Humid Subtropical",
    "Bihar": "Humid Subtropical",
    "Jharkhand": "Humid Subtropical",
    "Odisha": "Humid Subtropical",
    "Uttar Pradesh": "Humid Subtropical",
    "Uttarakhand": "Humid Subtropical",
    "Sikkim": "Humid Subtropical",

    # Moderate Seasonal
    "Punjab": "Moderate Seasonal",
    "Haryana": "Moderate Seasonal",
    "Himachal Pradesh": "Moderate Seasonal",
    "Jammu and Kashmir": "Moderate Seasonal",
    "Ladakh": "Moderate Seasonal",
    "Chandigarh": "Moderate Seasonal",
    "Karnataka": "Moderate Seasonal",
    "Andhra Pradesh": "Moderate Seasonal",
    "Arunachal Pradesh": "Moderate Seasonal",
    "Nagaland": "Moderate Seasonal",
    "Manipur": "Moderate Seasonal",
    "Mizoram": "Moderate Seasonal",

    # Semi-Arid
    "Maharashtra": "Semi-Arid",
    "Telangana": "Semi-Arid",
    "Madhya Pradesh": "Semi-Arid",
    "Chhattisgarh": "Semi-Arid",
    "Gujarat": "Semi-Arid",
    "Goa": "Semi-Arid",
    "Delhi": "Semi-Arid",
    "Puducherry": "Semi-Arid",

    # Dry Arid
    "Rajasthan": "Dry Arid",
    "Dadra and Nagar Haveli and Daman and Diu": "Dry Arid",
}



def derive_features(input_data: dict) -> dict:
    derived = input_data.copy()

    soil_type = derived.get("soil_texture", "Loamy")
    rainfall = derived.get("rainfall", 500)
    humidity = derived.get("humidity", 50)
    season = derived.get("season", "Kharif")
    temperature = derived.get("temperature", 25)

    region = derived.get("region", "").strip()

    print("REGION:", region)
    print("AVAILABLE REGION KEYS:", REGION_TO_CLIMATE.keys())

    climate_zone = REGION_TO_CLIMATE.get(region, None)

    print("CLIMATE ZONE:", climate_zone)

    defaults = derive_dynamic_soil_values(
        soil_type,
        rainfall,
        humidity,
        season,
        temperature,
        climate_zone
    )

    for key, value in defaults.items():
        if derived.get(key) is None:
            derived[key] = value

    if derived.get("moisture") is None:
        derived["moisture"] = humidity

    if derived.get("historical_yield") is None:
        derived["historical_yield"] = 4.0

    if derived.get("market_price") is None:
        derived["market_price"] = 3000

    if derived.get("estimated_profit") is None:
        derived["estimated_profit"] = (
            derived["historical_yield"] *
            derived["market_price"] *
            10
        )

    if derived.get("moisture_category") is None:
        if derived["moisture"] < 30:
            derived["moisture_category"] = "Low"
        elif derived["moisture"] < 60:
            derived["moisture_category"] = "Medium"
        else:
            derived["moisture_category"] = "High"

    if derived.get("season_encoded") is None:
        season_map = {
            "Rabi": 0,
            "Kharif": 1,
            "Monsoon": 2
        }

        derived["season_encoded"] = season_map.get(
            season,
            1
        )

    return derived