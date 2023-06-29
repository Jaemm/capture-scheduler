class CanData(tk.Tk):
    def canreceive(socket):
        global status, chargingwatt, chargingtime
        first = True
        while True:
            try:
                data = socket.recv(1024)
                decoded_data = data.decode('utf-8')
                splited_data = decoded_data.split(' : ')
                splited_data = splited_data[1].split(' ')

                if splited_data[0] == '0x100':      
                    if splited_data[2] == '0' :
                        status.set("충전건 해제")
                    elif splited_data[2] == '1' :
                        status.set("충전건 연결")
                    elif splited_data[2] == '2' :
                        status.set("충전중")
                    elif splited_data[2] == '3' :
                        status.set("에러")                   
                    chargingwatt.set(str(int(splited_data[6]+splited_data[5], 16))+"W")                     
                if splited_data[0] == '0x101':
                    chargingtime.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")
                    
    def cansend(socket):
        global go_send, go_out, startflag, stopflag       
        while True:
            if go_send:          
                if startflag == 100:     
                    message = '100x1'
                    message_byte = message.encode('utf-8')
                    socket.send(message_byte)
                    break
                if stopflag == 100:
                    message = '100x0'
                    message_byte = message.encode('utf-8')
                    socket.send(message_byte)
                    break    
            else:
                if go_out:
                    exit()