from io import StringIO
import socket
from _thread import *
from sre_parse import State
import threading
from tkinter import *
import tkinter.ttk
from time import sleep
# from turtle import onclick
import os
# from tkinter import filedialog
# from tkinter import messagebox
# # from __future__ import print_function
# # import can
# import asyncio
# import logging

# try:
#     import websockets
# except ModuleNotFoundError:
#     print("This example relies on the 'websockets' package.")
#     print("Please install it by running: ")
#     print()
#     print(" $ pip install websockets")
#     import sys
#     sys.exit(1)


# from ocpp.v16 import call
# from ocpp.v16 import ChargePoint as cp
# from ocpp.v16.enums import RegistrationStatus
import requests
import json


def send(socket):
    global go_send
    global stop_send
    ##시작, 정지 버튼 작업중
    while True:
        if go_send:
            #
            message = '1'
            message_byte = message.encode('utf-8')
            socket.send(message_byte)
            #
            url = 'http://127.0.0.1:5000/boot'
            rev_data = requests.get(url).json()
            print(rev_data)
            #
            data = socket.recv(1024)
            decoded_data = data.decode('utf-8')
            splited_data = decoded_data.split(' : ')
            splited_data = splited_data[1].split(' ')
            if splited_data[0] == '0x100':
                if splited_data[2] == '0' :
                    statusOneText.set("disconnect")
                if splited_data[2] == '1' :
                    statusOneText.set("connect")
                if splited_data[2] == '2' :
                    statusOneText.set("charging")
                if splited_data[2] == '3' :
                    statusOneText.set("error")
                status = str(statusOneText)
            url = 'http://127.0.0.1:5000/boot'
            send_data = requests.post(url, json={'status': status})
            print(send_data.status_code)
            #
            go_send = False
        #elif stop_send:
            #message = '0'
            #message_byte = message.encode('utf-8')
            #socket.send(message_byte)
            #stop_send = False
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
            # print(f'splited : {splited_data}')
            if splited_data[0] == '0x100':
                
                energyOneText.set(str(int(splited_data[3], 16))+"W")
                voltOneText.set(str(int(splited_data[5]+splited_data[6], 16))+"W")
                ##status 정보
                if splited_data[2] == '0' :
                    statusOneText.set("disconnect")
                elif splited_data[2] == '1' :
                    statusOneText.set("connect")
                elif splited_data[2] == '2' :
                    statusOneText.set("charging")
                elif splited_data[2] == '3' :
                    statusOneText.set("error")
               
            if splited_data[0] == '0x110':
                secondTwoText.set(str(int(splited_data[1], 16)))
                energyTwoText.set(str(int(splited_data[3], 16)))
                voltTwoText.set(str(int(splited_data[6], 16)))
            if splited_data[0] == '0x120':
                secondThreeText.set(str(int(splited_data[1], 16)))
                energyThreeText.set(str(int(splited_data[3], 16)))
                voltThreeText.set(str(int(splited_data[6], 16)))
            ##펌웨어 버전 정보 받아오기
            if splited_data[0] == '0x101':
                year = (str(int(splited_data[8]+splited_data[7], 16)))
                month = (str(int(splited_data[6], 16)))
                day = (str(int(splited_data[5], 16)))
                firmwareText.set(year+"년"+month +"월"+ day + "일")
                secondOneText.set(str(int(splited_data[6], 16))+"초")
            if splited_data[0] == '0x200' :
                powerOneText.set(str(int(splited_data[3]+splited_data[4],16))+"W")              
        except ConnectionAbortedError as e:
            exit()

def login():
    # 서버의 ip주소 및 포트
    HOST = '192.168.0.67'
    PORT = 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=send, args=(client_socket,)).start()
    threading.Thread(target=receive, args=(client_socket,)).start()
    exit()

def try_login():
    global go_out
    start_new_thread(login, ())
    go_out = False
    
def try_logout():
    global go_out
    go_out = True

def set_go_send():
    global go_send
    go_send = True

def set_stop_send():
    global stop_send
    stop_send = True
    
# def ocpp_login():
#     logging.basicConfig(level=logging.INFO)
#     class ChargePoint(cp):
#         async def send_boot_notification(self):
#             request = call.BootNotificationPayload(
#                 charge_point_model="FH22",
#                 charge_point_vendor="first",
#                 Reason="Unknown",
#                 Rssi=1234,
#                 Entityid="oneM2M"
#             )

#             response = await self.call(request)

#             if response.status == RegistrationStatus.accepted:
#                 print("Connected to central system.")
#     async def main():
#         async with websockets.connect(
#             'ws://localhost:9090/CP_1',
#             subprotocols=['ocpp1.6']
#         ) as ws:

