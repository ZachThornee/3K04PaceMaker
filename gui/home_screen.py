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
        self.hide_all()

        # When a mode is selected, call the internal change_mode method to perform the functionality of the PushButton
        self.ui.PB_VVI.clicked.connect(lambda: self.change_mode("VVI"))
        self.ui.PB_AOO.clicked.connect(lambda: self.change_mode("AOO"))
        self.ui.PB_AAI.clicked.connect(lambda: self.change_mode("AAI"))
        self.ui.PB_VOO.clicked.connect(lambda: self.change_mode("VOO"))
        self.ui.PB_DOO.clicked.connect(lambda: self.change_mode("DOO"))
        self.ui.PB_AOOR.clicked.connect(lambda: self.change_mode("AOOR"))
        self.ui.PB_AAIR.clicked.connect(lambda: self.change_mode("AAIR"))
        self.ui.PB_VOOR.clicked.connect(lambda: self.change_mode("VOOR"))
        self.ui.PB_VVIR.clicked.connect(lambda: self.change_mode("VVIR"))
        self.ui.PB_DOOR.clicked.connect(lambda: self.change_mode("DOOR"))

        # Functionality for all other PushButtons on the form
        self.ui.PB_Disconnect.clicked.connect(self.disconnect)
        self.ui.PB_ConfirmChanges.clicked.connect(self.confirm_changes)
        self.ui.PB_ConfirmPatient.clicked.connect(self.confirm_patient_changes)
        self.ui.show()

    def change_mode(self, mode):
        """
        Method to change passmaker mode

        :param mode string: mode to set the pacemaker to
        """

        self.pace_table.change_data("mode", mode, str)
        log.info('Pacing mode set to {}'.format(mode))
        self.mode = mode
        self.reset_screen()
        self.set_button_colour(mode)

        if self.mode == "VVI" or mode == "VOO":
            # Entries
            self.ui.TB_AtrialPulseWidth.hide()
            self.ui.TB_AtrialAmplitude.hide()
            self.ui.TB_ARP.hide()

            # Labels
            self.ui.LAB_AtrialAmplitude.hide()
            self.ui.LAB_AtrialAmplitude_Units.hide()
            self.ui.LAB_AtrialPulseWidth.hide()
            self.ui.LAB_AtrialPulseWidth_Units.hide()
            self.ui.LAB_ARP.hide()
            self.ui.LAB_ARP_Units.hide()
            self.rate_adaptive_hiding()

            if mode == "VOO":
                # In addition to VVI, hide the VRP entry box
                self.ui.TB_VRP.hide()

                # In addition to VVI, hide the VRP labels
                self.ui.LAB_VRP.hide()
                self.ui.LAB_VRP_Units.hide()

                log.info("VOO mode initialized successfully")

            else:
                log.info("VVI mode initialized successfully")

        elif mode == "AAI" or mode == "AOO":
            # Entries
            self.ui.TB_VentricularAmplitude.hide()
            self.ui.TB_VentricularPulseWidth.hide()
            self.ui.TB_VRP.hide()

            # Labels
            self.ui.LAB_VentricularAmplitude.hide()
            self.ui.LAB_VentricularPulseWidth.hide()
            self.ui.LAB_VentricularAmplitude_Units.hide()
            self.ui.LAB_VentricularPulseWidth_Units.hide()
            self.ui.LAB_VRP.hide()
            self.ui.LAB_VRP_Units.hide()
            self.rate_adaptive_hiding()

            if self.mode == "AOO":
                # In addition to AAI, hide the ARP entry box
                self.ui.TB_ARP.hide()

                # In addition to AAI, hide the ARP labels
                self.ui.LAB_ARP.hide()
                self.ui.LAB_ARP_Units.hide()

                log.info("AOO mode initialized correctly")

            else:
                log.info("AAI mode initialized successfully")

        elif mode == "DOO" or mode == "DOOR":
            # Entries
            self.ui.TB_VRP.hide()
            self.ui.TB_ARP.hide()

            # Labels
            self.ui.LAB_VRP.hide()
            self.ui.LAB_VRP_Units.hide()
            self.ui.LAB_ARP.hide()
            self.ui.LAB_ARP_Units.hide()

            if self.mode == "DOO":
                self.rate_adaptive_hiding()
                self.ui.TB_AV_Delay.show()
                self.ui.LAB_AV_Delay.show()
                self.ui.LAB_AV_Delay_Units.show()

                log.info("DOO mode initialized successfully")

            else:
                log.info("DOOR mode initialized successfully")

        elif mode == "AOOR" or mode == "AAIR":
            # Entries
            self.ui.TB_VentricularAmplitude.hide()
            self.ui.TB_VentricularPulseWidth.hide()
            self.ui.TB_VRP.hide()
            self.ui.TB_AV_Delay.hide()

            # Labels
            self.ui.LAB_VentricularAmplitude.hide()
            self.ui.LAB_VentricularAmplitude_Units.hide()
            self.ui.LAB_VentricularPulseWidth.hide()
            self.ui.LAB_VentricularPulseWidth_Units.hide()
            self.ui.LAB_VRP.hide()
            self.ui.LAB_VRP_Units.hide()
            self.ui.LAB_AV_Delay.hide()
            self.ui.LAB_AV_Delay_Units.hide()

            if self.mode == "AOOR":
                # Entries
                self.ui.TB_ARP.hide()

                # Labels
                self.ui.LAB_ARP.hide()
                self.ui.LAB_ARP_Units.hide()

                log.info("AOOR mode initialized successfully")

            else:
                log.info("AAIR mode initialized successfully")

        elif mode == "VVIR" or mode == "VOOR":
            # Entries
            self.ui.TB_AtrialAmplitude.hide()
            self.ui.TB_AtrialPulseWidth.hide()
            self.ui.TB_ARP.hide()
            self.ui.TB_AV_Delay.hide()

            # Labels
            self.ui.LAB_AtrialAmplitude.hide()
            self.ui.LAB_AtrialAmplitude_Units.hide()
            self.ui.LAB_AtrialPulseWidth.hide()
            self.ui.LAB_AtrialPulseWidth_Units.hide()
            self.ui.LAB_ARP.hide()
            self.ui.LAB_ARP_Units.hide()
            self.ui.LAB_AV_Delay.hide()
            self.ui.LAB_AV_Delay_Units.hide()

            if self.mode == "VOOR":
                # In addition to VVIR, hide the VRP entry box
                self.ui.TB_VRP.hide()

                # In addition to VVIR, hide the VRP labels
                self.ui.LAB_VRP.hide()
                self.ui.LAB_VRP_Units.hide()

                log.info("VOOR mode initialized successfully")

            else:
                log.info("VVIR mode initialized successfully")

        self.update()

    def reset_screen(self):
        # Text Boxes
        self.ui.TB_VentricularPulseWidth.show()
        self.ui.TB_VentricularAmplitude.show()
        self.ui.TB_AtrialPulseWidth.show()
        self.ui.TB_AtrialAmplitude.show()
        self.ui.TB_ARP.show()
        self.ui.TB_VRP.show()
        self.ui.TB_AV_Delay.show()
        self.ui.TB_ActivityThreshold.show()
        self.ui.TB_ResponseFactor.show()
        self.ui.TB_RecoveryTime.show()
        self.ui.TB_ReactionTime.show()

        # Labels
        self.ui.LAB_VentricularAmplitude.show()
        self.ui.LAB_VentricularAmplitude_Units.show()
        self.ui.LAB_VentricularPulseWidth.show()
        self.ui.LAB_VentricularPulseWidth_Units.show()
        self.ui.LAB_AtrialAmplitude.show()
        self.ui.LAB_AtrialAmplitude_Units.show()
        self.ui.LAB_AtrialPulseWidth.show()
        self.ui.LAB_AtrialPulseWidth_Units.show()
        self.ui.LAB_ARP.show()
        self.ui.LAB_ARP_Units.show()
        self.ui.LAB_VRP.show()
        self.ui.LAB_VRP_Units.show()
        self.ui.LAB_AV_Delay_Units.show()
        self.ui.LAB_ActivityThreshold_Units.show()
        self.ui.LAB_RecoveryTime_Units.show()
        self.ui.LAB_ReactionTime_Units.show()
        self.ui.LAB_ResponseFactor_Units.show()
        self.ui.LAB_AV_Delay.show()
        self.ui.LAB_ActivityThreshold.show()
        self.ui.LAB_RecoveryTime.show()
        self.ui.LAB_ReactionTime.show()
        self.ui.LAB_ResponseFactor.show()

        self.update()
        log.info("Resetting Screen Successful")

    def hide_all(self):
        """

        This method will hide all labels and TextBoxes in the parameters groupBox

        """

        # Hide TextBoxes (QLineEdit widgets)
        self.ui.TB_LowerRateLimit.hide()
        self.ui.TB_UpperRateLimit.hide()
        self.ui.TB_AtrialAmplitude.hide()
        self.ui.TB_AtrialPulseWidth.hide()
        self.ui.TB_VentricularAmplitude.hide()
        self.ui.TB_VentricularPulseWidth.hide()
        self.ui.TB_VRP.hide()
        self.ui.TB_ARP.hide()

        # Hide labels
        self.ui.LAB_LowerRateLimit.hide()
        self.ui.LAB_UpperRateLimit.hide()
        self.ui.LAB_AtrialAmplitude.hide()
        self.ui.LAB_AtrialPulseWidth.hide()
        self.ui.LAB_VentricularAmplitude.hide()
        self.ui.LAB_VentricularPulseWidth.hide()
        self.ui.LAB_VRP.hide()
        self.ui.LAB_ARP.hide()

        # Hide labels which display units
        self.ui.LAB_LowerRateLimit_Units.hide()
        self.ui.LAB_UpperRateLimit_Units.hide()
        self.ui.LAB_AtrialAmplitude_Units.hide()
        self.ui.LAB_AtrialPulseWidth_Units.hide()
        self.ui.LAB_VentricularAmplitude_Units.hide()
        self.ui.LAB_VentricularPulseWidth_Units.hide()
        self.ui.LAB_VRP.hide()
        self.ui.LAB_ARP.hide()

        # hide all rate-adaptive field widgets
        self.rate_adaptive_hiding()

    def rate_adaptive_hiding(self):
        # Labels
        self.ui.LAB_AV_Delay_Units.hide()
        self.ui.LAB_ActivityThreshold_Units.hide()
        self.ui.LAB_RecoveryTime_Units.hide()
        self.ui.LAB_ReactionTime_Units.hide()
        self.ui.LAB_ResponseFactor_Units.hide()
        self.ui.LAB_AV_Delay.hide()
        self.ui.LAB_ActivityThreshold.hide()
        self.ui.LAB_RecoveryTime.hide()
        self.ui.LAB_ReactionTime.hide()
        self.ui.LAB_ResponseFactor.hide()

        # Entries
        self.ui.TB_AV_Delay.hide()
        self.ui.TB_ActivityThreshold.hide()
        self.ui.TB_ResponseFactor.hide()
        self.ui.TB_RecoveryTime.hide()
        self.ui.TB_ReactionTime.hide()
        log.debug("Rate adaptive hiding complete")

    def set_button_colour(self, mode):
        """

        This method will change the colour of the QPushButton selected by the user to identify that it's been selected.
        Which button is selected is determined by the mode parameter.

        """

        # Creates the string for the normal-style StyleSheet
        normal_style = "BACKGROUND-COLOR: rgb(160, 238, 252); \
                        BORDER-COLOR: rgb(160, 238, 252); \
                        BORDER-RADIUS: 10px; \
                        BORDER-STYLE: outset; \
                        FONT-SIZE: 20px;"

        # Creates the string for the selected-style StyleSheet
        selected_style = "BACKGROUND-COLOR: rgb(170, 255, 127); \
                          BORDER-COLOR: rgb(160, 238, 252); \
                          BORDER-RADIUS: 10px; \
                          BORDER-STYLE: outset; \
                          FONT-SIZE: 20px;"

        # Reset all buttons to the normal StyleSheet
        self.ui.PB_VVI.setStyleSheet(normal_style)
        self.ui.PB_AAI.setStyleSheet(normal_style)
        self.ui.PB_AOO.setStyleSheet(normal_style)
        self.ui.PB_VOO.setStyleSheet(normal_style)
        self.ui.PB_DOO.setStyleSheet(normal_style)
        self.ui.PB_AOOR.setStyleSheet(normal_style)
        self.ui.PB_AAIR.setStyleSheet(normal_style)
        self.ui.PB_VOOR.setStyleSheet(normal_style)
        self.ui.PB_VVIR.setStyleSheet(normal_style)
        self.ui.PB_DOOR.setStyleSheet(normal_style)

        # Change the selected button to the selected StyleSheet
        if mode == "VVI":
            self.ui.PB_VVI.setStyleSheet(selected_style)
        elif mode == "AAI":
            self.ui.PB_AAI.setStyleSheet(selected_style)
        elif mode == "AOO":
            self.ui.PB_AOO.setStyleSheet(selected_style)
        elif mode == "VOO":
            self.ui.PB_VOO.setStyleSheet(selected_style)
        elif mode == "DOO":
            self.ui.PB_DOO.setStyleSheet(selected_style)
        elif mode == "AOOR":
            self.ui.PB_AOOR.setStyleSheet(selected_style)
        elif mode == "AAIR":
            self.ui.PB_AAIR.setStyleSheet(selected_style)
        elif mode == "VOOR":
            self.ui.PB_VOOR.setStyleSheet(selected_style)
        elif mode == "VVIR":
            self.ui.PB_VVIR.setStyleSheet(selected_style)

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

            # Check that the values entered are valid
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

    def confirm_patient_changes(self):

        log.info("entered")

        # Assign values from TextBoxes to variables
        patientNum = self.ui.TB_PatientNum.text()
        log.info("1")
        firstName = self.ui.TB_FirstName.text()
        log.info("2")
        lastName = self.ui.TB_LastName.text()
        log.info("3")
        healthCard = self.ui.TB_HealthCard.text()
        log.info("4")
        sex = self.ui.TB_Sex.text()
        log.info("5")
        age = self.ui.TB_Age.text()
        log.info("6")
        pacemakerID = self.ui.TB_PacemakerID.text()
        log.info("7")

        log.info("1")

        # Create array to store results
        patientResults = []
        log.info("2")

        # Append new values to the results array
        patientResults.append(self.patient_table.change_data("patient_number", patientNum, str))
        log.info("3")
        patientResults.append(self.patient_table.change_data("first_name", firstName, str))
        log.info("4")
        patientResults.append(self.patient_table.change_data("last_name", lastName, str))
        log.info("5")
        patientResults.append(self.patient_table.change_data("healthcard", healthCard, str))
        log.info("6")
        patientResults.append(self.patient_table.change_data("sex", sex, str))
        log.info("7")
        patientResults.append(self.patient_table.change_data("age", age, str))
        log.info("8")
        patientResults.append(self.patient_table.change_data("pacemaker_id", pacemakerID, str))
        log.info("9")

