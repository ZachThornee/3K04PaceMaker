import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import user_manager_screen as USER_MANAGER

# Global Variables
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class add_user_screen(QMainWindow):
    def __init__(self, database, users_table):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_AddUser.ui'),self)
        self.ui.show()
        self.database = database
        self.users_table = users_table
        self.ui.PB_Confirm.clicked.connect(self.add_new_user)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)

    def add_new_user(self):
        user_dictionary = self.users_table.get_table_dictionary()
        new_user = user_dictionary[0]

        try:
            valid_num = abs(int(self.ui.TB_ID.text()))
            new_user['employee_number'] = str(valid_num)
        except ValueError:
            log.warning("Invalid user input")
            new_user['employee_number'] = str(len(user_dictionary) + 1)

        for user in user_dictionary.values():
            if user['employee_number'] == new_user['employee_number']:
                log.warning("Invalid input -> same employee number")


        new_user['first_name'] = "'{0}'".format(self.ui.TB_FirstName.text())
        new_user['last_name'] = "'{0}'".format(self.ui.TB_LastName.text())
        new_user['password'] = "'{0}'".format(self.ui.TB_Password.text())
        new_user['user_login'] = "'{0}'".format(self.ui.TB_UserLogin.text())
        new_user['email'] = "'{0}'".format(self.ui.TB_Email.text())

        if self.CB_Admin.isChecked():
            new_user['admin_priveleges'] = True
        else:
            new_user['admin_priveleges'] = False

        new_user_list = []
        for value in new_user.values():
            new_user_list.append(str(value))

        self.users_table.add_row(new_user_list)
        self.return_to_user_manager()

    def return_to_user_manager(self):
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.database, self.users_table)

