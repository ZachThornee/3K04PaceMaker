import serial
import time
import struct

with serial.Serial("/dev/ttyACM0", 115200) as ser_boy:
    mode = b'\x03'
    send = struct.pack("B", 22)
    send = bytes([22])
    send = b'\x16'
    for i in range(100):
        result = ser_boy.write(send)
        print(result)
        time.sleep(.1)
