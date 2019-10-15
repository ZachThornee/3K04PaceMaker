import logging as log
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import user_manager_screen as USER_MANAGER

# Global Variables

log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class login_as_admin(QMainWindow):
    def __init__(self, database, table, home_screen):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_LoginAsAdmin.ui'),self)
        self.ui.show()
        self.database = database
        self.table = table
        self.home_screen = home_screen
        self.current_user = None
        self.PB_UserManager.clicked.connect(self.return_to_login_screen)
        self.PB_Confirm.clicked.connect(self.validate_admin)
        self.ui.show()

    def validate_admin(self):
        #TODO get text and check if user has admin priveleges
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.database, self.table, self.current_user)


    def return_to_login_screen(self):
        self.home_screen.ui.show()
        self.ui.close()


