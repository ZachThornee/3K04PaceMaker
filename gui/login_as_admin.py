import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER


class login_as_admin(QMainWindow):
    def __init__(self, tables_dict, login_screen):
        """
        Constructor for login as admin screen

        :param tables_dict dictionary: dictionary containing all tables
        :param login_screen class login_screen: login_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_LoginAsAdmin.ui'), self)
        log.info("Showing admin login screen")
        self.ui.show()
        self.login_screen = login_screen
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']
        self.PB_UserManager.clicked.connect(self.return_to_login_screen)
        self.PB_Confirm.clicked.connect(self.validate_admin)
        self.ui.show()

    def validate_admin(self):
        """
        Method to validate that a user is admin to allow access to user manager screen

        """\
        # Get values from text fields
        username = self.TB_Username.text().strip()
        password = self.TB_Password.text().strip()

        # Create the column_names, entries, and entry_types lists
        column_names = ["user_login", "password"]
        entries = [username, password]
        entry_types = [str, str]

        # If the username and password are valid
        if self.table.validate_entry(column_names, entries, entry_types):
            self.ui.close()
            USER_MANAGER.user_manager_screen(self.tables_dict)
            return
        else:
            log.info("Incorrect login or insufficient priveleges")

    def return_to_login_screen(self):
        """
        Method to return to login screen

        """
        self.ui.close()
        self.login_screen.ui.show()
