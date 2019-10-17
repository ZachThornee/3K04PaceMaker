import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import database_management as DBM
import connecting_screen as CONNECTING
import forgot_password_screen as FORGOT_PASSWORD
import login_as_admin as LOGIN_ADMIN

# Global configuration
DATABASE_NAME = "3K04_Database"
USER = "jeff"
LOGINS_TABLE = "user_logins"
LOGINS_TABLE_PARAMETERS = [
                ["EMPLOYEE_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["USER_LOGIN", "TEXT", "NOT", "NULL"],
                ["PASSWORD", "TEXT",  "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT", "NOT", "NULL"],
                ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"]
            ]
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class login_screen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Login.ui'),self)
        self.ui.show()
        self.title = 'Protect your heart'
        self.PB_Confirm.clicked.connect(self.login_button)
        self.PB_ForgotPassword.clicked.connect(self.forgot_password_button)
        self.PB_UserManager.clicked.connect(self.manage_users_button)
        self.database = DBM.db_manager(USER, DATABASE_NAME)
        self.logins_table = self.database.connect_to_table(LOGINS_TABLE, LOGINS_TABLE_PARAMETERS)
        self.ui.show()

    def login_button(self):
        inputted_username = self.lineEdit.text()
        inputted_password = self.lineEdit_2.text()
        user_dictionary = self.logins_table.get_table_dictionary()

        for user in user_dictionary.values():
            if inputted_username == user['user_login'] and inputted_password == user['password']:
                # If we have the correct password, username, allow connecting
                self.ui.close()
                log.info("Connecting to DCM serial reader")
                CONNECTING.connecting_screen(self.database, user)
                return
        else:
            log.info("Incorrect login")

    def manage_users_button(self):
        LOGIN_ADMIN.login_as_admin(self.database, self.logins_table, self)
        self.ui.close()

    def forgot_password_button(self):
        FORGOT_PASSWORD.forgot_password_screen(self.database, self.logins_table, self)
        self.ui.close()

if __name__ == "__main__":
    APP = QApplication([])
    window  = login_screen()
    sys.exit(APP.exec_())
