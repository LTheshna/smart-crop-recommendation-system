from __future__ import annotations


CROP_ECONOMICS = {
    "rice": {"yield": 6.0, "price": 2200},
    "maize": {"yield": 5.5, "price": 1900},
    "chickpea": {"yield": 2.5, "price": 5500},
    "lentil": {"yield": 2.2, "price": 6000},
    "mothbeans": {"yield": 2.0, "price": 5000},
    "banana": {"yield": 30.0, "price": 1200},
    "papaya": {"yield": 25.0, "price": 1500},
    "cotton": {"yield": 2.0, "price": 7000},
    "pigeonpeas": {"yield": 2.5, "price": 6500},
}


def rank_recommendations(
    predictions: list[dict],
    market_prices: dict[str, float] | None = None,
    expected_yields: dict[str, float] | None = None,
) -> list[dict]:
    """
    Rank predicted crops using confidence and crop-specific economics.
    """

    ranked = []
    all_estimated_profits = []

    for pred in predictions:
        crop = pred["crop"].lower()

        economics = CROP_ECONOMICS.get(
            crop,
            {"yield": 4.0, "price": 3000}
        )

        estimated_profit = (
            economics["yield"] *
            economics["price"]
        )

        all_estimated_profits.append(
            estimated_profit
        )

    max_profit = max(all_estimated_profits) if all_estimated_profits else 1

    for pred in predictions:
        crop = pred["crop"]
        confidence = pred["confidence"]

        economics = CROP_ECONOMICS.get(
            crop.lower(),
            {"yield": 4.0, "price": 3000}
        )

        estimated_profit = (
            economics["yield"] *
            economics["price"]
        )

        normalized_profit = min(
    (estimated_profit / max_profit) * 100,
    85
)

        combined_score = (
    confidence * 0.75 +
    normalized_profit * 0.25
)

        ranked.append({
            "crop": crop,
            "confidence": confidence,
            "estimated_profit": round(
                estimated_profit,
                2
            ),
            "combined_score": round(
                combined_score,
                2
            )
        })

    ranked.sort(
        key=lambda x: x["combined_score"],
        reverse=True
    )

    return ranked


if __name__ == "__main__":
    sample_predictions = [
        {"crop": "Rice", "confidence": 90},
        {"crop": "Maize", "confidence": 80},
        {"crop": "Chickpea", "confidence": 70},
    ]

    ranked = rank_recommendations(
        sample_predictions
    )

    print("\nRanked Recommendations:")
    for rec in ranked:
        print(rec)