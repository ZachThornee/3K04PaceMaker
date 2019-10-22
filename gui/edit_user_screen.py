import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER
import errors as ERRORS


class edit_user_screen(QMainWindow):
    def __init__(self, tables_dict, user):
        """
        Constructor for edit user screen

        :param tables_dict dict: A dictionary containing all tables used in application
        :param user dictionary: A dictionary object of the current user
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_EditUser.ui'), self)
        log.info("editing employee : {0}".format(user['employee_number']))

        # Populate the form
        self.ui.TB_FirstName.insert(user['first_name'])
        self.ui.TB_LastName.insert(user['last_name'])
        self.ui.TB_ID.insert(str(user['employee_number']))
        self.ui.TB_Email.insert(user['email'])
        self.ui.TB_UserLogin.insert(user['user_login'])
        self.ui.TB_Password.insert(user['password'])
        if bool(user['admin_priveleges']):
            self.ui.CB_Admin.setChecked(True)
        else:
            self.ui.CB_Admin.setChecked(False)

        self.ui.show()

        # Args
        self.user = user
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']
        self.users_dict = self.table.get_table_dict()

        # Buttons
        self.ui.PB_Confirm.clicked.connect(self.edit_user)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)

        # Unfilled vars
        self.edit_user_list = []

    def edit_user(self):
        """
        Method to edit a user in the database

        """
        # Get the current employee number
        old_employee_num = self.user['employee_number']

        # VITAL: New user does change old user due to table regen on class call

        try:
            # Confirm input is an int and make unsigned else raise ValueError
            valid_num = abs(int(self.ui.TB_ID.text()))

            for user in self.users_dict.values():
                # If our new employee number already exists in database
                if user['employee_number'] == valid_num and user != self.user:
                    log.warning("Invalid input -> same employee number")
                    # Show error dialogue for employee number already used
                    ERRORS.employee_number_already_used(self.tables_dict, self)
                    return
            else:
                self.user['employee_number'] = valid_num

            # Get TEXT type params.
            # VITAL: TEXT params in PostgreSQL require surrounding apostrophes
            self.user['first_name'] = "'{0}'".format(self.ui.TB_FirstName.text())
            self.user['last_name'] = "'{0}'".format(self.ui.TB_LastName.text())
            self.user['password'] = "'{0}'".format(self.ui.TB_Password.text())
            self.user['user_login'] = "'{0}'".format(self.ui.TB_UserLogin.text())
            self.user['email'] = "'{0}'".format(self.ui.TB_Email.text())

            if self.CB_Admin.isChecked():  # If check box is ticked
                self.user['admin_priveleges'] = True
            else:
                self.user['admin_priveleges'] = False

            for value in self.user.values():
                if value == "''":  # If a TEXT type param has no entry
                    raise ValueError
                else:
                    self.edit_user_list.append(str(value))

        except ValueError:
            # Show invalid input dialogue
            ERRORS.invalid_input(self.tables_dict, self)
            return

        # Call table method to edit row at previous employee number
        self.table.edit_row(self.edit_user_list, old_employee_num)
        self.return_to_user_manager()

    def return_to_user_manager(self):
        """
        Method to return to the user managaer screen

        """
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)

