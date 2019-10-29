import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER
import errors as ERRORS


class edit_user_screen(QMainWindow):
    def __init__(self, tables_dict, row_number):
        """
        Constructor for edit user screen

        :param tables_dict dict: A dictionary containing all tables used in application
        :param row_number int: The current row of the table from which to get data
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_EditUser.ui'), self)
        self.row_number = row_number
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']


        # Get the values from the table
        first_name = self.table.get_value(row_number, "first_name")
        last_name = self.table.get_value(row_number, "last_name")
        employee_number = self.table.get_value(row_number, "employee_number")
        email = self.table.get_value(row_number, "email")
        user_login = self.table.get_value(row_number, "user_login")
        password = self.table.get_value(row_number, "password")
        admin_priveleges = self.table.get_value(row_number, "admin_priveleges")

        log.info("editing employee : {0}".format(employee_number))

        # Insert the values into the form
        self.ui.TB_FirstName.insert(first_name)
        self.ui.TB_LastName.insert(last_name)
        self.ui.TB_ID.insert(str(employee_number))
        self.ui.TB_Email.insert(email)
        self.ui.TB_UserLogin.insert(user_login)
        self.ui.TB_Password.insert(password)

        # Determine if check box is checked or not
        if bool(admin_priveleges):
            self.ui.CB_Admin.setChecked(True)
        else:
            self.ui.CB_Admin.setChecked(False)

        self.ui.show()

        # Buttons
        self.ui.PB_Confirm.clicked.connect(self.edit_user)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)


    def edit_user(self):
        """
        Method to edit an existing user.
        The old employee number is used to determine which row in the databse to edit.

        """

        # Retrieve the old employee number
        old_employee_num = self.table.get_value(self.row_number, "employee_number")

        # Get all fields from text boxes
        employee_number = self.ui.TB_ID.text()
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        password = self.ui.TB_Password.text()
        user_login = self.ui.TB_UserLogin.text()
        email = self.ui.TB_Email.text()

        # Ensure that the employee number is unique
        if str(employee_number) != str(old_employee_num):
            unique = self.table.check_unique("employee_number", employee_number, int)
            log.warning("Invalid input -> same employee number")
            if unique is None:
                ERRORS.invalid_input(self.tables_dict, self)
                return
            elif not unique:
                ERRORS.employee_number_already_used(self.tables_dict, self)
                return
            else:
                self.table.change_data("employee_number", employee_number, int)
        else:
            self.table.change_data("employee_number", employee_number, int)

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


        # Call table method to edit row at previous employee number
        self.table.edit_row(abs(int(old_employee_num)))
        self.return_to_user_manager()

    def return_to_user_manager(self):
        """
        Method to return to the user managaer screen

        """
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)
