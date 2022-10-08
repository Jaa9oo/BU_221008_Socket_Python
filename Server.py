##Server


import socket
import threading

# 로컬호스트 서버 주소 -> 유니티에서 연결할 호스트와 동일
host = "127.0.0.1"
# 포트 주소 -> 유니티에서 연결할 포트와 동일
port = 65432

CONNs = []
ADDRs = []

def recv(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            SendBroadCast(data)
            print(data)

def SendBroadCast(_data):
    for _conn in CONNs:
        _conn.sendall(_data)




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    while True:
        conn, addr = s.accept()

        # 클라이언트 접속자 저장
        CONNs.append(conn)
        ADDRs.append(addr)

        # 다중 연결 스레드 구현
        t = threading.Thread(target=recv, args=(conn, addr))
        t.start()



       
# # TCP/IP 소켓을 생성하고
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

# # 소켓을 포트에 연결
# server_address = (host, port)
# print('Startinf up on {} port {}'.format(*server_address))
# sock.bind(server_address)

# # 연결을 기다림
# sock.listen()

# while True:
#     #연결을 기다림
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#     try:
#         print('connection from', client_address)

#         #작은 데이터를 받고 다시 전송
#         while True:
#             data = connection.recv(16)
#             print('received {!r}'.format(data))
#             if data:
#                 print('sending data back to the client')
#                 connection.sendall(data)
#             else:
#                 print('no data from', client_address)
#             break
#     finally:
#         # 연결 모두 지움
#         print("closing current connection")
#         connection.close()
