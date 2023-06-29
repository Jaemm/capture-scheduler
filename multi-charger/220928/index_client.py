import tkinter as tk
import tkinter as Tk
import tkinter.font
from tkinter import *

import datetime as dt
import time

import socket
from _thread import *
import threading

# import RPi.GPIO as GPIO
# import serial

class SampleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.switch_frame(StartPage)
        self.title('First C&D')
        self.geometry('1280x720')
        
    def switch_frame(self, frame_class):
        global status1, chargingwatt1, totalwatt1, chargingtime1
        global status2, chargingwatt2, totalwatt2, chargingtime2
        global status3, chargingwatt3, totalwatt3, chargingtime3      
        status1 = StringVar()
        chargingwatt1 = StringVar()
        totalwatt1 = StringVar()
        chargingtime1 = StringVar()
        status2 = StringVar()
        chargingwatt2 = StringVar()
        totalwatt2 = StringVar()
        chargingtime2 = StringVar()
        status3 = StringVar()
        chargingwatt3 = StringVar()
        totalwatt3 = StringVar()
        chargingtime3 = StringVar()
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.configure(bg='#004862')
        self._frame.place(width=1280, height=720)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        font2=tkinter.font.Font(family="맑은 고딕", size=12, weight='bold')
        image=tkinter.PhotoImage(file='C:\workspace\멀티충전기\image\electric-car.png')
        Label(text='안녕하세요!', font=font, bg='#004862', fg='white').place(
            x=350, y=50, width=600, height=50)
        Label(text='전기차 멀티 충전 시스템입니다.', font=font, bg='#004862', fg='white').place(
            x=350, y=120, width=600, height=50)
        Label(text='충전을 시작하시겠습니까?', font=font, bg='#004862', fg='white').place(
            x=350, y=190, width=600, height=50)
        Button(image=image, bg='#004862', fg='white', relief='flat', state='active', activebackground='#004862', font=font, 
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=290, width=420, height=420)
        Button.image=image
        date = dt.datetime.now()
        Label(text=f"{date:%Y-%m-%d(%A)}", font=font2, bg='#002A39', fg='white').place(
            x=950, y=590, width=250)
        Label(text=f"{date:%p-%H:%M:%S}", font=font2, bg='#002A39', fg='white').place(
            x=950, y=615, width=250)
        Label(text='전기차 멀티 충전기 / First C&D', font=font2, bg='#002A39', fg='white').place(
            x=950, y=635, width=250)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        font2=tkinter.font.Font(family="맑은 고딕", size=70, weight='bold')
        font3=tkinter.font.Font(family="맑은 고딕", size=25, weight='bold')
        Label(text='원하는 충전기 위치를 선택하세요.', font=font, bg='#004862', fg='white').place(
            x=300, y=100, width=750, height=50)
        Button(text='1', bg='#002A39', fg='#FFCA24', relief='flat' , font=font2, 
               command=lambda: master.switch_frame(PageTwo)).place(
            x=150, y=200, width=200, height=200)
        Label(text='사용 여부', bg='#6F878F', fg='white', font=font3).place(
            x=90, y=450, width=160, height=60)
        Label(textvariable=status1, bg='#002A39', fg='white', font=font3).place(
            x=250, y=450, width=160, height=60)
        Label(text='사용 시간', bg='#6F878F', fg='white', font=font3).place(
            x=90, y=520, width=160, height=60)
        Label(textvariable=chargingtime1, bg='#002A39', fg='white', font=font3).place(
            x=250, y=520, width=160, height=60)
        
        Button(text='2', bg='#002A39', fg='#FFCA24', relief='flat', font=font2,
               command=lambda: master.switch_frame(PageThree)).place(
            x=550, y=200, width=200, height=200)
        Label(text='사용 여부', bg='#6F878F', fg='white', font=font3).place(
            x=490, y=450, width=160, height=60)
        Label(textvariable=status2,bg='#002A39', fg='white', font=font3).place(
            x=650, y=450, width=160, height=60)
        Label(text='사용 시간', bg='#6F878F', fg='white', font=font3).place(
            x=490, y=520, width=160, height=60)
        Label(textvariable=chargingtime2, bg='#002A39', fg='white', font=font3).place(
            x=650, y=520, width=160, height=60)
        
        Button(text='3', bg='#002A39', fg='#FFCA24', relief='flat' , font=font2,
               command=lambda: master.switch_frame(PageFour)).place(
            x=950, y=200, width=200, height=200)
        Label(text='사용 여부', bg='#6F878F', fg='white', font=font3).place(
            x=890, y=450, width=160, height=60)
        Label(textvariable=status3, bg='#002A39', fg='white', font=font3).place(
            x=1050, y=450, width=160, height=60)
        Label(text='사용 시간', bg='#6F878F', fg='white', font=font3).place(
            x=890, y=520, width=160, height=60)
        Label(textvariable=chargingtime3, bg='#002A39', fg='white', font=font3).place(
            x=1050, y=520, width=160, height=60)
        Button(text='이전', bg='#6F878F', fg='white', relief='flat' , font=font,
               command=lambda: master.switch_frame(StartPage)).place(
            x=450, y=610, width=400, height=100)
        
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        image=tkinter.PhotoImage(file='C:\workspace\멀티충전기\image\card-tagging.png')
        Label(text='회원정보가 등록된 RFID카드를 태그하세요.', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=100)
        Button(image=image, bg='#004862', relief='flat',
                command=lambda: master.switch_frame(PageTwo_1), state='active', activebackground='#004862').place(
            x=450, y=200, width=400, height=400)
        Button.image=image
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=610, width=400, height=100)
        # try:
        #     rfid()
        # finally:
        #     lambda: master.switch_frame(PageTwo_1)
               
