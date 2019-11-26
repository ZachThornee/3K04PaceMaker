import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import management_screen as MANAGER
import initial_login as LOGIN_SCREEN


class maximum_number_of_users(QMainWindow):

    def __init__(self, tables_dict, user_manager):
        """
        Constructor for maximum number of users error screen

        :param tables_dict dictionary: dictionary containg all tables
        :param user_manager class user_manager_screen: instance of user_manager_screen class
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Options.ui'), self)
        log.warning("Maximum number of users exceeded. Showing popup")
        self.ui.LAB_ErrorTitle.setText("Maximum Users Exceeded")
        error_string = "The maximum number of users has been exceeded. What would you like to do?"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to user manager")
        self.ui.PB_Option2.setText("Return to login screen")
        self.ui.show()
        self.tables_dict = tables_dict
        self.user_manager = user_manager

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_user_manager)
        self.ui.PB_Option2.clicked.connect(self.return_to_login_screen)

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

    def __init__(self, tables_dict, add_user_screen, management_type):
        """
        Constructor for invalid input error screen

        :param tables_dict dictionary: dictionary contain all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Options.ui'), self)
        log.warning("Invalid input. Showing popup")
        self.ui.LAB_ErrorTitle.setText("Invalid input")
        error_string = "Invalid input user input"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to form")
        self.ui.PB_Option2.setText("Return to user manager")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen
        self.management_type = management_type

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_form)
        self.ui.PB_Option2.clicked.connect(self.return_to_user_manager)

    def return_to_form(self):
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
        MANAGER.manager(self.tables_dict, self.management_type)


class employee_number_already_used(QMainWindow):

    def __init__(self, tables_dict, add_user_screen, management_type,):
        """
        Constructor for employee number alrady in use error

        :param tables_dict dictionary: dictionary containing all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_2_Options.ui'), self)
        log.warning("Employee number already exists. Showing popup")
        self.ui.LAB_ErrorTitle.setText("Employee Number Already Used")
        error_string = "The employee number has already been used. What would you like to do?"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to form")
        self.ui.PB_Option2.setText("Return to user manager")
        self.ui.show()
        self.tables_dict = tables_dict
        self.add_user_screen = add_user_screen
        self.management_type = management_type

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_form)
        self.ui.PB_Option2.clicked.connect(self.return_to_user_manager)

    def return_to_form(self):
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
        MANAGER.manager(self.tables_dict, self.management_type)


class connection_error(QMainWindow):

    def __init__(self, tables_dict, connecting_screen):
        """
        Constructor for employee number alrady in use error

        :param tables_dict dictionary: dictionary containing all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_1_Option.ui'), self)
        log.warning("Connection error")
        self.ui.LAB_ErrorTitle.setText("Connection Error")
        error_string = "There has been a connection error what would you like to do?"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to connection screen")
        self.ui.show()
        self.ui.show()
        self.tables_dict = tables_dict
        self.connecting_screen = connecting_screen

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_connecting_screen)

    def return_to_connecting_screen(self):
        """
        Method to return to the add user screen

        """
        self.ui.close()


class privelege_error(QMainWindow):

    def __init__(self, tables_dict, previous_screen):
        """
        Constructor for employee number alrady in use error

        :param tables_dict dictionary: dictionary containing all tables
        :param previous_screen class mangement_screen: previous screen from which the privelge error was caused
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_1_Option.ui'), self)
        log.warning("Privelege error")
        self.ui.LAB_ErrorTitle.setText("Privelege Error")
        error_string = "Unable to change privelges as this user is the only admin"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to previous screen")
        self.ui.show()
        self.ui.show()
        self.tables_dict = tables_dict
        self.previous_screen = previous_screen

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_previous_screen)

    def return_to_previous_screen(self):
        """
        Method to return to the add user screen

        """
        self.ui.close()


class incorrect_login(QMainWindow):

    def __init__(self, tables_dict, add_user_screen, management_type):
        """
        Constructor for invalid input error screen

        :param tables_dict dictionary: dictionary contain all tables
        :param add_user_screen class add_user_screen: add_user_screen object
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_Error_1_Options.ui'), self)
        log.warning("Invalid input. Showing popup")
        self.ui.LAB_ErrorTitle.setText("Invalid input")
        error_string = "Invalid input user input"
        self.ui.LAB_ErrorMessage.setText(error_string)
        self.ui.PB_Option1.setText("Return to previous screen")
        self.ui.show()
        self.tables_dict = tables_dict

        # Buttons
        self.ui.PB_Option1.clicked.connect(self.return_to_prev)

    def return_to_prev(self):
        """
        Method to return to the previous screen

        """
        self.ui.close()