#             cp = ChargePoint('CP_1', ws)

#             await asyncio.gather(cp.start(), cp.send_boot_notification())

go_out, go_send, stop_send = False, False, False
window = Tk()
secondOneText = StringVar()
voltOneText = StringVar()
energyOneText = StringVar()
chargeOneText = StringVar()
powerOneText = StringVar()
firmwareText = StringVar()
powerOneText = StringVar()
statusOneText = StringVar()

secondTwoText = StringVar()
voltTwoText = StringVar()
energyTwoText = StringVar()
chargeTwoText = StringVar()

secondThreeText = StringVar()
voltThreeText = StringVar()
energyThreeText = StringVar()
chargeThreeText = StringVar()

window.title("완속 멀티충전기")
window.geometry("1280x720")
window.resizable(True,True)
#
frame1 = Frame(window, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)
frame2 = Frame(window, relief="solid", bd=2)
frame2.pack(side="left", fill="both", expand=True)
frame3 = Frame(window, relief="solid", bd=2)
frame3.pack(side="left", fill="both", expand=True)

# 1번 충전기
#progressbar
p_var1 = DoubleVar()
progressbar1 = tkinter.ttk.Progressbar(frame1, maximum=10000, length=240, variable=p_var1)
progressbar1.place(x=10, y=160, height=40)
#
def startbtn1():
    # ocpp_login()
    progressbar1.start()
    stopButton.config(state=NORMAL)
    try_login()
    set_go_send()
    
def stopbtn1():
    progressbar1.stop()
    startButton.config(state=NORMAL)
    set_stop_send()
    try_logout()
    
