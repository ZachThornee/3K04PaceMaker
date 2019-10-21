import logging as log
import sys

import login_screen as MAIN_SCREEN
from PyQt5.QtWidgets import QApplication
import database_management as DBM

# Global configuration
DB_NAME = "3K04_Database"
USER = "jeff"

LOGINS_TABLE = "user_logins"
LOGINS_PARAMETERS = [
                ["EMPLOYEE_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["USER_LOGIN", "TEXT", "NOT", "NULL"],
                ["PASSWORD", "TEXT",  "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT", "NOT", "NULL"],
                ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"],
            ]

PATIENT_TABLE = "patient_info"
PATIENT_PARAMETERS = [
                ["PATIENT_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT",  "NOT", "NULL"],
                ["HEALTHCARD", "TEXT", "NOT", "NULL"],
                ["SEX", "TEXT", "NOT", "NULL"],
                ["AGE", "INT", "NOT", "NULL"],
                ["PACEMAKER_ID", "INT", "NOT", "NULL"],
            ]

log.basicConfig(format='%(filename)s-%(levelname)s: %(message)s',
                level=log.INFO)


def main():
    APP = QApplication([])
    database = DBM.db_manager(USER, DB_NAME)
    users_table = database.con_table(LOGINS_TABLE, LOGINS_PARAMETERS)
    patient_table = database.con_table(PATIENT_TABLE, PATIENT_PARAMETERS)
    table_dict = {"users_table": users_table,
                  "patients_table": patient_table}
    MAIN_SCREEN.login_screen(table_dict)
    sys.exit(APP.exec_())


if __name__ == "__main__":
    main()
