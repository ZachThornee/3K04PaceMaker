import logging as log
import random
import sys

import psycopg2
from PyQt5.QtWidgets import *
from app.login_screen import Ui_Login
from PyQt5 import QtWidgets
from database_management import db_manager
from database_management import table

# Global configuration
DATABASE_NAME = "3K04_Database"
USER = "jeff"
LOGINS_TABLE = "user_logins"
INFO_ARRAY = [
                ["EMPLOYEE_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["USER_LOGIN", "TEXT", "NOT", "NULL"],
                ["PASSWORD", "TEXT",  "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT", "NOT", "NULL"],
                ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"]
            ]
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class login_screen(Ui_Login):

    def __init__(self, dialog):
        Ui_Login.__init__(self)
        self.setupUi(dialog)
        self.title = 'Protect your heart'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.PB_Confirm.clicked.connect(self.validate_user)
        self.PB_ForgotPassword.clicked.connect(self.send_email)
        self.PB_UserManager.clicked.connect(self.manage_users_window)
        self.database = db_manager(USER, DATABASE_NAME, INFO_ARRAY)
        self.logins_table = self.database.connect_to_table(LOGINS_TABLE)


    def validate_user(self):

        username = self.TB_Username.text()
        password = self.TB_Password.text()
        user_list = self.logins_table.get_rows()
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

    def manage_users_window(self):
        print("connected to window")

    def send_email(self):
        pass

if __name__ == "__main__":
    APP = QApplication([])
    dialog = QtWidgets.QDialog()
    prog = login_screen(dialog)
    dialog.show()
    sys.exit(APP.exec_())
