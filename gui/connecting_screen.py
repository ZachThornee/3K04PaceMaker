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

        patient_table = self.tables_dict["patients_table"]
        pacemaker_table = self.tables_dict["pacemaker_table"]
        pacemaker_dict = pacemaker_table.get_table_dict()
        current_patient = None
        current_pacemaker = None
        for patient in self.patient_dict.values():
            # If ID matches the serial num then show home screen and populate
            if patient['pacemaker_id'] == serial_num:
                current_patient = patient
                log.info("Patient : {0}".format(patient))

                for pacemaker in pacemaker_dict.values():
                    if pacemaker["id"] == patient["pacemaker_id"]:
                        current_pacemaker = pacemaker
                        break

            # Call the main DCM screen
            HOME.home_screen(patient_table, current_patient, pacemaker_table, current_pacemaker)
            return

        else:
            log.info("Patient does not exist please add patient info.")
            HOME.home_screen(patient_table, current_patient, pacemaker_table, current_pacemaker)
