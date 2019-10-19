import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import login_screen as LOGIN
import add_user_screen as ADD_USER
import errors as ERRORS


class user_manager_screen(QMainWindow):
    def __init__(self, database, table):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_UserManager.ui'), self)
        self.database = database
        self.table = table
        self.PB_Back.clicked.connect(self.return_to_login_screen)
        self.PB_AddUser.clicked.connect(self.add_user)
        self.populate_table()

    def populate_table(self):
        user_dictionary = self.table.get_table_dictionary()
        self.columns = self.table.get_columns()
        self.rows = self.table.get_rows()
        self.ui.TAB_Users.setColumnCount(len(self.columns))
        self.ui.TAB_Users.setHorizontalHeaderLabels(self.columns)
        self.ui.TAB_Users.setRowCount(len(user_dictionary))

        for i in range(len(self.rows)):
            for j in range(len(self.columns)):
                self.ui.TAB_Users.setItem(
                        i, j, QTableWidgetItem(str(self.rows[i][j])))

        self.ui.show()

    def add_user(self):
        user_dictionary = self.table.get_table_dictionary()
        print(len(user_dictionary))
        if len(user_dictionary) >= 10:
            ERRORS.maximum_number_of_users(self.database, self.table, self)
        else:
            self.ui.close()
            ADD_USER.add_user_screen(self.database, self.table)

    def return_to_login_screen(self):
        LOGIN.login_screen()
        self.ui.close()
