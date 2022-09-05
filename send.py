import time
import serial

data = serial.Serial('COM3', 115200, timeout=0.050)
count = 0
while 1:
    data_write = data.write('6'.encode())
    time.sleep(1)
    count += 1
