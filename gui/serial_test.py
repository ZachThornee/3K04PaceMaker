import serial
import time
import struct

try:
    serial_con = serial.Serial(port="/dev/ttyACM0",
                               baudrate=115200,
                               timeout=1,
                               parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE,
                               bytesize=serial.EIGHTBITS,
                               )
except:
    serial_con = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)


def read():
    while True:
        response = serial_con.read(8)
        print(response)
        response = struct.unpack("q", response)
        print(response)


def write():
    while True:
        string = "True"
        result = serial_con.write(True)
        print(result)
        time.sleep(0.5)


read()
