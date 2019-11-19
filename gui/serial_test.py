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
    try:
        serial_con = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    except:
        pass


def read():
    while True:
        response = serial_con.read(8)
        print(response)
        response = struct.unpack("q", response)
        print(response)


def write(byte_array):
    while True:
        print(byte_array)
        byte_array = bytes(array)
        print(byte_array)
        result = serial_con.write(byte_array)
        print(result)
        time.sleep(0.5)

pace_mode = 4
lower = 0
upper = 100
sensor_rate = 100
fixed_av_delay = 100
dynamic_av_delay = 100
sensed_av_delay_offset = 100
Atrial_amplitude = 100
ventricular_amplitude = 100
atrial_pulse_width = 100
ventricular_pulse_width = 100
atrial_sensitivity = 100
ventricular_sensitivty = 100
vrp = 100
arp = 299
pvarp = 300
pvarp_extension = 100
hysteresis = 100
rate_smoothing = 100
atr_duration = 100
atr_fallback_mode = 100
atr_fallback_time = 100
activity_threshold = 100
reaction_time = 100
response_factor = 100
recovery_time = 100
rate_toggle = 1

array = []
array.append(pace_mode)
# array.append(lower)
# array.append(upper)
# array.append(sensor_rate)
# array.append(fixed_av_delay)
# array.append(dynamic_av_delay)
# array.append(sensed_av_delay_offset)
# array.append(Atrial_amplitude)
# array.append(ventricular_amplitude)
# array.append(atrial_pulse_width)
# array.append(ventricular_pulse_width)
# array.append(atrial_sensitivity)
# array.append(ventricular_sensitivty)
# array.append(vrp)
# array.append(arp)
# array.append(pvarp)
# array.append(pvarp_extension)
# array.append(hysteresis)
# array.append(rate_smoothing)
# array.append(atr_duration)
# array.append(atr_fallback_mode)
# array.append(atr_fallback_time)
# array.append(activity_threshold)
# array.append(reaction_time)
# array.append(response_factor)
# array.append(recovery_time)
# array.append(rate_toggle)

write(array[0])
# print(int.from_bytes(string, "big"))
