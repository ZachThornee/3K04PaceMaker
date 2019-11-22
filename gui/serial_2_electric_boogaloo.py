import serial
import time
import struct

start_byte = 22
send_bool = 85
pace_mode = 1
lower_rate = 60
upper_rate = 0
max_sensor_rate = 0
fixed_av_delay = 0
atrial_amplitude = 3000
ventricular_amplitude = 0
atrial_pulse_width = 10
ventricular_pulse_width = 0
arp = 0
vrp = 0
activity_threshold = 0
reaction_time = 0
response_factor = 0
recovery_time = 0
rate_toggle = 0
empty = 0

send = struct.pack("4B13H2B",
                   start_byte,  # B1
                   send_bool,  # B2
                   pace_mode,  # B3
                   activity_threshold,  # B
                   lower_rate,  # H1
                   upper_rate,  # H2
                   max_sensor_rate,  # H3
                   fixed_av_delay,  # H4
                   atrial_amplitude,  # H5
                   ventricular_amplitude,  # H6
                   atrial_pulse_width,  # H7
                   ventricular_pulse_width,  # H8
                   arp,  # H9
                   vrp,  # H10
                   reaction_time,  # H11
                   response_factor,  # H12
                   recovery_time,  # H13
                   rate_toggle,  # B1
                   empty,  # B2
                   )
print(send)

with serial.Serial("/dev/ttyACM0", 115200) as ser_boy:
    print("entered serial")
    for i in range(5):
        result = ser_boy.write(send)
        print(result)
        time.sleep(1)
    input()
