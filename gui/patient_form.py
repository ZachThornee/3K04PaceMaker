import logging as log

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

import errors as ERRORS
import management_screen as MANAGER


class patient_form(QMainWindow):

    def __init__(self, tables_dict, edit_type, management_type, row_number=None):
        """
        Constructor for edit user screen

        :param tables_dict dict: A dictionary containing all tables used in application
        :param row_number int: The current row of the table from which to get data
        """
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_PatientForm.ui'), self)
        self.tables_dict = tables_dict
        self.edit_type = edit_type
        self.table = self.tables_dict['patients_table']
        self.rn = row_number
        self.management_type = management_type

        # Set the font
        font = QtGui.QFont()
        font.setPointSize(26)
        self.LAB_Title.setFont(font)

        # Set the title string
        if self.edit_type == "add":
            self.ui.LAB_Title.setText("Add Patient Form")
            log.info("Adding new user")

        elif self.edit_type == "edit":
            self.edit_patient_setup()

        self.ui.show()

        # Buttons
        self.ui.PB_Confirm.clicked.connect(self.confirm_button)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)

    def edit_patient_setup(self):
        self.ui.LAB_Title.setText("Edit Patient Form")
        # Get the values from the table
        patient_number = self.table.get_value(self.rn, "patient_id")
        first_name = self.table.get_value(self.rn, "first_name")
        last_name = self.table.get_value(self.rn, "last_name")
        healthcard = self.table.get_value(self.rn, "healthcard")
        age = self.table.get_value(self.rn, "age")
        pacemaker_id = self.table.get_value(self.rn, "pacemaker_id")

        log.info("Editing Patient : {0}".format(patient_number))

        # Insert the values into the form
        self.ui.TB_FirstName.insert(first_name)
        self.ui.TB_LastName.insert(last_name)
        self.ui.TB_PatientID.insert(str(patient_number))
        self.ui.TB_Age.insert(str(age))
        self.ui.TB_PacemakerID.insert(str(pacemaker_id))
        self.ui.TB_Healthcard.insert(healthcard)

        # Determine if check box is checked or not
        if self.table.get_value(self.rn, "sex") == "male":
            self.ui.RB_Male.setChecked(True)
            self.ui.RB_Female.setChecked(False)
        else:
            self.ui.RB_Male.setChecked(False)
            self.ui.RB_Female.setChecked(True)

    def confirm_button(self):
        """
        Method to edit an existing user.
        The old employee number is used to determine which row in the databse to edit.

        """
        # Get all fields from text boxes
        first_name = self.ui.TB_FirstName.text()
        last_name = self.ui.TB_LastName.text()
        patient_id = self.ui.TB_PatientID.text()
        age = self.ui.TB_Age.text()
        pacemaker_id = self.ui.TB_PacemakerID.text()
        healthcard = self.ui.TB_Healthcard.text()

        # Change the data in the table
        try:
            self.table.change_data("first_name",    first_name,     str)
            self.table.change_data("last_name",     last_name,      str)
            self.table.change_data("pacemaker_id",  pacemaker_id,   int)
            self.table.change_data("healthcard",    healthcard,     str)
            self.table.change_data("age",           age,            int)

            # Get the value of the checkbox
            if self.ui.RB_Male.isChecked():  # If check box is ticked
                sex = "male"
            else:
                sex = "female"

            self.table.change_data("sex", sex, str)

            # Verify employee number and changes
            if self.edit_type == "edit":
                # Retrieve the old employee number
                old_patient_id = self.table.get_value(self.rn, "patient_id")
                if str(patient_id) != str(old_patient_id):
                    valid_num = self.validate_patient_id(patient_id)
                    if not valid_num:
                        return
                else:
                    self.table.change_data("patient_id", patient_id, int)

                self.table.edit_row(abs(int(old_patient_id)))

            elif self.edit_type == "add":
                valid_num = self.validate_patient_id(patient_id)
                if valid_num:
                    self.table.change_data("patient_id", patient_id, int)
                    self.table.add_row()
        except ValueError:
            ERRORS.invalid_input(self.tables_dict, self)

        self.return_to_user_manager()

    def validate_patient_id(self, patient_id):
        unique = self.table.check_unique("patient_id", patient_id, int)
        if unique is None:
            ERRORS.invalid_input(self.tables_dict, self)
            log.warning("Invalid input")
            return False
        elif not unique:
            ERRORS.employee_number_already_used(self.tables_dict, self)
            log.warning("Invalid input -> same patient id")
            return False
        else:
            self.table.change_data("patient_id", patient_id, int)
            log.debug("Patient id is valid")
            return True

    def return_to_user_manager(self):
        """
        Method to return to the user managaer screen

        """
        self.ui.close()
        MANAGER.manager(self.tables_dict, self.management_type)
