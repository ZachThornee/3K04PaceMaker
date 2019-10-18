import logging as log
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import user_manager_screen as USER_MANAGER
import login_screen as LOGIN_SCREEN

# Global Variables

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class maximum_number_of_users(QWidget):
    def __init__(self, database, table, user_manager):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_MaxUsers.ui'),self)
        self.ui.show()
        self.database = database
        self.table = table
        self.user_manager = user_manager
        self.ui.show()
        self.ui.PB_Login.clicked.connect(self.return_to_login_screen)
        self.ui.PB_ManageUsers.clicked.connect(self.return_to_user_manager)

    def return_to_user_manager(self):
        self.ui.close()

    def return_to_login_screen(self):
        self.ui.close()
        self.user_manager.ui.close()
        LOGIN_SCREEN.login_screen()

