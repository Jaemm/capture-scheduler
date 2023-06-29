# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time
import binascii
#if use half-auto, EN_485 = LOW is Receiver, EN_485 = HIGH is Send
MODE = 0 #mode = 0 is full-guto, mode = 1 is half-auto
if MODE == 1:
    EN_485 =  4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN_485,GPIO.OUT)
    GPIO.output(EN_485,GPIO.HIGH)

ser = serial.Serial("/dev/ttyS0",115200,timeout=0.01) #receive data once every 0.01S 

ser.flushInput()

data = ""
print("You can always receive data, press Ctrl + C to exit")
while 1: 
    while ser.inWaiting() > 0:
        data = ser.readline()
    if data != "":
        print(str(binascii.b2a_hex(data))[2:-1])
        data = ""