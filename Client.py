##Client


import socket

# 로컬호스트 서버 주소
host = "127.0.0.1"
# 포트 주소
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b"Hello, World")
    data = s.recv(1024)
    
print(f"Received {data!r}")