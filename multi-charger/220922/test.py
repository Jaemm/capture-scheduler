import tkinter as tk
import tkinter as Tk
import tkinter.font
from tkinter import Place, Tk, messagebox
from tkinter import *

import time
import datetime as dt

import threading
from _thread import *

import socket
import serial

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title('First C&D')
        self.geometry('1280x720')
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect(('127.0.0.1', 9000))
        # threading.Thread(target=PageTwo_1_1.canreceive, args=(self.client_socket,)).start()
        # self.client_socket.close() 


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(width=1280, height=720)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='안녕하세요!', font=font).place(
            x=200, y=110, width=900, height=100)
        Label(text='전기차 멀티 충전 시스템입니다.', font=font).place(
            x=200, y=220, width=900, height=100)
        Label(text='충전을 시작하시겠습니까?', font=font).place(
            x=300, y=320, width=700, height=100)
        Button(text='시작', bg='#1E1E2A', fg='white', font=font, 
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=460, width=400, height=200)
        date = dt.datetime.now()
        Label(text=f"{date:%Y-%m-%d(%A)}", bg='gray', fg='white').place(
            x=1000, y=50, width=200)
        Label(text=f"{date:%p-%H:%M:%S}", bg='gray', fg='white').place(
            x=1000, y=70, width=200)
        Label(text='전기차 멀티 충전기 / First C&D', bg='gray', fg='white').place(
            x=1000, y=90, width=200)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='충전을 원하는 충전기 위치를 선택하세요.', font=font).place(
            x=300, y=100, width=750, height=100)
        Button(text='1번 충전기', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=250, y=300, width=200, height=100)
        Label(text='사용 여부', bg='gray', fg='white').place(
            x=250, y=450, width=200, height=40)
        Label(text='사용 시간', bg='gray', fg='white').place(
            x=250, y=500, width=200, height=40)
        Button(text='2번 충전기', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=550, y=300, width=200, height=100)
        Label(text='사용 여부', bg='gray', fg='white').place(
            x=550, y=450, width=200, height=40)
        Label(text='사용 시간', bg='gray', fg='white').place(
            x=550, y=500, width=200, height=40)
        Button(text='3번 충전기', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=850, y=300, width=200, height=100)
        Label(text='사용 여부', bg='gray', fg='white').place(
            x=850, y=450, width=200, height=40)
        Label(text='사용 시간', bg='gray', fg='white').place(
            x=850, y=500, width=200, height=40)
        Button(text='이전', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(StartPage)).place(
            x=450, y=610, width=400, height=100)
        

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='회원정보가 등록된 RFID카드를 태그하세요.', font=font).place(
            x=250, y=100, width=800, height=100)
        Button(text='다음', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo_1)).place(
            x=450, y=500, width=400, height=100)
        Button(text='이전', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=610, width=400, height=100)
               
class PageTwo_1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='커넥터 위치에 맞게 케이블을 조절하세요.', font=font).place(
            x=250, y=100, width=800, height=100)
        Button(text='1m', bg='#1E1E2A', fg='white', font=font).place(
            x=300, y=300, width=100, height=100)
        Button(text='2m', bg='#1E1E2A', fg='white', font=font).place(
            x=500, y=300, width=100, height=100)
        Button(text='3m', bg='#1E1E2A', fg='white', font=font).place(
            x=700, y=300, width=100, height=100)
        Button(text='0m', bg='#1E1E2A', fg='white', font=font).place(
            x=900, y=300, width=100, height=100)
        Button(text='다음', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo_1_1)).place(
            x=450, y=500, width=400, height=100)
        Button(text='이전', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=450, y=610, width=400, height=100)
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
        if status == "충전건 해제":
            ser  = serial.Serial("/dev/serial0",9600)
            ser.write(bytes(bytearray([2,1,48,48,0,0,0,0])))
            ser.close()
        # else:
        #     errorApp()
                
class PageTwo_1_1(tk.Frame):            
    def __init__(self, master):
        tk.Frame.__init__(self, master)      
          
        global status, chargingwatt, chargingtime
        
        status = StringVar()
        chargingwatt= StringVar()
        totalwatt= StringVar()
        chargingtime = StringVar()

        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='1번 충전기', font=font).place(
            x=250, y=100, width=800, height=50)
        Label(text='충전 상세 내역', font=font).place(
            x=250, y=200, width=800, height=50)
        Label(text='충전건 상태', bg='gray', fg='white', font=font).place(
            x=100, y=300, width=250, height=70)
        Label(textvariable=status, bg='gray', fg='white', font=font).place(
            x=360, y=300, width=250, height=70)
        Label(text='충전 전력량', bg='gray', fg='white', font=font).place(
            x=100, y=400, width=250, height=70)
        Label(textvariable=chargingwatt, bg='gray', fg='white', font=font).place(
            x=360, y=400, width=250, height=70)
        Label(text='충전 시간', bg='gray', fg='white', font=font).place(
            x=700, y=300, width=250, height=70)
        Label(textvariable=chargingtime, bg='gray', fg='white', font=font).place(
            x=960, y=300, width=250, height=70)
        Label(text='충전 요금', bg='gray', fg='white', font=font).place(
            x=700, y=400, width=250, height=70)
        Label(textvariable=totalwatt, bg='gray', fg='white', font=font).place(
            x=960, y=400, width=250, height=70)
        
        Button(text='충전 시작', bg='#1E1E2A', fg='white', font=font,
               command=PageTwo_1_1.startbtn).place(
            x=450, y=500, width=190, height=100)
        Button(text='충전 중지', bg='#1E1E2A', fg='white', font=font,
               command=PageTwo_1_1.stopbtn).place(
            x=660, y=500, width=190, height=100)            
        Button(text='처음으로', bg='#1E1E2A', fg='white', font=font,
               command=lambda: master.switch_frame(StartPage)).place(
            x=450, y=610, width=400, height=100)
               
    def canreceive(socket):
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
            except ConnectionAbortedError as e:
                exit()
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
    def startbtn():
        global go_send, startflag, stopflag
        PageTwo_1_1.try_login()
        PageTwo_1_1.set_go_send()
        startflag = 100
        stopflag = 0
    def stopbtn():
        global go_send, startflag, stopflag
        PageTwo_1_1.try_login()
        PageTwo_1_1.set_go_send()
        startflag = 0
        stopflag = 100 
    def login():
        threading.Thread(target=PageTwo_1_1.cansend, args=(SampleApp.__init__,)).start()
        exit()
    def try_login():
        global go_out
        start_new_thread(PageTwo_1_1.login, ())
        go_out = False  
    def set_go_send():
        global go_send
        go_send = True
               
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()