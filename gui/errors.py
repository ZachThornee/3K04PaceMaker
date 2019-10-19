import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import login_screen as LOGIN_SCREEN


class maximum_number_of_users(QWidget):

    def __init__(self, database, table, user_manager):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_MaxUsers.ui'), self)
        log.warning("Maximum number of users exceeded. Showing popup")
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
