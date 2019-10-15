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
        self.PB_Back.clicked.connect(self.return_to_login_screen)

    def check_login(self):
        self.ui.close()
        pass
        #TODO get the email text and compare it against the database
        #TODO if email is valid create a new password and send it to the user

    def return_to_login_screen(self):
        self.ui.close()
        self.home_screen.ui.show()

