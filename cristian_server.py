import socket
import time
from datetime import datetime

def cristian_server():

    host = '127.0.0.1'
    port = 8011

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Cristian's Time Server started on {host}:{port}")
        print("Waiting for clock synchronization requests...")

        while True:

            conn, addr = server_socket.accept()
            print(f"Request received from {addr}")

            server_time = time.time()

            conn.send(str(server_time).encode())

            print(f"Sent server time: {datetime.fromtimestamp(server_time).strftime('%Y-%m-%d %H:%M:%S.%f')}")

            conn.close()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    cristian_server()
