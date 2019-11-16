import logging as log

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import management_screen as MANAGER


class user_form(QMainWindow):

    def __init__(self, tables_dict, edit_type, row_number=None):
        """
        Constructor for edit user screen

        :param tables_dict dict: A dictionary containing all tables used in application
        :param row_number int: The current row of the table from which to get data
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_UserForm.ui'), self)
        self.tables_dict = tables_dict
        self.edit_type = edit_type
        self.table = self.tables_dict['users_table']
        self.rn = row_number

        # Set the font
        font = QtGui.QFont()
        font.setPointSize(26)
        self.LAB_Title.setFont(font)

        # Set the title string
        if self.edit_type == "add":
            self.ui.LAB_Title.setText("Add User Form")
            log.info("Adding new user")

        elif self.edit_type == "edit":
            self.edit_user_setup()

        self.ui.show()

        # Buttons
        self.ui.PB_Confirm.clicked.connect(self.confirm_button)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)

    def edit_user_setup(self):
        self.ui.LAB_Title.setText("Edit User Form")
        # Get the values from the table
        first_name = self.table.get_value(self.rn, "first_name")
        last_name = self.table.get_value(self.rn, "last_name")
        employee_number = self.table.get_value(self.rn, "employee_number")
        email = self.table.get_value(self.rn, "email")
        user_login = self.table.get_value(self.rn, "user_login")
        password = self.table.get_value(self.rn, "password")
        admin_priveleges = self.table.get_value(self.rn, "admin_priveleges")

        log.info("Editing Employee : {0}".format(employee_number))

        # Insert the values into the form
        self.ui.TB_FirstName.insert(first_name)
        self.ui.TB_LastName.insert(last_name)
        self.ui.TB_EmployeeID.insert(str(employee_number))
        self.ui.TB_Email.insert(email)
        self.ui.TB_UserLogin.insert(user_login)
        self.ui.TB_Password.insert(password)

        # Determine if check box is checked or not
        if bool(admin_priveleges):
            self.ui.CB_Admin.setChecked(True)
        else:
            self.ui.CB_Admin.setChecked(False)


    def confirm_button(self):
        """
        Method to edit an existing user.
        The old employee number is used to determine which row in the databse to edit.

        """
        # Get all fields from text boxes
        employee_number = self.ui.TB_EmployeeID.text()
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        password = self.ui.TB_Password.text()
        user_login = self.ui.TB_UserLogin.text()
        email = self.ui.TB_Email.text()

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

        # Verify employee number and changes
        if self.edit_type == "edit":
            # Retrieve the old employee number
            old_employee_num = self.table.get_value(self.self.rn, "employee_number")
            if str(employee_number) != str(old_employee_num):
                valid_num = self.validate_employee_number(employee_number)
                if not valid_num:
                    return
            else:
                self.table.change_data("employee_number", employee_number, int)

            self.table.edit_row(abs(int(old_employee_num)))

        elif self.edit_type == "add":
            valid_num = self.validate_employee_number(employee_number)
            if valid_num:
                self.table.add_row()

        self.return_to_user_manager()

    def validate_employee_number(self, employee_number):
        unique = self.table.check_unique("employee_number", employee_number, int)
        if unique is None:
            ERRORS.invalid_input(self.tables_dict, self)
            log.warning("Invalid input")
            return False
        elif not unique:
            ERRORS.employee_number_already_used(self.tables_dict, self)
            log.warning("Invalid input -> same employee number")
            return False
        else:
            self.table.change_data("employee_number", employee_number, int)
            log.debug("Employee number is valid")
            return True

    def return_to_user_manager(self):
        """
        Method to return to the user managaer screen

        """
        self.ui.close()
        MANAGER.manager(self.tables_dict, self.edit_type)
