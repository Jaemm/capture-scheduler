import json
import socket
import time
from _thread import *


# thread를 생성하는 threaded함수 구현
def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])  # addr[0]은 ip,addr[1]은 port

    while True:
        try:
            data = client_socket.recv(1024)  # client가 보낸 메세지를 받아 data에 저장
            if not data:
                print('Disconnected by '+addr[0], ':', addr[1])
                break
            
            # 받은 데이터 출력
            print('Received from '+':', data.decode())
            
            # client에 받은 데이터 재전송
            # client_socket.send(data)
            
            #
            for c in c_list:
                c.sendall((' : ' + data.decode()).encode())
                
        except ConnectionResetError as e:
            c_list.remove(client_socket)
            
            for c in c_list:
                c.sendall(('[System] ' + str(addr[1]) + ' 님이 나갔습니다.').encode())
            print('Disconnected by '+addr[0], ':', addr[1])
            break
    # client와 연결 끊음
    client_socket.close()


HOST = '127.0.0.1'
PORT = 9999
c_list = []

# socket생성 후 listen상태 만들기
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('server start')
addr = ''
while True:
    print('wait')

    client_socket, addr = server_socket.accept()
    print(client_socket, addr)
    c_list.append(client_socket)
    start_new_thread(threaded, (c_list[-1], addr))

server_socket.close()
