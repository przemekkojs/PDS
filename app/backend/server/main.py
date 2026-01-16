import time
import pickle
import pandas as pd
import requests

HOST = '127.0.0.1'
PORT = 65432
INTERVAL = 1 # To jest w sekundach
DATA_PATH:str = "contents/yellow_tripdata_2025-08.parquet"

df = pd.read_parquet(DATA_PATH)

if __name__ == "__main__":
    for _, row in df.iterrows():
        record = row.to_dict()
        data = pickle.dumps(record)
        # Request na http://{HOST}:{PORT}/receive?data={data}
        
        print("Wysłano rekord:", record)
        time.sleep(INTERVAL)
