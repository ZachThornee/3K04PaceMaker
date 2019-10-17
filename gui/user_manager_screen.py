import logging as log
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import login_screen as LOGIN
import add_user_screen as ADD_USER

# Global Variables

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class user_manager_screen(QMainWindow):
    def __init__(self, database, table, current_user):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_UserManager.ui'),self)
        self.ui.show()
        self.database = database
        self.table = table
        self.current_user = current_user
        self.PB_Back.clicked.connect(self.return_to_login_screen)
        self.PB_AddUser.clicked.connect(self.add_user)
        self.populate_table()
        self.ui.show()

    def populate_table(self):
        user_dictionary = self.table.get_table_dictionary()
        pass

    def add_user(self):
        if len(self.table.get_table_dictionary()) > 10:
            error = uic.load("ui_files/UF_Error_MaxUsers.ui")
            error.show()
        else:
            self.ui.close()
            ADD_USER.add_user_screen(self.database, self.table, self)

    def return_to_login_screen(self):
        LOGIN.login_screen()
        self.ui.close()


