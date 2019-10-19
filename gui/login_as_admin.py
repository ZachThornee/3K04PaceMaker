import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER


class login_as_admin(QMainWindow):
    def __init__(self, database, table, home_screen):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_LoginAsAdmin.ui'), self)
        log.info("Showing admin login screen")
        self.ui.show()
        self.database = database
        self.table = table
        self.home_screen = home_screen
        self.PB_UserManager.clicked.connect(self.return_to_login_screen)
        self.PB_Confirm.clicked.connect(self.validate_admin)
        self.ui.show()

    def validate_admin(self):
        inputted_username = self.TB_Username.text().strip()
        inputted_password = self.TB_Password.text().strip()

        user_dictionary = self.table.get_table_dictionary()
        for user in user_dictionary.values():
            if (inputted_username == user['user_login'] and
               inputted_password == user['password'] and
               user['admin_priveleges'] is True):
                self.ui.close()
                USER_MANAGER.user_manager_screen(self.database, self.table)
                return
        else:
            log.info("Incorrect login or insufficient priveleges")

    def return_to_login_screen(self):
        self.home_screen.ui.show()
        self.ui.close()
