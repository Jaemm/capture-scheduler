#import os, sys
import serial
import time

port = "COM3"
baud = 9600
ser = serial.Serial(port, baud, timeout = 1)

def run():
    Send_Recv = bytes(bytearray([0x01]))
    Charger_Number = bytes(bytearray([0x02]))
    #charger1 = 1, charger2 = 2, charger3 = 3
    
    Charger_Status = bytes(bytearray([0x03]))
    #disconnected = 0, connected = 1, charging = 2, error = 3
    
    Charger_Position = bytes(bytearray([0x04]))
    #0M = 0, 1M = 1, 2M =  2, 3M = 3
    
    Lock = bytes(bytearray([0x05]))
    #unlock = 0, lock = 1
    
    Data = bytes(bytearray([0x06]))
    Crc = bytes(bytearray([0x07]))
    CRC = bytes(bytearray([0x08]))

    ser.write(bytes(bytearray([0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08])))
    
    while True:
        line = ser.read(8)
        
        if len(line) == 0:
                break; 
            
        hex_list = ["{:x}".format(ord(c)) for c in line];
        print( ''.join(hex_list))
        
while True:
    run();