class PageTwo_1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        font2=tkinter.font.Font(family="맑은 고딕", size=70, weight='bold')
        Label(text='커넥터 위치에 맞게 케이블을 조절하세요.', font=font, bg='#004862', fg='white' ).place(
            x=250, y=100, width=800, height=100)
        Button(text='1m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend1).place(
            x=100, y=200, width=200, height=200)
        Button(text='2m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend2).place(
            x=400, y=200, width=200, height=200)
        Button(text='3m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend3).place(
            x=700, y=200, width=200, height=200)
        Button(text='0m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend0).place(
            x=1000, y=200, width=200, height=200)
        Button(text='다음', bg='#002A39', fg='#FFCA24', relief='flat', font=font,
               command=lambda: master.switch_frame(PageTwo_2)).place(
            x=450, y=500, width=400, height=100)
        Button(text='이전', bg='#6F878F', fg='white', relief='flat', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=450, y=610, width=400, height=100)
                
class PageTwo_2(tk.Frame):            
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='1번 충전기', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=50)
        Label(text='충전기 상세내역', font=font, bg='#004862', fg='white').place(
            x=250, y=200, width=800, height=50)
        Label(text='충전건 상태', bg='#6F878F', fg='white', font=font).place(
            x=100, y=300, width=250, height=70)
        Label(textvariable=status1, bg='#002A39', fg='white', font=font).place(
            x=350, y=300, width=250, height=70)
        Label(text='충전 전력량', bg='#6F878F', fg='white', font=font).place(
            x=100, y=400, width=250, height=70)
        Label(textvariable=totalwatt1, bg='#002A39', fg='white', font=font).place(
            x=350, y=400, width=250, height=70)
        Label(text='충전 시간', bg='#6F878F', fg='white', font=font).place(
            x=700, y=300, width=250, height=70)
        Label(textvariable=chargingtime1, bg='#002A39', fg='white', font=font).place(
            x=950, y=300, width=250, height=70)
        Label(text='충전 요금', bg='#6F878F', fg='white', font=font).place(
            x=700, y=400, width=250, height=70)
        Label( bg='#002A39', fg='white', font=font).place(
            x=950, y=400, width=250, height=70)
        Button(text='충전 시작', bg='#002A39', fg='#FFCA24', font=font, command=startbtn1).place(
            x=450, y=500, width=190, height=100)
        Button(text='충전 중지', bg='#002A39', fg='#FFCA24', font=font, command=stopbtn1).place(
            x=660, y=500, width=190, height=100)            
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageTwo_1)).place(
            x=450, y=610, width=400, height=100)

class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        image=tkinter.PhotoImage(file='card-tagging.png')
        Label(text='회원정보가 등록된 RFID카드를 태그하세요.', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=100)
        Button(image=image, bg='#004862', relief='flat',
                command=lambda: master.switch_frame(PageThree_1), state='active', activebackground='#004862').place(
            x=450, y=200, width=400, height=400)
        Button.image=image
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=610, width=400, height=100)
        rfid()
               
