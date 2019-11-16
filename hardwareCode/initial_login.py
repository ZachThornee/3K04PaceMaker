import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import connecting_screen as CON_SCREEN
from specific_login import specific_login


class login_screen(QMainWindow):

    def __init__(self, tables_dict):
        """
        Constructor for the initial doctor login screen

        :param tables_dict dictionary: A dictionary containing all tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_LoginScreen.ui'), self)
        log.info("Showing main login screen")
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']
        self.ui.PB_Confirm.clicked.connect(self.login_button)
        self.ui.PB_ForgotPassword.clicked.connect(self.forgot_password_button)
        self.ui.PB_UserManager.clicked.connect(self.manage_users_button)
        self.ui.PB_PatientManager.clicked.connect(self.manage_patients_button)
        self.ui.show()

    def login_button(self):
        """
        Method to validate a user name and password to allow a user to login

        """
        # Get the fields from the text boxes
        user_login = self.ui.TB_Username.text()
        password = self.ui.TB_Password.text()

        # Create the column_names, entries, and entry_types lists
        column_names = ["user_login", "password"]
        entries = [user_login, password]
        entry_types = [str, str]

        # If the user_login and password is valid
        if self.table.validate_entry(column_names, entries, entry_types):
            self.ui.close()
            log.info("Connecting to DCM serial reader")
            CON_SCREEN.con_screen(self.tables_dict)
            return
        else:
            log.info("Incorrect login")

    def manage_users_button(self):
        """
        Method to open the login as admin screen before opening the user manager

        """
        specific_login(self.tables_dict, "admin")
        self.ui.close()

    def manage_patients_button(self):
        """
        Method to open the login as a doctor before opening the patient manager

        """
        specific_login(self.tables_dict, "doctor")
        self.ui.close()

    def forgot_password_button(self):
        """
        Method to open the forgot password screen

        """
        specific_login(self.tables_dict, "forgot_password")
        self.ui.close()
