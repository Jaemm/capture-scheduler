import serial
 
RS485 = serial.Serial(
    port='com3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
 
while True:
    x = RS485.readline()
    print(x)