startButton = Button(frame1, text="충전", width=12, height=5, bg="lightblue", command=startbtn1)
startButton.place(x=5, y=50)
stopButton = Button(frame1, text="중단", width=12, height=5, bg="lightgray", command=stopbtn1)
stopButton.place(x=130, y=50)
#
lbl1 = Label(frame1, text="A01", width=10, height=2, bg="lightgray")
lbl1.pack()
status = Label(frame1, text="충전기 상태", width=15, height=1, bg="lightblue")
status.place(x=5, y=220)
status_value = Label(frame1, textvariable=statusOneText, bg="lightgray")
status_value.place(x=135, y=220, width=120, height=20)
lbl2 = Label(frame1, text="충전 시간", width=15, height=1, bg="lightblue")
lbl2.place(x=5, y=250)
seconds = Label(frame1, textvariable=secondOneText,text="초", bg="lightgray")
seconds.place(x=135, y=250, width=120, height=20)
lbl3 = Label(frame1, text="충전 전력", width=15, height=1, bg="lightblue")
lbl3.place(x=5, y=280)
entry3 = Label(frame1, textvariable=voltOneText, bg="lightgray")
entry3.place(x=135, y=280, width=120, height=20)
lbl4 = Label(frame1, text="누적 충전량", width=15, height=1, bg="lightblue")
lbl4.place(x=5, y=310)
entry4 = Label(frame1, textvariable=energyOneText, bg="lightgray")
entry4.place(x=135, y=310, width=120, height=20)
lbl5 = Label(frame1, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
entry5 = Label(frame1, text="292.9"+" 원/kWh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)
#
#lbl = Label(frame1, text="펌웨어 버전", width=15, height=1, bg="lightblue")
#lbl.place(x=5, y=370)
#entry = Label(frame1, bg="lightgray", textvariable=firmwareText)
#entry.place(x=135, y=370, width=120, height=20)
#
#lbl = Label(frame1, text="파워지령", width=15, height=1, bg="lightblue")
#lbl.place(x=5, y=400)
#entry = Label(frame1, bg="lightgray", textvariable=powerOneText)
#entry.place(x=135, y=400, width=120, height=20)

#관리자 페이지 새창 등록
# def firmwarebtn():
#     newwin = Tk()
#     newwin.title("관리자 페이지")
#     newwin.geometry("500x300")
#     lbl = Label(newwin, text="펌웨어 버전", width=15, height=1, bg="lightblue")
#     lbl.place(x=5, y=50)
#     entry = Label(newwin, bg="lightgray", textvariable=firmwareText)
#     entry.place(x=135, y=50, width=340, height=20)
    
#     def update():
#         newwin.file=filedialog.askopenfile(
#         initialdir='path',
#         title='select file',
#         filetypes=(('png files', '*.png'), 
# 		('all files', '*.*')))      
#         entry2.configure(text=":" + newwin.file.name)
        
#     btn = Button(newwin, text="펌웨어 업데이트", width=14, height=1, bg="lightblue", command=update)
#     btn.place(x=5, y=80)
#     entry2 = Label(newwin, bg="lightgray",text=" ")
#     entry2.place(x=135, y=80, width=340, height=20)
#     lbl3 = Label(newwin, text="고장 코드", width=15, height=1, bg="lightblue")
#     lbl3.place(x=5, y=110)
#     entry3 = Label(newwin, bg="lightgray")
#     entry3.place(x=135, y=110, width=340, height=20)
    
#     newwin.mainloop()
#       
#updatebtn = Button(frame1, text="관리자 페이지 ", width=14, height=1, bg="lightblue", command=firmwarebtn)
#updatebtn.place(x=5, y=370)
#





# 2번 충전기
#
def startbtn2():
    progressbar2.start(1)
    stopButton.config(state=NORMAL)
    
def stopbtn2():
    progressbar2.stop()
    
startButton = Button(frame2, text="충전", width=12, height=5,bg="lightblue", command=startbtn2)
startButton.place(x=5, y=50)
stopButton = Button(frame2, text="중단", width=12, height=5, bg="lightgray", command=stopbtn2)
stopButton.place(x=130, y=50)
#
p_var2 = DoubleVar()
progressbar2 = tkinter.ttk.Progressbar(frame2, maximum=10000, length=240, variable=p_var2)
progressbar2.place(x=10, y=160, height=70)
#
lbl1 = Label(frame2, text="A02", width=10, height=2, bg="lightgray")
lbl1.pack()
lbl2 = Label(frame2, text="충전 시간", width=15, height=1, bg="lightblue")
lbl2.place(x=5, y=250)
lbl3 = Label(frame2, text="충전 전력", width=15, height=1, bg="lightblue")
lbl3.place(x=5, y=280)
lbl4 = Label(frame2, text="누적 충전 에너지", width=15, height=1, bg="lightblue")
lbl4.place(x=5, y=310)
lbl5 = Label(frame2, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
#
seconds = Label(frame2, textvariable=secondTwoText, bg="lightgray")
seconds.place(x=135, y=250, width=120, height=20)
entry3 = Label(frame2, textvariable=voltTwoText, bg="lightgray")
entry3.place(x=135, y=280, width=120, height=20)
entry4 = Label(frame2, textvariable=energyTwoText, bg="lightgray")
entry4.place(x=135, y=310, width=120, height=20)
entry5 = Label(frame2, text="292.9"+"원/kwh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)

# 3번 충전기
#
def startbtn3():
    progressbar3.start(1)
    
def stopbtn3():
    progressbar3.stop()
    
startButton = Button(frame3, text="충전", width=12, height=5,bg="lightblue", command=startbtn3)
startButton.place(x=5, y=50)
stopButton = Button(frame3, text="중단", width=12, height=5, bg="lightgray", command=stopbtn3)
stopButton.place(x=130, y=50)
#
p_var3 = DoubleVar()
progressbar3 = tkinter.ttk.Progressbar(frame3, maximum=10000, length=240, variable=p_var3)
progressbar3.place(x=10, y=160, height=70)
#
lbl1 = Label(frame3, text="A03", width=10, height=2, bg="lightgray")
lbl1.pack()
lbl2 = Label(frame3, text="충전 시간", width=15, height=1, bg="lightblue")
lbl2.place(x=5, y=250)
lbl3 = Label(frame3, text="충전 전력", width=15, height=1, bg="lightblue")
lbl3.place(x=5, y=280)
lbl4 = Label(frame3, text="누적 충전 에너지", width=15, height=1, bg="lightblue")
lbl4.place(x=5, y=310)
lbl5 = Label(frame3, text="충전 요금", width=15, height=1, bg="lightblue")
lbl5.place(x=5, y=340)
#
seconds = Label(frame3, textvariable=secondThreeText, bg="lightgray")
seconds.place(x=135, y=250, width=120, height=20)
entry3 = Label(frame3, textvariable=voltThreeText, bg="lightgray")
entry3.place(x=135, y=280, width=120, height=20)
entry4 = Label(frame3, textvariable=energyThreeText, bg="lightgray")
entry4.place(x=135, y=310, width=120, height=20)
entry5 = Label(frame3, text="292.9"+"원/kwh", bg="lightgray")
entry5.place(x=135, y=340, width=120, height=20)

#
window.mainloop()

#
HOST = '127.0.0.1'
PORT = 9999
# socket 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # 서버로 부터 메세지 받기
    message = 'hello'
    # 메세지 전송
    client_socket.send(message.encode())
    data = client_socket.recv(1024)
    print('received from the server:', repr(data.decode()))
client_socket.close()