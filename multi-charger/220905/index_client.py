import socket
import threading
import time
import tkinter as tk
import tkinter.font
import tkinter.ttk
from _thread import *
from ast import Set
from email import header
from email.mime import image
from time import sleep
from tkinter import *
from tkinter import Place, Tk
from turtle import bgcolor, color, onclick

# import RPi.GPIO as GPIO
import serial


def sersend():
    ser  = serial.Serial("/dev/serial0",9600)
    ser.write(bytes(bytearray([2,1,48,49,0,0,0,0])))
    time.sleep(3)
    ser.close()
    
def sersend2():
    ser  = serial.Serial("/dev/serial0",9600)
    ser.write(bytes(bytearray([2,1,48,50,0,0,0,0])))
    ser.close()
    
def sersend3():
    ser  = serial.Serial("/dev/serial0",9600)
    ser.write(bytes(bytearray([2,1,48,51,0,0,0,0])))
    ser.close()
    
def serstop():
    ser  = serial.Serial("/dev/serial0",9600)
    ser.write(bytes(bytearray([2,1,48,48,0,0,0,0])))
    ser.close()
    
#소켓을 통해 데이터 전송 하는 함수
def cansend(socket):
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
def canreceive(socket):
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
    threading.Thread(target=cansend, args=(client_socket,)).start()
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
        
#서버 접속 
HOST = '127.0.0.1'
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#서버 데이터 받기
threading.Thread(target=canreceive, args=(client_socket,)).start()

# 1번 충전기 GUI
#Tk 변수 선언
status_a1 = StringVar()
chargingwatt_a1 = StringVar()
totalwatt_a1 = StringVar()
chargingtime_a1 = StringVar()

#시작 버튼
def startbtn_a1():
    global go_send, startflag, stopflag, image1
    try_login()
    set_go_send()
    startflag = 100
    stopflag = 0
    image1 = tkinter.PhotoImage(file="charging.png" )
    label = tkinter.Label(frame1, image=image1, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)

    
#정지 버튼    
def stopbtn_a1():
    global go_send, startflag, stopflag, image1
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 100
    image1 = tkinter.PhotoImage(file="connect.png" )
    label = tkinter.Label(frame1, image=image1, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)
    
#화면 분류
frame1 = Frame(window, relief="solid", bd=2, bg='black')
frame1.pack(side="left", fill="both", expand=True)

