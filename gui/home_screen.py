import logging as log

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import initial_login as LOGIN
import time


class home_screen(QMainWindow):

    def __init__(self, tables_dict, params_dict, serial):
        """
        Initialization method for the DCM home screen

        :param tables_dict dictionary: dictionary containg all tables
        :param patient_num int: patient id number
        """

        super().__init__()
        log.info("before ui file")
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        log.info("Showing home screen")
        self.tables_dict = tables_dict
        self.table = self.tables_dict['patients_table']
        self.params_dict = params_dict
        self.rate_toggle = None
        self.mode = (self.params_dict["pace_mode"])
        self.mode_number = None
        self.change_mode(self.mode)
        self.id = self.params_dict['patient_id']
        self.ui.LAB_UniquePatientID.setText(str(self.id))
        self.ui.LAB_ID.setText("ID: " + str(self.id))
        self.populate_patient_info()
        self.populate_params()
        self.serial = serial

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

        log.info('Pacing mode set to {}'.format(mode))
        self.mode = mode
        self.reset_screen()
        self.set_button_colour(mode)

        if self.mode in ["AOOR", "AAIR", "VVIR", "VOOR", "DOOR"]:
            self.rate_toggle = 1
            mode_dict = {"AOOR": 1,
                         "VOOR": 2,
                         "AAIR": 3,
                         "VVIR": 4,
                         "DOOR": 5}
        else:
            self.rate_toggle = 0
            mode_dict = {"AOO": 1,
                         "VOO": 2,
                         "AAI": 3,
                         "VVI": 4,
                         "DOO": 5}

        self.mode_number = mode_dict[mode]

        if self.mode == "VVI" or mode == "VOO":
            # Entries
            self.ui.SB_AtrialPulseWidth.hide()
            self.ui.SB_AtrialAmplitude.hide()
            self.ui.SB_ARP.hide()

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
                self.ui.SB_VRP.hide()

                # In addition to VVI, hide the VRP labels
                self.ui.LAB_VRP.hide()
                self.ui.LAB_VRP_Units.hide()

                log.info("VOO mode initialized successfully")

            else:
                log.info("VVI mode initialized successfully")

        elif mode == "AAI" or mode == "AOO":
            # Entries
            self.ui.SB_VentricularAmplitude.hide()
            self.ui.SB_VentricularPulseWidth.hide()
            self.ui.SB_VRP.hide()

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
                self.ui.SB_ARP.hide()

                # In addition to AAI, hide the ARP labels
                self.ui.LAB_ARP.hide()
                self.ui.LAB_ARP_Units.hide()

                log.info("AOO mode initialized correctly")

            else:
                log.info("AAI mode initialized successfully")

        elif mode == "DOO" or mode == "DOOR":
            # Entries
            self.ui.SB_VRP.hide()
            self.ui.SB_ARP.hide()

            # Labels
            self.ui.LAB_VRP.hide()
            self.ui.LAB_VRP_Units.hide()
            self.ui.LAB_ARP.hide()
            self.ui.LAB_ARP_Units.hide()

            if self.mode == "DOO":
                self.rate_adaptive_hiding()
                self.ui.SB_AV_Delay.show()
                self.ui.LAB_AV_Delay.show()
                self.ui.LAB_AV_Delay_Units.show()

                log.info("DOO mode initialized successfully")

            else:
                log.info("DOOR mode initialized successfully")

        elif mode == "AOOR" or mode == "AAIR":
            # Entries
            self.ui.SB_VentricularAmplitude.hide()
            self.ui.SB_VentricularPulseWidth.hide()
            self.ui.SB_VRP.hide()
            self.ui.SB_AV_Delay.hide()

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
                self.ui.SB_ARP.hide()

                # Labels
                self.ui.LAB_ARP.hide()
                self.ui.LAB_ARP_Units.hide()

                log.info("AOOR mode initialized successfully")

            else:
                log.info("AAIR mode initialized successfully")

        elif mode == "VVIR" or mode == "VOOR":
            # Entries
            self.ui.SB_AtrialAmplitude.hide()
            self.ui.SB_AtrialPulseWidth.hide()
            self.ui.SB_ARP.hide()
            self.ui.SB_AV_Delay.hide()

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
                self.ui.SB_VRP.hide()

                # In addition to VVIR, hide the VRP labels
                self.ui.LAB_VRP.hide()
                self.ui.LAB_VRP_Units.hide()

                log.info("VOOR mode initialized successfully")

            else:
                log.info("VVIR mode initialized successfully")

        self.update()

    def reset_screen(self):

        # Text Boxes
        self.ui.SB_VentricularPulseWidth.show()
        self.ui.SB_VentricularAmplitude.show()
        self.ui.SB_AtrialPulseWidth.show()
        self.ui.SB_AtrialAmplitude.show()
        self.ui.SB_ARP.show()
        self.ui.SB_VRP.show()
        self.ui.SB_AV_Delay.show()
        self.ui.SB_ActivityThreshold.show()
        self.ui.SB_ResponseFactor.show()
        self.ui.SB_RecoveryTime.show()
        self.ui.SB_ReactionTime.show()
        self.ui.SB_UpperRateLimit.show()
        self.ui.SB_LowerRateLimit.show()
        self.ui.SB_MSR.show()

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
        self.ui.LAB_MSR.show()
        self.ui.LAB_MSR_Units.show()

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
        self.ui.LAB_MSR.hide()
        self.ui.LAB_MSR_Units.hide()

        # Entries
        self.ui.SB_AV_Delay.hide()
        self.ui.SB_ActivityThreshold.hide()
        self.ui.SB_ResponseFactor.hide()
        self.ui.SB_RecoveryTime.hide()
        self.ui.SB_ReactionTime.hide()
        self.ui.SB_MSR.hide()
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

        try:

            vent_pulse_width = self.ui.SB_VentricularPulseWidth.value()
            vent_amplitude = self.ui.SB_VentricularAmplitude.value()
            atrial_pulse_width = self.ui.SB_AtrialPulseWidth.value()
            atrial_amplitude = self.ui.SB_AtrialAmplitude.value()
            arp = self.ui.SB_ARP.value()
            vrp = self.ui.SB_VRP.value()
            av_delay = self.ui.SB_AV_Delay.value()
            activity_thres = self.ui.SB_ActivityThreshold.value()
            response_factor = self.ui.SB_ResponseFactor.value()
            recovery_time = self.ui.SB_RecoveryTime.value()
            reaction_time = self.ui.SB_ReactionTime.value()
            upper_rate = self.ui.SB_UpperRateLimit.value()
            lower_rate = self.ui.SB_LowerRateLimit.value()
            msr = self.ui.SB_MSR.value()

            # Upper and Lower
            self.table.check_values(upper_rate, 50, 175)
            self.table.check_values(lower_rate, 30, 175)
            self.params_dict['upper_rate'] = upper_rate
            self.params_dict['lower_rate'] = lower_rate

            # Ventricle
            self.table.check_values(vent_pulse_width, 5, 40)
            self.table.check_values(vent_amplitude, 1250, 5000)
            self.table.check_values(vrp, 150, 500)
            self.params_dict['vent_pulse_width'] = vent_pulse_width
            self.params_dict['vent_pulse_amp'] = vent_amplitude
            self.params_dict['vrp'] = vrp

            # Atrium

            self.table.check_values(atrial_pulse_width, 5, 40)
            self.table.check_values(atrial_amplitude, 1250, 5000)
            self.table.check_values(arp, 150, 500)
            self.params_dict['atr_pulse_width'] = atrial_pulse_width
            self.params_dict['atr_pulse_amp'] = atrial_amplitude
            self.params_dict['arp'] = arp

            # Other
            self.table.check_values(av_delay, 70, 300)
            self.table.check_values(activity_thres, 1, 7)
            self.table.check_values(response_factor, 1, 16)
            self.table.check_values(recovery_time, 2, 16)
            self.table.check_values(reaction_time, 10, 50)
            self.table.check_values(msr, 50, 175)  #TODO fix msr
            self.params_dict['fixed_av_delay'] = av_delay
            self.params_dict['activity_thres'] = activity_thres
            self.params_dict['response_factor'] = response_factor
            self.params_dict['recovery_time'] = recovery_time
            self.params_dict['reaction_time'] = reaction_time
            self.params_dict['msr'] = msr


            # Mode based info
            self.params_dict['pace_mode'] = self.mode_number
            self.params_dict['rate_toggle'] = self.rate_toggle

            start_byte = 22  # Start of serial msg
            echo_bool = 85  # Write params
            params = [start_byte,
                      echo_bool,
                      self.params_dict['pace_mode'],
                      self.params_dict['activity_thres'],
                      self.params_dict['lower_rate'],
                      self.params_dict['upper_rate'],
                      self.params_dict['msr'],
                      self.params_dict['fixed_av_delay'],
                      self.params_dict['atr_pulse_amp'],
                      self.params_dict['vent_pulse_amp'],
                      self.params_dict['atr_pulse_width'],
                      self.params_dict['vent_pulse_width'],
                      self.params_dict['arp'],
                      self.params_dict['vrp'],
                      self.params_dict['reaction_time'],
                      self.params_dict['response_factor'],
                      self.params_dict['recovery_time'],
                      self.params_dict['rate_toggle'],
                      0]
            for _ in range(5):
                self.serial.send("4B13H2B", params)  # Write
            params[1] = 34  # Echo params
            self.serial.send("4B13H2B", params)  # Echo

            self.params_dict = self.serial.get_params_dict(32, "13H6B")
            log.info("Confirmed changes to patient")
            self.populate_params()
            self.update()

        except ValueError:  # If there is an error with serial params
            log.error("Invalid serial input")
            ERRORS.invalid_serial()
            return

        except SystemError:  # If there is an error with the pacemaker connection
            log.error("No serial device connected")
            ERRORS.no_serial_connected(self.tables_dict, self)


    def confirm_patient_changes(self):

        # Assign values from TextBoxes to variables
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        healthcard = self.ui.TB_HealthCard.text()
        if self.ui.RB_Male.isChecked():
            sex = "Male"
        else:
            sex = "Female"

        age = self.ui.SB_Age.value()

        # Change the values in the patient table
        try:
            unique = self.table.check_unique("patient_id", self.id, int)
            self.table.change_data("patient_id", self.id, int)
            self.table.change_data("first_name", first_name, str)
            self.table.change_data("last_name", last_name, str)
            self.table.change_data("healthcard", healthcard, str)
            self.table.change_data("sex", sex, str)
            self.table.change_data("age", age, int)

            if unique:
                self.table.add_row()
            else:
                self.table.edit_row(self.id)

        except ValueError:
            log.warning("Invalid input for patient data")
            ERRORS.invalid_input(self.tables_dict, self)

        log.info("Changes made to patient info")

    def populate_patient_info(self):

        rn = self.table.get_value(None, "patient_id", self.id)

        if rn is not None:
            first_name = self.table.get_value(rn, 'first_name')
            last_name = self.table.get_value(rn, 'last_name')
            healthcard = self.table.get_value(rn, 'healthcard')
            sex = self.table.get_value(rn, 'sex')
            age = self.table.get_value(rn, 'age')

            self.ui.TB_FirstName.setText(str(first_name))
            self.ui.TB_LastName.setText(str(last_name))
            self.ui.TB_HealthCard.setText(str(healthcard))
            self.ui.SB_Age.setValue(age)
            if sex.lower() == "male":
                self.ui.RB_Male.setChecked(True)
                self.ui.RB_Female.setChecked(False)
            else:
                self.ui.RB_Male.setChecked(False)
                self.ui.RB_Female.setChecked(True)

        log.info("Populated patient info")

    def populate_params(self):
        self.ui.SB_VentricularPulseWidth.setValue(self.params_dict['vent_pulse_width'])
        self.ui.SB_VentricularAmplitude.setValue(self.params_dict['vent_pulse_amp'])
        self.ui.SB_AtrialPulseWidth.setValue(self.params_dict['atr_pulse_width'])
        self.ui.SB_AtrialAmplitude.setValue(self.params_dict['atr_pulse_amp'])
        self.ui.SB_ARP.setValue(self.params_dict['arp'])
        self.ui.SB_VRP.setValue(self.params_dict['vrp'])
        self.ui.SB_AV_Delay.setValue(self.params_dict['fixed_av_delay'])
        self.ui.SB_ActivityThreshold.setValue(self.params_dict['activity_thres'])
        self.ui.SB_ResponseFactor.setValue(self.params_dict['response_factor'])
        self.ui.SB_RecoveryTime.setValue(self.params_dict['recovery_time'])
        self.ui.SB_ReactionTime.setValue(self.params_dict['reaction_time'])
        self.ui.SB_UpperRateLimit.setValue(self.params_dict['upper_rate'])
        self.ui.SB_LowerRateLimit.setValue(self.params_dict['lower_rate'])
        self.ui.SB_MSR.setValue(self.params_dict['msr'])
