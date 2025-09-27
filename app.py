from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


class InputData(BaseModel):
    area: float


# Load model from local pickle
model = joblib.load("model.pkl")


app = FastAPI(title="MLOps Capstone - Housing Price Predictor")


@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return {"prediction": prediction.tolist()}


@app.get("/")
def root():
    return {"message": "API is running!"}
