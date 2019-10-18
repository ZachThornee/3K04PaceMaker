import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import serial
import home_screen as HOME

# Global Variables
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class forgot_password_screen(QMainWindow):
    def __init__(self, database, logins_table, home_screen):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_ForgotPassword.ui'),self)
        self.ui.show()
        self.database = database
        self.home_screen = home_screen
        self.logins_table = logins_table
        self.PB_Enter.clicked.connect(self.check_login)
        self.PB_Return.clicked.connect(self.return_to_login_screen)

    def check_login(self):
        self.ui.close()
        inputted_email = self.ui.TB_Email.text()
        inputted_user_login = self.ui.TB_Username.text()
        user_dictionary = self.logins_table.get_table_dictionary()

        for user in user_dictionary.values():
            if user['email'] == inputted_email and user['user_login'] == inputted_user_login:
                log.info("Email is valid sending email")
                self.return_to_login_screen()

    def return_to_login_screen(self):
        self.ui.close()
        self.home_screen.ui.show()

