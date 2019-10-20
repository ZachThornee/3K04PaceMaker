import logging as log

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import user_manager_screen as USER_MANAGER


class edit_user_screen(QMainWindow):
    def __init__(self, tables_dict, user):
        super().__init__()
        self.ui = uic.loadUi(('ui_files/UF_EditUser.ui'), self)
        log.info("editing user : {0}".format(user['employee_number']))
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
        self.user = user
        self.tables_dict = tables_dict
        self.table = self.tables_dict['users_table']
        self.users_dict = self.table.get_table_dict()
        self.ui.PB_Confirm.clicked.connect(self.edit_user)
        self.ui.PB_Cancel.clicked.connect(self.return_to_user_manager)
        self.edit_user_list = []

    def edit_user(self):
        old_employee_num = self.user['employee_number']

        try:
            valid_num = abs(int(self.ui.TB_ID.text()))
            self.user['employee_number'] = str(valid_num)
        except ValueError:
            log.warning("Invalid user input")

        for user in self.users_dict.values():
            if user['employee_number'] == self.user['employee_number']:
                log.warning("Invalid input -> same employee number")

        self.user['first_name'] = "'{0}'".format(self.ui.TB_FirstName.text())
        self.user['last_name'] = "'{0}'".format(self.ui.TB_LastName.text())
        self.user['password'] = "'{0}'".format(self.ui.TB_Password.text())
        self.user['user_login'] = "'{0}'".format(self.ui.TB_UserLogin.text())
        self.user['email'] = "'{0}'".format(self.ui.TB_Email.text())

        if self.CB_Admin.isChecked():
            self.user['admin_priveleges'] = True
        else:
            self.user['admin_priveleges'] = False

        for value in self.user.values():
            self.edit_user_list.append(str(value))

        self.table.edit_row(self.edit_user_list, old_employee_num)
        self.return_to_user_manager()

    def return_to_user_manager(self):
        self.ui.close()
        USER_MANAGER.user_manager_screen(self.tables_dict)

