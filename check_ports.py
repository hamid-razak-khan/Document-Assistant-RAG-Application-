import socket

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

backend_open = check_port('127.0.0.1', 8000)
frontend_open = check_port('127.0.0.1', 3000)

print(f"Backend (8000): {'OPEN' if backend_open else 'CLOSED'}")
print(f"Frontend (3000): {'OPEN' if frontend_open else 'CLOSED'}")
