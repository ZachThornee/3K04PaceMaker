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
                ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"]
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
        username = self.ui.TB_Username.toPlainText()
        password = self.ui.TB_Password.toPlainText()
        user_list = self.logins_table.get_rows()
        current_user=None
        log.info("Connecting to DCM serial reader")
        CONNECTING.connecting_screen(self.database, current_user)
        self.ui.close()
        for user in user_list:
            username_bool = False
            password_bool = False
            current_user = None
            for info in user:
                if info == username:
                    username_bool = True
                if info == password:
                    password_bool = True
            if password_bool and username_bool:
                current_user = user
                break
        if current_user is not None:
            log.info("Connecting to DCM serial reader")
            self.ui.close()

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
