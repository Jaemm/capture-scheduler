from tkinter import *
import tkinter.ttk

from _thread import *
import threading

from time import sleep

import socket
from turtle import onclick

import requests

#================================================================
#
def send(socket):
    global go_send, go_out, startflag, stopflag
         
    while True:
        if go_send:
            if startflag == 1:     
                message = '1'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
            if stopflag == 1:
                message = '0'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
          
            url = 'http://127.0.0.1:5000/boot'
            rev_data = requests.get(url).json()
            print(rev_data)
            # 
            json_data = {
                'test':'test',
                'test':'test',
                'test':'test',
                'test':'test',
                'test':'test',
                'test':'test',
            }
            send_data = requests.post(url='http://127.0.0.1:5000/create', json=json_data)
            print(json_data)
            print("Server responded with %s" % send_data.status_code)
            #
            go_send = False
        else:
            if go_out:
                socket.close()
                exit()
            sleep(0.1)      

def receive(socket):
    first = True
    while True:
        try:
            data = socket.recv(1024)
            decoded_data = data.decode('utf-8')
            splited_data = decoded_data.split(' : ')
            splited_data = splited_data[1].split(' ')
            print(f'splited : {splited_data}')
#=========================================================================
#1번 충전기
            if splited_data[0] == '0x100':
                             
                #충전기 상태
                if splited_data[2] == '0' :
                    statusOneText_A1.set("disconnect")
                elif splited_data[2] == '1' :
                    statusOneText_A1.set("connect")
                elif splited_data[2] == '2' :
                    statusOneText_A1.set("charging")
                elif splited_data[2] == '3' :
                    statusOneText_A1.set("error")
                
                #충전 전류량
                ChargingCurrent_A1.set(str(int(splited_data[3], 16))+"A")
                
                #충전 전압
                Voltage_A1.set(str(int(splited_data[7], 16))+"V")
                
                #충전 전력량 (시작~종료시까지)
                ChargingWatt_A1.set(str(int(splited_data[5]+splited_data[6], 16))+"W")
                
                #충전 에러 코드
                ErrorCode_A1.set(str(int(splited_data[4], 16)))
                     
            if splited_data[0] == '0x101':
                
                #누적 전력량
                TotalWatt_A1.set(str(int(splited_data[4]+splited_data[3]+splited_data[2]+splited_data[1], 16))+"W")
                
                #충전 시간
                ChargingTime_A1.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")
                
                #프로그램 버전
                ProgramVer.set(str(int(splited_data[5], 16)))

#=========================================================================
#2번 충전기     
            if splited_data[0] == '0x110':
                secondTwoText.set(str(int(splited_data[1], 16)))
                energyTwoText.set(str(int(splited_data[3], 16)))
                voltTwoText.set(str(int(splited_data[6], 16)))
                
#=========================================================================
            if splited_data[0] == '0x120':
                secondThreeText.set(str(int(splited_data[1], 16)))
                energyThreeText.set(str(int(splited_data[3], 16)))
                voltThreeText.set(str(int(splited_data[6], 16)))
                
#========================================================================= 
            if splited_data[0] == '0x200' :
                powerOneText.set(str(int(splited_data[3]+splited_data[4],16))+"w")
        except ConnectionAbortedError as e:
            exit()              
        except ConnectionAbortedError as e:
            exit()

def login():
    # 서버의 ip주소 및 포트
    # HOST = '192.168.0.67'
    # PORT = 9999
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((HOST, PORT))

    threading.Thread(target=send, args=(client_socket,)).start()
    #threading.Thread(target=receive, args=(client_socket,)).start()
    exit()

def try_login():
    global go_out
    start_new_thread(login, ())
    go_out = False  

def set_go_send():
    global go_send
    go_send = True

#Tk GUI
window = Tk()
window.title("완속 멀티충전기")
window.geometry("1280x720")
window.resizable(True,True)

#서버 접속 
HOST = '192.168.0.67'
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#서버 데이터 받기
threading.Thread(target=receive, args=(client_socket,)).start()

#==========================================================================================
# 1번 충전기

#Tk 변수 선언
secondOneText = StringVar()
chargeOneText = StringVar()
powerOneText = StringVar()
firmwareText = StringVar()
powerOneText = StringVar()
chargingstatus_A1 = StringVar()
statusOneText_A1 = StringVar()
ChargingCurrent_A1 = StringVar()
ErrorCode_A1 = StringVar()
ChargingWatt_A1 = StringVar()
Voltage_A1 = StringVar()
TotalWatt_A1 = StringVar()
ProgramVer = StringVar()
ChargingTime_A1 = StringVar()

