import logging as log

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow

import home_screen as HOME
import serial_connect
import time


class con_screen(QMainWindow):

    thread_received = QtCore.pyqtSignal(object)

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
        self.thread_received.connect(self.connected)
        self.reader_thread = read_serial(self.table, self.serial, self.thread_received, True)
        self.reader_thread.start()

    def connected(self, params_dict):
        self.ui.close()

        # Call the main DCM screen
        HOME.home_screen(self.tables_dict, params_dict, self.serial)


class read_serial(QtCore.QThread):

    def __init__(self, table, serial, call_thread, echo_bool):
        QtCore.QThread.__init__(self)
        self.table = table
        self.serial = serial
        self.call_thread = call_thread
        self.echo_bool = echo_bool

    def run(self):
        start_byte = 22
        if self.echo_bool:
            send_val = 34  # Echo params
        else:
            send_val = 85  # Send params

        echo_msg = [0] * 17
        echo_msg.insert(0, send_val)
        echo_msg.insert(0, start_byte)

        value_sent = False
        while value_sent is False:
            value_sent = self.serial.send("4B13H2B", echo_msg)

        params_dict = False
        start_time = time.time()
        while params_dict is False:
            if time.time() - start_time > 1:
                params_dict = self.serial.get_params_dict(32, "13H6B")
                start_time = time.time()

        self.call_thread.emit(params_dict)
