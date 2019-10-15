import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import serial
import home_screen as HOME

# Global Variables

PATIENT_LOOKUP_TABLE = "patient_info"
PATIENT_LOOKUP_PARAMETERS = [
                ["PATIENT_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT",  "NOT", "NULL"],
                ["HEALTHCARD", "TEXT", "NOT", "NULL"],
                ["SEX", "TEXT", "NOT", "NULL"],
                ["AGE", "INT", "NOT", "NULL"],
            ]

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class connecting_screen(QMainWindow):
    def __init__(self, database, current_user):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnecting.ui'),self)
        self.ui.show()
        self.database = database
        self.current_user = current_user
        self.patient_table = self.database.connect_to_table(PATIENT_LOOKUP_TABLE, PATIENT_LOOKUP_PARAMETERS)
        self.serial = None
        self.ui.show()
        self.read_serial()


    def read_serial(self):
        # while True:
        #     for i in range(100):
        #         port = "/dev/ttyACM" + str(i)
        #         try:
        #             self.serial = serial.Serial("/dev/ttyACM0")
        #             break
        #         except serial.serialutil.SerialException:
        #             log.debug("Cannot connect to serial port {0}".format(i))

        #     if self.serial is not None:
        #         break
        patient = self.find_patient()
        if patient is not None:
            log.info("Interfacing with patient : {0}, pacemaker id: {1}".format(patient, "123"))
            self.ui.close()
            HOME.home_screen(self.database, self.current_user, patient)

        else:
            log.info("This patient does not exist in the database. Please add patient info")



    def find_patient(self):
        return True
        #TODO query over serial to get patient info
        #self.ui.close()
        # while True:
        #     response = self.serial.readline()
        #     if response is not None:
                # TODO : Add code for reading and looking up serial port value
                # IF response is found move to next login screen
