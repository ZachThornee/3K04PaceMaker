import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER
import errors as ERRORS


class add_user_screen(QMainWindow):

    def __init__(self, tables_dict):
        """
        Initialization call for add user screen

        :param tables_dict 2D_dictionary: contains both the user and patient tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_AddUser.ui'), self)
        log.info("Adding new user")
        self.ui.show()
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']  # Get the users table
        self.ui.PB_Confirm.clicked.connect(self.add_new_user)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)

    def add_new_user(self):
        """
        Method to add a new user when add user button is clicked

        """
        employee_num = self.ui.TB_EmployeeID.text()
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        password = self.ui.TB_Password.text()
        user_login = self.ui.TB_UserLogin.text()
        email = self.ui.TB_Email.text()

        # Ensure that the employee number is unique
        unique = self.table.check_unique("employee_number", employee_num, int)
        if not unique:
            ERRORS.employee_number_already_used(self.tables_dict, self)
        elif unique:
            self.table.change_data("employee_num", employee_num, int)

        # Change the data in the table
        self.table.change_data("first_name", first_name, str)
        self.table.change_data("last_name",  last_name,  str)
        self.table.change_data("password",   password,   str)
        self.table.change_data("user_login", user_login, str)
        self.table.change_data("email",      email,      str)

        # Get the value of the checkbox
        if self.CB_Admin.isChecked():  # If check box is ticked
            admin_priveleges = True
        else:
            admin_priveleges = False

        self.table.change_data("admin_priveleges", admin_priveleges, bool)
        self.table.add_row()  # Call table method to add new row
        self.return_to_user_manager()

    def return_to_user_manager(self):
        """
        Method to return to user manager screen

        """
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)
