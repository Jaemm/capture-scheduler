import can
import socket
import os
import time
from __future__ import print_function

HOST = '127.0.0.1'
PORT = 9999

# 리눅스 CAN통신 연결
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
except OSError:
    print('Cannot find PiCAN board.')
    exit()
# socket 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

##   
while True:
    message = bus.recv()
    c = '{0:x} {1:x} '.format(message.arbitration_id, message.dlc)
    s = hex(message.arbitration_id)+' '
    for i in range(message.dlc):
        s += '{0:x} '.format(message.data[i])
    time.sleep(1)   
    # 메세지 전송
    client_socket.send(s.encode())
    # 서버로 부터 메세지 받기
    data1 = client_socket.recv(1024)
    data_str = data1.decode('utf-8')
    if data_str == '1' :
        msg = can.Message(arbitration_id=0x200,
                  data=[0,0,0,10,1,0,0,0],
                  is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
            print(msg)
        except can.CanError:
            print("Messge NOT sent")
    ###
    if data1 == '0' :
        msg = can.Message(arbitration_id=0x200,
                  data=[0,0,0,10,0,1,0,0],
                  is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Messge NOT sent")
            
    print('received from the server:', repr(data1.decode()))
    
client_socket.close()