import socket
import pickle

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Połączono z serwerem")
    
    while True:
        try:
            data = s.recv(4096)
            
            if not data:
                break

            record = pickle.loads(data)
            print("Otrzymano rekord:", record)
            
        except EOFError:
            break
