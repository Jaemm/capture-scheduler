# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import string
import binascii
#if use half-auto, EN_485 = LOW is Receiver, EN_485 = HIGH is Send
MODE = 0 #mode = 0 is full-guto, mode = 1 is half-auto
if MODE == 1:
    EN_485 =  4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN_485,GPIO.OUT)
    GPIO.output(EN_485,GPIO.HIGH)

ser = serial.Serial("/dev/ttyS0",9600,timeout=1) 

print("You can always send hex, press Ctrl + C to exit")
while 1:
    hexInput = bytes.fromhex(input([0,0,0,0,0,0,0,0]))
    ser.write(hexInput)

ser.flush()