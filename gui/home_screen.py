import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import serial


class home_screen(QMainWindow):

    def __init__(self, tables_dict, patient):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        self.ui.show()
        self.tables_dict = tables_dict
        self.table = self.tables_dict['patients_table']
        self.patient = patient
        # self.serial = serial.Serial("/dev/ttyACM0")
        self.ui.show()

    def read_serial(self):
        self.ui.close()
