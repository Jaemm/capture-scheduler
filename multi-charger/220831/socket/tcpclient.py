import socket
import json

socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.10.254'
port = 9000

socket.connect((host, port))
print("socket server connect success...")

chargerid = {"01":"12345678910"}
data = json.dumps(chargerid)

send=socket.send(ascii(data.encode()))
print("send:",(send))
recv=socket.recv(1024)
print("recv:",recv)
# close=socket.close()
# print("socket close...")