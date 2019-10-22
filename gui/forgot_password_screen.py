import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class forgot_pass_scrn(QMainWindow):
    def __init__(self, tables_dict, login_screen):
        """
        Constructor for forgot password screen

        :param tables_dict dictionary: dictionary containg all tables
        :param login_screen class login_screen: login_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_ForgotPassword.ui'), self)
        log.info("Showing forgot password screen")
        self.ui.show()
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']
        self.login_screen = login_screen
        self.PB_Enter.clicked.connect(self.validate_email)
        self.PB_Return.clicked.connect(self.return_to_login_screen)

    def validate_email(self):
        """
        Method to validate a user's email address and email a new password

        """
        #TODO Add the email verification and password sending
        self.ui.close()
        inputted_email = self.ui.TB_Email.text()
        inputted_user_login = self.ui.TB_Username.text()
        user_dict = self.table.get_table_dict()

        for user in user_dict.values():
            if (user['email'] == inputted_email and
               user['user_login'] == inputted_user_login):
                log.info("Email is valid sending email")
                self.return_to_login_screen()

    def return_to_login_screen(self):
        """
        Method to return to login screen

        """
        self.ui.close()
        self.login_screen.ui.show()
