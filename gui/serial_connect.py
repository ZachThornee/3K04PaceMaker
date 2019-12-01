import serial
import struct
import logging as log
import threading
import time


class serial_reader:

    def __init__(self, port, baud):
        """
        serial reader class constructor

        :param port string: A string for which port to open
        :param baud int: Baud rate to use to read serial
        """
        self.serial = None
        self.baud = baud
        self.prev_msg = None
        self.port_list = ["/dev/ttyACM0", "/dev/ttyACM1"]
        self.port_list.insert(0, port)  # Try passed port first
        self.t1 = threading.Thread(target=self.connect)
        self.t1.start()

    def connect(self):
        """
        Method to connnect to a new serial device

        """
        while self.serial is None:
            for port in self.port_list:  # Try all our ports
                try:
                    tmp_serial = serial.Serial(port, self.baud, timeout=0.1)
                    time.sleep(1)
                    self.serial = tmp_serial
                except FileNotFoundError:
                    pass
                except serial.serialutil.SerialException:
                    pass

        log.info("Serial connnected")

    def send(self, send_format, params):
        """
        Method to send a list of params over serial

        :param send_format string: A struct pack string used to format the pack
        :param params list: List of parameters to send
        """

        if self.serial is None:
            return False

        # *list unpacks the list into seperate args
        msg = struct.pack(send_format, *params)  # Pack into string
        self.prev_msg = msg  # Set previous message to current msg
        log.debug("Just before message send")
        try:
            self.serial.write(msg)  # Write the messsage
            log.info("Serial message sent")
            return True
        except serial.serialutil.SerialException:
            log.error("No device connnected")
            raise SystemError


    def get_params_dict(self, byte_len, receive_format):
        """
        Method to a dictionary of params

        :param byte_len int: Length of bytes to read
        :param receive_format string: Struct.unpack defining byte array
        """

        if self.serial is None:
            return False
        log.info("Receiving serial")

        start_time = time.time()
        response = None
        while response is None:
            # If the buffer has the right length of bytes to read
            if self.serial.in_waiting == byte_len:
                response = self.serial.read(byte_len)
                log.info("Serial message received")
                break
            # Every 0.5s resend the previous message
            if time.time() - start_time > 0.5:
                self.serial.write(self.prev_msg)
                log.info("Resending previous message")
                start_time = time.time()

        # Get all the params as a list
        result = struct.unpack(receive_format, response)
        log.debug(result)
        log.debug(len(result))

        # Make the params dict
        params_dict = {"lower_rate": int(result[0]),
                       "vent_pulse_width": int(result[1]),
                       "vent_pulse_amp": int(result[2]),
                       "vrp": int(result[3]),
                       "arp": int(result[4]),
                       "fixed_av_delay": int(result[5]),
                       "atr_pulse_width": int(result[6]),
                       "atr_pulse_amp": int(result[7]),
                       "upper_rate": int(result[8]),
                       "reaction_time": int(result[9]),
                       "response_factor": int(result[10]),
                       "recovery_time": int(result[11]),
                       "msr": int(result[12]),
                       "pace_mode": int(result[13]),
                       "rate_toggle": int(result[14]),
                       "activity_thres": int(result[15]),
                       "vent_detect": int(result[16]),
                       "atr_detect": int(result[17]),
                       "patient_id": int(result[18])
                       }

        # Change the mode based on values from pacemaker
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

        # Set the new pacemode
        params_dict["pace_mode"] = mode_dict[params_dict["pace_mode"]]
        log.debug(params_dict)

        return params_dict
