from ast import Set
from email import header
from email.mime import image
from tkinter import *
import tkinter.ttk
import tkinter.font
import tkinter as tk
from tkinter import Place, Tk
from _thread import *
import threading
from time import sleep
import socket
from turtle import bgcolor, color, onclick



#소켓을 통해 데이터 전송 하는 함수
def send(socket):
    global go_send, go_out, startflag, stopflag       
    while True:
        if go_send:

            #1번 충전기 충전, 정지 전송 신호
            #충전          
            if startflag == 100:     
                message = '100x1'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break
            #정지
            if stopflag == 100:
                message = '100x0'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break

            #2번 충전기 충전, 정지 전송 신호
            #충전
            if startflag == 110:     
                message = '110x1'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break
            
            #정지
            if stopflag == 110:
                message = '110x0'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break

            #3번 충전기 충전, 정지 전송 신호
            #충전
            if startflag == 120:     
                message = '120x1'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break
            
            #정지
            if stopflag == 120:
                message = '120x0'
                message_byte = message.encode('utf-8')
                socket.send(message_byte)
                break               
        else:
            if go_out:
                exit()
                  
#소켓을 통해 데이터 수신 하는 함수
def receive(socket):
    global status_a1_json, chargingwatt_a1_json, chargingtime_a1_json
    first = True
    while True:
        try:
            data = socket.recv(1024)
            decoded_data = data.decode('utf-8')
            splited_data = decoded_data.split(' : ')
            splited_data = splited_data[1].split(' ')

            #1번 충전기 CAN 데이터 분석
            if splited_data[0] == '0x100':      
                #충전기 상태
                if splited_data[2] == '0' :
                    status_a1_json = ("disconnect")
                    status_a1.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status_a1_json = ("connect")
                    status_a1.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status_a1_json = ("charging")
                    status_a1.set("충전중")
                elif splited_data[2] == '3' :
                    status_a1_json = ("error")
                    status_a1.set("에러")
                
                #충전 전력량 (시작~종료시까지)
                chargingwatt_a1.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
                chargingwatt_a1_json = (str(int(splited_data[6]+splited_data[5], 16))+"W")
                     
            if splited_data[0] == '0x101':
                #충전 시간
                chargingtime_a1.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")
                chargingtime_a1_json = (str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")

            #2번 충전기 CAN 데이터 분석
            if splited_data[0] == '0x110':
                if splited_data[2] == '0' :
                    status_a2.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status_a2.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status_a2.set("충전중")
                elif splited_data[2] == '3' :
                    status_a2.set("에러")
                
                #충전 전력량 (시작~종료시까지)
                chargingwatt_a2.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
                
            if splited_data[0] == '0x111':
                
                #충전 시간
                chargingtime_a2.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")           
                
            #3번 충전기 CAN 데이터 분석
            if splited_data[0] == '0x120':
                             
                #충전기 상태
                if splited_data[2] == '0' :
                    status_a3.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status_a3.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status_a3.set("충전중")
                elif splited_data[2] == '3' :
                    status_a3.set("에러")
                
                #충전 전력량 (시작~종료시까지)
                chargingwatt_a3.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
                
            if splited_data[0] == '0x121':
                
                #충전 시간
                chargingtime_a3.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")
                
        except ConnectionAbortedError as e:
            exit()

def login():
    threading.Thread(target=send, args=(client_socket,)).start()
    exit()

def try_login():
    global go_out
    start_new_thread(login, ())
    go_out = False  

def set_go_send():
    global go_send
    go_send = True
    
window = Tk()
window.title("First C&D")
window.geometry("1280x720")
window.resizable(True,True)    

fram1 = Frame()

#서버 접속 
# HOST = '127.0.0.1'
# PORT = 9999
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

#서버 데이터 받기
threading.Thread(target=receive, args=(client_socket,)).start()

# 1번 충전기 GUI
#Tk 변수 선언
status_a1 = StringVar()
chargingwatt_a1 = StringVar()
totalwatt_a1 = StringVar()
chargingtime_a1 = StringVar()

#시작 버튼
def startbtn_a1():
    global go_send, startflag, stopflag
    btn_stop_a1.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 100
    stopflag = 0
    
#정지 버튼    
def stopbtn_a1():
    global go_send, startflag, stopflag
    btn_start_a1.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 100
    
#화면 분류
frame1 = Frame(window, relief="solid", bd=2, bg='black')
frame1.pack(side="left", fill="both", expand=True)

#충전기 제어 버튼   
btn_title_a1 = Button(frame1, text="1m", width=5, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=10, y=20)

btn_title_a1 = Button(frame1, text="2m", width=5, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=60, y=20)

btn_title_a1 = Button(frame1, text="3m", width=5, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=110, y=20)

btn_title_a1 = Button(frame1, text="충전", width=5, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=160, y=20)

btn_title_a1 = Button(frame1, text="정지", width=5, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=210, y=20)


def openFrame(frame):
    frame.tkraise()
    
#충전 이미지
image1 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame1, image=image1, width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=78)

