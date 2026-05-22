import socket
import time
import random

HOST = '127.0.0.1'
PORT = 5000

local_offset = random.randint(-5, 5)

def get_local_time():
    return time.time() + local_offset

def start_client():
    global local_offset

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    msg = client.recv(1024).decode()

    if msg == "TIME_REQUEST":
        local_time = get_local_time()
        print(f"[Client] Local Time: {local_time}")

        client.sendall(str(local_time).encode())

        adjustment = float(client.recv(1024).decode())
        print(f"[Client] Adjustment received: {adjustment}")

        local_offset += adjustment

        print(f"[Client] Updated Time: {get_local_time()}")

    client.close()

if __name__ == "__main__":
    start_client()
