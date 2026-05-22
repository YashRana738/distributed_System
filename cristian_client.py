import socket
import time
from datetime import datetime

def cristian_client():

    host = '127.0.0.1'
    port = 8011

    t0 = time.time()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client_socket.connect((host, port))

        server_time_str = client_socket.recv(1024).decode()
        t_server = float(server_time_str)

        t1 = time.time()

        rtt = t1 - t0

        synchronized_time = t_server + (rtt / 2)

        print("--- Cristian's Algorithm Synchronization ---")
        print(f"Request sent at (T0):      {datetime.fromtimestamp(t0).strftime('%H:%M:%S.%f')}")
        print(f"Server time received:      {datetime.fromtimestamp(t_server).strftime('%H:%M:%S.%f')}")
        print(f"Response received at (T1): {datetime.fromtimestamp(t1).strftime('%H:%M:%S.%f')}")
        print(f"Round Trip Time (RTT):     {rtt:.6f} seconds")
        print(f"Clock Adjustment (RTT/2):  {rtt/2:.6f} seconds")
        print(f"-------------------------------------------")
        print(f"Client Processed Time:     {datetime.fromtimestamp(synchronized_time).strftime('%H:%M:%S.%f')}")
        print(f"Actual Local Time:        {datetime.fromtimestamp(t1).strftime('%H:%M:%S.%f')}")

    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    cristian_client()
