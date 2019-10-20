import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import serial
import home_screen as HOME


class con_screen(QMainWindow):
    def __init__(self, table_dict, current_user):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnecting.ui'), self)
        log.info("Waiting for device connection")
        self.ui.show()
        self.table_dict = table_dict
        self.current_user = current_user
        self.patient_dict = self.table_dict["patient_info"].get_table_dict()
        self.serial = None
        self.ui.show()
        self.read_serial()

    def read_serial(self):
        # TODO actually read the serial port
        serial_num = 123456789
        log.info("Searching for patient with unique id {0}".format(serial_num))

        table_name_dict = self.table_name.get_table_dict()

        for patient in table_name_dict.values():
            if patient['pacemaker_id'] == serial_num:
                log.info("Patient : {0}".format(patient))
                self.ui.close()
                HOME.home_screen(self.db, self.current_user, patient)
                return
        else:
            log.info("Patient does not exist please add patient info.")

