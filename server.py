import socket
import threading

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    while True:
        try:

            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"From {addr}: {data}")

            reply = input(f"Reply to {addr} -> ")
            conn.send(reply.encode())

        except Exception as e:
            print(f"Error with connection from {addr}: {e}")
            break

    conn.close()
    print(f"Connection closed with {addr}")

def server_program():

    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print("Server started... Waiting for connections")

    while True:

        conn, addr = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    server_program()
