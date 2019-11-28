import serial
import struct
import logging as log
import threading
import time


class serial_reader:

    def __init__(self, port, baud):
        self.serial = None
        self.port = port
        self.baud = baud
        self.prev_msg = None
        self.t1 = threading.Thread(target=self.connect)
        self.t1.start()

    def connect(self):
        while self.serial is None:
            try:
                tmp_serial = serial.Serial(self.port, self.baud, timeout=0.1)
                time.sleep(1)
                self.serial = tmp_serial

            except FileNotFoundError:
                pass
            except serial.serialutil.SerialException:
                pass
        log.info("Serial connnected")

    def send(self, send_format, params):

        if self.serial is None:
            return False

        msg = struct.pack(send_format, *params)
        self.prev_msg = msg
        self.serial.write(msg)
        log.info("Serial message sent")

    def get_params_dict(self, byte_len, receive_format):

        if self.serial is None:
            return False
        log.info("Receiving serial")

        start_time = time.time()
        response = None
        while response is None:
            if self.serial.in_waiting == byte_len:
                response = self.serial.read(byte_len)
                log.info("Serial message received")
                break

            if time.time() - start_time > 0.5:
                self.serial.write(self.prev_msg)
                log.info("Resending previous message")
                start_time = time.time()

        result = struct.unpack(receive_format, response)


        params_dict = {"lower_rate": int(result[0]),
                       "vent_pulse_width": int(result[1]),
                       "vent_pulse_amp": int(result[2]),
                       "vrp": int(result[3]),
                       "arp": int(result[4]),
                       "fixed_av_delay": int(result[5]),
                       "atr_pulse_width": int(result[6]),
                       "atr_pulse_amp": int(result[7]),
                       "upper_rate_limit": int(result[8]),
                       "reaction_time": int(result[9]),
                       "response_factor": int(result[10]),
                       "recovery_time": int(result[11]),
                       "msr": int(result[12]),
                       "pace_mode": int(result[13]),
                       "rate_toggle": int(result[14]),
                       "activity_thres": int(result[14]),
                       "vent_detect": int(result[15]),
                       "atr_detect": int(result[16]),
                       "patient_id": int(result[17])
                       }

        if params_dict["rate_toggle"] == 1:
            mode_dict = {1: "AOOR",
                         2: "VOOR",
                         3: "AAIR",
                         4: "VVIR",
                         5: "DOOR",
                         }
        else:
            mode_dict = {1: "AOO",
                         2: "VOO",
                         3: "AAI",
                         4: "VVI",
                         5: "DOO",
                         }

        params_dict["pace_mode"] = mode_dict[params_dict["pace_mode"]]

        return params_dict


if __name__ == "__main__":

    start_byte = 22
    send_bool = 34  # 85 is receive, 34 is echo
    echo_msg = [0] * 17
    echo_msg.insert(0, send_bool)
    echo_msg.insert(0, start_byte)

    SERIAL = serial_reader("/dev/ttyACM0", 115200)
    time.sleep(1)
    SERIAL.send("4B13H2B", echo_msg)
    print(SERIAL.get_params_dict(32, "13H6B"))
