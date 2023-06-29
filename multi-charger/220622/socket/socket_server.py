import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('192.168.225.1', 20))

server_socket.listen(1)
print("server standby")

client_socket, addr = server_socket.accept()
print("connected by", addr)

data = client_socket.recv(1024)
print("received from :", addr, data.decode())
    
client_socket.send(data)

server_socket.close()
print("socket closed. end")