import socket
import threading

# root name database (static)
root_db = {
    "google.com": "142.250.192.110",
    "youtube.com": "142.250.72.174",
    "openai.com": "104.18.13.135",
}

HOST = "127.0.0.1"
PORT = 5300

def handle_client(conn, addr):
    print(f"[Root Server] Connection from {addr}")
    data = conn.recv(1024).decode()
    print(f"[Root Server] Query received: {data}")

    ip = root_db.get(data, "NOT_FOUND")
    conn.send(ip.encode())
    conn.close()

def start():
    print("[Root Server] Starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[Root Server] Running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start()
