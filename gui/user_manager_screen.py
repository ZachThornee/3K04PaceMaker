import logging as log
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import login_screen as LOGIN

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
        self.ui.show()

    def validate_admin(self):
        #TODO get text and check if user has admin priveleges
        self.ui.close()

    def return_to_login_screen(self):
        LOGIN.login_screen()
        self.ui.close()


