from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.feature_derivation import derive_features
from ml.training.predict_crop import predict_top_crops
from ml.training.rank_recommendations import rank_recommendations


app = FastAPI(title="Smart Crop Recommendation API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CropInput(BaseModel):
    region: str
    soil_texture: str
    season: str

    temperature: float = Field(..., ge=5, le=50)
    humidity: float = Field(..., ge=0, le=100)
    rainfall: float = Field(..., ge=0, le=3000)

    N: Optional[float] = Field(None, ge=0, le=300)
    P: Optional[float] = Field(None, ge=0, le=300)
    K: Optional[float] = Field(None, ge=0, le=300)

    ph: Optional[float] = Field(None, ge=3, le=10)
    moisture: Optional[float] = Field(None, ge=0, le=100)

    historical_yield: Optional[float] = Field(None, ge=0, le=20)
    market_price: Optional[float] = Field(None, ge=0)
    estimated_profit: Optional[float] = Field(None, ge=0)

    moisture_category: Optional[str] = None
    season_encoded: Optional[int] = None


@app.get("/")
def root():
    return {
        "message": "Smart Crop Recommendation API Running"
    }


@app.post("/recommend")
def recommend_crop(data: CropInput):
    raw_input = data.dict()

    input_dict = derive_features(raw_input)

    print("FINAL INPUT TO MODEL:")
    print(input_dict)

    predictions = predict_top_crops(input_dict)

    if predictions[0]["crop"] in [
        "Low Confidence Recommendation",
        "No Suitable Crop Found"
    ]:
        return {
            "recommendations": predictions
        }

    predictions = [
    pred for pred in predictions
    if pred["confidence"] >= 10
]

    predictions = predictions[:3]

    total_confidence = sum(
    pred["confidence"] for pred in predictions
)
    if total_confidence > 0:
        for pred in predictions:
          pred["confidence"] = round(
            (pred["confidence"] / total_confidence) * 100,
            2
        )
    print("AFTER RENORMALIZATION:", predictions)
          

    override_crops = {
        "chickpea", "lentil", "mothbeans",
        "rice", "banana", "papaya",
        "maize", "cotton", "pigeonpeas"
    }

    if all(
        pred["crop"] in override_crops
        for pred in predictions
    ):
        return {
            "recommendations": predictions
        }

    print("PREDICTIONS BEFORE RANKING:", predictions)

    ranked = rank_recommendations(predictions)

    print("RANKED OUTPUT:", ranked)

    return {
        "recommendations": ranked
    }