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
        user_dict = self.table.get_table_dict()  # Get the users dictionary
        new_user = user_dict[0]  # Use the first user as a template

        # VITAL: New user does change old user due to table regen on class call

        try:
            # Confirm input is an int and make unsigned else raise ValueError
            valid_num = abs(int(self.ui.TB_EmployeeID.text()))

            for user in user_dict.values():
                # If our new employee number already exists in database
                if user['employee_number'] == valid_num:
                    log.warning("Invalid input -> same employee number")
                    # Show error dialogue for employee number already used
                    ERRORS.employee_number_already_used(self.tables_dict, self)
                    return
            else:
                new_user['employee_number'] = valid_num

            # Get TEXT type params.
            # VITAL: TEXT params in PostgreSQL require surrounding apostrophes
            new_user['first_name'] = "'{0}'".format(self.ui.TB_FirstName.text())
            new_user['last_name'] = "'{0}'".format(self.ui.TB_LastName.text())
            new_user['password'] = "'{0}'".format(self.ui.TB_Password.text())
            new_user['user_login'] = "'{0}'".format(self.ui.TB_UserLogin.text())
            new_user['email'] = "'{0}'".format(self.ui.TB_Email.text())

            if self.CB_Admin.isChecked():  # If check box is ticked
                new_user['admin_priveleges'] = True
            else:
                new_user['admin_priveleges'] = False

            new_user_list = []
            for value in new_user.values():
                if value == "''":  # If a TEXT type param has no entry
                    raise ValueError
                else:
                    new_user_list.append(str(value))

        except ValueError:
            # Show invalid input dialogue
            ERRORS.invalid_input(self.tables_dict, self)
            return

        # Call table method to add new row
        self.table.add_row(new_user_list)
        self.return_to_user_manager()

    def return_to_user_manager(self):
        """
        Method to return to user manager screen

        """
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)
