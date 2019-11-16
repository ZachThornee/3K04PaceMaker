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

        # When a mode is selected, call the internal change_mode method to perform the functionality of the PushButton
        self.ui.PB_VVI.clicked.connect(lambda: self.change_mode("VVI"))
        self.ui.PB_AOO.clicked.connect(lambda: self.change_mode("AOO"))
        self.ui.PB_AAI.clicked.connect(lambda: self.change_mode("AAI"))
        self.ui.PB_VOO.clicked.connect(lambda: self.change_mode("VOO"))
        self.ui.PB_DOO.clicked.connect(lambda: self.change_mode("DOO"))

        # Functionality for all other PushButtons on the form
        self.ui.PB_Disconnect.clicked.connect(self.disconnect)
        #self.ui.PB_EditInfo.clicked.connect(self.edit_patient_info)
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
        self.reset_buttons()
        log.info("Change_mode successful")

        if mode == "VVI":

            # Note the required parameters for VVI mode:
            # Lower Rate Limit, Upper Rate Limit, Ventricular Amplitude, Ventricular Pulse Width

            # Make all QLineEdit widgets (TextBoxes) and QLabel widgets visible and editable
            self.restore_boxes()

            # Change the colour of the VVI-mode push button to notify the user which mode they are currently in
            self.ui.PB_VVI.setStyleSheet(
                "BACKGROUND-COLOR: rgb(170, 255, 127); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; "
                "BORDER-STYLE: outset;")

            log.info ("Button colour changed successfully")

            # Make the unnecessary QLineEdit widgets (TextBoxes) hidden by changing the stylesheet
            self.ui.TB_AtrialPulseWidth.setReadOnly(True)
            self.ui.TB_AtrialPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_AtrialAmplitude.setReadOnly(True)
            self.ui.TB_AtrialAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_ARP.setReadOnly(True)
            self.ui.TB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            log.info("TextBoxes hidden successfully")

            # Make the unnecessary QLabel widgets hidden by removing the text
            self.ui.LAB_AtrialPulseWidth.setText("")
            self.ui.LAB_AtrialPulseWidth_Units.setText("")
            self.ui.LAB_AtrialAmplitude.setText("")
            self.ui.LAB_AtrialAmplitude_Units.setText("")
            self.ui.LAB_ARP.setText("")
            self.ui.LAB_ARP_Units.setText("")

            log.info("Label widgets hidden successfully")

            # Made the QLabel widgets hidden which display the units for unnecessary parameters
            self.ui.LAB_AtrialPulseWidth_Units.setText("")
            self.ui.LAB_AtrialPulseWidth_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_AtrialAmplitude_Units.setText("")
            self.ui.LAB_AtrialAmplitude_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_ARP_Units.setText("")
            self.ui.LAB_ARP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            log.info("Unit labels hidden successfully")

            # Make the rate adaptive fields hidden by calling the internal method
            self.rate_adaptive_hiding()

            # Log a message to record that the VVI mode has been properly initialized
            log.info("VVI mode initialized successfully")

        if mode == "AOO":

            # Note the required parameters for AOO mode:
            # Lower Rate Limit, Upper Rate Limit, Atrial Amplitude, Atrial Pulse Width

            # Make all QLineEdit widgets (TextBoxes) and QLabel widgets visible and editable
            self.ui.PB_AOO.setStyleSheet(
                "BACKGROUND-COLOR: rgb(170, 255, 127); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; "
                "BORDER-STYLE: outset;")

            # Make all QLineEdit widgets (TextBoxes) and QLabel widgets visible and editable
            self.restore_boxes()

            # Make the unnecessary QLineEdit widgets (TextBoxes) hidden by changing the stylesheet
            self.ui.TB_VentricularAmplitude.setReadOnly(True)
            self.ui.TB_VentricularAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VentricularPulseWidth.setReadOnly(True)
            self.ui.TB_VentricularPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VRP.setReadOnly(True)
            self.ui.TB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_ARP.setReadOnly(True)
            self.ui.TB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            # Make the unnecessary QLabel widgets hidden by changing the stylesheet
            self.ui.LAB_VentricularAmplitude.setText("")
            self.ui.LAB_VentricularAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP.setText("")
            self.ui.LAB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_ARP.setText("")
            self.ui.LAB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VentricularPulseWidth.setText("")
            self.ui.LAB_VentricularPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            # Make the unnecessary QLabel widgets which display units to be hidden by changing the stylesheet
            self.ui.LAB_VentricularAmplitude_Units.setText("")
            self.ui.LAB_VentricularAmplitude_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP_Units.setText("")
            self.ui.LAB_VRP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_ARP_Units.setText("")
            self.ui.LAB_ARP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VentricularPulseWidth_Units.setText("")
            self.ui.LAB_VentricularPulseWidth_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            # Make the rate adaptive fields hidden by calling the internal method
            self.rate_adaptive_hiding()

            # Log a message to record that AOO mode was initialized successfully
            log.info("AOO mode initialized successfully")

        if mode == "AAI":

            # Change the colour of the QPushButton widget to show that AAI mode is currently selected
            self.ui.PB_AAI.setStyleSheet(
                "BACKGROUND-COLOR: rgb(170, 255, 127); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")

            #
            #

            # Restore the original properties of all QLineEdit and QLabel widgets
            self.restore_boxes()

            # Make the unnecessary QLineEdit widgets (TextBoxes) hidden
            self.ui.TB_VentricularAmplitude.setReadOnly(True)
            self.ui.TB_VentricularAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VentricularPulseWidth.setReadOnly(True)
            self.ui.TB_VentricularPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VRP.setReadOnly(True)
            self.ui.TB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make the unnecessary QLabel widgets hidden by changing the stylesheet
            self.ui.LAB_VentricularAmplitude.setText("")
            self.ui.LAB_VentricularAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VentricularPulseWidth.setText("")
            self.ui.LAB_VentricularPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP.setText("")
            self.ui.LAB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make the unnecessary QLabel widgets which display units hidden by changing the stylesheet
            self.ui.LAB_VentricularAmplitude_Units.setText("")
            self.ui.LAB_VentricularAmplitude_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VentricularPulseWidth_Units.setText("")
            self.ui.LAB_VentricularPulseWidth_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP_Units.setText("")
            self.ui.LAB_VRP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make the rate adaptive fields hidden by calling the internal method
            self.rate_adaptive_hiding()

            # Log message to record that AOO mode has been successfully initialized
            log.info("AAO mode initialized successfully")

        if mode == "VOO":

            # Change colour of the QPushButton to show that VOO mode is currently selected
            self.ui.PB_VOO.setStyleSheet(
                "BACKGROUND-COLOR: rgb(170, 255, 127); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")

            # Make all rate adaptive fields hidden by calling the internal method
            self.restore_boxes()

            #
            #

            # Make the unnecessary QLineEdit widgets (TextBoxes) hidden
            self.ui.TB_AtrialAmplitude.setReadOnly(True)
            self.ui.TB_AtrialAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_AtrialPulseWidth.setReadOnly(True)
            self.ui.TB_AtrialPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_ARP.setReadOnly(True)
            self.ui.TB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VRP.setReadOnly(True)
            self.ui.TB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make unnecessary QLabel widgets hidden by changing the stylesheet
            self.ui.LAB_AtrialAmplitude.setText("")
            self.ui.LAB_AtrialAmplitude.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_AtrialPulseWidth.setText("")
            self.ui.LAB_AtrialPulseWidth.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_ARP.setText("")
            self.ui.LAB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP.setText("")
            self.ui.LAB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make unnecessary QLabel widgets which display units hidden by changing the stylesheet
            self.ui.LAB_AtrialAmplitude_Units.setText("")
            self.ui.LAB_AtrialAmplitude_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_AtrialPulseWidth_Units.setText("")
            self.ui.LAB_AtrialPulseWidth_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_ARP_Units.setText("")
            self.ui.LAB_ARP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP_Units.setText("")
            self.ui.LAB_VRP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make all rate adaptive fields hidden by calling the internal method
            self.rate_adaptive_hiding()

            # Log message to record that VOO mode has been successfully initialized
            log.info("VOO mode initialized successfully")

        if mode == "DOO":
            # Change colour of the QPushButton to show that VOO mode is currently selected
            self.ui.PB_VOO.setStyleSheet(
                "BACKGROUND-COLOR: rgb(170, 255, 127); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")

            # Make all rate adaptive fields hidden by calling the internal method
            self.restore_boxes()

            #
            #

            # Make the unnecessary QLineEdit widgets (TextBoxes) hidden
            self.ui.TB_ARP.setReadOnly(True)
            self.ui.TB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.TB_VRP.setReadOnly(True)
            self.ui.TB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make unnecessary QLabel widgets hidden by changing the stylesheet
            self.ui.LAB_ARP.setText("")
            self.ui.LAB_ARP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP.setText("")
            self.ui.LAB_VRP.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make unnecessary QLabel widgets which display units hidden by changing the stylesheet
            self.ui.LAB_ARP_Units.setText("")
            self.ui.LAB_ARP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_VRP_Units.setText("")
            self.ui.LAB_VRP_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            #
            #

            # Make all rate adaptive fields hidden by calling the internal method
            self.rate_adaptive_hiding()

            # After all rate adaptive fields have been made hidden, restore only the Fixed AV Delay field
            self.ui.TB_AV_Delay.setReadOnly(False)
            self.ui.TB_AV_Delay.setStyleSheet(
                "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            self.ui.LAB_AV_Delay.setText("Fixed AV Delay:")
            self.ui.LAB_AV_Delay_Units.setText("units")

            self.ui.LAB_AV_Delay_Units.setStyleSheet(
                "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
                "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

            # Log message to record that VOO mode has been successfully initialized
            log.info("VOO mode initialized successfully")

    def reset_buttons(self):
        self.ui.PB_VVI.setStyleSheet(
            "BACKGROUND-COLOR: rgb(160, 238, 252); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")
        self.ui.PB_AAI.setStyleSheet(
            "BACKGROUND-COLOR: rgb(160, 238, 252); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")
        self.ui.PB_AOO.setStyleSheet(
            "BACKGROUND-COLOR: rgb(160, 238, 252); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")
        self.ui.PB_VOO.setStyleSheet(
            "BACKGROUND-COLOR: rgb(160, 238, 252); BORDER-COLOR: rgb(160, 238. 252); BORDER-RADIUS: 10px; BORDER-STYLE: outset;")

    def restore_boxes(self):

        # Set all QLineEdit widgets (TextBoxes) to be editable (set ReadOnly property to false)
        self.ui.TB_VRP.setReadOnly(False)
        self.ui.TB_ARP.setReadOnly(False)
        self.ui.TB_VentricularPulseWidth.setReadOnly(False)
        self.ui.TB_VentricularAmplitude.setReadOnly(False)
        self.ui.TB_AtrialPulseWidth.setReadOnly(False)
        self.ui.TB_AtrialAmplitude.setReadOnly(False)
        self.ui.TB_UpperRateLimit.setReadOnly(False)
        self.ui.TB_LowerRateLimit.setReadOnly(False)
        self.ui.TB_AV_Delay.setReadOnly(False)
        self.ui.TB_ActivityThreshold.setReadOnly(False)
        self.ui.TB_ResponseFactor.setReadOnly(False)
        self.ui.TB_ReactionTime.setReadOnly(False)
        self.ui.TB_RecoveryTime.setReadOnly(False)

        log.info("restore_boxes: textbox read-only condition reset")

        #
        #

        # Reset the StyleSheet for all QLineEdit widgets (TextBox) to make them visible
        self.ui.TB_VRP.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_ARP.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_VentricularPulseWidth.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_VentricularAmplitude.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_AtrialPulseWidth.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_AtrialAmplitude.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_UpperRateLimit.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_LowerRateLimit.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_AV_Delay.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_ActivityThreshold.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_ResponseFactor.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_ReactionTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.TB_RecoveryTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        log.info("Reset_boxes: textbox style sheets reset")

        #
        #

        # Clear the text in the QLineEdit widgets so the user can input their parameters
        self.ui.TB_VRP.setText("")
        self.ui.TB_ARP.setText("")
        self.ui.TB_VentricularPulseWidth.setText("")
        self.ui.TB_VentricularAmplitude.setText("")
        self.ui.TB_AtrialPulseWidth.setText("")
        self.ui.TB_AtrialAmplitude.setText("")
        self.ui.TB_UpperRateLimit.setText("")
        self.ui.TB_LowerRateLimit.setText("")
        self.ui.TB_AV_Delay.setText("")
        self.ui.TB_ActivityThreshold.setText("")
        self.ui.TB_ResponseFactor.setText("")
        self.ui.TB_ReactionTime.setText("")
        self.ui.TB_RecoveryTime.setText("")

        log.info("Reset_boxes: textbox text reset")

        #
        #

        # Reset the text of the QLabels which allows them to be visible again
        self.ui.LAB_LowerRateLimit.setText("Lower Rate Limit:")
        self.ui.LAB_LowerRateLimit_Units.setText("bpm")

        self.ui.LAB_UpperRateLimit.setText("Upper Rate Limit:")
        self.ui.LAB_UpperRateLimit_Units.setText("bpm")

        self.ui.LAB_VRP.setText("VRP:")
        self.ui.LAB_VRP_Units.setText("s")

        self.ui.LAB_ARP.setText("ARP:")
        self.ui.LAB_ARP_Units.setText("s")

        self.ui.LAB_AtrialAmplitude.setText("Atrial Amplitude:")
        self.ui.LAB_AtrialAmplitude_Units.setText("units")

        self.ui.LAB_AtrialPulseWidth.setText("Atrial Pulse Width:")
        self.ui.LAB_AtrialPulseWidth_Units.setText("units")

        self.ui.LAB_VentricularAmplitude.setText("Ventricular Amplitude:")
        self.ui.LAB_VentricularAmplitude_Units.setText("units")

        self.ui.LAB_VentricularPulseWidth.setText("Ventricular Pulse Width:")
        self.ui.LAB_VentricularPulseWidth_Units.setText("units")

        self.ui.LAB_AV_Delay.setText("Fixed AV Delay:")
        self.ui.LAB_AV_Delay_Units.setText("units")

        self.ui.LAB_ActivityThreshold.setText("Activity Threshold:")
        self.ui.LAB_ActivityThreshold_Units.setText("units")

        self.ui.LAB_ResponseFactor.setText("Response Factor:")
        self.ui.LAB_ResponseFactor_Units.setText("units")

        self.ui.LAB_ReactionTime.setText("Reaction Time:")
        self.ui.LAB_ReactionTime_Units.setText("units")

        self.ui.LAB_RecoveryTime.setText("Recovery Time")
        self.ui.LAB_RecoveryTime_Units.setText("units")

        log.info("Reset_boxes: labels text reset")

        #
        #

        # Restore the colour of the QLabels which display parameter units after they were made white for invisibility
        self.ui.LAB_LowerRateLimit_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_UpperRateLimit_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_AtrialAmplitude_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_AtrialPulseWidth_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_VentricularAmplitude_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_VentricularPulseWidth_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_VRP_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ARP_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_AV_Delay_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ActivityThreshold_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ResponseFactor_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_RecoveryTime_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ReactionTime_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(245, 245, 245); BORDER-COLOR: rgb(245, 245, 245); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        log.info("Restore_Boxes method ran successfully")

    def rate_adaptive_hiding(self):
        """
        Hides all of the QLabel and QLineEdit widgets which are corresponding to values only required in rate-adaptive
        modes.

        This method is to be called from the change_mode method, when a mode is selective that is NOT rate-adaptive.

        Note: Rate-Adaptive parameters include the following:
            AV Delay, Activity Threshold, Response Factor, Recovery Time, Reaction Time
        """

        log.info("rate_adaptive_hiding method entered")

        # Hides all QLabel widgets that display units for rate-adaptive parameters
        self.ui.LAB_AV_Delay_Units.setText("")
        self.ui.LAB_AV_Delay_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ActivityThreshold_Units.setText("")
        self.ui.LAB_ActivityThreshold_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_RecoveryTime_Units.setText("")
        self.ui.LAB_RecoveryTime_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ReactionTime_Units.setText("")
        self.ui.LAB_ReactionTime_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ResponseFactor_Units.setText("")
        self.ui.LAB_ResponseFactor_Units.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        log.info("unit label widgets hidden successfully")

        # Hides all QLineEdit widgets (TextBoxes) that receive input values for rate-adaptive parameters
        self.ui.TB_AV_Delay.setReadOnly(True)
        self.ui.TB_AV_Delay.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")
        log.info("av delay")

        self.ui.TB_ActivityThreshold.setReadOnly(True)
        self.ui.TB_ActivityThreshold.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")
        log.info("act thresh")

        self.ui.TB_ResponseFactor.setReadOnly(True)
        self.ui.TB_ResponseFactor.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")
        log.info("resp fact")

        self.ui.TB_RecoveryTime.setReadOnly(True)
        self.ui.TB_RecoveryTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")
        log.info("rec time")

        self.ui.TB_ReactionTime.setReadOnly(True)
        self.ui.TB_ReactionTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")
        log.info("reac time")

        log.info("textboxes hidden successfully")

        # Hides all QLabel widgets which display the headings for rate-adaptive parameters
        self.ui.LAB_AV_Delay.setText("")
        self.ui.LAB_AV_Delay.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ActivityThreshold.setText("")
        self.ui.LAB_ActivityThreshold.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_RecoveryTime.setText("")
        self.ui.LAB_RecoveryTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ReactionTime.setText("")
        self.ui.LAB_ReactionTime.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        self.ui.LAB_ResponseFactor.setText("")
        self.ui.LAB_ResponseFactor.setStyleSheet(
            "BACKGROUND-COLOR: rgb(255, 255, 255); BORDER-COLOR: rgb(255, 255, 255); BORDER-RADIUS: 7px; "
            "BORDER-WIDTH: 1px; BORDER-STYLE: outset;")

        log.info("rate_adaptive_hiding ran successfully")

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