#충전기 제어 버튼
btn_sersend = Button(frame1, text="1m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=sersend)
btn_sersend.place(x=10, y=20)

btn_sersend = Button(frame1, text="2m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=sersend2)
btn_sersend.place(x=60, y=20)

btn_sersend = Button(frame1, text="3m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=sersend3)
btn_sersend.place(x=110, y=20)

btn_start = Button(frame1, text="충전",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                   ,command=startbtn_a1)
btn_start.place(x=160, y=20)

btn_stop = Button(frame1, text="정지",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=stopbtn_a1)
btn_stop.place(x=210, y=20)
    
#충전 이미지
image1 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame1, image=image1, width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=100)

#충전기 상태 화면
lb_status_attr_a1 = Label(frame1, text="충전건 상태",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a1.place(x=5, y=270)
lb_status_value_a1 = Label(frame1, textvariable=status_a1,font="bold", bg="#1E1E2A", fg='white')
lb_status_value_a1.place(x=135, y=270, width=120, height=25)

#충전 전력량 화면
lb_chargingwatt_attr_a1 = Label(frame1, text="충전 전력량",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingwatt_attr_a1.place(x=5, y=300)
lb_chargingwatt_value_a1 = Label(frame1, textvariable=chargingwatt_a1,font="bold", bg="#1E1E2A", fg='white')
lb_chargingwatt_value_a1.place(x=135, y=300, width=120, height=25)

#충전 요금 화면
lb_chargingamount_attr_a1 = Label(frame1, text="충전 요금",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a1.place(x=5, y=330)
lb_chargingamount_value_a1 = Label(frame1,font="bold", bg="#1E1E2A", fg='white')
lb_chargingamount_value_a1.place(x=135, y=330, width=120, height=25)

#충전 시간 화면
lb_chargingtime_attr_a1 = Label(frame1, text="충전 시간",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a1.place(x=5, y=360)
lb_chargingtime_value_a1 = Label(frame1, textvariable=chargingtime_a1,font="bold", bg="#1E1E2A", fg='white')
lb_chargingtime_value_a1.place(x=135, y=360, width=120, height=25)

# 2번 충전기 GUI
#Tk 변수 선언
status_a2 = StringVar()
chargingwatt_a2 = StringVar()
totalwatt_a2 = StringVar()
chargingtime_a2 = StringVar()

#시작 버튼
def startbtn_a2():
    global go_send, startflag, stopflag, image2
    try_login()
    set_go_send()
    startflag = 110
    stopflag = 0
    image2 = tkinter.PhotoImage(file = "charging.png" )
    label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)
    
#정지 버튼    
def stopbtn_a2():
    global go_send, startflag, stopflag, image2
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 110
    image2 = tkinter.PhotoImage(file = "connect.png" )
    label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)
    
#화면 분류
frame2 = Frame(window, relief="solid", bd=2, bg='black')
frame2.pack(side="left", fill="both", expand=True)

#충전기 분류    
btn_title_a1 = Button(frame2, text="1m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=10, y=20)

btn_title_a1 = Button(frame2, text="2m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=60, y=20)

btn_title_a1 = Button(frame2, text="3m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=110, y=20)

btn_title_a1 = Button(frame2, text="충전",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=startbtn_a2)
btn_title_a1.place(x=160, y=20)

btn_title_a1 = Button(frame2, text="정지",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=stopbtn_a2)
btn_title_a1.place(x=210, y=20)

#충전 이미지
image2 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame2, image=image2, width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=100)

#충전기 상태 화면
lb_status_attr_a2 = Label(frame2, text="충전건 상태",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a2.place(x=5, y=270)
lb_status_value_a2 = Label(frame2, textvariable=status_a2,font="bold", bg="#1E1E2A", fg='white')
lb_status_value_a2.place(x=135, y=270, width=120, height=25)

#충전 전력량 화면
lb_chargingWatt_attr_a2 = Label(frame2, text="충전 전력량",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingWatt_attr_a2.place(x=5, y=300)
lb_chargingWatt_value_a2 = Label(frame2, textvariable=chargingwatt_a2,font="bold", bg="#1E1E2A", fg='white')
lb_chargingWatt_value_a2.place(x=135, y=300, width=120, height=25)

#충전 요금 화면
lb_chargingamount_attr_a2 = Label(frame2, text="충전 요금",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a2.place(x=5, y=330)
lb_chargingamount_value_a2 = Label(frame2,font="bold", bg="#1E1E2A", fg='white')
lb_chargingamount_value_a2.place(x=135, y=330, width=120, height=25)

#충전 시간 화면
lb_chargingtime_attr_a2 = Label(frame2, text="충전 시간",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a2.place(x=5, y=360)
lb_chargingtime_value_a2 = Label(frame2, textvariable=chargingtime_a2,font="bold", bg="#1E1E2A", fg='white')
lb_chargingtime_value_a2.place(x=135, y=360, width=120, height=25)

# 3번 충전기 GUI

#Tk 변수 선언
status_a3 = StringVar()
chargingwatt_a3 = StringVar()
totalwatt_a3 = StringVar()
chargingtime_a3 = StringVar()

#시작 버튼
def startbtn_a3():
    global go_send, startflag, stopflag, image3
    try_login()
    set_go_send()
    startflag = 120
    stopflag = 0
    image3 = tkinter.PhotoImage(file = "charging.png" )
    label = tkinter.Label(frame3, image=image3, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)
    
#정지 버튼    
def stopbtn_a3():
    global go_send, startflag, stopflag, image3
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 120
    image3 = tkinter.PhotoImage(file = "connect.png" )
    label = tkinter.Label(frame3, image=image3, width=240, height=150, bg="#1E1E2A")
    label.place(x=10, y=100)
    
#화면 분류
frame3 = Frame(window, relief="solid", bd=2, bg='black')
frame3.pack(side="left", fill="both", expand=True)

#충전기 분류    
btn_title_a1 = Button(frame3, text="1m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=10, y=20)

btn_title_a1 = Button(frame3, text="2m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=60, y=20)

btn_title_a1 = Button(frame3, text="3m",font="bold", width=2, height=2, bg="#1E1E2A", fg='white')
btn_title_a1.place(x=110, y=20)

btn_title_a1 = Button(frame3, text="충전",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=startbtn_a3)
btn_title_a1.place(x=160, y=20)

btn_title_a1 = Button(frame3, text="정지",font="bold", width=2, height=2, bg="#1E1E2A", fg='white'
                      ,command=stopbtn_a3)
btn_title_a1.place(x=210, y=20)

#충전 이미지
image3 = tkinter.PhotoImage(file = "connect.png" )
label = tkinter.Label(frame3, image=image3,width=240, height=150, bg="#1E1E2A")
label.place(x=10, y=100)

#충전기 상태 화면
lb_status_attr_a3 = Label(frame3, text="충전기 상태",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_status_attr_a3.place(x=5, y=270)
lb_status_value_a3 = Label(frame3, textvariable=status_a3,font="bold", bg="#1E1E2A", fg='white')
lb_status_value_a3.place(x=135, y=270, width=120, height=25)

#충전 전력량 화면
lb_chargingwatt_attr_a3 = Label(frame3, text="충전 전력량",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingwatt_attr_a3.place(x=5, y=300)
lb_chargingwatt_value_a3 = Label(frame3, textvariable=chargingwatt_a3,font="bold", bg="#1E1E2A", fg='white')
lb_chargingwatt_value_a3.place(x=135, y=300, width=120, height=25)

#충전 요금 화면
lb_chargingamount_attr_a3 = Label(frame3, text="충전 요금",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingamount_attr_a3.place(x=5, y=330)
lb_chargingamount_value_a3 = Label(frame3,font="bold", bg="#1E1E2A", fg='white')
lb_chargingamount_value_a3.place(x=135, y=330, width=120, height=25)

#충전 시간 화면
lb_chargingtime_attr_a3 = Label(frame3, text="충전 시간",font="bold", width=12, height=1, bg="#1E1E2A", fg='white')
lb_chargingtime_attr_a3.place(x=5, y=360)
lb_chargingtime_value_a3 = Label(frame3, textvariable=chargingtime_a3,font="bold", bg="#1E1E2A", fg='white')
lb_chargingtime_value_a3.place(x=135, y=360, width=120, height=25)

window.mainloop()
client_socket.close()
