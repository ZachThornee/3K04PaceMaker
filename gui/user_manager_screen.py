import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QTableWidget

import add_user_screen as ADD_USER
import edit_user_screen as EDIT_USER
import errors as ERRORS
import login_screen as LOGIN


class user_manager_screen(QMainWindow):

    max_users = 10

    def __init__(self, tables_dict):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_UserManager.ui'), self)
        self.tables_dict = tables_dict
        self.table = tables_dict['users_table']
        self.user_dict = self.table.get_table_dict()
        self.PB_Back.clicked.connect(self.return_to_login_screen)
        self.PB_AddUser.clicked.connect(self.add_user)
        self.PB_EditUser.clicked.connect(self.edit_user)
        self.populate_table()

    def populate_table(self):
        self.columns = self.table.get_columns()
        self.rows = self.table.get_rows()
        self.ui.TAB_Users.setColumnCount(len(self.columns))
        self.ui.TAB_Users.setHorizontalHeaderLabels(self.columns)
        self.ui.TAB_Users.setRowCount(len(self.user_dict))

        for i in range(len(self.rows)):
            for j in range(len(self.columns)):
                self.ui.TAB_Users.setItem(
                        i, j, QTableWidgetItem(str(self.rows[i][j])))

        self.ui.show()

    def add_user(self):

        if len(self.user_dict) >= self.max_users:
            ERRORS.maximum_number_of_users(self.tables_dict, self)
        else:
            self.ui.close()
            ADD_USER.add_user_screen(self.tables_dict)

    def edit_user(self):

        if len(self.ui.TAB_Users.selectedRanges()) == 0:
            log.error("No user selected")
            return False

        selected = self.ui.TAB_Users.selectedRanges()[0]

        if selected.rowCount() > 1:
            log.error("Too many users selected")
        else:
            row_number = selected.topRow()
            user_to_edit = self.user_dict[row_number]
            self.ui.close()
            EDIT_USER.edit_user_screen(self.tables_dict, user_to_edit)

    def return_to_login_screen(self):
        LOGIN.login_screen(self.tables_dict)
        self.ui.close()
