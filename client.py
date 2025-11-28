import socket

RESOLVER_HOST = "127.0.0.1"
RESOLVER_PORT = 5400

def query(domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RESOLVER_HOST, RESOLVER_PORT))
    s.send(domain.encode())
    ip = s.recv(1024).decode()
    s.close()
    return ip

if __name__ == "__main__":
    while True:
        domain = input("\nEnter domain name: ")
        ip = query(domain)
        print("IP Address:", ip)
