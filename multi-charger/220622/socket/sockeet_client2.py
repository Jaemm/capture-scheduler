import json
import socket 

HOST = '192.168.10.254'
PORT = 9000

header = []
header.append(0x20)

di = {}
di["01"] = "12345678910"
body = json.dumps(di)

leng = len(body)

message = bytearray(header)
message += bytearray(leng.to_bytes(2, byteorder="big"))
message += bytes(body,'utf-8')
print("send Message: ",message)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.sendall(message)

data = client_socket.recv(1024)
print('Server Received my Message~!')
print('recv Message:',data)
client_socket.close()