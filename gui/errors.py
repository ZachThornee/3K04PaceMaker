import logging as log
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import login_screen as LOGIN_SCREEN
import user_manager_screen as USER_MANAGER


class maximum_number_of_users(QWidget):

    def __init__(self, tables_dict, user_manager):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_MaxUsers.ui'), self)
        log.warning("Maximum number of users exceeded. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.user_manager = user_manager
        self.ui.PB_Login.clicked.connect(self.return_to_login_screen)
        self.ui.PB_ManageUsers.clicked.connect(self.return_to_user_manager)
        self.ui.show()

    def return_to_user_manager(self):
        self.ui.close()

    def return_to_login_screen(self):
        self.ui.close()
        self.user_manager.ui.close()
        LOGIN_SCREEN.login_screen(self.tables_dict)


class invalid_input(QWidget):

    def __init__(self, tables_dict, add_user_screen):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_InvalidInput.ui'), self)
        log.warning("Invalid input. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen
        self.ui.PB_AddUser.clicked.connect(self.return_to_add_user)
        self.ui.PB_UserManager.clicked.connect(self.return_to_user_manager)
        self.ui.show()

    def return_to_add_user(self):
        self.ui.close()

    def return_to_user_manager(self):
        self.ui.close()
        self.add_user_screen.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)



class employee_number_already_used(QWidget):

    def __init__(self, tables_dict, add_user_screen):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_ProfileExists.ui'), self)
        log.warning("Employee number already exists. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen
        self.ui.PB_AddUser.clicked.connect(self.return_to_add_user)
        self.ui.PB_UserManager.clicked.connect(self.return_to_user_manager)
        self.ui.show()

    def return_to_add_user(self):
        self.ui.close()

    def return_to_user_manager(self):
        self.ui.close()
        self.add_user_screen.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)

