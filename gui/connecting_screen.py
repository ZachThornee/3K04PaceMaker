import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import serial
import home_screen as HOME
import time
import threading


class con_screen(QMainWindow):

    def __init__(self, tables_dict, current_user):
        """
        Initialization method for connection screen

        :param tables_dict 2D_dictionary: contains both the user and patient tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnecting.ui'), self)
        log.info("Waiting for device connection")
        self.ui.show()
        self.tables_dict = tables_dict
        self.patient_dict = self.tables_dict["patients_table"].get_table_dict()
        self.serial = None
        self.ui.show()
        self.read_serial()

    def read_serial(self):
        """
        Method to read serial port and look for unique id. Also check connectivity.

        """
        # TODO actually read the serial port
        serial_num = 123456789
        log.info("Searching for patient with unique id {0}".format(serial_num))
        for patient in self.patient_dict.values():
            # If ID matches the serial num then show home screen and populate
            if patient['pacemaker_id'] == serial_num:
                log.info("Patient : {0}".format(patient))
                self.ui.close()
                # Call the main DCM screen
                HOME.home_screen(self.tables_dict, serial_num, patient)
                return
        else:
            log.info("Patient does not exist please add patient info.")
            HOME.home_screen(self.tables_dict, serial_num, None)
