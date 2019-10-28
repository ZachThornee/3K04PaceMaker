import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import connecting_screen as CON_SCREEN
import forgot_password_screen as FORGT_PASS
import login_as_admin as LOGIN_ADMIN


class login_screen(QMainWindow):
    def __init__(self, tables_dict):
        """
        Constructor for the initial doctor login screen

        :param tables_dict dictionary: A dictionary containing all tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Login.ui'), self)
        log.info("Showing main login screen")
        self.tables_dict = tables_dict
        self.ui.PB_Confirm.clicked.connect(self.login_button)
        self.ui.PB_ForgotPassword.clicked.connect(self.forgot_password_button)
        self.ui.PB_UserManager.clicked.connect(self.manage_users_button)
        self.ui.show()

    def login_button(self):
        """
        Method to validate a user name and password to allow a user to login

        """
        inputted_username = self.ui.TB_Username.text()
        inputted_password = self.ui.TB_Password.text()

        user_dict = self.tables_dict['users_table'].get_table_dict()

        for user in user_dict.values():
            if (inputted_username == user['user_login'] and
               inputted_password == user['password']):
                # If we have the correct password, username, allow connecting
                self.ui.close()
                log.info("Connecting to DCM serial reader")
                CON_SCREEN.con_screen(self.tables_dict, self)
                return
        else:
            log.info("Incorrect login")

    def manage_users_button(self):
        """
        Method to open the login as admin screen before opening the user manager

        """
        LOGIN_ADMIN.login_as_admin(self.tables_dict, self)
        self.ui.close()

    def forgot_password_button(self):
        """
        Method to open the forgot password screen

        """
        FORGT_PASS.forgot_pass_scrn(self.tables_dict, self)
        self.ui.close()