class PageThree_1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        font2=tkinter.font.Font(family="맑은 고딕", size=70, weight='bold')
        Label(text='커넥터 위치에 맞게 케이블을 조절하세요.', font=font, bg='#004862', fg='white' ).place(
            x=250, y=100, width=800, height=100)
        Button(text='1m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend1).place(
            x=100, y=200, width=200, height=200)
        Button(text='2m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend2).place(
            x=400, y=200, width=200, height=200)
        Button(text='3m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend3).place(
            x=700, y=200, width=200, height=200)
        Button(text='0m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend0).place(
            x=1000, y=200, width=200, height=200)
        Button(text='다음', bg='#002A39', fg='#FFCA24', relief='flat', font=font,
               command=lambda: master.switch_frame(PageThree_2)).place(
            x=450, y=500, width=400, height=100)
        Button(text='이전', bg='#6F878F', fg='white', relief='flat', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=450, y=610, width=400, height=100)
    
class PageThree_2(tk.Frame):            
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='2번 충전기', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=50)
        Label(text='충전기 상세내역', font=font, bg='#004862', fg='white').place(
            x=250, y=200, width=800, height=50)
        Label(text='충전건 상태', bg='#6F878F', fg='white', font=font).place(
            x=100, y=300, width=250, height=70)
        Label(textvariable=status2, bg='#002A39', fg='white', font=font).place(
            x=350, y=300, width=250, height=70)
        Label(text='충전 전력량', bg='#6F878F', fg='white', font=font).place(
            x=100, y=400, width=250, height=70)
        Label(textvariable=totalwatt2, bg='#002A39', fg='white', font=font).place(
            x=350, y=400, width=250, height=70)
        Label(text='충전 시간', bg='#6F878F', fg='white', font=font).place(
            x=700, y=300, width=250, height=70)
        Label(textvariable=chargingtime2, bg='#002A39', fg='white', font=font).place(
            x=950, y=300, width=250, height=70)
        Label(text='충전 요금', bg='#6F878F', fg='white', font=font).place(
            x=700, y=400, width=250, height=70)
        Label(bg='#002A39', fg='white', font=font).place(
            x=950, y=400, width=250, height=70)
        Button(text='충전 시작', bg='#002A39', fg='#FFCA24', font=font, command=startbtn2).place(
            x=450, y=500, width=190, height=100)
        Button(text='충전 중지', bg='#002A39', fg='#FFCA24', font=font, command=stopbtn2).place(
            x=660, y=500, width=190, height=100)            
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageThree_1)).place(
            x=450, y=610, width=400, height=100)
      
class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        image=tkinter.PhotoImage(file='card-tagging.png')
        Label(text='회원정보가 등록된 RFID카드를 태그하세요.', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=100)
        Button(image=image, bg='#004862', relief='flat',
                command=lambda: master.switch_frame(PageFour_1), state='active', activebackground='#004862').place(
            x=450, y=200, width=400, height=400)
        Button.image=image
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageOne)).place(
            x=450, y=610, width=400, height=100)
        rfid()
               
class PageFour_1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        font2=tkinter.font.Font(family="맑은 고딕", size=70, weight='bold')
        Label(text='커넥터 위치에 맞게 케이블을 조절하세요.', font=font, bg='#004862', fg='white' ).place(
            x=250, y=100, width=800, height=100)
        Button(text='1m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend1).place(
            x=100, y=200, width=200, height=200)
        Button(text='2m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend2).place(
            x=400, y=200, width=200, height=200)
        Button(text='3m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend3).place(
            x=700, y=200, width=200, height=200)
        Button(text='0m', bg='#002A39', fg='#FFCA24', relief='flat', font=font2, command=sersend0).place(
            x=1000, y=200, width=200, height=200)
        Button(text='다음', bg='#002A39', fg='#FFCA24', relief='flat', font=font,
               command=lambda: master.switch_frame(PageFour_2)).place(
            x=450, y=500, width=400, height=100)
        Button(text='이전', bg='#6F878F', fg='white', relief='flat', font=font,
               command=lambda: master.switch_frame(PageTwo)).place(
            x=450, y=610, width=400, height=100)
           
