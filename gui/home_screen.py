import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import serial

# Global Variables

PATIENT_LOOKUP_TABLE = "patient_info"

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class home_screen(QMainWindow):
    def __init__(self, database, current_user, patient):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'),self)
        self.ui.show()
        self.database = database
        self.current_user = current_user
        self.patient_table = self.database.connect_to_table(PATIENT_LOOKUP_TABLE)
        #self.serial = serial.Serial("/dev/ttyACM0")
        self.ui.show()


    def read_serial(self):
        self.ui.close()
        # while True:
        #     response = self.serial.readline()
        #     if response is not None:
                # TODO : Add code for reading and looking up serial port value
                # IF response is found move to next login screen
