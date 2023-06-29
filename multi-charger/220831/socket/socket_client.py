import socket
import json

HOST = '192.168.10.254'
PORT = 9000

chargerid = {"chargeid":"1234567890AAA"}
data = json.dumps(chargerid)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

send_data = client_socket.sendall(bytes(data.encode()))
recv_data = client_socket.recv(1024)
client_socket.close()
    
print('Send: {}'.format(send_data))
print('Received: {}'.format(recv_data.decode()))