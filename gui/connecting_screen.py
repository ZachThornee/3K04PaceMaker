import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import home_screen as HOME
import struct
import serial_connect
import threading


class con_screen(QMainWindow):

    def __init__(self, tables_dict):
        """
        Initialization method for connection screen

        :param tables_dict 2D_dictionary: contains all tables defined in main.py
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnecting.ui'), self)
        log.info("Waiting for device connection")
        self.ui.show()
        self.tables_dict = tables_dict
        self.serial = serial_connect.serial_reader("/dev/ttyACM0", 115200)
        self.table = self.tables_dict['patients_table']
        self.received_bytes = False
        t1 = threading.Thread(target=self.read_serial)
        t1.start()

    def read_serial(self):
        """
        Method to read serial port and look for unique id. Also check connectivity.

        """

        start_byte = 22
        send_bool = 34  # 85 is receive, 34 is echo
        echo_msg = [0] * 17
        echo_msg.insert(0, send_bool)
        echo_msg.insert(0, start_byte)

        log.info(echo_msg)

        value_sent = False
        while value_sent is False:
            value_sent = self.serial.send("4B13H2B", echo_msg)

        params_dict = self.serial.get_params_dict(32, "13H6B")

        self.ui.close()

        patient_rn = self.table.find_row_number(params_dict["pacemaker_id"], "pacemaker_id")

        # Call the main DCM screen
        HOME.home_screen(self.tables_dict, patient_rn, params_dict)
        self.received_bytes = True
