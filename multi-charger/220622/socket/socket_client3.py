import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_address = ('192.168.10.254', 9000)
sock.bind(recv_address)

sock.listen(1)
 
conn, addr = sock.accept()

# recv and send loop
while 1:
    data = conn.recv()
    # 받고 data를 돌려줌.
    conn.send(data)

conn.close()