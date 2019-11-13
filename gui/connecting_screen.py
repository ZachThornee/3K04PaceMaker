import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import home_screen as HOME


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
        self.serial = None
        self.ui.show()
        self.ui.PB_HomeScreen.clicked.connect(self.read_serial)
        self.ui.PB_ConnectionError.clicked.connect(self.connection_error)

    def read_serial(self):
        """
        Method to read serial port and look for unique id. Also check connectivity.

        """
        self.ui.close()
        # TODO actually read the serial port
        patient_num = None
        # Call the main DCM screen
        HOME.home_screen(self.tables_dict, patient_num)
        return

    def connection_error(self):
        """
        Temporary method to display connection error

        """
        ERRORS.connection_error(self.tables_dict, self)
