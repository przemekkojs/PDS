import lightgbm as lgb
from datetime import datetime
from .utils import retrain, process_row
import json
import pandas as pd

LAST_TRAIN_TIME = datetime.now()
DEFAULT_WINDOW = 60
MAX_WINDOW_SIZE = 100

buffer_window = []
fee_model = lgb.Booster(model_file="contents/pred_fee.txt")
time_model = lgb.Booster(model_file="contents/pred_time.txt")

# ENDPOINT 1.
# /retr
# POST
def retr():
    fee_model = retrain(LAST_TRAIN_TIME, DEFAULT_WINDOW, fee_model, buffer_window, 'fare_amount')
    time_model = retrain(LAST_TRAIN_TIME, DEFAULT_WINDOW, time_model, buffer_window, 'trip_time')

    buffer_window.clear()

# ENDPOINT 2.
# /receive
# Przyjmuje: rekord w formacie pickle
# POST
def receive(data):
    try:
        r = process_row(data)
        buffer_window.append(r)

        if len(buffer_window) > MAX_WINDOW_SIZE:
            retr()

    except Exception as e:
        print(str(e))

# ENDPOINT 3.
# /predict
# Przyjmuje JSON
# GET
def predict(data):
    row = pd.DataFrame(data)

    return json.dumps({
        "fee" : 5,
        "time" : 300,
        "fee_deviation" : 1
    })
