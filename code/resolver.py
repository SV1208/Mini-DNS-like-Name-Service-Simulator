import socket
import time
import threading

CACHE = {}
TTL = 25   # seconds

HOST = "127.0.0.1"
PORT = 5400
ROOT_HOST = "127.0.0.1"
ROOT_PORT = 5300

def ask_root_server(name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROOT_HOST, ROOT_PORT))
    s.send(name.encode())
    ip = s.recv(1024).decode()
    s.close()
    return ip

def resolve(name):
    now = time.time()

    # CACHE CHECK
    if name in CACHE:
        entry = CACHE[name]
        if now < entry["expires"]:
            print("[Resolver] CACHE HIT")
            return entry["ip"]
        else:
            print("[Resolver] CACHE EXPIRED")
            del CACHE[name]

    # CACHE MISS → Ask root server
    print("[Resolver] CACHE MISS → contacting Root Server...")
    ip = ask_root_server(name)

    if ip != "NOT_FOUND":
        CACHE[name] = {
            "ip": ip,
            "expires": now + TTL
        }
        print(f"[Resolver] Cached {name} for {TTL} sec")

    return ip

def handle_client(conn, addr):
    print(f"[Resolver] Connection from {addr}")
    name = conn.recv(1024).decode()

    ip = resolve(name)
    conn.send(ip.encode())
    conn.close()

def start():
    print("[Resolver] Starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[Resolver] Running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start()
