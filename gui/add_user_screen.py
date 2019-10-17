import logging as log
import random
import sys
import time

import psycopg2
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *

# Global Variables
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class add_user_screen(QMainWindow):
    def __init__(self, database, users_table, user_manager):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_AddUser.ui'),self)
        self.ui.show()
        self.database = database
        self.user_manager = user_manager
        self.users_table = users_table
        self.PB_Confirm.clicked.connect(self.add_new_user)

    def add_new_user(self):
        user_dictionary = self.users_table.get_table_dictionary()
        new_user = user_dictionary[0]

        #TODO implement checks to make sure that these values don't conflict
        new_user['employee_number'] = self.TB_ID.text()
        new_user['first_name'] = "'{0}'".format(self.TB_FirstName.text())
        new_user['last_name'] = "'{0}'".format(self.TB_LastName.text())
        new_user['admin_priveleges'] = self.TB_Admin.text()
        new_user['password'] = "'{0}'".format(self.TB_Password.text())
        new_user['user_login'] = "'{0}'".format(self.TB_UserLogin.text())
        new_user['email'] = "'{0}'".format(self.TB_Email.text())

        new_user_list = []
        for value in new_user.values():
            new_user_list.append(str(value))

        self.users_table.add_row(new_user_list)

        self.ui.close()

    def return_to_user_manager(self):
        self.ui.close()
        self.user_manager.ui.show()

