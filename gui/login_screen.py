import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import connecting_screen as CON_SCREEN
import forgot_password_screen as FORGT_PASS
import login_as_admin as LOGIN_ADMIN


class login_screen(QMainWindow):
    def __init__(self, tables_dict):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Login.ui'), self)
        log.info("Showing main login screen")
        self.ui.show()
        self.title = 'Protect your heart'
        self.tables_dict = tables_dict
        self.PB_Confirm.clicked.connect(self.login_button)
        self.PB_ForgotPassword.clicked.connect(self.forgot_password_button)
        self.PB_UserManager.clicked.connect(self.manage_users_button)
        self.ui.show()

    def login_button(self):
        inputted_username = self.ui.TB_Username.text()
        inputted_password = self.ui.TB_Password.text()

        user_dict = self.tables_dict['users_table'].get_table_dict()
        print(user_dict)

        for user in user_dict.values():
            if (inputted_username == user['user_login'] and
               inputted_password == user['password']):
                # If we have the correct password, username, allow connecting
                self.ui.close()
                log.info("Connecting to DCM serial reader")
                CON_SCREEN.con_screen(self.tables_dict, self)
                return
        else:
            log.info("Incorrect login")

    def manage_users_button(self):
        LOGIN_ADMIN.login_as_admin(self.tables_dict, self)
        self.ui.close()

    def forgot_password_button(self):
        FORGT_PASS.forgot_pass_scrn(self.tables_dict, self)
        self.ui.close()