#충전기 상태 화면
lb_status_attr_a1 = Label(frame1, text="충전건 상태", width=15, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a1.place(x=5, y=250)
lb_status_value_a1 = Label(frame1, textvariable=status_a1, bg="#1E1E2A", fg='white')
lb_status_value_a1.place(x=135, y=250, width=120, height=20)

#충전 전력량 화면
lb_chargingwatt_attr_a1 = Label(frame1, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingwatt_attr_a1.place(x=5, y=280)
lb_chargingwatt_value_a1 = Label(frame1, textvariable=chargingwatt_a1, bg="#1E1E2A", fg='white')
lb_chargingwatt_value_a1.place(x=135, y=280, width=120, height=20)

#충전 요금 화면
lb_chargingamount_attr_a1 = Label(frame1, text="충전 요금", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a1.place(x=5, y=310)
lb_chargingamount_value_a1 = Label(frame1, bg="#1E1E2A", fg='white')
lb_chargingamount_value_a1.place(x=135, y=310, width=120, height=20)

#충전 시간 화면
lb_chargingtime_attr_a1 = Label(frame1, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a1.place(x=5, y=340)
lb_chargingtime_value_a1 = Label(frame1, textvariable=chargingtime_a1, bg="#1E1E2A", fg='white')
lb_chargingtime_value_a1.place(x=135, y=340, width=120, height=20)

# 2번 충전기 GUI
#Tk 변수 선언
status_a2 = StringVar()
chargingwatt_a2 = StringVar()
totalwatt_a2 = StringVar()
chargingtime_a2 = StringVar()

#시작 버튼
def startbtn_a2():
    global go_send, startflag, stopflag, image2
    btn_stop_a2.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 110
    stopflag = 0
    image2 = tkinter.PhotoImage(file = "charging.png" )
    label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=40)
    
#정지 버튼    
def stopbtn_a2():
    global go_send, startflag, stopflag, image2
    btn_start_a2.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 110
    image2 = tkinter.PhotoImage(file = "connect.png" )
    label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=40)
    
#화면 분류
frame2 = Frame(window, relief="solid", bd=2, bg='black')
frame2.pack(side="left", fill="both", expand=True)

#충전기 분류    
btn_title_a2 = Button(frame2, text="N번 커넥터 상세제어", width=30, height=2, bg="#1E1E2A", fg="white")
btn_title_a2.place(x=20, y=20)

#충전 이미지
image2 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=78)

#충전기 상태 화면
lb_status_attr_a2 = Label(frame2, text="충전건 상태", width=15, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a2.place(x=5, y=250)
lb_status_value_a2 = Label(frame2, textvariable=status_a2, bg="#1E1E2A", fg='white')
lb_status_value_a2.place(x=135, y=250, width=120, height=20)

#충전 전력량 화면
lb_chargingWatt_attr_a2 = Label(frame2, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingWatt_attr_a2.place(x=5, y=280)
lb_chargingWatt_value_a2 = Label(frame2, textvariable=chargingwatt_a2, bg="#1E1E2A", fg='white')
lb_chargingWatt_value_a2.place(x=135, y=280, width=120, height=20)

#충전 요금 화면
lb_chargingamount_attr_a2 = Label(frame2, text="충전 요금", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a2.place(x=5, y=310)
lb_chargingamount_value_a2 = Label(frame2, bg="#1E1E2A", fg='white')
lb_chargingamount_value_a2.place(x=135, y=310, width=120, height=20)

#충전 시간 화면
lb_chargingtime_attr_a2 = Label(frame2, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a2.place(x=5, y=340)
lb_chargingtime_value_a2 = Label(frame2, textvariable=chargingtime_a2, bg="#1E1E2A", fg='white')
lb_chargingtime_value_a2.place(x=135, y=340, width=120, height=20)

# 3번 충전기 GUI

#Tk 변수 선언
status_a3 = StringVar()
chargingwatt_a3 = StringVar()
totalwatt_a3 = StringVar()
chargingtime_a3 = StringVar()

#시작 버튼
def startbtn_a3():
    global go_send, startflag, stopflag
    btn_stop_a3.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 120
    stopflag = 0
    
#정지 버튼    
def stopbtn_a3():
    global go_send, startflag, stopflag
    btn_start_a3.config(state=NORMAL)
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 120
    
#화면 분류
frame3 = Frame(window, relief="solid", bd=2, bg='black')
frame3.pack(side="left", fill="both", expand=True)

#충전기 분류    
btn_title_a3 = Button(frame3, text="N번 커넥터 상세제어", width=30, height=2, bg="#1E1E2A", fg="white")
btn_title_a3.place(x=20, y=20)

#충전 이미지
image3 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame3, image=image3,width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=78)

#충전기 상태 화면
lb_status_attr_a3 = Label(frame3, text="충전기 상태", width=15, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a3.place(x=5, y=250)
lb_status_value_a3 = Label(frame3, textvariable=status_a3, bg="#1E1E2A", fg='white')
lb_status_value_a3.place(x=135, y=250, width=120, height=20)

#충전 전력량 화면
lb_chargingwatt_attr_a3 = Label(frame3, text="충전 전력량", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingwatt_attr_a3.place(x=5, y=280)
lb_chargingwatt_value_a3 = Label(frame3, textvariable=chargingwatt_a3, bg="#1E1E2A", fg='white')
lb_chargingwatt_value_a3.place(x=135, y=280, width=120, height=20)

#충전 요금 화면
lb_chargingamount_attr_a3 = Label(frame3, text="충전 요금", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a3.place(x=5, y=310)
lb_chargingamount_value_a3 = Label(frame3, bg="#1E1E2A", fg='white')
lb_chargingamount_value_a3.place(x=135, y=310, width=120, height=20)

#충전 시간 화면
lb_chargingtime_attr_a3 = Label(frame3, text="충전 시간", width=15, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a3.place(x=5, y=340)
lb_chargingtime_value_a3 = Label(frame3, textvariable=chargingtime_a3, bg="#1E1E2A", fg='white')
lb_chargingtime_value_a3.place(x=135, y=340, width=120, height=20)

window.mainloop()
client_socket.close()