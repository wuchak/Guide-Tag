import serial
import os
from data_process import *
'''
for i in range(3):
    print(i)
'''

#cmd =[0xA5,0x5A, 0x00, 0x08, 0x04, 0x0C, 0x0D, 0x0A]
cmd = [0XA5,0X5A,0X00,0X0A,0X82,0X00,0X10,0X98,0X0D,0X0A]
while True:
    with serial.Serial(f'/dev/ttyUSB0', 115200, timeout=1) as ser:
        ser.write(cmd)
        raw = ser.read(1000)        # read up to ten bytes (timeout)
#        msg = handle_raw(raw.hex())
        print(raw.hex())
'''
import serial.tools.list_ports
myports = [list(p) for p in list(serial.tools.list_ports.comports())]
print(myports)
'''