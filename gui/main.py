import logging as log
import sys

import login_screen as MAIN_SCREEN
from PyQt5.QtWidgets import QApplication

# Global configuration
DB_NAME = "3K04_Database"
USER = "jeff"

LOGINS_TABLE = "user_logins"
LOGINS_TABLE_PARAMETERS = [
                ["EMPLOYEE_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["USER_LOGIN", "TEXT", "NOT", "NULL"],
                ["PASSWORD", "TEXT",  "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT", "NOT", "NULL"],
                ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"],
                ["EMAIL", "TEXT", "NOT", "NULL"]
            ]

PATIENT_TABLE = "patient_info"
PATIENT_LOOKUP_PARAMETERS = [
                ["PATIENT_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                ["LAST_NAME", "TEXT",  "NOT", "NULL"],
                ["HEALTHCARD", "TEXT", "NOT", "NULL"],
                ["SEX", "TEXT", "NOT", "NULL"],
                ["AGE", "INT", "NOT", "NULL"],
                ["PACEMAKER_ID", "INT", "NOT", "NULL"],
            ]

TABLE_DICTIONARY = {LOGINS_TABLE: LOGINS_TABLE_PARAMETERS,
                    PATIENT_TABLE: PATIENT_LOOKUP_PARAMETERS}

log.basicConfig(format='%(filename)s-%(levelname)s: %(message)s',
                level=log.INFO)

if __name__ == "__main__":
    APP = QApplication([])
    window = MAIN_SCREEN.login_screen(USER, DB_NAME, LOGINS_TABLE, TABLE_DICTIONARY)
    sys.exit(APP.exec_())
