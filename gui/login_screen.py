import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import database_management as DBM
import con_screen as CON_SCREEN
import forgot_pass_scrn as FORGT_PASS
import login_as_admin as LOGIN_ADMIN


class login_screen(QMainWindow):
    def __init__(self, db_user, db_name, table_name, table_dict):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Login.ui'), self)
        log.info("Showing main login screen")
        self.ui.show()
        self.title = 'Protect your heart'
        self.table_dict = table_dict
        self.PB_Confirm.clicked.connect(self.login_button)
        self.PB_ForgotPassword.clicked.connect(self.forgot_password_button)
        self.PB_UserManager.clicked.connect(self.manage_users_button)
        self.db = DBM.db_manager(db_user, db_name)
        self.table = self.db.con_table(table_name, table_dict[table_name])
        self.ui.show()

    def login_button(self):
        inputted_username = self.ui.TB_Username.text()
        inputted_password = self.ui.TB_Password.text()
        user_dict = self.table.get_table_dict()

        for user in user_dict.values():
            if (inputted_username == user['user_login'] and
               inputted_password == user['password']):
                # If we have the correct password, username, allow connecting
                self.ui.close()
                log.info("Connecting to DCM serial reader")
                CON_SCREEN.con_screen(self.db, user, self.table_dict, self)
                return
        else:
            log.info("Incorrect login")

    def manage_users_button(self):
        LOGIN_ADMIN.login_as_admin(self.db, self.table, self)
        self.ui.close()

    def forgot_password_button(self):
        FORGT_PASS.forgot_pass_scrn(self.db, self.table, self.table_dict, self)
        self.ui.close()
