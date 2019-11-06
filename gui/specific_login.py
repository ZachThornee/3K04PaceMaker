import logging as log

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

import management_screen as MANAGER
import initial_login as LOGIN


class specific_login(QMainWindow):

    def __init__(self, tables_dict, login_type):
        """
        Constructor for login as admin screen

        :param tables_dict dictionary: dictionary containing all tables
        :param login_type string: a string specifying the login type
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_SpecificLogin.ui'), self)

        self.login_type = login_type
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']

        # Set the font size
        font = QtGui.QFont()
        font.setPointSize(26)
        self.LAB_Title.setFont(font)

        # Create the appropriate login screen
        if self.login_type == "admin":
            self.ui.LAB_Title.setText("Login as Admin")
            log.info("Showing admin login screen")

        elif self.login_type == "doctor":
            self.ui.LAB_Title.setText("Login as Doctor")
            log.info("Showing doctor login screen")

        elif self.login_type == "forgot_password":
            self.ui.LAB_Title.setText("Forgot Password")
            log.info("Showing forgot password screen")

        # Buttons
        self.PB_GeneralLogin.clicked.connect(self.return_to_login_screen)
        self.PB_Confirm.clicked.connect(self.validate_login)
        if self.login_type == "forgot_password":
            self.PB_Confirm.clicked.connect(self.validate_email)

        # Show ui
        self.ui.show()

    def validate_login(self):
        """
        Method to validate a user login for both regular and admin

        """\
        # Get values from text fields
        username = self.ui.TB_Field_1.text().strip()
        password = self.ui.TB_Field_2.text().strip()

        # Create the column_names, entries, and entry_types lists
        column_names = ["user_login", "password"]
        entries = [username, password]
        entry_types = [str, str]

        # If the required login is admin
        if self.login_type == "admin":
            column_names.append("admin_priveleges")
            entries.append(True)
            entry_types.append(bool)

        # If the username and password are valid
        if self.table.validate_entry(column_names, entries, entry_types):
            self.ui.close()
            if self.login_type == "admin":
                MANAGER.manager(self.tables_dict, "users")
            elif self.login_type == "doctor":
                MANAGER.manager(self.tables_dict, "patients")

            return
        else:
            log.info("Incorrect login or insufficient priveleges")

    def validate_email(self):
        """
        Method to validate a user's email address and email a new password

        """
        self.ui.close()
        # Get all the fields from the text boxes
        email = self.ui.TB_Email.text()
        user_login = self.ui.TB_Username.text()

        # Create the column_names, entries, and entry_types lists
        column_names = ["email", "user_login"]
        entries = [email, user_login]
        entry_types = [str, str]

        # If the entries are valid
        if self.table.validate_entry(column_names, entries, entry_types):
            log.info("Email is valid sending email")
            self.return_to_login_screen()

    def return_to_login_screen(self):
        """
        Method to return to login screen

        """
        self.ui.close()
        LOGIN.login_screen(self.tables_dict)


