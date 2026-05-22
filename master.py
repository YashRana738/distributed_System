import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 5000

clients = []
time_diffs = {}

def handle_client(conn, addr):
    try:

        conn.sendall(b"TIME_REQUEST")

        client_time = float(conn.recv(1024).decode())
        server_time = time.time()

        diff = client_time - server_time
        time_diffs[conn] = diff

        print(f"[{addr}] Client Time: {client_time}, Diff: {diff}")

    except Exception as e:
        print("Error:", e)

def start_master():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Master started... Waiting for clients")

    while len(clients) < 3:
        conn, addr = server.accept()
        print(f"Connected: {addr}")
        clients.append(conn)

    threads = []
    for conn in clients:
        t = threading.Thread(target=handle_client, args=(conn, conn.getpeername()))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    all_diffs = list(time_diffs.values())
    all_diffs.append(0)

    avg_diff = sum(all_diffs) / len(all_diffs)
    print(f"\nAverage Time Difference: {avg_diff}")

    for conn in clients:
        adjustment = avg_diff - time_diffs[conn]
        conn.sendall(str(adjustment).encode())

    print("Adjustments sent. Closing connections.")

    for conn in clients:
        conn.close()

if __name__ == "__main__":
    start_master()
