import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import errors as ERRORS


class home_screen(QMainWindow):

    def __init__(self, tables_dict, patient_num):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PMConnected.ui'), self)
        log.info("Showing home screen")
        self.patient_num = patient_num
        self.pacemaker_table = tables_dict['pacemaker_table']
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
        self.pacemaker_table.change_data("mode", mode, str)
        log.info('Pacing mode set to {}'.format(mode))

    def disconnect(self):
        log.info("Disconnecting")

    def edit_patient_info(self):
        log.info("Editing info for patient")

    def confirm_changes(self):

        try:
            vrp = self.ui.TB_VRP.text()
            arp = self.ui.TB_ARP.text()
            vent_pulse_width = self.ui.TB_VentricularPulseWidth.text()
            vent_pulse_amplitude = self.ui.TB_VentricularAmplitude.text()
            atrial_pulse_width = self.ui.TB_AtrialPulseWidth.text()
            atrial_pulse_amplitude = self.ui.TB_AtrialAmplitude.text()
            upper_rate = self.ui.TB_UpperRateLimit.text()
            lower_rate = self.ui.TB_LowerRateLimit.text()

            self.pacemaker_table.change_data("vrp", vrp, int)
            self.pacemaker_table.change_data("arp", arp, int)
            self.pacemaker_table.change_data("vent_pulse_width", vent_pulse_width, int)
            self.pacemaker_table.change_data("vent_pulse_amplitude", vent_pulse_amplitude, int)
            self.pacemaker_table.change_data("atrial_pulse_width", atrial_pulse_width, int)
            self.pacemaker_table.change_data("atrial_pulse_amplitude", atrial_pulse_amplitude, int)
            self.pacemaker_table.change_data("upper_rate", upper_rate, int)
            self.pacemaker_table.change_data("lower_rate", lower_rate, int)

        except ValueError:
            # Show invalid input dialogue
            ERRORS.invalid_input(self.tables_dict, self)
            return

        if self.patient_num is None:
            self.pacemaker_table.add_row()

        else:
            self.pacemaker_table.edit_row(self.patient_num)
            self.return_to_user_manager()


        log.info("Confirming changes to patient")