#시작 버튼
def startbtn1():
    global go_send, startflag, stopflag
    stopButton.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 1
    stopflag = 0
    
#정지 버튼    
def stopbtn1():
    global go_send, startflag, stopflag
    startButton.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 1
    
#화면 분류
frame1 = Frame(window, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)

#충전기 분류    
lbl1 = Label(frame1, text="A01", width=10, height=2, bg="lightgray")
lbl1.pack()
    
#충전 시작
startButton = Button(frame1, text="충전", width=12, height=5, bg="lightblue", command=startbtn1)
startButton.place(x=5, y=50)

#충전 중지
stopButton = Button(frame1, text="중단", width=12, height=5, bg="lightgray", command=stopbtn1)
stopButton.place(x=130, y=50)

#충전 진행바
# p_var1 = DoubleVar()
# progressbar1 = tkinter.ttk.Progressbar(frame1, maximum=10000, length=240, variable=p_var1)
# progressbar1.place(x=10, y=160, height=40)

#충전기 상태 화면
lb_TextstatusOneText_A1 = Label(frame1, text="충전기 상태", width=15, height=1, bg="lightblue")
lb_TextstatusOneText_A1.place(x=5, y=160)
lb_statusOneText_A1 = Label(frame1, textvariable=statusOneText_A1, bg="lightgray")
lb_statusOneText_A1.place(x=135, y=160, width=120, height=20)

#충전 전류 화면
lb_TextChargingCurrent_A1 = Label(frame1, text="충전 전류", width=15, height=1, bg="lightblue")
lb_TextChargingCurrent_A1.place(x=5, y=190)
lb_ChargingCurrent_A1 = Label(frame1, textvariable=ChargingCurrent_A1, bg="lightgray")
lb_ChargingCurrent_A1.place(x=135, y=190, width=120, height=20)

#충전 에러 코드 화면
# lb_TextErrorCode_A1 = Label(frame1, text="충전 에러 코드", width=15, height=1, bg="lightblue")
# lb_TextErrorCode_A1.place(x=5, y=310)
# lb_ErrorCode_A1 = Label(frame1, textvariable=ErrorCode_A1, bg="lightgray")
# lb_ErrorCode_A1.place(x=135, y=310, width=120, height=20)

#충전 전압 화면
lb_TextVoltage_A1 = Label(frame1, text="충전 전압", width=15, height=1, bg="lightblue")
lb_TextVoltage_A1.place(x=5, y=220)
lb_Voltage_A1 = Label(frame1, textvariable=Voltage_A1, bg="lightgray")
lb_Voltage_A1.place(x=135, y=220, width=120, height=20)

#충전 전력량 화면
lb_TextChargingWatt_A1 = Label(frame1, text="충전 전력량", width=15, height=1, bg="lightblue")
lb_TextChargingWatt_A1.place(x=5, y=250)
lb_ChargingWatt_A1 = Label(frame1, textvariable=ChargingWatt_A1, bg="lightgray")
lb_ChargingWatt_A1.place(x=135, y=250, width=120, height=20)

#누적 전력량 화면
lb_TextTotalWatt_A1 = Label(frame1, text="누적 전력량", width=15, height=1, bg="lightblue")
lb_TextTotalWatt_A1.place(x=5, y=280)
lb_TotalWatt_A1 = Label(frame1, textvariable=TotalWatt_A1, bg="lightgray")
lb_TotalWatt_A1.place(x=135, y=280, width=120, height=20)

#충전 시간 화면
lb_TextChargingTime_A1 = Label(frame1, text="충전 시간", width=15, height=1, bg="lightblue")
lb_TextChargingTime_A1.place(x=5, y=310)
lb_ChargingTime_A1 = Label(frame1, textvariable=ChargingTime_A1, bg="lightgray")
lb_ChargingTime_A1.place(x=135, y=310, width=120, height=20)

