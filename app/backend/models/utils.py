import lightgbm as lgb
import pandas as pd

from datetime import datetime
import os
import pickle

def retrain(last_train_time: datetime, window: int, model, buffer_window, y_name="fare_amount"):
    current_time = datetime.now()

    if (current_time - last_train_time).total_seconds() < window:
        print("Za wcześnie na douczanie")
        return None

    tmp_filename = f"model_tmp_{current_time.strftime('%Y%m%d_%H%M%S')}.txt"
    model.save_model(tmp_filename)

    try:
        model_copy = lgb.Booster(model_file=tmp_filename)

        tmp_df = pd.DataFrame(buffer_window)

        if tmp_df.empty or y_name not in tmp_df.columns:
            return None

        X_train = tmp_df.drop(columns=[y_name])
        y_train = tmp_df[y_name]

        train_data = lgb.Dataset(X_train, label=y_train)

        model_copy = lgb.train(
            params=model_copy.params,
            train_set=train_data,
            init_model=model_copy,
            keep_training_booster=True
        )

        return model_copy

    finally:
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def check(record, col) -> bool:
    return col not in record or record[col] is None and record[col] != 'nan'

def process_row(data) -> dict:
    record:dict = pickle.loads(data)

    fill_values = {
        'passenger_count': 1,
        'RatecodeID': 1,
        'store_and_fwd_flag': 'N',
        'congestion_surcharge': 0,
        'Airport_fee': 0,
        'cbd_congestion_fee': 0
    }
    
    filter_cols = ['extra', 'mta_tax', 'tolls_amount', 'improvement_surcharge', 'congestion_surcharge', 'Airport_fee', 'fare_amount', "cbd_congestion_fee"]
    total_cols = ['extra', 'mta_tax', 'tolls_amount', 'improvement_surcharge', 'congestion_surcharge', 'Airport_fee', "cbd_congestion_fee"]
    int_cols = ["PULocationID", "DOLocationID", "RatecodeID", "passenger_count"]
    float_cols = ["trip_time", "total_extras", "trip_distance", "fare_amount"]
    drop_cols = ["VendorID", "store_and_fwd_flag", "payment_type", "tip_amount", "total_amount"]

    for col, val in fill_values.items():
        if check(record, col):
            record[col] = val

    for col in filter_cols:
        if check(record, col):
            if record[col] < 0:
                return None
            
    total_extras = 0.0
    
    for col in total_cols:
        if check(record, col):
            total_extras += float(record[col])
            del record[col]

    record["total_extras"] = total_extras

    try:
        pickup = datetime.fromisoformat(record["tpep_pickup_datetime"])
        dropoff = datetime.fromisoformat(record["tpep_dropoff_datetime"])
        trip_time = (dropoff - pickup).total_seconds()

        if trip_time < 0:
            return None

        record["trip_time"] = trip_time
    except Exception:
        return None

    del record["tpep_pickup_datetime"]
    del record["tpep_dropoff_datetime"]

    for col in int_cols:
        if check(record, col):
            record[col] = int(record[col])

    for col in float_cols:
        if check(record, col):
            record[col] = float(record[col])

    good_cols = ["passenger_count", "trip_distance", "RatecodeID", "PULocationID", "DOLocationID", "fare_amount", "total_extras", "trip_time"]
    record = {k: record[k] for k in good_cols if k in record}

    return record