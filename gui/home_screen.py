import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import serial


class home_screen(QMainWindow):
    def __init__(self, database, current_user, patient_table):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        self.ui.show()
        self.database = database
        self.table = patient_table
        self.current_user = current_user
        # self.serial = serial.Serial("/dev/ttyACM0")
        self.ui.show()

    def read_serial(self):
        self.ui.close()
