import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import add_user_screen as ADD_USER
import edit_user_screen as EDIT_USER
import errors as ERRORS
import login_screen as LOGIN


class user_manager_screen(QMainWindow):

    def __init__(self, tables_dict):
        """
        Constructor for user manager screen

        :param tables_dict dictionary: A dictionary containing all tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_UserManager.ui'), self)
        self.tables_dict = tables_dict
        self.table = tables_dict['users_table']

        # Buttons
        self.PB_Back.clicked.connect(self.return_to_login_screen)
        self.PB_AddUser.clicked.connect(self.add_user_button)
        self.PB_EditUser.clicked.connect(self.edit_user_button)
        self.PB_DeleteUser.clicked.connect(self.delete_user_button)

        self.update_table()

    def update_table(self):
        """
        Method to update the QWidgetTable
        """
        self.table.populate(self.ui.TAB_Users)
        self.ui.show()

    def add_user_button(self):
        """
        Method to validate user count and if valid open add user screen

        """
        if not self.table.check_max_user(10):
            ERRORS.maximum_number_of_users(self.tables_dict, self)
        else:
            self.ui.close()
            ADD_USER.add_user_screen(self.tables_dict)

    def edit_user_button(self):
        """
        Method to open the edit user screen and to update with user information

        """

        if len(self.ui.TAB_Users.selectedRanges()) == 0:
            log.error("No user selected")
            return False

        selected = self.ui.TAB_Users.selectedRanges()[0]
        row_number = selected.topRow()
        self.ui.close()
        EDIT_USER.edit_user_screen(self.tables_dict, row_number)

    def delete_user_button(self):
        """
        Method to delete a user in the table

        """

        if len(self.ui.TAB_Users.selectedRanges()) == 0:
            log.error("No user selected")
            return False

        selected = self.ui.TAB_Users.selectedRanges()[0]
        row_number = selected.topRow()
        employee_number = self.table.get_value(row_number, "employee_number")

        # Delete the row with the corresponding employee number
        self.table.delete_row(employee_number)
        self.ui.close()
        self.update_table()

    def return_to_login_screen(self):
        """
        Method to return to the login screen

        """
        LOGIN.login_screen(self.tables_dict)
        self.ui.close()
