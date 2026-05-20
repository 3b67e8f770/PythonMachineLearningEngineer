from pydantic import BaseModel
from fastapi import FastAPI
from model import FraudDetectionModel


# 1. Inicjal FastAPI i model ML
app = FastAPI(title="Loss Prevention Model Service")
model = FraudDetectionModel()

# 2. Definiujemy Schema danych wejściowych przy użyciu Pydantic.
class TransactionInput(BaseModel):
    amount: float
    total_amount: float
    moving_avg_3: float

# 3. Endpoint typu POST.
#  http://localhost:8000/predict 
@app.post("/predict")
def predict_fraud(data: TransactionInput):
    # JSONa to Pythona by Pydantic
    prediction = model.predict(
        amount=data.amount,
        total_amount=data.total_amount,
        moving_avg_3=data.moving_avg_3
    )

# output = Dict, FastAPI: Dict to JSON
    return {
        "fraud_probability": round(prediction, 4),
        "model_version": model.version
    }