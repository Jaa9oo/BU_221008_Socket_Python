##Server


import socket
import threading
import cv2
from matplotlib import pyplot as plt
import numpy as np
# import io

# 로컬호스트 서버 주소 -> 유니티에서 연결할 호스트와 동일
host = "127.0.0.1"
# 포트 주소 -> 유니티에서 연결할 포트와 동일
port = 65432

CONNs = []
ADDRs = []

isImgDown = False
imgSize = 1024

def recv(conn, addr):
    global isImgDown
    global imgSize
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(imgSize)
            # print(data)

            if not data:
                break

            # 이미지 수신 모드일경우
            if (isImgDown) :
                # 수신 데이터 변환
                encoded_img = np.frombuffer(data, dtype = np.uint8)
                # print(encoded_img)
                
                # 변환된 데이터 이미지 변환
                img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
                # img_Color = cv2.imread(img, 1)

                # 이미지 출력
                cv2.imshow('color', img)
                cv2.waitKey(0) 

                # 바이트 크기 일반 메세지 전송 크기로 수정
                imgsize = 1024

                # 이미지 수신 모드 해제
                isImgDown = False
            else :
                # 데이터 디코드
                result = data.decode('utf-8')
                
                # 이미지 수신 명령 여부 확인
                if("LoadImg" in result) :
                    # 송신부에 이미지 수신 준비 완료 전송
                    send = "LoadImgOk"
                    conn.sendall(send.encode('utf-8'))
                    
                    # 이미지 수신 모드 설정
                    isImgDown = True

                    # 수신 데이터에서 전송될 이미지 크기 확인하여 바이트 크기 설정
                    imgcnt = result.split('_')
                    imgSize = int(imgcnt[1])
                else :
                    conn.sendall(data)
                    SendBroadCast(data)
                    print(data)
                    imgsize = 1024


def SendBroadCast(_data):
    for _conn in CONNs:
        _conn.sendall(_data)

def ImgShow(_data):
    img_gray = cv2.imread(_data,0) #cv2.IMREAD_GRAYSCALE
    img_color = cv2.imread(_data,1) #cv2.IMREAD_COLOR
    cv2.imshow('gray', img_gray)
    cv2.imshow('color', img_color)
    cv2.waitKey(0) 




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
