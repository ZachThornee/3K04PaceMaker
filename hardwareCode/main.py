import logging as log
import sys

import initial_login as LOGIN
from PyQt5.QtWidgets import QApplication
import database_management as DBM

# Global configuration
DB_NAME = "3K04_Database"
USER = "postgres"
PASSWORD = "SVictoria99"

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
ADMIN_CREDS = ["0", "'admin'", "'admin'", "'admin'", "'admin'", "'admin'", "TRUE"]



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
DEFAULT_PATIENT = ["0", "'admin'", "'admin'", "'admin'", "'admin'", "0", "0"]


PACEMAKER_TABLE = "pacemaker_info"
PACEMAKER_PARAMS = [
                ["ID", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                ["MODE", "TEXT",  "NOT", "NULL"],
                ["VRP", "FLOAT",  "NOT", "NULL"],
                ["ARP", "FLOAT",  "NOT", "NULL"],
                ["VENT_PULSE_WIDTH", "FLOAT",  "NOT", "NULL"],
                ["VENT_AMPLITUDE", "FLOAT",  "NOT", "NULL"],
                ["ATRIAL_PULSE_WIDTH", "FLOAT",  "NOT", "NULL"],
                ["ATRIAL_AMPLITUDE", "FLOAT", "NOT", "NULL"],
                ["UPPER_RATE", "FLOAT",  "NOT", "NULL"],
                ["LOWER_RATE", "FLOAT",  "NOT", "NULL"],
            ]
DEFAULT_PACEMAKER = ["0", "'admin'", "0", "0", "0", "0", "0", "0", "0", "0"]

# Setup log style
log.basicConfig(format='%(filename)s-%(levelname)s: %(message)s',
                level=log.INFO)


def main():
    """
    Main applicaiton loop

    """
    APP = QApplication([])  # Create the app
    database = DBM.db_manager(USER, DB_NAME, PASSWORD)  # Connect to the database

    # Connect to all tables
    users_table = database.con_table(LOGINS_TABLE, LOGINS_PARAMETERS, ADMIN_CREDS)
    patient_table = database.con_table(PATIENT_TABLE, PATIENT_PARAMETERS, DEFAULT_PATIENT)
    pacemaker_table = database.con_table(PACEMAKER_TABLE, PACEMAKER_PARAMS, DEFAULT_PACEMAKER)

    # Create a dictionary of all relevant tables
    table_dict = {"users_table": users_table,
                  "patients_table": patient_table,
                  "pacemaker_table": pacemaker_table}

    # Login to main screen
    LOGIN.login_screen(table_dict)

    # Allow the application to run seperately
    sys.exit(APP.exec_())


if __name__ == "__main__":
    main()