class PageFour_2(tk.Frame):            
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        font=tkinter.font.Font(family="맑은 고딕", size=30, weight='bold')
        Label(text='3번 충전기', font=font, bg='#004862', fg='white').place(
            x=250, y=100, width=800, height=50)
        Label(text='충전기 상세내역', font=font, bg='#004862', fg='white').place(
            x=250, y=200, width=800, height=50)
        Label(text='충전건 상태', bg='#6F878F', fg='white', font=font).place(
            x=100, y=300, width=250, height=70)
        Label(textvariable=status3, bg='#002A39', fg='white', font=font).place(
            x=350, y=300, width=250, height=70)
        Label(text='충전 전력량', bg='#6F878F', fg='white', font=font).place(
            x=100, y=400, width=250, height=70)
        Label(textvariable=totalwatt3, bg='#002A39', fg='white', font=font).place(
            x=350, y=400, width=250, height=70)
        Label(text='충전 시간', bg='#6F878F', fg='white', font=font).place(
            x=700, y=300, width=250, height=70)
        Label(textvariable=chargingtime3, bg='#002A39', fg='white', font=font).place(
            x=950, y=300, width=250, height=70)
        Label(text='충전 요금', bg='#6F878F', fg='white', font=font).place(
            x=700, y=400, width=250, height=70)
        Label(bg='#002A39', fg='white', font=font).place(
            x=950, y=400, width=250, height=70)
        Button(text='충전 시작', bg='#002A39', fg='#FFCA24', font=font, command=startbtn3).place(
            x=450, y=500, width=190, height=100)
        Button(text='충전 중지', bg='#002A39', fg='#FFCA24', font=font, command=stopbtn3).place(
            x=660, y=500, width=190, height=100)            
        Button(text='이전', bg='#6F878F', fg='white', font=font,
               command=lambda: master.switch_frame(PageFour_1)).place(
            x=450, y=610, width=400, height=100)
               
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

def recv(socket):
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
                    status1.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status1.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status1.set("충전중")
                elif splited_data[2] == '3' :
                    status1.set("에러")
                #충전 전력량 (시작~종료시까지)
                chargingwatt1.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
            if splited_data[0] == '0x101':
                #충전 시간
                chargingtime1.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")
            #2번 충전기 CAN 데이터 분석
            if splited_data[0] == '0x110':
                if splited_data[2] == '0' :
                    status2.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status2.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status2.set("충전중")
                elif splited_data[2] == '3' :
                    status2.set("에러")
                #충전 전력량 (시작~종료시까지)
                chargingwatt2.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
            if splited_data[0] == '0x111':
                #충전 시간
                chargingtime2.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")           
            #3번 충전기 CAN 데이터 분석
            if splited_data[0] == '0x120':
                #충전기 상태
                if splited_data[2] == '0' :
                    status3.set("충전건 해제")
                elif splited_data[2] == '1' :
                    status3.set("충전건 연결")
                elif splited_data[2] == '2' :
                    status3.set("충전중")
                elif splited_data[2] == '3' :
                    status3.set("에러")
                #충전 전력량 (시작~종료시까지)
                chargingwatt3.set(str(int(splited_data[6]+splited_data[5], 16))+"W")
            if splited_data[0] == '0x121':
                #충전 시간
                chargingtime3.set(str(int(splited_data[8]+splited_data[7]+splited_data[6], 16))+"초")                
        except ConnectionAbortedError as e:
            exit()

def login():
    # threading.Thread(target=send, args=(client_socket,)).start()
    exit()

def try_login():
    global go_out
    start_new_thread(login, ())
    go_out = False  

def set_go_send():
    global go_send
    go_send = True

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('127.0.0.1', 9000))
# threading.Thread(target=recv, args=(client_socket,)).start()

def sersend1():
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
    
def sersend0():
    if status1 == "충전건 해제":
        ser  = serial.Serial("/dev/serial0",9600)
        ser.write(bytes(bytearray([2,1,48,48,0,0,0,0])))
        ser.close()

def rfid():
    reader = SimpleMFRC522()
    try:
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        tk.messagebox.showinfo('회원 정보 확인','회원정보가 확인되었습니다.')
        GPIO.cleanup()
        startbtn1()

def startbtn1():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 100
    stopflag = 0
      
def stopbtn1():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 100
    
def startbtn2():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 110
    stopflag = 0
   
def stopbtn2():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 110
    
def startbtn3():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 120
    stopflag = 0
 
def stopbtn3():
    global go_send, startflag, stopflag
    try_login()
    set_go_send()
    startflag = 0
    stopflag = 120
               
if __name__ == "__main__": 
    app = SampleApp()
    app.mainloop()
    client_socket.close() 