from .zones import get_zones
import json

# ENDPOINT 1.
# /zones
# Przyjmuje: Nic
# Zwraca: JSON z zones'ami
# GET
def zones():
    data = get_zones()
    zones = json.dumps(data)

# ENDPOINT 2.
# /predict
# Przyjmuje JSON
# body = {
#     from: from,
#     to: to,
#     type: type,
#     persons: persons,
#     departure: departure
# };
# Zwraca JSON
# body = {
#     fee: ...,
#     time: ...,
#     fee_deviation: ...
# };
# GET
def predict(data):
    data_dict = json.loads(data)

    row_dict = {
        'passenger_count': data_dict["persons"],
        'trip_distance': data_dict["trip_distance"],
        'RatecodeID': data_dict["type"],
        'PULocationID': data_dict["from"],
        'DOLocationID': data_dict["to"],

        # Te 3 są niepotrzebne do predykcji
        'fare_amount': 0.0,
        'total_extras': 0.0,
        'trip_time': 0.0
    }

    # TUTAJ ROBIMY REQUEST NA /predict
    # data to będzie JSON w postaci stringa
    data:str = ...

    return data
