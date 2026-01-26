from zones import get_zones, calculate_trip_distance
from utils import process_row, retr, predict_info

import lightgbm as lgb
from datetime import datetime
import json
import pandas as pd

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_WINDOW_SIZE = 100
buffer_window = []
fee_model = lgb.Booster(model_file="models/pred_fee.txt")
time_model = lgb.Booster(model_file="models/pred_time.txt")

class PredictRequest(BaseModel):
    start: int
    end: int
    type: int
    persons: int
    departure: str | None = None
    tip: float = 0.0

    class Config:
        validate_by_name = True

class PredictResponse(BaseModel):
    fee: float
    time: float
    dist: float

@app.get("/zones")
def zones() -> Dict[str, Any]:
    try:
        data = get_zones()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    try:
        trip_distance = calculate_trip_distance(data.start, data.end)

        row_dict = {
            'passenger_count': data.persons,
            'trip_distance': trip_distance,
            'RatecodeID': data.type,
            'PULocationID': data.start,
            'DOLocationID': data.end,

            'fare_amount': 0.0,
            'total_extras': data.tip,
            'trip_time': 0.0
        }

        fee, time, dist = predict_info(row_dict, fee_model, time_model)

        return {
            "fee": fee,
            "time": time,
            "dist": dist
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/receive")
def receive(data: bytes = Body(...)):
    global buffer_window, fee_model, time_model

    try:
        row = pickle.loads(data)
        r = process_row(row)
        buffer_window.append(r)

        if len(buffer_window) > MAX_WINDOW_SIZE:
            buffer_window, fee_model, time_model = retr(buffer_window, fee_model, time_model)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
