import socket
import time
import pickle
import pandas as pd

HOST = '127.0.0.1'
PORT = 65432
INTERVAL = 1
DATA_PATH:str = "data/yellow_tripdata_2025-08.parquet"

df = pd.read_parquet(DATA_PATH)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")
    conn, addr = s.accept()

    with conn:
        print(f"Połączono z {addr}")

        for _, row in df.iterrows():
            record = row.to_dict()
            data = pickle.dumps(record)
            conn.sendall(data)
            
            print("Wysłano rekord:", record)
            time.sleep(INTERVAL)
