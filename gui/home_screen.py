import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import errors as ERRORS


class home_screen(QMainWindow):

    def __init__(self, patient_table, patient, pacemaker_table, pacemaker):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        log.info("Showing home screen")

        # Tables
        self.patient_table = patient_table
        self.pacemaker_table = pacemaker_table

        # Patient info
        self.patient = patient
        self.pacemaker = pacemaker

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
        self.patient['pacing_mode'] = mode
        log.info('Pacing mode set to {}'.format(mode))

    def disconnect(self):
        log.info("Disconnecting")

    def edit_patient_info(self):
        log.info("Editing info for patient {}".format(self.patient['name']))

    def confirm_changes(self):

        try:
            self.pacemaker["vrp"] = abs(int(self.ui.TB_VRP.text()))
            self.pacemaker["arp"] = abs(int(self.ui.TB_ARP.text()))
            self.pacemaker["vent_pulse_width"] = abs(int(self.ui.TB_VentricularPulseWidth.text()))
            self.pacemaker["vent_pulse_amplitude"] = abs(int(self.ui.TB_VentricularAmplitude.text()))
            self.pacemaker["atrial_pulse_width"] = abs(int(self.ui.TB_AtrialPulseWidth.text()))
            self.pacemaker["atrial_pulse_amplitude"] = abs(int(self.ui.TB_AtrialAmplitude.text()))
            self.pacemaker["atrial_pulse_amplitude"] = abs(int(self.ui.TB_AtrialAmplitude.text()))
            self.pacemaker["upper_rate"] = abs(int(self.ui.TB_UpperRateLimit.text()))
            self.pacemaker["lower_rate"] = abs(int(self.ui.TB_LowerrateLimit.text()))
        except ValueError:
            # Show invalid input dialogue
            ERRORS.invalid_input(self.tables_dict, self)
            return

        self.pacemaker_table.edit_row(self.edit_pacemaker_list, serial_num)
        self.return_to_user_manager()


        log.info("Confirming changes to patient")
