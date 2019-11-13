import logging as log

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import initial_login as LOGIN_SCREEN
import user_form as USER_FORM
import patient_form as PATIENT_FORM


class manager(QMainWindow):

    def __init__(self, tables_dict, management_type):
        """
        Constructor for user manager screen

        :param tables_dict dictionary: A dictionary containing all tables
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_ManagementScreen.ui'), self)
        self.tables_dict = tables_dict
        self.management_type = management_type

        # User Manager setup
        if self.management_type == "users":
            self.PB_Add.setText("Add User")
            self.PB_Edit.setText("Edit User")
            self.PB_Delete.setText("Delete User")
            self.table = tables_dict['users_table']
            self.ui.LAB_Title.setText("User Manager")

        elif self.management_type == "patients":
            self.PB_Add.setText("Add Patients")
            self.PB_Edit.setText("Edit Patients")
            self.PB_Delete.setText("Delete Patients")
            self.table = tables_dict['patients_table']
            self.ui.LAB_Title.setText("Patient Manager")

        # Buttons
        self.PB_Back.clicked.connect(self.return_to_login_screen)
        self.PB_Add.clicked.connect(self.add_button)
        self.PB_Edit.clicked.connect(self.edit_button)
        self.PB_Delete.clicked.connect(self.delete_button)

        font = QtGui.QFont()
        font.setPointSize(26)
        self.LAB_Title.setFont(font)

        self.update_table()

    def update_table(self):
        """
        Method to update the QWidgetTable
        """
        self.table.populate(self.ui.TAB_Table)
        self.ui.show()

    def add_button(self):
        """
        Method to validate user count and if valid open add user screen

        """

        if self.management_type == "users":
            if not self.table.check_max_user(10):
                ERRORS.maximum_number_of_users(self.tables_dict, self)
            else:
                self.ui.close()
                USER_FORM.user_form(self.tables_dict, "add", self.management_type)

        elif self.management_type == "patients":
            self.ui.close()
            PATIENT_FORM.patient_form(self.tables_dict, "add", self.management_type)

    def edit_button(self):
        """
        Method to open the edit user screen and to update with user information

        """

        if len(self.ui.TAB_Table.selectedRanges()) == 0:
            log.error("No user selected")
            return False

        selected = self.ui.TAB_Table.selectedRanges()[0]
        row_number = selected.topRow()
        self.ui.close()

        if self.management_type == "users":
            USER_FORM.user_form(self.tables_dict, "edit", self.management_type, row_number)

        elif self.management_type == "patients":
            PATIENT_FORM.patient_form(self.tables_dict, "edit", self.management_type, row_number)

    def delete_button(self):
        """
        Method to delete a user in the table

        """

        if len(self.ui.TAB_Table.selectedRanges()) == 0:
            log.error("No user selected")
            return False

        selected = self.ui.TAB_Table.selectedRanges()[0]
        row_number = selected.topRow()

        if self.management_type == "users":
            employee_number = self.table.get_value(row_number, "employee_number")
            self.table.delete_row(employee_number)

        elif self.management_type == "patients":
            patient_id = self.table.get_value(row_number, "patient_id")
            pacemaker_id = self.table.get_value(row_number, "pacemaker_id")
            self.table.delete_row(patient_id)
            self.tables_dict['pacemaker_table'].delete_row(pacemaker_id)

        self.ui.close()
        self.update_table()

    def return_to_login_screen(self):
        """
        Method to return to the login screen

        """
        LOGIN_SCREEN.login_screen(self.tables_dict)
        self.ui.close()