#충전 요금 화면
lbl5 = Label(frame1, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
entry5 = Label(frame1, text="292.9"+" 원/kWh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)

#프로그램 버전 화면
lb_TextProgramVer = Label(frame1, text="버전 정보", width=15, height=1, bg="lightblue")
lb_TextProgramVer.place(x=5, y=370)
lb_ProgramVer = Label(frame1, textvariable=ProgramVer, bg="lightgray")
lb_ProgramVer.place(x=135, y=370, width=120, height=20)


#==========================================================================================
# 2번 충전기

##
secondTwoText = StringVar()
voltTwoText = StringVar()
energyTwoText = StringVar()
chargeTwoText = StringVar()

##
frame2 = Frame(window, relief="solid", bd=2)
frame2.pack(side="left", fill="both", expand=True)

##
def startbtn2():
    progressbar2.start(1)
    stopButton.config(state=NORMAL)
    
##    
def stopbtn2():
    progressbar2.stop()
    
##    
startButton = Button(frame2, text="충전", width=12, height=5,bg="lightblue", command=startbtn2)
startButton.place(x=5, y=50)

##
stopButton = Button(frame2, text="중단", width=12, height=5, bg="lightgray", command=stopbtn2)
stopButton.place(x=130, y=50)

##
p_var2 = DoubleVar()
progressbar2 = tkinter.ttk.Progressbar(frame2, maximum=10000, length=240, variable=p_var2)
progressbar2.place(x=10, y=160, height=70)

##
lbl1 = Label(frame2, text="A02", width=10, height=2, bg="lightgray")
lbl1.pack()

##
lbl2 = Label(frame2, text="충전 시간", width=15, height=1, bg="lightblue")
lbl2.place(x=5, y=250)
seconds = Label(frame2, textvariable=secondTwoText, bg="lightgray")
seconds.place(x=135, y=250, width=120, height=20)

##
lbl3 = Label(frame2, text="충전 전력", width=15, height=1, bg="lightblue")
lbl3.place(x=5, y=280)
entry3 = Label(frame2, textvariable=voltTwoText, bg="lightgray")
entry3.place(x=135, y=280, width=120, height=20)

##
lbl4 = Label(frame2, text="누적 충전 에너지", width=15, height=1, bg="lightblue")
lbl4.place(x=5, y=310)
entry4 = Label(frame2, textvariable=energyTwoText, bg="lightgray")
entry4.place(x=135, y=310, width=120, height=20)

##
lbl5 = Label(frame2, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
entry5 = Label(frame2, text="292.9"+"원/kwh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)



#========================================================================================
# 3번 충전기
##
secondThreeText = StringVar()
voltThreeText = StringVar()
energyThreeText = StringVar()
chargeThreeText = StringVar()

##
frame3 = Frame(window, relief="solid", bd=2)
frame3.pack(side="left", fill="both", expand=True)

##
def startbtn3():
    progressbar3.start(1)
    
##    
def stopbtn3():
    progressbar3.stop()
    
##   
startButton = Button(frame3, text="충전", width=12, height=5,bg="lightblue", command=startbtn3)
startButton.place(x=5, y=50)

##
stopButton = Button(frame3, text="중단", width=12, height=5, bg="lightgray", command=stopbtn3)
stopButton.place(x=130, y=50)

##
p_var3 = DoubleVar()
progressbar3 = tkinter.ttk.Progressbar(frame3, maximum=10000, length=240, variable=p_var3)
progressbar3.place(x=10, y=160, height=70)

##
lbl1 = Label(frame3, text="A03", width=10, height=2, bg="lightgray")
lbl1.pack()

##
lbl2 = Label(frame3, text="충전 시간", width=15, height=1, bg="lightblue")
lbl2.place(x=5, y=250)
seconds = Label(frame3, textvariable=secondThreeText, bg="lightgray")
seconds.place(x=135, y=250, width=120, height=20)

##
lbl3 = Label(frame3, text="충전 전력", width=15, height=1, bg="lightblue")
lbl3.place(x=5, y=280)
entry3 = Label(frame3, textvariable=voltThreeText, bg="lightgray")
entry3.place(x=135, y=280, width=120, height=20)

##
lbl4 = Label(frame3, text="누적 충전 에너지", width=15, height=1, bg="lightblue")
lbl4.place(x=5, y=310)
entry4 = Label(frame3, textvariable=energyThreeText, bg="lightgray")
entry4.place(x=135, y=310, width=120, height=20)

##
lbl5 = Label(frame3, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
entry5 = Label(frame3, text="292.9"+"원/kwh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)

##
window.mainloop()

#=================================================================================

##
HOST = '127.0.0.1'
PORT = 9999

## socket 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

##
while True:
    # 서버로 부터 메세지 받기
    message = 'hello'
    # 메세지 전송
    client_socket.send(message.encode())
    data = client_socket.recv(1024)
    print('received from the server:', repr(data.decode()))
    
##
client_socket.close()