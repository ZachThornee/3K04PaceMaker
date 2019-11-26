import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import initial_login as LOGIN
import random


class home_screen(QMainWindow):

    def __init__(self, tables_dict, patient_num, params_dict):
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
        self.patient_table = tables_dict['patients_table']
        self.params_dict = params_dict
        self.mode(self.params_dict["pace_mode"])
        self.ui.LAB_PacemakerID.setText(self.params_dict["pacemaker_id"])

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
        self.ui.TB_UpperRateLimit.show()
        self.ui.TB_LowerRateLimit.show()

        # Labels
        self.ui.LAB_LowerRateLimit.show()
        self.ui.LAB_UpperRateLimit.show()
        self.ui.LAB_LowerRateLimit_Units.show()
        self.ui.LAB_UpperRateLimit_Units.show()
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
        elif mode == "DOOR":
            self.ui.PB_DOOR.setStyleSheet(selected_style)

    def disconnect(self):
        """
        Disconnect a user and return to the main login screen

        """
        log.info("Disconnecting")
        self.ui.close()
        LOGIN.login_screen(self.tables_dict)

    def confirm_changes(self):
        """
        Method to confirm all new changes to the pacemaker

        """

        vent_pulse_width = self.ui.TB_VentricularPulseWidth.text()
        vent_amplitude = self.ui.TB_VentricularAmplitude.text()
        atrial_pulse_width = self.ui.TB_AtrialPulseWidth.text()
        atrial_amplitude = self.ui.TB_AtrialAmplitude.text()
        arp = self.ui.TB_ARP.text()
        vrp = self.ui.TB_VRP.text()
        av_delay = self.ui.TB_AV_Delay.text()
        activity_threshold = self.ui.TB_ActivityThreshold.text()
        response_factor = self.ui.TB_ResponseFactor.text()
        recovery_time = self.ui.TB_RecoveryTime.text()
        reaction_time = self.ui.TB_ReactionTime.text()
        upper_rate = self.ui.TB_UpperRateLimit.text()
        lower_rate = self.ui.TB_LowerRateLimit.text()

        try:
            # Upper and Lower
            self.table.check_value(upper_rate, 50, 175)
            self.table.check_value(lower_rate, 30, 175)
            self.pace_table.change_data("upper_rate", upper_rate, int)
            self.pace_table.change_data("lower_rate", lower_rate, int)

            # Ventricle
            self.table.check_value(vent_pulse_width, 0.05, 1.9)
            self.table.check_value(vent_amplitude, 0.5, 5)
            self.table.check_value(vrp, 150, 500)
            self.pace_table.change_data("vent_pulse_width", vent_pulse_width, float)
            self.pace_table.change_data("vent_amplitude", vent_amplitude, float)
            self.pace_table.change_data("vrp", vrp, float)

            # Atrium
            self.table.check_value(atrail_pulse_width, 0.05, 1.9)
            self.table.check_value(atrial_amplitude, 0.5, 5)
            self.table.check_value(arp, 150, 500)
            self.pace_table.change_data("atrial_pulse_width", atrial_pulse_width, float)
            self.pace_table.change_data("atrial_amplitude", atrial_amplitude, float)
            self.pace_table.change_data("arp", atrial_amplitude, float)

            # Other
            self.table.check_value(av_delay, 0.05, 1.9)
            self.table.check_value(activity_threshold, 0.05, 1.9)
            self.table.check_value(response_factor, 0.05, 1.9)
            self.table.check_value(recovery_time, 0.05, 1.9)
            self.table.check_value(reaction_time, 0.05, 1.9)
            self.pace_table.change_data("av_delay", av_delay, float)
            self.pace_table.change_data("activity_threshold", activity_threshold, float)
            self.pace_table.change_data("response_factor", response_factor, float)
            self.pace_table.change_data("recovery_time", recovery_time, float)
            self.pace_table.change_data("reaction_time", reaction_time, float)

        except ValueError:
            log.error("Upper and lower rate error")
            ERRORS.invalid_input(self.tables_dict, self)
            return

        # If this is a new patient add a new patient
        if self.patient_num is None:
            self.pace_table.add_row()

        else:
            self.pace_table.edit_row(self.patient_num)

        log.info("Confirming changes to patient")

    def confirm_patient_changes(self):

        # Assign values from TextBoxes to variables
        patient_num = self.ui.TB_PatientNum.text()
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        healthcard = self.ui.TB_HealthCard.text()
        sex = self.ui.TB_Sex.text()
        age = self.ui.TB_Age.text()

        # Change the values in the patient table
        try:
            self.patient_table.change_data("patient_number", patient_num, str)
            self.patient_table.change_data("first_name", first_name, str)
            self.patient_table.change_data("last_name", last_name, str)
            self.patient_table.change_data("healthcard", healthcard, str)
            self.patient_table.change_data("sex", sex, str)
            self.patient_table.change_data("age", age, str)
        except ValueError:
            log.warning("Invalid input for patient data")
            ERRORS.invalid_input(self.tables_dict, self)
