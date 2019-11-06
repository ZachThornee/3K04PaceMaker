import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from management_screen import manager


class maximum_number_of_users(QMainWindow):

    def __init__(self, tables_dict, user_manager):
        """
        Constructor for maximum number of users error screen

        :param tables_dict dictionary: dictionary containg all tables
        :param user_manager class user_manager_screen: instance of user_manager_screen class
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Option.ui'), self)
        log.warning("Maximum number of users exceeded. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.user_manager = user_manager

        # Buttons
        self.ui.PB_Login.clicked.connect(self.return_to_login_screen)
        self.ui.PB_ManageUsers.clicked.connect(self.return_to_user_manager)

    def return_to_user_manager(self):
        """
        Method to return to user manager screen

        """
        self.ui.close()

    def return_to_login_screen(self):
        """
        Method to return to login screen and restart the application

        """
        self.ui.close()
        self.user_manager.ui.close()
        LOGIN_SCREEN.login_screen(self.tables_dict)


class invalid_input(QMainWindow):

    def __init__(self, tables_dict, add_user_screen):
        """
        Constructor for invalid input erro screen

        :param tables_dict dictionary: dictionary contain all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Options.ui'), self)
        log.warning("Invalid input. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen

        # Buttons
        self.ui.PB_AddUser.clicked.connect(self.return_to_add_user)
        self.ui.PB_UserManager.clicked.connect(self.return_to_user_manager)

    def return_to_add_user(self):
        """
        Method to return to the add user screen

        """
        self.ui.close()

    def return_to_user_manager(self):
        """
        Method to return to the user manager

        """
        self.ui.close()
        self.add_user_screen.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)


class employee_number_already_used(QMainWindow):

    def __init__(self, tables_dict, add_user_screen):
        """
        Constructor for employee number alrady in use error

        :param tables_dict dictionary: dictionary containing all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Options.ui'), self)
        log.warning("Employee number already exists. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen

        # Buttons
        self.ui.PB_AddUser.clicked.connect(self.return_to_add_user)
        self.ui.PB_UserManager.clicked.connect(self.return_to_user_manager)

    def return_to_add_user(self):
        """
        Method to return to the add user screen

        """
        self.ui.close()

    def return_to_user_manager(self):
        """
        Method to return to the user_manager_screen

        """
        self.ui.close()
        self.add_user_screen.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)


class connection_error(QMainWindow):

    def __init__(self, tables_dict, connecting_screen):
        """
        Constructor for employee number alrady in use error

        :param tables_dict dictionary: dictionary containing all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_1_Option.ui'), self)
        log.warning("Employee number already exists. Showing popup")
        self.ui.show()
        self.tables_dict = tables_dict
        self.connecting_screen = connecting_screen

        # Buttons
        self.ui.PB_TryAgain.clicked.connect(self.return_to_connecting_screen)

    def return_to_connecting_screen(self):
        """
        Method to return to the add user screen

        """
        self.ui.close()
