import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import initial_login as LOGIN
import random


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
        self.mode = None

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
        self.mode = mode

        if mode == "VVI":
            self.restore_boxes()
            atrial_pulse_width = self.ui.TB_AtrialPulseWidth.setReadOnly(True)
            atrial_amplitude = self.ui.TB_AtrialAmplitude.setReadOnly(True)
            arp = self.ui.TB_ARP.setReadOnly(True)

        if mode == "AOO":
            self.restore_boxes()
            vrp = self.ui.TB_VRP.setReadOnly(True)
            arp = self.ui.TB_ARP.setReadOnly(True)
            vent_pulse_width = self.ui.TB_VentricularPulseWidth.setReadOnly(True)
            vent_amplitude = self.ui.TB_VentricularAmplitude.setReadOnly(True)

        if mode == "AAI":
            self.restore_boxes()
            vrp = self.ui.TB_VRP.setReadOnly(True)
            vent_pulse_width = self.ui.TB_VentricularPulseWidth.setReadOnly(True)
            vent_amplitude = self.ui.TB_VentricularAmplitude.setReadOnly(True)

        if mode == "VOO":
            self.restore_boxes()
            vrp = self.ui.TB_VRP.setReadOnly(True)
            arp = self.ui.TB_ARP.setReadOnly(True)
            atrial_pulse_width = self.ui.TB_AtrialPulseWidth.setReadOnly(True)
            atrial_amplitude = self.ui.TB_AtrialAmplitude.setReadOnly(True)


    def restore_boxes(self):
        vrp = self.ui.TB_VRP.setReadOnly(False)
        arp = self.ui.TB_ARP.setReadOnly(False)
        vent_pulse_width = self.ui.TB_VentricularPulseWidth.setReadOnly(False)
        vent_amplitude = self.ui.TB_VentricularAmplitude.setReadOnly(False)
        atrial_pulse_width = self.ui.TB_AtrialPulseWidth.setReadOnly(False)
        atrial_amplitude = self.ui.TB_AtrialAmplitude.setReadOnly(False)
        upper_rate = self.ui.TB_UpperRateLimit.setReadOnly(False)
        lower_rate = self.ui.TB_LowerRateLimit.setReadOnly(False)

        vrp = self.ui.TB_VRP.setText("")
        arp = self.ui.TB_ARP.setText("")
        vent_pulse_width = self.ui.TB_VentricularPulseWidth.setText("")
        vent_amplitude = self.ui.TB_VentricularAmplitude.setText("")
        atrial_pulse_width = self.ui.TB_AtrialPulseWidth.setText("")
        atrial_amplitude = self.ui.TB_AtrialAmplitude.setText("")
        upper_rate = self.ui.TB_UpperRateLimit.setText("")
        lower_rate = self.ui.TB_LowerRateLimit.setText("")


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

        if self.mode == "VVI":
            try:
                if float(lower_rate) > float(upper_rate):
                    ERRORS.invalid_input(self.tables_dict, self)
                    log.warning("Lower rate > upper rate")
                    return
                if float(vrp) < 150 or float(vrp) > 500:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(vent_pulse_width) < 0.05 or float(vent_pulse_width) > 1.9:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(vent_amplitude) < 0.5 or float(vent_amplitude) > 5:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(upper_rate) < 50 or float(upper_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(lower_rate) < 30 or float(lower_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
            except ValueError:
                log.error("VVI Error")
                ERRORS.invalid_input(self.tables_dict, self)
                return

            results.append(self.pace_table.change_data("vrp", vrp, float))
            results.append(self.pace_table.change_data("vent_pulse_width", vent_pulse_width, float))
            results.append(self.pace_table.change_data("vent_amplitude", vent_amplitude, float))
            results.append(self.pace_table.change_data("upper_rate", upper_rate, int))
            results.append(self.pace_table.change_data("lower_rate", lower_rate, int))

        if self.mode == "AOO":

            try:
                if float(lower_rate) > float(upper_rate):
                    log.warning("Lower rate > upper rate")
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(atrial_pulse_width) < 0.05 or float(atrial_pulse_width) > 1.9:
                    log.error("atrial_pulse_width")
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(atrial_amplitude) < 0.5 or float(atrial_amplitude) > 5:
                    log.error("atrial_amplitude")
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(upper_rate) < 50 or float(upper_rate) > 175:
                    log.error("upper_rate")
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(lower_rate) < 30 or float(lower_rate) > 175:
                    log.error("lower_rate")
                    ERRORS.invalid_input(self.tables_dict, self)
                    return

            except ValueError:
                log.error("AOO Error")
                ERRORS.invalid_input(self.tables_dict, self)
                return

            results.append(self.pace_table.change_data("atrial_pulse_width", atrial_pulse_width, float))
            results.append(self.pace_table.change_data("atrial_amplitude", atrial_amplitude, float))
            results.append(self.pace_table.change_data("upper_rate", upper_rate, int))
            results.append(self.pace_table.change_data("lower_rate", lower_rate, int))

        if self.mode == "AAI":

            try:
                if float(lower_rate) > float(upper_rate):
                    ERRORS.invalid_input(self.tables_dict, self)
                    log.warning("Lower rate > upper rate")
                    return

                if float(arp) < 150 or float(arp) > 500:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(atrial_pulse_width) < 0.05 or float(atrial_pulse_width) > 1.9:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(atrial_amplitude) < 0.5 or float(atrial_amplitude) > 5:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(upper_rate) < 50 or float(upper_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(lower_rate) < 30 or float(lower_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
            except ValueError:
                log.error("AAI Error")
                ERRORS.invalid_input(self.tables_dict, self)
                return

            results.append(self.pace_table.change_data("arp", arp, float))
            results.append(self.pace_table.change_data("atrial_pulse_width", atrial_pulse_width, float))
            results.append(self.pace_table.change_data("atrial_amplitude", atrial_amplitude, float))
            results.append(self.pace_table.change_data("upper_rate", upper_rate, int))
            results.append(self.pace_table.change_data("lower_rate", lower_rate, int))

        if self.mode == "VOO":

            try:
                if float(lower_rate) > float(upper_rate):
                    ERRORS.invalid_input(self.tables_dict, self)
                    log.warning("Lower rate > upper rate")
                    return

                if float(vent_pulse_width) < 0.05 or float(vent_pulse_width) > 1.9:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(vent_amplitude) < 0.5 or float(vent_amplitude) > 5:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(upper_rate) < 50 or float(upper_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
                if float(lower_rate) < 30 or float(lower_rate) > 175:
                    ERRORS.invalid_input(self.tables_dict, self)
                    return
            except ValueError:
                log.error("VOO Error")
                ERRORS.invalid_input(self.tables_dict, self)
                return

            results.append(self.pace_table.change_data("arp", arp, float))
            results.append(self.pace_table.change_data("atrial_pulse_width", atrial_pulse_width, float))
            results.append(self.pace_table.change_data("atrial_amplitude", atrial_amplitude, float))
            results.append(self.pace_table.change_data("upper_rate", upper_rate, int))
            results.append(self.pace_table.change_data("lower_rate", lower_rate, int))



        # If any of our results are None because they couldn't be entered
        results.append(self.pace_table.change_data("id", random.randint(1, 10000), int))
        print(results)
        for val in results:
            if val is None:
                self.ui.close()
                ERRORS.invalid_input(self.tables_dict, self)
                return

        print(self.pace_table._get_rows())

        # If this is a new patient add a new patient
        if self.patient_num is None:
            self.pace_table.add_row()

        else:
            self.pace_table.edit_row(self.patient_num)
            self.return_to_user_manager()

        log.info("Confirming changes to patient")
