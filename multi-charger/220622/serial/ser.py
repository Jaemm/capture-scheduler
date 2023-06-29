import time
import serial
from time import sleep
import random
import string
 
send = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
 
 
while True:
    letters = string.ascii_letters
    digits = string.digits
    data = ''.join(random.choice(letters) + random.choice(digits) for i in range(20))
    data = (data +"\n\r")
    send.write(data)
    print(data)
    time.sleep(0.2)