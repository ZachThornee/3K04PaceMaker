


import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import login_screen as LOGIN


class home_screen(QMainWindow):

    def __init__(self, tables_dict, patient_num):
        """
        Initialization method for the DCM home screen

        :param tables_dict dictionary: dictionary containg all tables
        :param patient_num int: patient id number
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        log.info("Showing home screen")
        self.patient_num = patient_num
        self.tables_dict = tables_dict
        self.pace_table = tables_dict['pacemaker_table']
        self.patient_table = tables_dict['patients_table']

        # Buttons
        self.ui.PB_VVI.clicked.connect(lambda: self.change_mode("VVI"))
        self.ui.PB_AOO.clicked.connect(lambda: self.change_mode("AOO"))
        self.ui.PB_AAI.clicked.connect(lambda: self.change_mode("AAI"))
        self.ui.PB_VOO.clicked.connect(lambda: self.change_mode("VOO"))
        self.ui.PB_Disconnect.clicked.connect(self.disconnect)
        self.ui.PB_EditInfo.clicked.connect(self.edit_patient_info)
        self.ui.PB_ConfirmChanges.clicked.connect(self.confirm_changes)
        self.ui.show()

    def change_mode(self, mode):
        """
        Method to change passmaker mode

        :param mode string: mode to set the pacemaker to
        """
        self.pace_table.change_data("mode", mode, str)
        log.info('Pacing mode set to {}'.format(mode))

    def disconnect(self):
        """
        Disconnect a user and return to the main login screen

        """
        log.info("Disconnecting")
        self.ui.close()
        LOGIN.login_screen(self.tables_dict)

    def edit_patient_info(self):
        """
        Method to edit the info of a patient

        """
        log.info("Editing info for patient")

    def confirm_changes(self):
        """
        Method to confirm all new changes to the pacemaker

        """

        # Get all fields from the text boxes
        vrp = self.ui.TB_VRP.text()
        arp = self.ui.TB_ARP.text()
        vent_pulse_width = self.ui.TB_VentricularPulseWidth.text()
        vent_amplitude = self.ui.TB_VentricularAmplitude.text()
        atrial_pulse_width = self.ui.TB_AtrialPulseWidth.text()
        atrial_amplitude = self.ui.TB_AtrialAmplitude.text()
        upper_rate = self.ui.TB_UpperRateLimit.text()
        lower_rate = self.ui.TB_LowerRateLimit.text()

        results = []

        # Make the changes to the pacemaker table
        results.append(self.pace_table.change_data("vrp", vrp, int))
        results.append(self.pace_table.change_data("arp", arp, int))
        results.append(self.pace_table.change_data("vent_pulse_width", vent_pulse_width, int))
        results.append(self.pace_table.change_data("vent_amplitude", vent_amplitude, int))
        results.append(self.pace_table.change_data("atrial_pulse_width", atrial_pulse_width, int))
        results.append(self.pace_table.change_data("atrial_amplitude", atrial_amplitude, int))
        results.append(self.pace_table.change_data("upper_rate", upper_rate, int))
        results.append(self.pace_table.change_data("lower_rate", lower_rate, int))

        # If any of our results are None because they couldn't be entered
        for val in results:
            if val is None:
                self.ui.close()
                ERRORS.invalid_input(self.tables_dict, self)
                return

        # If this is a new patient add a new patient
        if self.patient_num is None:
            self.pace_table.add_row()

        else:
            self.pace_table.edit_row(self.patient_num)
            self.return_to_user_manager()

        log.info("Confirming changes to patient")
