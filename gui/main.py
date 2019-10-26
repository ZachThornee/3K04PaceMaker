import logging as log
import sys

import login_screen as MAIN_SCREEN
from PyQt5.QtWidgets import QApplication
import database_management as DBM

# Global configuration
DB_NAME = "3K04_Database"
USER = "jeff"

# User Logins Table Information
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

# Patient Table Information
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

PACEMAKER_TABLE = "pacemaker_info"
PACEMAKER_PARAMS = [
                ["ID", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["MODE", "TEXT",  "NOT", "NULL"],
                ["VRP", "INT",  "NOT", "NULL"],
                ["ARP", "INT",  "NOT", "NULL"],
                ["VENT_PULSE_WIDTH", "INT",  "NOT", "NULL"],
                ["VENT_AMPLITUDE", "INT",  "NOT", "NULL"],
                ["ATRIAL_PULSE_WIDTH", "INT",  "NOT", "NULL"],
                ["ATRIAL_AMPLITUDE", "INT", "NOT", "NULL"],
                ["UPPER_RATE", "INT",  "NOT", "NULL"],
                ["LOWER_RATE", "INT",  "NOT", "NULL"],
            ]

# Setup log style
log.basicConfig(format='%(filename)s-%(levelname)s: %(message)s',
                level=log.INFO)


def main():
    """
    Main applicaiton loop

    """
    APP = QApplication([])  # Create the app
    database = DBM.db_manager(USER, DB_NAME)  # Connect to the database

    # Connect to all tables
    users_table = database.con_table(LOGINS_TABLE, LOGINS_PARAMETERS)
    patient_table = database.con_table(PATIENT_TABLE, PATIENT_PARAMETERS)
    pacemaker_table = database.con_table(PACEMAKER_TABLE, PACEMAKER_PARAMS)

    # Create a dictionary of all relevant tables
    table_dict = {"users_table": users_table,
                  "patients_table": patient_table,
                  "pacemaker_table": pacemaker_table}

    # Login to main screen
    MAIN_SCREEN.login_screen(table_dict)

    # Allow the application to run seperately
    sys.exit(APP.exec_())


if __name__ == "__main__":
    main()
